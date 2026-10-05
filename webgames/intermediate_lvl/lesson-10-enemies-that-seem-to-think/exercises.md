# Lesson 10 — Enemies That Seem To Think

## Cheat sheet

### Decide, then act. Separately.

```js
function updateEnemy(e, dt) {
  decide(e);        // should I change what I am doing?
  act(e, dt);       // do what I am doing
}
```

### Hysteresis: two thresholds, one boundary

```js
if (e.mode === "patrol" && d < SIGHT)        e.mode = "chase";
else if (e.mode === "chase" && d > SIGHT+GAP) e.mode = "patrol";
```

Same number for both → the enemy flickers **every frame** at the edge. The band
between the two is how much noise it tolerates.

### Line of sight

```js
const dir = to.sub(from).normalise();
const STEP = TILE / 2;              // smaller than a tile!
for (let i = 1; i < dist / STEP; i++) {
  const p = from.add(dir.scale(i * STEP));
  if (isSolid(floor(p.x/TILE), floor(p.y/TILE)))
    return false;
}
return true;
```

### Vision cone — one dot product

```js
facing.dot(toPlayer) > 0.7     // ±45°
```

`cos 30 = 0.87` · `cos 45 = 0.71` · `cos 90 = 0` · `-1` = sees everywhere.

### Steering

```js
seek:  (target - me).normalise()
flee:  (me - target).normalise()

arrive:
  let speed = MAX;
  if (d < SLOW) speed = MAX * (d / SLOW);

wander:
  e.angle += (Math.random()-0.5) * 2.5 * dt;   // += NOT =

separation:
  for each other enemy within PERSONAL_SPACE:
    push += away.normalise()
            * (SPACE - d) / SPACE;
```

Separation is three lines and turns a stack into a pack.

### Fair, not strong

| | why |
|---|---|
| reaction time 200–400 ms | looks like realising |
| telegraph | the player can respond |
| inaccuracy | perfect aim reads as cheating |
| max turn rate | can be outmanoeuvred |

**The player must be able to see why they lost.**

### AI need not run every frame

Ten decisions a second is indistinguishable from sixty, and costs a sixth as
much.

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> Where does the illusion of intelligence come from, if not from any behaviour being clever?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> Why keep <code>decide</code> and <code>act</code> as separate functions?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> What is hysteresis, what bug does it prevent, and give one example from outside games.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Why must the line-of-sight ray step in pieces smaller than a tile? What goes wrong otherwise?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why is a dot product better than comparing angles for a vision cone?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A6.</span> What problem does <em>separation</em> solve, and why does it look like a bug in each individual enemy when it is missing?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A7.</span> Name three deliberate handicaps that make an enemy better to play against, and say what each one buys.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> <code>SIGHT</code> is 180 and <code>GAP</code> is 70. At what distance does the guard start chasing? At what distance does it give up? How wide is the band where nothing changes?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> A player stands at exactly distance 180 with <code>GAP = 0</code>, and small movements take them a pixel either side. Describe what happens over one second at 60 fps.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> <code>TILE</code> is 32, the enemy is 200 px from the player, and <code>STEP</code> is 16. How many tile lookups does one line-of-sight test do? For 12 enemies at 60 fps, how many per second?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> <code>facing</code> is <code>(1, 0)</code>. The player is directly above the enemy, so <code>toPlayer</code> is <code>(0, -1)</code>. What is the dot product, and is the player inside a cone of <code>&gt; 0.7</code>?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B5.</span> <code>MAX_SPEED</code> is 200 and <code>SLOW_RADIUS</code> is 100. Give the arrive speed at distances 300, 100, 50 and 0.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The enemy changes state several times a second whenever the player stands still at a certain distance.

```js
if (dist < SIGHT) { e.mode = "chase"; }
else              { e.mode = "patrol"; }
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Five chasers behave as if they were one enemy: they overlap exactly and move as a single sprite. Each one's code is correct. What is missing, and why does it look like an individual bug?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The enemy twitches violently instead of meandering.

```js
e.wanderAngle = (Math.random() - 0.5) * 2.5 * dt;
e.vel = Vec2.fromAngle(e.wanderAngle).scale(SPEED);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The enemy sees the player through a one-tile-thick wall, sometimes but not always. <code>TILE</code> is 32.

```js
const STEP = 48;
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> The enemy disappears permanently whenever it catches the player exactly.

```js
const dir = player.pos.sub(e.pos).normalise();
e.pos = e.pos.add(dir.scale(SPEED * dt));
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

Use your tilemap game from lessons 5 and 6.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Add one enemy with a <code>mode</code> and separate <code>decide</code> and <code>act</code> functions. Draw the mode on screen above its head &mdash; keep that label all lesson.</li>
<li><strong>Checkpoint 2.</strong> Patrol and chase, with <em>one</em> threshold. Stand at the edge and count the state changes on screen. Then add the gap and watch the counter stop.</li>
<li><strong>Checkpoint 3.</strong> Add line of sight. Draw the ray, and draw it in a different colour when it is blocked. Hide behind a wall and check you are invisible.</li>
<li><strong>Checkpoint 4.</strong> Add a vision cone with the dot product, and draw the cone. Sneak up from behind.</li>
<li><strong>Checkpoint 5.</strong> Add four more enemies, then add separation. Turn it off and on while they chase you. This is the moment the lesson pays.</li>
<li><strong>Checkpoint 6.</strong> Add <em>arrive</em> so they stop at you instead of orbiting, and <em>wander</em> so the patrolling ones do not look as if they are on rails.</li>
<li><strong>Checkpoint 7.</strong> Add the four fairness handicaps, each on a key: reaction delay, telegraph, inaccuracy, turn rate. Play with all four off, then all four on.</li>
<li><strong>Checkpoint 8.</strong> Make <code>decide()</code> run only ten times a second instead of sixty. Try to tell the difference by playing. Then put the cost on screen and compare.</li>
</ul>

<div class="note">
<span class="note-label">Draw everything the enemy knows</span>
<p>The mode, the sight ray, the cone, the distance, and the target it is moving
towards. Enemy bugs are nearly impossible to reason about from the code and nearly
trivial to see once the enemy's own information is on the screen.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** What is the smallest number of times per second an enemy could reconsider
before a player noticed? How would you find out, and does the answer depend on
what the enemy is doing?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** When a guard gives up a chase, should it return to the start of its route,
carry on from where it is, or go to where it last saw you? Each makes a different
game. Pick one and say what it implies about how the player should play.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design an enemy that is genuinely hard and entirely fair: the player should
lose and know exactly why. List what it does, what it telegraphs, how long each
telegraph lasts, and the player's counter to each.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. A guard who notices you, loses you, then **searches**: goes
to where you were, looks around, gives up after a while. The enemy has to remember
something, and the memory must expire. Where does that live, and what does it do
to your state machine?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Search (E4).
2. Alert nearby enemies when one spots you — one distance test, whole new game.
3. A flyer whose wander is biased towards the player, so it drifts in on a curve.
4. One difficulty dial from 0 to 1 driving reaction, accuracy, speed and turn rate.
   Then say which of those actually changes the difficulty.
5. Three chasers that approach from different sides.
