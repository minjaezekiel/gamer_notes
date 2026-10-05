# Lesson 12 — Capstone: A Platformer

> **Web Games · Intermediate level · Lesson 12 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A platformer that **feels good to jump in**. Not just a game where a square can get off the ground — a
game where the jump is forgiving in the five specific ways that every well-regarded platformer is
forgiving, and where you can say what each of those five things does and why.

```
   ┌──────────────────────────────────────────────┐
   │  ·  o            ▂▂▂▂▂                   ▛▀▀ │
   │        ☺                      ◆              │
   │   ▀▀▀▀▀▀▀▀      o        ▀▀▀▀▀▀▀▀▀      ▀▀▀▀ │
   │                     ▂▂▂▂▂                    │
   │  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ │
   └──────────────────────────────────────────────┘
      coyote time · jump buffer · variable height
      apex hang  · fast fall   · one-way platforms
```

Everything in it is something you built in the last eleven lessons. Today is about **assembling** it,
and then about the part nobody teaches: **tuning it by watching somebody else play.**

## Where this fits

- **Back:** all of it. Lesson 1's modules, lesson 2's vectors, lesson 3's acceleration, lesson 4's
  sprites, lesson 5's tile collision, lesson 6's camera, lesson 7's scenes, lesson 8's sound, lesson 9's
  juice, lesson 10's enemies, lesson 11's saving.
- **Forward:** the advanced level takes the same game and makes it correct under stress — a fixed
  timestep, spatial partitioning, pathfinding, profiling, and shipping it to other people.
- **A promise kept:** beginner lesson 3 ended with a question you were asked to try to invent — *"a
  player presses jump a few milliseconds before landing and nothing happens; how would you fix it?"*
  Today you find out that it has a name, and that you were probably close.

---

## The idea, in plain words

### A jump is not one number

Here is the jump everybody writes first, and it is correct:

```js
if (jumpPressed && player.onGround) {
  player.vy = -JUMP_SPEED;
}
```

It works. It is also the thing that separates a student platformer from a good one, because real
platformers do **five** things on top of it. None of them is complicated, and each of them exists to fix
a specific moment where the game would otherwise feel as though it had ignored the player.

### 1. Variable jump height

Tap for a small hop, hold for a full jump. One `if`:

```js
/* Let go early and the upward velocity is CUT, not stopped. The player is still
   rising, just less. Stopping it dead feels like hitting something. */
if (!jumpHeld && player.vy < 0) {
  player.vy = player.vy * 0.45;
}
```

The whole of a platformer's control depth is in that line. Without it, every jump is the same height and
the player has exactly one thing they can do.

### 2. Coyote time

The player runs off a ledge and presses jump 50 ms later. They *meant* to jump from the ledge. The game
says no, because `onGround` became false.

```js
const COYOTE_TIME = 0.1;        // 100 ms. Six frames.

/* Instead of asking "am I on the ground?", ask "was I on the ground recently?" */
if (player.onGround) { player.coyote = COYOTE_TIME; }
else { player.coyote -= dt; }

if (jumpPressed && player.coyote > 0) {
  player.vy = -JUMP_SPEED;
  player.coyote = 0;            // cancel it, or they get a second jump
}
```

The name comes from cartoon coyotes, who hang in the air for a moment after running off a cliff. Players
never notice this is there. They notice its absence, and describe it as the game being "stiff" or
"unfair" without being able to say why.

### 3. Jump buffering

The mirror image, and the answer to the question from beginner lesson 3. The player presses jump 50 ms
*before* landing. The press is thrown away, they land, and nothing happens.

```js
const JUMP_BUFFER = 0.12;

if (jumpPressed) { player.jumpBuffer = JUMP_BUFFER; }
else { player.jumpBuffer -= dt; }

/* Now the jump is not triggered by the press. It is triggered by the two
   conditions both being true, in either order. */
if (player.jumpBuffer > 0 && player.coyote > 0) {
  player.vy = -JUMP_SPEED;
  player.jumpBuffer = 0;
  player.coyote = 0;
}
```

Read those two together: a press remembers itself for 120 ms, and the ground remembers itself for
100 ms. The jump happens when both memories overlap. That is the whole trick, and the two features are
the same idea pointing in opposite directions.

> **Both of these are "remember an input for a little while".** Once you see that, a whole class of
> responsiveness problems has one answer — and it is the same answer as the input buffering in fighting
> games.

### 4. Apex hang time

