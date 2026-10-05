# Lesson 5 — Tilemaps

> **Web Games · Intermediate level · Lesson 5 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A world. Not a screen with some rectangles on it — a **level**, made of solid walls you cannot walk
through, written as text you can edit while the game is running.

```js
const LEVEL = [
  "####################",
  "#..................#",
  "#..###....####.....#",
  "#....#.......#..@..#",      //  @ is where the player starts
  "#....#..##...#.....#",
  "#.......##.........#",
  "#..####.......###..#",
  "####################"
];
```

That is the entire level. Twenty characters by eight, and by the end of the lesson you will be able to
redraw the whole world by typing in a box.

## Where this fits

- **Back:** [lesson 4](../lesson-04-sprites-and-spritesheets/notes.md) gave you `drawImage` with a
  source rectangle. A tile is exactly that, used 160 times instead of once.
- **Forward:** [lesson 6](../lesson-06-the-camera/notes.md) makes the world bigger than the screen.
  [Lesson 12](../lesson-12-capstone-a-platformer/notes.md) adds gravity and jumping to today's
  collision code without changing it.
- **Other tracks:** the C++ beginner track already did this with a 2-D array as a screen buffer, and
  Python's intermediate lesson 6 loads one from a file. The grid arithmetic is identical everywhere.

---

## The idea, in plain words

### Why a grid, when a game could be any shape

A level could be a list of arbitrary rectangles. Some games do that. A grid is better for almost
everything a 13-year-old wants to make, for four reasons:

1. **It is tiny.** 160 characters for the level above. The equivalent list of rectangles is pages.
2. **You can see it.** The data *looks like* the level. That is rare and worth a great deal.
3. **Looking things up is instant.** "Is there a wall at this spot?" is one division and one array
   lookup — not a loop over every wall in the level.
4. **Editing it is editing text.** No tools to build, no file format to invent.

Point 3 is the one that matters most and is the least obvious. With a list of rectangles, checking the
player against the world means testing every single rectangle, every frame. With a grid, you work out
*which* square the player is standing in and look only there. It is the difference between asking
everybody in a school whether they are in your seat, and looking at your seat.

### The map analogy, and where it breaks

A tilemap is squared paper. Each square is one thing: wall, floor, water, ladder.

Where it breaks: **squared paper has no thickness and your player does.** The player is a box that
sits across square boundaries most of the time. A player 26 pixels wide on 32-pixel tiles is touching
**two** columns almost always, and four squares whenever they are also between rows. Nearly every
tilemap bug is a failure to think about that overlap.

### The two conversions, which you will use constantly

```js
const TILE = 32;

// world position  →  which square
const col = Math.floor(x / TILE);
const row = Math.floor(y / TILE);

// which square  →  world position (the square's top-left corner)
const x = col * TILE;
const y = row * TILE;
```

`Math.floor`, not `Math.round`. Position 95 with 32-pixel tiles is in column 2 (`95/32 = 2.97`), and
rounding would wrongly say 3. And `Math.floor` is also right for negative numbers in a way that simply
chopping off the decimals is not: `Math.floor(-0.5)` is `-1`, which is correct, while `-0.5 | 0` is
`0`, which would let a player stand just outside the left wall.

### Reading the map safely

```js
function tileAt(col, row) {
  /* OUT OF BOUNDS COUNTS AS SOLID. This single decision removes a whole class
     of bug: no "undefined is not a function", no player wandering off the edge
     of the array into nothing, and no separate screen-edge code. */
  if (col < 0 || row < 0 || row >= LEVEL.length || col >= LEVEL[0].length) {
    return "#";
  }
  return LEVEL[row].charAt(col);
}

function isSolid(col, row) {
  return TILES[tileAt(col, row)].solid;
}
```

Treating off-the-map as wall is the kind of small choice that separates code that mostly works from
code that works. It also means you can delete the border of `#` from your level and the player still
cannot escape.

### Tiles as data, not as `if`s

The temptation is `if (tile === "#") { ... } else if (tile === "~") { ... }`. Resist it. Put the
*properties* in a table:

