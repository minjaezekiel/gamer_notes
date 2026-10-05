# Lesson 11 — Saving And Loading

> **Web Games · Intermediate level · Lesson 11 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A game that **remembers**: a top-ten high score table with names, settings that survive a reload, and a
full save of the game in progress that can be loaded back — including a save file from an *older version
of your own game*, which is the part real games get wrong.

```
  ┌─ HIGH SCORES ──────────┐     ┌─ SETTINGS ─────────┐
  │  1.  Ada        4,200  │     │  volume     ████··  │
  │  2.  Kwame      3,850  │     │  shake      on      │
  │  3.  Yuki       3,100  │     │  controls   WASD    │
  └────────────────────────┘     └─────────────────────┘
        survives a reload              survives a reload
```

And you will handle the three things that will otherwise break it: storage that **throws**, data that
has been **edited by the player**, and a save written by a **previous version** of your game.

## Where this fits

- **Back:** [lesson 7](../lesson-07-scenes-properly/notes.md) built the screens that need saving;
  [lesson 9](../lesson-09-particles-and-juice-engineering/notes.md) built settings worth remembering.
- **Forward:** the [capstone](../lesson-12-capstone-a-platformer/notes.md) saves which level you reached.
- **Other tracks:** the Python beginner capstone already wrote a high score to a file, and Python's
  advanced lesson 3 goes much further with JSON. C++'s advanced lesson 8 saves a seed instead of a world,
  which is a genuinely different idea worth meeting.

---

## The idea, in plain words

### A browser gives you a small, permanent box of text

```js
localStorage.setItem("highScore", "4200");
const score = localStorage.getItem("highScore");    // "4200" — a STRING
localStorage.removeItem("highScore");
```

Four facts about that box, and each of them will matter today:

1. **It stores strings and nothing else.** Put a number in, get a string out. `"4200" + 1` is
   `"42001"`, which is a bug that looks like arithmetic having gone wrong.
2. **It is per origin.** Your game at `localhost:8000` and the same game at `file://` have *separate*
   storage, which is confusing the first time you notice it.
3. **It is small** — about 5 MB. Enormous for a save file, nothing for images.
4. **It can throw.** Not return `null`: *throw*. More on that in a moment, because it is the single most
   important thing in this lesson.

### Objects go in as text, and come back slightly different

Storage holds strings, so an object has to become text first:

```js
const save = { level: 3, score: 1200, unlocked: [1, 2, 5] };
localStorage.setItem("save", JSON.stringify(save));          // object → text

const text = localStorage.getItem("save");
const loaded = JSON.parse(text);                             // text → object
```

That works, and it is lossy in ways nothing warns you about:

| What you saved | What comes back |
|---|---|
| a number, string, boolean | the same |
| an array, a plain object | the same |
| **a function / method** | **the key disappears entirely** |
| **`undefined`** | **the key disappears** |
| **`Infinity` or `NaN`** | **`null`** |
| **a `Date`** | **a string that looks like a date** |
| **a `Map` or `Set`** | **`{}`** — an empty object |
| **a circular reference** | throws (the only one that complains) |

Only the last one tells you anything is wrong. The rest come back quietly different, and you find out
later when the player's dash is missing or their best time is `null`.

The rule that follows is short: **save only plain numbers, strings, booleans, arrays and plain
objects.** If you want a `Set`, save an array and rebuild the `Set` on load. If you want a date, save
`Date.now()` — a plain number.

### `localStorage` throws, and this is the bug that will bite you

This is not a theoretical risk. In a private window, or with site data blocked, or in some embedded
browsers, **even reading** `localStorage` raises an exception:

```js
// This line can throw. Not return null. THROW.
const data = localStorage.getItem("save");
```

An uncaught exception at the top of your startup code means your game **does not start at all**, for
that player, and you will probably never see it happen because it works perfectly on your machine.

So every single access is wrapped, and the game works without storage:

```js
/* The whole storage layer. Six lines, and your game can no longer be broken by
   somebody's privacy settings. */
const Store = {
  available: false,

  init: function () {
    try {
      localStorage.setItem("__test", "1");
      localStorage.removeItem("__test");
      this.available = true;
    } catch (err) {
      this.available = false;       // and that is FINE. Carry on.
    }
  },

  load: function (key, fallback) {
    if (!this.available) { return fallback; }
    try {
      const text = localStorage.getItem(key);
      if (text === null) { return fallback; }
      return JSON.parse(text);
    } catch (err) {
      return fallback;              // unreadable or corrupt: use the default
    }
  },

  save: function (key, value) {
    if (!this.available) { return false; }
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (err) {
      return false;                 // full, or blocked. Say so, do not crash.
    }
  }
};
```

Notice `load` takes a **fallback**. Every load site therefore has to say what it wants when there is no
save, which means a missing save is never a special case.

### Never trust what comes back

Three completely different reasons the data you load might be wrong:

1. **The player edited it.** `localStorage` is visible and editable in every browser's developer tools.
   A fourteen-year-old will find it within a week of you telling them not to.
2. **An older version of your game wrote it.** You renamed `hp` to `health` last month. The save on
   their machine still says `hp`.
3. **It is corrupt.** The tab was closed mid-write, or storage was full, so the text is half an object.

So loading is not "parse it and use it". It is **parse it, check it, repair it**:

```js
function loadSettings() {
  const raw = Store.load("settings", {});
  /* Build a clean object from scratch, taking only what is valid. Anything
     missing or absurd falls back to a default, so there is no path by which a
     bad save can put the game into a state it cannot run in. */
  return {
    volume: clampNumber(raw.volume, 0, 1, 0.3),
    shake: typeof raw.shake === "boolean" ? raw.shake : true,
    scheme: (raw.scheme === "wasd" || raw.scheme === "arrows") ? raw.scheme : "arrows"
  };
}

function clampNumber(value, lo, hi, fallback) {
  if (typeof value !== "number" || !isFinite(value)) { return fallback; }
  return Math.max(lo, Math.min(hi, value));
}
```

That is more code than `return JSON.parse(text)`, and it is the difference between a game that survives
contact with real people and one that does not. The useful way to think about it: **data from storage is
input, and all input is untrusted** — exactly like something typed into a box.

### Versioning, so last month's save still loads

Write a version number into every save from the very first day:

```js
const SAVE_VERSION = 3;

function makeSave(game) {
  return {
    version: SAVE_VERSION,
    level: game.level,
    score: game.score,
    health: game.health
  };
}
```

Then **migrate** on load, one version at a time:

```js
function migrate(save) {
  /* Each block upgrades by exactly one step, and they run in order. Writing them
     as a chain means you only ever have to think about one version gap. */
  if (save.version === 1) {
    save.health = save.hp;          // we renamed it
    delete save.hp;
    save.version = 2;
  }
  if (save.version === 2) {
    save.unlocked = [1];            // a field that did not exist before
    save.version = 3;
  }
  if (save.version !== SAVE_VERSION) {
    return null;                    // from the FUTURE, or unrecognisable
  }
  return save;
}
```

The `null` case matters and is easy to forget: a save from a *newer* version of your game is not
something you can repair, so the honest answer is "I cannot read this", followed by starting fresh with
a message. A game that silently loads a future save and then behaves oddly is worse.

### When to save

**Not every frame.** Writing to storage is slow compared with everything else in your loop, and sixty
writes a second will produce a visible stutter.

Save on **events that matter**: finishing a level, changing a setting, dying, closing the tab. If you
want an autosave, put a timer on it:

```js
let saveTimer = 0;

function update(dt) {
  saveTimer += dt;
  if (saveTimer > 10) {           // at most once every ten seconds
    saveTimer = 0;
    Store.save("save", makeSave(game));
  }
}
```

And one worth knowing about: the tab closing.

```js
/* visibilitychange is the reliable one. "beforeunload" is unreliable on mobile,
   where a tab can be discarded without it ever firing. */
document.addEventListener("visibilitychange", function () {
  if (document.visibilityState === "hidden") {
    Store.save("save", makeSave(game));
  }
});
```

### What not to save

- **Anything you can work out again.** The number of coins left in the level is `coins.filter(alive)`.
  Saving it means you now have two answers to one question, and one day they will disagree.
- **References to objects.** `{ target: thatEnemy }` becomes a *copy* of the enemy in JSON, so on load
  you have two enemies, one of which nothing can see.
