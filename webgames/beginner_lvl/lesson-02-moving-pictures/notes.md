# Lesson 2 — Moving Pictures

> **Web Games · Beginner level · Lesson 2 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A ball that bounces around inside the canvas, hitting all four walls — and which moves at
**exactly the same speed on every computer in the room**. That second part is the real lesson, and
it is the difference between a toy and a game.

```
┌──────────────────────────────────────┐
│                      ●               │
│                    ↗                 │
│                                      │
│         ↘                            │
│           ●                          │
└──────────────────────────────────────┘
```

## Where this fits

- **Back:** [lesson 1](../lesson-01-what-is-a-game/notes.md) gave you the loop. Your square moved
  `2` pixels every frame.
- **Forward:** [lesson 3](../lesson-03-player-in-control/notes.md) puts you in control of
  something.
- **Today we fix a bug you did not know you had.** That `2` was wrong, and in a way that only shows
  up on someone else's laptop.

---

## The idea, in plain words

### Part 1: the screen is a grid, and it is upside down

Every point on the canvas has two numbers: how far **across**, and how far **down**.

In maths class, you learned that the y axis points *up* and that `(0, 0)` sits in the middle. On a
screen, neither of those is true:

- `(0, 0)` is the **top-left corner**.
- `x` grows to the **right**, as you would expect.
- `y` grows **downwards**. This is the one that catches everybody.

So to move something **up**, you **subtract** from y:

```js
ball.y = ball.y - 5;     // moves UP the screen
ball.y = ball.y + 5;     // moves DOWN the screen
```

> **Why on earth is it like this?** It is a leftover from old televisions. A cathode-ray tube drew
> the picture with a beam that swept across the top row first, then the next row down, and so on to
> the bottom. "Row 0" meant the first row drawn, which was the top one. Every graphics system since
> has kept that numbering — the web canvas, Python's tkinter, SDL, raylib, your phone. One famous
> exception is Python's `turtle`, which uses maths-class coordinates on purpose because it was built
> for teaching. You will meet both in this course.

### Part 2: velocity is just "how much to add"

Last lesson you wrote `squareX = squareX + 2`. That `2` has a name: **velocity**.

Velocity is not quite the same as speed. Speed is *how fast*. Velocity is *how fast **and which
way***, and the direction is carried in the sign:

| Velocity | Means |
|---|---|
| `speedX = 5` | moving right |
| `speedX = -5` | moving left |
| `speedY = 5` | moving **down** (remember: y grows downwards) |
| `speedY = -5` | moving **up** |

Which makes bouncing almost embarrassingly simple. To bounce off a wall, **flip the sign**:

```js
if (ball.x > canvasWidth) {
  ball.speedX = -ball.speedX;      // was going right, now goes left
}
```

That is the entire physics of Pong, and you now know it.

### Part 3: the bug in lesson 1

Here is the problem, and it is a serious one.

`squareX = squareX + 2` means *"move 2 pixels **every frame**"*. How many frames happen per second?
That depends on the computer.

| The computer | Frames per second | Your square's actual speed |
|---|---|---|
| A normal laptop | 60 | 120 pixels per second |
| A gaming monitor | 144 | **288 pixels per second** |
| An old school machine, struggling | 30 | **60 pixels per second** |

Same code. Same `2`. Three completely different games.

On a gaming monitor your game runs at more than double speed and is unplayable. On a tired old
laptop it crawls. And here is the cruel part: **it will look perfect on your machine**, because you
wrote the `2` by tweaking it until it felt right *on your machine*.

This is not a small or theoretical problem. Several famous commercial games shipped with it. There
are speedruns of *Dark Souls 2* that rely on weapon durability draining at double rate at high frame
rates, because the code counted frames rather than seconds.

### Part 4: the fix is to measure time, not frames

Stop saying "move 2 pixels per frame". Start saying **"move 120 pixels per second"**.

To do that, you need to know how long the last frame took. That number is called **delta time**,
almost always shortened to `dt`. "Delta" is the mathematician's word for "the change in".

```js
ball.x = ball.x + 120 * dt;
```

- On a 60 fps machine, `dt` is about `0.0167` seconds, so the ball moves `120 × 0.0167 ≈ 2` pixels.
- On a 144 fps machine, `dt` is about `0.0069`, so it moves `0.83` pixels — but it does so more
  often.
- On a 30 fps machine, `dt` is about `0.0333`, so it moves `4` pixels — fewer, bigger steps.

**In every case it covers 120 pixels in one second.** Slower computers take bigger steps; faster
ones take smaller steps; everyone ends up in the same place at the same time.

---

## The idea, in pictures

### First, the coordinate system

Open [the coordinates explainer](../../../shared/visualizers/coordinates.html).

**What to look for:** drag the orange dot and watch both readouts. Move it *upwards* and the
screen's `y` gets **smaller** while the maths `y` gets bigger. Then watch the ball on the right,
which is told `y = y - 90 * dt` and rises because of it.

### Then, the frame-rate problem

Open [the delta-time explainer](../../../shared/visualizers/delta-time.html).

**What to look for:**

