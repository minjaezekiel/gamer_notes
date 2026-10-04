# AUTHORING_GUIDE — how to add to this course

Read [`COURSE_SPEC.md`](COURSE_SPEC.md) first. That is the contract; this is the mechanics.

---

## 1. Scaffold the lesson

```bash
python3 tools/new_lesson.py webgames/intermediate_lvl 3 "Acceleration and friction"
```

That creates the folder, numbers it, and fills `notes.md`, `exercises.md` and `visualizer.html` from
`templates/`, with the correct relative paths back to `shared/` already wired up. Always use it
rather than copying a previous lesson by hand — a stale relative path is the commonest way to break
a page, and the link checker will catch it but only after you have wasted the time.

---

## 2. Write `notes.md`

Nine sections, fixed order, none empty. The order is not decoration: it moves from *idea* to
*picture* to *code* to *maths*, which is the opposite of how a textbook does it and is the reason
this course works for students who think they are bad at maths.

```markdown
# Lesson 3 — Acceleration and Friction

## By the end of today you will have built
## Where this fits
## The idea, in plain words
## The idea, in pictures
## The idea, in code
## The maths you just used
## Break it on purpose
## Think like an engineer
## Vocabulary · Recap · Stretch goals · Teacher notes
```

### Voice

Write for a 13-year-old who is capable but has no context. The full rules are in COURSE_SPEC §8;
the four that are hardest to remember:

- **Never write "simply", "just", "obviously", or "trivially".** If it were obvious the student would
  not be reading the lesson. This is the single easiest way to make someone feel stupid.
- **Idea first, name second.** "A little bit of movement every frame" → *then* call it velocity.
- **No motivational padding.** No "awesome job!". Students can tell, and it reads as condescension.
- **Show the broken version** wherever it helps. A ball that moves at double speed on a fast laptop
  teaches delta time in five seconds.

### Linking a visualizer

Most lessons link a shared explainer rather than shipping their own:

```markdown
## The idea, in pictures

Open [the delta-time explainer](../../shared/visualizers/delta-time.html).

**What to look for:** press Play with the frame rate at 60 and the two balls tie. Drag it to 20 and
press Reset. The top ball crawls, and nobody changed its speed setting.
```

Always include the *what to look for* line. A visualizer without it is a toy; with it, it is a lesson.

---

## 3. Write the code examples

In `code/`, numbered in teaching order, each one **runnable on its own**:

```
code/
├── 01-the-smallest-loop.html
├── 02-adding-velocity.html
└── 03-delta-time.html
```

Every file opens with a header comment saying what it shows, how to run it, and what to change first:

```python
# ============================================================
# 02 - Making the turtle move on its own
#
# RUN IT:     python3 02-moving.py
# CHANGE ME:  SPEED, on line 12. Try 1, then 20. What breaks at 20?
# ============================================================
```

That `CHANGE ME` line matters more than it looks. It converts a file a student reads into a file a
student *experiments with*, which is the difference between watching and learning.

For C++, state the exact compile command in the header. No build system at beginner level:

```cpp
// COMPILE:  clang++ -std=c++17 -Wall 03-buffer.cpp -o 03-buffer
// RUN:      ./03-buffer
```

---

## 4. Write `exercises.md`

Sections A–E plus a cheat sheet. The split is deliberate and each part does a different job:

| Section | Job |
|---|---|
| Cheat sheet | One printable side holding the whole lesson. Students keep these. |
| A — Recall | Did the vocabulary land? Fast, low stakes. |
| B — Predict the output | Read code, **write down** the answer, *then* run it. Being wrong on paper is where the learning is. |
| C — Find and fix the bug | The most transferable skill in the course. Use real bugs students actually write. |
| D — Hands-on build | The main event, 70 minutes, with numbered checkpoints so a student knows they are on track. |
| E — Design challenge | Open-ended. Marked on reasoning, never on matching our answer. |
| Stretch | For whoever finishes in 40 minutes. Never required. |

Mark up a question with the furniture that `print.css` provides:

```html
<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> What does this print?
<div class="lines"><i></i><i></i><i></i></div>
</div>
```

`<div class="lines"><i></i>…</div>` gives ruled answer space, one `<i>` per line.
`<div class="sketchbox" data-label="Draw your state diagram here"></div>` gives an empty box.
`<ul class="checkpoints">` gives tick-boxes for the build checkpoints.

### Section D must fit in 70 minutes

Time it. If you cannot finish it yourself in 35 minutes, a student cannot finish it in 70. Cut it,
and move what you cut into Stretch.

---

## 5. Write the solutions

`solutions/` answers **every** question in A–D, and for E gives *marking notes* instead of an answer:
what a strong response notices, what a weak one misses, and the name of the real technique if the
student has just invented one.