- **The whole game object.** It has the canvas in it, and functions, and everything else. Write a
  deliberate `makeSave()` that lists exactly what is worth keeping. That list is also documentation of
  what your game's state actually *is*, which is a surprisingly useful thing to have written down.

---

## The idea, in pictures

Open [what survives a save](../../../shared/visualizers/save-round-trip.html).

**What to look for:** press **Step 1 frame** four times to walk one object through stringify, storage and
parse. Then read the right-hand column. Six of the ten values come back as something other than what went
in, and **not one of them produced an error**. The method was dropped, the `undefined` disappeared,
`Infinity` became `null`, and the date is now a string that looks like a date. Only the circular reference
complained — and it complained at save time, not load time, which is the wrong end.

---

## The idea, in code

1. `code/01-storage-that-cannot-crash.html` — the `Store` wrapper, with a switch that simulates storage
   being blocked so you can watch the game carry on working.
2. `code/02-what-json-keeps.html` — a round trip of every awkward value, side by side, with what came
   back. Add your own values to the list.
3. `code/03-high-scores.html` — a top-ten table with names, sorted, persisted, and validated on load.
   There is a button that corrupts the save on purpose.
4. `code/04-save-and-migrate.html` — a small game with a full save, and buttons that write a version 1
   and a version 2 save so you can watch the migration chain run.

---

## The maths you just used

Almost none, and it is worth saying so rather than inventing some. Two small things:

**1. Clamping, again.** `Math.max(lo, Math.min(hi, v))` appears in every validator, and it is the same
clamp from lesson 3 and lesson 6 doing a third job. The addition here is the type check *before* the
clamp: `Math.min(1, "banana")` is `NaN`, and `NaN` passes straight through a clamp without complaint.

**2. Sorting, and the comparator.** A high score table needs

```js
scores.sort(function (a, b) { return b.score - a.score; });    // highest first
```

`sort` wants a function that returns a negative number, zero, or a positive number. `b - a` is
descending and `a - b` is ascending, and mixing them up is a one-character bug with a very visible
result. Note that `sort` **changes the array in place** and returns it, which surprises people, and that
sorting an array of strings with no comparator sorts them as *text* — so `"100"` comes before `"99"`.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Read a saved number and add 1 to it, without `Number()` | | |
| Save an object containing a method, then call that method after loading | | |
| Save `Infinity` as a best time, then compare against it | | |
| Save a `Set` of unlocked levels and check its `.size` after loading | | |
| Open the game in a **private window** with the `try`/`catch` removed | | |
| Edit the save in devtools to `{"score": "banana"}` and load it | | |
| Delete the `version` field from the migration chain's input | | |
| Save every frame instead of on events, then watch the frame-time graph | | |
| Sort the high scores with `a.score - b.score` | | |

The private window one is the most important thing in this lesson, and it is worth actually doing: your
game does not load, in a way you would otherwise never see.

---

## Think like an engineer

1. A high score table stores a name typed by the player. What could go in that box that you would not
   want in your table? List five things, then say what you would do about each.
2. Your save contains `level: 3`. A player edits it to `level: 99`, which does not exist. What should the
   game do? Now: they edit `score` to 999999. Is that the same kind of problem, and does it deserve the
   same answer?
3. **Design something.** Three save slots, each showing the level, score and when it was last played, so
   the player can choose. What do you store, and what do you store it *under*? What happens when the
   player overwrites a slot — do you ask first?
4. **The hard one.** C++'s advanced level saves a **seed** rather than a world: instead of storing every
   tile of a generated dungeon, it stores the one number the generator started from, and rebuilds it.
   That save is a few bytes instead of a megabyte. What has to be true of your generator for that to
   work? And what breaks the moment you change the generator?

---

## Vocabulary

| Word | What it means |
|---|---|
| **`localStorage`** | A small permanent store of strings, per origin. |
| **Origin** | Protocol + host + port. `file://` and `localhost` have separate storage. |
| **`JSON.stringify` / `.parse`** | Object → text, and text → object. |
| **Lossy** | Some things do not survive the round trip, silently. |
| **Validation** | Checking loaded data and repairing it before use. |
| **Save version** | A number in every save, so old ones can be upgraded. |
| **Migration** | Code that upgrades a save by one version at a time. |
| **Quota** | The storage limit, about 5 MB. Exceeding it throws. |
| **Debounce** | Doing something at most once per interval, however often it is asked for. |
| **Derived value** | Something you could work out again. Do not save it. |

