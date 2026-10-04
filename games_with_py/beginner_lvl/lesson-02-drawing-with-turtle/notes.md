# Lesson 2 — Drawing With Turtle

> **Games with Python · Beginner level · Lesson 2 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A game board and a set of sprites, drawn with code — and a `draw_sprite(x, y, colour)` function you
will reuse for the rest of this track.

```
      +---+---+---+---+---+---+
      |   |   | @ |   |   |   |
      +---+---+---+---+---+---+
      |   |   |   |   | * |   |
      +---+---+---+---+---+---+
      |   | # | # |   |   |   |
      +---+---+---+---+---+---+
```

Nothing moves yet. That is lesson 3. Today is about **getting pixels under your control**, and about
one idea that will save you more time than any other: a function that draws one thing can draw a
hundred.

## Where this fits

- **Back:** [lesson 1](../lesson-01-the-loop-without-pixels/notes.md) built a game with state and a
  loop, and no graphics at all.
- **Forward:** [lesson 3](../lesson-03-making-it-move/notes.md) puts that loop and these graphics
  together, and things start moving.
- **Today only changes the RENDER job.** Input and update are untouched. That separation is why this
  lesson is short on new ideas and long on practice.

---

## The idea, in plain words

### What turtle actually is

`turtle` comes with Python. There is nothing to install, nothing to download, and no setup — which
is exactly why we start here rather than with a game library.

The idea comes from a 1960s teaching language called Logo: imagine a turtle on a sheet of paper,
holding a pen. You tell it to move and turn, and it draws a line as it goes.

```python
import turtle

t = turtle.Turtle()
t.forward(100)     # walk 100 steps, drawing a line
t.left(90)         # turn 90 degrees to the left
t.forward(100)
```

That is the whole model. Four commands — `forward`, `backward`, `left`, `right` — plus a pen that can
be lifted (`penup`) so you can move without drawing.

### Turtle's coordinates are the ones from maths class

Here is something genuinely important, and it is the opposite of what the web track has to deal with.

| | Turtle | Nearly everything else |
|---|---|---|
| Where is `(0, 0)`? | **the middle** of the window | the **top-left** corner |
| Which way does y grow? | **upwards** | **downwards** |

Turtle deliberately uses maths-class coordinates, because it was built for teaching. Almost every
other graphics system — the web canvas, tkinter, pygame, raylib, your phone — puts `(0, 0)` in the
top-left corner with y growing *downwards*.

That makes turtle comfortable today and a small trap in lesson 5, when you move to tkinter and
suddenly "up" means subtracting. **This is worth knowing now rather than discovering later.**

> **Why is everything else upside down?** It is a leftover from old televisions. The picture was
> drawn by a beam sweeping across the top row first, then the next row down. "Row 0" meant the first
> row drawn, which was the top one. Every graphics system since has kept that numbering.
>
> The lesson is not "one of them is wrong". It is: **always ask which convention you are in.** That
> question will save you hours over the next few years.

### Jumping instead of walking

For a game, you rarely want to *walk* the turtle. You want to put something at a position
immediately:

```python
t.penup()           # lift the pen, so no line is drawn
t.goto(100, 50)     # jump straight there
t.pendown()         # put the pen back down
```

`penup` / `goto` / `pendown` is the pattern you will use constantly. Forget the `penup` and your
screen fills with lines connecting everything you drew, which is a memorable mistake to make once.

### A function that draws one thing can draw a hundred

This is the real lesson of today.

```python
# Draws ONE square, anywhere, in any colour, at any size.
def draw_square(x, y, size, colour):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(colour)
    t.begin_fill()
    for _ in range(4):      # four sides
        t.forward(size)
        t.left(90)
    t.end_fill()
```

Written once, it can now build an entire board:

```python
for row in range(6):
    for column in range(8):
        draw_square(-200 + column * 50, 150 - row * 50, 46, "steelblue")
```

Forty-eight squares from three lines. And — the part that matters — if you later decide squares
should have rounded corners or a shadow, you change **one function** and all forty-eight change.

> That is what a function is *for*. Not to avoid typing. To give you **one place to change your
> mind.**

### Turtle is slow, and you need to know why

Turtle animates every movement by default, because it was designed to teach children about angles.
For a game that is useless — drawing a board takes several seconds while you watch the turtle crawl.

Two lines fix it:

```python
screen.tracer(0)     # stop drawing to the screen after every single step
# ... do all your drawing ...
screen.update()      # now show the finished picture, all at once
```

`tracer(0)` says "stop updating the screen automatically". `update()` says "show what I have drawn".

**This is not a turtle quirk.** It is called **double buffering**, and every graphics system in the
world does it: draw the whole frame somewhere invisible, then show the finished thing in one go. If
you did not, the player would see the picture being assembled piece by piece, which looks like
flickering.

You will use these two lines in every program from here on.

---

## The idea, in pictures

