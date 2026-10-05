# Lesson 9 — Particles And Juice Engineering

> **Web Games · Intermediate level · Lesson 9 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A **juice toolkit**: particles, screen shake, hitstop, flashes, squash and stretch, floating damage
numbers, and tweens. Then you will put them all into one small game with a switch for each, so you can
turn the whole lot off and on in front of somebody.

You will also answer the question lesson 2 left open — *does making thousands of objects per second
actually matter?* — by **measuring it** rather than guessing.

```
        juice off                         juice on
   ┌──────────────────┐            ┌──────────────────┐
   │                  │            │   ·  ✦  ·        │
   │       ▪  ●       │            │ ·  ▪↯ ✦ ●  ·     │   ← particles, flash,
   │                  │            │   ·     ·  "12"  │     shake, a number
   └──────────────────┘            └──────────────────┘
      same rules                      same rules
```

Nothing about the *rules* changes today. Everything about how the game **feels** does.

## Where this fits

- **Back:** [lesson 3](../lesson-03-acceleration-friction-and-drag/notes.md) was feel in the controls;
  [lesson 8](../lesson-08-sound-design-with-web-audio/notes.md) was feel in the ears. Today is feel in
  the eyes.
- **Forward:** the [capstone](../lesson-12-capstone-a-platformer/notes.md) uses all of it, and the
  advanced level pushes it further with input buffering and camera dynamics.
- **Other tracks:** Python's intermediate lesson 11 and C++'s intermediate lesson 12 do the same, and
  C++'s advanced lesson 2 is where pooling becomes a necessity rather than a nicety.

---

## The idea, in plain words

### What "juice" actually means

A game where you press a button and a number changes is *correct*. A game where you press a button and
the world **reacts** is satisfying. The difference is almost never in the rules — it is in the feedback,
and the feedback is cheap.

The useful way to think about it: **every action the player takes should be acknowledged by at least
three things.** Hitting an enemy might be

- the enemy flashing white for 60 ms,
- a handful of particles flying off,
- a short screen shake,
- the enemy squashing and recovering,
- a sound,
- a number floating upwards,
- and the game freezing for 50 ms at the moment of contact.

Each of those is a few lines. Together they are the difference between a prototype and a game. And
there is a timing rule underneath all of it: **feedback must arrive within about 100 milliseconds**, or
the player stops connecting it to what they did. 100 ms is six frames. That is the budget.

### Particles are one object and three lines

A particle is not a special kind of thing. It is a position, a velocity, and a countdown:

```js
function spawnParticle(x, y) {
  const angle = Math.random() * Math.PI * 2;      // any direction
  const speed = 60 + Math.random() * 180;
  return {
    x: x, y: y,
    vx: Math.cos(angle) * speed,                  // lesson 2's fromAngle
    vy: Math.sin(angle) * speed,
    life: 0.5 + Math.random() * 0.4,              // seconds remaining
    maxLife: 0,                                   // filled in below
    size: 2 + Math.random() * 3
  };
}
```

```js
// update: lesson 3's physics, with a countdown bolted on
p.vy += GRAVITY * dt;
p.x += p.vx * dt;
p.y += p.vy * dt;
p.life -= dt;
```

```js
// draw: fade and shrink as life runs out. THIS is what makes it look like smoke
// rather than like a list of squares.
const t = p.life / p.maxLife;        // 1 at birth, 0 at death
ctx.globalAlpha = t;
ctx.fillRect(p.x, p.y, p.size * t, p.size * t);
```

That `t` going from 1 to 0 is the whole visual trick, and it is the same `t` as the easing lesson.
Everything you can multiply by it — alpha, size, speed, colour — makes the effect better.

**Removing dead particles: backwards.** You met this in the beginner level and it comes back every time:

```js
for (let i = particles.length - 1; i >= 0; i--) {
  if (particles[i].life <= 0) { particles.splice(i, 1); }
}
```

### Different effects are different *numbers*, not different code

One emitter, four effects:

| Effect | direction | speed | gravity | life | colour |
|---|---|---|---|---|---|
| **explosion** | all round | high | low | short | yellow → red |
| **dust** | upwards-ish | low | low | medium | grey, big, faint |
| **blood / sparks** | away from impact | high | high | short | one colour |
| **smoke** | up | very low | negative | long | grey, growing |

Negative gravity for smoke is worth noticing: nothing in the code knows what smoke is. It is dust that
falls upwards.

### Object pooling, and the answer to lesson 2's question

Lesson 2 ended with a question: a hundred chasers making three `Vec2`s each per frame is 18,000 objects
a second. Does that matter?

Here is the honest answer, and it has two halves.