```js
const TILES = {
  ".": { solid: false, colour: "#121820", name: "floor" },
  "#": { solid: true,  colour: "#3c4756", name: "wall" },
  "~": { solid: false, colour: "#1c4f7c", name: "water",  slows: true },
  "^": { solid: false, colour: "#7c2d2d", name: "spikes", deadly: true },
  "o": { solid: false, colour: "#ffd43b", name: "coin",   collectable: true }
};
```

Now adding a tile type is adding one line, and the drawing code never grows at all — it asks the table
what colour to use. This is the "data, not code" idea from the beginner capstone, and it is the single
habit that most reliably keeps a game from collapsing under its own weight.

### Collision: the thing that has to be done in two steps

Here is the part everybody gets wrong first, and the reason it has its own visualizer.

The obvious approach: add the whole movement, check if the player is inside a wall, and if so undo it.
It fails, and it fails in a way that is very hard to read from the code. When the player moves
diagonally into a corner, the code knows they are in a wall but has **no information about which
direction caused it**, so it has to guess. Guess wrong and the player climbs walls, sticks to them, or
is pushed through them.

The fix is to never create that ambiguity:

```js
/* ---- STEP 1: move on X ONLY, then fix X only ---- */
player.x = player.x + player.vx * dt;
const hitX = findSolidOverlap(player);
if (hitX) {
  if (player.vx > 0) {
    player.x = hitX.col * TILE - player.w;      // flush against its left edge
  } else {
    player.x = (hitX.col + 1) * TILE;           // flush against its right edge
  }
  player.vx = 0;
}

/* ---- STEP 2: now move on Y ONLY, from the corrected X ---- */
player.y = player.y + player.vy * dt;
const hitY = findSolidOverlap(player);
if (hitY) {
  if (player.vy > 0) {
    player.y = hitY.row * TILE - player.h;
    player.onGround = true;                     // ← this is how a platformer
  } else {                                      //   knows it has landed
    player.y = (hitY.row + 1) * TILE;
  }
  player.vy = 0;
}
```

Because each step moved in only one direction, each step *knows* which direction to undo. No guessing.

Two consequences worth noticing:

- **Sliding along a wall is free.** Walk diagonally into a wall: X is cancelled, Y is not, so you slide
  along it. That feels right, and you did not write any code for it.
- **The Y step is where "on the ground" comes from.** `onGround` is not a thing you set when you press
  a key. It is what the downward collision test tells you. Lesson 12 depends entirely on this.

### Only test the tiles you are touching

```js
function findSolidOverlap(box) {
  // The range of squares this box touches. The -0.001 matters: a box whose right
  // edge is exactly on a boundary should not count the next column along.
  const c0 = Math.floor(box.x / TILE);
  const c1 = Math.floor((box.x + box.w - 0.001) / TILE);
  const r0 = Math.floor(box.y / TILE);
  const r1 = Math.floor((box.y + box.h - 0.001) / TILE);

  for (let row = r0; row <= r1; row++) {
    for (let col = c0; col <= c1; col++) {
      if (isSolid(col, row)) { return { col: col, row: row }; }
    }
  }
  return null;
}
```

For a player smaller than a tile that is at most four squares, whatever the size of the level. A 500 ×
500 tile world has a quarter of a million tiles, and this looks at four of them. That is the real
reason for the grid.

That `- 0.001` is an ugly little thing and it is load-bearing. Without it, a player whose right edge
lands exactly on `x = 64` is counted as touching column 2, so a wall in column 2 pushes them back even
though they are only *adjacent* to it. The symptom is a player who gets stuck in gaps exactly their own
width — the classic tilemap bug.

### Drawing: only what is on screen

Drawing all 250,000 tiles of a large map, every frame, when 300 of them are visible, is the most
common performance mistake in tile games. Work out the visible range and loop over that:

```js
const firstCol = Math.floor(camera.x / TILE);
const lastCol  = Math.floor((camera.x + canvas.width) / TILE) + 1;   // +1: the partly-visible one
const firstRow = Math.floor(camera.y / TILE);
const lastRow  = Math.floor((camera.y + canvas.height) / TILE) + 1;
```

`code/04-only-draw-whats-visible.html` counts the draw calls both ways on a 300 × 300 map. The
difference is not subtle.

---

## The idea, in pictures

Open [tile collision, one axis at a time](../../../shared/visualizers/tile-collision.html).

