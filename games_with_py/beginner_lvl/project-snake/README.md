# Project: Snake, stage by stage

Snake does not arrive in one lesson. The pieces are built across lessons 1 to 4, and each stage adds
exactly one idea.

The staged files are **the lesson code examples themselves** — there are no duplicate copies here, so
nothing can drift out of sync with the lessons.

| Stage | What it adds | The file |
|---|---|---|
| **1. State and a loop** | a game with no graphics at all | [`lesson-01/code/03-adventure.py`](../lesson-01-the-loop-without-pixels/code/03-adventure.py) |
| **2. Drawing a grid** | grid-to-pixel conversion, reusable sprites | [`lesson-02/code/03-game-board.py`](../lesson-02-drawing-with-turtle/code/03-game-board.py) |
| **3. A loop that never waits** | `ontimer`, polled keys, movement | [`lesson-03/code/03-steerable-player.py`](../lesson-03-making-it-move/code/03-steerable-player.py) |
| **4. The game** | a list as the snake, growth, rules | [`lesson-04/code/02-snake.py`](../lesson-04-snake/code/02-snake.py) |

Before the graphical version, read
[`lesson-04/code/01-list-as-snake.py`](../lesson-04-snake/code/01-list-as-snake.py). It prints the
list at every step, with no window at all, so you can *watch* the snake move as data before you see
it as pixels. Run it first — the mechanic is much easier to believe when you can read it.

## Seeing exactly what each stage added

```bash
# stage 2 -> stage 3: what does it take to make a drawing move?
diff ../lesson-02-drawing-with-turtle/code/03-game-board.py \
     ../lesson-03-making-it-move/code/03-steerable-player.py
```

Before running a diff, write down what you *think* changed. The gap between your prediction and the
real answer is the most useful thing on this page.

## Suggested teaching use

- **Stage 1 → 2.** Ask what a text adventure and a drawn board have in common. The answer is the
  state and the loop; only the render job changed.
- **Stage 2 → 3.** The lesson is that `ontimer` is the same idea as the web track's
  `requestAnimationFrame`. Put the two side by side.
- **Stage 3 → 4.** Snake adds almost no new *technique*. What it adds is **rules** — and the
  observation that choosing a grid made collision detection disappear entirely.

## Build it yourself

The point is not to read these. Each lesson's `exercises.md` section D walks you through building
your own, and yours will be better because you will understand every line.
