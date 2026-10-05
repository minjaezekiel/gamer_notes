# Lesson 10 — Enemies That Seem To Think

> **Web Games · Intermediate level · Lesson 10 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

Three kinds of enemy that behave as though they have noticed you: a **guard** who walks a route and
gives chase, a **flyer** that circles and swoops, and a **pack** that spreads out instead of stacking
into one lump. They will look through windows and not through walls, and they will be beatable — on
purpose.

```
        ┌────────────────────────────┐
        │  ◆ ·  ·  ·  ·              │   the guard's vision, blocked by the wall
        │  ◆ ·  ·  ████              │
        │       ·   ████   ☺         │   ← the player, currently unseen
        │  ◆ ·  ·  ████              │
        └────────────────────────────┘
```

The last part matters more than it sounds. An enemy that always wins is not difficult; it is boring.
Most of the craft here is making something that *could* win and does not.

## Where this fits

- **Back:** [lesson 2](../lesson-02-vectors-for-real/notes.md) gave you subtract-normalise-scale and the
  dot product; [lesson 7](../lesson-07-scenes-properly/notes.md) gave you state machines; lesson 5 gave
  you a tilemap to see through.
- **Forward:** the [capstone](../lesson-12-capstone-a-platformer/notes.md) needs at least one enemy that
  is interesting. The advanced level adds pathfinding, so enemies can go *round* things.
- **Other tracks:** Python's intermediate lesson 10 does waves and difficulty curves; C++'s intermediate
  lesson 11 builds the same state machine with an `enum class`, where the compiler checks that every
  state is handled.

---

## The idea, in plain words

### Enemies are not intelligent, and should not be

A guard who walks a route, notices you, runs at you, and backs off when hurt will be described by
players as "smart". It is three states and two numbers.

The illusion does not come from the thinking. It comes from the **switching** — from the fact that the
behaviour *changes* at a moment the player can see and understand. An enemy with one complicated
behaviour looks mechanical. An enemy with three simple behaviours and visible reasons for moving between
them looks alive.

So the goal for today is not clever enemies. It is **legible** ones.

### One value, three behaviours

This is lesson 7's state machine, pointed at an enemy:

```js
const enemy = {
  pos: new Vec2(100, 100),
  mode: "patrol",          // "patrol" | "chase" | "flee"  — exactly one
  hp: 100
};
```

Then every frame, two separate jobs — and keeping them separate is what stops this becoming a mess:

```js
function updateEnemy(e, dt) {
  decide(e);        // 1. should I change what I am doing?
  act(e, dt);       // 2. do whatever I am currently doing
}
```

```js
function decide(e) {
  const dist = player.pos.distanceTo(e.pos);

  if (e.hp < 30 && dist < 260) { e.mode = "flee"; return; }

  if (e.mode === "patrol" && dist < SIGHT)          { e.mode = "chase"; }
  else if (e.mode === "chase" && dist > SIGHT + GAP) { e.mode = "patrol"; }
  else if (e.mode === "flee"  && e.hp >= 30)         { e.mode = "patrol"; }
}
```

```js
function act(e, dt) {
  if (e.mode === "patrol")     { walkRoute(e, dt); }
  else if (e.mode === "chase") { moveTowards(e, player.pos, CHASE_SPEED, dt); }
  else                         { moveAway(e, player.pos, FLEE_SPEED, dt); }
}
```

Three branches, a couple of lines each, and none of them knows what the others do. Adding a fourth
behaviour does not touch the first three.

### The two thresholds, and the bug that needs them

Look carefully at `decide`. Entering a chase uses `SIGHT`. Leaving one uses `SIGHT + GAP`. Those are
**deliberately different numbers**, and if you make them the same you get a real and very recognisable
bug.

With one threshold, a player standing exactly on the boundary flips the enemy between patrol and chase
**every frame**. It looks broken, it sounds broken if there is a sound attached, and nothing in the code
looks wrong.

Using two different thresholds for the two directions is called **hysteresis**. The word is worth
knowing because the pattern is everywhere: a thermostat that heats to 21° and stops at 22°, a lift that
will not change direction for one person, a UI that needs a deliberate drag before it starts dragging.
Any time something switches on a comparison, ask whether it needs two numbers instead of one.

### Line of sight: an enemy that cannot see through walls

Distance alone gives you an enemy with x-ray vision, which players notice immediately and resent.

Two things have to be true for an enemy to see the player: **close enough**, and **nothing in the way**.
The first is lesson 2's distance test. The second is a *ray*: walk along the line between them in small
steps and ask the tilemap whether each step is solid.

