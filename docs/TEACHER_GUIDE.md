# TEACHER_GUIDE — running this course

Written for a teacher who is **not** a game developer. You do not need to be one. You need to be able
to read a lesson the night before, run the code once, and manage a room.

---

## The ten minutes of preparation that matter most

Open [`shared/visualizers/index.html`](../shared/visualizers/index.html) and click through all nine
explainers. Press **Step 1 frame** on each. That is the whole conceptual content of the beginner
course, and once you have seen it you can teach it.

Then, for the specific lesson: run every file in the lesson's `code/` folder yourself. Not to check
them — they are verified — but so that when a student's screen looks wrong you recognise it.

---

## The shape of a 2 h 30 m lesson

| Minutes | Block | What you are doing |
|---|---|---|
| 0–10 | **Hook** | Play the finished game. Or show the broken thing you are about to fix. Do not explain anything yet. |
| 10–25 | **Concept** | The visualizer, on the projector. **Laptops closed.** |
| 25–40 | **Live code** | Build the smallest working version together, with everyone typing along. |
| 40–50 | **Break** | A real break. They have been going for 40 minutes. |
| 50–120 | **Build** | Exercises section D. You circulate. This is the bulk of the lesson. |
| 120–140 | **Break it** | The *break it on purpose* experiments, then share-outs. |
| 140–150 | **Land it** | Recap, vocabulary, point at the stretch goals. |

Each lesson's **Teacher notes** section adapts this and tells you where to cut.

### Why laptops closed during the concept

Because a laptop is more interesting than you are, and that is not a criticism of you. Fifteen minutes
of genuine attention on the visualizer buys you an hour of productive building. Fifteen minutes
competing with a screen buys you neither.

### Make them predict before you press Step

The highest-value move in this entire course is four words: **"what happens next?"**

Pause the visualizer. Ask the class to predict. Take two or three answers, including wrong ones,
without correcting them. *Then* press Step. A student who predicted wrong and saw it has learned
something that cannot be transmitted by explanation. Being wrong in public, with no stakes, is the
mechanism — so never make the wrong answer costly.

---

## Circulating during the build

Your job for those 70 minutes is **not** to fix code. It is to ask questions.

| Instead of | Say |
|---|---|
| "You're missing a bracket on line 12." | "What's the last line you're sure works?" |
| "Add delta time there." | "Would this behave the same on a slower laptop?" |
| *typing on their keyboard* | "Show me what you expected to happen, then what happened." |
| "That's wrong." | "What would you expect to see if that were right?" |

**Do not touch their keyboard.** Once you do, the fix is yours and not theirs, and they have learned
that getting stuck means waiting for an adult.

### The question that unsticks almost anyone

> "Print the value just before the line that breaks. What is it?"

Most beginner bugs are a variable holding something other than what the student assumed. Teaching
them to *look* rather than *reason* is the single most valuable debugging habit, and it transfers to
every language.

---

## Differentiation

### The student who finishes in 40 minutes

They exist in every class. Every lesson has **Stretch goals** for exactly this, and they are never
required, so a student who does none has still completed the lesson.

Three options, in order of preference:

1. Point them at the stretch goals. These are designed to be genuinely harder, not just more of the
   same.
2. Ask them to make the game *feel* better rather than do more. "Make the ball bounce feel satisfying"
   is open-ended, has no finish line, and teaches game feel — which is the hardest thing in the course.
3. Ask them to help a neighbour **without touching their keyboard**. Explaining is how you find out
   you did not quite understand. Enforce the no-keyboard rule or they will just do it for them.

### The student who is badly stuck

Usually one of four things, in this order of likelihood:

1. **A typo.** Check spelling and brackets before anything else.
2. **They are editing a different file from the one they are running.** Astonishingly common.
3. **They skipped a step** in section D and are two checkpoints ahead of their code.
4. **They do not understand the concept** — the rarest cause, though it is the one we assume first.

Make them say out loud what the line they are stuck on is supposed to do. They often debug it
themselves mid-sentence. That is not a trick; it is how understanding works.

### Mixed experience in one room

Some students will have coded before. Pair them with someone who has not, and give the **less**
experienced student the keyboard. Make this explicit and non-negotiable or the experienced one will
take over within four minutes and both will learn less.

