# Lesson 4 — Sprites And Spritesheets

## Cheat sheet

### The three forms of drawImage

```js
drawImage(img, dx, dy);
drawImage(img, dx, dy, dw, dh);
drawImage(img, sx, sy, sw, sh,
               dx, dy, dw, dh);
```

Only the **nine-argument** form can take a piece of a sheet. Using the
four-argument one with a sheet puts the whole sheet on screen — the commonest bug
in this lesson.

```
s = SOURCE      (where to copy FROM)
d = DESTINATION (where to put it)
```

### Which cell of the grid

```js
const sx = column * FRAME_W;
const sy = row    * FRAME_H;
```

### The frame timer

```js
sprite.timer += dt;
while (sprite.timer >= FRAME_TIME) {
  sprite.timer -= FRAME_TIME;
  sprite.frame = (sprite.frame + 1) % FRAMES;
}
```

- **`while`**, not `if` — a slow frame may owe you two poses.
- **subtract**, do not zero — zeroing loses the leftover and drifts slow.
- **`%`** wraps the counter with no `if`.

### State chooses the animation

```js
const ANIMATIONS = {
  idle: { row: 0, frames: 2, fps: 2 },
  walk: { row: 1, frames: 6, fps: 8 }
};

if (state !== lastState) {
  frame = 0; timer = 0; lastState = state;
}
```

Compare `state !== lastState`, not `state === "walk"`: you want the moment it
**became** walk.

### Facing left

```js
ctx.save();
ctx.translate(x, y);
ctx.scale(-1, 1);
ctx.translate(-x, -y);
ctx.drawImage(/* ... */);
ctx.restore();
```

The two translates are because the mirror is about **x = 0**, not about the
sprite.

### Crisp pixels

```js
ctx.imageSmoothingEnabled = false;   // in draw()
const drawX = Math.round(pos.x);     // round when DRAWING, not when moving
```

```css
canvas { image-rendering: pixelated; }
```

### Loading

```js
const img = new Image();
img.onload = () => ready = true;
img.src = "hero.png";     // src LAST
```

Drawing before it loads draws **nothing**, with no error.

### A canvas is an image

```js
const sheet = document.createElement("canvas");
// draw into sheet.getContext("2d") …
ctx.drawImage(sheet, …);   // works exactly like a PNG
```

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Give three reasons real games put many poses in one image instead of one file per pose.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> In <code>drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh)</code>, which four numbers describe the image and which four describe the canvas?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why must the animation have its own timer rather than advancing one pose per game frame? Name two separate problems with the one-per-frame version.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why <code>while</code> rather than <code>if</code> in the frame timer?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> What does <code>(frame + 1) % FRAMES</code> do, and what does it save you writing?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A6.</span> Why should the character's <em>state</em> choose the animation, rather than the key being pressed? Give a practical benefit.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> You round the position when drawing but not when moving. Why both halves of that?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> Frames are 32&times;32 and the sheet has 6 columns and 3 rows. What are <code>sx</code> and <code>sy</code> for row 2, column 4? What is the whole sheet's size in pixels?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The game runs at 60 fps and <code>FRAME_TIME</code> is <code>1/8</code>. How many game frames pass per pose? How many poses in two seconds?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> What appears on screen, and why?

```js
// sheet is 192 x 32, frames are 32 x 32
ctx.drawImage(sheet, 100, 100, 32, 32);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> <code>FRAMES</code> is 6 and the current frame is 5. The <code>% FRAMES</code> has been deleted. What is <code>sx</code> next frame, and what is drawn?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B5.</span> <code>FRAME_TIME</code> is <code>1/8</code> = 0.125 s and the game runs at exactly 60 fps, so <code>dt</code> is 0.01667. The author wrote <code>timer = 0</code> instead of <code>timer -= FRAME_TIME</code>. Work out the real time each pose is held for, and how far behind the animation is after one minute.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> Nothing is drawn, and there is no error in the console. Name the most likely cause and a way to prove it.

```js
const img = new Image();
img.src = "hero.png";
ctx.drawImage(img, 0, 0, 32, 32, 100, 100, 32, 32);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The walk animation never gets past its first pose, however long the player walks.

