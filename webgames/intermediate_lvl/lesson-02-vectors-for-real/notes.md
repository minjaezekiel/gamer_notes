# Lesson 2 — Vectors For Real

> **Web Games · Intermediate level · Lesson 2 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A ship that flies in **any** direction, turns to face where it is going, and fires bullets along
whatever line it is pointing down — plus a small swarm of chasers that home in on it.

```
                    ·
              ·      ╲
         ▲            ╲        ← bullets leave along the nose,
        ╱ ╲            ·          not along x or y
       ╱   ╲
      ───────         ◆  ◆     ← chasers, all heading for the ship
                        ◆
```

Everything in that picture is the same four-line idea applied four times. By the end you will have a
file called `vec2.js` that you will keep using for the rest of this course.

## Where this fits

- **Back:** [lesson 1](../lesson-01-one-file-becomes-many/notes.md) gave you somewhere to put this
  file. Beginner [lesson 3](../../beginner_lvl/lesson-03-player-in-control/notes.md) left you with a
  bug on purpose: moving diagonally was 41% faster than moving straight. Today you fix it properly.
- **Forward:** [lesson 3](../lesson-03-acceleration-friction-and-drag/notes.md) adds acceleration to
  this ship. Everything from here to lesson 12 uses vectors, so this is the highest-leverage lesson
  in the level.
- **Other tracks:** Python's intermediate lesson 3 uses pygame's built-in `Vector2`, and C++'s
  intermediate lesson 5 uses raylib's `Vector2` with `raymath`. Both of those are *this file*, written
  by somebody else. Knowing what is inside it is why you are writing your own first.

---

## The idea, in plain words

### Two numbers that belong together

You have been writing this since beginner lesson 2:

```js
ball.x += ball.speedX * dt;
ball.y += ball.speedY * dt;
```

Two lines, almost identical, and you have to remember to change both. Forget one and you get a bug
that looks like physics: the ball drifts sideways and you cannot see why.

A **vector** is just the admission that `x` and `y` are not two separate facts. They are one fact
with two parts. "Move 30 right and 40 down" is a single instruction, so it should be a single thing in
your program.

### The arrow analogy, and where it breaks

Picture a vector as an **arrow**: it has a direction and a length, and it does *not* have a position —
an arrow meaning "30 right, 40 down" is the same arrow wherever you draw it.

That gets you a long way. Here is where it breaks, and it trips up almost everybody: **the same two
numbers are used for two different jobs.** `(100, 50)` can mean

- *a place*: the ship is at x=100, y=50 — an arrow drawn from the origin to the ship; or
- *a movement*: go 100 right and 50 down — an arrow you could draw anywhere.

They are the same type and they are not the same kind of thing. Adding two positions together is
almost always a bug. Adding a movement to a position is the single most common line in game
programming. You will write both this term, and knowing which you have is most of what stops a vector
library from feeling like magic.

### Three operations are enough for a game

| Operation | What it means in a game |
|---|---|
| **add** | "and then move by this as well" |
| **subtract** | **"from here, how do I get to there?"** |
| **scale** (multiply by one number) | "same direction, different amount" |

Subtract is the one that does the real work, and it is worth saying very plainly:

> **target − me = the way to the target.**

Every chasing enemy, every homing missile, every "look at the mouse" and every knockback in every
game you have played starts with that subtraction.

### Length, and the one operation that matters most

The **length** (or **magnitude**) of a vector is how long the arrow is. You already know how to work
it out: it is Pythagoras, which you used in beginner lesson 4 for circle collisions.

But look at what subtract gives you. `target − me` points the right way, and its length is *however
far apart they happen to be*. If you use it as a speed, your enemy moves fast when far away and
crawls when close. That is not what anyone wants.

So you **normalise**: keep the direction, force the length to exactly 1.

```
          divide both parts by the length
(30, 40)  ───────────────────────────────→  (0.6, 0.8)
length 50                                   length 1
```

