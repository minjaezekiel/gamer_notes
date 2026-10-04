# Lesson 4 — When Things Touch

## Cheat sheet

### The AABB test

```js
function boxesOverlap(a, b) {
  return (
    a.x < b.x + b.w &&
    a.x + a.w > b.x &&
    a.y < b.y + b.h &&
    a.y + a.h > b.y
  );
}
```

**All four**, joined by `and`.

### How to remember it

Do not ask when they *do* overlap. Ask **when they definitely cannot**: a is entirely left of b,
entirely right, entirely above, or entirely below. Those are the only four escape routes. Flip them
and you have the test.

### Boxing a circle

```js
function ballBox(ball) {
  return {
    x: ball.x - ball.radius,
    y: ball.y - ball.radius,
    w: ball.radius * 2,
    h: ball.radius * 2
  };
}
```

Drawn as a circle, collides as a square. That is a **hitbox**.

### Circles

```js
const dx = b.x - a.x;
const dy = b.y - a.y;
const d = Math.sqrt(dx*dx + dy*dy);
return d < a.radius + b.radius;
```

**distance = √(dx² + dy²)** — Pythagoras.
Skip the square root when only comparing:
`dx*dx + dy*dy < limit*limit`

### Responding

```js
if (boxesOverlap(ballBox(ball), paddle)) {
  ball.y = paddle.y - ball.radius;  // FIRST
  ball.speedY = -ball.speedY;       // THEN
}
```

Position before velocity, or it sticks and vibrates.

### Steering the ball (design, not physics)

```js
const centre = paddle.y + paddle.h / 2;
const off = (ball.y - centre) / (paddle.h / 2);
ball.speedY = off * 320;
```

`off` is −1 at the top, 0 in the middle, +1 at the bottom. This is what turns Pong from standing in
the right place into **aiming**.

### Words

**AABB** — axis-aligned bounding box.
**Hitbox** — the shape you test, not the shape you see.
**Tunnelling** — passing through because one step was too big.

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> What does AABB stand for, and what does &ldquo;axis-aligned&rdquo; rule out?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Write out the four conditions for two boxes overlapping.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Explain the &ldquo;ask the opposite question&rdquo; trick for remembering the test.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Two circles have radii 20 and 30. Their centres are 45 pixels apart. Are they touching? Show how you know.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Give one reason a game might deliberately make the player's hitbox <em>smaller</em> than the picture of the player.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> Box <code>a</code> is at <code>{x:10, y:10, w:50, h:50}</code>. Box <code>b</code> is at <code>{x:55, y:70, w:40, h:40}</code>. Work out each of the four conditions separately, then say whether they overlap.
<div class="lines"><i></i><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> A ball at <code>(100, 100)</code> has radius 12. What are the <code>x</code>, <code>y</code>, <code>w</code> and <code>h</code> of its hitbox?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> Someone changes one <code>&amp;&amp;</code> to <code>||</code> in <code>boxesOverlap</code>. Describe what the player would see happen to the ball.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> A ball travels at 2400 pixels per second. The game runs at 60 fps. The wall is 14 pixels thick. How far does the ball move in one frame, and what will happen when it reaches the wall? Name the problem.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The ball reaches the paddle and then shivers inside it instead of bouncing away. What is missing? You have seen this bug before &mdash; where?

```js
if (boxesOverlap(ballBox(), paddle)) {
  ball.speedX = -ball.speedX;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The ball bounces off the paddle correctly most of the time, but occasionally gets caught and bounces twice in a row, ending up behind the paddle. The position fix <em>is</em> present. What other condition is needed, and why?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> This collision test never returns true, no matter where the ball is. Why?

```js
function ballBox(ball) {
  return { x: ball.x, y: ball.y, w: ball.radius, h: ball.radius };
}
```

Hint: there are <em>two</em> mistakes here, and only one of them is about the size.

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 3 paddle, with the lesson 2 ball bouncing around.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write <code>boxesOverlap(a, b)</code> and test it by logging the result to the console. Move the ball past the paddle and watch the value flip.</li>
<li><strong>Checkpoint 2.</strong> Write <code>ballBox()</code> so the circular ball has a rectangular hitbox. Add a debug view: hold a key to draw every hitbox as an outline.</li>
<li><strong>Checkpoint 3.</strong> Make the ball bounce off the paddle. Fix the <strong>position first</strong>, then flip the velocity.</li>
<li><strong>Checkpoint 4.</strong> Add a second paddle on the far side. Make it follow the ball automatically &mdash; but <em>more slowly than the ball can travel</em>, or it can never be beaten.</li>
<li><strong>Checkpoint 5.</strong> Add the steering: where the ball hits the paddle should change the angle it leaves at. Play a rally with <code>STEER_STRENGTH</code> set to 0, then to 320, and write down which is more fun.</li>
<li><strong>Checkpoint 6.</strong> Make the ball speed up slightly on every paddle hit. Find a rate that makes rallies exciting rather than impossible.</li>
</ul>

<div class="note">
<span class="note-label">The debug view is not optional</span>
<p>Checkpoint 2 looks like extra work and is not. Being able to see the hitboxes turns every
collision bug for the rest of this course from a mystery into something you can simply look at.
Real developers all build one.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning. Every fix for these problems costs something &mdash; name the cost.</p>
</div>

**E1. Tunnelling.** Your collision test correctly answers "are these overlapping *right now*?" But
the game only looks 60 times a second. Sketch the positions of a fast ball on three consecutive
frames to show how it can get from in front of a wall to behind it without ever being inside it.

<div class="sketchbox" data-label="Three frames of a fast ball approaching a thin wall"></div>

**E2.** Invent a fix. You may change anything.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Now critique your own fix. What does it cost — in speed, in complexity, or in how the game
feels?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4. Too many tests.** Imagine 500 bullets and 200 enemies. That is 100,000 collision tests every
frame — six million a second. Without looking anything up, invent a way to avoid most of them. You
may change how the objects are stored.

*Hint: if you knew a bullet was in the top-left corner of the screen, which enemies could you skip
without testing at all?*

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Add three bricks that disappear when hit. You now have the core of Breakout.
2. Write a proper circle-against-rectangle test instead of boxing the ball. (Find the point on the
   rectangle closest to the circle's centre, then measure to it. Harder than it sounds.)
3. Set the ball speed to 3000, watch it tunnel, then fix it. Any fix that works counts.
4. Give the paddle a hitbox 20 pixels taller than it is drawn. Play for a minute. Does the game feel
   better or worse? Can you tell it is happening?