```js
if (player.state === "walk") {
  player.frame = 0;
  player.timer = 0;
}
player.timer += dt;
while (player.timer >= FRAME_TIME) { /* ... */ }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The character disappears completely whenever they turn to face left. Explain and fix.

```js
ctx.save();
if (facing === -1) { ctx.scale(-1, 1); }
ctx.drawImage(sheet, sx, 0, FW, FH, x, y, FW, FH);
ctx.restore();
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C4.</span> The sprite is sharp when standing still and blurry while walking slowly. Smoothing is already off. What is left?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C5.</span> On a slow laptop the walk cycle plays in slow motion, while the character still moves at the right speed. Both bugs are in these four lines — name them.

```js
player.timer += 1;
if (player.timer >= 8) {
  player.timer = 0;
  player.frame = player.frame + 1;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 3 ship, or from `code/01-make-a-spritesheet.html`.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Build a spritesheet in code: an offscreen canvas, 6 cells across, with a figure in each whose legs are at different angles. Draw the finished sheet on screen at 3&times; size and look at it.</li>
<li><strong>Checkpoint 2.</strong> Draw <em>one</em> cell of it with the nine-argument <code>drawImage</code>. Add two keys that step the frame index up and down by hand, and watch <code>sx</code> change.</li>
<li><strong>Checkpoint 3.</strong> Add the frame timer so it animates by itself. Put the pose number and the timer on screen while you work &mdash; you cannot debug what you cannot see.</li>
<li><strong>Checkpoint 4.</strong> Add a second row for &ldquo;idle&rdquo; (two slow poses) and an <code>ANIMATIONS</code> table. Make the character's <em>state</em> pick the row, and reset the frame when the state changes.</li>
<li><strong>Checkpoint 5.</strong> Make them face the way they are moving, using <code>scale(-1, 1)</code> and the two translates. Test by walking left, right, then stopping &mdash; they should keep facing the way they last went.</li>
<li><strong>Checkpoint 6.</strong> Turn smoothing off and round the draw position. Compare a sprite drawn at <code>x</code> with one drawn at <code>Math.round(x)</code>, side by side, moving very slowly.</li>
<li><strong>Checkpoint 7.</strong> Add a switch that advances one pose per game frame, so you can show somebody the difference. Keep it; it is the best demonstration in the lesson.</li>
</ul>

<div class="note">
<span class="note-label">If nothing appears</span>
<p>Draw a bright filled rectangle at exactly the same destination coordinates
first. If the rectangle appears and the sprite does not, the problem is the
<em>source</em> rectangle or the image not being ready &mdash; not the position.
That one test saves a lot of time.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** A sprite is drawn from a point: top-left, centre, or middle of the feet.
Choose one for a platform game and justify it. What happens when a character's
picture gets taller? What is the collision box measured from?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** A player moving at double speed still shows 8 poses a second, so their feet
slide. How would you tie animation speed to actual speed? What breaks if you tie
it too tightly — think about a character being pushed, or standing on a moving
platform.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design the state machine for a character who can be hurt while walking,
jumping or standing still. Does "hurt" interrupt, or play on top? What happens if
they are hurt twice in quick succession?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. Your sheet has 200 poses and you need team-red and team-blue
shirts. Three real options: ship two sheets, recolour once at load time, or draw a
separate shirt layer on top. Pick one, name its cost, and say what would make you
change your mind.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Animation fps proportional to actual speed, so the feet never slide.
2. Recolour your sheet at load time into two team colours.
3. A ping-pong animation: 0,1,2,3,2,1 — which `%` alone cannot do.
4. Write an atlas packer: a list of offscreen canvases in, one sheet plus a lookup
   of source rectangles out.
5. Onion skin: draw the previous two poses faintly behind the current one.