---

## Assessment

### What to mark

| Section | How to mark it |
|---|---|
| A — Recall | Right or wrong. Quick. |
| B — Predict the output | Mark the *prediction*, not the final answer. A wrong prediction with sound reasoning is worth more than a right one copied from running the code. |
| C — Find and fix the bug | Did they find it? Can they say *why* it was wrong? The second part is the real question. |
| D — Hands-on build | Checkpoints. Reaching checkpoint 4 of 6 is a clear, honest, non-punitive result. |
| E — Design challenge | See below. |

### Marking the design challenges

These have **no answer key**, on purpose. Mark them on:

- **Did they consider the trade-off?** Every design answer costs something. Naming the cost is the
  skill.
- **Is the reasoning followed through?** "Store only the walls, because most of the map is empty" is a
  good answer even if incomplete.
- **Did they consider the player?** The best answers in this course talk about how something *feels*.

A student who reaches a different conclusion from ours with good reasoning gets full marks. Say this
out loud when you set the work, or they will hunt for the answer you want instead of thinking.

Several prompts ask students to invent something that has a real name — spatial partitioning, sparse
storage, state machines. **Do not give the name first.** The solutions file has the names, for you.
"What you just described is called a uniform grid and it is in every game engine" is a sentence worth
waiting for.

---

## Room and machine setup

### Before the first lesson

- [ ] Check that every machine can run the track's hello-world. Five minutes per machine now saves
      the first lesson.
- [ ] Python track: check `python3 -c "import tkinter"` works. On some Linux installs `tkinter` is a
      separate package, and that is the only setup surprise in the whole beginner Python track.
- [ ] C++ track: check the compiler is on the PATH and that students can write to a folder.
- [ ] Decide where students save their work, and tell them. "I lost it" costs more lessons than any
      bug.
- [ ] Print the lesson 1 handouts.
- [ ] Open the visualizer gallery on the projector machine and leave the tab open.

### Things that go wrong, and the fix

| Symptom | Cause | Fix |
|---|---|---|
| Visualizer widget is blank | the page cannot reach `../js/anim.js` | the `shared/` folder was moved, or the file was copied out of the repo alone |
| Student's canvas is blank | they are opening the wrong file, or there is a typo in the `<canvas>` id | open the browser console (<kbd>F12</kbd>) and read the red text |
| Python window opens then closes instantly | the script ends, so the window closes | the examples all have a loop or `mainloop()`; they have probably deleted the last line |
| C++ "command not found" | compiler not installed or not on the PATH | `clang++ --version` to confirm |
| Nothing works and Wi-Fi is down | — | nothing here needs the internet. Look for a different cause. |

### Projector notes

Dark mode usually projects better in a bright room — the button is in the top-right of every page, and
the choice is remembered on that machine. The visualizers are readable from the back of a room by
design, but check from the back row once.

You can drive any visualizer from the keyboard, so you can teach from anywhere in the room:
<kbd>Space</kbd> play/pause, <kbd>&rarr;</kbd> step one frame, <kbd>R</kbd> reset. Most presenter
remotes send those keys.

---

## Which track to teach

| If… | Teach |
|---|---|
| machines are locked down, or it is a short course | **web** — nothing to install, and students can share a link |
| students already learn Python in another subject | **python** — the transfer is immediate and motivating |
| students are older, confident, and heading for CS | **c++** — it is the honest one about how computers work |
| you have a full year | **web, then python** — the second track is much faster because the ideas are already in place |

Teaching two tracks is **not** twice the work for the student. The concepts carry over, which is the
entire design. The second track typically runs at close to double speed, and students report that the
second time is when they actually understood the first.

---

## If you only have one week

Lessons 1, 2, 4 and 5 of any beginner track give a complete, playable Pong-equivalent and cover the
game loop, delta time, collision and game states. Skip lesson 3 by giving students the input-handling
code, and skip the capstone. You lose the decomposition and data-driven-design content, which is the
right thing to lose if something must go.

---

## A last thing

The goal of this course is **not** that students can build Pong. It is that a student looks at a game
and thinks *I could work out how that is done*. Every time you are tempted to give an answer, you are
trading a small amount of time now for that outcome later. Ask a question instead.
