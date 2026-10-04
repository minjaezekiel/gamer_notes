# Web Games — Beginner Level

**HTML, CSS and JavaScript · 6 lessons · 2 weeks · 15 contact hours**

Build Pong and Breakout from nothing. No game engine, no frameworks, no libraries, nothing to
install, and nothing that needs the internet.

---

## What you need

A web browser and a text editor. That is the entire list.

Any editor works — Notepad, TextEdit, VS Code, whatever is on the machine. If you have a choice,
VS Code is free and will tell you about typos before you run the file.

**Nothing here needs the internet.** No CDN script tags, no package manager, no build step. Open an
`.html` file by double-clicking it and it runs.

---

## The lessons

| # | Lesson | What you build | Core idea |
|---|---|---|---|
| 1 | [What is a game, really?](lesson-01-what-is-a-game/notes.md) | a square that moves on its own | the **game loop**: input, update, render, repeat |
| 2 | [Moving pictures](lesson-02-moving-pictures/notes.md) | a bouncing ball | coordinates, velocity, and **delta time** |
| 3 | [Player in control](lesson-03-player-in-control/notes.md) | a paddle you steer | **polled input**, not event-driven |
| 4 | [When things touch](lesson-04-when-things-touch/notes.md) | **Pong**, part 1 | **AABB collision** and response |
| 5 | [Rules, score and feel](lesson-05-rules-score-and-feel/notes.md) | **Pong**, finished | **state machines** and **juice** |
| 6 | [Capstone: Breakout](lesson-06-capstone-breakout/notes.md) | **Breakout** | levels as **data**, and decomposition |

Each lesson folder contains:

```
notes.md        the lesson - read this first
code/           runnable examples, numbered in teaching order
exercises.md    practice questions and the build task
solutions/      worked answers (teacher-facing)
```

Printable handouts for every lesson are in [`handouts/`](handouts/).

---

## If you are working through this alone

1. Read `notes.md` from the top. Do not skip the *in pictures* section — open the visualizer and
   press **Step 1 frame** a few times.
2. Open each file in `code/` **in order**, run it, and then change the number the header comment
   tells you to change. Predict what will happen *before* you reload.
3. Do `exercises.md` section D. That is where you actually build the thing.
4. Do the *break it on purpose* table in the notes. It takes ten minutes and it is worth more than
   re-reading.

Do not read ahead to the finished game and copy it. It will take you twice as long to understand and
you will not be able to change it afterwards.

---

## The visualizers

Nine animated explainers live in [`../../shared/visualizers/`](../../shared/visualizers/index.html).
They work offline — double-click `index.html`.

Every one has a **Step 1 frame** button, and that button is the point. Press it rather than pressing
Play, at least the first time. Watching an animation shows you a result; stepping through it shows
you a mechanism.

| Lesson | Open these |
|---|---|
| 1 | [the game loop](../../shared/visualizers/game-loop.html) |
| 2 | [coordinates](../../shared/visualizers/coordinates.html), [delta time](../../shared/visualizers/delta-time.html), [gravity](../../shared/visualizers/gravity-and-velocity.html) |
| 4 | [box collision](../../shared/visualizers/aabb-collision.html), [circle collision](../../shared/visualizers/circle-collision.html) |
| 5 | [game states](../../shared/visualizers/state-machine.html) |
| 6 | [grids and flat arrays](../../shared/visualizers/tilemap-indexing.html) |

---

## Pong, stage by stage

Pong grows across lessons 2 to 5. [`project-pong/README.md`](project-pong/README.md) shows which file
is which stage, and how to `diff` consecutive stages to see exactly what each step added.

---

## What you will know at the end

- Why a game is a loop, and what the three jobs inside it are.
- Why moving things "a bit each frame" is a bug, and how `dt` fixes it.
- How collision detection actually works, and why detection is the easy half.
- Why one state variable beats four flags.
- Why hitting things in a game feels good, and how little code that takes.
- How to describe a level as data so that changing it does not mean changing code.

And one thing that is not on the list but matters more: **you will have built four working games**,
and you will know that nothing in them was magic.

---

## Where next

[`../intermediate_lvl/`](../intermediate_lvl/) — 12 lessons over 4 weeks. It starts by splitting your
one big Breakout file into many, then adds vectors, sprites, tilemaps, cameras, scenes, sound design,
enemy AI, and saving. It finishes with a platformer.

If you would rather see the same ideas in another language,
[`../../games_with_py/beginner_lvl/`](../../games_with_py/beginner_lvl/) and
[`../../games_with_cpp/beginner_lvl/`](../../games_with_cpp/beginner_lvl/) teach the same concepts in
the same order. The second track goes much faster, because the ideas are already in place — and most
students say that is when they genuinely understood the first one.
