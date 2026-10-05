# Web Games — Intermediate Level

**HTML, CSS and JavaScript · 12 lessons · 4 weeks · 30 contact hours**

Take the one-file Breakout you finished at beginner level and build a real game out of it: a scrolling
platformer with sprites, sound, enemies, saved scores, and a jump that feels right.

Still no frameworks, no package manager and no build step. Two of the twelve lessons use ES modules,
which need a local server — one command, and no internet. Everything else opens by double-clicking.

---

## Before you start

You should have finished [`../beginner_lvl/`](../beginner_lvl/), or be comfortable with all of it: the
game loop, delta time, state in variables, polled input, collision detection, a state machine, and
levels as data.

**One thing to check on your machine first.** Lessons 1 and 12 use `import`, which a browser refuses to
do from a `file://` page. Open a terminal in the lesson folder and run:

```bash
python3 -m http.server 8000
```

then open <http://localhost:8000>. That server runs on your own computer; no network is involved, and
it works with the Wi-Fi off. If you cannot run that command — a locked-down school account, a
Chromebook with no terminal — lesson 1 teaches a second way of splitting a program that works by
double-clicking, and every later lesson is built that way.

---

## The lessons

| # | Lesson | What you build | Core idea |
|---|---|---|---|
| 1 | [One file becomes many](lesson-01-one-file-becomes-many/notes.md) | Breakout, in seven files | **which way dependencies point** |
| 2 | [Vectors for real](lesson-02-vectors-for-real/notes.md) | a ship that aims and shoots | **subtract, normalise, scale** |
| 3 | [Acceleration, friction and drag](lesson-03-acceleration-friction-and-drag/notes.md) | a ship that feels good to fly | momentum, and **four numbers** |
| 4 | [Sprites and spritesheets](lesson-04-sprites-and-spritesheets/notes.md) | a character that walks | **two clocks**: the game's and the animation's |
| 5 | [Tilemaps](lesson-05-tilemaps/notes.md) | a world with solid walls | **axis-separated collision** |
| 6 | [The camera](lesson-06-the-camera/notes.md) | a world bigger than the screen | **one subtraction**, and a dead zone |
| 7 | [Scenes, properly](lesson-07-scenes-properly/notes.md) | title, pause, game over | a **scene stack** |
| 8 | [Sound design with Web Audio](lesson-08-sound-design-with-web-audio/notes.md) | eight sounds, no files | **envelopes**, and the audio clock |
| 9 | [Particles and juice engineering](lesson-09-particles-and-juice-engineering/notes.md) | a juice toolkit | **feedback**, measured |
| 10 | [Enemies that seem to think](lesson-10-enemies-that-seem-to-think/notes.md) | three kinds of enemy | **decide, then act** |
| 11 | [Saving and loading](lesson-11-saving-and-loading/notes.md) | high scores and settings | **loaded data is untrusted** |
| 12 | [**Capstone: a platformer**](lesson-12-capstone-a-platformer/notes.md) | a complete platformer | the **six parts of a jump** |

Each lesson folder holds `notes.md` (read this), `code/` (run these, in order),
`exercises.md` (the handout's source) and `solutions/` (for the teacher).

Printable handouts: [`handouts/`](handouts/).

---

## What is different about this level

**Three habits, which matter more than any single feature.**

1. **Programs are made of parts that each do one job.** By lesson 12 the game is fifteen files, and you
   can find anything in it in under ten seconds. Lesson 1 is about nothing else.
2. **Tune in the units of the design.** Not "jump speed 520" but "three tiles high, a third of a second
   to the top". The code works the engine numbers out for you.
3. **Check your work by measuring, not by guessing.** Lesson 9 times two versions of the same code.
   Lesson 12 draws a map of where players died. Both answer a question that an argument cannot.

**Two bugs you will meet repeatedly**, because they are the ones that survive your own testing:

- **Frame-rate dependence.** `vel *= 0.98` looks fine and behaves differently on a faster monitor
  (lesson 3).
- **Things that work on your machine.** `localStorage` throws in a private window; modules will not
  import from a file; audio will not start until somebody clicks (lessons 1, 8, 11).

---

## The visualizers

Open [`../../shared/visualizers/`](../../shared/visualizers/index.html) at the start of a lesson and
project from there. The ones this level uses most:

| Lesson | Explainer |
|---|---|
| 1 | which way do dependencies point |
| 2 | vectors |
| 3 | acceleration, friction and drag · easing |
| 4 | spritesheets and animation |
| 5 | tile collision, one axis at a time · grids and flat arrays |
| 6 | the camera |
| 7 | game states · easing |
| 8 | why sounds need an envelope |
| 9 | easing · acceleration and friction |
| 10 | enemies that seem to think · game states |
| 11 | what survives a save |
| 12 | gravity, velocity, position · tile collision |

---

## Verifying the code

From the repository root:

```bash
bash tools/check_all.sh            # everything
bash tools/check_all.sh --quick    # skip the Chrome pass
```

The Chrome pass loads every page, steps 90 frames of every visualizer, and plays the capstone
headlessly for 400 frames (see `lesson-12-capstone-a-platformer/code/03-the-whole-game/selftest.html`)
checking that the player's numbers stay finite and in bounds.

---

## Next

[`../advanced_lvl/`](../advanced_lvl/) takes this same platformer and makes it correct under stress: a
fixed timestep, spatial partitioning, pathfinding, procedural generation, profiling, and shipping it to
other people.
