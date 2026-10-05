# Lesson 6 — Tilemaps

## Cheat sheet

### Loading, and the four traps

```python
from pathlib import Path
HERE = Path(__file__).parent

def load_level(path):
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    while lines and not lines[-1].strip():
        lines.pop()
    width = len(lines[0])
    bad = [i for i, r in enumerate(lines) if len(r) != width]
    if bad:
        raise ValueError("rows %s are not %d chars" % (bad, width))
    return lines
```

1. the **trailing newline** adds an empty row
2. `rstrip()` also eats trailing **spaces** — use `rstrip("\n")`
3. **rows of different lengths** → `IndexError`, or a silent hole
4. `open("level.txt")` uses the **working directory** — use `HERE / "level.txt"`

### The two conversions

```python
col = int(x // TILE)     # position → column   (FLOOR division)
x   = col * TILE         # column → position
```

`-5 // 32 == -1` (right). `int(-5 / 32) == 0` (lets you stand in the wall).

### Out of bounds is solid

```python
if col < 0 or row < 0 or row >= ROWS or col >= COLS:
    return "#"
```

### Tiles as a table

```python
TILES = {".": {"solid": False},
         "#": {"solid": True},
         "~": {"solid": False, "slows": True},
         "^": {"solid": False, "deadly": True}}
```

### Which tiles does the box touch?

```python
c0 = rect.left   // TILE
c1 = (rect.right  - 1) // TILE    # the -1 matters
r0 = rect.top    // TILE
r1 = (rect.bottom - 1) // TILE
```

At most **4**. Without the `-1` you stick in gaps exactly your own width.

### Collide in TWO steps

```python
# X
pos.x += vel.x * dt;  rect.centerx = round(pos.x)
if hit: rect.right = wall.left   (or rect.left = wall.right)

# Y
pos.y += vel.y * dt;  rect.centery = round(pos.y)
if hit and vel.y > 0:
    rect.bottom = wall.top
    on_ground = True      # ← where this comes from
```

Sliding along walls comes **free**. One step cannot know what to undo.

### Pre-rendering

Draw the level once onto a Surface, blit it every frame. Size is
`cols × rows × TILE² × 4` bytes — 500×500 at 32 px is about **1 GB**.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Give three advantages a grid has over a list of arbitrary rectangles.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Name three things that go wrong when loading a level from a text file.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why <code>//</code> rather than <code>int(x / TILE)</code>? Give the case where they differ and what it causes.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why does <code>tile_at</code> return a wall for positions off the map? Name two problems that removes.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why must collision be resolved one axis at a time? What does the one-step version not know?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Where does <code>on_ground</code> come from, and why not from a key press?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> What is the <code>- 1</code> in <code>(rect.right - 1) // TILE</code> for?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> <code>TILE</code> is 32. Give the column and row for (95, 64), and the top-left corner of that tile.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> What do <code>-5 // 32</code> and <code>int(-5 / 32)</code> give? Which is correct for a player at x = &minus;5, and why does it matter?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> A rect is at left = 60, top = 30, 26 wide, 26 tall, with <code>TILE</code> = 32. Which columns and rows does it touch? How many tiles is that?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> The level file's last line is <code>"########"</code> followed by a newline. How many rows does a naive <code>readlines()</code> give, and what is the last one?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> A level is 400 &times; 400 tiles at 32 px. How big would one pre-rendered Surface be, in bytes and in gigabytes?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> <code>FileNotFoundError: level.txt</code>, although the file is definitely next to the script.

```python
lines = open("level.txt").read().splitlines()
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Walking diagonally into a corner makes the player climb the wall.

```python
self.pos += self.vel * dt
self.rect.center = self.pos
if self.hits_a_wall():
    self.pos -= self.vel * dt
    self.rect.center = self.pos
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The bottom row of the level is empty, although the file ends with a row of walls.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C4.</span> The player gets stuck in a gap that is exactly their own width.

```python
c1 = rect.right // TILE
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C5.</span> The right-hand quarter of the level has no walls at all, although the author typed them, and there is no error.

```python
LEVEL = [
  "####################",
  "#..................#",
  "#..###....####.#",
  "####################",
]
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write <code>level.txt</code> and a loader with the row-length check and <code>Path(__file__).parent</code>. Break the file on purpose and read your own error message.</li>
<li><strong>Checkpoint 2.</strong> Draw the level with a <code>TILES</code> table. Print the column, row and character under the mouse pointer.</li>
<li><strong>Checkpoint 3.</strong> Add a player that moves with the arrow keys and <em>no</em> collision. Outline every tile the player's rect is touching &mdash; you should see at most four.</li>
<li><strong>Checkpoint 4.</strong> Add the two-step collision. Test by walking head-on into a wall, then diagonally &mdash; you should slide without writing any sliding code.</li>
<li><strong>Checkpoint 5.</strong> Add gravity and make <code>on_ground</code> come from the downward test. Draw it on screen as a word, then add a jump that only works when it is true.</li>
<li><strong>Checkpoint 6.</strong> Add water and spikes from the table. Neither should need a change to the drawing code.</li>
<li><strong>Checkpoint 7.</strong> Add a reload key. Edit <code>level.txt</code> in another window and press it. Then design a level.</li>
<li><strong>Checkpoint 8.</strong> Pre-render the level to one Surface. Put the draw time on screen for both methods and write down the two numbers.</li>
</ul>

<div class="note">
<span class="note-label">If the player sticks</span>
<p>Print <code>c0, c1, r0, r1</code> on screen and walk slowly. If <code>c1</code>
jumps forward a column before the player has actually crossed into it, you need the
<code>- 1</code>.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** The tile table holds *properties*. Where does that stop working? Think about
a door that opens, a platform that moves, a button that remembers being pressed.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** A list of strings, a list of lists, a flat `bytearray`, or a real format
like `.tmx`. What does each make easy? Which for a level 10,000 tiles wide?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design a one-way platform: solid from above, pass-through from below. What
must the collision code know that it does not know now?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** The hard one. 200 coins, and collecting one changes the world — but the
level is also what you draw and collide against. Where does "taken" live? Edit the
level in memory, keep a separate set, or keep two layers? Pick one and say what
happens on restart.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. One-way platforms (E3).
2. A tileset built in code, with a different top edge on walls.
3. Auto-tiling: pick a wall's picture from its four neighbours. Find the pattern.
4. A level editor that writes `level.txt` back out.
5. Chunked pre-rendering, a screen at a time.
