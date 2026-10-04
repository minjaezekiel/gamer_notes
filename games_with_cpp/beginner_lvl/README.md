# Games with C++ — Beginner Level

**C++ · 6 lessons · 2 weeks · 15 contact hours**

Build a dice game, a battle, an animated dungeon, a maze, ASCII Pong and a complete arcade game —
**in the terminal, with a compiler and nothing else.** No libraries, no linker flags, no setup beyond
the compiler itself.

---

## What you need

A C++17 compiler and a text editor. Check it works **before lesson 1**:

```bash
clang++ --version     # or: g++ --version
```

| System | How to get one |
|---|---|
| **macOS** | `xcode-select --install` |
| **Linux** | `sudo apt install g++` (or your distribution's equivalent) |
| **Windows** | MSYS2 or WSL are the least painful. Visual Studio works but hides the compile command, which is one of the things being taught. |

**Run the games from a real terminal**, not an editor's built-in console. From lesson 4 onwards the
games read individual keystrokes, and many IDE consoles do not pass those through — your perfectly
correct program will appear dead.

Every example compiles with exactly this and nothing more:

```bash
clang++ -std=c++17 -Wall file.cpp -o file
./file
```

**Compile, then run. Two steps, every time.**

---

## The lessons

| # | Lesson | What you build | Core idea |
|---|---|---|---|
| 1 | [Closer to the metal](lesson-01-closer-to-the-metal/notes.md) | a dice duel | what **compiling** is, and why games use C++ |
| 2 | [A game is data](lesson-02-a-game-is-data/notes.md) | a turn-based battle | **`struct`**, and `&` — copies vs the real thing |
| 3 | [Drawing with letters](lesson-03-drawing-with-letters/notes.md) | an animated dungeon | a **screen buffer**, and `y*WIDTH+x` |
| 4 | [Input and movement](lesson-04-input-and-movement/notes.md) | a maze walker | input that **does not wait** |
| 5 | [Many things at once](lesson-05-many-things-at-once/notes.md) | **ASCII Pong** | **`std::vector`**, and smooth movement |
| 6 | [Capstone: ASCII arcade](lesson-06-capstone-ascii-arcade/notes.md) | **ASCII Invaders** | **split files**, a Makefile, a **fixed timestep** |

Each lesson folder has `notes.md`, `code/`, `exercises.md` and `solutions/`. Printable handouts are
in [`handouts/`](handouts/).

---

## Why terminal and ASCII, and not a graphics library?

Because a beginner fighting a linker is a beginner who quits.

Setting up SDL or raylib means installing a library, finding its headers, passing the right `-l`
flags, and debugging link errors — before drawing a single pixel. That is a genuinely hard first
lesson about build systems disguised as a game lesson.

So this track uses nothing but the compiler. The result is that **you build the machinery yourself**:

| You build | Which in other tracks was handed to you |
|---|---|
| a screen buffer, cleared and presented by hand | turtle's `tracer(0)`, the canvas's `clearRect` |
| a frame timer with `<chrono>` and `sleep_for` | `requestAnimationFrame`, `ontimer`, `after` |
| non-blocking keyboard input | `addEventListener`, `onkeypress` |

That is the point of the C++ track. The ideas are the same ones the other tracks teach; here the
machinery is **visible**.

`raylib` arrives at intermediate level, once the toolchain is familiar and a linker error is an
inconvenience rather than a wall.

---

## The visualizers

Nine animated explainers in [`../../shared/visualizers/`](../../shared/visualizers/index.html). They
work offline — double-click `index.html`. They are web pages, and you are writing C++, **on purpose**:
the game loop is an idea, not a feature of a language.

| Lesson | Open these |
|---|---|
| 1 | [the game loop](../../shared/visualizers/game-loop.html) |
| 3 | [grids and flat arrays](../../shared/visualizers/tilemap-indexing.html), [coordinates](../../shared/visualizers/coordinates.html) |
| 4 | [the game loop](../../shared/visualizers/game-loop.html), [grids and flat arrays](../../shared/visualizers/tilemap-indexing.html) |
| 5 | [box collision](../../shared/visualizers/aabb-collision.html), [gravity](../../shared/visualizers/gravity-and-velocity.html) |
| 6 | [delta time](../../shared/visualizers/delta-time.html), [box collision](../../shared/visualizers/aabb-collision.html) |

---

## If something goes wrong

| Symptom | Cause |
|---|---|
| Your change seems to do nothing | **You did not recompile.** Happens to everyone. |
| `command not found: ./game` | Wrong folder, or you compiled without `-o` and have an `a.out` |
| `error: 'cout' was not declared` | Missing `#include <iostream>` or missing `std::` |
| Error points at the line *after* the mistake | A missing `;` — that is where the compiler first *noticed* |
| **Your terminal stops showing what you type** | A game exited without restoring it. **Type `reset` and press Enter.** You will not see yourself typing; it works anyway. |
| Keys do nothing from lesson 4 onwards | You are in an IDE console. Use a real terminal. |
| `make: *** missing separator` | Spaces instead of a **tab** in the Makefile |
| `Undefined symbols ...` | A **link** error: a `.cpp` is missing from the build |

---

## ASCII Pong, stage by stage

[`project-ascii-pong/README.md`](project-ascii-pong/README.md) maps each stage to the lesson file that
builds it, with `diff` commands.

---

## What you will know at the end

- What **compiling** actually is, and why games are written in C++.
- What `&` means, and why forgetting it fails **silently**.
- That C++ will let you write outside an array, and why that makes bounds-checking a habit rather
  than a nicety.
- How a screen buffer, double buffering and `y*WIDTH+x` work — because you built them.
- Why a real-time loop never waits, and how to make a terminal cooperate.
- When to use a `std::vector`, and the list-removal bug that follows you into every language.
- How to split a program across files, what linking is, and what a Makefile buys you.
- What a **fixed timestep** is for.

---

## Where next

[`../intermediate_lvl/`](../intermediate_lvl/) — 12 lessons over 4 weeks with **raylib**: real
graphics, textures, sprite animation, tilemaps, cameras, sound, and classes. Setting raylib up is
lesson 1, deliberately, now that a linker error is an inconvenience rather than a wall.

If you would rather see the same ideas somewhere else first,
[`../../webgames/beginner_lvl/`](../../webgames/beginner_lvl/) and
[`../../games_with_py/beginner_lvl/`](../../games_with_py/beginner_lvl/) teach the same concepts in
the same order, and run much faster the second time around.
