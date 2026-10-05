# Lesson 3 — Solutions and marking notes

---

## Section A

**A1.** [3] Change the **position** directly — instant, weightless, arcade. Change the **velocity** —
responsive, slightly robotic. Change the **acceleration** — heavy, physical, momentum. One mark each.

**A2.** [2] The multiplication happens once per **frame**, so the total over one second depends on how
many frames there are: `0.98⁶⁰ ≈ 0.30` but `0.98³⁰ ≈ 0.55`. One mark for "per frame, not per second",
one for a concrete consequence (the ship handles differently on a faster monitor).

**A3.** [3] Any two differences: drag multiplies / friction subtracts; drag takes a share / friction
takes a fixed amount; drag never quite reaches zero / friction actually stops; drag slows fast things
more than slow things / friction slows everything equally. Two marks. Stone → **friction** — one mark.

**A4.** [2] Because the length is the actual speed. Limiting x and y separately allows `(MAX, MAX)`,
whose length is `MAX × 1.414` — one mark — which is the diagonal bug from lesson 2 returning — one
mark.

**A5.** [2] The speed at which thrust and drag cancel, so the thing stops speeding up. It is
`THRUST / DRAG`. One mark each.

**A6.** [2] Because the position should use the velocity worked out *this* frame — one mark. Otherwise
every input is acted on one frame late, which is a lag of about 16 ms: too small to see and large
enough to feel as "dead" controls — one mark.

**A7.** [2] The test for whether the loss is bigger than the remaining speed
(`if (vel.length() <= loss) vel = zero`) — one mark. Without it the subtraction overshoots zero and the
thing accelerates slowly in the opposite direction, for ever — one mark.

---

## Section B

**B1.** [4] `1200 / 4 = 300 px/s`. Two marks. The clamp **never fires**, because 300 is below 500 —
two marks. This is exactly the "my max-speed slider does nothing" bug, now predicted in advance rather
than discovered.

**B2.** [3] Half: `ln(2) / 2 ≈ 0.347 s`. Two marks. Three quarters is two half-lives, so about
`0.69 s` — one mark. Credit anyone who notices that "three quarters gone" = "a quarter left" = two
halvings.

**B3.** [4] Acceleration `(0, 600)`. `vel = (100, 0) + (0, 600) × 0.1 = (100, 60)`. Two marks.
`pos = (0, 0) + (100, 60) × 0.1 = (10, 6)`. Two marks. Common error: adding the acceleration straight
to the position.

**B4.** [3] Length is 5, which is less than the loss of 6, so **with** the test the velocity becomes
`(0, 0)` — one mark. **Without** it: the unit vector is `(0.6, 0.8)`, times 6 is `(3.6, 4.8)`, and
`(3, 4) − (3.6, 4.8) = (−0.6, −0.8)` — one mark — so it is now moving backwards at 1 unit per frame,
and next frame it will reverse again, so it jitters or creeps instead of stopping — one mark.

**B5.** [3] 60 fps: about **0.18%** left. 20 fps: about **12%** left. One mark each. One mark for the
observation that the slower machine's ship is far *less* slowed, which is the opposite of what most
people guess.

---

## Section C

**C1.** [3] There is no drag and no speed limit, so velocity only ever grows. Two marks. One mark for
either fix; the better answer names both and says what each is for.

**C2.** [4] Two marks for identifying the per-axis clamp as the bug (and for noting it also fails for
negative velocities, since nothing clamps below `−MAX`). Two marks for:

```js
if (ship.vel.length() > MAX_SPEED) {
  ship.vel = ship.vel.normalise().scale(MAX_SPEED);
}
```

**C3.** [4] The missing zero test. When the remaining speed is smaller than `loss`, the subtraction
takes it past zero into the opposite direction — two marks. It never settles because each frame
reverses it again, and the sizes are tiny so it looks like a mysterious drift rather than arithmetic —
one mark. Fix, one mark: guard with `if (vel.length() <= loss) vel = Vec2.zero();`.

**C4.** [4] The position is updated **before** the velocity, so it uses last frame's velocity. Two
marks. Every input therefore takes effect one frame late — about 16 ms at 60 fps — which is below the
threshold at which people can identify a lag and above the threshold at which they can feel one: hence
"dead, and I can't say why" — two marks.