A vector of length 1 is called a **unit vector**, and it is the single most useful object in game
maths, because it is a *pure direction* with the distance stripped out. Then you multiply by whatever
speed you actually wanted:

```
direction (length 1)  ×  speed  =  velocity
```

**Subtract, normalise, scale.** Those three steps are the recipe, and you will write them so many
times this term that they stop looking like maths.

> **The one trap.** If `target` and `me` are in exactly the same place, the subtraction gives
> `(0, 0)`, whose length is 0, and dividing by 0 gives `NaN` — "not a number". `NaN` spreads: one
> `NaN` position means the sprite vanishes with no error message at all, forever. Check the length
> before you divide. Every single time. This is the most common crash in this lesson and the hardest
> to diagnose, because nothing throws.

---

## The idea, in pictures

Open [the vectors explainer](../../../shared/visualizers/vectors.html).

**What to look for:** drag the two arrow tips. Watch the **length** number change, and find the
positions where one arrow is exactly `(0.6, 0.8)` or `(1, 0)` — those are unit vectors. Then use the
normalise control: the arrow keeps pointing the same way and snaps to the same length every time,
whatever you do to it. That snapping-to-one is the whole idea. Finally, drag both tips to the same
spot and watch the numbers break.

Then open [acceleration, friction and drag](../../../shared/visualizers/acceleration-and-friction.html)
and drag the target around. That is subtract-normalise-scale running 30 times a second, and it is
exactly what you are about to write.

---

## The idea, in code

### Step 1: the diagonal bug, measured

Run `code/01-the-diagonal-bug.html`. Move with the arrow keys and watch the speed readout.

```js
// What you wrote at beginner level.
if (keys["ArrowRight"]) { player.x += SPEED * dt; }
if (keys["ArrowDown"])  { player.y += SPEED * dt; }
```

Straight: 300 px/s. Diagonally: 424 px/s. Players find this in under a minute and then run everywhere
diagonally, because you accidentally rewarded it.

The fix is not a special case for diagonals. The fix is to stop treating the two axes as separate
decisions:

```js
// 1. Collect the intent as ONE vector. Its length is 1, or 1.414, or 0.
let moveX = 0;
let moveY = 0;
if (keys["ArrowRight"]) { moveX += 1; }
if (keys["ArrowLeft"])  { moveX -= 1; }
if (keys["ArrowDown"])  { moveY += 1; }
if (keys["ArrowUp"])    { moveY -= 1; }

// 2. Normalise it, so "some direction" always means the same amount of push.
const length = Math.hypot(moveX, moveY);
if (length > 0) {                      // the NaN guard. Never skip it.
  moveX = moveX / length;
  moveY = moveY / length;
}

// 3. Scale by the speed you meant.
player.x += moveX * SPEED * dt;
player.y += moveY * SPEED * dt;
```

Toggle the fix on in the example and watch the readout stay at 300 in all eight directions.

`Math.hypot(a, b)` is Pythagoras with a name. It returns `√(a² + b²)`.

### Step 2: a Vec2 you will keep

```js
/* vec2.js — two numbers that travel together.

   Every method returns a NEW Vec2 rather than changing this one. That is more
   objects than a professional engine would make, and it is the right trade at
   this point: nothing can be modified behind your back, so a bug in one place
   cannot show up in another. Lesson 9 revisits the cost. */
export class Vec2 {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  // "and then also move by other"
  add(other) { return new Vec2(this.x + other.x, this.y + other.y); }

  // "from other, how do I get to this?"  →  this - other
  sub(other) { return new Vec2(this.x - other.x, this.y - other.y); }

  // same direction, different amount
  scale(k) { return new Vec2(this.x * k, this.y * k); }

  // how long the arrow is. Pythagoras.
  length() { return Math.hypot(this.x, this.y); }

  /* Comparing distances does not need the square root, and square roots are the
     expensive part. If a² + b² is bigger, so is √(a² + b²). Lesson 9 measures
     this; for now, know the function exists and why. */
  lengthSquared() { return this.x * this.x + this.y * this.y; }

  /* Same direction, length exactly 1 — unless there is no direction at all, in
     which case there is no honest answer and we return (0, 0) rather than NaN. */
  normalise() {
    const len = this.length();
    if (len === 0) { return new Vec2(0, 0); }
    return new Vec2(this.x / len, this.y / len);
  }

  // How far is it from here to there?
  distanceTo(other) { return this.sub(other).length(); }

  /* Which way is this arrow pointing, as an angle in radians?
     Note the argument order: y FIRST. It is the commonest mistake with atan2. */
  angle() { return Math.atan2(this.y, this.x); }

  /* Build a unit vector from an angle. The pair of these two is how you get
     between "an angle" and "a direction". */
  static fromAngle(radians) {
    return new Vec2(Math.cos(radians), Math.sin(radians));
  }
}
```