**Half one: usually not.** Modern JavaScript engines allocate small objects extremely quickly. For
hundreds of particles you will never notice.

**Half two: it matters when it matters, and then it matters suddenly.** Objects you throw away have to
be collected later, and garbage collection happens *when the engine decides*, not when it is convenient.
The symptom is not a slow game — it is a game that runs at a steady 60 fps and then **drops one frame
every couple of seconds**. That stutter is far more noticeable than a game that is uniformly slower, and
it is why professionals care.

A **pool** fixes it by never throwing anything away:

```js
/* Make them all once. Then "spawning" means finding a dead one and refilling it,
   and "dying" means setting a flag. No object is ever created or discarded. */
const pool = [];
for (let i = 0; i < MAX_PARTICLES; i++) {
  pool.push({ x: 0, y: 0, vx: 0, vy: 0, life: 0, size: 0, alive: false });
}

function spawn(x, y) {
  for (let i = 0; i < pool.length; i++) {
    if (!pool[i].alive) {
      const p = pool[i];
      p.x = x; p.y = y; p.alive = true;  /* ...and the rest */
      return p;
    }
  }
  return null;        // the pool is full. Dropping a particle is fine.
}
```

Two things to notice:

- **The array never changes length.** No `push`, no `splice`, no allocation, nothing to collect.
- **A full pool drops the request.** That is a feature: it puts a hard ceiling on the work per frame, so
  a hundred explosions at once cannot bring the game down.

The scan for a dead one looks wasteful. `code/02-pooling-measured.html` measures both versions with
`performance.now()`, at particle counts from 100 to 50,000, and prints real numbers. **Do the measuring
before you form an opinion** — that is the actual lesson, and it applies to every optimisation you will
ever consider.

### Screen shake, done right

```js
// shake is a NUMBER: how much is left. Set it on impact, decay it every frame.
function addShake(amount) {
  shake = Math.min(MAX_SHAKE, shake + amount);      // cap it
}

function updateShake(dt) {
  shake *= Math.exp(-SHAKE_DECAY * dt);             // lesson 3's drag
  if (shake < 0.1) { shake = 0; }
}

// at draw time, as an OFFSET - never by moving the camera itself
const ox = (Math.random() * 2 - 1) * shake;
const oy = (Math.random() * 2 - 1) * shake;
ctx.save();
ctx.translate(Math.round(ox), Math.round(oy));
drawWorld();
ctx.restore();
```

Four things people get wrong, and all four are visible in `code/03`:

1. **Adding to `camera.x` instead of using an offset.** The camera's follow code then fights the shake
   and the view drifts.
2. **No decay.** The screen shakes for ever.
3. **No cap.** Ten explosions at once and the screen is unreadable.
4. **Too much.** This is the big one. A shake you *notice* is nearly always too strong. 3–8 pixels for a
   hit; 15 for something enormous. Most first attempts use 40 and make people feel ill.

### Hitstop: the most effective four lines in this lesson

At the moment of a big impact, **stop the whole game for 50–80 milliseconds**.

```js
if (hitstop > 0) {
  hitstop -= realDt;
  dt = 0;                 // the world does not advance. Particles may still move.
}
```

It sounds like a bug. It is used in essentially every fighting game, action game and good platformer
ever made, because it tells the player's hands that the hit *connected*. Three frames of nothing is
enormous feedback for almost no code.

The judgement is in the length: under about 30 ms it is invisible, over about 120 ms it feels like
lag. Put it on a slider and find your own number.

### Squash and stretch

Borrowed directly from hand-drawn animation. A thing that lands squashes; a thing that accelerates
stretches along the way it is going.

```js
// scale the sprite by two numbers that multiply to roughly 1, so the volume looks kept
const squash = 1 + landImpact * 0.4;       // wider
const stretch = 1 - landImpact * 0.4;      // and shorter
ctx.scale(squash, stretch);
```

Then let `landImpact` decay to 0 over about 150 ms. Two lines, and a falling block starts to look like
it has weight.

### Tweens, so these do not become a mess

Every one of these effects is the same shape: *a number moves from A to B over a length of time, then
something happens*. Writing that out by hand eight times produces eight timers scattered through your
update function.

```js
/* One list of little jobs, updated in one place. A tween is: a target object, a
   field, a start, an end, a duration, and a shape. */
const tweens = [];

function tween(target, field, to, duration, ease) {
  tweens.push({
    target: target, field: field,
    from: target[field], to: to,
    t: 0, duration: duration,
    ease: ease || function (x) { return 1 - (1 - x) * (1 - x); }   // easeOutQuad
  });
}

function updateTweens(dt) {
  for (let i = tweens.length - 1; i >= 0; i--) {
    const w = tweens[i];
    w.t += dt;
    const k = Math.min(1, w.t / w.duration);
    w.target[w.field] = w.from + (w.to - w.from) * w.ease(k);
    if (k >= 1) { tweens.splice(i, 1); }
  }
}
```

