# Lesson 5 — Tilemaps

## Cheat sheet

### The level

```js
const TILE = 32;
const LEVEL = [
  "####################",
  "#..................#",
  "#..###....####.....#",
  "####################"
];
```

### The two conversions

```js
col = Math.floor(x / TILE);   // position → square
x   = col * TILE;             // square → position
```

**`floor`, not `round`.** `floor(-1.2) = -2`, which is right; chopping gives
`-1`, which lets the player stand in the left wall.

### Reading it safely

```js
function tileAt(col, row) {
  if (col < 0 || row < 0 ||
      row >= LEVEL.length ||
      col >= LEVEL[0].length) return "#";
  return LEVEL[row].charAt(col);
}
```

**Out of bounds counts as solid.** One decision, a whole class of bug gone.

### Tiles as a table, not as `if`s

```js
const TILES = {
  ".": { solid: false, colour: "#121820" },
  "#": { solid: true,  colour: "#3c4756" },
  "^": { solid: false, deadly: true }
};
```

A new tile type is one line. The drawing code never grows.

### Which tiles does the box touch?

```js
c0 = floor( box.x               / TILE);
c1 = floor((box.x + box.w - 0.001) / TILE);
r0 = floor( box.y               / TILE);
r1 = floor((box.y + box.h - 0.001) / TILE);
```

At most **4 tiles**, whatever the size of the level. The `- 0.001` stops a box
whose edge is exactly on a boundary from counting the next column — without it
the player sticks in gaps exactly their own width.

### Collision: TWO steps, never one

```js
// X
x += vx * dt;
if (hit) {
  x = vx > 0 ? hit.col * TILE - w
             : (hit.col + 1) * TILE;
  vx = 0;
}
// Y
y += vy * dt;
if (hit) {
  if (vy > 0) { y = hit.row * TILE - h;
                onGround = true; }
  else        { y = (hit.row + 1) * TILE; }
  vy = 0;
}
```

One step cannot know **which** direction to undo. Two steps always know.

Sliding along walls comes free. `onGround` comes out of the **downward** test.

### Only draw what is visible

```js
firstCol = floor(camera.x / TILE);
lastCol  = floor((camera.x + W) / TILE) + 1;
```

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Give three advantages a grid has over a list of arbitrary rectangles.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> Why <code>Math.floor</code> rather than <code>Math.round</code>, and why rather than chopping off the decimals?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> Why does <code>tileAt</code> return a wall for positions off the map? Name two problems that removes.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Why must collision be resolved one axis at a time? What information does the one-step version not have?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Where does <code>onGround</code> come from, and why is it not something you set when a key is pressed?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> What is the <code>- 0.001</code> for? What is the symptom without it?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> Why put tile properties in a table instead of using <code>if</code> statements?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> <code>TILE</code> is 32. Which column and row is the point (95, 64) in? What is the top-left corner of that square?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> A player box is at x = 60, y = 30, 26 wide and 26 tall. <code>TILE</code> is 32. Which columns and rows does it touch? How many squares is that?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> Same player, now at exactly x = 64. With the <code>- 0.001</code>, which columns does it touch? Without it?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> A player 26 tall is falling with <code>vy</code> = 500 and <code>dt</code> = 0.1, starting at y = 100. There is a floor of solid tiles in row 5. Where do they end up, and what is <code>vy</code> afterwards? (<code>TILE</code> = 32.)
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> A level is 300 &times; 300 tiles and the screen shows 25 &times; 16 of them. How many tiles does the naive draw loop visit per frame? How many does the culled one?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The player sinks exactly 16 pixels into the floor. <code>TILE</code> is 32.

```js
const row = Math.round(y / TILE);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Walking diagonally into a corner makes the player climb the wall. Name the bug and describe the fix.

```js
player.x += player.vx * dt;
player.y += player.vy * dt;
const hit = findSolidOverlap(player);
if (hit) {
  player.x -= player.vx * dt;
  player.y -= player.vy * dt;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The console says <code>Cannot read properties of undefined (reading 'charAt')</code> when the player reaches the top of the level.

```js
function tileAt(col, row) {
  return LEVEL[row].charAt(col);
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The player can jump for ever by holding into a wall. Both halves of this snippet contribute &mdash; name them.

```js
const hit = findSolidOverlap(player);
if (hit) {
  player.onGround = true;
  player.vy = 0;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> The right-hand quarter of the level has no walls in it at all, although the author typed them. The level loads with no error.

```js
const LEVEL = [
  "####################",
  "#..................#",
  "#..###....####.#",
  "####################"
];
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write your level as an array of strings and draw it with coloured rectangles. Add a check at startup that every row is the same length, and make it complain loudly if not.</li>
<li><strong>Checkpoint 2.</strong> Write <code>tileAt</code> with the out-of-bounds rule, and <code>isSolid</code> using a <code>TILES</code> table. Print the column and row under the mouse pointer so you can see the conversion working.</li>
<li><strong>Checkpoint 3.</strong> Add a player box that moves with the arrow keys. No collision yet &mdash; walk through walls on purpose, and draw an outline on every tile your box is touching. You should see at most four.</li>
<li><strong>Checkpoint 4.</strong> Add the two-step collision. Test: walk into a wall head-on, then walk into it diagonally. You should slide along it without writing any sliding code.</li>
<li><strong>Checkpoint 5.</strong> Add gravity and make <code>onGround</code> come out of the downward test. Draw <code>onGround</code> on screen as a word. Then add a jump that only works when it is true.</li>
<li><strong>Checkpoint 6.</strong> Add two more tile types from your table &mdash; spikes that reset the player and coins that score. Neither should need a change to the drawing code.</li>
<li><strong>Checkpoint 7.</strong> Put the level in a <code>&lt;textarea&gt;</code> and reload it as you type. Then redesign your level by typing.</li>
<li><strong>Checkpoint 8.</strong> Add the broken one-step collision on a key, so you can demonstrate the difference to somebody.</li>
</ul>

<div class="note">
<span class="note-label">If the player sticks in gaps</span>
<p>Print <code>c0</code>, <code>c1</code>, <code>r0</code> and <code>r1</code> on screen and walk
slowly. If <code>c1</code> jumps forward one square before the player has actually
crossed into it, you need the <code>- 0.001</code>.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** The tile table holds *properties*. Where does that approach break down?
Think about a tile that needs *behaviour* — a door that opens, a platform that
moves, a button that does something when stood on.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Our level is an array of strings. Alternatives: a flat array of numbers,
an array of arrays, one long string with newlines. What does each make easy, and
awkward? Which would you pick for a level 10,000 tiles across, and why?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design a one-way platform: solid from above, pass-through from below. What
must the collision code know that it currently does not?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** The hard one. 200 coins, and collecting one changes the map — but the map
is also what you draw and what you collide against. Where does "this coin is
taken" live? Change the level array, keep a separate list, or keep two layers?
Pick one, name its cost, and say what happens when the level restarts.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. One-way platforms (E3). One condition.
2. Draw tiles from a tileset built in code, as in lesson 4.
3. Auto-tiling: pick a wall's picture from which of its four neighbours are walls.
   Sixteen combinations — find the pattern rather than writing sixteen cases.
4. A level editor: click to place, right-click to erase, and a button that prints
   the level back out as text.
5. Slopes. Genuinely hard. Attempt it and write down exactly which assumption breaks.
