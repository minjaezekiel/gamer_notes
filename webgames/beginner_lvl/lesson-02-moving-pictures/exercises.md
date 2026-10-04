# Lesson 2 — Moving Pictures

## Cheat sheet

### The screen is upside down

`(0, 0)` is the **top-left**.
`x` grows right. **`y` grows DOWN.**

| To move | Write |
|---|---|
| right | `x = x + s` |
| left | `x = x - s` |
| **up** | **`y = y - s`** |
| down | `y = y + s` |

### Velocity

Speed **with a direction**. The sign is the direction.

```js
speedX =  220   // rightwards
speedX = -220   // leftwards
speedY = -160   // UPWARDS
```

Bounce = **flip the sign**: `speedX = -speedX`

### Delta time

```js
let lastTime = 0;

function frame(currentTime) {
  if (!lastTime) lastTime = currentTime;
  let dt = (currentTime - lastTime) / 1000;
  lastTime = currentTime;
  if (dt > 0.1) dt = 1 / 60;   // CLAMP

  update(dt);
  render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

Then multiply **every** movement by `dt`:

```js
ball.x += ball.speedX * dt;
```

Now the speed is **pixels per second**, not per frame.

### distance = speed × time

At 60 fps, `dt ≈ 0.0167`, so
`120 × 0.0167 ≈ 2` pixels.

### Bouncing, correctly

```js
if (ball.x + ball.radius > canvas.width) {
  ball.x = canvas.width - ball.radius; // FIRST
  ball.speedX = -ball.speedX;          // THEN
}
```

Test the **edge**, not the centre.
Fix the **position** before the **velocity**,
or the ball vibrates against the wall.

### Words

**dt** — seconds the last frame took.
**Clamp** — force a number into sensible limits.
**Radius** — centre to edge.

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> On a canvas, which direction does <code>y</code> get bigger in? Write the line of code that moves something <em>up</em>.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does <code>dt</code> stand for, and what does it actually measure?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> What is the difference between <em>speed</em> and <em>velocity</em>?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> A ball moves at 300 pixels per second. The last frame took 0.02 seconds. How far did it move this frame? Show your working.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why must you <em>clamp</em> <code>dt</code>? Give two different situations where an unclamped <code>dt</code> would be huge.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

**Write your prediction down before running anything.**

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> A game moves a square with <code>x = x + 4</code> each frame. On your 60 fps laptop it crosses a 600-pixel canvas in 2.5 seconds. Your friend has a 144 fps monitor. How long does it take on their machine? Show your working.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The ball starts at <code>y = 100</code> with <code>speedY = -90</code>. Where is it one second later, and is that higher or lower on the screen?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> What is drawn here, and where does the ball end up?

```js
let dt = (currentTime - lastTime) / 1000;
// lastTime is never updated
update(dt);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> A student starts their loop with <code>frame()</code> instead of <code>requestAnimationFrame(frame)</code>. The ball disappears completely and never comes back. Explain the chain of events. What is the value of <code>ball.x</code> after the first frame?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The ball reaches the right wall and then shivers against it forever instead of bouncing away. Explain what happens on each of the first three frames after it touches the wall, then write the fix.

```js
ball.x = ball.x + ball.speedX * dt;

if (ball.x + ball.radius > canvas.width) {
  ball.speedX = -ball.speedX;
}
```

<div class="lines"><i></i><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The ball sinks halfway into every wall before bouncing back out. The bounce itself works. What is wrong?

```js
if (ball.x > canvas.width) {
  ball.x = canvas.width;
  ball.speedX = -ball.speedX;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The ball is somewhere near the middle when the page loads, then instantly vanishes. The console shows no errors at all. What is the most likely cause, and why does it produce no error message?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 1 file, or from `code/02-delta-time.html`.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Add the <code>dt</code> calculation to your loop, including the clamp. Draw <code>dt</code> and <code>Math.round(1 / dt)</code> on screen so you can see them. What frame rate is your machine running at?</li>
<li><strong>Checkpoint 2.</strong> Replace your square with a circle using <code>ctx.arc</code>, and store its numbers in a single <code>ball</code> object rather than loose variables.</li>
<li><strong>Checkpoint 3.</strong> Give the ball <code>speedX</code> and <code>speedY</code> in <em>pixels per second</em>, and move it with <code>* dt</code>. It should drift diagonally off the screen.</li>
<li><strong>Checkpoint 4.</strong> Make it bounce off all four walls. Remember: test the <strong>edge</strong>, and fix the <strong>position before the velocity</strong>.</li>
<li><strong>Checkpoint 5.</strong> Prove your delta time works. Open the page in two windows, drag one around constantly to make its frame rate wobble, and check both balls stay in step. (They will drift apart eventually &mdash; think about why that is <em>not</em> the same bug.)</li>
<li><strong>Checkpoint 6.</strong> Add gravity: <code>ball.speedY = ball.speedY + 600 * dt;</code> at the top of update. Then make the floor bounce lose energy with <code>-0.8</code> instead of <code>-1</code>.</li>
</ul>

<div class="note">
<span class="note-label">If the ball flies off the screen the instant you load the page</span>
<p>You have not clamped <code>dt</code>. The first frame is measuring the whole page-load time, so
the ball is being told to move several seconds' worth in one go. This is the single most common bug
in this lesson &mdash; everybody hits it.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on your reasoning. Name what your idea costs, not only what it gains.</p>
</div>

Delta time fixes *movement*. But other things in a game can be measured in frames by accident.

**E1.** For each of these, describe exactly what a player on a 144 fps monitor would experience, then
write the fixed version:

1. An enemy that fires every 30 frames.
2. An explosion animation that advances one picture per frame.
3. A countdown that does `secondsLeft = secondsLeft - 1` each frame.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

**E2.** Is there any situation where counting frames genuinely *is* the right choice? Competitive
fighting games describe moves as "7 frames of startup", and tournament players really do count
frames. What is different about that situation?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Delta time makes the game fair across machines, but it also makes it **non-deterministic**:
run the same game twice with the same button presses and you get slightly different results, because
the frame times are never identical. Why might that be a serious problem for online multiplayer, or
for a replay feature?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Many balls — if you start writing `ball1`, `ball2`, `ball3`, stop. That feeling is what an
   **array** is for.
2. A fading trail from the last 20 positions.
3. Draw a live frames-per-second readout. What makes the number move?
4. Make the ball change colour based on how fast it is going.
