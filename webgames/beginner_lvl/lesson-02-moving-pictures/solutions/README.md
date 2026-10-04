# Lesson 2 — Solutions and marking notes

---

## Section A

**A1.** [2] `y` gets bigger **downwards**. To move up: `y = y - speed` (or `y -= speed`). One mark
each.

**A2.** [2] Delta time. It measures how many **seconds the previous frame took**. Take a mark off
only if they say "frames" rather than seconds — the unit is the whole point.

**A3.** [2] Speed is how fast. Velocity is how fast **and in which direction**, with the direction
carried by the sign.

**A4.** [3] `300 × 0.02 = 6` pixels. One mark for using distance = speed × time, two for the answer.

**A5.** [3] One mark for "otherwise a single enormous frame moves everything a huge distance". Two
marks for two situations: (a) the very first frame, where `lastTime` is 0 so `dt` is the whole
page-load time; (b) the tab being in the background or the laptop sleeping, so no frames run for
seconds or minutes. Also accept: the browser throttling a hidden tab, or a very slow asset load.

---

## Section B

**B1.** [3] At 60 fps it does 4 × 60 = 240 px/sec, and 600 ÷ 240 = 2.5 s. ✓
At 144 fps it does 4 × 144 = 576 px/sec, so 600 ÷ 576 ≈ **1.04 seconds**.
It runs about **2.4× faster**. One mark for the method, one for the number, one for noticing the
game is now unplayable rather than just "a bit quick".

**B2.** [3] `100 + (−90 × 1) = 10`. It is at `y = 10`, which is **higher** on the screen — near the
top. Full marks need both the number and "higher", because that is where the confusion lives.

**B3.** [4] `lastTime` stays at 0, so `currentTime - lastTime` is the entire time since the page
loaded, and it grows every frame. So `dt` keeps increasing: 0.016, then 0.033, then 0.05… The ball
accelerates without limit and shoots off screen almost immediately. Good answers note that the ball
*appears* to accelerate even though no acceleration was written anywhere — a bug that looks like a
feature.

**B4.** [4] `requestAnimationFrame` passes a timestamp as the argument. Calling `frame()` by hand
passes nothing, so `currentTime` is `undefined`. Then `(undefined - 0) / 1000` is `NaN`. Then
`ball.x + ball.speedX * NaN` is `NaN`. The ball's position is now `NaN` forever, because any sum
involving `NaN` is `NaN`, and `ctx.arc` with `NaN` draws nothing.

`ball.x` after the first frame is **`NaN`**.

This question is worth real class time. `NaN` silently contaminating every calculation it touches,
with no error thrown, is a bug pattern students will meet for the rest of their lives.

---

## Section C

**C1.** [4] Two marks for the frame-by-frame account:

- **Frame 1:** the ball moves past the wall. The test is true, so `speedX` flips to negative. The
  ball is still outside the wall.
- **Frame 2:** the ball moves inward, but not far enough to get fully back inside. The test is true
  **again**, so `speedX` flips back to positive — pointing out of the wall.
- **Frame 3:** the ball moves further out. The test is true again. Flip again. And so on forever.

Two marks for the fix: set `ball.x = canvas.width - ball.radius;` **before** flipping, so the test is
false next frame.

The general rule is worth stating: *fix the position first, then change the velocity*.

**C2.** [3] It compares `ball.x`, which is the **centre**, against the wall. The ball has only
"arrived" at the wall when its *edge* gets there, which is one radius earlier. So the ball travels a
further `radius` pixels into the wall before the test fires. Fix:
`if (ball.x + ball.radius > canvas.width)` and `ball.x = canvas.width - ball.radius`.

**C3.** [4] Almost certainly `NaN`, from an unclamped or badly-initialised `dt` (see B4). Two marks.

The "no error message" part is the real question, and is worth two marks on its own: arithmetic with
`NaN` is perfectly legal JavaScript. It does not throw. `NaN` simply spreads through every
calculation, and canvas drawing commands given `NaN` quietly draw nothing at all. Teach them the
diagnostic: `console.log(ball.x)` and look for `NaN`.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 1.** Most classroom machines report 60. Anyone with a high-refresh laptop or external
monitor will see 120 or 144 — find that student and put their screen on the projector, because they
are living proof of the entire lesson.

**Checkpoint 4.** The two things to look for while circulating: are they testing the edge or the
centre, and are they fixing the position before flipping? Both bugs are visually obvious from across
the room — sinking into the wall, and vibrating against it.

**Checkpoint 5 — the deliberate subtlety.** The two balls *will* slowly drift apart, and students
should not conclude that delta time is broken. The reason is accumulated floating-point rounding:
each window gets a slightly different sequence of `dt` values, and tiny differences build up over
thousands of frames. This is **not** the frame-rate bug; the balls stay in step to within a pixel or
two over a short run, rather than one running at double the speed of the other. Strong students who
raise this are asking exactly the right question, and the honest answer is "yes, and the real fix is
the fixed timestep, which is the first lesson of the advanced level."

**Checkpoint 6.** Gravity must be applied to the *velocity*, before the velocity is applied to the
position. Students who add gravity straight to `ball.y` get a constant downward drift rather than
acceleration, and that is a useful mistake to discuss.

---

## Section E — marking notes, not answers

**E1.** [the fixes]

1. **Enemy firing every 30 frames.** At 144 fps it fires every 0.21 s instead of every 0.5 s —
   roughly **2.4× more often**, so the game is far harder on a better computer. Fix: keep a timer in
   seconds.
   ```js
   fireTimer = fireTimer - dt;
   if (fireTimer <= 0) { fire(); fireTimer = 0.5; }
   ```
2. **Explosion, one picture per frame.** The animation plays 2.4× too fast and is over before it
   registers. Fix: accumulate time and advance a frame every `1/12` of a second.
3. **Countdown, −1 per frame.** This is the worst of the three. It subtracts 144 per second instead
   of 60, so a "60 second" timer expires in under half a second. Fix: `secondsLeft -= dt;`.

Award marks for correctly describing *faster* in each case and for a fix that uses seconds.

**E2.** The key difference is that fighting games **lock the simulation to a fixed rate** — usually
60 ticks per second — regardless of how fast the display refreshes. Within that locked rate, "frame"
is a precise and reliable unit of time, so counting frames is exact rather than machine-dependent.
Strong answers notice that this is really the *fixed timestep* idea, and that the game is still not
counting *display* frames; it is counting simulation ticks that happen to be called frames.

Also accept: determinism matters more than smoothness in a competitive game, and a locked rate buys
that.

**E3.** This is the best question on the sheet and it is genuinely hard. Look for:

- **Multiplayer.** If each player's machine simulates with slightly different `dt` values, the two
  simulations drift apart. Player A sees the shot hit; player B sees it miss. The usual fixes are to
  run a fixed timestep so both machines compute identically, or to make one machine authoritative and
  have the other follow it.
- **Replays.** A replay is usually stored as a list of inputs, not a video, because that is tiny. It
  only works if replaying the same inputs reproduces the same game — which needs determinism.
  Non-deterministic physics means the replay gradually diverges and ends up showing something that
  never happened.

A student who gets anywhere near "the same inputs must give the same outputs" has understood it.
Tell them the name — **determinism** — and that lesson 1 of the advanced level is about exactly this.
