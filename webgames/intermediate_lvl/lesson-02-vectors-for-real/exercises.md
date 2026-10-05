# Lesson 2 — Vectors For Real

## Cheat sheet

### The recipe

**Subtract, normalise, scale.**

```js
const toTarget  = target.sub(me);       // 1. which way?
const direction = toTarget.normalise(); // 2. direction only
me = me.add(direction.scale(SPEED*dt)); // 3. how much
```

Say step 1 out loud: **target minus me**.

### The whole class

```js
add(o)    → (x+o.x, y+o.y)
sub(o)    → (x-o.x, y-o.y)
scale(k)  → (x*k, y*k)
length()  → Math.hypot(x, y)
normalise() → divide both by length
dot(o)    → x*o.x + y*o.y
angle()   → Math.atan2(y, x)   ← y FIRST
Vec2.fromAngle(r) → (cos r, sin r)
```

### Normalise

```
(30, 40)  →  (0.6, 0.8)
length 50    length 1
```

A length-1 vector is a **unit vector**: a pure direction with the distance
removed.

### The guard you must never remove

```js
normalise() {
  const len = this.length();
  if (len === 0) return new Vec2(0, 0);
  return new Vec2(this.x/len, this.y/len);
}
```

Without it: `0/0 = NaN`, which spreads to everything it touches, never throws,
and never recovers. A sprite silently vanishes for ever.

### Four behaviours, one line apart

```js
chase:  (target - me).normalise()
flee:   (me - target).normalise()
orbit:  perpendicular of chase → (-y, x)
cone:   facing.dot(toTarget) > 0.7
```

### Angles

- Angle **0 points right**, not up.
- Angles grow **clockwise**, because y points down.
- Radians, not degrees. A full turn is `2π ≈ 6.283`.
- `atan2(y, x)` → angle · `cos`/`sin` → direction.

### Dot product of two unit vectors

| value | meaning |
|---|---|
| 1 | same way |
| 0 | right angles |
| −1 | opposite |

### Drawing something rotated

```js
ctx.save();
ctx.translate(pos.x, pos.y);
ctx.rotate(angle);
drawShape(ctx);     // as if at (0,0)
ctx.restore();      // NEVER forget
```

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> What does it mean to <em>normalise</em> a vector, and what is the result called?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> Write the sentence that tells you which way round a subtraction goes when you want the direction from A to B.
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why must <code>normalise()</code> check for a length of zero? Name the value you get without the check, and say why it is harder to find than a crash.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> The same two numbers <code>(100, 50)</code> can mean two different kinds of thing. What are they, and which one should you never add to another of its own kind?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Which direction does angle 0 point in, and which way do angles grow on a canvas? Why?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A6.</span> For two unit vectors, what do dot products of 1, 0 and &minus;1 tell you?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> When would you use <code>lengthSquared()</code> instead of <code>length()</code>, and why is it allowed?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

**Write your answer down before you run anything.**

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> What are the length and the normalised form of <code>(9, 12)</code>? Show your working.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> An enemy is at <code>(100, 100)</code>, the player at <code>(160, 180)</code>, <code>SPEED</code> is 200 and <code>dt</code> is 0.1. Where is the enemy after one frame of the recipe? Give the numbers.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> The <code>.normalise()</code> is deleted from B2. Where does the enemy end up after that one frame, and what is wrong with it as a behaviour?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> What does <code>Vec2.fromAngle(0)</code> return? And <code>Vec2.fromAngle(Math.PI / 2)</code>? Say where each one points <em>on the screen</em>.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B5.</span> A guard faces <code>(1, 0)</code>. The player is at 30&deg; to its right, then at 60&deg;, then at 120&deg;. The test is <code>dot &gt; 0.7</code>. Which of the three are seen? (<code>cos 30 = 0.87</code>, <code>cos 60 = 0.5</code>, <code>cos 120 = &minus;0.5</code>.)
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The enemy runs away instead of chasing. One thing is wrong. What?