**What to look for:** the dashed box is where the player *tried* to go; the solid box is where they
ended up. Step one frame at a time and watch the two separate corrections — **red** is horizontal,
**orange** is vertical. Notice the yellow outlines: only the handful of tiles the box is touching are
ever tested. Then switch on "move both axes at once" and walk diagonally into a corner. The player
climbs the wall. Nothing in that code looks wrong, which is exactly why this is worth seeing before
you write it.

Then open [grids and flat arrays](../../../shared/visualizers/tilemap-indexing.html) for the
`col`/`row` arithmetic on its own.

---

## The idea, in code

Work through the examples in order.

1. `code/01-draw-a-tilemap.html` — a level as text, drawn, with a live readout of which square the
   mouse is in.
2. `code/02-tile-collision.html` — the two-step move, with every tested tile outlined and a switch to
   run the broken one-step version.
3. `code/03-level-as-data.html` — edit the level in a text box while the game runs, with a tile table
   that includes water, spikes and coins.
4. `code/04-only-draw-whats-visible.html` — a 300 × 300 map, with the draw count shown both ways.

---

## The maths you just used

**1. Integer division by flooring.** `Math.floor(x / TILE)` answers "how many whole tiles fit before
this point?", which is exactly the column number. The partner operation is the remainder:
`x % TILE` tells you how far *into* the tile you are, which is what you need for pixel-perfect edge
cases and for drawing something aligned to the grid.

**2. Why `floor` and not truncation.** For positive numbers they agree. For negative ones they do not:
`Math.floor(-1.2)` is `-2`, while chopping the decimal gives `-1`. A player at `x = -5` is genuinely in
column −1, not column 0, and getting that wrong lets them stand in the wall at the left edge.

**3. How many tiles can a box overlap?** If the box is no larger than a tile, the answer is at most
**2 in each direction**, so 4 in total. Why: the box's left edge is in some column, and its right edge
is at most one tile further on. Worth proving to yourself with a drawing, because it tells you that the
collision cost does not grow with the level.

**4. Grid to flat array.** We used an array of strings, where `LEVEL[row].charAt(col)` is natural. A
single flat array is the other common choice, and then the index is `row * WIDTH + col` — the same
formula the C++ track used for its screen buffer. One line, two ways of thinking, and the same grid.

---

## Break it on purpose

