# Lesson 12 — Capstone: A Platformer

## Cheat sheet

### The six parts of a jump

```js
// 1. the impulse
if (buffer > 0 && coyote > 0) {
  vy = -JUMP_SPEED;
  buffer = 0; coyote = 0;      // BOTH, or you get a double jump
}

// 2. variable height — cut, do not stop
if (!jumpHeld && vy < 0) vy *= 0.45;

// 3. coyote time — ground remembers itself
if (onGround) coyote = 0.10;
else          coyote -= dt;

// 4. jump buffer — the press remembers itself
if (jumpPressed) buffer = 0.12;
else             buffer -= dt;

// 5. apex hang
const g = Math.abs(vy) < APEX
            ? GRAVITY * 0.55 : GRAVITY;

// 6. fast fall
const g = vy < 0 ? GRAVITY_UP : GRAVITY_DOWN;
```

Coyote time and jump buffering are **the same idea in opposite directions**:
remember an input briefly. The jump fires when the two windows **overlap**.

### Tune in design units

```js
const JUMP_HEIGHT = TILE * 3;     // what you care about
const TIME_TO_APEX = 0.33;

GRAVITY_UP = 2*JUMP_HEIGHT / TIME_TO_APEX²;
JUMP_SPEED = GRAVITY_UP * TIME_TO_APEX;
```

```
height = v²/(2g)        v = √(2·g·height)
time up = v/g
```

### One-way platforms

Needs **direction of travel** and **the previous position**:

```js
const wasAbove = previousBottom <= topEdge + 1;
if (!(movingDown && wasAbove)) continue;   // not solid
```

### Moving platforms — order matters

1. move the platforms
2. carry any passenger by the same amount
3. move the player, then collide

`ridingPlatform` is set by the **downward** collision test — the same one that
sets `onGround`.

### Playtesting

**Watch. Say nothing.**

- "Here, have a go." No instructions.
- Write down every moment of confusion, as it happens.
- Afterwards ask what they were *trying* to do. Never ask if they liked it.

Then **measure**: where did they die?

### Done

title · pause · winnable (by somebody else) · survives blocked storage, resize,
hidden tab · controls discoverable · **one** polished level

---

## Section A — Recall

<div class="q"><span class="marks">[6 marks]</span>
<span class="q-num">A1.</span> Name the six parts of a good jump, and for each one name the <em>moment</em> it fixes.
<div class="lines"><i></i><i></i><i></i><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Explain how coyote time and jump buffering are the same idea. What single condition fires the jump once you have both?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> Why must <code>coyote</code> be reset to 0 when a jump fires?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why multiply <code>vy</code> by 0.45 on release rather than setting it to 0?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why tune the jump in <em>height</em> and <em>time to apex</em> rather than in speed and gravity?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A6.</span> What two pieces of information does a one-way platform test need that an ordinary solid test does not, and what goes wrong without the second one?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A7.</span> Give the three rules of watching somebody playtest your game.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> You want a jump 96 px high taking 0.3 s to the top. Work out <code>GRAVITY_UP</code> and <code>JUMP_SPEED</code>.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>JUMP_SPEED</code> is 600 and gravity is 1800. How high is the jump, and how long to the apex?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> Coyote time is 0.1 s and the buffer is 0.12 s. The player walks off a ledge at t = 0 and presses jump at t = 0.08. Does it jump? Now they press at t = 0.14. Does it? Explain both.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> The player presses jump at t = 0 while falling and lands at t = 0.09. The buffer is 0.12 s. What happens, and what would happen with no buffer?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> A platform moves up at 60 px/s and <code>dt</code> is 0.016. The player stands on it, and the player is moved <em>before</em> the platform. Describe what happens over a second.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The player can jump twice in mid-air, every time.

```js
if (buffer > 0 && coyote > 0) {
  player.vy = -JUMP_SPEED;
  buffer = 0;
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Holding the jump key makes the player bounce repeatedly the moment they land.

```js
if (keys[" "]) { buffer = JUMP_BUFFER; }
if (buffer > 0 && coyote > 0) { player.vy = -JUMP_SPEED; coyote = 0; }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> Releasing the jump key feels like hitting an invisible ceiling.

```js
if (!jumpHeld && player.vy < 0) { player.vy = 0; }
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The player slowly sinks into a platform that is rising, and is left floating when it falls.

```js
movePlayer(dt);
resolveCollisions();
for (const p of platforms) { p.y += p.vy * dt; }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C5.</span> Jumping up through a one-way platform snaps the player onto its top instead of passing through.

```js
if (tile.oneWay && movingDown) { /* land on it */ }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

This is the capstone. You have 60 minutes of build time, and then you are going to
watch somebody else play it, so leave time for that.

**One level, finished.** Not four sketches.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Start from your lesson 5/6 tilemap game. Get gravity and a basic jump working, tuned from <code>JUMP_HEIGHT</code> and <code>TIME_TO_APEX</code> rather than from raw numbers.</li>
<li><strong>Checkpoint 2.</strong> Add all five refinements, each on a key so you can switch it off. Draw <code>coyote</code>, <code>buffer</code>, <code>vy</code> and <code>onGround</code> on screen.</li>
<li><strong>Checkpoint 3.</strong> Set coyote time to 0.5 s and play. Then find the largest value you cannot notice. Write it down.</li>
<li><strong>Checkpoint 4.</strong> Add one-way platforms and one moving platform, with the platforms moved first.</li>
<li><strong>Checkpoint 5.</strong> Add the rest: camera with a dead zone, one enemy that is beatable, coins, a sound per event, particles on landing and on pickup, a title screen, a pause, and a save of the best time. All of this is lessons 6&ndash;11; none of it is new.</li>
<li><strong>Checkpoint 6.</strong> Build <strong>one</strong> level that is winnable in about 60 seconds. Play it five times yourself and fix the worst thing each time.</li>
<li><strong>Checkpoint 7.</strong> <strong>Playtest.</strong> Swap machines with somebody. Say nothing at all. Write down every moment they hesitate, every wrong assumption, and everywhere they die. One sheet of paper.</li>
<li><strong>Checkpoint 8.</strong> Make exactly <strong>one</strong> change based on what you saw, then have them play again and see whether it helped.</li>
</ul>

<div class="note">
<span class="note-label">The hardest instruction in this course</span>
<p>During checkpoint 7, <strong>do not help.</strong> Not a hint, not a nudge, not
&ldquo;try pressing up&rdquo;. Every time you help, you destroy the information you
were there to collect. Sit on your hands and write.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** Coyote time and jump buffering are both "remember an input briefly". Name
two other places in a game where that idea would help. (You met one in lesson 7.)

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** You tuned the jump in design units. What else in your game would be better
expressed that way? Give three examples, with the units you would use.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design one new mechanic — dash, wall jump, double jump, grapple. Before any
code: what problem does it solve for the player, what must the level design do to
make it worth having, and what does it break about the level you already built?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. Somebody died eleven times at the same jump. Five possible
causes: the jump is too long, the landing is not visible, the run-up is too short,
the controls were never explained, the penalty for failure is too high. How would
you tell which? What would you change **first**, and how would you know if it
worked?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. A wall jump — a wall-touch test, a coyote window for it, and a push away.
2. A dash with a cooldown and a trail.
3. Record and replay a run. If it does not replay exactly, you have learned
   something — and the advanced level fixes it.
4. A browser level editor that prints your level back out as text.
5. **Ship it.** Put it on a free static host, send it to five people, and write down
   the first thing each of them did.
