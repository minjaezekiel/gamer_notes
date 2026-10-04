# COURSE_SPEC — the contract

This file is the single source of truth for what this repository must contain and how it must read.
Everything else in the repo is checked against this document. If a lesson and this spec disagree,
the spec wins — or the spec gets changed deliberately, in a commit of its own.

---

## 1. Who this is for

**Primary audience: a student aged 13–15 (US grade 8 to 9 / Form 2 to 3).**

Assume they:

- can read and write a little code — a variable, an `if`, a loop, maybe a function;
- have **never seen how a whole program fits together** from start to finish;
- have never written anything that runs continuously rather than once;
- know maths up to basic algebra, negative numbers, and coordinates on a grid;
- have **not** met vectors, trigonometry, or calculus, and do not need to in order to succeed here;
- are motivated by seeing something move on screen within the first 30 minutes.

Do **not** assume they:

- know what a compiler, terminal, frame, buffer, or API is;
- can install software with admin rights;
- have a fast machine, a GPU, or a reliable internet connection.

**Secondary audience: the teacher**, who may not be a game developer. Every lesson must be teachable
by someone reading it for the first time the night before, which is why each lesson carries timing
boxes, a list of predictable student mistakes, and worked solutions.

## 2. The non-negotiable goal

A student finishing a level must be able to **invent a game mechanic we never taught them** and work
out how to build it. Reproducing our Pong is the floor, not the ceiling. That is why every lesson
contains a *Think like an engineer* prompt with no single right answer, and why we always teach the
underlying idea before the library call that happens to implement it.

## 3. Shape of the course

| Level | Weeks | Lessons | Contact hours |
|---|---|---|---|
| `beginner_lvl` | 2 | 6 | 15 h |
| `intermediate_lvl` | 4 | 12 | 30 h |
| `advanced_lvl` | 4 | 12 | 30 h |

- **3 lessons per week, 2 h 30 m each.** Every lesson's content must fit that slot with time to
  spare — see the timing budget in §7.
- Three tracks: `webgames/` (HTML/CSS/JS), `games_with_py/` (Python), `games_with_cpp/` (C++).
- 3 tracks × 3 levels × (6|12|12) lessons = **90 lessons total.**

"Level" is relative to the *student*, never to the industry. `advanced_lvl` means
advanced-for-a-9th-grader: state machines, tilemaps, simple enemy AI, basic optimisation, shaders as
a *concept*. It does not mean professional engine architecture.

## 4. The conceptual spine

Every track teaches the **same ideas in the same order**. This is the whole design: a student who
meets the game loop in JavaScript in week 1 and then meets it again in Python and C++ learns that
*the loop is an idea, not a library feature*. That transfer is the point.

| # | Concept | First taught (beginner lesson) |
|---|---|---|
| 1 | A game is a loop: input → update → render | 1 |
| 2 | State: what the game remembers between frames | 1–2 |
| 3 | Coordinates: the screen is a grid, and Y points **down** | 2 |
| 4 | Velocity: position changes by a little bit every frame | 2 |
| 5 | Delta time: frames are not all the same length | 2 |
| 6 | Input as polled *state*, not as one-off events | 3 |
| 7 | Collision: overlap tests (AABB) and distance tests (circles) | 4 |
| 8 | Response: reflecting, blocking, destroying | 4 |
| 9 | Rules and a state machine: menu → play → game over | 5 |
| 10 | Game feel: juice, feedback, why 80 ms matters | 5 |
| 11 | Data not code: levels as arrays, tuning as numbers | 6 |
| 12 | Decomposition: splitting one big file into parts that each do one thing | 6 |

Intermediate adds: vectors proper, acceleration and friction, sprite animation, tilemaps, cameras,
scene management, saving, simple AI, sound design.
Advanced adds: fixed timestep, spatial partitioning, entity patterns, pathfinding, procedural
generation, profiling, polish and shipping.

## 5. Technology choices and why