Open [the coordinates explainer](../../../shared/visualizers/coordinates.html).

**What to look for:** the explainer shows **two** grids. The left one — origin in the middle, y
pointing up — is **turtle's**. The right one — origin top-left, y pointing down — is what tkinter,
pygame and everything else uses.

Drag the dot and watch both readouts. Move it *upwards* and turtle's y gets bigger while the screen's
y gets smaller. Today you are working in the left-hand grid. In lesson 5 you move to the right-hand
one, and this is the moment to notice the difference rather than lesson 5.

---

## The idea, in code

### Step 1: a window that behaves

```python
import turtle

screen = turtle.Screen()
screen.setup(width=800, height=600)     # window size, in pixels
screen.bgcolor("midnightblue")
screen.title("My board")
screen.tracer(0)                        # stop automatic redrawing

t = turtle.Turtle()
t.hideturtle()       # hide the arrow - you are drawing a game, not teaching angles
t.speed(0)           # as fast as possible

# ... drawing goes here ...

screen.update()      # show the finished picture
screen.exitonclick() # keep the window open until clicked
```

Those six setup lines are boilerplate. Copy them into every turtle program you write.

### Step 2: the reusable sprite

```python
def draw_sprite(x, y, size, colour, shape="square"):
    """Draw one sprite centred at (x, y).

    Centred, not corner-based, because in a game you almost always think
    about where the middle of something is. Doing the conversion once, here,
    means you never have to think about it again.
    """
    t.penup()
    t.color(colour)

    if shape == "circle":
        # goto the BOTTOM of the circle, because turtle draws circles upward
        # from where the turtle is standing.
        t.goto(x, y - size / 2)
        t.pendown()
        t.begin_fill()
        t.circle(size / 2)
        t.end_fill()
    else:
        t.goto(x - size / 2, y - size / 2)   # bottom-left corner
        t.setheading(0)                      # face right, so rotation cannot
                                             # leak in from a previous call
        t.pendown()
        t.begin_fill()
        for _ in range(4):
            t.forward(size)
            t.left(90)
        t.end_fill()

    t.penup()
```

That `setheading(0)` line is worth noticing. Turtle remembers which way it is facing between calls,
so a function that turns without resetting first will quietly draw crooked squares later. Making a
function reset what it depends on is a habit that prevents a whole family of mysterious bugs.

### Step 3: grid position to screen position

A game thinks in **columns and rows**. The screen thinks in **pixels**. You need to convert:

```python
COLUMNS = 8
ROWS = 6
CELL = 50

# Work out where the grid starts, so it ends up centred in the window.
LEFT = -(COLUMNS * CELL) / 2 + CELL / 2
TOP  =  (ROWS * CELL) / 2 - CELL / 2

def cell_to_pixels(column, row):
    """Turn a grid square into the screen position of its centre."""
    x = LEFT + column * CELL
    y = TOP - row * CELL        # MINUS, because row 0 is at the top and
                                # turtle's y grows upwards
    return x, y
```

That minus sign is the whole coordinate conversation in one character. Row numbers go *down* the
board; turtle's y goes *up* the screen. So moving down a row means subtracting.

---

## The maths you just used

### Centring a grid

```python
LEFT = -(COLUMNS * CELL) / 2 + CELL / 2
```

The whole grid is `COLUMNS × CELL` pixels wide. To centre it, start half a grid to the left of the
middle — that is the `-(COLUMNS * CELL) / 2`. Then add half a cell, because `draw_sprite` wants the
**centre** of a cell, not its left edge.

Work through it with real numbers: 8 columns of 50 pixels is 400 wide, so the grid runs from −200 to
+200, and the first cell's centre is at −200 + 25 = **−175**.

### Angles and a full turn

```python
for _ in range(4):
    t.forward(size)
    t.left(90)
```

Four turns of 90° is 360°, a full circle, so the turtle ends up facing exactly where it started. That
generalises:

```python
def draw_polygon(sides, length):
    angle = 360 / sides        # the turns must always add up to 360
    for _ in range(sides):
        t.forward(length)
        t.left(angle)
```

A triangle turns 120° three times. A hexagon turns 60° six times. A 36-sided shape turns 10° thirty-
six times and looks like a circle, which is in fact how your computer draws circles.

`_` as a variable name is a Python convention meaning "I need to repeat this, but I do not care about
the number". It is still a real variable; the name just tells a reader to ignore it.

---

## Break it on purpose

Use `code/03-game-board.py`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Delete `screen.tracer(0)` | | |
| Delete `screen.update()` (keeping `tracer(0)`) | | |
| Remove the `t.penup()` from `draw_sprite` | | |
| Change `TOP - row * CELL` to `TOP + row * CELL` | | |
| Remove `t.setheading(0)` and draw a few shapes in a row | | |
| Change `CELL` to `200` | | |

