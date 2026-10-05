# Lesson 3 — Acceleration, Friction And Drag

> **Web Games · Intermediate level · Lesson 3 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A ship that **feels** like something. Not a rectangle that teleports when you press a key — a thing
with weight, that takes a moment to get going, slides when you let go, and has a top speed.

And next to it, a panel of four sliders. You will spend the last twenty minutes of the lesson moving
those sliders until the ship feels right to *you*, and then comparing with the person next to you,
who will have chosen different numbers.

```
   press and hold →                    release →

   ·                                   ▸▸▸▸▸▸▸▸▸ ·  ·   ·    ·     ·
   ·▸                                  it keeps going, and slows down
   ·▸▸
   ·▸▸▸▸          it builds up
   ·▸▸▸▸▸▸▸
```

That is the whole lesson: **four numbers, and the judgement to pick them.**

## Where this fits

- **Back:** [lesson 2](../lesson-02-vectors-for-real/notes.md) gave you direction. Beginner
  [lesson 2](../../beginner_lvl/lesson-02-moving-pictures/notes.md) gave you velocity, and beginner
  lesson 3 ended with a question: *is instant response actually good?* Today is the answer.
- **Forward:** [lesson 12](../lesson-12-capstone-a-platformer/notes.md)'s platformer is this lesson
  plus gravity plus a jump. [Lesson 9](../lesson-09-particles-and-juice-engineering/notes.md) is about
  everything else that makes a game feel good.
- **Other tracks:** Python's intermediate lesson 3 and C++'s intermediate lesson 5 do this with their
  own `Vector2`. The three numbers are the same three numbers.

---

## The idea, in plain words

### Three levels of "how things move"

You have already met two of them.

| What you change | Called | What it feels like |
|---|---|---|
| position directly | *teleporting* | instant, weightless, arcade |
| velocity directly | *constant speed* | responsive, slightly robotic |
| **acceleration** | *momentum* | heavy, physical, real |

Beginner lesson 2 moved from the first to the second. Today you move to the third, and the jump is
bigger than it sounds, because **you stop controlling the thing you want to control.** Pressing a key
no longer decides where the ship goes. It decides how hard the ship is being *pushed*. Where it ends
up is a consequence.

That is uncomfortable to program and it is why the result feels alive.

### The chain, as vectors

In beginner lesson 2 you wrote a chain of two additions for gravity:

```js
ball.vy = ball.vy + GRAVITY * dt;    // acceleration changes velocity
ball.y  = ball.y  + ball.vy * dt;    // velocity changes position
```

With `Vec2` from lesson 2, that same chain works in any direction:

```js
ship.vel = ship.vel.add(acceleration.scale(dt));   // push changes speed
ship.pos = ship.pos.add(ship.vel.scale(dt));       // speed changes place
```

Those two lines are the entire physics of most 2D games. Everything else is a decision about what
`acceleration` should be.

### Friction is what makes it playable

Acceleration alone gives you a ship that goes faster for ever. Tap forward for three seconds and you
will never see it again.

So every frame, you take a little velocity back:

```js
ship.vel = ship.vel.scale(0.98);     // keep 98% of it
```

Two things about that line. First, it is why the ship slides to a stop instead of stopping dead —
it is doing the "slide a little after you release" that beginner lesson 3 asked you to design.

Second: **as written, it is a bug.** A quiet one, which is why it gets its own section.

### Why `vel * 0.98` is frame-rate dependent

That `0.98` happens *per frame*. Count the frames:

- At 60 fps: 60 multiplications a second. `0.98⁶⁰ ≈ 0.30`, so about **70%** of the speed is gone.
- At 30 fps: 30 multiplications. `0.98³⁰ ≈ 0.55`, so about **45%** is gone.
- At 144 fps: `0.98¹⁴⁴ ≈ 0.055`, so **94%** is gone.

The same code, the same number, and the ship is a brick on a gaming monitor and an ice cube on a
school laptop. Nobody notices while they only ever test on one machine, which is exactly how this ends
up in a finished game.