Use `code/02-tile-collision.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Switch on "move both axes at once", then walk diagonally into a corner | | |
| Remove the `- 0.001` and walk down a gap exactly the player's width | | |
| Make `tileAt` return `"."` for out of bounds instead of `"#"` | | |
| Use `Math.round` instead of `Math.floor` in the conversion | | |
| Resolve Y before X | | |
| Make the player 40 px wide on 32 px tiles | | |
| Forget `player.vx = 0` after the X correction | | |
| Set `onGround = true` whenever any collision happens | | |

The player-wider-than-a-tile one is the most interesting: predict whether your four-tile test is still
enough, then test it against a single pillar.

---

## Think like an engineer

1. We put tile properties in a table so that adding a type costs one line. Where does that approach
   start to break down? (Think about a tile that needs *behaviour* rather than properties — a door that
   opens, a platform that moves.)
2. The level is an array of strings. Alternatives: a flat array of numbers, an array of arrays, or a
   string with newlines. Each is used in real games. What does each make easy, and what does each make
   awkward? Which would you choose if a level could be 10,000 tiles across?
3. **Design something.** A one-way platform: solid from above, pass-through from below, so the player
   can jump up through it and then stand on it. You already have everything you need. What must the
   collision code know that it does not currently know?
4. **The hard one.** Your level has 200 coins, and collecting one must change the map. But the map is
   also the thing you draw and the thing you test collisions against. Where does "this coin has been
   taken" live? Three options: change the level array, keep a separate list of taken coins, or keep two
   layers. Pick one and say what it costs. (Think about restarting the level.)

Question 3 is in essentially every platform game ever made, and the answer is one condition.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Tile** | One square of the grid. Also the image drawn in it. |
| **Tilemap** | The grid of tiles that makes up a level. |
| **Tileset** | The image holding every tile's picture. A spritesheet for tiles. |
| **Legend** | The table mapping a character to what that tile means. |
| **`Math.floor(x / TILE)`** | World position → column. |
| **Out of bounds** | Off the edge of the map. Here, treated as solid. |
| **Axis-separated resolution** | Move and fix X, then move and fix Y. Two steps, never one. |
| **Culling** | Not drawing what cannot be seen. |
| **`onGround`** | Not a flag you set — what the downward collision test tells you. |
| **Data-driven** | Behaviour decided by a table you edit, not by code you rewrite. |

---

## Recap

- A grid makes a level **small, readable, instantly searchable, and editable as text**.
- `col = Math.floor(x / TILE)`. Use `floor`, and treat out of bounds as **solid**.
- Put tile properties in a **table**, so a new tile type is one line and the drawing code never grows.
- Collide in **two steps**: move X, fix X, then move Y, fix Y. One step cannot know what to undo.
- Test only the tiles the player's box touches — at most four, whatever the size of the level.
- `onGround` comes out of the **downward** collision test. Lesson 12 depends on that.

---

## Stretch goals

1. **One-way platforms** (question 3). One condition, enormous payoff.
2. **A tileset.** Build an offscreen tileset in code as in lesson 4, and draw tiles with `drawImage`
   instead of coloured rectangles. Then give walls a different top edge from their middle.
3. **Auto-tiling.** Choose a wall's picture based on which of its four neighbours are also walls. There
   are 16 combinations; work out the pattern rather than writing 16 cases.
4. **A level editor.** Click to place a tile, right-click to erase, and a button that prints the level
   back out as text you can paste into your code.
5. **Slopes.** Genuinely hard, and worth attempting to find out why. A 45° slope breaks the assumption
   that a tile is either solid or not.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Project `03-level-as-data.html` and edit the level live in front of them. Add a wall by typing `#`. The reaction to the world changing as you type is worth the whole hook. |
| 10–25 | **Concept.** The tile-collision visualizer. Spend the time on the "both axes at once" switch: let them watch the player climb the wall, and ask what information the code is missing. |
| 25–40 | **Live-code** `tileAt`, `isSolid` and the conversions. Make the out-of-bounds decision out loud and explain why. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–4 are the core. |
| 120–140 | Break-it-on-purpose. The `- 0.001` one is the best: have them walk down a gap exactly their own width. |
| 140–150 | Recap. Lesson 6: the world gets bigger than the screen. |

**What usually goes wrong**

1. **The player gets stuck in gaps their own width.** The `- 0.001` is missing, so touching a boundary
   counts as being in the next column. Extremely common and completely baffling without the explanation.
2. **The player climbs walls when moving diagonally.** They resolved both axes at once. This is the
   lesson; the visualizer is there for exactly this moment.
3. **`undefined` errors from `tileAt`.** No out-of-bounds check, and the player walked off the array.
4. **`Math.round` instead of `Math.floor`.** Collisions are half a tile off, and the player sinks into
   the floor by sixteen pixels. The symptom does not obviously point at the cause.
5. **The whole map is drawn every frame.** Fine at this size, and worth naming now so that lesson 6 does
   not slow to a crawl.
6. **`onGround` set on any collision.** The player can then jump off a wall by pressing into it, which
   some students will declare a feature. It is a bug, and it is also how wall-jumping works, so this is
   a good conversation.
7. **The level array has rows of different lengths.** One short row and the right-hand side of the world
   has a hole in it. Suggest a check at startup: all rows the same length, or refuse to start.

**If you are running short on time** — cut `code/04` and the culling section; it matters in lesson 6
rather than today. Cut the water and spike tiles too, keeping only floor and wall. Do **not** cut the
two-step collision or the `- 0.001`: everything after this lesson stands on them.

**For the student who finishes at minute 90** — stretch goal 1 (one-way platforms) first, then stretch
goal 3 (auto-tiling), which is the best "work out the pattern instead of writing 16 cases" exercise in
the whole course.

**The point to land at the end:** they typed 160 characters and got a world. Then they wrote about
twenty lines and the world became solid. The reason it took twenty lines rather than two hundred is
that the data was shaped so that the questions they needed to ask were cheap to answer — and choosing
that shape, before writing the code, is what design means.
