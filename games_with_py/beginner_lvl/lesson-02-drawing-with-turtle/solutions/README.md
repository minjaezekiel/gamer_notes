# Lesson 2 — Solutions and marking notes

---

## Section A

**A1.** [3] Turtle: `(0, 0)` is the **middle** of the window and y grows **upwards** — the
maths-class convention. tkinter, the web canvas, pygame and raylib all put `(0, 0)` in the
**top-left** with y growing **downwards**. Two marks for turtle, one for the contrast.

**A2.** [2] `tracer(0)` stops turtle redrawing the screen after every individual step.
`update()` shows what has been drawn. You need both: `tracer(0)` alone gives a blank window, and
`update()` alone does nothing useful because the screen is already redrawing constantly.

**A3.** [2] Moving without drawing a line — placing something at a position rather than walking
there. Without the `penup` you get lines joining everything.

**A4.** [3] `360 / 6 = 60` degrees. Two marks (one for the method, one for the number). One for:

```python
for _ in range(6):
    t.forward(80)
    t.left(60)
```

**A5.** [3] Any two: one place to change your mind, so altering how a sprite looks changes every
sprite at once; one place for a bug to live, rather than forty copies; the code that uses it reads
like what it does; it can be tested on its own; the calling code stops being about pen positions and
starts being about game objects.

Do **not** accept "saves typing" alone — the question rules it out.

---

## Section B

**B1.** [3] `LEFT = -(8 × 50) / 2 + 50 / 2 = -400/2 + 25 = -200 + 25 = -175`.
Column 0 centre: **−175**. Column 7 centre: `−175 + 7 × 50` = **175**.
One mark for LEFT, one each for the two columns. Good answers notice the symmetry, which is a sign
the centring is right.

**B2.** [4] **A completely blank window**, which then stays open until clicked.

`tracer(0)` switched off automatic redrawing, `draw_board()` ran every drawing command perfectly, and
`screen.update()` was never called — so nothing was ever shown. Two marks for "blank", two for the
explanation.

The important part for students: **nothing is wrong with the drawing code.** The instinct is to go
hunting there, and the bug is at the end of the file.

**B3.** [3] A **pentagon** (5 sides, since `360 / 5 = 72`). The turtle finishes facing exactly where
it started, because five turns of 72° is 360°. Two marks for the shape, one for the heading.

**B4.** [4] `y = TOP - row * CELL`:
row 0 → `150`; row 1 → `100`; row 4 → `150 − 200 = −50`.
**Row 0 is highest on the screen**, because turtle's y grows upwards and row 0 has the largest y.
One mark each for the three values, one for the conclusion.

---

## Section C

**C1.** [3] Two problems:

1. No `screen.update()`, so with `tracer(0)` nothing is ever shown.
2. No `screen.exitonclick()` (or `turtle.done()`), so the script finishes and the window closes
   immediately.

Two marks for finding both, one for correctly pairing each with its symptom.

**C2.** [3] `t.penup()` before the `goto`, and ideally `t.pendown()` after it. As written, the pen is
down while the turtle travels from the last sprite to this one, so it draws a line across the screen
each time.

Fix:
```python
def draw_sprite(x, y, size, colour):
    t.penup()
    t.goto(x, y)
    t.pendown()
    ...
```
(A `setheading(0)` would also be wise — see the notes.)

**C3.** [4] The `+` should be a `-`:

```python
return LEFT + column * CELL, TOP - row * CELL
```

Two marks for finding the character. Two for the reason: **row numbers increase downwards** (row 0 is
the top row of the list), but **turtle's y increases upwards**. Adding `row * CELL` therefore moves
each successive row *up* the screen, so the board is drawn bottom-to-top and appears flipped.

This is worth a minute at the board with the coordinates visualizer open, because the same confusion
returns in lesson 5 with the opposite sign.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 2 — centred, not corner-based.** Many students will draw from the corner because that is
what `goto` + `forward` naturally gives. Ask them to draw one at `(0, 0)`: if it sits up and to the
right of the middle rather than on it, it is corner-based. Centring is worth insisting on, because
every later lesson assumes it.

**Checkpoint 4.** The test is whether the drawing loop mentions pixels at all. It should read
`x, y = cell_to_pixels(column, row)` and nothing more.

**Checkpoint 5.** If they have to edit the drawing code to change the board, the separation has not
happened. Ask them to add a new row to the board while you watch.

**Checkpoint 6.** This is the one students enjoy, and the one worth leaving time for. Encourage
genuinely bad art — the point is the function signature, not the drawing.

---

## Section E — marking notes, not answers

**E1.** There is no fixed number, but somewhere around four or five positional arguments a function
becomes hard to call correctly — `draw_sprite(x, y, 40, "red", "circle", True, 0.5, 30)` is
unreadable, and swapping two arguments by mistake is silent.

Expected suggestions, all legitimate:
- **Keyword arguments with defaults** (`shape="square", border=None`), which is the Pythonic answer
  and what students should reach for.
- **Pass a dictionary** describing the sprite.
- **Make a sprite object** — which is lesson 6's answer and the intermediate level's.

The point to draw out: the problem is not the *number* of arguments, it is that the call site stops
communicating what the arguments mean.

**E2.** The honest answer is that one character per cell cannot hold two things, so something has to
give:

| Option | Cost |
|---|---|
| Two parallel boards (floor + items) | readable, but they must be kept in step |
| Multi-character cells (`"#."`, `".*"`) | the board stops lining up visually |
| A list of lists instead of strings | general, but no longer looks like the level |
| A separate list of items with positions | clean, and it is what most real games do |

The last one is worth praising — separating "the map" from "the things on the map" is a genuine
design insight and is how nearly every tile-based game actually works.

**E3.** Two different *kinds* of answer are available, and good responses find one of each:

- **Draw less:** only redraw the cells that changed, rather than the whole board. This is a real
  technique (*dirty rectangles*) and is what lesson 3 effectively starts doing.
- **Draw faster:** batch the drawing (which is what `tracer(0)` already does), draw simpler shapes,
  or use a library that talks to the graphics hardware. This is the pygame answer at intermediate
  level.

Students who say "do not redraw the walls, they never change" have found the single most important
optimisation in 2-D rendering, and should be told so.

**E4.** Looking for *one conversion function*, written once and used everywhere, rather than
remembering the rule each time:

```python
def to_screen(turtle_x, turtle_y):
    return turtle_x + WIDTH / 2, HEIGHT / 2 - turtle_y
```

The general principle is the valuable part: when two systems disagree, **convert at the boundary and
pick one convention for the inside of your program**. That is how real software handles units,
time zones, text encodings and coordinate systems. Say so — it transfers far beyond games.

---

## Teacher note: the display problem

A few students will run this from an editor that swallows the turtle window (some Thonny and Jupyter
configurations do). Make sure everyone can run `python3 file.py` from a terminal before the build
starts, or you will spend the build debugging environments instead of code.
