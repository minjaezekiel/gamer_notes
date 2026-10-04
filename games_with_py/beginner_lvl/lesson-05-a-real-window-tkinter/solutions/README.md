# Lesson 5 — Solutions and marking notes

---

## Section A

**A1.** [2] `(0, 0)` is the **top-left corner** and y grows **downwards**. To move up:
`y = y - speed`. One mark each.

**A2.** [2] **left, top, right, bottom** — two opposite corners. Not x, y, width, height.

**A3.** [3] **Retained mode:** the system remembers every shape you create, and you move them —
tkinter's canvas. **Immediate mode:** you redraw everything yourself each frame, and the system
remembers nothing — turtle and the web canvas. Two marks for the distinction, one for correctly
assigning each.

Neither is better; knowing which you are in is what matters.

**A4.** [2] An **integer** — an item ID. The canvas keeps the real shape and hands you a number to
refer to it by. Students who say "an object" have the common misconception; that is what the question
is for.

**A5.** [3] Because you are keeping **two separate records** of the same thing: your Python list and
the canvas's own list of items. Removing from one does not touch the other. Forget `canvas.delete`
and the fruit vanishes from the game logic — no collisions, no score — but stays visible on screen
forever.

---

## Section B

**B1.** [3] `speed = 200 + 320 × 0.016 = 200 + 5.12 = **205.12**`.
`y = 100 + 205.12 × 0.016 ≈ **103.28**`.
Since y grew, it is **lower** on the screen. Two marks for the numbers, one for "lower".

The "lower" part is where the marks are lost, and it is the whole lesson.

**B2.** [4] A brand new oval is created every frame and the canvas keeps all of them. At 60 fps for
10 seconds that is **about 600 shapes** — and the canvas has to consider every one of them on every
redraw, so it gets progressively slower.

Fix: create the oval once before the loop, then `canvas.coords(ball, ...)` to move it.

Two marks for the diagnosis, one for the number, one for the fix.

**B3.** [3] It draws a rectangle from `(100, 400)` to `(92, 18)` — tkinter normalises the corners, so
it comes out spanning x from 92 to 100 and y from 18 to 400. That is an **8 pixels wide, 382 pixels
tall** vertical sliver, nowhere near where it was wanted.

The author passed width and height where right and bottom were expected. Correct call:
`create_rectangle(100, 400, 192, 418)`.

**B4.** [4] One mark each:

- score 0 → `1.2 − 0 = **1.2 s**`
- score 100 → `1.2 − 0.4 = **0.8 s**`
- score 300 → `1.2 − 1.2 = 0`, but `max(0.35, 0)` gives **0.35 s**
- score 10,000 → still **0.35 s**, because the `max` floors it.

Without the floor the delay would be `1.2 − 40 = −38.8` seconds, which would spawn fruit on every
single frame and instantly fill the screen. The `max` is what stops the game becoming unplayable
rather than merely hard.

---

## Section C

**C1.** [3] The `-=` should be `+=`. In tkinter, y grows **downwards**, so adding moves something
down the screen. Subtracting moves it up — which is why the fruit rises.

One mark for the character, two for the reason. Students coming from turtle will make this exact
mistake, which is why lesson 2 warned about it.

**C2.** [4] `canvas.delete(fruit["item"])` is missing from the removal. The item is popped from the
Python list, so the game stops knowing about it, but the canvas still holds the shape and keeps
drawing it.

Two marks for the fix, two for correctly explaining the *split* between the two records — that is
the idea being tested, not the single missing line.

**C3.** [4] The **forward loop while removing** bug. Removing index `i` shifts everything after it
down one place, so the next `i` steps straight over the shifted-up element. Roughly half are missed,
and `remove_fruit` is called with indexes that now point at a different fruit — hence lives lost at
the wrong times.

Two marks for naming and explaining, one for a fix (`for i in range(len(fruits) - 1, -1, -1)`), and
**one for noticing this is the third time**: the web track's particles (L5), Breakout's bricks (L6),
and now here.

