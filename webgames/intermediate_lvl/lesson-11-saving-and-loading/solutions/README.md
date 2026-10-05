# Lesson 11 — Solutions and marking notes

---

## Section A

**A1.** [4] Strings only · per origin · about 5 MB · **it can throw**. Three marks for the four facts (one
mark per two facts, or use judgement). One mark for identifying the throwing as the one that stops a game
starting, because an uncaught exception in startup code ends everything.

**A2.** [3] Any three, one mark each: a **function** → the key disappears · **`undefined`** → the key
disappears · **`Infinity`/`NaN`** → `null` · a **`Date`** → a string · a **`Map`/`Set`** → `{}` · a
**circular reference** → throws.

**A3.** [3] The **player edited it** (storage is visible and editable in devtools) · an **older version of
the game wrote it** (fields renamed, fields added) · it is **corrupt** (interrupted write, or storage
full). One mark each.

**A4.** [2] So that every load site has to say what it wants when there is nothing stored — one mark —
which means a missing save is never a special case and there is no path where `undefined` leaks into the
game — one mark.

**A5.** [3] Because each migration block then only has to handle a gap of one version, so adding version 4
means writing one new block rather than revisiting everything — two marks. A save from the future cannot be
repaired, so the honest answer is to refuse it and start fresh with a message — one mark.

**A6.** [2] It is a **derived value**: it can be worked out from the coins that are still alive — one mark.
Saving it means two answers to one question, and one day they will disagree — one mark.

**A7.** [2] Writing to storage is slow compared with everything else in the loop, and sixty writes a second
causes a visible stutter — one mark. Save on events that matter — finishing a level, changing a setting,
dying — plus `visibilitychange` for the tab being hidden — one mark.

---

## Section B

**B1.** [3] `"42001"`. Two marks. Because `getItem` returns the **string** `"4200"`, and `+` with a string
concatenates — one mark. Fix: `Number(localStorage.getItem("score"))`.

**B2.** [4] `{ hp: 100, best: null, when: "2026-..." }` — a string. `seen` becomes `{}`. `heal` is
**absent entirely**. One mark each for `best`, `when`, `seen` and `heal`; `hp` is free.

The important observation, worth a bonus mark: no error was produced anywhere.

**B3.** [3] `localStorage.getItem` returns `null`, and `JSON.parse(null)` returns **`null`** rather than
throwing — two marks. So the failure is deferred: `save.level` then throws "cannot read properties of
null", on a line that has nothing to do with saving — one mark.

That deferral is what makes it worth asking. The bug appears somewhere innocent.

**B4.** [3] `Math.min(1, "loud")` is `NaN`, and `Math.max(0, NaN)` is also `NaN`, so `volume` is **`NaN`**
— two marks. The clamp did not reject it; a clamp has no opinion about types, so the type check has to come
first — one mark.

**B5.** [3] Version 1: the first block runs (1→2), then the second runs (2→3), then the version matches
`SAVE_VERSION` and the save is returned, upgraded. Two marks. Version 5: neither block runs, the version
does not match 3, so it returns `null` and the game starts fresh — one mark.

---

## Section C

**C1.** [4] Two faults, and they compound. (a) No try/catch, so in a private window — or with site data
blocked — `getItem` **throws** and the game never starts. Two marks. (b) `JSON.parse(null)` returns `null`
on a first run, so `startGame(null)` is also broken. One mark. The author never sees either because it
works on their machine with a save already present — one mark, and this is the half worth drawing out.

**C2.** [3] `JSON.stringify` drops functions, so the saved `player` has an `x` and no `dash` — two marks.
Fix: save only **data** and rebuild behaviour on load — `Object.assign(makePlayer(), Store.load(...))`, or
better, a deliberate `makeSave()` listing the fields worth keeping — one mark.

**C3.** [3] `sort()` with no comparator converts everything to **strings** and sorts alphabetically, so
`"1000"` comes before `"92"` because `"1"` is before `"9"` — two marks. Fix:
`scores.sort(function (a, b) { return b - a; })` for highest first — one mark.

**C4.** [4] `Infinity` becomes `null` in JSON — two marks. Every later `time < null` comparison is a
comparison against 0, so no time is ever better and the best never updates — one mark. Fix: do not save
`Infinity`; either store nothing until there is a real time and use the fallback, or use a plainly absurd
large number and document it — one mark.

