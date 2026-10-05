# Lesson 6 — Tilemaps

> **Games with Python · Intermediate level · Lesson 6 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A world loaded from a **text file you can edit in any editor**, with solid walls you cannot pass
through, water that slows you down and spikes that send you back to the start — and a reload key, so
you can redesign the level without restarting the game.

```
level.txt
########################
#@.....................#
#....####.......o.o.o..#
#.......#.....#########.
#..o....#..............#
#.####.........####....#
#....#...~~~~..#..#..o.#
#....#^^^^^^^^^#..#.####
########################
```

That file is the level. Twenty-four characters by nine, and by the end of the lesson you will be
designing levels by typing.

## Where this fits

- **Back:** [lesson 2](../lesson-02-rects-images-and-the-display/notes.md) gave you `Rect` and
  `colliderect`; [lesson 4](../lesson-04-sprites-and-groups/notes.md) gave you groups. Today the world
  itself becomes data.
- **Forward:** lesson 7 *(not yet written)* makes the world bigger
  than the window, and lesson 9 *(not yet written)* adds gravity to today's
  collision without changing it.
- **Other tracks:** `webgames` intermediate lesson 5 is this lesson with an array in the source instead
  of a file. The C++ beginner track already built one as a screen buffer. The grid arithmetic is
  identical everywhere.

---

## The idea, in plain words

### Why a grid

A level could be a list of arbitrary rectangles, and some games do that. A grid wins for four reasons,
and the third is the one that matters most:

1. **It is tiny.** A few hundred characters for a whole level.
2. **You can see it.** The data *looks like* the level.
3. **Looking things up is instant.** "Is there a wall here?" is one division and one index — not a loop
   over every wall. With rectangles you ask everybody; with a grid you work out your seat number.
4. **Editing it is editing text.** No tools to write.

### Loading it from a file, and the four things that go wrong

```python
def load_level(path):
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    # drop blank lines at the end, which almost every editor adds
    while lines and not lines[-1].strip():
        lines.pop()
    return lines
```

Four traps, all of which you will meet:

- **The trailing newline.** Nearly every editor writes one, so the last "row" is an empty string, and
  your level is one row taller than it looks with a row of nothing at the bottom.
- **`rstrip()` versus `rstrip("\n")`.** Plain `rstrip()` also removes trailing **spaces** — and if your
  level uses spaces for empty tiles, it silently shortens those rows.
- **Rows of different lengths.** A short row returns an `IndexError`, or worse, silently has no floor.
  Check at load time:

  ```python
  width = len(lines[0])
  bad = [i for i, row in enumerate(lines) if len(row) != width]
  if bad:
      raise ValueError("rows %s are not %d characters" % (bad, width))
  ```

- **Where the file is.** `open("level.txt")` looks in the *working directory*, not next to your script.
  Run the game from somewhere else and it vanishes. The fix is one line and worth making a habit:

  ```python
  from pathlib import Path
  HERE = Path(__file__).parent
  lines = load_level(HERE / "level.txt")
  ```

### The two conversions

```python
col = int(x // TILE)      # position  →  column
x = col * TILE            # column    →  position
```

`//` is **floor division**, and it is the right one: it rounds towards negative infinity, so `-5 // 32`
is `-1` and not `0`. A player at `x = -5` is genuinely in column −1, and getting that wrong lets them
stand inside the left-hand wall. `int(-5 / 32)` gives `0`, which is the bug.

### Reading it safely

```python
def tile_at(col, row):
    # OUT OF BOUNDS IS SOLID. One decision, several bugs gone: no IndexError, no
    # walking off the edge, and the border of '#' becomes optional.
    if col < 0 or row < 0 or row >= len(LINES) or col >= len(LINES[0]):
        return "#"
    return LINES[row][col]
```

### Tiles as data, not as `if`s