Real jumps feel best when the player has a moment of control at the top. Lower the gravity when they are
moving slowly vertically:

```js
/* Near the top of the jump, |vy| is small. Weakening gravity there stretches the
   apex without changing the height or the total time much. */
const nearApex = Math.abs(player.vy) < APEX_THRESHOLD;
const gravity = nearApex ? GRAVITY * 0.55 : GRAVITY;
player.vy += gravity * dt;
```

This one is invisible and powerful. Nobody can tell you it is there; everybody can tell when it is not.

### 5. Fast fall

Falling at the same rate you rose feels floaty. Platformers almost always fall faster than they rise:

```js
const gravity = player.vy < 0 ? GRAVITY_UP : GRAVITY_DOWN;   // DOWN is bigger
```

A ratio of about 1.5 to 2 is normal. This is the single cheapest improvement in the list.

### Putting the numbers in terms you can think about

`JUMP_SPEED = 520` means nothing to anybody. **Jump height** and **time to the top** are things you can
picture, and the physics converts between them:

```
height  = v² / (2g)                  so   v = √(2 · g · height)
time up = v / g
```

So "I want a jump three tiles high, taking about a third of a second to the top" is a *design*
statement, and these two lines turn it into numbers:

```js
const JUMP_HEIGHT = TILE * 3;        // what you actually care about
const TIME_TO_APEX = 0.33;

/* Work the physics backwards from the design. Now changing the jump height does
   not require re-tuning gravity, and the two numbers in the code are the two
   numbers you were thinking about. */
const GRAVITY_UP = (2 * JUMP_HEIGHT) / (TIME_TO_APEX * TIME_TO_APEX);
const JUMP_SPEED = GRAVITY_UP * TIME_TO_APEX;
```

That is a small thing with a large consequence: **tune in the units of the design, not the units of the
engine.**

### One-way platforms

Solid from above, pass-through from below. Lesson 5 asked you to design this; here it is:

```js
/* The test needs two things the ordinary one does not: which way we are moving,
   and where we WERE before the move. Without the previous position, the player
   snaps to the top of a platform they are halfway through. */
if (tile.oneWay) {
  const topEdge = row * TILE;
  const wasAbove = previousBottom <= topEdge + 1;
  if (!(movingDown && wasAbove)) { continue; }     // not solid: ignore it
}
```

### Moving platforms, and the thing that goes wrong

Move the platform, then move the player, and the player sinks through a rising platform or is left
behind by a falling one. The fix is an ordering rule and a carry:

```js
/* 1. move the platforms FIRST
   2. then carry any passenger by the same amount
   3. then run the player's own movement and collision */
for (const p of platforms) {
  const dx = p.vx * dt, dy = p.vy * dt;
  p.x += dx; p.y += dy;
  if (player.ridingPlatform === p) { player.x += dx; player.y += dy; }
}
```

`ridingPlatform` is set by the downward collision test — the same test that sets `onGround`. That test is
doing a lot of work by now, which is a sign it was the right place to put it.

### The part that is not code: playtesting

You have now built something. Here is how to find out whether it is any good, and it is not by playing it
yourself — you know where everything is and you have practised every jump a hundred times.

**Watch somebody else play it, and do not speak.**

That is the whole technique and it is extremely hard to do. Rules:

- Say only "here, have a go". No instructions, no controls, nothing.
- **Write down every moment they are confused**, not what they say about it afterwards.
- When they get stuck, say nothing. The urge to help is enormous. Helping destroys the information.
- Afterwards, ask what they were *trying* to do, never whether they liked it.

Three things you will learn in five minutes that you could not learn in an hour of your own play: which
jump is too hard, which instruction you forgot to give, and which thing you thought was obvious is
invisible.

Then **measure**. `code/04-death-heatmap.html` records where every death happened and draws them. Twenty
deaths in one spot is not a difficulty curve; it is a design problem, and you can see it at a glance.
That is the difference between "this bit feels too hard" and "forty per cent of all deaths are at this
one jump".

### What "done" means for a small game

You will not finish today. Nobody does. So decide what finished means before you run out of time, and
the honest list is short:

- [ ] It starts from a title screen and can be restarted without reloading the page.
- [ ] It can be paused.
- [ ] It is winnable, and somebody other than you has won it.
- [ ] It does not crash when storage is blocked, when the window is resized, or when the tab is hidden.
- [ ] The controls are discoverable without being told.
- [ ] One complete level, polished, rather than four unfinished ones.