> Keep the names out of the student-facing text. A student who invents spatial partitioning and is
> then told it is in every game engine has learned something a lecture cannot deliver.

---

## 6. Build the handout

```bash
python3 tools/build_handouts.py webgames/beginner_lvl    # one level
python3 tools/build_handouts.py                          # everything
```

The pipeline is `exercises.md` → HTML with `shared/css/print.css` → headless Chrome → PDF. It needs
**Chrome and nothing else**: no LaTeX, no pandoc, no `wkhtmltopdf`.

**Always open the PDF and look at it.** Check specifically that no code block is clipped at the right
edge and that no question is split across a page break. Those two defects make a handout useless and
neither shows up in any automated check.

---

## 7. Verify

```bash
bash tools/check_all.sh --quick   # while writing: syntax, compile, links
bash tools/check_all.sh           # before committing: adds the Chrome pass
```

The Chrome pass loads every page in a real browser and fails on any console error, which is how we
catch a visualizer that silently dies. It takes a couple of minutes.

What the checks **cannot** tell you, and you must do by hand:

- Does the visualizer actually animate, step and reset? Open it and click.
- Does the turtle/tkinter picture actually *look* right? `check_turtle.py` proves the code runs
  without exceptions; only a human can see that the board is the right way up.
- Is the PDF laid out properly? Look at it.
- Does section D fit in the time? Do it yourself with a timer.

---

## 8. Working with `anim.js`

A visualizer is a config object. `anim.js` supplies the loop, the controls, the theming, the canvas
scaling and the draggable handles.

```javascript
var sk = Anim.sketch({
  mount: '#myDemo',
  width: 900, height: 420,      // LOGICAL size; the canvas scales to fit
  fps: 60,                      // length of one logical frame = 1/fps
  controls: ['play', 'step', 'reset', 'speed'],
  state: function () { return { x: 0 }; },      // called on start and on reset
  update: function (s, dt, api) { s.x += 120 * dt; },
  draw: function (s, g, api) { g.clear(); g.circle(s.x, 100, 20, g.color.accent); }
});
```

### Rules

- **Draw in logical coordinates.** A sketch declared 900×420 always draws in a 900×420 space,
  whatever size it ends up on screen. Never think about pixels or `devicePixelRatio`.
- **Colours come from `g.color`**, which is read from the `--anim-*` CSS properties, so your sketch
  works in light mode, dark mode and print. Never hard-code a hex value.
- **Add extra controls with `sk.slider()`, `sk.toggle()` and `sk.button()`.** These redraw the canvas
  on change. A hand-built `<input>` will appear to do nothing while the sketch is paused, because
  `anim.js` listens to `ResizeObserver` rather than the window `resize` event.
- **If the sketch animates, it must offer `step`.** `check_pages.js` enforces this by looking for an
  `update()` in the source. A purely interactive sketch — drag two boxes, watch a test flip — needs
  only `reset`.
- `api.handle(name, x, y, opts)` makes a draggable point. Call it from `draw()`; it paints itself and
  returns its current position. Pass `{hidden: true}` to read the position before drawing other
  things on top of it, then call it again without `hidden` to paint it last.
- `api.say(html)` writes the caption under the canvas. Use it to narrate what just happened, so a
  student reading alone gets what the teacher would have said out loud.

### Drawing helpers on `g`

`clear` · `rect` · `strokeRect` · `circle` · `ring` · `line` · `dashed` · `arrow` · `text` · `badge` ·
`grid` · `panel` · `alpha` · and `g.ctx` for the raw 2D context when you need a curve.

`arrow` is how you draw a vector, and `badge` is a label with a plate behind it so it stays readable
over something busy.

### Adding a new theme colour

Three places in `notes.css`, or it will be wrong in dark mode: `:root`, the
`@media (prefers-color-scheme: dark)` block, and the `:root[data-theme="dark"]` block.

---

## 9. Code-block markup in a visualizer page

```html
<div class="code" data-lang="js" data-file="game.js" data-hl="4,7-9">
<pre><code>// your code, with &lt; and &amp; escaped</code></pre>
</div>
```

`data-lang` picks the highlighter (`js`, `python`, `cpp`, `bash`) and labels the block.
`data-hl` highlights lines — use it for "this is the new bit".
`data-numbers="off"` turns off line numbers, which is right for short snippets.

The highlighter is ours, in `codeblock.js`, because a CDN `<script>` tag is a lesson that fails on the
one morning the network is down. If you touch it: **comments and strings must be matched before
keywords**, or a keyword inside a comment gets coloured. That is the classic bug in hand-rolled
highlighters and there is a test for it.