| Track | Beginner | Intermediate / Advanced | Why |
|---|---|---|---|
| Web | Canvas 2D + vanilla JS | same, plus Web Audio, modules | Zero install. Runs on a Chromebook. A student can send a friend a link the same day. No framework ever — frameworks hide the loop, and the loop is the lesson. |
| Python | `turtle`, then `tkinter` | `pygame-ce` | Both are in the standard library, so nothing to install and nothing for a school IT lock-down to block. `pygame-ce` arrives at intermediate, once students already understand the loop they are being handed. |
| C++ | terminal / ASCII, compiler only | `raylib` | A beginner fighting a linker is a beginner who quits. Lesson 1 must compile with one command and no flags. `raylib` arrives only once the toolchain is familiar. |

**Hard rules.** No build tools, bundlers, package managers, or `node_modules` anywhere in the
beginner levels. No external CDN script tags in lesson code — a classroom Wi-Fi outage must not stop
a lesson. All C++ beginner examples must compile with exactly
`clang++ -std=c++17 -Wall file.cpp -o file` (or `g++`, same flags) and nothing more.

## 6. What every lesson folder contains

```
lesson-NN-kebab-case-title/
├── notes.md          # the lesson itself — the primary student artifact
├── visualizer.html   # projectable in-class animation, or a signpost to shared/visualizers/
├── exercises.md      # source for the printable handout
├── code/             # runnable examples, numbered in teaching order, heavily commented
└── solutions/        # worked answers + marking notes (teacher-facing)
```

Handout PDFs are generated, never hand-written, and land in `<level>/handouts/lesson-NN-handout.pdf`.

### `notes.md` — fixed section order

Same nine sections in every lesson in every track, so a student never has to relearn the shape of
the page:

1. **By the end of today you will have built —** concrete, with a picture or ASCII sketch.
2. **Where this fits** — one line back, one line forward, in the spine.
3. **The idea, in plain words** — no code at all. Analogy first.
4. **The idea, in pictures** — the visualizer, plus *what to look for* while it runs.
5. **The idea, in code** — built up in small increments, line-commented on first appearance.
6. **The maths (or physics) you just used** — named **after** it was needed. Never before.
7. **Break it on purpose** — change this number, predict what happens, then check. 3–5 experiments.
8. **Think like an engineer** — an open design/systems problem. No answer key.
9. **Vocabulary** · **Recap** · **Stretch goals** · **Teacher notes**.

### `exercises.md` — fixed section order

Page 1 of the PDF is a **one-page cheat sheet**: the whole lesson on one printable side. Then:

| Section | Purpose |
|---|---|
| A — Recall | 5–8 quick questions. Did the vocabulary land? |
| B — Predict the output | Read code, write down what it does, *then* run it. Builds a mental model. |
| C — Find and fix the bug | Deliberately broken code. The most transferable skill we teach. |
| D — Hands-on build | The main event. Numbered checkpoints so a student knows they are on track. |
| E — Design challenge | Open-ended and creative. Marked on reasoning, not on matching an answer. |
| Stretch | For whoever finishes in 40 minutes. Never required. |

## 7. Timing budget for a 2 h 30 m lesson

| Minutes | Block |
|---|---|
| 0–10 | Hook. Play a game, or show the broken thing we are about to fix. |
| 10–25 | Concept with the visualizer. Projector only — laptops closed. |
| 25–40 | Live-code the smallest version together. |
| 40–50 | **Break** |
| 50–120 | Hands-on build (exercises section D), teacher circulating. |
| 120–140 | Break-it-on-purpose experiments, then share-outs. |
| 140–150 | Recap, vocabulary, stretch-goal signpost. |

Every lesson's teacher notes must state where it can be cut if the class runs long, and what to do
with the student who finishes at minute 90.

## 8. Writing rules

1. **Plain words beat correct words, the first time.** Say "a little bit of movement every frame",
   then name it *velocity*. Introduce the term after the idea is already understood.
2. **Every new term is defined on first use**, in the sentence it appears in, and again in the
   Vocabulary box.
3. **Never belittle the reader's task.** No "simply add a line", "just type this", "obviously",
   "trivially", "it's easy", "all you have to do". If it were obvious the student would not be
   reading the lesson. ("Simply" meaning *merely* — "simply do not call it" — is fine;
   `tools/check_all.sh` flags the instructing forms only.)
