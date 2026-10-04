# Lesson 4 — Solutions and marking notes

---

## Section A

**A1.** [2] Axis-Aligned Bounding Box. "Axis-aligned" rules out **rotation** — the box's sides are
always parallel to the screen edges. That restriction is what makes the test only four comparisons.

**A2.** [3] `a.x < b.x + b.w`, `a.x + a.w > b.x`, `a.y < b.y + b.h`, `a.y + a.h > b.y`, all joined by
`&&`. Three marks for all four correct; two for three correct; one for the right idea with the
inequalities muddled.

**A3.** [3] Rather than enumerating the many ways two boxes *can* overlap (one inside the other,
corner on corner, one much wider), ask when they definitely **cannot**: a is entirely left of b,
entirely right, entirely above, or entirely below. Those four are easy to be certain about. If none
of them holds, they must overlap — so the test is those four escape routes flipped round.

**A4.** [3] `20 + 30 = 50`. The centres are 45 apart, and `45 < 50`, so **yes, they are touching**,
by 5 pixels. Two marks for the comparison, one for the conclusion.

**A5.** [2] It makes near misses feel like misses, which players experience as fair and as a skilful
escape. Accept any sensible answer about fairness or feel — "bullet hell games do this so dodging
feels possible" is a very good one. Do **not** accept "to make it faster"; the size of a hitbox makes
no difference to the speed of the test.

---

## Section B

**B1.** [4] `a = {10,10,50,50}` so a spans x from 10 to 60 and y from 10 to 60.
`b = {55,70,40,40}` so b spans x from 55 to 95 and y from 70 to 110.

| Condition | Working | Result |
|---|---|---|
| `a.x < b.x + b.w` | `10 < 95` | true |
| `a.x + a.w > b.x` | `60 > 55` | true |
| `a.y < b.y + b.h` | `10 < 110` | true |
| `a.y + a.h > b.y` | `60 > 70` | **false** |

**They do not overlap.** They line up horizontally but b starts 10 pixels below where a ends.

One mark per condition evaluated. This is exactly the three-green-one-red case from the visualizer,
and it is worth saying so.

**B2.** [3] `x = 88`, `y = 88`, `w = 24`, `h = 24`. Two marks for the corner (centre minus radius),
one for the size (diameter, not radius).

**B3.** [4] With `||`, only **one** condition has to be true, and at least one is almost always true,
so the function returns `true` nearly everywhere. The player sees the ball bouncing off the paddle
from right across the screen — ricocheting off nothing, often getting stuck in a corner flipping its
velocity every frame.

Full marks need "it reports a collision when they are nowhere near each other", not just "it breaks".

**B4.** [4] `2400 ÷ 60 = 40 pixels per frame`. The wall is 14 pixels thick, so the ball can be in
front of the wall on one frame and past it on the next, without ever overlapping it. The test never
fires and the ball **passes straight through**. The problem is called **tunnelling**.

Two marks for the 40, one for the explanation, one for the name.

---

## Section C

**C1.** [4] The position fix is missing: `ball.x = paddle.x - ball.radius;` (or equivalent) before
flipping the velocity. Without it the ball is still overlapping on the next frame, so the test fires
again and flips the velocity back, over and over.

Two marks for the fix. **Two marks for recognising this as the same bug as the wall bounce in lesson
2** — the question asks "where have you seen this before?" and noticing that two bugs are the same
bug is the skill being tested.

**C2.** [4] You also need a direction check, such as `&& ball.speedX < 0`.

The reason: the position fix moves the ball to the paddle's edge, where it is still *just* touching.
On the very next frame it may still overlap by a fraction of a pixel, so the test fires again and
flips the velocity back into the paddle. Checking that the ball is actually moving *towards* the
paddle means a ball already on its way out is ignored.

Two marks for the condition, two for the explanation. Accept other correct approaches — moving the
ball a pixel further clear, or a short "already hit" cooldown — but ask what those cost.

**C3.** [3] Two mistakes:

1. **Size.** `w` and `h` are set to the radius, but the box should be a full **diameter** —
   `ball.radius * 2`. So the hitbox is half the size it should be.
2. **Position.** `x` and `y` are set to the ball's **centre**, but a box's `x`/`y` are its
   **top-left corner**. It should be `ball.x - ball.radius`.

So the hitbox is both too small and offset down-and-right by a radius. Two marks for finding both,
one for correctly describing the effect.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 2 — insist on the debug view.** Students skip it because it does not make the game
better. It is the single highest-value thing in this lesson: every subsequent collision bug becomes
visible instead of mysterious, and lesson 6 is far easier for the students who built one. If anyone
refuses, let them hit one invisible bug and then suggest it again.

**Checkpoint 4 — the opponent must be beatable.** Students invariably write an opponent that tracks
the ball exactly, then discover the game is unwinnable and conclude their code is broken. It is not:
a perfect opponent is a correct implementation of a bad design. The fix is to make it slower than the
ball, or to add a dead zone, or to make it track with a delay. This is a genuinely good moment to
point out that "working correctly" and "good" are different things.

**Checkpoint 5 is the real lesson.** Make them actually play a rally with `STEER_STRENGTH` at 0.
With no steering, Pong is a game about standing in the right place and the rally is decided by
geometry. With steering, it is a game about aiming. Same code, completely different activity. Ask
the class which they would rather play and why — the answer is obvious and the *reason* is not.

---

## Section E — marking notes, not answers

**E1/E2/E3 — tunnelling.**

The sketch should show the ball on one side of the wall at frame 1, past it at frame 2, with the step
larger than the wall is thick, and no frame at which the two overlap.

Fixes students invent, and what each costs:

| Fix | Cost |
|---|---|
| Make the wall thicker than one frame's movement | Changes the game's design to work around a technical limit, and breaks again if anything gets faster |
| Cap the maximum speed | Limits the game |
| Move in several small steps per frame ("substepping") | Slower; and how many steps is enough? |
| Test the whole **line** the ball travelled, not just its end point | More complicated maths; this is the real answer, called **swept collision** |
| Run the physics at a fixed, higher rate | The fixed timestep — the advanced level's answer |

Full marks for any fix plus an honest cost. The best answers notice that substepping and swept
collision are really the same idea at different resolutions.

**E4 — too many tests.**

Students reliably invent some form of **spatial partitioning**. Expect answers like:

- "Divide the screen into a grid of squares and only test things in the same square."
- "Only test bullets against enemies that are close in x." (This is a *sweep and prune*.)
- "Give each enemy a big circle around it and check that first." (A bounding-volume hierarchy.)
- "Keep a list of enemies per region and look up the bullet's region."

All of these are real techniques used in real engines. The first is a **uniform grid** or **spatial
hash**; checking a cheap test before an expensive one is the **broad phase / narrow phase** split.

**Do not give the names before they have tried.** Telling a 14-year-old that the thing they just
invented in eight minutes is in every commercial game engine, and is called a uniform grid, is one of
the best moments available in this entire course. It is lesson 3 of the advanced level.

Push the strong students with: what happens to your grid when one object is enormous? What happens
when everything crowds into one cell? Those are the real difficulties, and they are what makes this
an interesting problem rather than a solved one.

---

## Stretch goals

1. **Bricks** — the usual approach is an array of brick objects with an `alive` flag, because
   removing items from an array while looping over it causes skipped elements. That trap is worth
   letting them hit; it comes back properly in lesson 6.
2. **Circle versus rectangle** — the standard solution is to clamp the circle's centre to the
   rectangle's bounds to find the closest point, then measure the distance from the centre to that
   point and compare with the radius. It is only four lines but it is genuinely hard to derive.
   Anyone who gets it unaided has done something impressive.
4. **The oversized paddle hitbox** — most students cannot tell it is happening, and report the game
   "feels better". That is the entire point, and it is worth telling them afterwards that commercial
   games do this constantly and never mention it.
