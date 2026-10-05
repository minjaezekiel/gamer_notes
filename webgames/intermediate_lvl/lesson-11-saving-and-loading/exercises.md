# Lesson 11 — Saving And Loading

## Cheat sheet

### Four facts

1. **strings only** — `getItem` always returns a string or `null`
2. **per origin** — `file://` and `localhost:8000` have separate storage
3. **about 5 MB**
4. **it can THROW** — in a private window, even reading

### The whole storage layer

```js
const Store = {
  available: false,
  init() {
    try {
      localStorage.setItem("__t", "1");
      localStorage.removeItem("__t");
      this.available = true;
    } catch (e) { this.available = false; }
  },
  load(key, fallback) {
    if (!this.available) return fallback;
    try {
      const t = localStorage.getItem(key);
      if (t === null) return fallback;
      return JSON.parse(t);
    } catch (e) { return fallback; }
  },
  save(key, value) {
    if (!this.available) return false;
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) { return false; }
  }
};
```

Every load takes a **fallback**, so "no save" is never a special case.

### JSON is lossy and silent

| in | out |
|---|---|
| number, string, boolean | same |
| array, plain object | same |
| function | **key gone** |
| `undefined` | **key gone** |
| `Infinity`, `NaN` | **`null`** |
| `Date` | a **string** |
| `Map`, `Set` | **`{}`** |
| circular | throws |

Save only numbers, strings, booleans, arrays, plain objects.

### Loaded data is untrusted input

```js
return {
  volume: clampNumber(raw.volume, 0, 1, 0.3),
  shake: typeof raw.shake === "boolean"
           ? raw.shake : true
};
```

Build a **clean** object. Check the type *before* clamping — `Math.min(1,
"banana")` is `NaN` and sails straight through.

### Version from day one

```js
if (save.version === 1) { /* 1 → 2 */ save.version = 2; }
if (save.version === 2) { /* 2 → 3 */ save.version = 3; }
if (save.version !== SAVE_VERSION) return null;  // from the future
```

One step at a time. Treat a missing `version` as 1.

### When

On events, plus:

```js
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") saveNow();
});
```

**Never every frame.**

### Do not save

derived values · references to objects · the whole game object

---

## Section A — Recall

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">A1.</span> Give the four facts about <code>localStorage</code>, and say which one would stop a game from starting at all.
<div class="lines"><i></i><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Name three kinds of value that do not survive <code>JSON.stringify</code>, and say what each becomes.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Give three completely different reasons the data you load might not be what you saved.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why does <code>Store.load</code> take a <em>fallback</em> argument?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why migrate one version at a time instead of writing one function that handles every old format? What should happen to a save from a <em>newer</em> version?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why should you not save the number of coins remaining in a level?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> Why not save on every frame, and when should you save instead?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> What is printed, and why?

```js
localStorage.setItem("score", 4200);
console.log(localStorage.getItem("score") + 1);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What does <code>loaded</code> contain? Be precise about every key.

```js
const save = { hp: 100, best: Infinity, when: new Date(),
               seen: new Set([1, 2]), heal: function () {} };
const loaded = JSON.parse(JSON.stringify(save));
```

<div class="lines"><i></i><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> There is no save yet. What does this produce, and when does the problem actually show up?

```js
const save = JSON.parse(localStorage.getItem("save"));
console.log(save.level);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> The player has edited the save to <code>{"volume": "loud"}</code>. What does <code>volume</code> end up as?

```js
const volume = Math.max(0, Math.min(1, raw.volume));
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> A save has <code>version: 1</code> and the chain handles 1&rarr;2 and 2&rarr;3. Walk through what happens. Now the save has <code>version: 5</code> and <code>SAVE_VERSION</code> is 3 &mdash; what happens then?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The game works perfectly for the author and does not start at all for one of their friends. No error is ever reported to the author.

```js
const settings = JSON.parse(localStorage.getItem("settings"));
startGame(settings);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> After loading a save, <code>TypeError: player.dash is not a function</code> appears &mdash; but only in games that were loaded, never in new ones.

```js
const player = { x: 0, dash: function () { /* ... */ } };
Store.save("player", player);
// next session:
const player = Store.load("player", {});
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The high score table shows 9, 850, 92, 1000 in that order.

```js
scores.sort();
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The best time is displayed as "null" after the first game, and every later comparison against it fails.

```js
let best = Infinity;
if (time < best) { best = time; }
Store.save("best", best);     // on the very first run, before any game
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> The game stutters about once a second, and the frame-time graph shows a spike each time.

```js
function update(dt) {
  movePlayer(dt);
  Store.save("save", makeSave(game));
}
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write the <code>Store</code> wrapper with <code>init</code>, <code>load</code> and <code>save</code>. Show <code>Store.available</code> on screen. Then open your game in a private window and check it still runs.</li>
<li><strong>Checkpoint 2.</strong> Save and restore one number &mdash; a high score. Prove the string problem to yourself by adding 1 to it before you convert it.</li>
<li><strong>Checkpoint 3.</strong> Save a settings object: volume, a toggle, and a control scheme. Change them, reload, confirm they stick.</li>
<li><strong>Checkpoint 4.</strong> Write a validator for those settings that builds a clean object from defaults. Then edit the save in devtools to something absurd and confirm the game still starts with sensible values.</li>
<li><strong>Checkpoint 5.</strong> Build a top-ten high score table with names. Sort it correctly, keep ten, and validate every entry on load (a name must be a string; a score must be a finite number).</li>
<li><strong>Checkpoint 6.</strong> Add a <code>version</code> to your save and a migration chain. Then hand-write an old-format save into storage and watch it upgrade.</li>
<li><strong>Checkpoint 7.</strong> Save on events plus <code>visibilitychange</code>, and show on screen when the last save happened. Confirm you are not saving every frame.</li>
<li><strong>Checkpoint 8.</strong> Add a &ldquo;corrupt my save&rdquo; button that damages it five different ways: truncated text, wrong types, missing fields, a future version, and not JSON at all. All five must load without crashing.</li>
</ul>

<div class="note">
<span class="note-label">The test that matters</span>
<p>Open your game in a private browsing window. If it does not start, you have the
bug this whole lesson exists to prevent &mdash; and it is the one bug you will never
find by playing your own game normally.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** A high score table stores a name the player typed. List five things somebody
might put in that box that you would not want in your table, and say what you would
do about each.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

**E2.** A player edits their save so `level: 99`, which does not exist. What should
the game do? Now they edit `score: 999999`. Same kind of problem? Same answer?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design three save slots, each showing level, score and when it was last
played. What do you store, and under what keys? What happens when a slot is
overwritten — do you ask first?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. Instead of saving every tile of a generated dungeon, save the
**seed** the generator started from and rebuild it. A few bytes instead of a
megabyte. What has to be true of your generator for that to work? What breaks the
moment you change the generator?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Export and import the save as text the player can copy. (Also a cheating device
   — worth discussing.)
2. A checksum that refuses an edited save. Honest about what it does and does not stop.
3. Three save slots (E3).
4. A settings scene pushed onto your lesson 7 stack, writing on every change.
5. The five-way corruption button, and surviving all of it.