Now a flash is `tween(enemy, "flash", 0, 0.12)`, a menu slide is
`tween(menu, "y", 100, 0.3)`, and a difficulty ramp is `tween(game, "speed", 400, 20)`. This is the
general answer to lesson 3's ice power-up question and lesson 7's fade — one small system, used
everywhere.

---

## The idea, in pictures

Open [tweens and easing](../../../shared/visualizers/easing.html).

**What to look for:** five dots leave together and arrive together. Only the *shape* of the journey
differs, and that shape is what people mean by game feel. Watch `easeOutQuad` — fast then settling — and
notice it is the one that looks "right" for almost everything: a flash fading, a menu arriving, a camera
catching up. Then look at `easeOutBack`, which overshoots and comes back; that is the curve for something
appearing with confidence.

Then open [acceleration, friction and drag](../../../shared/visualizers/acceleration-and-friction.html)
again and look at the velocity arrow. A particle is that, times two hundred.

---

## The idea, in code

1. `code/01-particles.html` — one emitter, four presets, every number on a slider. Make smoke by setting
   gravity negative.
2. `code/02-pooling-measured.html` — allocate-every-frame against a pool, with real timings and a frame-time
   graph where the stutter is visible. Decide for yourself what the numbers mean.
3. `code/03-shake-and-hitstop.html` — screen shake with each of the four mistakes on a switch, plus
   hitstop, flash and squash.
4. `code/04-juice-it.html` — one small game, eight juice switches. Turn them all off, play it, then turn
   them on one at a time.

---

## The maths you just used

**1. Normalised life.** `t = life / maxLife` goes from 1 to 0 as the particle dies. Multiply anything by
it and that thing fades out in step. This is the same `t` as easing, running backwards.

**2. A random direction.** `angle = Math.random() * Math.PI * 2`, then `cos` and `sin`. Picking random
`vx` and `vy` separately does *not* give an even spread — it clusters along the diagonals, because
getting a large value in both at once is more likely than getting a large one in just one. Spawn 300 and
look: the difference is obvious.

**3. Exponential decay, again.** Shake, flash, squash and hitstop all decay the same way as lesson 3's
drag: `value *= Math.exp(-RATE * dt)`. Fourth time this term, and each time it was the frame-rate-safe
version of "a bit less each frame".

**4. Measuring, properly.** One sample of `performance.now()` tells you almost nothing — a frame might be
slow because the operating system decided to do something else. The honest method is:

```js
const t0 = performance.now();
doTheThing();
const ms = performance.now() - t0;
samples.push(ms);          // keep the last 120
// then report the AVERAGE and the WORST, not one reading
```

Report both. The average tells you the cost; the **worst** tells you whether the player will feel it, and
for garbage collection the worst is the whole story.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the `* t` from the particle's alpha and size | | |
| Spawn particles with random `vx` and `vy` instead of a random angle | | |
| Set shake decay to 0 | | |
| Add the shake to `camera.x` instead of using a translate | | |
| Set the shake amount to 50 | | |
| Set hitstop to 400 ms | | |
| Remove the cap on the particle pool and hold the spawn key | | |
| Remove `globalAlpha = 1` after drawing particles | | |
| Make `splice` run forwards through the particle list | | |

The last-but-one is a lovely bug: everything drawn after the particles is faintly transparent, including
the score, and nothing in that code mentions the score at all.

---

## Think like an engineer

1. Hitstop freezes the game. But the particles from the hit should probably keep moving, and the UI
   definitely should. So "freeze the game" is not quite right. What *exactly* should freeze? Write the
   rule.
2. You measured pooling in `code/02`. At what particle count did it start to matter on *your* machine?
   What does that tell you about when to pool and when not to bother? Would your answer change on a
   five-year-old school laptop?
3. **Design something.** A hit that feels progressively bigger: a light hit, a medium hit, a killing
   blow. You have shake, particles, hitstop, flash, squash, sound and damage numbers. Do you scale all of
   them together, or do some only appear for the big one? Be specific about numbers.
4. **The hard one.** Juice can lie. A shake and a flash tell the player "something important happened" —
   so if you use them for everything, you have told them nothing, and if you use them for a hit that did
   no damage, you have actively misled them. Where is the line? Give one example of juice that would be
   dishonest.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Juice** | Feedback that is not required for the rules but changes how a game feels. |