4. **Second person.** "You will move the ball", not "the student moves the ball".
5. **Short sentences.** Target a grade 7 reading level so the English is never the obstacle.
6. **Every code block on first introduction is commented line by line.** Later repeats of known code
   need no comments.
7. **Show the broken version first** where it helps. A student who has seen the ball move at double
   speed on a fast laptop understands delta time in a way no explanation achieves.
8. **Analogies must be checkable.** A flipbook for frames, a recipe for an algorithm. Say explicitly
   where an analogy stops being true.
9. **No motivational padding.** No "awesome job!", no exclamation-mark encouragement. Respect the
   reader; they can tell.
10. **Mistakes are content, not failures.** Each lesson lists what usually goes wrong and why.
11. **Pronouns:** use *they/them* for any student, teacher, or player referred to in the abstract.
12. **Gender-neutral, culture-neutral examples.** Names in examples should vary across cultures.

## 9. Code rules

- Beginner code is **boringly explicit**. No clever one-liners, no ternaries, no comprehensions that
  save a line at the cost of a concept. Long names: `ballSpeedX`, not `bsx`.
- **Consistent names across all three tracks.** The ball is `ball`, its speed is `speedX`/`speed_x`,
  the loop function is `update()` and `draw()`. A student moving from JS to Python should recognise
  the program.
- Every `code/` file opens with a comment block: what it demonstrates, how to run it, and what to
  change first.
- Every file in `code/` **runs on its own.** No shared imports between lesson examples.
- Numbered in teaching order: `01-...`, `02-...`.
- Magic numbers are named constants at the top of the file, where a student can find and change them.

## 10. Visualizer rules

- Built on `shared/js/anim.js`. Do not hand-roll a loop or controls in a visualizer.
- Every visualizer that **animates** has **play, pause, step-one-frame, reset**. Step-one-frame is
  mandatory there: it is how a student sees that a game is a sequence of discrete moments rather than
  continuous motion. A visualizer that is purely interactive instead — drag two boxes and watch a
  test flip — has nothing to step through, and needs only **reset**. `tools/check_pages.js` enforces
  this distinction by looking for an `update()` in the sketch.
- Works offline. No CDN. No build step. Opens by double-clicking the file.
- Readable from the back of a classroom: minimum 16 px body text, 20 px+ for labels on canvas.
- Legible in light and dark mode, and legible when printed in black and white.
- Concept visualizers are **language-neutral and live once** in `shared/visualizers/`, linked from
  all three tracks. Only a genuinely language-specific visual (for example, how `tkinter.after()`
  differs from `requestAnimationFrame`) gets a track-local `visualizer.html`.

## 11. Definition of done for one lesson

A lesson may be marked complete in `PROGRESS.md` only when **all** of these hold:

- [ ] `notes.md` has all nine sections, in order, none empty.
- [ ] Every code example runs or compiles, verified by `tools/check_all.sh`.
- [ ] `visualizer.html` opens offline and its step-one-frame button works.
- [ ] `exercises.md` has sections A–E plus the cheat sheet.
- [ ] `solutions/` answers every question in A–D and gives marking notes for E.
- [ ] The handout PDF is generated and no code block is clipped at a page edge.
- [ ] Teacher notes include timings, likely student mistakes, a cut-for-time plan, and an
      early-finisher plan.
- [ ] Every relative link resolves.
- [ ] The build in section D fits in the 70-minute hands-on block. If it does not, cut it.

## 12. Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Directories | `kebab-case`, lessons prefixed `lesson-NN-` | `lesson-04-when-things-touch` |
| Level dirs | `beginner_lvl`, `intermediate_lvl`, `advanced_lvl` | — |
| Code examples | `NN-kebab-case.ext` | `02-the-game-loop.html` |
| Handouts | `lesson-NN-handout.pdf` | `lesson-01-handout.pdf` |
| JS / Python vars | `camelCase` in JS, `snake_case` in Python, same *words* in both | `speedX` / `speed_x` |
| C++ | `snake_case` for variables, `PascalCase` for structs | `struct Ball; int speed_x;` |
