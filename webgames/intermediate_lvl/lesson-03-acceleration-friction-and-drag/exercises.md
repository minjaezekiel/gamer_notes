# Lesson 3 — Acceleration, Friction And Drag

## Cheat sheet

### The six steps, in this order

```js
// 1. turn
ship.angle += TURN_SPEED * dt * dir;

// 2. build the acceleration from zero
let a = new Vec2(0, 0);
if (thrusting) {
  a = a.add(Vec2.fromAngle(ship.angle)
             .scale(THRUST));
}

// 3. acceleration → velocity
ship.vel = ship.vel.add(a.scale(dt));

// 4. drag, PER SECOND
ship.vel = ship.vel
             .scale(Math.exp(-DRAG * dt));

// 5. limit the LENGTH
if (ship.vel.length() > MAX_SPEED) {
  ship.vel = ship.vel.normalise()
                    .scale(MAX_SPEED);
}

// 6. velocity → position  (always last)
ship.pos = ship.pos.add(ship.vel.scale(dt));
```

### The bug that looks fine

```js
vel = vel.scale(0.98);   // per FRAME — wrong
```

| fps | speed left after 1 s |
|---|---|
| 30 | 55% |
| 60 | 30% |
| 144 | 5.5% |

Same code, three machines, three games. Use:

```js
vel = vel.scale(Math.exp(-DRAG * dt));
```

### Drag vs friction

**Drag** multiplies → takes a *share* → never quite stops → air, water, ships.

**Friction** subtracts → takes a *fixed amount* → really stops → ground.

```js
const loss = FRICTION * dt;
if (vel.length() <= loss) vel = Vec2.zero();
else vel = vel.sub(vel.normalise().scale(loss));
```

Without that `if`, the ship drives slowly **backwards** for ever.

### The numbers are linked

```
settled speed = THRUST / DRAG
half-life     = 0.693 / DRAG
```

If `THRUST/DRAG` is below `MAX_SPEED`, the speed limit never fires at all.

### Four presets, same code

| | THRUST | DRAG | MAX |
|---|---|---|---|
| spaceship | 420 | 0.3 | 500 |
| car | 900 | 2.5 | 380 |
| ice | 300 | 0.15 | 450 |
| snappy | 4000 | 14 | 320 |

### Words

**Acceleration** — change in velocity, px/s per second.
**Terminal velocity** — where push and drag cancel.
**Frame-rate dependent** — behaves differently on a faster machine. A bug.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Name the three levels of &ldquo;how things move&rdquo;, in order, and say what each feels like.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> Why is <code>vel = vel.scale(0.98)</code> a bug, given that no <code>dt</code> appears to be missing?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Give two differences between <em>drag</em> and <em>friction</em>, and say which you would use for a character walking on stone.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why must a speed limit be applied to the velocity's <em>length</em> rather than to <code>x</code> and <code>y</code> separately?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> What is <em>terminal velocity</em>, and what two numbers decide it?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why must the position update come <em>after</em> the velocity update, and what is the symptom if it does not?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> What is the one line you must never leave out of subtractive friction, and what happens without it?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> <code>THRUST</code> is 1200 and <code>DRAG</code> is 4. The player holds thrust for a long time. What speed does the ship settle at? If <code>MAX_SPEED</code> is 500, does the clamp ever fire?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>DRAG</code> is 2. Roughly how long does the ship take to lose half its speed? And three quarters of it?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> A ship has velocity <code>(100, 0)</code>, <code>THRUST</code> 600 pointing straight down, <code>DRAG</code> 0, and <code>dt</code> is 0.1. Give the velocity and position change after one frame. Starting position <code>(0, 0)</code>.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> Velocity is <code>(3, 4)</code> and subtractive friction removes 6 units this frame. With the zero test, what is the new velocity? Without it?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> One ship runs at 60 fps and one at 20 fps, both using <code>vel *= 0.9</code> per frame. After one second, what fraction of the starting speed does each have left? (<code>0.9^60 ≈ 0.0018</code>, <code>0.9^20 ≈ 0.12</code>.)
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The ship speeds up for ever and leaves the screen in two seconds. What is missing?

