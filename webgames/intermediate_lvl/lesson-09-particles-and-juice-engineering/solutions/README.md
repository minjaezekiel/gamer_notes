# Lesson 9 — Solutions and marking notes

---

## Section A

**A1.** [3] A position, a velocity, and a countdown (`life`). Two marks. `t = life / maxLife` runs from 1
to 0, and multiplying alpha, size, speed or colour by it makes the particle fade out in step — one mark.

**A2.** [2] Feedback that arrives later than about 100 ms after the action stops feeling connected to it —
one mark. That is six frames at 60 fps — one mark.

**A3.** [3] Because getting a large value in **both** `vx` and `vy` is more likely than getting a large
one in just one, so the directions bunch towards the diagonals — two marks. Instead pick a random
**angle** and use `cos` and `sin` — one mark. Credit anyone who suggests spawning 300 and looking, which
is how you would check.

**A4.** [3] Objects that are thrown away must later be collected, and collection happens when the engine
chooses — two marks. The symptom is **not** a slow game: it is a game at a steady 60 fps that drops a
single frame every few seconds, which is more noticeable than being uniformly slower — one mark.

**A5.** [3] Any three, one mark each: adding to `camera.x` instead of using a draw-time offset (the view
drifts and fights the follow code); no decay (it shakes for ever); no cap (several explosions make the
screen unreadable); too strong (it should be barely noticed — 3–8 px, not 40).

**A6.** [2] Freezing the game's update for 50–80 ms at the moment of impact — one mark. It works because
the pause tells the player's hands that the hit connected; three frames of nothing is a lot of feedback —
one mark.

**A7.** [2] The average tells you the cost; the **worst** tells you what the player actually feels — one
mark. A game with a 4 ms average and a 30 ms worst stutters visibly, and the average hides it completely —
one mark.

---

## Section B

**B1.** [3] `t = 0.2 / 0.8 = 0.25`. Alpha **0.25**, size `6 × 0.25 = 1.5`. One mark for `t`, one each for
the two results.

**B2.** [3] After 0.2 s: `12 × e^(−1.2) = 12 × 0.301 ≈ **3.6**`. Two marks. After 1 s:
`12 × e^(−6) ≈ 0.03`, which the `< 0.1` test would snap to **0** — one mark.

**B3.** [4] Removing an element shifts everything after it down one, while `i` still goes up, so the
particle immediately after each removed one is **skipped** — two marks. The player sees some dead
particles persisting for an extra frame or two, and with several dying at once, some stay visibly stuck —
one mark. Fix: loop backwards — one mark.

**B4.** [3] The last particle's alpha is nearly 0 when it is drawn, and nothing resets it, so the score
drawn afterwards is almost invisible — two marks. It fades in and out in time with the particles, and
nothing in the score's code mentions transparency, which is what makes it hard to find — one mark.

**B5.** [4] 200 slots are still in use, so `500 − 200 = 300` are free and the second explosion gets all
**300** of the particles it asked for. Two marks for the arithmetic.

Two marks for the judgement, which is the real question: it is **not** a problem — and it would not have
been a problem if it had come up short either. Dropping the extras is the correct behaviour, because the
pool size puts a hard ceiling on the work per frame, so a hundred explosions at once cannot bring the game
down.

The case worth drawing out with the class: if the first explosion were still holding 400 slots, the second
would get only 100 and would look visibly thin. So the pool size is a **design decision** about the worst
case, not just a number — which is why `code/02` lets them change it.

Credit any student who notices the more interesting case: if the first explosion were still holding 400,
the second would get only 100 and look thin — so the pool size is a design decision, not just a number.

---

## Section C

**C1.** [3] `globalAlpha` is fixed at 1 and the size does not use `t`. Two marks. Fix: `t = life /
maxLife`, then `globalAlpha = t` and `size * t` — one mark.

**C2.** [4] The shake is written into `camera.x`, which is the camera's real position — two marks. So the
shake never cancels out (the random values do not sum to zero), and it fights the follow code, leaving a
permanent offset — one mark. Fix: keep `shake` as a separate number and apply it as a `translate` at draw
time, inside a `save`/`restore` — one mark.

**C3.** [3] There is no decay — the `if` only snaps a small value to zero, and `shake` never gets small.
Two marks. Fix: `shake *= Math.exp(-DECAY * dt);` before the test — one mark.

