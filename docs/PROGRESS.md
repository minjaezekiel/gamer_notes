# PROGRESS — what actually exists

Updated as work completes. See [`CURRICULUM_MAP.md`](CURRICULUM_MAP.md) for the design of everything,
authored or not, and [`COURSE_SPEC.md`](COURSE_SPEC.md) §11 for the definition-of-done checklist each
lesson must pass before it is ticked here.

**Legend:** ✅ done and verified · 🟡 in progress · ⬜ not started

---

## Phase 1 — scaffold and all three beginner levels

**Status: complete.** 18 lessons, 9 visualizers, 18 handout PDFs, 3 logic test suites.

| | |
|---|---|
| Lessons authored | 18 of 18 |
| Code examples | see per-track tables below; all compile/run, verified |
| Handout PDFs | 18, committed |
| Links | all resolve (`tools/check_all.sh`) |
| HTML pages | all load in real Chrome with no console errors |
| C++ | all compile with `clang++ -std=c++17 -Wall`, no warnings |
| Python | all byte-compile; every turtle/tkinter example runs to completion |
| Logic tests | Snake, Brick Breaker, maze reachability, quit-path crashes — all passing |

### Bugs found and fixed by the checks

| Bug | Where | Fix |
|---|---|---|
| Quitting crashed with `TclError: invalid command name ".!canvas"` — a frame was still queued when the window was destroyed | both tkinter games, and all four turtle games via the window's X button | a `running` flag + `after_cancel()` for the quit key; `WM_DELETE_WINDOW` for tkinter's close button; a narrow `except (TclError, Terminator)` for turtle, which cannot be prevented. Locked down by `games_with_py/beginner_lvl/test_quit_does_not_crash.py` |
| A random index taken by casting a `double` could, in principle, land one past the end of a vector | `games_with_cpp/.../lesson-06/code/game.cpp` | use `uniform_int_distribution` for an index. Latent portability risk; not reproducible on this machine's library |


### Foundation

| Item | State |
|---|---|
| `README.md` | ✅ |
| `LICENSE` (MIT) | ✅ |
| `CLAUDE.md` | ✅ |
| `docs/COURSE_SPEC.md` | ✅ |
| `docs/CURRICULUM_MAP.md` | ✅ all 90 lessons specified |
| `docs/AUTHORING_GUIDE.md` | ✅ |
| `docs/TEACHER_GUIDE.md` | ✅ |
| `docs/PROGRESS.md` | ✅ this file |

### Shared layer

| Item | State | Notes |
|---|---|---|
| `shared/js/anim.js` | ✅ | the teaching-animation library: play/step/reset, draggable handles, drawing helpers |
| `shared/js/codeblock.js` | ✅ | dependency-free highlighter for js/python/cpp; regression-tested on comment-vs-keyword ordering |
| `shared/js/vec.js` | ✅ | also the reference answer for web intermediate L2 |
| `shared/js/page.js` | ✅ | light/dark toggle, storage-safe |
| `shared/css/notes.css` | ✅ | screen styling + the `--anim-*` tokens |
| `shared/css/code.css` | ✅ | code blocks; comments deliberately high-contrast |
| `shared/css/print.css` | ✅ | handouts; `pre-wrap` so code never clips |

### Visualizers — all 9 load clean in real Chrome

| File | Teaches | State |
|---|---|---|
| `game-loop.html` | input/update/render; step advances ONE phase | ✅ |
| `coordinates.html` | screen y-down vs maths y-up, one dot in both grids | ✅ |
| `delta-time.html` | two balls race; drag the frame rate and one breaks | ✅ |
| `gravity-and-velocity.html` | the two-addition chain, with a live numbers table | ✅ |
| `vectors.html` | drag two arrows, add head-to-tail, normalise | ✅ |
| `aabb-collision.html` | four conditions, each with its own light | ✅ |
| `circle-collision.html` | Pythagoras, with the triangle drawn | ✅ |
| `state-machine.html` | clickable states; ignored presses are the lesson | ✅ |
| `tilemap-indexing.html` | grid ↔ flat array, colour-banded by row | ✅ |
| `index.html` | gallery launcher for the teacher | ✅ |

### Tooling

| Item | State |
|---|---|
| `tools/check_pages.js` | ✅ parallel Chrome load check + link check |
| `tools/check_turtle.py` | ✅ actually runs every turtle/tkinter example |
| `tools/build_handouts.py` | ✅ |
| `tools/new_lesson.py` | ✅ |
| `tools/check_all.sh` | ✅ |
| `templates/` | ✅ |

### `webgames/beginner_lvl`

| # | Lesson | notes | visualizer | code | exercises | solutions | handout |
|---|---|---|---|---|---|---|---|
| 1 | What is a game, really? | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Moving pictures | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | Player in control | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | When things touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | Rules, score and feel | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | Capstone: Breakout | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| — | `project-pong/` guide | ✅ | | | | | |

### `games_with_py/beginner_lvl`

| # | Lesson | notes | visualizer | code | exercises | solutions | handout |
|---|---|---|---|---|---|---|---|
| 1 | The loop without pixels | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Drawing with turtle | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | Making it move | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | Snake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | A real window: tkinter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | Capstone: Brick Breaker | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| — | `project-snake/` guide | ✅ | | | | | |

### `games_with_cpp/beginner_lvl`