That is the whole file, and it will serve you for the rest of the course.

### Step 3: the recipe, three times

Once you have `Vec2`, three different-looking game features turn out to be the same three lines.

```js
// A chaser homing in on the player.
const toPlayer = player.pos.sub(enemy.pos);        // subtract
const direction = toPlayer.normalise();            // normalise
enemy.pos = enemy.pos.add(direction.scale(ENEMY_SPEED * dt));   // scale, then add
```

```js
// A bullet leaving the ship's nose, along whatever way it is facing.
const nose = Vec2.fromAngle(ship.angle);           // a direction, length 1
bullet.pos = ship.pos.add(nose.scale(18));         // start just in front
bullet.vel = nose.scale(BULLET_SPEED);             // fly that way
```

```js
// Knockback: push the player AWAY from an explosion.
const away = player.pos.sub(blast.pos).normalise(); // note the order: away, not towards
player.vel = player.vel.add(away.scale(KNOCKBACK));
```

Three features. One idea. The only thing that changed between them is *which way round the subtraction
goes* and *what number you scale by*. That is what people mean when they say vectors make game code
shorter: not fewer characters, but fewer ideas.

### Step 4: angles, and how to face where you are going

Run `code/03-aim-and-shoot.html`.

```js
// Turning: an angle is a single number, in radians, and it changes like anything
// else — a little bit every frame.
if (keys["ArrowLeft"])  { ship.angle -= TURN_SPEED * dt; }
if (keys["ArrowRight"]) { ship.angle += TURN_SPEED * dt; }

// Drawing something rotated: move the canvas, spin it, draw at the origin,
// then put it back. save() and restore() are a matching pair, always.
ctx.save();
ctx.translate(ship.pos.x, ship.pos.y);
ctx.rotate(ship.angle);
drawShipShape(ctx);           // drawn as if the ship were at (0,0) facing right
ctx.restore();
```

Two details that cost people an hour each:

- **Angle 0 points right, not up.** The positive x direction is zero. So draw your ship pointing
  right, or add a quarter turn when you draw it.
- **Angles go clockwise**, because y points down. On a maths test they go anticlockwise. Both are
  "correct"; the screen's y direction is what flips it.

---

## The maths you just used

You just used four pieces of real mathematics, and you used them before anybody named them.

**1. Pythagoras.** `length = √(x² + y²)`. You met this for circle collisions; it is the same theorem
doing the same job. `Math.hypot` is its name in JavaScript.

**2. Unit vectors.** Dividing both parts by the length leaves the direction untouched and forces the
length to 1. Check it: `(30, 40)` has length 50, and `(0.6, 0.8)` gives `√(0.36 + 0.64) = √1 = 1`.

**3. `atan2` and `cos`/`sin`.** These convert between the two ways of saying the same thing:

```
(x, y)  ──atan2(y, x)──→  angle
angle   ──cos, sin─────→  (x, y)
```

That is all the trigonometry this course needs. You do not have to remember what cosine *is* to use
it correctly: `cos` gives the x part of a direction and `sin` gives the y part, and for a unit vector
nothing else is required.