```python
TILES = {
    ".": {"solid": False},
    "#": {"solid": True,  "colour": (58, 69, 85)},
    "~": {"solid": False, "colour": (28, 79, 124), "slows": True},
    "^": {"solid": False, "colour": (124, 45, 45), "deadly": True},
    "o": {"solid": False, "coin": True},
    "@": {"solid": False},
}
```

Now a new tile type is **one line**, and the drawing and collision code never grows: it asks the table
rather than knowing the answers. A `dict.get(ch, UNKNOWN)` means a typo in the level file shows up as a
visible question mark rather than a crash.

### Collision: two steps, never one

This is the part everybody gets wrong first, and it is why it has its own visualizer.

Move both axes at once, discover you are inside a wall, and you have **no information about which
direction caused it** — so there is nothing sensible to undo. Guess, and the player climbs walls or
sticks to them.

```python
# ---- step 1: X only, then fix X ----
self.pos.x += self.vel.x * dt
self.rect.centerx = round(self.pos.x)
for wall in self.walls_touching():
    if self.vel.x > 0:
        self.rect.right = wall.left
    elif self.vel.x < 0:
        self.rect.left = wall.right
    self.pos.x = self.rect.centerx

# ---- step 2: Y only, from the corrected X ----
self.pos.y += self.vel.y * dt
self.rect.centery = round(self.pos.y)
self.on_ground = False
for wall in self.walls_touching():
    if self.vel.y > 0:
        self.rect.bottom = wall.top
        self.on_ground = True          # ← this is how a platformer knows it landed
    elif self.vel.y < 0:
        self.rect.top = wall.bottom
    self.pos.y = self.rect.centery
    self.vel.y = 0
```

Because each step moved in one direction only, each correction **knows** what it is undoing. Two
consequences fall out:

- **Sliding along a wall is free.** Walk diagonally into one: X is cancelled, Y is not. You wrote no
  sliding code.
- **`on_ground` comes from the downward test.** Not from a key press. Lesson 9 depends entirely on this.

Notice `rect.right = wall.left` — one assignment, no arithmetic. That is lesson 2's point about `Rect`
paying off.

### Only test the tiles you are touching

```python
def tiles_touching(rect):
    c0 = rect.left // TILE
    c1 = (rect.right - 1) // TILE          # -1: a right edge ON a boundary is not in the next column
    r0 = rect.top // TILE
    r1 = (rect.bottom - 1) // TILE
    for row in range(r0, r1 + 1):
        for col in range(c0, c1 + 1):
            yield col, row
```

For a player smaller than a tile that is at most **four** tiles, whatever the size of the level. A
500 × 500 world has a quarter of a million tiles and this looks at four of them.

That `- 1` is small and load-bearing. Without it, a player whose right edge lands exactly on `x = 64` is
counted as touching column 2, so a wall there pushes them back even though they are only *adjacent* to
it — and the symptom is a player who sticks in gaps exactly their own width.

### Drawing: two ways, and when each is right

**Per tile, every frame** — simple, and only the visible ones:

```python
for row in range(first_row, last_row + 1):
    for col in range(first_col, last_col + 1):
        info = TILES.get(tile_at(col, row))
        if info.get("colour"):
            screen.blit(TILE_IMAGES[tile_at(col, row)], (col * TILE, row * TILE))
```

**Pre-rendered onto one Surface**, once, at load time:

```python
level_surface = pygame.Surface((COLS * TILE, ROWS * TILE))
for row in range(ROWS):
    for col in range(COLS):
        level_surface.blit(TILE_IMAGES[tile_at(col, row)], (col * TILE, row * TILE))
# then, every frame:
screen.blit(level_surface, (0, 0))
```

One blit instead of several hundred. This is the lesson 2 idea — draw it once, keep the Surface — and
for a level that fits in memory it is a large, free win. `code/04` measures both.

Where it stops working: a 500 × 500 tile level at 32 px is a **16,000 × 16,000** Surface, which is about
a gigabyte. The usual answer is to pre-render in **chunks** — a screen's worth at a time — which is the
right idea to know about and more than this level needs.

---