---

## Recap

- `localStorage` holds **strings only**, is **per origin**, holds about **5 MB**, and **can throw** — so
  wrap every access and give the game a working fallback.
- JSON is **lossy and silent**. Save only numbers, strings, booleans, arrays and plain objects.
- **Loaded data is untrusted input.** Validate every field against a default; build a clean object rather
  than using what you were given.
- Put a **version** in every save from day one, and migrate **one step at a time**. Refuse a save from
  the future.
- Save on **events**, not every frame, plus `visibilitychange` for the tab closing.
- Do not save anything you can **work out again**, and never save references.

---

## Stretch goals

1. **Export and import.** A text box showing the save as JSON, which the player can copy out and paste
   back. Ten lines, and you have just built save sharing — and a cheating device, which is a good
   conversation.
2. **A checksum.** Add a simple hash of the save's contents, and refuse a save whose hash does not match.
   It stops casual editing and not determined editing, which is an honest and useful thing to understand
   about security.
3. **Three slots** (question 3).
4. **A settings screen** that writes immediately on every change, pushed onto your lesson 7 scene stack.
5. **Deliberate corruption.** Write a button that damages the save in five different ways — truncated,
   wrong types, missing fields, a future version, not JSON at all — and make sure all five load without
   crashing.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Open `03-high-scores.html`, set a high score, reload the page: it is still there. Then open devtools, edit the score to `"banana"`, and reload. Discuss what *should* happen. |
| 10–25 | **Concept.** The round-trip visualizer, mostly on the right-hand column. Then the `Store` wrapper on the board, and the private-window problem. |
| 25–40 | **Live-code** `Store.load` and `Store.save` with the try/catch and the fallback. Short, and the most reusable twenty lines in the lesson. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–4 are the core; 5 onwards is the validation work, which is where the real content is. |
| 120–140 | **Break-each-other's-saves.** Pair them up and let each student corrupt their partner's save in devtools. Whoever's game survives everything wins. This is the most effective twenty minutes in the lesson. |
| 140–150 | Recap. Lesson 12 is the capstone. |

**Before the lesson:** check that your classroom browsers allow `localStorage`. Some locked-down school
profiles block site data entirely, which — if you have taught the try/catch — is a brilliant live
demonstration, and if you have not, is thirty students whose games do not start.

**What usually goes wrong**

1. **`"4200" + 1` is `"42001"`.** Strings out of storage. Very common, and it looks like arithmetic
   breaking.
2. **No try/catch**, and it works perfectly all lesson, because nobody is in a private window. Make them
   test in one. This is the one failure they cannot find by playing.
3. **A method disappears after a save/load round trip** and `TypeError: x.dash is not a function`
   appears somewhere unrelated.
4. **Saving every frame**, then wondering why the game stutters.
5. **`JSON.parse(null)`** when there is no save yet. `JSON.parse(null)` actually returns `null` rather
   than throwing, which is worse — the bug surfaces later as "cannot read properties of null".
6. **Trusting the save.** A student edits their own save to test it, the game breaks, and they conclude
   they should not have edited it. Reframe it: a player *will*, and the game has to cope.
7. **Version added later.** A save with no `version` field is the one case the migration chain cannot
   handle gracefully unless you treat `undefined` as version 1. Worth putting in from the start.

**If you are running short on time** — cut migration and `code/04`; a single-version save is fine for a
first game. Do **not** cut the try/catch or the validation: those are the two things that distinguish a
save system that works from one that works on your machine.

**For the student who finishes at minute 90** — stretch goal 1 (export/import as text) takes ten minutes
and leads naturally to stretch goal 2 and a genuinely interesting discussion about why you cannot stop a
determined player from cheating in a game that runs on their computer.

**The point to land at the end:** the saving was five lines. Everything else today was about not trusting
the result — because a save file is the only part of your program written by somebody else, at a time you
cannot control, possibly by a previous version of you.
