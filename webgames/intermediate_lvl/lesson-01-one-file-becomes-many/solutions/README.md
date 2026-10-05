# Lesson 1 — Solutions and marking notes

---

## Section A

**A1.** [2] Any two of: you scroll in order to think; you are afraid to change it because you cannot
tell what else depends on a line; names start colliding (`x` taken, so `px`); two people cannot work
on it at once; no part can be tested on its own. One mark each. Reject "it's too long" on its own —
push for a consequence.

**A2.** [2] "`game.js` needs `config.js`", and therefore `config.js` must be ready first. Full marks
need both halves: the dependency *and* the ordering consequence.

**A3.** [2] It can be reused in a completely different game without editing. One mark. Second mark
for the deeper reason: being able to isolate it proves you understood its job well enough to draw the
boundary, and it means a new control scheme touches one file.

**A4.** [3] Load order worked out from the imports · names private unless exported · strict mode
always on · runs after the HTML is parsed. Any three.

**A5.** [3] Because the browser treats every local file as a separate **origin**, so one local file
importing another is a cross-origin request, and CORS blocks it. Two marks. One mark for the fix:
serve the folder, e.g. `python3 -m http.server 8000`, and open `http://localhost:8000`.

**A6.** [2] *Coupling* = how much one file depends on another's insides (want it **low**).
*Cohesion* = how much the contents of one file belong together (want it **high**). One mark each,
and the "which is high" must be right.

---

## Section B

**B1.** [3] `main.js` runs first and immediately uses `Config`, which does not exist yet, so the
console says `Uncaught ReferenceError: Config is not defined` and the game never starts.
`config.js` then loads perfectly well, far too late to help. Two marks for the error, one for
noticing that the second file is not itself broken.

Teaching note worth making out loud: this failure *is* the topological-order idea arriving on its own.

**B2.** [3] **Once.** A module is evaluated the first time it is imported; every later import gets
the same already-finished module. One mark for "once", two for the reason. Students who say "four"
have the script-tag model in their head, which is a reasonable mistake and worth discussing.

**B3.** [4] In a module: `ReferenceError: scoer is not defined`, and `"ok"` never prints, because
modules are always in strict mode. In a plain script: it silently creates a global called `scoer`,
prints `ok`, and the typo survives for weeks. Two marks each. Full marks require naming strict mode.

**B4.** [4] `d.js, b.js, c.js, a.js, e.js`. `b` and `c` may be swapped — accept either. Two marks for
a valid order, one for noticing more than one order is valid, one for naming the method (take
whatever has nothing left to wait for, repeatedly).

**B5.** [3] There is now no order at all: `a` needs `b` needs `d` needs `a`. It is a cycle, so no
topological order exists. Accept any clear statement of the loop. The important half is "no order
exists" rather than "it would be slow" or "it would crash".

---

## Section C

**C1.** [3] A bare specifier like `"config.js"` is reserved for package names, which need a bundler or
an import map. A file path must start with `./` (or `../`, or `/`). Fix: `from "./config.js"`.

**C2.** [3] Either (a) the tags are in the wrong order — `render.js` runs first, and if it reads
`Config.INK` at the top level that is `undefined`; or (b) `config.js` exists but does not define
`INK`, or spells it differently (`Ink`, `INK_COLOUR`). One mark per cause, one for a sensible way to
tell them apart — move the tag, or `console.log(Config)` and look.

Subtlety worth a bonus mark: if `render.js` only reads `Config.INK` *inside* `draw()`, the wrong
order does no harm at all, because by then everything has loaded. Order only matters for code that
runs at load time.

**C3.** [4] `entities.js` is importing from `main.js`, so an arrow points **upwards** from a
low-level file to the entry point. Consequences, any two: it is now impossible to reuse `entities.js`
anywhere without a `main.js` that exports a `ctx`; it cannot be tested without a canvas; and it is one
small step from a cycle. Two marks for identifying the upward arrow, two for the fix — either pass
`ctx` in as a parameter (`drawBall(ctx, ball)`), or better, move the function to `render.js` where
drawing belongs.