## The idea, in pictures

Open [tile collision, one axis at a time](../../../shared/visualizers/tile-collision.html).

**What to look for:** the dashed box is where the player *tried* to go; the solid box is where they
ended up. Step one frame at a time and watch the two separate corrections — **red** horizontal, **orange**
vertical. The yellow outlines show that only the handful of tiles the box touches are ever tested. Then
switch on "move both axes at once" and walk diagonally into a corner: the player climbs the wall, and
nothing in that code looks wrong.

Then open [grids and flat arrays](../../../shared/visualizers/tilemap-indexing.html) for the `col`/`row`
arithmetic on its own.

---

## The idea, in code

1. `code/01-load-a-level.py` — read `level.txt`, validate it, draw it, and show the column and row under
   the mouse. Includes a switch that loads a deliberately broken file.
2. `code/02-tile-collision.py` — the two-step move with every tested tile outlined, and a key for the
   one-step version so you can watch the player climb.
3. `code/03-edit-and-reload.py` — press R to reload `level.txt` while the game runs. Edit the file in
   another window and watch the world change.
4. `code/04-pre-rendered.py` — per-tile drawing against one pre-rendered Surface, timed, with the tile
   count and the milliseconds on screen.

---

## The maths you just used

**1. Floor division.** `x // TILE` answers "how many whole tiles fit before this point?". For positive
numbers it agrees with `int(x / TILE)`; for negative ones it does not — `-5 // 32` is `-1`, which is
right, and `int(-5 / 32)` is `0`, which lets a player stand in the left wall.

**2. The remainder.** `x % TILE` is how far *into* the tile you are. Useful for snapping and for
pixel-perfect edges, and it is the partner of the division.

**3. How many tiles can a box overlap?** If the box is no larger than a tile, at most **two per axis**,
so four in all: the left edge is in some column, and the right edge is at most one column further on.
Worth proving to yourself on paper, because it says the collision cost does **not** grow with the level.

**4. The size of a pre-rendered Surface.** `cols × TILE × rows × TILE × 4 bytes`. For 500 × 500 tiles at
32 px that is about 1 GB — which is why chunking exists. Doing that multiplication before you write the
code is a habit worth having.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Use `int(x / TILE)` instead of `x // TILE`, then walk off the left edge | | |
| Remove the `- 1` from `c1` and walk down a gap exactly your own width | | |
| Make `tile_at` return `"."` out of bounds instead of `"#"` | | |
| Resolve Y before X | | |
| Use `rstrip()` instead of `rstrip("\n")` on a level that uses spaces | | |
| Delete one character from one row of `level.txt` | | |
| Run the game from a different folder | | |
| Set `on_ground = True` on any collision rather than the downward one | | |
| Make the level 400 × 400 and pre-render it | | |

The last one will either be very slow or run out of memory, and doing the multiplication first — about a
gigabyte — is the point.

---

## Think like an engineer

1. The tile table holds **properties**. Where does that stop working? Think about a door that opens, a
   platform that moves, or a button that remembers it was pressed.
2. Our level is a list of strings. Alternatives: a list of lists, a flat `bytearray`, or a proper format
   like Tiled's `.tmx`. What does each make easy? Which would you pick for a level 10,000 tiles wide?
3. **Design something.** A one-way platform: solid from above, pass-through from below. What must the
   collision code know that it does not know now?
4. **The hard one.** Your level has 200 coins, and collecting one changes the world — but the level is
   also what you draw and what you collide against. Where does "this coin is taken" live? Three options:
   edit the level in memory, keep a separate set of taken positions, or keep two layers. Pick one, and
   say what happens when the level restarts.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Tile / tilemap** | One square of the grid; the grid of them that makes a level. |