That last one is the hardest and the most important. **One good level beats four sketches**, every time.

---

## The idea, in pictures

Open [gravity, velocity, position](../../../shared/visualizers/gravity-and-velocity.html) and step a jump
frame by frame. Watch `vy` cross zero at the apex — that is the moment apex hang time acts on, and
seeing it as a single frame makes the feature concrete rather than magical.

Then open [tile collision, one axis at a time](../../../shared/visualizers/tile-collision.html) and watch
the vertical correction fire. **That one test is what sets `onGround`, which starts the coyote timer,
which is what makes the jump feel fair.** Five lessons of this course meet in that one `if`.

---

## The idea, in code

1. `code/01-the-jump.html` — all five refinements on switches, with every timer drawn on screen. Turn
   them all off, play, then add them one at a time. This is the most important file in the level.
2. `code/02-platforms.html` — one-way platforms and moving platforms, with the "move platforms first"
   rule demonstrated by breaking it.
3. `code/03-the-whole-game/` — the complete platformer, as modules. Eleven small files, each of which is
   a lesson from this level. Needs a local server (lesson 1).
4. `code/04-death-heatmap.html` — the same level, recording where you die, with a heatmap and the
   statistics. Play it ten times and look at the picture.

---

## The maths you just used

**1. The two jump equations.** With a constant acceleration `g`, a body launched upwards at speed `v`
reaches

```
height  = v² / (2g)
time up = v / g
```

Both come from the same two lines of code you have been writing since the beginner level —
`v += g·dt` and `y += v·dt` — and they let you work **backwards** from a height you want to a speed you
need. Being able to go backwards is what makes a design tunable.

**2. Rearranging a formula.** `height = v²/(2g)` becomes `v = √(2·g·height)`. This is the first time in
this course that rearranging an equation has done something immediately useful, and it is worth doing on
the board: multiply both sides by `2g`, then take the square root.

**3. Asymmetric gravity is still just a number.** Using a different `g` going up and coming down breaks
the tidy formulas above — the jump is no longer symmetrical, so the fall takes less time than the rise.
That is not a problem, it is the point, and it is worth noticing that games are allowed to use physics
that is *wrong* if the result is better. Honesty about this matters: your game is not a simulation.

**4. Two overlapping intervals.** Coyote time and jump buffering are two countdowns, and the jump happens
when both are positive at once. That is an intersection of two time windows, which is a genuinely
different shape of thinking from "when the key is pressed" — and once a student sees it, they can invent
the next four features in this family themselves.

---

## Break it on purpose

