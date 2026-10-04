# Lesson 3 — Solutions and marking notes

---

## Section A

**A1.** [3] **Clear** the buffer, **draw** into it, **show** it all at once. Two marks. One for the
name: **double buffering**.

**A2.** [3] `index = y * WIDTH + x`; `x = index % WIDTH`; `y = index / WIDTH`. One mark each.

**A3.** [3] C++ **does not check**: it writes into memory belonging to something else and carries on
as though nothing happened. One mark. Python raises `IndexError` immediately, pointing at the line
that did it — one mark.

Why it is worse, one mark: the program does not fail where the mistake is. It fails later, somewhere
unrelated, or appears to work, or behaves differently on each run and on each machine. A bug that
does not show up where it was caused is one of the hardest kinds to find.

**A4.** [2] The system clock can **jump** — a time-server sync, daylight saving, or the user changing
it — which would make a duration come out negative or enormous. `steady_clock` only ever moves
forward at a steady rate.

**A5.** [2] The `3.0` multiplies the **input**, so it controls **how fast** it wobbles. The `5.0`
multiplies the **output**, so it controls **how far**.

---

## Section B

**B1.** [3] `(5, 3)` → `3 × 32 + 5 = **101**`.
Index 101 → `x = 101 % 32 = **5**`, `y = 101 / 32 = **3**`. ✓
Two marks for the first, one for the reverse. Note that they are the same square — the question is
checking the two formulas agree.

**B2.** [4] `x * WIDTH + y` gives `4 × 32 + 2 = **130**`. The correct index is
`2 × 32 + 4 = **68**`.

So the character lands at index 130, which is `(130 % 32, 130 / 32)` = `(2, 4)` — the row and column
have been **swapped**, and the whole picture comes out mirrored along the diagonal. Two marks for the
numbers, two for the effect.

**Worth adding:** with a non-square buffer this is also dangerous. `put(30, 6, c)` would give
`30 × 32 + 6 = 966`, far past the end of a 224-character array — so the bug is an out-of-bounds write
as well as a visual mess.

**B3.** [3] It sleeps for `16 − 4 = **12 ms**`, giving a 16 ms frame, so about **62 fps**. Two marks.

With 25 ms of work there is nothing left to sleep for, so the `if` is skipped and the frame simply
takes 25 ms — about **40 fps**. The game **runs slower**; it does not skip anything. One mark.

**B4.** [4] Driven by `frame`, the bat advances a fixed amount per frame rather than per second. At
60 fps it crosses the room **twice as fast** as at 30 fps. Two marks.

The bug is **frame-rate dependence**, and the fix is to drive animation from elapsed time — which is
the same **delta time** idea the web track meets in its lesson 2 and the Python track in lesson 3.
Two marks, with one reserved for connecting it to the other tracks.

---

## Section C

**C1.** [3] `x < WIDTH - 1` stops one column early. It should be `x < WIDTH`.

A classic off-by-one, and worth noting that `-Wall` cannot catch it — the loop is perfectly legal,
it just does the wrong thing. Compilers find type errors, not logic errors.

**C2.** [4] There is no bounds check, so an out-of-range `x` or `y` writes outside the array.

Why all three outcomes happen, three marks: C++ does not check, so what you corrupt depends entirely
on **what happens to be stored next to the array in memory** — and that differs between compilers,
optimisation settings, operating systems and runs. Sometimes it is unused padding (appears to work);
sometimes another variable (prints garbage); sometimes memory the program is not allowed to touch at
all (crash).

One mark for the fix: the `if` that returns early.

**Emphasise the worst case is "it seemed to work."** The bug is still there, and it will surface on
someone else's machine, or in the version you ship.

**C3.** [3] The `sleep_for` at the end of the frame. Without it, the loop runs as fast as the machine
possibly can — hundreds of thousands of iterations a second — so the animation is a blur and the
processor is fully occupied doing nothing useful.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 2 — make them test the bounds check deliberately.** Calling `put(-5, 0, 'X')` and seeing
nothing bad happen is the point. Students who skip the check because "I will not make that mistake"
should be reminded that the whole problem is that you cannot tell when you have.

**Checkpoint 3.** The test is whether changing the dungeon strings requires any change to the drawing
code. It should not.

**Checkpoint 6 is the real assessment.** Change `TARGET_FPS` with them watching. If the bat visibly
changes speed, they are driving animation from `frame`. This catches far more students than you would
expect, including ones who did the delta-time lesson in another track.

---

## Section E — marking notes, not answers

**E1.** One `char` cannot hold both a character and a colour. Expected designs:

| Approach | Memory for 200×60 |
|---|---|
| A second parallel array of colour codes | 12,000 chars + 12,000 colours = ~24 KB |
| A struct `{char ch; char colour;}` per cell | ~24 KB, but the two can never drift apart |
| Store the ANSI escape string per cell | far larger, and slow |
| Pack character and colour into one 16-bit value | 24 KB, and fiddly to read |

The struct version is the answer to praise, because it makes it impossible for the character and its
colour to get out of step — the same principle as lesson 5 of the Python track.

Worth mentioning: this is genuinely how old text-mode graphics worked. The IBM PC's text buffer
stored exactly two bytes per cell — one character, one colour — which is why those games look the way
they do.

**E2.** The technique is **dirty rectangles** (or dirty flags): remember which cells changed, and
redraw only those. Terminal games and old 2-D engines did this constantly, because redrawing
everything was genuinely too slow.

The costs, and good answers name at least one:
- You must *track* what changed, which is extra code and a new way to be wrong.
- If you ever forget to mark something dirty, stale pixels stay on screen — a bug that is hard to
  spot and easy to introduce.
- For a small screen, the tracking costs more than the redrawing saves.

That last point is the mature answer: **the optimisation is only worth it past a certain size, and
you should measure rather than assume.**

**E3.** The game **runs slower**. `sleep_for` is skipped, the frame takes however long it takes, and
the frame rate drops. Nothing is skipped and nothing breaks — the whole game just runs behind.

What you might *want* instead, and this is the interesting part:
- **Let it slow down** (what we do) — simple, and everything stays in step. Fine for a single-player
  game.
- **Skip rendering, keep simulating** — the game stays at the right *speed* but looks choppy. What
  most action games do.
- **Take bigger time steps** — keeps real time, but large steps cause the tunnelling problems the web
  track met in lesson 4.

The honest answer is "it depends on whether being *smooth* or being *on time* matters more", and that
differs between a puzzle game and an online shooter. A student who gets to "it depends, and here is
what it depends on" has answered it completely.

**E4.** Mark on honesty rather than on a particular insight. Things students genuinely say:

- They had not realised `tracer(0)` was doing anything *real* — it looked like a magic speed switch.
- Seeing the buffer as a plain array made "a picture is just numbers" concrete.
- They now expect every graphics system to have this somewhere, and go looking for it.
- The flicker version made it obvious *why* it exists, which the Python and web versions never showed
  them.

The point of the C++ track is that the machinery is visible. This question is where that pays off,
and it is worth reading a few answers out.

---

## Teacher note: the demo to do first

Run `01-the-flicker.cpp` on the projector before you explain anything. Let it run for a full ten
seconds; it is genuinely unpleasant to look at.

Then run `02-screen-buffer.cpp`.

Say nothing between them. The question "why is the second one smooth?" will come from the class, and
then you have their full attention for the explanation.
