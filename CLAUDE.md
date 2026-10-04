# CLAUDE.md — working notes for this repository

This is a **teaching content repository**, not an application. The product is lessons: Markdown
notes, HTML visualizers, runnable code examples, and printable PDF handouts for a game-development
course aimed at 13–15 year olds.

## Read these before changing anything

| File | What it is |
|---|---|
| `docs/COURSE_SPEC.md` | **The contract.** Audience, cadence, the conceptual spine, writing rules, code rules, and the definition-of-done checklist for a lesson. If a lesson and the spec disagree, the spec wins — or the spec changes in a commit of its own. |
| `docs/CURRICULUM_MAP.md` | All 90 lessons across 3 tracks × 3 levels. The resume point: it says what is authored and what is not. |
| `docs/AUTHORING_GUIDE.md` | How to add a lesson, how to use `anim.js`, how to build the PDFs. |
| `docs/PROGRESS.md` | What actually exists right now. Update it when you finish a lesson. |

## Commands

```bash
bash tools/check_all.sh            # full verification: C++, Python, pages, links
bash tools/check_all.sh --quick    # skip the Chrome pass (much faster)
node tools/check_pages.js --only tilemap   # check one page while iterating
python3 tools/check_turtle.py      # run every turtle/tkinter example for real
python3 tools/build_handouts.py    # rebuild every handout PDF
python3 tools/new_lesson.py --help # scaffold a new lesson folder
```

Run `check_all.sh` before committing. The Chrome pass takes a couple of minutes; `--quick` is the
loop to use while writing.

## Conventions that matter most

- **No dependencies in lesson code. Ever.** No CDN `<script>` tags, no `npm`, no `pip` at beginner
  level, no build step. A lesson must not fail because the classroom Wi-Fi is down.
- **Beginner code is boringly explicit.** No clever one-liners, no comprehensions that trade a
  concept for a line. Long names.
- **Consistent names across all three tracks.** The ball is `ball`, its speed is `speedX` / `speed_x`,
  the functions are `update()` and `draw()`. A student moving from JS to Python should recognise the
  program.
- **Comments are the lesson.** On first introduction, every code block is commented line by line.
  `code.css` deliberately renders comments in *high* contrast, not faded grey.
- **Visualizers are built on `shared/js/anim.js`.** Never hand-roll a loop or controls. Use
  `api.slider()` / `api.toggle()` / `api.button()` rather than building raw inputs, because those
  helpers redraw the canvas — a hand-built input appears to do nothing while the sketch is paused.
- **Concept visualizers live once**, in `shared/visualizers/`, and all three tracks link to them. Only
  genuinely language-specific visuals get a track-local `visualizer.html`.
- **The maths comes after the problem**, never before. Name the theorem once the student has already
  used it.
- Pronouns: **they/them** for any student, teacher or player in the abstract.

## Things that have bitten before

- `localStorage` **throws** (it does not merely return null) in a private window or with site data
  blocked. Every access in `page.js` is wrapped in try/catch, and pages must render correctly without
  it.
- `anim.js` reads its canvas colours from `--anim-*` CSS custom properties. A new colour needs adding
  in **three** places in `notes.css`: `:root`, the `prefers-color-scheme: dark` block, and the
  `[data-theme="dark"]` block.
- The syntax highlighter in `codeblock.js` must match comments and strings **before** keywords, or a
  keyword inside a comment gets coloured. There is a regression test for this; keep the alternation
  order.
- `anim.js` uses `ResizeObserver`, not the window `resize` event, so dispatching a synthetic `resize`
  will not force a redraw.
- **Every tkinter/turtle game must quit cleanly.** A queued `after()`/`ontimer()` frame firing after
  the window is gone raises `TclError: invalid command name ".!canvas"`. Needs a `running` flag plus
  `after_cancel()` for the quit key, `WM_DELETE_WINDOW` for tkinter's X button, and a *narrow*
  `except (tkinter.TclError, turtle.Terminator)` for turtle, where teardown cannot be prevented.
  `games_with_py/beginner_lvl/test_quit_does_not_crash.py` guards this.
- **`tools/check_turtle.py` hides its windows** (`Tk.withdraw()`), or running the checks flashes a
  dozen windows at the user. Keep it that way; it still catches runtime errors.
- Handout PDFs must use `white-space: pre-wrap` for code. A code block clipped at the right page edge
  makes a printed worksheet useless, and it is the most common defect in printed programming material.