```js
const direction = enemy.pos.sub(player.pos).normalise();
enemy.pos = enemy.pos.add(direction.scale(SPEED * dt));
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The enemy reaches the player and then vanishes. It never comes back, and the console is empty. Explain exactly what happened, and give the fix.

```js
normalise() {
  const len = this.length();
  return new Vec2(this.x / len, this.y / len);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The ship is drawn at 90&deg; to the direction it travels in. The movement is correct. Two possible causes &mdash; name both.

```js
const nose = Vec2.fromAngle(ship.angle);
ship.pos = ship.pos.add(nose.scale(SPEED * dt));
// ... later, in draw():
ctx.rotate(Math.atan2(nose.x, nose.y));
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C4.</span> After about ten seconds the whole game is spinning, and it gets worse the longer it runs. What is missing?

```js
ctx.save();
ctx.translate(ship.pos.x, ship.pos.y);
ctx.rotate(ship.angle);
drawShip(ctx);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C5.</span> The enemy creeps along at about a pixel a second. The author says &ldquo;but <code>SPEED</code> is 250!&rdquo;. What has gone wrong, and what is a unit vector's length in pixels?

```js
const direction = player.pos.sub(enemy.pos).normalise();
enemy.pos = enemy.pos.add(direction);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from `code/01-the-diagonal-bug.html`, or from your own lesson 1 split.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write <code>vec2.js</code> yourself: <code>add</code>, <code>sub</code>, <code>scale</code>, <code>length</code>, <code>normalise</code>. Type it; do not copy ours. Test each method by printing the answer for <code>(3, 4)</code> and checking it by hand.</li>
<li><strong>Checkpoint 2.</strong> Fix the diagonal bug in your own movement code using normalised intent. Prove it with a speed readout &mdash; the number must be the same in all eight directions.</li>
<li><strong>Checkpoint 3.</strong> Make a ship with an <code>angle</code>. <code>&larr;</code> and <code>&rarr;</code> turn it. Draw it with <code>save</code> / <code>translate</code> / <code>rotate</code> / <code>restore</code>, and draw a dashed line out of its nose so you can see the direction it will travel.</li>
<li><strong>Checkpoint 4.</strong> <code>&uarr;</code> thrusts: move along <code>Vec2.fromAngle(ship.angle)</code>. Add screen wrapping.</li>
<li><strong>Checkpoint 5.</strong> <code>Space</code> fires. A bullet starts at the nose and its velocity is the nose direction scaled by <code>BULLET_SPEED</code>. Give bullets a <code>life</code> in seconds and remove them <strong>backwards</strong> through the array.</li>
<li><strong>Checkpoint 6.</strong> Add rocks that drift in random <em>directions</em> &mdash; pick a random angle, not random x and y speeds. Then say why those two are not the same thing.</li>
<li><strong>Checkpoint 7.</strong> Bullets destroy rocks, using <code>lengthSquared()</code> and no square root. Score it.</li>
<li><strong>Checkpoint 8.</strong> Add three chasers that home in on the ship. Make one of them flee instead, by changing exactly one thing.</li>
</ul>

<div class="note">
<span class="note-label">If something vanishes</span>
<p>Check for <code>NaN</code> first, before anything else. Print the position:
<code>NaN</code> prints as <code>NaN</code>, and once a position is <code>NaN</code> it
will never be a number again. Something normalised a zero-length vector.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost of your idea.</p>
</div>

**E1.** Our `normalise()` returns `(0, 0)` for a zero vector. Three alternatives:
throw an error, return `null`, return `(1, 0)`. Argue for one. Which is most
likely to **hide** a bug, and which is most likely to be irritating in practice?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Design a homing missile that *turns* towards its target rather than
snapping to face it, so it can overshoot, loop round and come back. What does it
need to remember beyond a position? What limits how fast it turns? Write the
update in words, then in code.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

**E3.** Every `Vec2` method makes a new object. A hundred chasers at 60 fps is
about 18,000 new objects a second. Is that a problem? Say how you would **find
out** rather than guess, and write down your prediction now so you can check it in
lesson 9.

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** The hard one. A ball bounces off a flat wall by flipping one speed
component. Now the wall is at 30&deg;. You have a unit vector along the wall, a unit
vector at right angles to it, and the dot product. What does "the part of my
velocity pointing into the wall" mean, and what would you do to it?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Add `rotate(radians)` to `Vec2` using `x' = x·cos − y·sin`, `y' = x·sin + y·cos`.
2. Make a chaser that turns at most 180&deg; per second instead of snapping.
3. Add `lerp` and use it for the camera, a health bar and a menu item.
4. Time ten million `Vec2` creations with `performance.now()`, then compare a
   mutable `addInPlace`. Report real numbers.
5. Bounce a ball off a slope you can drag (question E4, for real).
