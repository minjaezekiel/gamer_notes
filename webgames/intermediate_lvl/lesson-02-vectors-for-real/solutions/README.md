# Lesson 2 — Solutions and marking notes

---

## Section A

**A1.** [2] Divide both parts by the vector's length, so the direction is unchanged and the length
becomes exactly 1. The result is a **unit vector**. One mark each.

**A2.** [2] **"target minus me."** Accept any clear equivalent (`to = destination − start`). The point
is that they have a sentence to say, not a rule to remember.

**A3.** [3] Length 0 means dividing by zero, which in JavaScript gives `NaN`. One mark. `NaN` never
throws, and every arithmetic operation involving it produces `NaN`, so the value spreads through
position, velocity and everything downstream — one mark. The sprite simply disappears with a clean
console, so there is no error message and no line number to start from — one mark.

**A4.** [2] A **position** (an arrow from the origin to a point) or a **movement/direction** (an arrow
that could be drawn anywhere). One mark. You should never add two positions together — one mark.
Credit students who note that *subtracting* two positions is not only allowed but is the most useful
operation there is; the result is a movement, not a position, which is the real insight.

**A5.** [2] Angle 0 points **right** (the positive x direction), and angles grow **clockwise** — one
mark. Because y points down on a screen, which mirrors the direction of rotation compared with a maths
diagram — one mark.

**A6.** [3] 1 = pointing the same way · 0 = at right angles · −1 = pointing opposite ways. One mark
each. Deduct nothing for saying "parallel" instead of "same way", but do point out that −1 is also
parallel.

**A7.** [2] When you only need to **compare** distances or test a radius, because the square root is
the expensive part — one mark. It is valid because squaring preserves order for non-negative numbers:
if `a² < b²` then `a < b` — one mark. Remember to compare against `range * range`, not `range`.

---

## Section B

**B1.** [3] `length = √(81 + 144) = √225 = 15`. Normalised: `(9/15, 12/15) = (0.6, 0.8)`. Two marks for
the length with working, one for the unit vector. Bonus point: this is the 3-4-5 triangle scaled by 3,
which is why the numbers are tidy.

**B2.** [4]
- `toPlayer = (160−100, 180−100) = (60, 80)`
- `length = √(3600 + 6400) = √10000 = 100`
- `direction = (0.6, 0.8)`
- `step = direction × 200 × 0.1 = (12, 16)`
- new position `(112, 116)`

One mark per stage, up to four. A common wrong answer is `(106, 108)`, from multiplying by `dt` twice.

**B3.** [3] `direction` is now `(60, 80)` with length 100, so the step is `(60, 80) × 20 = (1200, 1600)`
and the enemy lands at `(1300, 1700)` — right off the screen. Two marks for the numbers. One mark for
the behaviour: speed becomes proportional to distance, so the enemy rockets in from far away and
crawls when close, which is the opposite of what anybody wants.

**B4.** [3] `fromAngle(0)` is `(cos 0, sin 0) = (1, 0)`, pointing **right**. `fromAngle(π/2)` is
`(0, 1)`, pointing **down** on screen — one mark each — and the third mark is for getting "down"
rather than "up", which is the whole reason the question is asked.

**B5.** [4] 30° → dot 0.87 → **seen**. 60° → dot 0.5 → not seen. 120° → dot −0.5 → not seen. One mark
each, plus one for noticing that `dot > 0.7` is a cone of about ±45°, so anything beyond 45° to either
side is invisible.

---

## Section C

**C1.** [3] The subtraction is backwards. `enemy − player` points *from the player towards the enemy*,
which is away. Fix: `player.pos.sub(enemy.pos)`.

Watch for students who "fix" it with `scale(-SPEED * dt)`. It works, and it leaves them with no model.
Make them say "target minus me" out loud.

**C2.** [4] When the enemy arrives exactly on the player, `this.length()` is 0, so both divisions are
`0 / 0`, which is `NaN`. One mark. The enemy's position becomes `NaN`, so `ctx.arc(NaN, NaN, …)` draws
nothing — one mark. `NaN` is never equal to anything, including itself, so no later arithmetic repairs
it: the enemy is gone permanently — one mark. Fix: the `if (len === 0) return new Vec2(0, 0);` guard —
one mark.

Accept, and praise, a second fix: stop the enemy before it reaches the player (`if (dist > 22)`), which
avoids the situation instead of handling it. The best answers do both.

