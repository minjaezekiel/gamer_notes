# Lesson 5 — Rules, Score And Feel

## Cheat sheet

### One variable, not four flags

```js
let state = "MENU";
// MENU | PLAYING | PAUSED | GAME_OVER
```

Four flags = 16 combinations, 12 of them nonsense.
One state = 4 combinations, all valid.
The bad states become **impossible to write**.

### Use it once, in the loop

```js
function update(dt) {
  if (state !== "PLAYING") return;
  updatePaddles(dt);
  updateBall(dt);
}
```

**Not** `if (!paused)` inside every object — you will forget one.

### Sound, no files needed

```js
let audio = null;
function beep(freq, duration) {
  if (!audio) audio = new AudioContext();
  const osc = audio.createOscillator();
  const vol = audio.createGain();
  osc.frequency.value = freq;
  osc.type = "square";
  vol.gain.setValueAtTime(0.08, audio.currentTime);
  vol.gain.exponentialRampToValueAtTime(
    0.0001, audio.currentTime + duration);
  osc.connect(vol);
  vol.connect(audio.destination);
  osc.start();
  osc.stop(audio.currentTime + duration);
}
```

Create the context **lazily** — browsers block audio until the user interacts.
Always **fade**, or you hear a click.

### Screen shake

```js
ctx.save();
if (shakeTime > 0) {
  const fade = shakeTime / shakeTotal;
  ctx.translate(
    (Math.random()-0.5)*2*strength*fade,
    (Math.random()-0.5)*2*strength*fade);
}
drawEverything();
ctx.restore();     // ALWAYS
```

### Particles

```js
const angle = Math.random() * Math.PI * 2;
speedX = Math.cos(angle) * speed;
speedY = Math.sin(angle) * speed;
```

Angle first → an even circle.
Random x and y separately → a lumpy square.

**Remove backwards:**

```js
for (let i = a.length - 1; i >= 0; i--) {
  if (dead) a.splice(i, 1);
}
```

Forwards + splice = skipped items.

### Fade anything

`alpha = life / totalLife` → slides 1 → 0.

### The 100 ms rule

Juice should last about **a tenth of a second**. Long enough to notice, short enough to never get in
the way.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Why is one <code>state</code> variable better than four true/false flags? Use numbers in your answer.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What is a <em>transition</em>, and what does it mean when a key press has no transition for the current state?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> Why must <code>ctx.save()</code> always be matched with <code>ctx.restore()</code>? What goes wrong?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Roughly how long should a screen shake last, and why not longer?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> A particle has <code>life = 0.12</code> and started with <code>0.45</code>. What alpha should it be drawn at? Write the expression and the number.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> An array holds 6 particles and <strong>all six</strong> have run out of life. This loop runs once. How many are left, and why?

```js
for (let i = 0; i < particles.length; i++) {
  if (particles[i].life <= 0) {
    particles.splice(i, 1);
  }
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> What does the player see after about one second?

```js
function render() {
  ctx.translate(shakeX, shakeY);
  drawEverything();
  // no save, no restore
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> The game is in <code>GAME_OVER</code>. What happens when the player holds the up arrow?

```js
function update(dt) {
  if (keys["ArrowUp"]) { player.y -= SPEED * dt; }
  if (state === "PLAYING") { updateBall(dt); }
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> Describe the <em>shape</em> of the particle spray each version produces, and say which has more particles going diagonally.

```js
// version A
const angle = Math.random() * Math.PI * 2;
speedX = Math.cos(angle) * 200;
speedY = Math.sin(angle) * 200;

// version B
speedX = (Math.random() - 0.5) * 400;
speedY = (Math.random() - 0.5) * 400;
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The game pauses correctly, but the particles keep flying around and one enemy keeps moving. The author added <code>if (!paused)</code> to the ball, the paddles and the score. Explain what is wrong with this <em>approach</em>, not just this instance.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> No sound is ever heard. There is no error in the console. The <code>beep</code> function is correct. What is the most likely cause, and why would the browser do this deliberately?

```js
const audio = new AudioContext();   // at the top of the file, on page load
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> Every beep ends with an audible click. What is missing?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 4 Pong.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Add a <code>state</code> variable with <code>MENU</code>, <code>PLAYING</code> and <code>GAME_OVER</code>. Space starts the game from the menu. Draw a title screen.</li>
<li><strong>Checkpoint 2.</strong> Add scores for both players. Draw them. First to 5 wins, and reaching 5 moves the game to <code>GAME_OVER</code> with a message saying who won.</li>
<li><strong>Checkpoint 3.</strong> Make space restart from the game-over screen. Check that the scores reset &mdash; forgetting this is extremely common.</li>
<li><strong>Checkpoint 4.</strong> Add <strong>sound</strong>: different pitches for paddle hits, wall hits and scoring. Play a rally with your eyes shut and see if you can follow what is happening.</li>
<li><strong>Checkpoint 5.</strong> Add <strong>screen shake</strong> (small on a paddle hit, bigger on a score) and <strong>particles</strong>. Find a shake duration that feels like impact rather than an earthquake.</li>
<li><strong>Checkpoint 6.</strong> Add a <code>PAUSED</code> state on P. Verify that <em>nothing</em> moves &mdash; including the particles.</li>
</ul>

<div class="note">
<span class="note-label">The experiment that is the point of today</span>
<p>Once it works, play one rally with every effect switched off, then switch them on one at a time.
The code that decides who wins never changes. Write down which single effect made the biggest
difference for the least code.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Draw the state diagram for a game you actually play. Include the states most people forget:
loading, settings, cutscene, "are you sure you want to quit?", level complete.

<div class="sketchbox tall" data-label="State diagram: boxes for states, arrows labelled with what causes each move"></div>

**E2.** Find a transition in your diagram that should **not** be allowed. What would go wrong if it
were? (For example: what breaks if you could go from PAUSED straight to GAME_OVER?)

<div class="lines"><i></i><i></i><i></i></div>

**E3.** Pick one thing in your game that currently gives no feedback at all. Design feedback for it in
three different senses: something **seen**, something **heard**, and something **felt** through the
controls.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4. The uncomfortable one.** Juice makes a game feel better without making it fairer, deeper, or
more skilful. A slot machine is almost entirely juice. Where is the line between good feedback and
manipulation? Does it matter whether the player can tell it is happening?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. **Hitstop.** Freeze the entire game for 40 ms on a paddle hit. Try 20, 40 and 150 ms. Freezing the
   game briefly makes it feel *more* responsive, which sounds like nonsense until you try it.
2. A fading trail behind the ball.
3. Make the paddle-hit pitch depend on *where* the ball struck, so the sound carries information.
4. A best-of-five match system, with a different message for winning the match than a round.
5. **An option to turn screen shake off.** Motion effects cause genuine nausea for some players. Then
   think about what else in your game should be optional.