**C4.** [4] The `return` skips the **whole frame**, including `draw`, so nothing is redrawn and the game
appears to lock up — two marks. Fix: do not return. Set `dt = 0` for the world's update and carry on, so
that drawing, the HUD and the particles still run — two marks.

This is question E1, and students who get C4 right have usually answered E1 too.

**C5.** [3] The average is the wrong number. Two marks: a 4 ms average with a once-a-second stutter means
the **worst** frame is far above 16 ms, and the average hides one bad frame among sixty good ones. One
mark for the likely cause — garbage collection from objects allocated every frame — and for the right next
step: measure the worst, not the average, and look at whether the stutter goes away when pooling.

---

## Section D — marking the build

1. **The fade works before anything else** (checkpoint 1). Particles without `t` look wrong and no amount
   of other effects fixes it.
2. **Smoke uses negative gravity** (checkpoint 2). If they wrote a separate smoke function, ask what is
   different about it. The answer should be "numbers".
3. **Shake is a translate, not a camera change** (checkpoint 3). Test by shaking a lot and then standing
   still: the view must return exactly.
4. **The HUD draws during hitstop** (checkpoint 4). This is C4 in their own code.
5. **The frame-time readout exists** (checkpoint 8) and shows **both** numbers.
6. **They actually did the all-off / all-on comparison.** Ask them to do it for you. The students who do
   it are the ones who understand what they built.

The halving exercise is worth running as a whole class: have everybody halve every juice number and play
again. Most will prefer it, and several will not believe you beforehand.

---

## Section E — marking notes

**E1.** A good rule separates three groups:

- **Frozen:** the player, enemies, projectiles, physics, timers that affect the rules. Anything the
  outcome depends on.
- **Not frozen:** particles from the hit itself (they are *showing* the impact, so they should fly), the
  flash and squash animations, the HUD, the camera shake, and anything the player needs to keep seeing.
- **A judgement call:** sound. Usually it should continue; a frozen sound is a glitch.

The clean way to say it: hitstop sets `dt = 0` for the **simulation** but leaves `realDt` for
**presentation**. Full marks for any answer that separates those two words, however they phrase it.
Credit anyone who notices this means their update function needs two different time values, which is a
real and slightly uncomfortable consequence.

**E2.** The answer is machine-dependent, which is the point. Typical findings on a modern laptop: no
measurable difference below about 2,000 particles; a visible difference in the *worst* frame time
somewhere between 5,000 and 20,000; and a clear one at 50,000.

What it tells them: **do not pool by default.** Pool when you have a measurement, or when you know the
count will be large and unbounded. On an old school laptop the threshold is lower — perhaps by a factor
of three or four — and the way to find out is to run the same page on one, which is a reasonable homework
task and a genuinely professional instinct.

Full marks require a number from their own machine and a stated rule for when to bother.

**E3.** Good answers do **not** scale everything linearly. The strongest version is roughly:

| | shake | particles | hitstop | flash | sound | number |
|---|---|---|---|---|---|---|
| light | 2 px | 4 | 0 | 60 ms | soft, high | small |
| medium | 5 px | 12 | 40 ms | 100 ms | solid | medium |
| kill | 12 px | 40 | 90 ms | 200 ms white | low, with noise | large, slower |

The insight worth most credit: **some effects should be absent entirely at the low end**, not merely
small. Hitstop at 10 ms is not a small hitstop, it is a jitter. Keeping an effect off until it matters is
what makes the big hit feel big — if everything shakes, nothing does.

**E4.** This is the most interesting question in the lesson.

Where the line is: juice should be **proportional and truthful**. It may exaggerate what happened; it must
not report something that did not happen.

Dishonest examples to look for in their answers:

- A big shake and flash on a hit that did **no damage** (blocked, immune, out of range) — the player
  believes they are winning and they are not. This is the clearest case.
- Hitstop on a miss.
- Damage numbers that are rounded up, or shown for damage that was then absorbed.
- A healing effect that looks identical to a damage effect.
- Juice that **hides information**: particles so thick the player cannot see the enemy, or shake so strong
  they cannot read their own health bar. This one is worth drawing out: it is dishonest by omission.

Full marks for a clear principle plus one specific example. Strong answers note that the test is "would a
player who could not see the numbers draw the right conclusion?", which is exactly what feedback is for.

---

## If you only mark one thing

Ask them to play their game with every effect off, then on. If they can tell you which effect they would
keep if they could only have one — and give a reason — they have understood that juice is a set of
deliberate choices rather than a pile of effects.