| # | Lesson | notes | visualizer | code | exercises | solutions | handout |
|---|---|---|---|---|---|---|---|
| 1 | Closer to the metal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | A game is data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | Drawing with letters | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | Input and movement | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | Many things at once | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | Capstone: ASCII arcade | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| — | `project-ascii-pong/` guide | ✅ | | | | | |

---

## Phase 2 — intermediate levels (36 lessons)

🟡 **In progress. `webgames/intermediate_lvl` is complete: 12 lessons.**

| | |
|---|---|
| Lessons authored | 12 of 12 (web) · 0 of 12 (python) · 0 of 12 (c++) |
| Code examples | 48 pages plus a 15-module capstone game |
| New shared visualizers | 10, bringing the gallery to 19 |
| Handout PDFs | 12, committed |
| Verification | every page loads clean in real Chrome; every visualizer is stepped 90 frames with its toggles flipped and its sliders pushed to both ends; the capstone is played headlessly for 400 frames |

### `webgames/intermediate_lvl`

| # | Lesson | notes | code | exercises | solutions | handout |
|---|---|---|---|---|---|---|
| 1 | One file becomes many | ✅ | ✅ 17 files | ✅ | ✅ | ✅ |
| 2 | Vectors for real | ✅ | ✅ 5 | ✅ | ✅ | ✅ |
| 3 | Acceleration, friction and drag | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 4 | Sprites and spritesheets | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 5 | Tilemaps | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 6 | The camera | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 7 | Scenes, properly | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 8 | Sound design with Web Audio | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 9 | Particles and juice engineering | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 10 | Enemies that seem to think | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 11 | Saving and loading | ✅ | ✅ 4 | ✅ | ✅ | ✅ |
| 12 | **Capstone: a platformer** | ✅ | ✅ 3 + 16-file game | ✅ | ✅ | ✅ |

### New shared visualizers

| File | What it shows |
|---|---|
| `module-dependencies.html` | a load order resolved one file per Step press; one extra arrow makes it impossible |
| `acceleration-and-friction.html` | overshoot, orbiting at zero friction, and the per-frame friction bug |
| `sprite-animation.html` | the game clock and the animation clock, kept apart |
| `tile-collision.html` | two corrections in two colours; one combined move climbs the wall |
| `camera.html` | world space and screen space at the same moment, with the subtraction |
| `easing.html` | five dots, same `t`, five journeys |
| `audio-envelope.html` | the vertical edge in the waveform that *is* the click |
| `enemy-ai.html` | hysteresis: set the give-up gap to zero and count the state changes |
| `save-round-trip.html` | six of ten values come back different, and one complains |
| (`gravity-and-velocity.html` re-used for the capstone's apex) | |

### Tooling added in this phase

| Item | Why |
|---|---|
| `?selftest=N` hook in `anim.js` | loading a page only proved the **first** frame drew. The checker now steps 90 frames, flips every toggle and pushes every slider to both ends. It found two real latent crashes in pages that had already passed. Verified by planting a frame-40 crash. |
| local http server in `check_pages.js` | ES-module pages cannot be imported from `file://`, so they were unverifiable. Module pages are now served and loaded over `http://127.0.0.1`. |
| module-aware inline-script parsing | `new Function()` refuses `import`; those blocks go through `node --check` instead. |
| HTML comments stripped before the inline-script scan | several lessons discuss `<script>` tags inside a comment. |
| `ERROR:CONSOLE` treated as a failure | so a page can report a failed self-check by throwing. |
| `tools/.venv` (gitignored) with `pygame-ce` | for the Python intermediate checks. Excluded from every checker walk. |
| `raylib` 6.0 installed via Homebrew | for the C++ intermediate checks. `/usr/local/include` is already on the default search path, so no `-I` is needed. |
| `selftest.html` in the capstone | dispatches real keyboard events, plays 400 frames, and asserts the player's numbers stay finite and in bounds. Verified by planting a NaN. |

### Bugs found by the new checks

| Bug | Where | Fix |
|---|---|---|
| `Anim.clamp is not a function` — the helpers live on `Anim.util`, and the call sites were in `update()`, which a plain page load never runs | `camera.html`, `easing.html`, `enemy-ai.html` | corrected to `Anim.util.clamp`. These pages had already **passed** the old checker; the 90-frame self-test is what found them |
| mismatched quote in a template string | `lesson-11/code/02-what-json-keeps.html` | caught by the inline-script parse |
| an HTML comment closed with `*/`, which would have commented out the whole page | `lesson-12/.../selftest.html` | closed with `-->` |

## Phase 3 — advanced levels (36 lessons)

⬜ Not started. Specified in `CURRICULUM_MAP.md`, with a README per level.

---

## Known limitations, stated honestly

- **The checks run the windows hidden.** `tools/check_turtle.py` creates each window *withdrawn*,
  so verifying 14 examples does not flash 14 windows across your screen. Everything is still really
  drawn and every error still surfaces — this was verified by introducing a deliberate typo and
  confirming it was still caught.
- **`turtle`/`tkinter` examples are run, but not looked at.** `tools/check_turtle.py` executes each
  one to completion with the blocking calls (`exitonclick`, `mainloop`, `after`) neutralised, so a
  bad method name or wrong argument count is caught. It cannot tell whether the resulting picture is
  *correct* — that still needs a human to open it. It also needs a display, and skips with a message
  on a headless machine.
- **The Chrome check cannot confirm an animation looks right.** It catches console errors and a sketch
  that failed to build a canvas. Whether the step button genuinely advances one frame has to be
  clicked by a human.
- **PDF layout is not machine-checkable.** Clipped code and awkward page breaks need eyes.
