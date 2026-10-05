# Games with Python — Intermediate Level

**Python 3 + `pygame-ce` · 12 lessons · 4 weeks · 30 contact hours**

At beginner level you built Snake and Brick Breaker with `turtle` and `tkinter`, which come with
Python and need no installation. Those libraries were never meant for games, and you will have felt
it. This level hands you one that was.

By the end you will have an arcade shooter with sprites, animation, a scrolling world, sound, waves of
enemies, menus and a save file.

---

## Before you start

- Finish [`../beginner_lvl/`](../beginner_lvl/), or be comfortable with all of it: the game loop,
  delta time, lists of entities, collision tests, a state machine, and reading and writing a file.
- **Install `pygame-ce`.** Read [`INSTALL.md`](INSTALL.md) first — it is five minutes on a normal
  machine, and the rest of that page is for the machines that are not normal.

If you cannot install it on your school machine, read the last section of `INSTALL.md`. You have not
lost the course; you have lost one library, and the [`webgames/`](../../webgames/) track needs nothing
but a browser.

---

## The lessons

| # | Lesson | What you build | Core idea |
|---|---|---|---|
| 1 | [Hello pygame-ce](lesson-01-hello-pygame-ce/notes.md) | a window with a moving square | the **explicit loop** and the event queue |
| 2 | [Rects, images and the display](lesson-02-rects-images-and-the-display/notes.md) | a sprite you steer | `Rect`, `Surface`, `blit` |
| 3 | [Vector2](lesson-03-vector2/notes.md) | a ship that flies at any angle | **subtract, normalise, scale** |
| 4 | [Sprites and Groups](lesson-04-sprites-and-groups/notes.md) | a hundred things at once | pygame's **sprite system** |
| 5 | [Sprite animation](lesson-05-sprite-animation/notes.md) | a character that walks | **two clocks** |
| 6 | [Tilemaps](lesson-06-tilemaps/notes.md) | a world from a text file | **axis-separated collision** |
| 7 | [Cameras and scrolling worlds](lesson-07-cameras-and-scrolling-worlds/notes.md) | a world bigger than the window | **one subtraction** |
| 8 | [Sound and music](lesson-08-sound-and-music/notes.md) | a game you can hear | the **mixer**, and latency |
| 9 | [Platform physics](lesson-09-platform-physics/notes.md) | a platformer jump | gravity, and **coyote time** |
| 10 | [Enemies, waves and simple AI](lesson-10-enemies-waves-and-simple-ai/notes.md) | waves that get harder | **difficulty as data** |
| 11 | [Menus, scenes and save files](lesson-11-menus-scenes-and-save-files/notes.md) | title, pause, settings | a **scene stack**, and JSON |
| 12 | [**Capstone: an arcade shooter**](lesson-12-capstone-an-arcade-shooter/notes.md) | a complete game | all of it, assembled |

Each lesson folder holds `notes.md` (read this), `code/` (run these, in order),
`exercises.md` (the handout's source) and `solutions/` (for the teacher).

Printable handouts: [`handouts/`](handouts/).

---

## How to run an example

```bash
cd lesson-01-hello-pygame-ce/code
python3 01-a-window.py
```

Every example is a single file that runs on its own. Close the window, or press `Escape`, to quit.

**Every example also runs without a window**, which is how this repository checks itself:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy SELFTEST_FRAMES=150 python3 01-a-window.py
```

That is four visible lines in each example — see `INSTALL.md` — and it means every one of the 48
examples in this level is verified to run, not merely to parse.

---

## What is different about this level

**You are given a loop instead of being handed one.** `turtle.ontimer` and `tkinter.after` called
*your* function for you. pygame does not: you write `while running:` yourself, you ask for the events
yourself, and you decide when to draw. That is more code and far less mystery, and it is the same loop
the C++ and web tracks have had all along.

**No assets, on purpose.** This course ships no `.png` and no `.wav`, and no lesson downloads any.
Every sprite is drawn in code onto a `Surface`, which turns out to be a genuinely useful technique
rather than a workaround — see lesson 5 — and it means the course cannot break because a file is
missing.

**Three habits this level is really about:**

1. **Delta time, everywhere.** pygame will happily let you write a game that runs at a different speed
   on a different computer. Lesson 1 fixes that in the first twenty minutes and nothing afterwards
   forgets it.
2. **Separate what the game *is* from how it is *drawn*.** By lesson 11 the game logic does not import
   pygame's display at all, which is what makes the capstone testable.
3. **Measure instead of arguing.** Lesson 4 times a hundred sprites two ways. Lesson 10 tunes a
   difficulty curve by playing it, not by guessing.

---

## Cross-track callbacks

This level deliberately points at the other two. These are the moments worth stopping on:

| In | Points at | The observation |
|---|---|---|
| I-L1 | `webgames` B-L1 | `while running:` and `requestAnimationFrame` are the same loop. One calls you; in the other, you call. |
| I-L3 | `webgames` I-L2 | `pygame.Vector2` is the `Vec2` the web track writes by hand. Same methods, same traps, including the zero-length one. |
| I-L6 | `games_with_cpp` B-L3 | A tilemap and an ASCII screen buffer are the same grid with different paint. |
| I-L9 | `webgames` I-L12 | Coyote time and jump buffering, in Python. Identical idea, identical numbers. |
| I-L12 | all capstones | Three languages, one architecture: data, update, draw. |

---

## Verifying the code

From the repository root:

```bash
python3 tools/check_pygame.py              # run every example headlessly
python3 tools/check_pygame.py --only snake
bash tools/check_all.sh                    # everything, all tracks
```

`check_pygame.py` runs each example for 150 frames with SDL's dummy drivers, so a wrong argument
count, a missing method or a bad colour tuple is caught before a class ever sees it. It skips with a
message, rather than failing, if `pygame` is not importable.

---

## Next

[`../advanced_lvl/`](../advanced_lvl/) adds a fixed timestep, packages and a scene manager,
data-driven design, dataclasses, profiling, pathfinding, procedural generation, `pytest` on game logic,
and packaging the game for somebody else's computer.