That recognition is the point. Tell the class plainly: this bug will follow them into every language
they ever use.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 1.** Ask them to show you a rectangle exactly 92×18. If they wrote
`create_rectangle(x, y, 92, 18)` they have the two-corners misunderstanding and will hit it again in
checkpoint 3.

**Checkpoint 3.** The test is whether `create_rectangle` appears anywhere inside `game_loop`. If it
does, let them run it for ten seconds and watch the slowdown before you say anything.

**Checkpoint 5.** Two things to check: backwards loop, and both records cleaned.

**Checkpoint 6.** The floor on the difficulty curve. A student whose game becomes literally
impossible has learned something useful — ask them at what score it broke, and what they would do
about it.

---

## Section E — marking notes, not answers

**E1.** There is a real answer for each, and the reasoning matters more than the choice:

| | Better fit | Why |
|---|---|---|
| **Snake** | either | few objects, grid-aligned; both work comfortably |
| **500 sparks** | **immediate** | creating and destroying 500 retained items constantly is expensive; redrawing 500 dots is cheap |
| **Chess board** | **retained** | 64 squares and 32 pieces that rarely move — redrawing all of it 60 times a second is pure waste |
| **Scrolling level** | **immediate** | everything moves every frame, so there is nothing to retain |

The principle to draw out: **retained mode wins when little changes; immediate mode wins when
everything changes.** Students who find that generalisation have got more out of the question than
the four answers.

**E2.** What goes wrong: shapes left on screen with nothing behind them (a missing `delete`), or
items referenced after deletion (a `TclError`), or a list of fruit whose item IDs no longer exist.

Designs for making disagreement impossible:

- **One function that owns both.** `remove_fruit(i)` does the `delete` and the `pop` together, and
  nothing else is allowed to remove a fruit. This is the reference code's approach and is a perfectly
  good answer.
- **A class.** Give `Fruit` a `destroy()` method that cleans up both. Same idea, tidier.
- **Rebuild from the list each frame** (immediate mode) so there is only ever one record. Honest, and
  it gives up the advantage of retained mode.

The general principle is worth naming: **when you must keep two things in step, give exactly one
piece of code the job of changing them.** That is the real answer, and it applies far beyond canvases.

**E3.** How to find the point without guessing: **measure**. Record how long it takes players to
react — the time between a fruit becoming catchable and the basket arriving — and look for where the
success rate falls off a cliff. Or more simply, play it and log the score at which people start
losing. Strong answers say "test it with actual people", which is the real method.

What to change instead of speed: the *number* of fruit at once (planning, not reflexes); the spread
across the screen; fruit you must avoid; narrowing the basket; mixed speeds so you have to prioritise.

The distinction worth drawing out, as in lesson 4: **difficulty from reaction time runs out quickly;
difficulty from decision-making does not.**

**E4.** If the window is dragged or the machine is busy, `after` does not fire and the next `dt` is
enormous — half a second instead of a sixtieth. Without the clamp, every fruit jumps hundreds of
pixels in one step: fruit teleports through the basket without being caught, and things vanish off
the bottom.

What the clamp costs: the game **loses that time**. A half-second stall becomes a sixtieth of a
second of simulated movement, so the game world runs slightly behind real time. For this game nobody
would notice. For a game with a real-time clock, or multiplayer, it would matter — and that is the
honest trade-off the question is after.

---

## Teacher note: the demo worth doing live

Write the `create_oval`-in-the-loop bug deliberately, on the projector, with
`print(len(canvas.find_all()))` in the draw function. Let it run for twenty seconds while you talk.

The number climbing into the thousands while the animation visibly stutters makes retained mode
concrete in a way that no explanation does. Then change one line to `canvas.coords(...)` and run it
again. The count stays at a handful and the animation is smooth.

Thirty seconds, and the single most important idea of the lesson is landed.