```js
function canSee(from, to) {
  const delta = to.sub(from);
  const distance = delta.length();
  if (distance > SIGHT) { return false; }

  const direction = delta.normalise();
  /* Step in pieces smaller than a tile, or the ray can jump over a thin wall. */
  const STEP = TILE / 2;
  const steps = Math.floor(distance / STEP);

  for (let i = 1; i < steps; i++) {
    const point = from.add(direction.scale(i * STEP));
    const col = Math.floor(point.x / TILE);
    const row = Math.floor(point.y / TILE);
    if (isSolid(col, row)) { return false; }      // blocked
  }
  return true;
}
```

That is the whole thing: twelve lines, and enemies stop cheating. Two honest limitations, both worth
knowing:

- **It can miss a very thin wall** if `STEP` is too large. Half a tile is safe for tile-sized walls.
- **It costs a loop per enemy per frame.** For a dozen enemies at a sight range of ten tiles that is
  about 240 tile lookups a frame, which is nothing. For two hundred enemies you would check less often —
  say every fifth frame, which no player can detect.

That second point is a real technique and worth naming: **AI does not have to run every frame.** Nobody
can see the difference between an enemy that reconsiders 60 times a second and one that reconsiders 10
times a second, and the second costs a sixth as much.

### A vision cone, from one dot product

An enemy that sees in all directions is harder to sneak past than one with a face. Lesson 2's dot
product does this in one line:

```js
const toPlayer = player.pos.sub(enemy.pos).normalise();
const facing = Vec2.fromAngle(enemy.angle);
const inCone = facing.dot(toPlayer) > 0.7;       // 0.7 ≈ cos 45°, so ±45°
```

Raise the number to narrow the cone; `0` is 180°, and `-1` sees everywhere. The great advantage of using
the dot product rather than comparing angles is that there is no awkwardness around 359° being next to
1°.

### Steering: four behaviours that are all the same three lines

You already know **seek** and **flee** from lesson 2. Two more, and they are what make movement look
deliberate rather than robotic.

**Arrive** — seek, but slow down as you get close, so the enemy stops instead of orbiting:

```js
const toTarget = target.sub(e.pos);
const distance = toTarget.length();
let speed = MAX_SPEED;
if (distance < SLOW_RADIUS) {
  speed = MAX_SPEED * (distance / SLOW_RADIUS);     // proportional slow-down
}
e.vel = toTarget.normalise().scale(speed);
```

**Wander** — a direction that drifts, so a patrolling enemy does not look like it is on rails:

```js
/* Nudge the angle a little each frame rather than picking a new random direction.
   Picking a fresh random direction every frame gives a twitching mess; nudging
   gives a believable meander. The difference is one word: += instead of =. */
e.wanderAngle += (Math.random() - 0.5) * 2.5 * dt;
e.vel = Vec2.fromAngle(e.wanderAngle).scale(WANDER_SPEED);
```

**Separation** — the fix for the thing that ruins every first pack of enemies. Five chasers all run the
same recipe towards the same point, so they end up stacked in exactly the same place and look like one
enemy:

```js
let push = new Vec2(0, 0);
for (const other of enemies) {
  if (other === e) { continue; }
  const away = e.pos.sub(other.pos);
  const d = away.length();
  if (d > 0 && d < PERSONAL_SPACE) {
    /* closer means a stronger push: divide by the distance */
    push = push.add(away.normalise().scale((PERSONAL_SPACE - d) / PERSONAL_SPACE));
  }
}
e.vel = e.vel.add(push.scale(SEPARATION_STRENGTH));
```

Add those three lines and a pack of identical enemies immediately looks like a *group*: they spread,
they jostle, they surround. Nothing was added to any individual's behaviour.

### Making it fair, which is most of the work

An enemy that chases at exactly your speed, turns instantly, and shoots the moment it sees you is easy
to write and horrible to play. Four techniques, all deliberate handicaps:

| Technique | What it does | Why |
|---|---|---|
| **Reaction time** | wait 200–400 ms after noticing before acting | gives the player a moment; makes the enemy look like it is *realising* |
| **Telegraph** | a visible wind-up before an attack | the player can respond, so losing feels like their mistake |
| **Inaccuracy** | aim at the player's position plus a small random offset | perfect aim is unbeatable and reads as cheating |
| **Turn rate** | a maximum degrees-per-second, instead of snapping | you can outmanoeuvre it, which is a skill |

