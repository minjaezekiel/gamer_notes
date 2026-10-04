# Lesson 5 — Solutions and marking notes

---

## Section A

**A1.** [3] An **array** has a size fixed when the program is compiled; a **vector** can grow and
shrink while it runs. Two marks. One for an example where you must have a vector: particles, bullets,
enemies, dropped items — anything whose count depends on what happens in the game.

**A2.** [3] Erasing element `i` shifts everything after it **down one place**, so the next iteration's
`i++` steps over the item that just moved into position `i`. Two marks. Going backwards, a removal can
only affect indexes you have already passed. One mark.

Without it, roughly **half** of what should be removed survives.

**A3.** [3] `size()` returns an **unsigned** type, which cannot hold a negative number. Two marks.

Without the cast, when the vector is empty `size() - 1` wraps round to about 18 quintillion, so
`i >= 0` is always true and the loop runs essentially for ever — while reading far outside the
vector. One mark.

**A4.** [2] Because the ball moves a fraction of a square per frame. With an `int` it would either not
move at all (the fraction truncated to 0) or jump a whole square at a time. The simulation is
continuous even though the screen is not.

**A5.** [2] **3**. No — it **truncates**, throwing the fraction away. `(int)3.9` is 3 and so is
`(int)3.1`.

---

## Section B

**B1.** [4] **`[10, 20, 40, 60]`** is left. Walk it through:

| i | vector before | erases | after | next i |
|---|---|---|---|---|
| 0 | 10 20 30 40 50 60 | — | — | 1 |
| 1 | 10 20 30 40 50 60 | — | — | 2 |
| 2 | 10 20 30 40 50 60 | 30 | 10 20 40 50 60 | 3 → **40 skipped** |
| 3 | 10 20 40 50 60 | 50 | 10 20 40 60 | 4 → size is 4, loop ends |

So 40 and 60 survive. Two marks for the result, two for the explanation.

**B2.** [3] `v.size()` is 0, and it is **unsigned**, so `0 - 1` wraps round to the largest possible
value (about 1.8 × 10¹⁹). `i >= 0` is **always true** for an unsigned type, so the loop never ends —
and it reads `v[huge]`, far outside the vector.

The program hangs, and may crash or corrupt memory on the way.

**B3.** [3] With `PADDLE_HEIGHT = 4`: `4 / 2.0 = 2.0` and `4 / 2 = 2`, so **both give 8.0**. The bug
is invisible.

With `PADDLE_HEIGHT = 5`: `5 / 2.0 = 2.5` giving **8.5**, but `5 / 2 = 2` (whole-number division)
giving **8.0**. Now they differ by half a square.

Two marks for the numbers, one for the observation that **the bug hides at even heights** — which is
exactly why it survives testing and then appears when someone changes a constant.

**B4.** [4] Both are drawn in **column 0**, because `(int)` truncates. Two marks.

Crossing from 0.0 to 2.0, the player sees the ball sit in column 0 for a while, jump to column 1,
sit there, then jump to column 2 — so it appears to move in steps rather than smoothly. One mark.

**Is it a bug?** No — it is the screen being coarse, not the physics being wrong. The simulation is
perfectly smooth; the display has only 46 columns. One mark. (Strong answers notice this is exactly
what pixels do too, just at a finer grain.)

---

## Section C

**C1.** [4] `particles.size()` is unsigned, so `size() - 1` is computed as **unsigned** before being
assigned to the `int i`. When the vector is empty that is a huge number, which converts to `i` in an
implementation-defined way — and in practice the loop runs enormously long, reading far out of
bounds.

The warning was about **comparing or converting signed and unsigned values**. `-Wall` tells you about
this precisely because it is so often a real bug. Two marks for the diagnosis, one for the warning,
one for the fix: `(int)particles.size() - 1`.

**Point out that the compiler told them in advance and they ignored it.**

**C2.** [3] The **forward loop with erase**. Two marks.

One mark for where they have met it: the web track's particles (lesson 5), Breakout's bricks (lesson
6), and the Python track's falling fruit (lesson 5). This is the **fourth** appearance.

Say out loud that it is not a C++ problem or a Python problem. It is a *lists* problem, and it will
follow them into every language they ever use.

**C3.** [4] Erasing from a vector while iterating it with a **range-based `for`** invalidates the
iterator the loop is using. The behaviour is **undefined** — the standard says nothing about what
happens.

