# Lesson 9 — Particles And Juice Engineering

## Cheat sheet

### A particle

```js
{ x, y, vx, vy, life, maxLife, size }
```

```js
// update
p.vy += GRAVITY * dt;
p.x += p.vx * dt;
p.y += p.vy * dt;
p.life -= dt;

// draw — the whole visual trick
const t = p.life / p.maxLife;   // 1 → 0
ctx.globalAlpha = t;
ctx.fillRect(p.x, p.y, p.size*t, p.size*t);
```

Remove dead ones **backwards**. Reset `globalAlpha = 1` afterwards, or the score
goes transparent too.

### Random direction

```js
const a = Math.random() * Math.PI * 2;
vx = Math.cos(a) * speed;
vy = Math.sin(a) * speed;
```

Random `vx` and `vy` separately **clusters on the diagonals**.

### Four effects, one emitter

| | dir | speed | gravity | life |
|---|---|---|---|---|
| explosion | all | high | low | short |
| dust | up-ish | low | low | medium |
| sparks | away | high | high | short |
| smoke | up | tiny | **negative** | long |

### Pooling

```js
// built once, never allocated again
if (!pool[i].alive) { reuse pool[i]; }
```

Array length never changes. A full pool **drops** the request, which caps the
work per frame.

Pool when you have **measured** a reason to. The symptom it fixes is one dropped
frame every few seconds, not a slow game.

### Screen shake

```js
shake = Math.min(MAX, shake + amount);  // cap
shake *= Math.exp(-DECAY * dt);         // decay

ctx.save();
ctx.translate(rand(-shake, shake),
              rand(-shake, shake));
drawWorld();
ctx.restore();                          // OFFSET, not the camera
```

3–8 px for a hit. 15 for something enormous. If you *notice* it, it is too much.

### Hitstop — four lines, huge effect

```js
if (hitstop > 0) { hitstop -= realDt; dt = 0; }
```

50–80 ms. Under 30 is invisible, over 120 feels like lag.

### Tween

```js
tween(obj, "flash", 0, 0.12, easeOutQuad);
```

One list, one update, every effect.

### Measuring

```js
const t0 = performance.now();
work();
samples.push(performance.now() - t0);
```

Report the **average and the worst**. The worst is what the player feels.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What three things is a particle made of? What is <code>t = life / maxLife</code> used for?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> State the 100 ms rule, and say how many frames that is at 60 fps.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why does picking random <code>vx</code> and <code>vy</code> not give an even spread of directions? What should you do instead?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> What problem does object pooling solve? Describe the <em>symptom</em> a player would notice without it.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Name three mistakes people make with screen shake, and what each one looks like.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> What is hitstop, how long should it last, and why does it work?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> Why report both the average and the worst frame time rather than just the average?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> A particle has <code>maxLife</code> 0.8 s and <code>life</code> 0.2 s, with <code>size</code> 6. What are its alpha and drawn size?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>shake</code> is 12 and <code>SHAKE_DECAY</code> is 6 per second. What is it after 0.2 s? After 1 s?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> What goes wrong here, and what does the player see?

```js
for (let i = 0; i < particles.length; i++) {
  if (particles[i].life <= 0) { particles.splice(i, 1); }
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> The particle loop sets <code>ctx.globalAlpha</code> each time and never resets it. The score is drawn afterwards. Describe exactly what the player sees as the last particle dies.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B5.</span> A pool holds 500 particles. An explosion asks for 300 and another asks for 300 one frame later, while 200 from the first are still alive. How many does the second explosion get, and is that a problem?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The particles look like a cloud of hard-edged squares that vanish all at once rather than fading.

```js
ctx.globalAlpha = 1;
ctx.fillRect(p.x, p.y, p.size, p.size);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> After a few explosions the view has drifted away from the player and never comes back.

```js
function addShake(n) { camera.x += (Math.random() * 2 - 1) * n; }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The screen shakes for the rest of the game after the first explosion.

```js
function updateShake(dt) {
  if (shake < 0.1) { shake = 0; }
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> Hitstop makes the game feel broken: the whole screen locks up, including the pause menu and the score.

```js
if (hitstop > 0) { hitstop -= dt; return; }   // skips update AND draw
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> The game runs at a steady 60 fps and stutters noticeably about once a second. The author has measured the average frame time at 4 ms and concluded there is no problem.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Use your game from the previous lessons.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Build one particle emitter. Spawn 20 particles on a key press. Get the fade working with <code>t = life / maxLife</code> before you do anything else.</li>
<li><strong>Checkpoint 2.</strong> Make four presets from the same emitter: explosion, dust, sparks and smoke. Smoke must use negative gravity. Put every number on a slider first and find the presets by playing.</li>
<li><strong>Checkpoint 3.</strong> Add screen shake as a decaying, capped offset applied with <code>translate</code>. Start at 6 pixels. Then try 40 so that you know what too much looks like.</li>
<li><strong>Checkpoint 4.</strong> Add hitstop on a slider from 0 to 200 ms. Find your own number. Make sure the HUD still draws while it is frozen.</li>
<li><strong>Checkpoint 5.</strong> Add a white flash on the thing that got hit, decaying over about 120 ms, and squash-and-stretch on landing.</li>
<li><strong>Checkpoint 6.</strong> Add floating damage numbers: a position, a value, and a countdown, drifting upwards and fading. It is the particle system with text.</li>
<li><strong>Checkpoint 7.</strong> Build the tween system from the notes, and rewrite your flash and your squash to use it. Count how many timers that removed.</li>
<li><strong>Checkpoint 8.</strong> Add a switch for every effect, and a frame-time readout showing average and worst. Then turn everything off, play for a minute, and turn them on one at a time.</li>
</ul>

<div class="note">
<span class="note-label">Before you tune anything</span>
<p>Get the frame-time readout (average <em>and</em> worst over the last two seconds)
working early, and leave it in your game for the rest of the course. Every
performance question after this becomes a five-second answer instead of an
argument.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** Hitstop freezes the game — but the hit's particles probably should keep
moving and the HUD definitely should. Write the rule for exactly what freezes.

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** At what particle count did pooling start to matter on *your* machine? What
does that tell you about when to bother? Would your answer change on a five-year-old
school laptop, and how would you find out?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Design three strengths of hit — light, medium, killing blow — using shake,
particles, hitstop, flash, squash, sound and numbers. Do you scale everything
together, or do some effects only appear for the big one? Give numbers.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. Juice can lie. A shake and a flash say "something important
happened", so using them for everything says nothing, and using them for a hit
that did no damage actively misleads. Where is the line? Give one concrete example
of juice that would be dishonest.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Trails: the last ten positions, fading.
2. Colour over life: yellow → red → grey.
3. A tween with an `onDone` callback, and three chained effects.
4. Impact direction: particles fly away from where the hit came from.
5. A frame-time graph you keep in your game for the rest of the course.