The second one is the most surprising: with `tracer(0)` and no `update()`, you get a completely blank
window, even though all the drawing code ran perfectly. **Nothing is wrong with the drawing — it was
just never shown.**

---

## Think like an engineer

1. You now have `draw_sprite(x, y, size, colour, shape)`. **How many arguments is too many?** What
   would you do if it also needed a border, a rotation, an opacity and a label?
2. Your board is drawn with two nested loops. If you wanted *some* squares a different colour, where
   would that information come from? (You already know the answer from lesson 1: do not write it in
   the loop.)
3. **A real performance question.** Drawing 48 squares takes a moment. Drawing 4,800 would be slow
   enough to notice. Without knowing anything about how turtle works internally, suggest two
   different ways to make it faster. *Hint: does everything need redrawing every time?*
4. Turtle puts `(0, 0)` in the middle and tkinter puts it in the corner. If you had to work in both
   at once, what would you write to stop yourself making mistakes? (This is a real technique, and you
   will need it in lesson 5.)

---

## Vocabulary

| Word | What it means |
|---|---|
| **Sprite** | A single drawn thing in a game — a player, an enemy, a block. |
| **`penup` / `pendown`** | Lift or lower the pen, so moving does or does not draw. |
| **`tracer(0)`** | Stop redrawing the screen after every step. |
| **Double buffering** | Draw the whole frame invisibly, then show it in one go. |
| **Origin** | Where `(0, 0)` is. Turtle: the middle. Nearly everything else: top-left. |
| **Heading** | Which way the turtle is currently facing. |

---

## Recap

- Turtle needs no installation, which is why we start here.
- Turtle uses **maths-class coordinates**: origin in the middle, **y grows up**. Nearly everything
  else does the opposite — always ask which convention you are in.
- `penup` → `goto` → `pendown` is how you place things rather than walk to them.
- **`tracer(0)` and `update()`** make turtle fast enough to be a game. That is double buffering, and
  every graphics system does it.
- A function that draws one thing can draw a hundred — and gives you **one place to change your
  mind**.

---

## Stretch goals

1. **Draw your own sprite.** A spaceship, a cat, your initials. Make it a function taking `(x, y,
   size)` so you can put it anywhere.
2. **A chequerboard.** Alternate two colours. (Hint: `(row + column) % 2` is 0 or 1.)
3. **`draw_polygon(sides, length)`.** Try 3, 5, 8, then 36 sides. At what number does it stop looking
   like a polygon?
4. **A spiral.** Move forward a little more each step while turning a constant amount. Small changes
   to the numbers give dramatically different shapes — try turning 89° instead of 90°.
5. **Time it.** Use `time.time()` to measure how long your board takes to draw with and without
   `tracer(0)`. The ratio will surprise you.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run a turtle drawing with `tracer` **on**, so the class watches it crawl. Then turn it off and run it again. You now have their attention for the whole double-buffering explanation. |
| 10–25 | **Concept.** Coordinates, with the visualizer. Make the turtle-versus-everything-else contrast explicitly; it pays off in lesson 5. |
| 25–40 | **Live-code** the setup boilerplate and `draw_square`. Then turn `draw_square` into a loop drawing twelve of them, so the point of the function lands. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. |
| 120–140 | Break-it-on-purpose, then share the sprites people drew. |
| 140–150 | Recap. Next lesson it moves. |

**What usually goes wrong**

1. **The window opens and closes instantly.** They are missing `screen.exitonclick()` or
   `turtle.done()` at the end. The script finishes, so the window closes. Extremely common, and the
   fix is one line.
2. **A completely blank window.** `tracer(0)` without a matching `update()`. The drawing code ran
   perfectly and was never shown. A great bug, because the instinct is to go hunting in the drawing
   code where nothing is wrong.
3. **Lines everywhere connecting the sprites.** Missing `penup()`.
4. **Crooked squares after a few draws.** The turtle's heading carried over. `setheading(0)` fixes
   it, and the general principle — make a function reset what it relies on — is worth naming.
5. **Everything drawn upside down.** They used `TOP + row * CELL`. The coordinates visualizer
   resolves it in about ten seconds.
6. **Running from an IDE that swallows the turtle window.** Thonny, some Jupyter setups. Running from
   a terminal with `python3 file.py` always works; make sure everyone can do that.

**If you are running short on time** — give them the setup boilerplate and `draw_sprite` as a
paste-in, and spend the build time on the grid conversion and drawing their own sprites. Do not cut
`tracer`/`update`; they need it in every later lesson.

**For the student who finishes at minute 90** — stretch goal 4 (the spiral with 89° instead of 90°)
is wonderful. Tiny changes produce wildly different shapes, it is entirely visual, and it occupies a
strong student happily for half an hour.

**Worth saying at the end:** today changed only the RENDER job. The loop and the state from lesson 1
are untouched. That is not a coincidence — it is the payoff for keeping the three jobs separate, and
it is why next lesson can add movement without disturbing anything they wrote today.