**C3.** [3] Both bugs are in the one line. (a) The arguments are the wrong way round: it must be
`atan2(y, x)`, not `atan2(x, y)` — swapping them reflects the angle about the 45° line, which at the
cardinal directions looks like a 90° error. (b) There is no need for `atan2` at all here: the ship
already *has* an `angle`, so `ctx.rotate(ship.angle)` is the whole answer. Two marks for the argument
order, one for noticing the round trip is pointless.

**C4.** [2] `ctx.restore()` is missing, so the `translate` and `rotate` accumulate every frame for the
whole life of the program. Full marks need "accumulate", not just "it's missing".

**C5.** [4] `direction` has length 1, so adding it moves the enemy exactly **one pixel per frame** —
and nothing is multiplied by `SPEED` or by `dt`. Two marks. A unit vector's length is 1 pixel, which is
to say it has no useful scale at all: it is a pure direction, and supplying the size is the caller's
job — one mark. Fix: `.add(direction.scale(SPEED * dt))` — one mark.

---

## Section D — marking the build

Four things to look for, in order of importance:

1. **The speed readout is identical in all eight directions.** This is the one objective test in the
   lesson. Make them demonstrate it.
2. **The `NaN` guard is present** in their own `normalise`. Ask them to delete it and drive a chaser
   onto the player, so they have seen the failure once in their life.
3. **Bullets are removed backwards** through the array. A forward loop with `splice` skips elements;
   this was taught at beginner level and this is the lesson where it bites again.
4. **Rocks use a random angle, not random x and y speeds.** Checkpoint 6 asks them to say why. The
   answer: independent random x and y favour the diagonals, because getting a large value in *both* is
   more likely than getting a large value in one and nearly zero in the other. A student who draws 200
   random vectors and looks at the picture has done real science; give extra credit.

Expect checkpoint 3 to take longest. Drawing something rotated is the first time most of them have met
a canvas transform, and the mental model (move the paper, not the pen) needs saying out loud more than
once.

---

## Section E — marking notes

**E1.** All three alternatives are defensible; the reasoning is what is marked.

- `(0, 0)` — what we chose. Nothing breaks and the thing stops moving. **Cost: it hides the bug.** An
  enemy that quietly fails to move looks like a different problem entirely.
- **Throw** — the loudest option, and in a 60 fps loop it also stops your whole game because one enemy
  happened to arrive on the player. Good for a test suite, harsh in a game.
- **`null`** — forces the caller to think, which is honest, and makes every single call site longer.
- **`(1, 0)`** — the worst of the four, and worth discussing: the enemy would snap to facing right for
  no reason the player can see, which is a visible bug with an invisible cause.

Full credit for anyone who distinguishes *development* from *shipping*: throw while building, return
`(0, 0)` in the released game. That is a real engineering answer.

**E2.** A good answer lists:
- it must remember its own **facing** (an angle or a unit vector) separately from where its target is;
- a **turn rate** in radians per second limits it;
- each frame: work out the desired angle with `atan2`, find the *difference*, clamp that difference to
  `turnRate * dt`, add it;
- fly along its own facing, not towards the target.

The subtlety worth hunting for: the angle difference has to be wrapped into the range −π…π, or a
missile at 350° chasing a target at 10° turns the long way round. Students discover this by watching a
missile spin. Credit anyone who predicts it in advance.

**E3.** The method matters more than the answer. Good answers propose: open the performance profiler,
look for garbage-collection pauses, and compare against a mutable version — rather than guessing.
The honest answer for a school-sized game is "no, it is not a problem, and you should still know how
to check". Have them write their prediction down; lesson 9 opens the profiler.

**E4.** This is the reflection formula, and it is the best question on the sheet.

- Let `n` be the unit vector at right angles to the wall (the **normal**).
- `v.dot(n)` is **how much of the velocity is heading into the wall**. That is the part to reverse; the
  part along the wall should be left alone.
- Subtracting it once removes it (giving a slide along the wall). Subtracting it **twice** reverses it:
  `v' = v − n·(2·v.dot(n))`.

Check it on a case they know: a floor has `n = (0, −1)`, so `v.dot(n) = −vy`, and the formula gives
`vy' = −vy` with `vx` untouched — exactly the beginner-level bounce. Full credit for anybody who
arrives at "subtract twice", with or without the notation. Strong credit for testing it against the
flat-wall case, because checking a new formula against a case you already know is a habit worth more
than the formula.

---

## If you only mark one thing

The speed readout in checkpoint 2. A student who has watched 424 become 300 has internalised
normalising in a way that no amount of explanation achieves, and the rest of the level depends on it.
