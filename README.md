# Game Dev Bootcamp

A complete, teachable game-development course for students aged **13 to 15** (US grade 8–9 /
Form 2–3), in three languages, built to be run in a real classroom.

No game engine. No frameworks. No installers for the first two weeks. Students build **Pong,
Breakout, Snake and an ASCII arcade game from nothing**, and come out understanding why each line is
there.

---

## What makes this course different

Most beginner tutorials hand you a finished game loop and ask you to fill in the blanks. This course
does the opposite: it teaches **one set of ideas three times, in three languages**, so a student
learns that a game loop is an *idea* rather than a library feature.

| | |
|---|---|
| **One conceptual spine** | Game loop → state → coordinates → velocity → delta time → input → collision → rules → feel → data → decomposition. Same order in every track, so the third time around a student recognises the shape immediately. |
| **Animated explainers you can step** | Nine interactive visualizers with a **step-one-frame** button. That button is the point: it is how a student *sees* that a game is a flipbook, not continuous motion. |
| **The maths comes second** | Pythagoras appears when we need to measure a distance, not in a preliminary chapter. Vectors, modulo and acceleration arrive the same way — as the answer to a problem the student already has. |
| **Bugs are taught, not avoided** | Every lesson shows the broken version first where it helps, and every handout has a *find and fix the bug* section. Watching a ball move at double speed on a fast laptop teaches delta time better than any paragraph. |
| **Open-ended by design** | Every lesson ends with a *Think like an engineer* problem that has no answer key. Several of them ask students to invent, from scratch, a technique real engines use — spatial partitioning, sparse storage, state machines. Inventing it first and naming it second is the whole pedagogy. |

---

## Pick a track

| Track | Language | Beginner uses | Why |
|---|---|---|---|
| [`webgames/`](webgames/) | HTML, CSS, JavaScript | Canvas 2D, no libraries | Zero install. Works on a Chromebook. A student can send a friend a playable link the same afternoon. |
| [`games_with_py/`](games_with_py/) | Python | `turtle`, then `tkinter` | Both ship with Python, so there is nothing to install and nothing for school IT to block. `pygame-ce` arrives at intermediate level. |
| [`games_with_cpp/`](games_with_cpp/) | C++ | terminal / ASCII, compiler only | A beginner fighting a linker is a beginner who quits. Lesson 1 compiles with one command. `raylib` arrives at intermediate level. |

Each track has `beginner_lvl/`, `intermediate_lvl/` and `advanced_lvl/`.

> **Build status.** The three **beginner levels are complete** (18 lessons). The 72 intermediate and
> advanced lessons are fully specified in [`docs/CURRICULUM_MAP.md`](docs/CURRICULUM_MAP.md) and are
> being authored next. See [`docs/PROGRESS.md`](docs/PROGRESS.md) for exactly what exists today.

---

## Course shape

| Level | Weeks | Lessons | Contact hours |
|---|---|---|---|
| Beginner | 2 | 6 | 15 h |
| Intermediate | 4 | 12 | 30 h |
| Advanced | 4 | 12 | 30 h |

**3 lessons per week, 2 h 30 m each.** Every lesson is timed to fit that slot with room to spare, and
every lesson's teacher notes say where to cut if the class runs long.

### What students build at beginner level

| Track | Lessons 1–5 build toward | Capstone |
|---|---|---|
| Web | a bouncing ball, a paddle you steer, then **Pong** | **Breakout** |
| Python | a text adventure, turtle art, then **Snake** | **Brick Breaker** |
| C++ | a text RPG battle, an ASCII dungeon, then **ASCII Pong** | **an ASCII arcade game** |

---

## Start here

**If you are teaching this**, read these three, in order:

1. [`docs/TEACHER_GUIDE.md`](docs/TEACHER_GUIDE.md) — how to run a 2 h 30 m session, room setup,
   what to do about the student who finishes in 40 minutes, and how to mark open-ended work.
2. [`shared/visualizers/index.html`](shared/visualizers/index.html) — open this in a browser and
   click through all nine explainers. It takes ten minutes and it is the best preparation you can do.
