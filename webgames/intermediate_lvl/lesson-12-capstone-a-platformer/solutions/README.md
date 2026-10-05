# Lesson 12 — Solutions and marking notes

---

## Section A

**A1.** [6] One mark each, and the *moment* matters as much as the name:

| part | the moment it fixes |
|---|---|
| the impulse | the player wants to leave the ground |
| variable height | they wanted a small hop and got a full jump |
| coyote time | they pressed jump just after walking off a ledge |
| jump buffering | they pressed jump just before landing |
| apex hang | the top of the jump felt like no moment at all |
| fast fall | the whole jump felt floaty |

**A2.** [3] Both are "remember an input for a short while": coyote time remembers that the **ground** was
there, jump buffering remembers that the **press** happened — two marks. The jump then fires when both
countdowns are positive at the same time, in either order — one mark.

**A3.** [2] Because the window is still open on the following frames, so the next buffered press would fire
again in mid-air — one mark — giving an accidental double (or triple) jump — one mark.

**A4.** [2] Multiplying leaves the player still rising, just less, which reads as "a shorter jump" — one
mark. Setting it to 0 stops them dead, which reads as "I hit something" — one mark.

**A5.** [3] Because height and time are what you can *picture* and what the level design is actually about
— two marks — and because changing the jump height then does not require re-tuning gravity by trial and
error: the two numbers in the code are the two numbers you were thinking about — one mark.

**A6.** [3] It needs **which way the player is moving** and **where they were before the move** — two
marks. Without the previous position, a player jumping up through the platform satisfies "moving down" at
the moment gravity takes over mid-platform and snaps onto its top — one mark.

**A7.** [3] Say nothing / give no instructions · write down confusions as they happen, not afterwards ·
afterwards ask what they were *trying* to do rather than whether they liked it. One mark each. Accept "do
not help" as the first.

---

## Section B

**B1.** [4] `GRAVITY_UP = 2 × 96 / 0.3² = 192 / 0.09 ≈ **2133 px/s²**`. Two marks.
`JUMP_SPEED = 2133 × 0.3 ≈ **640 px/s**`. Two marks.

**B2.** [3] `height = 600² / (2 × 1800) = 360000 / 3600 = **100 px**`. Two marks.
`time = 600 / 1800 = **0.33 s**`. One mark.

**B3.** [4] At t = 0.08 the coyote timer still has 0.02 s left, so **yes, it jumps** — two marks. At
t = 0.14 the coyote timer expired at 0.1, so **no** — two marks. Credit anyone who notes the buffer is
irrelevant in both cases: the press is current, so it is the *ground's* memory that decides.

**B4.** [3] The press is remembered for 0.12 s, so at t = 0.09 the player lands with 0.03 s of buffer left
and jumps **immediately on landing** — two marks. With no buffer the press was thrown away, they land, and
nothing happens — the game appears to have ignored them — one mark.

**B5.** [3] The player is moved and collided against the platform's **old** position, then the platform
moves up into them — two marks. Each frame the platform overlaps them slightly more, so they sink into it,
and the vertical collision pushes them out only once per frame, producing a visible judder or a slow sink
of up to 60 px over a second — one mark.

---

## Section C

**C1.** [3] `coyote` is not reset, so the window stays open and the next press — or the same held press
after the buffer refills — fires again in the air. Two marks. Fix: set `coyote = 0` as well as `buffer = 0`
— one mark.