Use `code/01-the-jump.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Turn all five refinements off and play for two minutes | | |
| Coyote time 0.5 s | | |
| Forget `player.coyote = 0` after jumping | | |
| Jump buffer 1.0 s | | |
| Variable jump: set `vy = 0` on release instead of `vy *= 0.45` | | |
| `GRAVITY_DOWN` smaller than `GRAVITY_UP` | | |
| Apex threshold larger than `JUMP_SPEED` | | |
| In `02`, move the player before the platforms | | |
| One-way platforms with no "was above" test | | |

Coyote time at 0.5 s is the most instructive: the player can jump half a second after walking off a
cliff, which looks like flying. Somewhere between 0.08 and 0.15 is invisible and right, and finding that
edge yourself is the lesson.

---

## Think like an engineer

1. Coyote time and jump buffering are both "remember an input for a short while". Name two **other**
   places in a game where that same idea would help. (You met one in lesson 7 without knowing it.)
2. Your jump is tuned in `JUMP_HEIGHT` and `TIME_TO_APEX` rather than `JUMP_SPEED` and `GRAVITY`. What
   else in your game would be better expressed in the units of the design rather than the units of the
   engine? Give three examples.
3. **Design something.** A new mechanic for your platformer — a dash, a wall jump, a double jump, a
   grapple. Before writing any of it: what *problem* does it solve for the player, what does the level
   design have to do to make it worth having, and what does it break about the levels you already have?
4. **The hard one.** You watched somebody play and they died eleven times at the same jump. There are at
   least five different causes with five different fixes: the jump is too long, the landing is not
   visible, the run-up is too short, the controls were never explained, or the penalty for failure is too
   high. How would you tell which one it is? What would you change *first*, and how would you know
   whether it worked?

---

## Vocabulary

| Word | What it means |
|---|---|
| **Coyote time** | A short window after leaving the ground during which a jump still works. |
| **Jump buffering** | A short window before landing during which a press is remembered. |
| **Variable jump height** | Cutting upward velocity when the button is released. |
| **Apex hang time** | Reduced gravity near the top of a jump. |
| **Fast fall** | Higher gravity coming down than going up. |
| **One-way platform** | Solid from above, pass-through from below. |
| **Riding** | Being carried by a moving platform. |
| **Playtest** | Watching somebody else play, in silence. |
| **Heatmap** | A picture of where something happened a lot. Deaths, usually. |
| **Vertical slice** | One part of a game, finished to the standard the whole thing would be. |

---

## Recap

- A jump is **six** things: the impulse, variable height, coyote time, jump buffering, apex hang, and
  fast fall. Each fixes one moment where the game would otherwise seem to have ignored the player.
- Coyote time and jump buffering are the **same idea in opposite directions** — remember an input
  briefly — and the jump fires when both windows overlap.
- **Tune in the units of the design.** Jump height and time to apex, not speed and gravity.
- Move **platforms first**, then carry passengers, then move the player.
- `onGround` comes from the downward collision test, and five lessons of this course meet in that one
  `if`.
- **Watch somebody else play and say nothing.** Then measure where they die.
- One finished level beats four sketches.

---

## Stretch goals

1. **A wall jump.** Needs a "touching a wall" test, a short window after leaving it (coyote time again),
   and a velocity that pushes away as well as up.
2. **A dash with a cooldown**, using lesson 9's tweens for the trail and lesson 3's dash notes.
3. **Record and replay a run.** Store the input state for every frame, then play it back. If your game is
   deterministic it will replay exactly; if it is not, you have learned something important about it —
   and the advanced level's fixed timestep is the fix.
4. **A level editor** in the browser, writing your level back out as text to paste into the code.
5. **Ship it.** Put your folder on a free static host, send the link to five people, and write down the
   first thing each of them did. That list is the most valuable document you will produce in this level.

---

## Teacher notes

**Timing**

This lesson is different: it is mostly build time, and the hour at the end is a playtest session that is
worth protecting from overrunning code.

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** `01-the-jump.html` with all five switches off. Let a student play. Then switch them on one at a time without saying what they do, and ask after each what changed. Most will not be able to say — which is exactly the point about coyote time. |
| 10–25 | **Concept.** The five refinements on the board, each as the moment it fixes. Then the two jump equations, and work `GRAVITY` backwards from a height. |
| 25–40 | **Live-code** coyote time and jump buffering together, as two countdowns and one overlap test. |
| 40–50 | Break. |
| 50–110 | **Build.** Their own platformer. Tell them firmly: **one level, finished.** |
| 110–140 | **Playtest in pairs.** Swap machines. The player says nothing except what they are trying to do; the author says nothing at all, and writes down every moment of confusion. Enforce the silence — it is the whole exercise and students find it genuinely difficult. |
| 140–150 | Share-outs: each author names **one** thing they will change, and why. |

**The playtest is the lesson.** If you cut anything, cut code, not this. Students have never seen somebody
else play their game, and the experience changes how they build for good.

**What usually goes wrong**

1. **Double jumps appear by accident.** `coyote` is not reset after jumping, so the window is still open
   on the next frame. Very common.
2. **Coyote time set far too high**, producing flight. 0.1 s is right; 0.3 s is visibly wrong.
3. **Jump buffering retriggers.** The buffer is not cleared, so a held jump bounces them repeatedly.
   Reset it when the jump fires, and require a fresh press.
4. **Variable jump feels like hitting a ceiling.** They set `vy = 0` instead of multiplying it.
5. **Sinking through moving platforms.** The player is moved before the platforms.
6. **One-way platforms snap the player to the top** when jumping up through them. Missing the "was above"
   test.
7. **Four unfinished levels.** Expect this, and head it off at the start of the build block rather than at
   the end.
8. **Nobody writes anything down during the playtest**, and the information evaporates. Hand out paper.

**For the student who finishes early** — stretch goal 3 (record and replay) is the most interesting,
because it either works perfectly or reveals that their game is not deterministic, and both outcomes teach
something. Stretch goal 5 (actually ship it) is the most valuable.

**The point to land at the end of the level, not just the lesson:** twelve lessons ago a ball bounced
inside a box. The difference between that and this is not that they learned more syntax. It is that they
now build things in **parts that each do one job**, tune them in **numbers that mean something**, and
check their work by **watching a person and measuring what happened** rather than by guessing. That is
what the rest of the course is for, and it is also what the job is.