| **Legend** | The table from character to what that tile means. |
| **`//`** | Floor division. Rounds towards negative infinity. The right one here. |
| **Out of bounds** | Off the edge of the map. Here, treated as solid. |
| **Axis-separated resolution** | Move and fix X, then move and fix Y. Two steps, never one. |
| **`on_ground`** | Not a flag you set — what the downward collision test tells you. |
| **Culling** | Not drawing what cannot be seen. |
| **Pre-rendering** | Drawing the level once onto a Surface and blitting that. |
| **Chunking** | Pre-rendering a screen's worth at a time, for levels too big for one Surface. |

---

## Recap

- A grid makes a level **small, readable, instantly searchable and editable as text**.
- Load it with `Path(__file__).parent`, `rstrip("\n")` only, and a **row-length check**.
- `col = int(x // TILE)`. Use **floor division**, and treat out of bounds as **solid**.
- Put tile properties in a **table**; a new type is one line and the drawing code never grows.
- Collide in **two steps**. One step cannot know what to undo. Sliding comes free; `on_ground` comes
  from the downward test.
- Test only the tiles the box touches — at most four — and mind the `- 1`.
- **Pre-render** a level that fits in memory. Do the multiplication before you try it on a big one.

---

## Stretch goals

1. **One-way platforms** (question 3). One condition, enormous payoff, and lesson 9 will want it.
2. **A tileset.** Build a Surface of tile pictures in code and blit from it, instead of filling
   rectangles. Then give walls a different top edge from their middle.
3. **Auto-tiling.** Choose a wall's picture from which of its four neighbours are also walls. Sixteen
   combinations — find the pattern rather than writing sixteen cases.
4. **A level editor.** Click to place a tile, right-click to erase, and a key that writes `level.txt`
   back out. Then design a level with it.
5. **Chunked pre-rendering.** Pre-render one screen's worth at a time and throw away chunks you have
   moved away from. This is what lesson 7 would want if the level were enormous.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `03-edit-and-reload.py`, open `level.txt` on the projector, type a wall into it and press R. The world changes. That reaction is worth the whole hook. |
| 10–25 | **Concept.** The tile-collision visualizer, mostly on the "both axes at once" switch. Let them watch the player climb and ask what information the code is missing. |
| 25–40 | **Live-code** `load_level`, `tile_at` and the two conversions. Make the out-of-bounds decision out loud. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–5 are the core. |
| 120–140 | Break-it-on-purpose. The `- 1` one, by walking down a one-tile gap. |
| 140–150 | Recap. Lesson 7 makes the world bigger than the window. |

**Before the lesson:** put `level.txt` and the `.py` file in the same folder and check it runs from a
different working directory. The `Path(__file__).parent` line prevents a confusing first ten minutes.

**What usually goes wrong**

1. **`FileNotFoundError`**, because the game was run from a different folder. Fix it once, properly, in
   front of them.
2. **The level has an extra empty row at the bottom**, from the trailing newline.
3. **`IndexError: string index out of range`**, from a row that is shorter than the others. The
   load-time check prevents it, which is the argument for having one.
4. **The player sticks in gaps their own width.** The missing `- 1`. Baffling without the explanation.
5. **The player climbs walls diagonally.** Both axes resolved at once. This is the lesson.
6. **The player sinks half a tile into the floor.** `round()` instead of `//`, or `int(x / TILE)` with a
   negative position.
7. **`on_ground` set by any collision**, so they can jump off a wall by pressing into it. Some students
   will declare this a feature; it is also how wall-jumping works, which is a good conversation.

**If you are running short on time** — cut pre-rendering and `code/04`; it matters in lesson 7 more than
here. Cut water and spikes too, keeping floor and wall. Do **not** cut the two-step collision or the
`- 1`: lessons 7, 9 and 12 all stand on them.

**For the student who finishes at minute 90** — stretch goal 4 (a level editor) is the one they will
actually use, and it takes about twenty minutes once the two conversions work.

**The point to land at the end:** they typed a few hundred characters and got a world; twenty more lines
made it solid. The reason it was twenty lines rather than two hundred is that the data was shaped so the
questions they needed to ask were cheap to answer — and choosing that shape before writing the code is
what design means.