1. Leave the frame rate at **60** and press Play. Both balls cross together. Everything looks fine.
2. Press Reset, drag the slider to **20**, and press Play again. The top ball crawls.
3. **Nobody changed its speed setting.** Only the computer changed.
4. Drag the slider to **120** and watch the top ball overshoot wildly.

The bottom ball never cares, because it asks how much *time* passed instead of counting frames.

---

## The idea, in code

### Step 1: getting `dt`

The browser hands `requestAnimationFrame` a timestamp — the number of milliseconds since the page
loaded. Subtract the previous one from the current one and you have how long the frame took.

```js
let lastTime = 0;          // the timestamp of the previous frame

function frame(currentTime) {
  // currentTime comes from the browser, in MILLISECONDS.
  // Divide by 1000 to get seconds, which is a friendlier unit to think in.
  let dt = (currentTime - lastTime) / 1000;
  lastTime = currentTime;

  update(dt);              // pass dt along to whoever needs it
  render();
  requestAnimationFrame(frame);
}

requestAnimationFrame(frame);     // note: no longer frame() directly
```

### Step 2: the first-frame trap

There is a bug hiding in the code above, and it will bite you.

On the **very first** frame, `lastTime` is still `0`, but `currentTime` might be `2500` — the page
took two and a half seconds to load. So `dt` comes out as `2.5` **seconds**, and your ball
teleports 300 pixels before you have seen a single frame.

The same thing happens if someone switches to another tab for a minute and comes back.

So: throw away absurd values.

```js
let dt = (currentTime - lastTime) / 1000;
lastTime = currentTime;

// If a frame took longer than a tenth of a second, something unusual
// happened: the page just loaded, or the tab was in the background.
// Pretend it was a normal frame rather than letting everything teleport.
if (dt > 0.1) { dt = 1 / 60; }
```

This is called **clamping**, and essentially every real game does it.

### Step 3: bouncing off the walls

```js
const ball = {
  x: 300,
  y: 200,
  radius: 15,
  speedX: 220,      // pixels per SECOND
  speedY: 160
};

function update(dt) {
  // Move first.
  ball.x = ball.x + ball.speedX * dt;
  ball.y = ball.y + ball.speedY * dt;

  // Then check the walls. Note we test the EDGE of the ball, not its centre -
  // the centre is still 15 pixels from the wall when the ball first touches it.
  if (ball.x + ball.radius > canvas.width) {
    ball.x = canvas.width - ball.radius;   // push it back inside
    ball.speedX = -ball.speedX;            // and turn it around
  }
  if (ball.x - ball.radius < 0) {
    ball.x = ball.radius;
    ball.speedX = -ball.speedX;
  }
  // ...and the same two for the top and bottom, using y and speedY.
}
```

### Why the "push it back inside" line matters

Leave out `ball.x = canvas.width - ball.radius` and you get one of the classic beginner bugs: the
ball **sticks to the wall and vibrates**.

Here is why. The ball goes slightly past the wall. You flip the speed. Next frame it moves inward —
but perhaps not far enough to get fully clear. So it is *still* past the wall, so you flip the speed
again, which sends it back into the wall. Flip, flip, flip, forever. The ball jitters along the edge
looking possessed.

Moving it to a legal position *before* flipping breaks that cycle. The rule is worth remembering:

> **When you detect a collision, fix the position first, then change the velocity.**

---

## The maths you just used

### Distance = speed × time

This is the formula from science class, and nothing more:

> **distance = speed × time**

A frame is a very short amount of time. If the last frame lasted `dt` seconds and you are travelling
at `speed` pixels per second, then in that frame you moved `speed × dt` pixels. That is all
`ball.x += ball.speedX * dt` says.

### Where the "2" came from

At 60 fps, one frame lasts `1 ÷ 60 = 0.0167` seconds. So:

```
120 pixels/second × 0.0167 seconds ≈ 2 pixels
```

The `2` in lesson 1 was never wrong, exactly. It was *120 pixels per second measured on a 60 fps
machine, with the measurement baked in and then forgotten*. Delta time is just the habit of not
baking it in.

### Negative numbers have a job

You may have wondered what negative numbers were ever for. Here: the sign of a velocity **is** its
direction. `speedX = -220` is not a weird or broken value, it is "220 pixels per second, leftwards".
And `speed = -speed` — a thing that would be nonsense in a maths exercise — is exactly how a bounce
works.

---

## Break it on purpose

Use `code/03-bouncing-ball.html`. Predict first, then run.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| `speedX: 220` → `speedX: 1200` | | |
| Delete the `ball.x = canvas.width - ball.radius;` line | | |
| Change `if (dt > 0.1)` to `if (dt > 100)`, then reload a few times | | |
| Use `ball.x > canvas.width` instead of `ball.x + ball.radius > canvas.width` | | |
| Remove `* dt` from both movement lines | | |
| Set `speedY: 0` | | |

The second one gives you the vibrating-ball bug on demand. The third one is how you reproduce the
first-frame teleport. The fourth one makes the ball sink halfway into each wall before bouncing.

---

