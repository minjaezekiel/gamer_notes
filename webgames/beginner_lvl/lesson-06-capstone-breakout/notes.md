# Lesson 6 — Capstone: Breakout

> **Web Games · Beginner level · Lesson 6 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**Breakout**, by yourself. Multiple levels, a score, lives, and a link you can send to anyone.

```
╔══════════════════════════════════════╗
║ ███ ███ ███ ███ ███ ███ ███ ███      ║
║ ███ ███     ███ ███     ███ ███      ║
║ ███     ███ ███     ███     ███      ║
║                                      ║
║                ●                     ║
║            ▬▬▬▬▬▬▬▬                  ║
╚══════════════════════════════════════╝
 score 1240            lives ♥♥♥  level 2
```

This lesson teaches less new *syntax* than any other. Almost everything is something you already
know. What is new is **how to organise it** — and that turns out to be the harder skill.

## Where this fits

- **Back:** [lesson 5](../lesson-05-rules-score-and-feel/notes.md) finished Pong, with states,
  score and juice.
- **Forward:** the intermediate level, which starts by splitting this one big file into many.
- **Today:** two ideas that matter more than any individual game — **data instead of code**, and
  **decomposition**.

---

## The idea, in plain words

### Idea 1: levels are data, not code

Here is how most people first build a level of bricks:

```js
// DO NOT DO THIS
const brick1 = { x: 20,  y: 40, w: 60, h: 20, alive: true };
const brick2 = { x: 90,  y: 40, w: 60, h: 20, alive: true };
const brick3 = { x: 160, y: 40, w: 60, h: 20, alive: true };
// ...and 57 more lines
```

Three bricks is annoying. Sixty bricks is unmanageable. Three *levels* of sixty bricks is
impossible — and you cannot change the layout without editing code and risking breaking the game.

The alternative is to describe the level as **data**, and write code that reads it:

```js
// 0 = no brick, 1 = normal brick, 2 = tough brick (needs two hits)
const LEVEL_1 = [
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 2, 1, 1, 1, 1, 2, 1],
  [1, 1, 0, 1, 1, 0, 1, 1],
  [0, 1, 1, 1, 1, 1, 1, 0]
];
```

You can *see* the level in the code. You can change it by typing different digits. You can add a
fifth level by adding another array, and the game logic does not change at all.

This is one of the most important ideas in software:

> **Separate the thing that changes often (the levels) from the thing that changes rarely (the rules
> for playing them).**

Once a level is data, a hundred other things become easy: loading levels from a file, letting players
build their own, generating them randomly, emailing one to a friend. None of that is possible when a
level is sixty lines of code.

### Turning the grid into bricks

```js
function buildLevel(layout) {
  const bricks = [];

  // y is the ROW number, x is the COLUMN number.
  // Careful: it is layout[y][x], not layout[x][y]. The outer array holds rows,
  // so the first index chooses which row - which is y. Getting this backwards
  // gives you a level mirrored along the diagonal, and it is the single most
  // common bug in a first tile map.
  for (let y = 0; y < layout.length; y++) {
    for (let x = 0; x < layout[y].length; x++) {
      const kind = layout[y][x];
      if (kind === 0) { continue; }         // 0 means "no brick here"

      bricks.push({
        x: BRICK_LEFT + x * (BRICK_W + GAP),
        y: BRICK_TOP  + y * (BRICK_H + GAP),
        w: BRICK_W,
        h: BRICK_H,
        hitsLeft: kind,                     // 1 or 2
        alive: true
      });
    }
  }
  return bricks;
}
```

Two nested loops convert a picture made of digits into real objects with real positions. Read it
twice — this pattern appears in every tile-based game ever made.

### Idea 2: decomposition

Your Pong file is probably about 250 lines. Breakout will be 400 or more. At that size, "where is the
bit that does X?" becomes a real problem.

The fix is not clever. It is to make **every function do one thing**, and to name it after that
thing:

| Function | Does exactly |
|---|---|
| `buildLevel(layout)` | turn an array of digits into brick objects |
| `updateBall(dt)` | move the ball and bounce it off walls |
| `checkBrickCollisions()` | ball against bricks, and nothing else |
| `drawBricks()` | draw bricks, and nothing else |
| `loseALife()` | lose a life, and decide what happens next |

The test is simple: **if you cannot name a function without using the word "and", it is doing two
things.** Split it.

> **Why this matters more than it looks.** It is not about neatness. A 400-line `update()` function
> is a function you cannot hold in your head, so you cannot be confident about changing it, so you
> stop changing it, so the game stops improving. Decomposition is what keeps a project *fun to work
> on* after week two.

