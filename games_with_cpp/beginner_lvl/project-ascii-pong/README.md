# Project: ASCII Pong, stage by stage

Pong does not arrive in one lesson. Each stage adds exactly one idea, and the staged files are **the
lesson code examples themselves** — no duplicate copies, so nothing can drift out of sync.

| Stage | What it adds | The file |
|---|---|---|
| **1. Compile and loop** | the edit → compile → run cycle, a `while` loop | [`lesson-01/code/03-dice-duel.cpp`](../lesson-01-closer-to-the-metal/code/03-dice-duel.cpp) |
| **2. Data in one place** | `struct`, and references (`&`) | [`lesson-02/code/03-battle.cpp`](../lesson-02-a-game-is-data/code/03-battle.cpp) |
| **3. Pixels** | a screen buffer, `y*WIDTH+x`, frame timing | [`lesson-03/code/03-animated-dungeon.cpp`](../lesson-03-drawing-with-letters/code/03-animated-dungeon.cpp) |
| **4. Real-time input** | raw mode, `read_key()`, grid collision | [`lesson-04/code/03-maze-walker.cpp`](../lesson-04-input-and-movement/code/03-maze-walker.cpp) |
| **5. Many things** | `std::vector`, smooth `double` movement | [`lesson-05/code/02-ascii-pong.cpp`](../lesson-05-many-things-at-once/code/02-ascii-pong.cpp) |
| **6. A real project** | split files, a Makefile, a fixed timestep | [`lesson-06/code/`](../lesson-06-capstone-ascii-arcade/code/) |

## Seeing exactly what each stage added

```bash
# stage 3 -> stage 4: what does real-time input cost?
diff ../lesson-03-drawing-with-letters/code/03-animated-dungeon.cpp \
     ../lesson-04-input-and-movement/code/03-maze-walker.cpp

# stage 4 -> stage 5: what changes when there are MANY of something?
diff ../lesson-04-input-and-movement/code/03-maze-walker.cpp \
     ../lesson-05-many-things-at-once/code/02-ascii-pong.cpp
```

Before running a diff, write down what you *think* changed. The gap between your prediction and the
real answer is the most useful thing on this page.

## The one that is worth reading twice

Stage 5 → stage 6 is not a diff — it is a **reorganisation**. The same game, cut into six files.
Nothing about what the game *does* changed; what changed is where things live and who is allowed to
touch what.

Compare `02-ascii-pong.cpp` (one file, ~330 lines) with the capstone's `main.cpp` (~90 lines, and it
does nothing but timing). That difference is what the capstone lesson is about.

## Suggested teaching use

- **Stage 1 → 2.** Ask what happens if you add a third fighter to the dice game. Loose variables do
  not scale; a `struct` does.
- **Stage 2 → 3.** The first pixels. Point out that the screen buffer is a plain array and nothing
  more — this is the first time in the whole course the machinery is fully visible.
- **Stage 3 → 4.** Ask what had to change for the game to stop waiting. The answer is only the input
  function; the loop was already the right shape.
- **Stage 5 → 6.** Count the lines in `main.cpp`. That is the point of splitting a program up.

## Build it yourself

The point is not to read these. Each lesson's `exercises.md` section D walks you through building
your own.