**4. The dot product** — one new thing, and it is useful enough to be worth the two minutes.

```js
dot(other) { return this.x * other.x + this.y * other.y; }
```

Multiply the x parts, multiply the y parts, add them. For two **unit** vectors the answer is:

| dot | meaning |
|---|---|
| `1` | pointing exactly the same way |
| `0` | at right angles |
| `−1` | pointing exactly opposite |

So "is the guard facing the player?" is one line, with no angles, no `atan2`, and no awkwardness
about 359° being next to 1°:

```js
const toPlayer = player.pos.sub(guard.pos).normalise();
const facing = Vec2.fromAngle(guard.angle);
if (facing.dot(toPlayer) > 0.7) {
  // the player is within about 45° of straight ahead
}
```

`0.7` is roughly `cos(45°)`. Lower the number to widen the cone. You have just written a field of
view, and you can see it working in `code/04-chase-and-flee.html`.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the `if (len === 0)` guard, then put a chaser exactly on the player | | |
| In the chaser, forget `.normalise()` | | |
| Swap the subtraction: `enemy.pos.sub(player.pos)` | | |
| Use `atan2(x, y)` instead of `atan2(y, x)` | | |
| Delete `ctx.restore()` | | |
| Scale the direction by `SPEED` but forget `* dt` | | |
| Set the facing-cone threshold to `-1` | | |

The first one is the important one: predict the error message, then look. There is no error message.
The chaser simply disappears and never comes back, because `NaN` is contagious — every number it
touches becomes `NaN` too, forever.

Deleting `restore()` is almost as instructive: every frame adds another rotation, so after ten seconds
your whole game is spinning.

---

## Think like an engineer

1. Our `Vec2` methods each build a **new** object. A chaser that runs the recipe makes three new
   `Vec2`s per frame; a hundred chasers make 18,000 a second. Is that a problem? How would you find
   out, rather than guess? (Lesson 9 measures it. Make a prediction now and write it down.)
2. We wrote `normalise()` returning `(0, 0)` for a zero-length vector. Three other designs: throw an
   error, return `null`, or return `(1, 0)`. Argue for one. Which is most likely to hide a bug, and
   which is most likely to be annoying?
3. **Design something.** A homing missile that turns towards its target rather than snapping to face
   it — so it can miss, loop round, and come back. What does it need to remember beyond a position?
   What stops it turning instantly? Sketch the update function in words.
4. **The hard one.** A ball bounces off a flat wall by flipping one speed component. What about a wall
   at 30°? You have everything you need: a unit vector along the wall, a unit vector at right angles
   to it, and the dot product. Work out what "the part of my velocity that points into the wall"
   means, and what you would do to it. This is a real formula with a real name, and your version will
   probably be close.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Vector** | Two (or three) numbers treated as one thing: a direction and a length. |
| **Magnitude / length** | How long the arrow is. `√(x² + y²)`. |
| **Unit vector** | A vector of length exactly 1. A pure direction. |
| **Normalise** | Divide by the length, to get the unit vector pointing the same way. |
| **Scale** | Multiply by one number. Changes length, not direction. |
| **Dot product** | `x1·x2 + y1·y2`. For unit vectors: 1 same way, 0 at right angles, −1 opposite. |
| **Radian** | The angle unit JavaScript uses. A full turn is `2π ≈ 6.283`. |
| **`atan2(y, x)`** | Direction → angle. **y first.** |
| **`NaN`** | "Not a number". What `0 / 0` gives. It spreads silently. |
| **Immutable** | Never changed after it is made. Our `Vec2` is immutable. |

---

## Recap

- `x` and `y` are one fact, not two. Treat them as one thing and whole classes of bug disappear.
- **target − me** is the direction from me to the target. This is the most useful line in game code.
- **Subtract, normalise, scale.** Chasing, aiming, shooting and knockback are all this recipe.
- Normalising a zero-length vector gives `NaN`, which never throws and never recovers. Guard it.
- `atan2` turns a direction into an angle; `cos`/`sin` turn an angle back into a direction.
- Angle 0 points **right**, and angles increase **clockwise** on screen, because y points down.

