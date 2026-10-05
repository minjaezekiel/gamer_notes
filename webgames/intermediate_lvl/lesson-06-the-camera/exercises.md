# Lesson 6 — The Camera

## Cheat sheet

### The whole lesson

```js
screenX = worldX - camera.x;
screenY = worldY - camera.y;
```

and backwards, for the mouse:

```js
worldX = screenX + camera.x;
```

### Two coordinate systems

| | meaning |
|---|---|
| world | where it really is |
| screen | where it appears |

**Logic in world space. Convert only when drawing.** Name your variables
`worldX` / `screenX`.

### Following, in order of importance

```js
// 1. DEAD ZONE — the biggest win
const wanted = player.x - W / 2;
const gap = wanted - camera.x;
if (Math.abs(gap) > DEAD / 2) {
  camera.x += gap > 0 ? gap - DEAD / 2
                      : gap + DEAD / 2;
}

// 2. SMOOTHING (frame-rate safe)
const t = 1 - Math.exp(-SMOOTH * dt);
camera.x += (wanted - camera.x) * t;

// 3. LOOK-AHEAD
const wanted = player.x + player.vx * 0.25
               - W / 2;
```

### Clamping, with the trap

```js
if (worldW <= W) {
  camera.x = (worldW - W) / 2;   // small level: centre it
} else {
  camera.x = Math.max(0,
    Math.min(worldW - W, camera.x));
}
```

Clamp **after** smoothing. Clamp the camera, never the target.

### Applying it once

```js
ctx.save();
ctx.translate(-Math.round(camera.x),
              -Math.round(camera.y));
drawWorld();        // world coordinates
ctx.restore();

drawHud();          // OUTSIDE: does not scroll
```

`Math.round` the camera, or tiles show shimmering seams.

### Parallax

```js
sky    x - camera.x * 0.0
hills  x - camera.x * 0.3
trees  x - camera.x * 0.6
world  x - camera.x * 1.0
rain   x - camera.x * 1.4
```

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> Write the conversion from world space to screen space, and the one back again.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Why is &ldquo;<code>camera.x = player.x - width/2</code>&rdquo; unpleasant to play? Give two separate reasons.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> What is a <em>dead zone</em>, and which problem does it solve?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why should collision and physics use world space rather than screen space?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> What is the difference between drawing something inside <code>ctx.translate</code> and outside it? Give one thing that belongs in each.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why round the camera position, and what is the symptom if you do not?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A7.</span> Explain the trap in <code>Math.max(0, Math.min(worldWidth - canvasWidth, camera.x))</code>.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> The player is at world x = 1840 and the camera is at 1520. Where does the player appear on screen? If the canvas is 640 wide, are they left or right of centre?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> Someone clicks at screen x = 100 while the camera is at 1520. Which world x did they click? What world x would the un-converted version report?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> <code>camera.x</code> is 0 and <code>wanted</code> is 500, with smoothing <code>camera.x += (wanted - camera.x) * 0.1</code> each frame. Give the camera position after frames 1, 2 and 3. Does it ever reach 500?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> The world is 300 px wide and the canvas is 640. What does the clamp above produce, and what does the player see?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> A hill is at world x = 1000, the camera is at 600, and the parallax factor is 0.3. Where is the hill drawn? Where would it be drawn at factor 1.0?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The world scrolls the wrong way: walking right moves the level right as well.

```js
ctx.fillRect(thing.x + camera.x, thing.y + camera.y, thing.w, thing.h);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The score scrolls off the left-hand side of the screen as the player walks right.

```js
ctx.save();
ctx.translate(-camera.x, -camera.y);
drawWorld();
drawPlayer();
ctx.fillText("SCORE " + score, 10, 30);
ctx.restore();
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> Clicking places a block exactly where expected at the start of the level, and further and further off as the player walks right. Explain the shape of the error and fix it.

```js
canvas.addEventListener("click", function (e) {
  const b = canvas.getBoundingClientRect();
  placeBlock(e.clientX - b.left, e.clientY - b.top);
});
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> Collision stopped working the moment the camera was added. The player falls through floors. What has gone wrong?

```js
player.screenX = player.x - camera.x;
const col = Math.floor(player.screenX / TILE);
if (isSolid(col, row)) { /* ... */ }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> At the left-hand edge of the level, the camera judders back and forth every frame instead of sitting still.

```js
camera.x = Math.max(0, camera.x);
camera.x += (wanted - camera.x) * 0.1;
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 5 tilemap.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Make your level four screens wide. Add a <code>camera</code> object, set <code>camera.x = player.x - canvas.width / 2</code>, and apply it by subtracting in every draw call. Walk about. Note down how it feels &mdash; you will be comparing against this.</li>
<li><strong>Checkpoint 2.</strong> Show both coordinate systems on screen: <code>world x</code> and <code>screen x</code> for the player, side by side. Keep this readout for the rest of the lesson.</li>
<li><strong>Checkpoint 3.</strong> Switch to <code>ctx.save</code> / <code>translate</code> / <code>restore</code>, drawing everything in world coordinates. Then draw the score <em>after</em> <code>restore()</code> and confirm it stays put.</li>
<li><strong>Checkpoint 4.</strong> Clamp the camera to the level. Walk to both ends and check you never see outside the world. Then set your world width to 300 and make sure something sensible happens.</li>
<li><strong>Checkpoint 5.</strong> Add a dead zone, with a key to turn it on and off. Switch between them while walking in small steps. This is the comparison the whole lesson is for.</li>
<li><strong>Checkpoint 6.</strong> Add frame-rate-safe smoothing, and a slider or two keys to change it. Find a value you like and write it down.</li>
<li><strong>Checkpoint 7.</strong> Add look-ahead based on the player's velocity. Try 0.1, 0.25 and 1.0 seconds of it and decide which you prefer.</li>
<li><strong>Checkpoint 8.</strong> Add two parallax background layers, then convert mouse clicks to world space and place a block where you click. Scroll to the far end and check it still lands correctly.</li>
</ul>

<div class="note">
<span class="note-label">If something is in the wrong place</span>
<p>Draw the camera rectangle's world coordinates on screen as text, and draw a
marker at world (0, 0). If the marker is not at screen <code>(-camera.x, -camera.y)</code>,
your conversion is wrong. If it is, the conversion is right and the thing in the
wrong place is being drawn in the wrong space.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** Name three things a camera might follow or do other than tracking the
player, and say what each is for.

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** Two players, one screen, and they can walk apart. The camera cannot centre
on both. Design something — and say what happens when they are further apart than
the screen is wide. There is a decision there that cannot be avoided.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** A camera that zooms out when the player moves fast. What changes about
drawing? What breaks about tile culling? What breaks about a dead zone measured in
pixels?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. Three things want to control `camera.x`: following the
player, a screen shake, and a cut-scene that moves to fixed points. How do you
structure that so they do not fight, and so a fourth can be added next month?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. A vertical dead zone much larger than the horizontal one. Find the numbers.
2. Snap the camera on landing, lag it in the air.
3. Look-ahead that swings smoothly when the player turns, rather than jumping.
4. Edge triggers: move a whole screen at a time, as the first Zelda did. Then argue
   about which is better.
5. Zoom (E3). `ctx.scale` is only the beginning.
