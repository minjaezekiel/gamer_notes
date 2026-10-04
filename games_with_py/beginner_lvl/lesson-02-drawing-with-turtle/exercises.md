# Lesson 2 — Drawing With Turtle

## Cheat sheet

### Setup (copy into every turtle program)

```python
import turtle

screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("midnightblue")
screen.tracer(0)        # stop auto-redrawing

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# ... drawing ...

screen.update()         # NOW show it
screen.exitonclick()    # keep the window open
```

### Turtle's coordinates are the odd ones out

| | Turtle | Everything else |
|---|---|---|
| `(0,0)` | the **middle** | **top-left** |
| y grows | **up** | **down** |

Always ask which convention you are in.

### Placing, not walking

```python
t.penup()        # lift the pen
t.goto(x, y)     # jump
t.pendown()      # pen back down
```

Forget `penup` and lines connect everything.

### A square

```python
for _ in range(4):
    t.forward(size)
    t.left(90)
```

Four 90° turns = 360°, a full circle.
Any polygon: `angle = 360 / sides`

### Grid to screen

```python
LEFT = -(COLUMNS * CELL) / 2 + CELL / 2
TOP  =  (ROWS * CELL) / 2 - CELL / 2

def cell_to_pixels(column, row):
    return LEFT + column * CELL, TOP - row * CELL
```

**Minus** on the y, because rows go down and turtle's y goes up.

### Why `tracer(0)` / `update()`

Draw the whole frame invisibly, then show it in one go. That is **double buffering**, and every
graphics system does it. Without it you watch the picture being assembled.

### Words

**Sprite** — one drawn thing.
**Heading** — which way the turtle faces.
**Origin** — where `(0,0)` is.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Where is <code>(0, 0)</code> in turtle, and which way does y grow? How is that different from tkinter and the web canvas?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What do <code>screen.tracer(0)</code> and <code>screen.update()</code> each do? Why do you need both?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> What is the <code>penup()</code> / <code>goto()</code> / <code>pendown()</code> pattern for?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> To draw a regular hexagon (6 sides), how many degrees should the turtle turn each time? Show your working, then write the loop.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Give two reasons &mdash; other than saving typing &mdash; to write <code>draw_sprite()</code> rather than repeating the drawing code.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> The grid has 8 columns, <code>CELL</code> is 50. Work out <code>LEFT</code>, then the x of the centre of column 0 and column 7.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What appears on the screen? Be precise &mdash; this is not a trick about the drawing commands.

```python
screen.tracer(0)
draw_board()
screen.exitonclick()
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> What shape does this draw, and where does the turtle end up facing?

```python
for _ in range(5):
    t.forward(80)
    t.left(72)
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> Using <code>cell_to_pixels</code> with <code>TOP = 150</code> and <code>CELL = 50</code>, what is the y of row 0, row 1 and row 4? Which is highest on the screen?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The program runs, draws nothing visible, and the window closes instantly. Two separate things are wrong. Name both.

```python
screen = turtle.Screen()
screen.tracer(0)
draw_board()
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The sprites appear in the right places, but ugly lines connect every one of them to the next. What is missing, and where?

```python
def draw_sprite(x, y, size, colour):
    t.goto(x, y)
    t.color(colour)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.left(90)
    t.end_fill()
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The board is drawn upside down: the top row of the <code>BOARD</code> list appears at the bottom of the window. What single character is wrong, and why does it have that effect?

```python
def cell_to_pixels(column, row):
    return LEFT + column * CELL, TOP + row * CELL
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Get a window open with the setup boilerplate, and draw one square anywhere. Make sure the window stays open.</li>
<li><strong>Checkpoint 2.</strong> Write <code>draw_sprite(x, y, size, colour)</code> that draws a square <strong>centred</strong> at <code>(x, y)</code>. Test it by drawing one at <code>(0, 0)</code> and checking it is in the middle.</li>
<li><strong>Checkpoint 3.</strong> Use a loop to draw a grid of squares. Get them evenly spaced and centred in the window.</li>
<li><strong>Checkpoint 4.</strong> Write <code>cell_to_pixels(column, row)</code> and use it, so the grid code works in <em>columns and rows</em> rather than pixels.</li>
<li><strong>Checkpoint 5.</strong> Add a <code>BOARD</code> list of strings and draw different things for different characters. Change the board and reload to prove the drawing code did not need touching.</li>
<li><strong>Checkpoint 6.</strong> Design and draw your own sprite &mdash; a spaceship, a cat, your initials &mdash; as a function taking <code>(x, y, size)</code>, and put it on the board.</li>
</ul>

<div class="note">
<span class="note-label">If you get a blank window</span>
<p>You have <code>tracer(0)</code> but no <code>update()</code>. Every drawing command ran perfectly
and the result was never shown. Go looking at the end of your program, not at the drawing code.</p>
<p>If the window flashes open and shuts, you are missing <code>screen.exitonclick()</code>.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** `draw_sprite` currently takes five arguments. **How many is too many?** What would you do if
it also needed a border, a rotation, an opacity and a text label?

<div class="lines"><i></i><i></i><i></i></div>

**E2.** Your board draws from a list of strings, one character per cell. What would you change if a
cell needed to hold *two* things — a floor tile *and* an item standing on it?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Drawing 48 squares takes a moment. Drawing 4,800 would be slow enough to notice. Without
knowing how turtle works inside, suggest **two different** ways to make it faster.
*Hint: does everything need redrawing every time?*

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** Turtle puts `(0,0)` in the middle; tkinter puts it in the corner. If you had to work in both
at once, what would you write to stop yourself making mistakes? (You will need this in lesson 5.)

<div class="lines"><i></i><i></i><i></i></div>

---

## Stretch goals

1. Draw your own sprite as a reusable function.
2. A chequerboard — `(row + column) % 2` is 0 or 1.
3. `draw_polygon(sides, length)`. Try 3, 5, 8, then 36. When does it stop looking like a polygon?
4. A spiral: move forward a little more each step. Then turn **89°** instead of 90° and see what
   happens.
5. Time your board with and without `tracer(0)` using `time.time()`. The ratio will surprise you.