---

## Stretch goals

1. **Add `rotate(radians)`** to `Vec2`, without using `atan2`. The formula is
   `x' = x·cos − y·sin`, `y' = x·sin + y·cos`. Then make a chaser that circles its target instead of
   ramming it.
2. **Turn, do not snap.** Make the chaser's facing turn at a maximum of 180°/second towards the
   player. It will now overshoot and curve, which looks far more alive.
3. **`lerp(a, b, t)` for vectors.** Then make the camera, a health bar and a menu item all ease into
   place with the same three lines.
4. **Measure the cost.** Write a loop that creates ten million `Vec2`s and time it with
   `performance.now()`. Then write a mutable version (`addInPlace`) and time that. Report real
   numbers, not opinions.
5. **The 30° wall.** Attempt question 4 above for real. Bounce a ball off a slope you can drag.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `01-the-diagonal-bug.html` on the projector with the speed readout showing. Walk straight: 300. Walk diagonally: 424. Ask whether this is a bug or a feature — some will argue feature, which is a good argument to have. |
| 10–25 | **Concept.** The vectors visualizer. Spend most of it on *normalise*: drag an arrow all over the canvas and show the unit version refusing to change length. Then subtract-normalise-scale on the board, named as a recipe. |
| 25–40 | **Live-code** `Vec2` with them — `add`, `sub`, `scale`, `length`, `normalise`. Five methods, ten minutes, and they type it with you. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D: the ship, then the chasers. |
| 120–140 | Break-it-on-purpose. Do the `NaN` one together; it is the most valuable five minutes of the lesson. |
| 140–150 | Recap. Lesson 3 makes this ship feel good rather than merely work. |

**What usually goes wrong**

1. **`NaN` everywhere and no error message.** Something normalised a zero vector — usually a chaser
   spawning exactly on the player, or a bullet fired while the ship is stationary. Teach the symptom:
   *a thing vanished and the console is clean* means check for `NaN` first. `console.log` the vector,
   or test `Number.isNaN(x)`.
2. **The subtraction is backwards.** The chaser flees instead of chasing. Students fix this by
   negating the speed, which works and leaves them not understanding. Make them say the sentence out
   loud: "target minus me". The direction of a subtraction is not arbitrary.
3. **`atan2(x, y)`.** The ship points at 90° to where it is going. Extremely common; the argument
   order genuinely is surprising.
4. **Degrees and radians mixed.** `ship.angle = 45` turns the ship by seven and a bit full circles.
   Suggest `Math.PI / 4`, or a `degrees()` helper, but pick one and stay with it.
5. **Forgetting `ctx.restore()`.** The entire game starts rotating. Looks like a catastrophe, is one
   missing line. Teach save/restore as a matching pair from the start — like opening and closing a
   bracket.
6. **Normalising, then forgetting to scale.** The enemy moves at 1 pixel per second and looks frozen.
   Ask what units a unit vector is in. (None. That is the point of it.)
7. **Using positions as directions.** `enemy.pos.add(player.pos)` sends the enemy into a corner. Go
   back to the two-jobs-one-type idea in the notes.

**If you are running short on time** — cut the dot product and the facing cone entirely; they are a
bonus, and lesson 10 can introduce them when enemies need them. Cut `code/04` too. Do **not** cut
normalise or the `NaN` guard: everything after today depends on both.

**For the student who finishes at minute 90** — stretch goal 2 (turn, do not snap) is the best one;
it produces visibly better-looking movement than the lesson's own version, which is motivating.
Stretch goal 4 suits anyone who likes measuring things.

**The point to land at the end:** they wrote one small file, and with it, chasing, aiming, shooting
and knockback became the same three lines. That is what a good abstraction does. It does not hide the
maths — they can read every line of `Vec2` — it stops them having to think about it again.