Worth saying to the class: this is not a crash, it will never show up in a test, and it is the kind of
defect that gets shipped. Order is part of correctness.

**C5.** [3] With `DRAG = 8` and `dt = 0.2`, `1 - DRAG * dt = 1 - 1.6 = −0.6`, so the velocity is
multiplied by a negative number and the ship reverses — two marks. Fix: `Math.exp(-DRAG * dt)`, which
is always between 0 and 1 and so cannot change the sign — one mark. Accept "clamp the factor to at
least 0" as a patch, with the note that it is a patch.

---

## Section D — marking the build

Mark these four:

1. **The speed readout exists** (checkpoint 2). Without a number on screen, everything after this is
   guesswork, and students who skip it struggle with checkpoints 3 and 7.
2. **They confirmed `THRUST / DRAG`** in checkpoint 3. This is the only place in the level where the
   notes predict a number and the program confirms it. It is worth insisting on.
3. **Checkpoint 6 was actually done.** Running the broken version at two frame rates is the
   correctness content of this lesson. A student who skipped it has not met the bug.
4. **They have an opinion in checkpoint 7, with a reason.** "It feels good" is not enough. "Fast to
   start and slow to stop, because the game is about dodging" is a design argument.

Expect checkpoint 1 to alarm people: the ship becomes unusable and several will think they broke it.
Say in advance that it is meant to happen.

---

## Section E — marking notes

**E1.** There is a good procedure and most students will not find it unaided. Credit any ordered plan;
the strongest looks roughly like:

1. `MAX_SPEED` first, with thrust huge and drag nearly zero, judged against the screen: how long should
   it take to cross the world? That answer comes from the *game*, not from feel.
2. `THRUST` second: how long to reach top speed? A quarter of a second is snappy, two seconds is a
   lorry.
3. `DRAG` third: how long to stop? Then notice it has moved the top speed, and go back to step 2. The
   loop between 2 and 3 is the real work.
4. `TURN_SPEED` last, because it is the only one you can judge entirely on its own.

The insight worth most credit: steps 2 and 3 **interact**, so tuning is iterative, and knowing
`THRUST / DRAG` tells you which way to move.

**E2.** The point is "find out" rather than "argue". Good answers: put both versions in front of five
people who have not seen the code, let them play without being told which is which, and ask which they
would rather play — not which is better. Credit anyone who notices they must not be told which is the
"clever" one. Strong answers mention that the right answer depends on the game: a rhythm game wants the
beginner version, a space game does not.

**E3.** The mechanism:

```js
const forward  = Vec2.fromAngle(car.angle);
const sideways = forward.perpendicular();
const alongAmount  = car.vel.dot(forward);    // how much of the velocity is forwards
const acrossAmount = car.vel.dot(sideways);   // how much is sliding
// drag the two by DIFFERENT amounts, then rebuild the velocity
car.vel = forward.scale(alongAmount * Math.exp(-DRAG_ALONG * dt))
     .add(sideways.scale(acrossAmount * Math.exp(-DRAG_ACROSS * dt)));
```

High `DRAG_ACROSS` grips: the car goes where it points. Low `DRAG_ACROSS` drifts. Full credit for
getting the dot products and the rebuild; partial credit for describing it in words. This *is* how
arcade racing games work, and a student who builds it has built something genuinely good.

**E4.** The general answer is a **tween**, or a timed interpolation between two sets of values:

- store two sets of numbers, `normal` and `icy`;
- store a single `t` that runs 0 → 1 over half a second, holds, then runs back;
- every frame, `lerp` each of the four numbers using that one `t`;
- drive the whole thing from a small state machine: `normal → entering → active → leaving → normal`.

Where it lives: not inside the ship, and not inside the input code. It belongs to whatever owns
power-ups. Credit students who notice this is the same machinery as a screen fade, a difficulty ramp, a
camera zoom and a menu slide — which is why lesson 9 builds it properly, and why question E4 was worth
asking.

---

## If you only mark one thing

Checkpoint 6. Everything else in this lesson is a matter of taste; the frame-rate bug is not, and it is
the only defect here that would survive into a released game and ruin it on somebody else's machine.
