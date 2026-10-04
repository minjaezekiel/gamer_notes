# Lesson 6 — Solutions and marking notes

---

## Section A

**A1.** [3] Any two, one mark each, plus one for a well-expressed answer:
you can see the level by looking at it; you can change it without touching game logic; adding a level
means adding an array; a non-programmer could edit it; levels can be loaded from a file, generated,
or built by players; the game logic is tested once and works for every level.

**A2.** [2] The **first** index (`y`) chooses the row, because the outer array holds rows and each
inner array is one row's worth of cells.

**A3.** [2] If you cannot name the function without using the word "and", it is doing more than one
thing — split it.

**A4.** [3] `32 + 4 × (68 + 6) = 32 + 4 × 74 = 32 + 296 = 328`. One mark for the formula, two for the
answer.

**A5.** [3] **Flag:** simpler, keeps the array stable so indexes stay valid, and is better when
things come back (a level restart, respawning enemies). **Remove:** keeps the array small so loops
stay short, and avoids `if (!alive) continue` everywhere. One mark each, one for a sensible framing.

---

## Section B

**B1.** [4] Count the non-zero cells: row 0 has 2, row 1 has 2, row 2 has 4. **Eight bricks.**
The shape is a checkerboard pattern over two rows with a solid row of tough (orange) bricks
underneath. Two marks for the number, two for the shape.

**B2.** [4] The array is **3 rows of 4**, so it is not square — and that is what makes this
instructive.

`layout[x][y]` with `x` running 0…3 (because the loop uses the row length) will try `layout[3]`,
which **does not exist** — there are only rows 0, 1 and 2. So it is `undefined`, and `undefined[y]`
throws `TypeError: Cannot read properties of undefined`.

So it does not merely come out mirrored; it **crashes**. Two marks for the mirroring idea, two for
spotting that a non-square level turns the bug into a crash.

(Worth telling students: a square level would mirror silently, which is *worse*, because a crash tells
you where to look.)

**B3.** [4] The brick is destroyed and the ball's **vertical** speed is flipped, but the ball came in
**horizontally**. So it is still inside (or immediately adjacent to) the next brick along, still
travelling right. Next frame it destroys that one too, flips vertically again, and carries on.

The player sees the ball **carve straight through the whole row sideways**, flipping up and down as
it goes. Two marks for the mechanism, two for describing what is seen.

**B4.** [3] Both bricks are destroyed and the velocity is flipped **twice** — which returns it to
exactly what it was. So the ball carries on in the same direction as if nothing had happened, having
destroyed two bricks. It looks like the collision failed. Hence the `break`.

---

## Section C

**C1.** [4] It is the **forward loop with splice** bug, seen in lesson 5 with particles and before
that in principle. Removing index `i` shifts everything after it down one place, so the next
iteration's `i++` steps straight over the shifted-up element.

Fixes, any of: loop backwards; use the `alive` flag instead; or `i--` after splicing.

Two marks for naming/explaining, two for a correct fix. **Award a bonus mark for noticing it is the
same bug as lesson 5** — this is the third time a bug has returned in a new costume, and recognising
that is the skill.

**C2.** [3] The `alive` check is in the collision code but missing from `drawBricks`. The brick is
marked dead so the ball ignores it, but the drawing loop still paints it. Fix: `if (!brick.alive)
continue;` in `drawBricks` too.

(This is a good illustration of why a flag has a cost: you must remember it in *every* place that
touches the array.)

**C3.** [4] Two marks for any two specific reasons:

- You cannot find anything in it, so changing it is slow and frightening.
- You cannot test or reason about one part without the others.
- The state check has to be repeated or forgotten in many places.
- Two unrelated bugs look identical from outside, because everything is in one place.
- You cannot reuse any of it in the next game.

Two marks for a restructure: split into `updatePaddle`, `updateBall`, `checkPaddleCollision`,
`checkBrickCollisions`, `updateParticles`, each doing one named job, with `update(dt)` calling them
in order.

---

## Section D — marking the capstone

**Mark on four things, not on feature count:**

1. **Does it run without errors?**
2. **Is the level data separate from the game logic?** This is the lesson's main idea.
3. **Can they explain any function you point at?** Pick one at random and ask.
4. **Did they change something to make it theirs?**

Checkpoint 4 is a full pass. Checkpoints 5 and 6 are distinction.

**Point 4 deserves weight.** A student whose Breakout has a slightly wonky power-up they invented has
done something more valuable than a student with a flawless copy of the example. Say this before they
start, or they will aim for the copy.

**Common structural problems while circulating:**

- Everything in one function. Do not fix it for them; ask them to find the brick-collision code while
  you count to twenty. The difficulty makes the argument far better than you can.
- Level data mixed into the drawing code — brick positions hard-coded rather than computed from the
  grid. Ask: "how would you add a fourth level?"
- `break` missing, so bricks vanish in pairs. Visually obvious.

---

## Section E — marking notes, not answers

**E1.** Good answers notice that a *full* grid is boring because every shot hits something, so there
is no aiming. Interesting layouts have gaps that reward precision, tough bricks that shape the route,
or a shape that collapses in a satisfying order. Mark on the *sentence of reasoning*, not the drawing.

**E2.** The honest answer for most students' code is "a few numbers": `BRICK_W` would need to shrink,
and `BRICK_LEFT` would need recalculating, or the bricks run off the screen. The good follow-up is to
ask whether the brick width should be *computed* from the level width and the canvas width rather
than typed in:

```js
const BRICK_W = (W - 2 * MARGIN - (cols - 1) * GAP) / cols;
```

A student who arrives at that has learned the actual lesson about data-driven design — that the data
should drive as much as possible, not just the layout.

**E3.** Expect one of these shapes:

| Format | Cost |
|---|---|
| Bigger numbers (`11` = red brick, `12` = power-up) | hard to read, and columns stop lining up |
| Letters (`R`, `P`, `X`) | still one character wide, still readable — usually the best answer |
| An array of objects per cell | fully general, completely unreadable as a picture |
| Two parallel grids, one for type and one for contents | readable, but you must keep them in step |

The thing to draw out: the current format is readable *because* each cell is one character wide, so
the array looks like the level. Every extension threatens that, and the letter-based version is the
usual professional compromise. Real tile editors solve it by not using text at all — which is its own
trade-off, because now you need a tool to read your own levels.

**E4 — the engine question.** This is the best question in the beginner course. Look for the division:

**Reusable (the skeleton):** the loop with delta time and clamping; the state machine; input polling;
`boxesOverlap`; particles; shake; sound; a scene/level loader; drawing helpers.

**Always game-specific:** what the entities *are*; what collisions *mean*; the win and lose rules;
the level data; how it feels.

The best answers notice the hard part — that the boundary keeps moving. Is "paddle" a general idea or
a Breakout idea? Is "score" general? Every engine answers differently, and over-generalising produces
engines that are harder to use than writing the game directly.

If a student says "the skeleton is the stuff that was identical in Pong and Breakout, and the game is
the stuff that differed", they have understood it exactly. Tell them that this is what a game engine
is, and that the intermediate level begins by building one.

---

## End of the beginner course

Put `lesson-01/code/03-the-loop.html` next to `lesson-06/code/02-breakout.html` on the projector.

Same shape: state at the top, `update`, `render`, `requestAnimationFrame`. Thirty lines became four
hundred, and the **structure never changed** — everything went *inside* the functions that were
already there on day one.

Then tell them the true part: that is also what a commercial game looks like. Much more inside each
function, far better tools, hundreds of people — and no additional structural idea beyond the one
they now have.