Every one of these makes the enemy *worse* at its job and the game *better*. That is the central idea of
the lesson and it is not obvious: you are not building the best opponent you can. You are building the
most **interesting** one.

And one more, which is almost a rule: **the player must be able to see why they lost.** If an enemy hits
you and you do not know what you should have done differently, that is a design fault, not a difficulty
setting.

---

## The idea, in pictures

Open [enemies that seem to think](../../../shared/visualizers/enemy-ai.html).

**What to look for:** drag the blue player and watch the **state box** change rather than the enemy's
code. Then look at the two circles: the inner one is where it notices you, the outer one is where it
gives up. Set the gap to **0** and walk along the edge — the state counter runs away as the guard changes
its mind several times a second. That flicker is what hysteresis exists to prevent, and seeing it once is
worth a paragraph of explanation.

Then open [the state machine explainer](../../../shared/visualizers/state-machine.html) and notice how
many transitions are *missing*. Each missing arrow is a bug you can no longer write.

---

## The idea, in code

1. `code/01-states-and-hysteresis.html` — patrol, chase and flee, with a switch that makes both
   thresholds the same so you can watch the flicker and count it.
2. `code/02-line-of-sight.html` — the stepped ray on a tilemap, drawn, with the step size on a slider so
   you can make it miss a thin wall on purpose.
3. `code/03-steering.html` — seek, flee, arrive, wander and separation on switches, with a pack of eight.
   Turn separation off and watch them become one enemy.
4. `code/04-a-fair-fight.html` — the same enemy made "perfect" or fair: reaction time, telegraph,
   inaccuracy and turn rate, each switchable. Play both.

---

## The maths you just used

**1. Two thresholds for one boundary.** If entering uses `d < A` and leaving uses `d > B` with `B > A`,
then there is a band between `A` and `B` where the state simply does not change. The width of that band
is how much noise the system can tolerate. Nothing deeper than that, and it is the whole of hysteresis.

**2. Stepping along a line.** Walking a ray is `start + direction × (i × STEP)` — the
subtract-normalise-scale recipe used as a loop. The step size is a trade: smaller is more accurate and
costs more. There is an exact algorithm for this (a grid traversal that visits every tile the line
passes through, with no step size at all), and it is in the advanced level; the stepped version is right
for now because you can read it.

**3. The dot product as a cone test.** For unit vectors, `dot` is the cosine of the angle between them.
So `dot > cos(θ)` means "within θ of straight ahead". `cos 45° ≈ 0.707`, `cos 30° ≈ 0.866`,
`cos 90° = 0`. One multiplication and two additions, and no angle arithmetic anywhere.

**4. Proportional slow-down.** `speed = MAX × (distance / SLOW_RADIUS)` is a straight line through the
origin: at the edge of the radius you get full speed, at the target you get zero. Square it
(`(d/r)²`) and the enemy holds its speed longer and then brakes harder, which feels more purposeful.
That is an easing curve from lesson 9, applied to speed.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Make both thresholds the same, then stand exactly on the boundary | | |
| Remove the line-of-sight test, keeping the distance test | | |
| Set the ray's step size to 3 tiles | | |
| Turn separation off with eight chasers | | |
| Replace `wanderAngle +=` with `wanderAngle =` | | |
| Set the vision cone threshold to `-1` | | |
| Give the enemy the same speed as the player | | |
| Remove the reaction delay and the inaccuracy | | |
| Run `decide()` only once every 60 frames | | |

The last one is the interesting one: predict how obviously broken it will look, then try it. One second
of reaction delay is noticeable; a sixth of a second is not, and that is a six-times saving nobody can
see.

---

## Think like an engineer

1. Our enemy decides and acts every frame. What is the *smallest* number of times per second it could
   reconsider before a player would notice? How would you find out — and does the answer depend on what
   the enemy is doing?
2. The guard gives up chasing when you get far enough away. What should it do *then* — go back to the
   start of its route, continue from where it is, or go to where it last saw you? Each produces a
   noticeably different kind of game. Pick one and say what it implies.
3. **Design something.** An enemy that is genuinely difficult but entirely fair: the player should lose
   and know exactly why. List what it does, what it telegraphs, how long each telegraph lasts, and what
   the player's counter is to each.
4. **The hard one.** A guard who notices you, loses you, and then **searches**: goes to where you were,
   looks around, and gives up after a while. That needs the enemy to remember something, and the memory
   has to expire. Where does that information live, and what does it look like in your state machine?

---

## Vocabulary