**C4.** [4] Somebody added an `import` to `game.js` that points back at `hud.js`, completing a cycle —
or added a top-level `const`/`let` to `game.js` where there used to be only functions. `hud.js` now
reads `state` while `game.js` is still half-built. Two marks.

Smallest fix, one mark: stop importing the value and pass it in — `drawHud(state)`. One further mark
for noticing that moving `const startingLives = state.lives` *inside* `drawHud()` also makes the
error go away while leaving the cycle in place, which is a patch rather than a fix.

---

## Section D — marking the build

Do not mark this on file count. Mark it on these four things:

1. **The game is unchanged.** Play it. A student who "improved" something while moving it has done
   the one thing the brief forbade, and usually cannot explain why the game is now broken. This is the
   most important lesson in the exercise and it is worth being firm about.
2. **`render.js` is the only file containing `ctx.`** Grep it in front of them. This single test
   catches most boundary mistakes.
3. **`input.js` contains no game nouns.** Same test, different word.
4. **They can point at their arrows and say them out loud.** "`game` needs `entities` because…".
   A student who cannot narrate the graph has moved text around without building a model.

Common and acceptable variations: merging `entities.js` into `game.js` (defensible at this size —
ask them to justify it); a separate `levels.js` (good instinct, see E3); calling `config.js`
`settings.js` (fine).

Not acceptable: `game.js` importing `main.js`; `config.js` importing anything at all; a file called
`utils.js` that has become a drawer for everything that did not fit — which is the big-file problem
with a new name.

---

## Section E — marking notes

These are marked on reasoning. A confident answer with a stated cost beats a correct-sounding answer
with none.

**E1.** Both positions are defensible, and the professional answer is "render draws".

*For entities drawing itself:* everything about a ball is in one place; adding a new entity means
adding one file. (This is what most object-oriented tutorials teach, so expect it.)

*For render drawing everything:* `entities.js` stays free of the canvas, so it can be tested with no
browser, reused with a different drawing system, or run on a server. Changing the whole game's look
means touching one file.

The cost of "render draws" is honest and should be credited: `render.js` grows, and it has to know
something about every entity, so adding a new kind of thing means editing two files instead of one.
Full credit for naming that trade-off rather than pretending it does not exist.

**E2.** A good answer notices that paddle-at-the-top is mostly **numbers**, so a well-split version
touches `config.js` and little else. Give credit for spotting which parts are genuinely directional:
the `bounceOffPaddle` test (`ball.speedY > 0`), `moveBall`'s "fell off the bottom" check, and the
brick layout's starting row. Top marks for proposing that those comparisons be driven by a
configuration value, which is where this idea goes next — data, not code.

**E3.** The change-together test says **no**: `BALL_SPEED` changes when you are tuning feel, a level
layout changes when you are designing a level, and they are different jobs on different days. With
twelve levels, `config.js` becomes mostly level data, and the file whose name promises "the numbers
you tune" is now 400 lines of map. A `levels.js` — or one file per level — is the usual answer. Credit
anyone who says "it does not matter yet, but it will at about three levels", because knowing *when*
to split is the real skill.

**E4.** This is the question the whole lesson was built to provoke.

Can run with no canvas: `config.js`, `input.js` (it only needs `document` for listeners — a student
who spots that it would still need stubbing deserves credit), `entities.js`, and most of `game.js`.
Cannot: `render.js`, and `main.js` as written, because it fetches a canvas and calls
`requestAnimationFrame`.

The move they should propose: get the world size out of `canvas.width` and into the state (our
`Game.create(width, height)` already does this — point that out), and separate the *loop* from the
*game*, so something else can call `update(state, 1/60)` ten thousand times as fast as it likes.

The rule they are reinventing: **game logic must not depend on rendering.** Credit any wording of
that. It is the basis of the advanced level's testing lesson, and it is why `Game.create` takes a
width rather than a canvas — a decision that looked arbitrary in the code example and now has a
reason.

---

## If you only mark one thing

Ask them to run the original and their split version side by side and play both. Identical behaviour
after a structural change *is* the skill. Everything else in this lesson is in service of that.