This is the same mistake as forgetting `* dt`, in a disguise good enough to fool most people: there is
no `dt` missing from the line, so it *looks* fine.

The fix is to say what you mean. You do not want "multiply by 0.98 each frame". You want **"lose a
fixed share of your speed each second"**:

```js
const DRAG = 3.0;                               // per second
ship.vel = ship.vel.scale(Math.exp(-DRAG * dt));
```

`Math.exp(-DRAG * dt)` is a number slightly less than 1, and it adjusts itself to the length of the
frame. Double the frame rate and each multiplication is gentler, so the total over one second is
identical. Try it in `code/02-friction-and-frame-rate.html`, where three ships run at three different
frame rates side by side.

> **If `exp` feels like too much**, `1 - DRAG * dt` is close enough for a game and is what most
> tutorials write. It drifts from the exact answer when `dt` is large, and it goes *negative* if
> `DRAG * dt` ever exceeds 1 — which flips your ship into reverse. `exp` cannot do that, which is why
> it is worth the extra characters.

### A speed limit, applied to the whole speed

```js
// WRONG: this limits each direction separately, so diagonal is still faster.
if (ship.vel.x > MAX) { ship.vel.x = MAX; }
if (ship.vel.y > MAX) { ship.vel.y = MAX; }

// RIGHT: limit the LENGTH, keep the direction.
if (ship.vel.length() > MAX_SPEED) {
  ship.vel = ship.vel.normalise().scale(MAX_SPEED);
}
```

The wrong version is the diagonal bug from lesson 2 wearing a different hat. It will come back in
every lesson until you treat x and y as one thing.

### The four numbers, and what each one actually controls

| Number | Units | What the player feels |
|---|---|---|
| `THRUST` | px/s per s | how quickly it gets going — *responsiveness* |
| `DRAG` | per second | how quickly it stops — *weight* |
| `MAX_SPEED` | px/s | how fast it can ever go — *scale of the world* |
| `TURN_SPEED` | radians/s | how sharply it can change its mind — *agility* |

Here is the thing nobody tells you: **those four numbers are not independent.** Raise `DRAG` and the
ship also becomes slower at top speed, because drag fights thrust. In fact, if you hold thrust for
long enough, the ship settles at a speed where the two exactly cancel:

```
settled speed = THRUST / DRAG
```

So `THRUST = 900` and `DRAG = 3` gives a natural top speed of 300 px/s, and your `MAX_SPEED` of 420
will never be reached. That is not a bug — but if you did not know it, you would spend an hour
wondering why the slider does nothing.

That settled speed has a name in physics: **terminal velocity**. You can watch it happen in
`code/04-gravity-and-drag.html`, where a falling ball stops speeding up.

---

## The idea, in pictures

Open [acceleration, friction and drag](../../../shared/visualizers/acceleration-and-friction.html).

**What to look for:** drag the orange target and watch the ship *overshoot* it. That is not a bug —
anything with momentum that is pulled towards a point will sail past it. Now set friction to 0: the
ship orbits for ever and can never settle, because nothing is removing energy. Turn friction up and
the same code feels like a car on tarmac. **Then switch on "friction per frame" and watch the ship
become sluggish**, because this sketch runs at 30 fps rather than 60, and the per-frame version is
being applied half as often as its author assumed.

Also open [easing](../../../shared/visualizers/easing.html) and look at `easeOutQuad`. A ship under
drag follows almost exactly that curve, for the same reason: both take a share of what is left.

---

## The idea, in code

### Step 1: see the difference

Run `code/01-set-vs-accelerate.html`. Two ships, the same keys, one line different.

```js
// Ship A — velocity set directly. What you wrote at beginner level.
if (keys["ArrowUp"]) { shipA.vel = nose.scale(SPEED); }
else                 { shipA.vel = new Vec2(0, 0); }

// Ship B — velocity ACCUMULATED.
if (keys["ArrowUp"]) { shipB.vel = shipB.vel.add(nose.scale(THRUST * dt)); }
shipB.vel = shipB.vel.scale(Math.exp(-DRAG * dt));
```

