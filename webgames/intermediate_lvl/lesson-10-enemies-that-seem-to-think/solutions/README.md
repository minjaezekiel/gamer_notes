# Lesson 10 — Solutions and marking notes

---

## Section A

**A1.** [2] From the **switching** between simple behaviours, at moments the player can see and understand
— one mark. An enemy with one complicated behaviour looks mechanical; three simple ones with visible
reasons for changing look alive — one mark.

**A2.** [2] So that adding a behaviour touches nothing that already works: `decide` grows one branch and
`act` grows one branch — one mark. It also prevents the state from being changed halfway through acting,
which produces an enemy that is in two states in one frame — one mark.

**A3.** [3] Different thresholds for entering and leaving a state — one mark. It prevents flicker: with one
threshold, something sitting exactly on the boundary switches every frame — one mark. An outside example:
a thermostat that heats to 21° and stops at 22°, a lift that will not reverse for one person, or a UI drag
that needs a few pixels before it starts — one mark.

**A4.** [3] Because the ray is sampled at points, not swept continuously — two marks — so a step larger
than a tile can land on either side of a thin wall and never inside it, and the enemy sees through it. One
mark. Credit anyone who notes it would be *intermittent*, depending on the angle, which is worse than a
consistent bug.

**A5.** [2] No wrap-around arithmetic: comparing angles needs special handling because 359° and 1° are two
degrees apart but look 358 apart — one mark. And it is cheaper — two multiplications and an addition, no
`atan2` — one mark.

**A6.** [3] Five enemies running the same recipe towards the same point end up in exactly the same place,
so they look like one enemy — two marks. It looks like an individual bug because **every individual is
behaving perfectly**: the problem only exists between them, which is the first time most students meet
emergent behaviour — one mark.

**A7.** [3] Any three, one mark each: **reaction time** (gives the player a moment; makes the enemy look
like it is realising) · **telegraph** (the player can respond, so losing feels like their own mistake) ·
**inaccuracy** (perfect aim is unbeatable and reads as cheating) · **turn rate** (can be outmanoeuvred,
which is a skill the player can learn).

---

## Section B

**B1.** [3] Starts chasing at **under 180**. Gives up at **over 250**. The band is **70 px** wide, and
inside it nothing changes. One mark each.

**B2.** [4] The mode changes on almost every frame the player's distance crosses 180 — so with small
movements it could toggle dozens of times a second, up to about 60 state changes. Two marks. The player
sees the enemy start and stop, and any sound or animation attached to entering a chase fires repeatedly —
one mark. And nothing in the code looks wrong, which is the point — one mark.

**B3.** [3] `200 / 16 = 12.5`, so about **12 lookups** per test. Two marks. `12 × 12 enemies × 60 fps ≈
8,640 per second`, which is nothing — one mark. Credit anyone who notes that this is why you can afford it
every frame at this scale, and why you would not at 200 enemies.

**B4.** [3] `(1 × 0) + (0 × −1) = 0`. Two marks. **Not** inside the cone, since 0 is not greater than 0.7 —
the player is at exactly 90°, off to the side — one mark.

**B5.** [4] At 300: outside the radius, so **200** (full speed). At 100: `200 × (100/100) = 200`. At 50:
`200 × 0.5 = 100`. At 0: **0**. One mark each.

---

## Section C

**C1.** [3] One threshold for both directions, so a player on the boundary flips it every frame. Two
marks. Fix: test the two directions separately with different numbers, as in the cheat sheet — one mark.

**C2.** [4] Separation is missing. Two marks. It looks like an individual bug because each enemy is doing
exactly what it was told — the overlap is a property of the *group*, not of any member of it. One mark.
Fix: add a push away from any neighbour within a personal-space radius, stronger the closer they are — one
mark.

**C3.** [3] `=` instead of `+=`. Two marks. A brand-new random angle every frame gives a direction that
jumps all over the place; nudging the existing angle gives a meander — one mark. Note the random value is
also being scaled by `dt`, which only makes sense as a nudge, so the line is self-contradictory as written.

**C4.** [4] `STEP` of 48 is larger than `TILE` of 32, so consecutive sample points can straddle a
one-tile wall without landing in it. Two marks. "Sometimes but not always" is because it depends on the
angle and the exact distance, which is what makes it maddening to debug — one mark. Fix: `STEP = TILE / 2`
or smaller — one mark.