## Think like an engineer

Delta time fixes movement. But movement is not the only thing in a game that can accidentally be
measured in frames.

Consider these three:

1. An enemy that fires **every 30 frames**.
2. An explosion animation that advances **one picture per frame**.
3. A countdown that does `secondsLeft = secondsLeft - 1` **each frame**.

**Your questions:**

- For each one, describe exactly what a player on a 144 fps gaming monitor would experience.
- Write the fixed version of each.
- Now the harder question: is there **any** case where counting frames really is the right choice?
  Think about a fighting game where moves are described as "7 frames of startup", and where
  tournament players genuinely count frames. What is different about that situation?
- Hardest: delta time makes the game fair across machines, but it makes it **non-deterministic** —
  run the same game twice with the same inputs and you get slightly different results, because the
  frame times differ. Why might that be a serious problem for an online multiplayer game, or for a
  replay feature?

That last question is what lesson 1 of the advanced level is about. See if you can work out the shape
of the answer before you get there.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Velocity** | Speed *with a direction*. The sign carries the direction. |
| **Delta time** (`dt`) | How many seconds the previous frame took. |
| **Frame-rate dependent** | A bug where the game behaves differently on faster or slower computers. |
| **Clamping** | Forcing a number to stay within sensible limits. |
| **Radius** | Distance from the centre of a circle to its edge. Half the width. |
| **Origin** | The point where x and y are both zero. On a canvas, the top-left corner. |

---

## Recap

- `(0, 0)` is the top-left, and **y grows downwards**, so "up" means subtracting.
- **Velocity** is how much to add each step; its sign is its direction.
- Bouncing is `speed = -speed`. Fix the position **first**, then flip.
- Counting frames is a bug. Measure **seconds** and multiply by `dt`.
- Clamp `dt`, or the first frame (and every tab switch) will teleport everything.

---

## Stretch goals

1. **Gravity.** Add `ball.speedY = ball.speedY + 600 * dt;` at the top of `update`. The ball now
   falls and bounces. Then make it lose energy on each bounce with `ball.speedY *= -0.8` instead of
   `*= -1`. What value makes it settle most convincingly?
2. **Many balls.** Make ten balls, each with its own position and speed. If you find yourself
   writing `ball1`, `ball2`, `ball3`… stop: that is the moment an **array** becomes worth learning.
3. **Trail.** Keep the last 20 positions in an array and draw them as fading circles.
4. **Measure your own frame rate.** Draw `Math.round(1 / dt)` on screen. Resize the window, open a
   dozen tabs, drag the page around. What makes the number move?
5. **Prove it works.** Add a slider that artificially drops the frame rate by doing nothing in a busy
   loop. Show that the ball still crosses the screen in the same number of seconds.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run lesson 1's square on two machines side by side — ideally one with a high-refresh display. If you have no second machine, use the delta-time visualizer at 20 fps and 120 fps. Say nothing yet; let them notice. |
| 10–25 | **Concept.** Coordinates visualizer first (5 min), then the delta-time one (10 min). Step before you play. |
| 25–40 | **Live-code** the `dt` calculation and the first wall bounce together. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D: the bouncing ball. |
| 120–140 | Break-it-on-purpose, especially the vibrating-ball bug. Share-outs. |
| 140–150 | Recap. Flag that lesson 3 finally makes it interactive. |

**What usually goes wrong**

1. **The ball flies off instantly on load.** They have not clamped `dt`, so the first frame is worth
   several seconds. This is the single most common bug in this lesson. The fix is three lines, but
   let them hit it first — the diagnosis is the lesson.
2. **The ball vibrates along a wall.** They flipped the speed without correcting the position. Draw
   the frame-by-frame sequence on the board; it is far clearer than explaining it in words.
3. **The ball sinks halfway into the wall.** They are comparing the centre rather than the edge.
   Ask: "where exactly is `ball.x`?"
4. **They write `frame()` instead of `requestAnimationFrame(frame)` for the first call**, so
   `currentTime` is `undefined`, `dt` becomes `NaN`, and the ball vanishes. `NaN` spreading through
   arithmetic is worth five minutes of class time on its own — it is a bug pattern they will meet for
   the rest of their lives.
5. Someone will ask why we do not just lock the game to 60 fps. Good question, no cheap answer:
   you cannot reliably, the browser will not let you, and the advanced level's fixed-timestep lesson
   is the real response. Say that.

**If you are running short on time** — give them the `dt` calculation as a snippet to paste rather
than live-coding it, and cut bouncing to two walls instead of four. Do not cut the clamping; it is
the bit they will need in every subsequent lesson.

**For the student who finishes at minute 90** — stretch goal 1 (gravity) is the natural next step and
feeds straight into lesson 5. Stretch goal 2 is the better one though: pushing them to write ten
balls with ten sets of variables until it becomes unbearable is the best possible motivation for
arrays, which arrive in lesson 6.

**Worth saying out loud:** that `if (dt > 0.1)` line looks like a hack and it is. Real engines do
exactly this. Students often think professional code is free of patches like this; showing them one
on day two is honest and useful.