Fly both. Ship A obeys you. Ship B *has an opinion*. Try turning sharply at speed in both: A changes
direction instantly, B carries on roughly the way it was going and curves round. That curve is
momentum, and it is the whole reason the second one is more fun.

### Step 2: the full update, in the order that matters

```js
function updateShip(ship, dt) {
  /* 1. TURN. An angle is just a number that changes a little every frame. */
  if (keys["ArrowLeft"])  { ship.angle -= TURN_SPEED * dt; }
  if (keys["ArrowRight"]) { ship.angle += TURN_SPEED * dt; }

  /* 2. BUILD THE ACCELERATION. Start at zero and add every push there is.
        Doing it this way means gravity, wind and thrust combine for free. */
  let acceleration = new Vec2(0, 0);
  if (keys["ArrowUp"]) {
    const nose = Vec2.fromAngle(ship.angle);        // a pure direction
    acceleration = acceleration.add(nose.scale(THRUST));
  }

  /* 3. ACCELERATION CHANGES VELOCITY. */
  ship.vel = ship.vel.add(acceleration.scale(dt));

  /* 4. DRAG takes back a share of the velocity, measured PER SECOND. */
  ship.vel = ship.vel.scale(Math.exp(-DRAG * dt));

  /* 5. SPEED LIMIT, on the length, not on x and y separately. */
  if (ship.vel.length() > MAX_SPEED) {
    ship.vel = ship.vel.normalise().scale(MAX_SPEED);
  }

  /* 6. VELOCITY CHANGES POSITION. Always last. */
  ship.pos = ship.pos.add(ship.vel.scale(dt));
}
```

Six steps, and the order is not a matter of taste. Move step 6 above step 3 and the ship is using
last frame's velocity — which is a tiny, nearly invisible lag that makes the controls feel slightly
dead. Nobody will be able to tell you why.

### Step 3: two different kinds of slowing down

Multiplying is not the only way to lose speed, and the two feel different enough to be worth knowing.

```js
// DRAG (multiply): takes a SHARE. Fast things slow quickly, slow things gently.
// Never quite reaches zero. Feels like air or water. Good for ships, floaty things.
vel = vel.scale(Math.exp(-DRAG * dt));

// FRICTION (subtract): takes a FIXED AMOUNT. Slows everything equally and
// actually stops. Feels like a surface. Good for things on the ground.
const loss = FRICTION * dt;
if (vel.length() <= loss) {
  vel = new Vec2(0, 0);              // this test is NOT optional
} else {
  vel = vel.sub(vel.normalise().scale(loss));
}
```

That `if` is the whole trick with subtractive friction: without it, the subtraction overshoots zero
and the ship **drives slowly backwards for ever**. It is a genuinely confusing bug, because the
numbers are tiny and the movement looks like a drift.

Most games use both: drag in the air, friction on the ground. Switching between them is one line and
completely changes how a character feels.

### Step 4: tune it, and write down what you chose

Run `code/03-ship-feel.html` and press `1` to `4` for the presets. They use the same code.

| Preset | THRUST | DRAG | MAX | feels like |
|---|---|---|---|---|
| 1 — Spaceship | 420 | 0.3 | 500 | drifting in vacuum. Hard to control, and exciting. |
| 2 — Car | 900 | 2.5 | 380 | grippy, predictable, a bit heavy. |
| 3 — Ice | 300 | 0.15 | 450 | a sheet of ice. Infuriating on purpose. |
| 4 — Snappy | 4000 | 14 | 320 | nearly instant, with a flicker of weight. |

Preset 4 is worth staring at. `THRUST` is enormous and `DRAG` is enormous, so the ship reaches top
speed in about a tenth of a second and stops in about a tenth of a second. It is almost the
beginner-level "set the velocity" version — but *almost* is what makes it feel good instead of
mechanical. Most well-regarded 2D action games live near preset 4, not near preset 1.

---

## The maths you just used

**1. The chain rule of game physics** (not the calculus one). Acceleration changes velocity;
velocity changes position. Two additions, in that order, every frame. Doing them in the wrong order
costs you one frame of responsiveness.

