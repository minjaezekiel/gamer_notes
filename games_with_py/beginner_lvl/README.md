# Games with Python — Beginner Level

**Python · 6 lessons · 2 weeks · 15 contact hours**

Build a text adventure, Snake and Brick Breaker from nothing. **Standard library only** — there is
nothing to install, nothing to download, and nothing for a school network to block.

---

## What you need

Python **3.10 or newer**, and a text editor.

Check the machine is ready:

```bash
python3 --version
python3 -c "import tkinter; print('tkinter ok')"
```

Both of those must work. `turtle` and `tkinter` ship with Python, so there is normally nothing to do
— but on some Linux installs `tkinter` is a separate package (`sudo apt install python3-tk`). That is
the only setup surprise in this whole track, and it is worth finding before lesson 1 rather than
during lesson 5.

**Run your programs from a terminal** — `python3 myfile.py`. Some editors swallow the turtle window,
which looks exactly like a broken program.

---

## The lessons

| # | Lesson | What you build | Core idea |
|---|---|---|---|
| 1 | [The loop without pixels](lesson-01-the-loop-without-pixels/notes.md) | a text adventure | **state**, a loop, and a world as **data** |
| 2 | [Drawing with turtle](lesson-02-drawing-with-turtle/notes.md) | a game board and sprites | coordinates, and one function drawing a hundred things |
| 3 | [Making it move](lesson-03-making-it-move/notes.md) | a player you steer | **a loop that never waits** |
| 4 | [Snake](lesson-04-snake/notes.md) | **Snake** | a **list** as a game object; grids remove collision bugs |
| 5 | [A real window: tkinter](lesson-05-a-real-window-tkinter/notes.md) | Catch the Falling Fruit | **retained mode**, and y pointing **down** |
| 6 | [Capstone: Brick Breaker](lesson-06-capstone-brick-breaker/notes.md) | **Brick Breaker** | **classes**, levels as data, saving to a file |

Each lesson folder contains:

```
notes.md        the lesson - read this first
code/           runnable examples, numbered in teaching order
exercises.md    practice questions and the build task
solutions/      worked answers (teacher-facing)
```

Printable handouts are in [`handouts/`](handouts/).

Lessons 4 and 6 also have **runnable logic tests** in their `solutions/` folders. They work only
because the games keep their logic separate from their drawing — which is a practical reason for a
rule the course keeps repeating, not just a tidiness one.

---

## Three drawing systems in two weeks

This track deliberately changes drawing system twice:

| Lessons | System | `(0,0)` | y grows | Style |
|---|---|---|---|---|
| 1 | `print()` | — | — | text |
| 2–4 | `turtle` | the **middle** | **up** | immediate: you redraw everything |
| 5–6 | `tkinter` | **top-left** | **down** | retained: the canvas remembers shapes |

That is not padding. The point is that **the structure never changes** — same loop, same state, same
input pattern — while the thing underneath changes completely. By lesson 6 you will have adapted to
three different drawing systems, each in a single lesson, and that skill is worth more than any one
of them.

Turtle is the odd one out on coordinates. Everything else in the world — tkinter, pygame, raylib, the
web canvas, your phone — puts `(0,0)` top-left with y growing down. Lesson 2 warns you; lesson 5
collects.

---

## The visualizers

Nine animated explainers in [`../../shared/visualizers/`](../../shared/visualizers/index.html). They
work offline — double-click `index.html`.

| Lesson | Open these |
|---|---|
| 1 | [the game loop](../../shared/visualizers/game-loop.html) |
| 2 | [coordinates](../../shared/visualizers/coordinates.html) — turtle is the left-hand grid |
| 3 | [the game loop](../../shared/visualizers/game-loop.html), [delta time](../../shared/visualizers/delta-time.html) |
| 4 | [grids and flat arrays](../../shared/visualizers/tilemap-indexing.html), [box collision](../../shared/visualizers/aabb-collision.html) |
| 5 | [coordinates](../../shared/visualizers/coordinates.html) — now the **right-hand** grid, [gravity](../../shared/visualizers/gravity-and-velocity.html) |
| 6 | [grids and flat arrays](../../shared/visualizers/tilemap-indexing.html), [box collision](../../shared/visualizers/aabb-collision.html) |

Press **Step 1 frame** rather than Play, at least the first time. Watching an animation shows you a
result; stepping through it shows you a mechanism.

---

## Snake, stage by stage

[`project-snake/README.md`](project-snake/README.md) maps each stage to the lesson file that builds
it, and shows how to `diff` consecutive stages.

---

## What you will know at the end

- What a game actually *is*: state, a loop that changes it, and output that shows it. Only the last
  part needs graphics.
- Why a real-time loop **never waits** for the player, and what that makes possible.
- Why `global` behaves the way it does, and why Python's choice is deliberate.
- How a list becomes a snake, and why choosing a grid removed every collision bug.
- The difference between retained and immediate drawing, and when each one wins.
- When a class earns its place over a dictionary — and when it does not.
- How to save data so it survives the program closing, and why the error handling is part of the
  feature.

---

## Where next

[`../intermediate_lvl/`](../intermediate_lvl/) — 12 lessons over 4 weeks with `pygame-ce`
(`pip install pygame-ce`). Sprites, spritesheets, tilemaps, cameras, sound, platform physics, enemy
AI, scenes and save files, finishing with an arcade shooter.

If you would rather see the same ideas in another language,
[`../../webgames/beginner_lvl/`](../../webgames/beginner_lvl/) and
[`../../games_with_cpp/beginner_lvl/`](../../games_with_cpp/beginner_lvl/) teach the same concepts in
the same order. The second track runs much faster, because the ideas are already in place — and most
students say the second time is when they genuinely understood the first.