| **Particle** | A position, a velocity, and a countdown. Nothing more. |
| **Emitter** | The thing that spawns particles, with a set of numbers describing them. |
| **Object pool** | A fixed set of reusable objects, so nothing is ever allocated or collected. |
| **Garbage collection** | The engine reclaiming discarded objects, at a moment of its choosing. |
| **Hitstop** | Freezing the game for 50–80 ms on impact, so the hit registers. |
| **Screen shake** | A decaying random offset applied at draw time. Never a change to the camera. |
| **Squash and stretch** | Deforming a sprite to suggest weight. From hand-drawn animation. |
| **Tween** | A number moving from A to B over a duration, with a shape. |
| **The 100 ms rule** | Feedback arriving later than about 100 ms stops feeling connected to the action. |

---

## Recap

- Juice is not in the rules. **Every action deserves three kinds of acknowledgement**, and all of them
  must land within about 100 ms.
- A particle is a position, a velocity and a countdown. Multiply everything by `life / maxLife`.
- Different effects are **different numbers in the same emitter** — smoke is dust with negative gravity.
- **Pool when you have measured a reason to.** The symptom pooling fixes is one dropped frame every few
  seconds, not a uniformly slow game.
- Screen shake is a **decaying, capped offset applied at draw time**, and it should be smaller than you
  think.
- **Hitstop** is the best value for money here: four lines, 50–80 ms, enormous effect.
- A **tween system** stops eight effects becoming eight scattered timers.
- Remove things from lists **backwards**.

---

## Stretch goals

1. **Trails.** Keep the last ten positions of a fast-moving object and draw them fading. Three lines, and
   it changes how fast the thing feels.
2. **Colour over life.** Interpolate each particle's colour from yellow to red to grey as it dies. The
   single biggest improvement to an explosion.
3. **A tween with a callback.** Add an `onDone` to your tween system, and use it to chain three effects.
   You have just built the engine of every menu animation.
4. **Impact direction.** Make the particles from a hit fly away from the *direction the hit came from*,
   not in all directions. Your `Vec2` already has what you need, and it looks far better.
5. **Measure your own game.** Add a frame-time graph with the average and worst over the last two
   seconds, and keep it in your game for the rest of the course.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Open `04-juice-it.html` with everything **off**. Play it on the projector; it is dull. Then turn the switches on one at a time, slowly, while they watch. The reaction to hitstop in particular is worth the whole lesson. |
| 10–25 | **Concept.** The easing visualizer, then the particle anatomy on the board: position, velocity, countdown, and `t = life / maxLife`. |
| 25–40 | **Live-code** one emitter from nothing. Twenty lines, and it already looks good. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–4 are the core; 5 and 6 are the ones they will enjoy most. |
| 120–140 | **Juice gallery.** Everyone turns their effects on in front of the class. This is the most enjoyable twenty minutes of the level and worth protecting. |
| 140–150 | Recap. Lesson 10 makes enemies that seem to think. |

**What usually goes wrong**

1. **Too much of everything.** Shake at 40, 500 particles per hit, 300 ms hitstop. This is universal and
   it is a teaching opportunity rather than a mistake: let them build it, let them play it, then ask them
   to halve every number and play it again. Almost everybody prefers the halved version and is surprised.
2. **`globalAlpha` left set.** Everything drawn afterwards is transparent. Teach `save`/`restore` around
   anything that changes canvas state, as a habit.
3. **Particles never disappear.** The `life` countdown is missing, or the removal loop runs forwards.
4. **The screen drifts** after shaking. They added to `camera.x`.
5. **Hitstop freezes everything including the HUD**, so the game looks locked up. This is question 1.
6. **`dt` set to 0 for hitstop, and something divides by `dt`.** Rare and confusing; a good reason to
   never divide by `dt`.
7. **Pooling applied with no measurement**, usually because it sounds professional. Push back: what did
   you measure, and what did it say? The habit is worth more than the optimisation.

**If you are running short on time** — cut pooling and `code/02` entirely, and mention it as something to
come back to. Cut the tween system too; individual timers are fine for one lesson. Do **not** cut hitstop
or the 100 ms rule.

**For the student who finishes at minute 90** — stretch goal 2 (colour over life) takes five minutes and
improves their explosions more than anything else. Then stretch goal 4 (impact direction), which uses
lesson 2's vectors for something immediately visible.

**The point to land at the end:** they did not change a single rule today. The game is exactly as
difficult, exactly as fair, and plays exactly the same. It is simply much better — and that gap, between
correct and satisfying, is where most of the craft of game development lives.