**2. Exponential decay.** Multiplying by the same factor repeatedly is the thing that sits underneath
radioactive half-lives, cooling cups of tea, and the volume of an echo. After time `t`, with a decay
rate `k`:

```
remaining = starting × e^(−k·t)
```

which in code is `Math.exp(-k * t)`. The useful property, and the reason it fixes the frame-rate bug:
splitting the time into smaller pieces gives exactly the same total.

```
e^(−k·1)  ===  e^(−k·0.5) × e^(−k·0.5)
```

A per-frame multiplier does not have that property, which is precisely why it breaks when the frame
length changes.

If you want a number you can feel rather than a letter, the **half-life** is how long it takes to lose
half the speed:

```
half-life = ln(2) / DRAG ≈ 0.693 / DRAG
```

So `DRAG = 3` halves the ship's speed every quarter of a second. That is a far more useful sentence to
tune with than "the drag is three".

**3. Terminal velocity.** Thrust pushes, drag pulls back in proportion to speed, and they meet:

```
THRUST = DRAG × speed        →        speed = THRUST / DRAG
```

That is where your ship settles, and it is why raising one slider seems to move another.

**4. Clamping a vector's length.** `normalise().scale(MAX)` keeps the direction and replaces the
length. The same two-step idea as lesson 2, used for a different purpose.

---

## Break it on purpose