3. The `README.md` of whichever track you are teaching.

**If you are a student working alone**, go straight to your track's `beginner_lvl/` folder and start
at lesson 1. Read `notes.md`, run the files in `code/` in order, then do `exercises.md`.

**If you are curious what is actually in here**, open
[`shared/visualizers/game-loop.html`](shared/visualizers/game-loop.html) and press
**Step 1 frame** three times.

---

## Requirements

| Track | You need | Install time |
|---|---|---|
| Web | A browser. That is all. | none |
| Python (beginner) | Python 3.10 or newer, with `tkinter` | none — both are standard |
| Python (intermediate+) | `pip install pygame-ce` | 1 minute |
| C++ (beginner) | Any C++17 compiler: `clang++`, `g++`, or MSVC | varies |
| C++ (intermediate+) | `raylib` | 5 minutes |

**Nothing in the beginner levels needs the internet.** No CDN script tags, no package managers, no
build tools. A lesson must not fail because the classroom Wi-Fi is down, and these do not.

To check that a machine is ready, run:

```bash
python3 --version        # 3.10 or newer
python3 -c "import tkinter; print('tkinter ok')"
clang++ --version        # or: g++ --version
```

---

## Repository layout

```
.
├── docs/                  # the course design: spec, full 90-lesson map, teacher guide
├── shared/
│   ├── css/               # notes.css (screen), code.css (code blocks), print.css (handouts)
│   ├── js/                # anim.js — the teaching-animation library everything is built on
│   └── visualizers/       # the nine animated explainers; open index.html
├── webgames/              # beginner_lvl / intermediate_lvl / advanced_lvl
├── games_with_py/         #   each with lesson-NN-*/ folders and a handouts/ folder
├── games_with_cpp/
├── templates/             # skeletons for a new lesson
└── tools/                 # handout builder and the verification scripts
```

Every lesson folder has the same five things, so you never have to hunt:

```
lesson-04-when-things-touch/
├── notes.md          # the lesson — nine fixed sections, every time
├── visualizer.html   # the in-class animation (or a signpost to a shared one)
├── exercises.md      # source for the printable handout
├── code/             # runnable examples, numbered in teaching order
└── solutions/        # worked answers and marking notes, for the teacher
```

---

## Handouts

Printable PDFs for every lesson are committed under each level's `handouts/` folder, so a teacher can
print without running anything. To rebuild them after editing an `exercises.md`:

```bash
python3 tools/build_handouts.py              # all of them
python3 tools/build_handouts.py webgames     # just one track
```

The build needs **Google Chrome** (used headlessly to print the PDF) and nothing else — no LaTeX, no
pandoc, no `wkhtmltopdf`. See [`docs/AUTHORING_GUIDE.md`](docs/AUTHORING_GUIDE.md) for the details.

---

## Contributing or adapting this

This is MIT licensed, so you may use it in your own classroom, translate it, or rip it apart. If you
are adding or changing lessons, two documents matter:

- [`docs/COURSE_SPEC.md`](docs/COURSE_SPEC.md) is the **contract** — audience, writing rules, code
  rules, and the checklist that defines when a lesson is finished. If a lesson and the spec disagree,
  the spec wins.
- [`docs/AUTHORING_GUIDE.md`](docs/AUTHORING_GUIDE.md) is the **how** — scaffolding a lesson,
  using `anim.js`, and building the PDFs.

Before committing, run the checks:

```bash
bash tools/check_all.sh          # compiles C++, byte-compiles Python, loads every page in Chrome
bash tools/check_all.sh --quick  # same minus the Chrome pass, for a fast loop
```

---

## A note on the open-ended questions

Several *Think like an engineer* prompts ask students to invent something that has a real name —
spatial hashing, sparse data structures, finite state machines. **Please do not give the name away
first.** A student who invents the idea and is then told "what you just described is called a uniform
grid, and it is in every game engine" has learned something no lecture can deliver. The names are in
the solutions folder, for you.

---

## License

MIT — see [LICENSE](LICENSE). Use it, change it, teach with it.