### The bug that will cost you twenty minutes

When the ball hits a brick, which way should it bounce?

The naive answer — always flip `speedY` — is wrong, and it shows the moment the ball clips a brick
from the side: it carries on sideways through the whole row.

The fix is to work out **which side** it came in through, by comparing how far it overlapped
horizontally with how far it overlapped vertically:

```js
function bounceOffBrick(brick) {
  // How much do the two boxes overlap on each axis?
  const b = ballBox();
  const overlapX = Math.min(b.x + b.w, brick.x + brick.w) - Math.max(b.x, brick.x);
  const overlapY = Math.min(b.y + b.h, brick.y + brick.h) - Math.max(b.y, brick.y);

  // The SMALLER overlap tells you which way it came in. If the ball has only
  // just poked in from above, the vertical overlap is tiny while the horizontal
  // overlap is large - so it arrived vertically, and should bounce vertically.
  if (overlapY < overlapX) {
    ball.speedY = -ball.speedY;
  } else {
    ball.speedX = -ball.speedX;
  }
}
```

This is worth drawing on paper before you write it.

### Removing bricks without breaking the loop

Two choices, and both are used in real games:

```js
// OPTION A: an "alive" flag. Nothing is ever actually removed.
if (brick.alive && boxesOverlap(ballBox(), brick)) {
  brick.alive = false;
}
// ...and skip dead ones everywhere: if (!brick.alive) continue;

// OPTION B: really remove it. Loop BACKWARDS, as in lesson 5.
for (let i = bricks.length - 1; i >= 0; i--) {
  if (boxesOverlap(ballBox(), bricks[i])) {
    bricks.splice(i, 1);
  }
}
```

Option A is simpler and faster when things come back (respawning enemies, a level restart). Option B
keeps the array small when they do not. Pick one deliberately and know why — that is the actual
skill here.

---

## The idea, in pictures

Open [the grids and flat arrays explainer](../../../shared/visualizers/tilemap-indexing.html).

**What to look for:** drag the marker and watch the index formula fill in with real numbers. Move
**one square right** and the index changes by 1; move **one square down** and it jumps by a whole
row. That is why `layout[y][x]` has y first: the first index is choosing which row to skip to.

Then open [the AABB explainer](../../../shared/visualizers/aabb-collision.html) again and drag the
box so it only just clips a corner. That is the case your brick-bounce code has to get right.

---

## The maths you just used

### Grid position to pixel position

```js
x: BRICK_LEFT + column * (BRICK_W + GAP)
```

Read it as: start at the left margin, then move across by one brick-plus-gap for every column. It is
the same arithmetic as working out where the eighth chair in a row of chairs goes.

### Which side did it hit? (overlap comparison)

The overlap on one axis is:

> **overlap = min(right edges) − max(left edges)**

Think about why: the overlapping region starts wherever the *rightmost* left edge is, and ends
wherever the *leftmost* right edge is. If that comes out negative, they are not overlapping at all —
which is the AABB test from lesson 4, written a different way.

Comparing the two overlaps tells you which direction the ball entered from, because it will have
barely poked in along the axis it was travelling.

---

## Break it on purpose