Use `code/03-ship-feel.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| `DRAG` to 0 | | |
| `DRAG` to 200 | | |
| Replace `exp(-DRAG*dt)` with a flat `* 0.98` and set the frame rate to 20 | | |
| Clamp `vel.x` and `vel.y` separately instead of the length | | |
| Move "position += velocity" to the top of the update | | |
| Use subtractive friction and remove the `if (length <= loss)` test | | |
| `THRUST` 5000 with `DRAG` 0.2 | | |
| `TURN_SPEED` to 20 | | |

The subtractive-friction one is the most instructive: predict the direction the ship ends up moving
in. Then watch it reverse.

---

## Think like an engineer

1. You have four sliders and no idea where to start. Invent a **procedure** for tuning them, in an
   order, with a question you are answering at each step. (Hint: which of the four can you judge with
   your eyes closed to the other three?)
2. Preset 4 is nearly the beginner version, but not quite. Is the difference worth the extra code? How
   would you *find out* rather than argue — what would you measure, or who would you ask, and what
   would you ask them?
3. **Design something.** A car that grips when driving forwards and slides when driving sideways. Your
   `Vec2` can already tell you how much of the velocity points along the car and how much points
   across it. What would you apply to each part, and what would the car then feel like?
4. **The hard one.** Your ship feels great. Now the player picks up a "slippery ice" power-up, and the
   handling must change over half a second and change back when it wears off. Four numbers have to
   travel from one set of values to another and back. What does that machinery look like, and where in
   your program does it live? (There is a general answer here that is useful for far more than ice.)

Question 3 is how every racing game works, and your own version will be close.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Acceleration** | A change in velocity. Measured in px/s *per second*. |
| **Momentum** | The tendency to keep moving the way you already were. |
| **Drag** | Slowing by multiplying — takes a *share*. Never quite reaches zero. |
| **Friction** | Slowing by subtracting — takes a *fixed amount*. Actually stops. |
| **Exponential decay** | Repeated multiplication by the same factor. `Math.exp(-k*dt)`. |
| **Half-life** | How long to lose half of it. `ln(2) / k`. |
| **Terminal velocity** | The speed where push and drag cancel. `THRUST / DRAG`. |
| **Clamping a length** | `normalise().scale(MAX)` — keep direction, set length. |
| **Frame-rate dependent** | Behaves differently on a faster machine. Always a bug. |
| **Game feel** | How a control scheme feels to a hand, as opposed to what it does. |

---

## Recap

- **Acceleration changes velocity; velocity changes position.** In that order, every frame.
- Build the acceleration by **starting at zero and adding every push**. Then gravity, wind and thrust
  combine with no extra code.
- `vel *= 0.98` is **frame-rate dependent** even though no `dt` looks missing. Use
  `Math.exp(-DRAG * dt)`.
- Clamp the **length** of the velocity, never x and y separately.
- Drag multiplies and never quite stops; friction subtracts and does stop — and needs a guard, or it
  reverses.
- Your four numbers are not independent: `THRUST / DRAG` is the speed the ship will actually settle at.

---

## Stretch goals

1. **Tune by half-life.** Replace the drag slider with one labelled "time to lose half your speed",
   in seconds, and work `DRAG` out from it. Decide for yourself whether it is easier to tune.
2. **A dash.** Tapping shift adds a large one-off push along the nose. Then add a cooldown. Then make
   the ship briefly *immune to drag* during the dash and see how much better it feels.
3. **Wind.** One extra line in the acceleration step. Then make it vary across the screen, so the
   right-hand side is a gale.
4. **Separate grip.** Build question 3: split the velocity into the part along the ship and the part
   across it, and drag them by different amounts. This is the single biggest change to feel you can
   make with four lines.
5. **Prove the maths.** Hold thrust until the ship settles, and check the speed really is
   `THRUST / DRAG`. Report the measured number next to the predicted one.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** `01-set-vs-accelerate.html` on the projector. Fly ship A, fly ship B, and ask which is better. Do not settle it — the disagreement is the lesson. |
| 10–25 | **Concept.** The acceleration visualizer, mostly on *overshoot* and on friction = 0. Then the chain of two additions on the board, as vectors. |
| 25–40 | **Live-code** the six-step update. Write it in the wrong order on purpose once, and ask them to spot it. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D: the ship, then the tuning panel. |
| 120–140 | **Tuning gallery.** Everyone flies their neighbour's ship and the class votes. This is worth protecting — it is the only part of the course where the answer is a matter of taste and they get to find that out. |
| 140–150 | Recap. Lesson 4 adds pictures to this ship. |

**Before the lesson:** fly all four presets yourself and have an opinion ready. Students will ask
which is "right" and the honest answer — "that depends on the game, and here is what each one is good
for" — needs you to have felt them.

**What usually goes wrong**

1. **The ship accelerates for ever and leaves the screen.** No drag, or drag applied to the wrong
   variable. Ask them to print the speed.
2. **`vel *= 0.98` and nobody notices it is a bug**, because it works on their machine. Make them run
   `02-friction-and-frame-rate.html`. Seeing three ships at three frame rates end up in three
   different places is the only thing that makes this land.
3. **Diagonal is faster, again.** They clamped `vel.x` and `vel.y` separately. This is lesson 2's bug
   returning, and it returns for the same reason: x and y treated as two decisions.
4. **The ship drifts slowly backwards.** Subtractive friction with no zero test. The overshoot is tiny
   so it looks like a mystery drift rather than an arithmetic error.
5. **Units confusion.** `THRUST` of 5 does nothing visible; `THRUST` of 50000 is uncontrollable.
   Insist on units in the comment: px/s **per second**. Students who write the units down stop having
   this problem.
6. **"My max speed slider does nothing."** `THRUST / DRAG` is below the limit, so the clamp never
   fires. This is a genuinely good moment: the maths in the notes predicts it exactly, and predicting
   a bug before finding it is a new experience for most of them.
7. **Turning feels wrong at speed.** It is correct, and it is momentum. Some students will insist it is
   broken. Let them raise `DRAG` until it feels responsive and then notice they have removed the thing
   they liked.

**If you are running short on time** — cut subtractive friction and `code/04` entirely; drag alone is
enough for a ship, and lesson 12 can introduce ground friction where it is needed. Do **not** cut the
frame-rate demo: it is the only part of this lesson that is a correctness issue rather than a taste
issue.

**For the student who finishes at minute 90** — stretch goal 4 (separate grip along and across the
ship) is the best in the level. It is four lines, it uses the dot product from lesson 2 for something
they can feel, and the result is dramatically better than what the rest of the class has.

**The point to land at the end:** they changed four numbers and the same code became a spaceship, a
car and a sheet of ice. The code is not what makes a game feel good. The numbers are, and choosing them
is a skill with no right answer — which is why it is worth practising.