**C5.** [3] A full save on every frame, which means a `stringify` plus a storage write sixty times a second
— two marks. Fix: save on events, or debounce to at most once every few seconds — one mark.

---

## Section D — marking the build

1. **`Store.available` is on screen** (checkpoint 1), and they tested in a **private window**. This is the
   one thing in the lesson they cannot verify by normal play, so it is worth asking them to show you.
2. **The validator builds a clean object** (checkpoint 4) rather than patching the loaded one. Test it
   yourself: edit their save in devtools to `{"volume": "banana", "shake": 7}` and launch the game.
3. **The high score sort has a comparator** (checkpoint 5).
4. **The migration actually ran** (checkpoint 6) from a hand-written old save.
5. **Checkpoint 8, all five corruptions.** Do them yourself, on their machine, without warning. If the game
   survives all five, they have built a save system that will survive real players.

The pairing exercise in the teacher notes is worth the time: students are far more inventive about
breaking somebody else's save than their own.

---

## Section E — marking notes

**E1.** Five things, and the responses matter more than the list:

- **Nothing at all** (an empty name) → substitute a default such as "Anonymous"; never store an empty
  string that will render as a blank row.
- **Something enormously long** → cap the length, and cap it *before* saving, not when drawing.
- **HTML or a `<script>` tag** → if you render names with `innerHTML` you have just let the player run code
  in their own page, and if your game is ever on a shared leaderboard, in *other people's* pages. Use
  `textContent`, or draw it on the canvas, which is immune. This is the one worth most credit.
- **Something offensive** → a word filter, which is imperfect; or initials only, which is why arcade
  machines asked for three letters.
- **Characters your font cannot draw** (emoji, other scripts) → decide deliberately: allow them and test,
  or restrict the character set and say so.

Full marks need the `innerHTML` point or an equivalent recognition that a name is untrusted text, not just
awkward text.

**E2.** They are **not** the same kind of problem, and seeing why is the point.

- `level: 99` is **impossible**: there is no such level, so the game cannot do anything sensible. It must
  be rejected — clamp to the highest real level, or refuse the save.
- `score: 999999` is **possible but improbable**. The game runs perfectly well; the player has only cheated
  themselves. Nothing has to be fixed for the program to work.

So the rule: validate for **what would break the game**, not for **what would be unfair**. Fairness is only
enforceable where the server holds the truth, and in a game running entirely on the player's machine there
is no server and no truth. Credit anyone who reaches that, and strongly credit anyone who adds that a
shared online leaderboard changes the answer completely, because now one player's cheating affects others.

**E3.** A reasonable design:

- keys `save1`, `save2`, `save3`, plus a small `saveIndex` object holding just the summary of each so the
  menu can be drawn **without parsing three full saves**;
- each save holds level, score, health and `savedAt: Date.now()` — a plain number, not a `Date`;
- overwriting asks first, because this is the one destructive action in the whole game.

The insight worth most credit: the slot list and the slot contents are **different things with different
lifetimes**, and keeping a small index is why a menu with ten slots stays instant. Credit anyone who notices
that the index can drift out of step with the saves, and says what they would do about it (rebuild it on
start, or treat the saves as the truth and the index as a cache).

**E4.** This is the best question in the lesson and it is really about determinism.

What has to be true: **the generator must produce exactly the same world from the same seed, every time, on
every machine.** That means

- a seeded random number generator of your own, not `Math.random()` — which cannot be seeded and is not
  reproducible;
- no dependence on the order of anything that might vary (object key order, floating-point differences,
  the time, the screen size, how fast the computer is);
- no use of randomness from anywhere else during generation.

What breaks the moment you change the generator: **every existing save.** The seed is only meaningful
relative to the exact code that interprets it, so a bug fix in the generator silently produces a different
world from the same number — and a player's saved dungeon is now a different dungeon, with their character
possibly inside a wall.

The professional answer, worth full marks: version the **generator**, not just the save, and keep old
versions of the generation code available — or accept that generated worlds are not save-compatible across
updates, and say so. Credit anyone who notices that this is the same versioning problem as the rest of the
lesson, one level deeper.

---

## If you only mark one thing

Make them open their game in a private browsing window in front of you. It takes five seconds, it is the
only bug in this lesson that normal testing cannot find, and it is the one that would have stopped their
game from running for a real person.