| Word | What it means |
|---|---|
| **State machine** | One value holding the current behaviour, with named transitions. |
| **Hysteresis** | Different thresholds for entering and leaving a state. Stops flicker. |
| **Line of sight** | Whether anything solid is between two points. |
| **Ray** | A line walked in small steps to test what it passes through. |
| **Vision cone** | A field of view, tested with one dot product. |
| **Seek / flee** | Move towards / away. The same line with the subtraction reversed. |
| **Arrive** | Seek that slows down near the target, so it stops instead of orbiting. |
| **Wander** | An angle that drifts. `+=`, never `=`. |
| **Separation** | A push away from neighbours. Turns a stack of enemies into a group. |
| **Telegraph** | A visible wind-up before an attack, so the player can respond. |
| **Reaction time** | A deliberate delay between noticing and acting. |

---

## Recap

- The illusion of intelligence comes from **switching between simple behaviours**, not from any one
  behaviour being clever.
- Keep **decide** and **act** separate. Adding a behaviour then touches nothing that already works.
- Use **two thresholds** for one boundary, or an enemy at the edge of its vision flickers every frame.
- Distance is not sight. **Walk a ray** and ask the tilemap, or your enemies see through walls.
- A **dot product** is a vision cone, with no angle arithmetic.
- **Separation** is three lines and turns a stack of chasers into a pack.
- An enemy is made good by being made **worse**: reaction time, telegraphs, inaccuracy, turn limits.
- AI need not run every frame. Ten times a second is usually indistinguishable from sixty.

---

## Stretch goals

1. **Search.** Question 4: remember the last known position, go there, look around, give up.
2. **Alert the others.** When one enemy sees you, nearby enemies enter chase too — but only if they are
   close enough to have "heard". One distance test, and the game feels completely different.
3. **Flow.** Give the flyer a wander that is biased towards the player, so it drifts closer in a curve
   rather than making straight for them.
4. **A difficulty dial.** One number from 0 to 1 that adjusts reaction time, accuracy, speed and turn
   rate together. Then play at 0.2 and at 0.9 and write down which parts of it actually change the
   difficulty, and which just change how it feels.
5. **Group tactics.** Make three chasers approach from different sides rather than all from the front.
   You have separation; what else is needed?

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `04-a-fair-fight.html` with the enemy set to "perfect" and let a confident student try to beat it. They cannot. Then switch the four handicaps on and let them try again. The point lands without being stated. |
| 10–25 | **Concept.** The enemy AI visualizer, mostly on the two circles and the flicker at gap = 0. Then decide/act on the board. |
| 25–40 | **Live-code** `decide()` and `act()` for patrol and chase. Add flee as a question to the class rather than writing it. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–4 are the core; separation in checkpoint 5 produces the loudest reaction. |
| 120–140 | Break-it-on-purpose. Separation off with eight enemies is the best demonstration. |
| 140–150 | Recap. Lesson 11 saves the high score; lesson 12 is the capstone. |

**What usually goes wrong**

1. **The enemy flickers at the edge of its vision.** One threshold. This is the lesson, so let it happen
   before you fix it.
2. **Enemies stack into one lump.** No separation. They will often conclude their code is wrong when every
   individual enemy is behaving perfectly — a good moment to talk about emergent behaviour.
3. **Enemies see through walls.** Distance only. Students find this one themselves as soon as they play.
4. **The ray misses thin walls.** Step size bigger than a tile.
5. **`decide` and `act` tangled**, so `decide` moves the enemy and `act` changes the mode. The symptom is
   an enemy that is in two states in one frame. Insist on the separation.
6. **The enemy is unbeatable** and the student is proud of it. Ask them to let a classmate play it. The
   feedback is more persuasive than anything you can say.
7. **Wander twitches.** `wanderAngle =` instead of `+=`.
8. **`NaN` enemies disappearing.** Normalising a zero vector when the enemy reaches the player exactly.
   Lesson 2's guard, needed again.

**If you are running short on time** — cut steering (`code/03`) and keep patrol/chase/flee plus line of
sight. Or cut line of sight and keep steering; both are good lessons and either survives alone. Do **not**
cut hysteresis or the fairness discussion.

**For the student who finishes at minute 90** — stretch goal 2 (alerting other enemies) is a single
distance test and changes the whole feel of a level, so it is the best value. Stretch goal 1 (search) is
the most interesting and takes the longest.

**The point to land at the end:** they made an enemy *worse* at its job four times over, and the game got
better each time. An opponent is not a problem to be solved optimally. It is something the player has to
be able to read, respond to, and beat — and designing for that is a completely different job from
designing for strength.