**C2.** [4] `buffer` is refilled on every frame the key is **held**, not on the press. Two marks. So the
moment they land, the buffer is full and a new jump fires immediately, repeatedly — one mark. Fix: use a
just-pressed test (lesson 7's `wasPressed`) to fill the buffer, so holding does nothing after the first
frame — one mark.

**C3.** [3] `vy = 0` removes all the upward velocity at once, which is physically what happens when you hit
a ceiling, so that is what it feels like. Two marks. Fix: `vy *= 0.45` — one mark.

**C4.** [4] The platforms are moved **after** the player and after collision resolution. Two marks. Fix,
two marks: move the platforms first, carry any passenger by the same delta, then move the player and
resolve. Credit anyone who adds that `ridingPlatform` must be set by the downward collision test.

**C5.** [4] There is no "was above" test, so as soon as the jump's upward velocity turns downward — which
happens at the apex, possibly while the player is inside the platform — `movingDown` becomes true and they
land on top of it. Two marks. Fix: also require that the player's bottom edge was above the platform's top
edge *before* this frame's move — two marks.

---

## Section D — marking the build

Mark in this order, because the order is the priority:

1. **The jump refinements can each be switched off** (checkpoint 2), and the timers are drawn. Ask them to
   turn coyote time off while you watch them play. If they cannot feel the difference, have them try the
   ledge jump deliberately.
2. **Checkpoint 3 has a written-down number.** The largest coyote time they cannot notice is a real
   measurement they made, and it is usually between 0.08 and 0.15.
3. **One level, finished** (checkpoint 6). Resist rewarding ambition here. A student with one polished
   level has learned more than a student with four half-built ones, and the whole level has been building
   towards that judgement.
4. **The playtest sheet exists** (checkpoint 7) and has specific observations on it, not "they liked it".
   No sheet, no marks for checkpoint 7 — the writing *is* the exercise.
5. **Exactly one change** (checkpoint 8), tested. A student who made six changes has not learned what any
   one of them did.

The definition-of-done list in the notes is a good marking rubric for the game itself: title, pause,
winnable by somebody else, survives blocked storage, discoverable controls.

**On the playtest:** circulate and stop people from helping. You will have to do this repeatedly. It is
worth saying out loud, more than once: *every time you help, you destroy the thing you came for.*

---

## Section E — marking notes

**E1.** Plenty of good answers. Credit any two with a reason:

- **The pause/menu press** from lesson 7 — a buffered press so a menu selection registers during a
  transition. (This is the one they already met.)
- **An attack during a landing animation**, so a press at the end of one action starts the next.
- **A direction pressed just before a character becomes controllable** again after a hit.
- **A door or switch press** a moment before arriving at it.
- **A dash input** during hitstop, so the frozen frames do not eat the press.

The general statement, worth full marks: *any time the game is briefly unable to act on an input, the
input should be remembered rather than discarded.* Credit anyone who also names the opposite side — a short
window **after** an ability ends during which it still works, which is coyote time generalised.

**E2.** Three examples, with units. Strong answers:

- **Enemy speed** as "seconds to cross the screen", not px/s.
- **A reload or cooldown** as "shots per second", not a frame count.
- **Camera smoothing** as "seconds to catch up", not a lerp factor (which is also the frame-rate-safe
  version from lesson 6).
- **Drag** as a half-life in seconds, which was lesson 3's first stretch goal.
- **Level difficulty** as "expected deaths per attempt", which is a genuinely sophisticated answer.

The pattern worth drawing out: the design unit is usually a **time** or a **distance the player can see**,
and the engine unit is usually a rate. Converting once, at the top of the file, is the whole technique.

**E3.** Mark the *order* of their thinking. A strong answer answers the three questions in the order asked:

- **The problem it solves** — "the gaps are at the edge of the jump's reach, so there is no way to recover
  from a slight mistake" → a dash gives a second chance and a skill ceiling.
- **What the level must do** — gaps that are *just* beyond a jump, so the dash is required somewhere and
  optional elsewhere; somewhere safe to practise it.
- **What it breaks** — every existing gap is now trivial, so the level they already built becomes easy; and
  any place they relied on the player *not* being able to reach something is now broken.

The third part is the one students skip, and it is where the marks are. A new ability invalidates old level
design, which is why real games add abilities and then redesign the levels behind them.

**E4.** This is the best question in the level and the method is what is marked.

How to tell them apart — each cause has a different observable signature:

| cause | how you would know |
|---|---|
| the jump is too long | they *always* fall short, by a consistent amount. Measure the gap against their maximum jump. |
| the landing is not visible | they jump and then look surprised; they do not aim. The camera or the level composition is hiding the target. |
| the run-up is too short | they fall short only sometimes — when they have not got up to speed. Watch their horizontal speed at the moment they leave the ground. |
| the controls were never explained | they do not try the right input at all, or try it late. Watch their first three attempts specifically. |
| the penalty is too high | they succeed eventually but stop enjoying it. Watch their face, and count how far back the restart puts them. |

What to change first, and the best answer here is **not** the jump: it is whichever change is **cheapest to
test and most reversible**. Usually that is the camera or the run-up distance, not the physics, because
changing the jump re-tunes the entire level.

How you would know it worked: **the same test with a different person**, counting deaths at that spot. One
change, one measurement. A student who proposes changing three things at once and then declaring success
has not understood the method, however good the three changes are.

---

## If you only mark one thing

The playtest sheet. Specific, written-in-the-moment observations about somebody else playing — and one
change made because of them. That single page is the difference between a student who makes games and a
student who writes game code, and it is the right thing for this level to end on.