Use `code/02-breakout.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Swap `layout[y][x]` for `layout[x][y]` | | |
| Always flip `speedY` in `bounceOffBrick` | | |
| Remove the `alive` check in `drawBricks` but keep it in the collision | | |
| Add a row to `LEVEL_1` that is shorter than the others | | |
| Make `BRICK_W` 200 | | |
| Loop forwards while splicing bricks | | |

The first one is the single most common tile-map bug and you should see it at least once. The fourth
one is interesting: it works fine, and that tells you something about the loop you wrote.

---

## Think like an engineer

### Levels

1. Design a level that is **fun** rather than just full. What makes one brick layout better than
   another? Try: a gap down the middle, a tough row at the top, a shape.
2. Your layouts are 8 columns wide. What would you have to change to support a 20-wide level? If the
   answer is "nothing", your code is good. If it is "several numbers", find them and ask why.
3. **Design a format.** Invent a way of writing levels that also lets you say "this brick is red",
   "this brick drops a power-up", "this brick is unbreakable". What does your format look like, and
   what did it cost you in readability?

### Architecture

4. Your file is now 400+ lines. If you had to add a boss fight, where would the code go? If you cannot
   answer quickly, that is information about your structure, not about your memory.
5. List every global variable in your game. How many are there? Which ones could belong to an object
   instead? (This is exactly what the intermediate level starts with.)

### The hard one

6. You have built four games now, and all four had: a loop, a state machine, delta time, collision
   and a score. **Design the thing that is left over if you take the Breakout out of Breakout.**
   What would a reusable "game skeleton" contain, and what must always stay specific to one game?

That last question is what a game *engine* is, and your answer is more interesting than it sounds.
Engines are mostly made of people answering it badly and then fixing it.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Data-driven** | Behaviour described by data a non-programmer could edit, not by code. |
| **Decomposition** | Breaking one big job into small jobs that each do one thing. |
| **2-D array** | An array of arrays. `layout[y][x]` — row first, then column. |
| **Capstone** | A project that pulls together everything learned so far. |
| **Refactor** | Changing how code is organised without changing what it does. |

---

## Recap

- **Levels are data.** Separate what changes often from what changes rarely.
- `layout[y][x]`, not `layout[x][y]`. Rows first.
- **One job per function.** If you need "and" to name it, split it.
- Work out which **side** of a brick was hit by comparing the two overlaps.
- Choose deliberately between an `alive` flag and really removing things.
- You now know enough to build games nobody has taught you.

---

## Stretch goals

1. **Power-ups.** A brick drops something that widens the paddle, or gives a second ball.
2. **A level editor.** Click a grid to toggle bricks, then print the array to the console so you can
   paste it back into your code. This is a real tool and takes about 30 lines.
3. **Save the high score** with `localStorage`. Note that it can *throw* in a private window, so wrap
   it in `try`/`catch`.
4. **Tough bricks that look tough.** Make a two-hit brick change colour after the first hit. Without
   that feedback the player thinks the game is broken.
5. **Publish it.** Put it online and send someone the link. Instructions are in the `code/` folder.
6. **Make it your own.** Change the theme, the rules, the shape. Breakout with gravity. Breakout where
   the bricks move. Breakout for two players. This is the real stretch goal.

---

## Teacher notes

**Timing**

This lesson is mostly a long build. Resist the urge to teach.

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Show the finished Breakout, then show the `LEVEL_1` array next to it and change a few digits live. The connection lands instantly. |
| 10–25 | **Concept.** Levels as data, the nested loop, and the `[y][x]` trap. Then the one-job-per-function rule. |
| 25–35 | **Live-code** `buildLevel` only. Everything else they already know. |
| 35–45 | Break. |
| 45–135 | **Build.** This is a 90-minute build and they will need all of it. |
| 135–145 | **Show-and-tell.** Everyone demos. Protect this. |
| 145–150 | Where next: the intermediate level, and what it adds. |

**What usually goes wrong**

1. **`layout[x][y]`.** The level comes out mirrored along the diagonal, or crashes with
   "cannot read properties of undefined". Nearly everyone does this once. The tilemap visualizer is
   the fastest fix.
2. **The ball tunnels through a whole row of bricks.** They flip `speedY` unconditionally. Draw it on
   the board: ball clips a brick's left edge, bounces vertically, is still inside the next brick,
   repeat.
3. **Bricks vanish in pairs or threes.** One frame, several overlaps, all handled. Fix with a `break`
   after the first brick hit per frame, which is also what real Breakout does.
4. **Half the bricks never disappear.** Forward loop with `splice`. The lesson 5 bug returns. Point
   out that it is the same bug, in the same way you pointed out the wall-stick bug returning in
   lesson 4.
5. **Everything is one 300-line function.** The most common structural problem. Do not rewrite it for
   them. Ask them to find one thing, with a timer running, and let the difficulty make the argument.

**If you are running short on time** — give them `buildLevel` as a paste-in and one hard-coded level.
The brick-side bounce can be simplified to always flipping `speedY`; it is wrong, but it is playable,
and noting that it is wrong is itself worth something.

**For the student who finishes at minute 90** — the level editor (stretch 2) is the best use of their
time. It is a genuine tool, it is about 30 lines, and the student who builds one will supply levels to
the whole class, which is a good thing to have happen.

**Marking a capstone.** Do not mark on features. Mark on:
- Does it run without errors?
- Is the level data separate from the game code?
- Can they explain any function you point at?
- Did they change something to make it theirs?

The last one matters most. A technically weaker game with an original idea in it is a better outcome
than a flawless clone of the example.

**What to say at the end of the beginner course.** Put lesson 1's `03-the-loop.html` on the projector
next to today's Breakout. Same shape: state at the top, `update`, `render`, `requestAnimationFrame`.
Everything they built in two weeks went *inside* that structure, not around it. Then tell them the
truth — that this is also what the structure of a commercial game looks like, with a great deal more
inside each function and no extra ideas beyond the ones they already have.