```js
if (keys["ArrowUp"]) {
  ship.vel = ship.vel.add(nose.scale(THRUST * dt));
}
ship.pos = ship.pos.add(ship.vel.scale(dt));
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Diagonal flight is faster than straight flight, even though <code>MAX_SPEED</code> is set. Name the bug and write the correct version.

```js
if (ship.vel.x > MAX_SPEED) { ship.vel.x = MAX_SPEED; }
if (ship.vel.y > MAX_SPEED) { ship.vel.y = MAX_SPEED; }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The ship coasts to a near-stop and then creeps very slowly in the wrong direction and never stops. Why?

```js
const loss = FRICTION * dt;
ship.vel = ship.vel.sub(ship.vel.normalise().scale(loss));
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The controls feel very slightly dead, as if there is a lag the author cannot measure. The physics is otherwise correct. What is wrong with this order?

```js
ship.pos = ship.pos.add(ship.vel.scale(dt));
ship.vel = ship.vel.add(acceleration.scale(dt));
ship.vel = ship.vel.scale(Math.exp(-DRAG * dt));
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> With a very low frame rate, the ship suddenly flies <em>backwards</em>. <code>DRAG</code> is 8 and <code>dt</code> reached 0.2. Explain, and name the fix.

```js
ship.vel = ship.vel.scale(1 - DRAG * dt);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 2 ship.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Replace &ldquo;set the velocity&rdquo; with &ldquo;add to the velocity&rdquo;. The ship will now fly off the screen and never come back. That is correct, and it is progress.</li>
<li><strong>Checkpoint 2.</strong> Add drag with <code>Math.exp(-DRAG * dt)</code>. Print the speed on screen while you fly &mdash; you will need that number for the rest of the lesson.</li>
<li><strong>Checkpoint 3.</strong> Add a speed limit on the <em>length</em>. Then check your maths: hold thrust until the speed settles and confirm it equals <code>THRUST / DRAG</code>, not <code>MAX_SPEED</code>.</li>
<li><strong>Checkpoint 4.</strong> Add four sliders (plain <code>&lt;input type="range"&gt;</code> is fine) for THRUST, DRAG, MAX_SPEED and TURN_SPEED, showing the live value of each.</li>
<li><strong>Checkpoint 5.</strong> Add the four presets on keys <code>1</code>&ndash;<code>4</code>. Fly each one for thirty seconds before moving on.</li>
<li><strong>Checkpoint 6.</strong> Make a deliberately broken version alongside, using <code>* 0.98</code> per frame, and a control that drops your loop to 20 fps. Fly both at both frame rates and write down what you observe.</li>
<li><strong>Checkpoint 7.</strong> Tune your own preset. Write the four numbers on paper, with one sentence saying what sort of game it is for.</li>
<li><strong>Checkpoint 8.</strong> Swap seats and fly your neighbour's ship. Then argue about it &mdash; politely, with reasons.</li>
</ul>

<div class="note">
<span class="note-label">How to drop your frame rate on purpose</span>
<p>Do not try to make the computer slow. Call your own update from a
<code>setInterval(step, 50)</code> instead of <code>requestAnimationFrame</code>, with
<code>dt</code> fixed at <code>0.05</code>. That gives you an honest 20 fps with no
guesswork.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning. Name what your idea costs.</p>
</div>

**E1.** Invent a **procedure** for tuning four sliders from scratch — an order, with
the question you are answering at each step. Which of the four can you judge
without having settled the other three?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** The "snappy" preset is nearly the beginner version. Is the difference worth
the extra code? Say how you would **find out** rather than argue: what would you
measure, or who would you ask, and what exactly would you ask them?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Design a car that grips going forwards and slides going sideways. Your
`Vec2` already has the tool that splits the velocity into those two parts. What
would you do to each half, and what would the car then feel like?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. An "ice" power-up must change all four numbers over half a
second, hold them for five seconds, then change them back. What does that
machinery look like, and where in your program does it live? Would you reuse it
for anything else?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Replace the drag slider with a "seconds to lose half your speed" slider.
2. A dash: a one-off push, a cooldown, and no drag while it lasts.
3. Wind — one extra line in the acceleration step. Then make it vary across the screen.
4. Separate grip along and across the ship (E3, for real). Four lines, biggest
   change to feel in the whole level.
5. Measure the settled speed and compare it with `THRUST / DRAG`. Report both numbers.