Why the symptoms vary, two marks: undefined behaviour means the compiler and library may do anything.
Whether it crashes depends on whether the vector had to reallocate, what was in the memory afterwards,
the optimisation level, and the library implementation. It commonly "works" while the vector is small
and fails once it has grown — which is the worst possible failure mode, because the bug is invisible
in testing.

Two marks for a fix: a backwards indexed loop, or the erase-remove idiom.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 1 — insist on doing it wrong first.** Printing `[10, 20, 40, 60]` and seeing which items
survived takes thirty seconds and makes the bug concrete. Students who have seen their own output do
not forget it.

**Checkpoint 3 — the opponent must be beatable.** Expect students to write a perfect tracker, discover
the game is unwinnable, and conclude their code is broken. It is not: it is a correct implementation
of a bad design. Good moment to repeat that "works correctly" and "good" are different things.

**Checkpoint 4 — watch for `/ 2`.** With `PADDLE_HEIGHT = 4` it is invisible. Suggest they try 5 and
see whether anything changes.

**Checkpoint 5.** The two things to check are the backwards loop and the `(int)` cast. Both are
visible at a glance.

---

## Section E — marking notes, not answers

**E1.** When a vector runs out of room it allocates a bigger block and copies everything across. It
grows geometrically (usually doubling), so this happens rarely — but when it does, it costs
proportional to the current size.

For a game spawning particles every frame, the copies happen during play, which can cause an
occasional frame to take noticeably longer. That is worse than being uniformly slower: a stutter is
more noticeable than a consistent cost.

`reserve(n)` allocates room for `n` items **up front**, so no reallocation happens until you exceed
it. Call it when you know roughly how many you will need — at the start of the game, or when a level
loads.

The honest follow-up, which is stretch goal 4: for a few hundred particles the difference is usually
**not measurable**. A student who reserves and then measures no improvement has learned more than one
who applies it on faith.

**E2.** What you would gain: one loop updates everything; adding a new kind of thing needs no new
variable; you could sort them, count them, or save them all with one piece of code.

What gets harder: every entity needs a `type` field and the update becomes a `switch`; the ball and
the paddle need different data, so either the struct holds every field any entity might need (wasteful
and confusing) or you need something more advanced; and `ball.x` becomes `entities[0].x`, which says
much less to a reader.

The mature answer is **"it depends on how many kinds there are"**. With three fixed things, named
variables are clearer. With fifty of various kinds, a collection wins. Students who say "it depends,
and here is what on" have answered best.

(This question is the opening of the advanced level's ECS lesson. Do not resolve it.)

**E3.** Expected approaches:

| Approach | Trade-off |
|---|---|
| A `type` field plus a `switch` in the update | simple; grows awkward with many types |
| Fields for the behaviour: `gravity`, `drag`, `grow_rate` | data-driven and flexible; every particle carries fields it may not use |
| A function pointer per particle | very flexible; harder to read and slower |
| One vector per kind | fast and clear; more code, and ordering between kinds is lost |

The second is the one to praise: give the particle a `gravity` value, and sparks use `+9.0`, smoke
uses `-2.0`, and a shockwave uses `0.0` with a growing size. **One system, three behaviours,
expressed as data** — which is the same data-driven idea as levels-as-arrays, applied to behaviour.

**E4.** The key point is in the question: **write your guess first, then check it.** Programmers'
guesses about where time goes are famously wrong.

How to find out, in rough order of effort:
- **Time sections by hand** with `steady_clock` around the update and the draw separately, and print
  the numbers.
- **Comment things out** and see what the frame time does.
- **Use a profiler** — `perf` on Linux, Instruments on macOS, or the one in Visual Studio.

Common guesses, and what is usually actually true: students guess the particle maths. In this program
it is far more likely to be the **drawing** — building and printing a large string every frame — or
the vector erases shifting thousands of elements.

The rule worth stating: **measure before you optimise.** It is one of the few pieces of advice in
programming that is close to universal.

---

## Teacher note: the fourth appearance

Put this on the board at the end:

| Track | Lesson | What was being removed |
|---|---|---|
| Web | 5 | particles |
| Web | 6 | bricks |
| Python | 5 | falling fruit |
| C++ | 5 | particles |

Same bug, four times, three languages. Ask the class what that tells them.

The answer you want is that it is not a language feature they are failing to learn — it is a
consequence of how lists work, and it will be waiting for them in C#, Java, Rust, and whatever
replaces them. Recognising a bug they have seen before, in new clothes, is one of the most valuable
things they will take from this course.