**C5.** [3] When the enemy's position equals the player's exactly, the subtraction gives `(0, 0)`, whose
length is 0, and normalising divides by zero to give `NaN`. Two marks. `NaN` spreads and never recovers, so
the enemy is gone for good — and the console is clean. Fix: the zero guard in `normalise`, or stop the
enemy before it arrives (`if (dist > 20)`) — one mark. Best answers do both.

---

## Section D — marking the build

1. **The mode is drawn above the enemy** (checkpoint 1). Insist on it. Everything else in this lesson is
   diagnosable in seconds with that label and guesswork without it.
2. **They saw the flicker before fixing it** (checkpoint 2). The state-change counter is the evidence.
3. **The sight ray is drawn, in two colours** (checkpoint 3). This is the second most valuable debug
   drawing in the lesson.
4. **Separation on and off, with five enemies** (checkpoint 5). Ask them to do it for you; the difference
   gets a reaction every time.
5. **They played with the handicaps off and on** (checkpoint 7). Better still, have them hand the keyboard
   to a classmate for the "perfect" version.
6. **Checkpoint 8 was attempted honestly.** The expected finding is that they cannot tell, which is a
   surprising and useful result.

Expect checkpoint 3 to take the longest. Students often put the ray test in the wrong place — inside
`act` rather than `decide` — and then wonder why the enemy chases a player it cannot see.

---

## Section E — marking notes

**E1.** There is no single number, and the method is what is marked. A good answer: make the rate a
variable, play at 60, 20, 10, 5 and 2 decisions a second, and have somebody who does not know the setting
try to guess it. Typical honest finding: 10 is indistinguishable, 5 is noticeable on a fast-moving enemy
and fine on a slow one, 2 is clearly wrong.

Credit strongly any answer that says **it depends on what the enemy is doing**: a patrolling guard can
think twice a second; something dodging the player's bullets cannot. The general rule is that the rate has
to match how quickly the thing it is reacting to can change.

**E2.** All three are used in real games and they make different games:

- **Back to the start of the route** — the most forgiving. The player can reset a situation by breaking
  line of sight, which rewards hiding and makes stealth into a puzzle with a known solution.
- **Carry on from where it is** — the enemy's patrol is now disrupted permanently, so the level drifts away
  from its designed state. Realistic, and it makes a level harder to design.
- **Go to where it last saw you** — the most threatening, and it rewards *moving after* breaking line of
  sight rather than standing still. This is what most stealth games do, and it is why "hide and wait" does
  not work in them.

Full marks require naming the consequence for how the player should play. That is the actual design skill:
a rule about the enemy is a rule about the player.

**E3.** Mark the *specificity*. A strong answer looks like:

- a slow heavy attack with a **600 ms** wind-up, visible as a raised arm and a sound — counter: walk away,
  or attack during the wind-up;
- a fast attack with only **150 ms** of warning but short reach — counter: keep your distance;
- a charge that only happens in a straight line — counter: stand behind something;
- and the enemy **cannot** do two of these at once, so the player always has an answer.

The key marks are for *numbers* and for *a counter to each thing*. Watch for answers where the counter is
"be quicker", which is not a counter. Also credit anyone who says the enemy must be beatable by a player
who has understood it rather than by one with faster hands.

**E4.** The memory is the whole question. A good answer:

- a new state, `search`, between `chase` and `patrol`;
- stored on the enemy: `lastSeenPosition` (a `Vec2`) and `searchTimer` (seconds);
- `chase → search` when sight is lost, recording the position at that moment;
- `search`: move to `lastSeenPosition`, then wander near it while `searchTimer` counts down;
- `search → chase` if the player is seen again; `search → patrol` when the timer expires.

The marks are for noticing that (a) the memory lives **on the enemy**, not in a global, so two guards can
be searching different places; and (b) the memory must **expire**, or a guard searches for ever and the
level never recovers.

Strong answers go further: the memory should be *wrong* in a useful way. Recording where the player was,
not where they are, is exactly what makes the player's correct move "keep going", and that is the whole
tension of a stealth game — the enemy's out-of-date information is the gameplay.

---

## If you only mark one thing

Have a student hand you the keyboard with the enemy set to "perfect", let yourself lose, and ask them what
you should have done differently. If they cannot answer, the enemy is unfair, and that is the one thing in
this lesson worth getting right.
