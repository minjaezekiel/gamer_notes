# Lesson 6 — Capstone: ASCII Arcade

## Cheat sheet

### Headers and sources

| File | Holds | Think of it as |
|---|---|---|
| `screen.h` | **declarations** — what exists | the menu |
| `screen.cpp` | **definitions** — how it works | the kitchen |

```cpp
// screen.h
#pragma once
void put(int x, int y, char c);

// screen.cpp
#include "screen.h"
static char buffer[WIDTH * HEIGHT];   // private to this file
void put(int x, int y, char c) { ... }
```

`#include "mine.h"` — quotes for your files
`#include <iostream>` — brackets for the library
`#pragma once` — at the top of **every** header

### Compile vs link

| Error | Step | Cause |
|---|---|---|
| `use of undeclared identifier 'put'` | **compile** | missing `#include` |
| `Undefined symbols: "put(int,int,char)"` | **link** | no `.cpp` defines it, or it is missing from the build |

Read **which step** failed. They look similar and are not.

### Makefile

```makefile
CXX = clang++
CXXFLAGS = -std=c++17 -Wall
OBJECTS = main.o game.o screen.o

invaders: $(OBJECTS)
→	$(CXX) $(OBJECTS) -o invaders

%.o: %.cpp
→	$(CXX) $(CXXFLAGS) -c $< -o $@
```

**`→` must be a REAL TAB.** Spaces give `missing separator` and no hint why.

`$<` = the input · `$@` = the output · `-c` = compile only

### The fixed timestep

```cpp
const double STEP = 1.0 / 60.0;
accumulator += frame_time;
while (accumulator >= STEP) {
    update(STEP);          // ALWAYS the same dt
    accumulator -= STEP;   // SUBTRACT, do not zero
}
```

- **Clamp `frame_time`** (≤ 0.25 s) or a long stall becomes a spiral of death.
- Steps never get big → **no tunnelling**.
- Same inputs → same result → **replays and multiplayer are possible**.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What goes in a <code>.h</code> file and what goes in a <code>.cpp</code>? Why split them at all?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does <code>#pragma once</code> do, and what happens without it?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Explain the difference between <em>compiling</em> and <em>linking</em>. Give an error message that belongs to each.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> What problem does a fixed timestep solve that delta time does not?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why <code>accumulator -= STEP</code> rather than <code>accumulator = 0</code>? And why clamp <code>frame_time</code>?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> <code>STEP</code> is 1/60. A frame took <strong>0.05 s</strong>. How many times does <code>update</code> run, and what is left in the accumulator? Now the next frame takes 0.005 s &mdash; how many times then?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> Which step fails, and why?

```cpp
// game.cpp
#include "screen.h"
void draw() { put(1, 1, '@'); }
```

...and `screen.cpp` is left out of the Makefile's `OBJECTS`.

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> A student edits <code>screen.h</code> and runs <code>make</code>. Nothing rebuilds. What is missing from the Makefile, and what will they experience?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> The laptop is suspended for <strong>10 seconds</strong> mid-game. Describe what happens with each version.

```cpp
// version A - delta time
update(frame_time);

// version B - fixed timestep, no clamp
accumulator += frame_time;
while (accumulator >= STEP) { update(STEP); accumulator -= STEP; }

// version C - fixed timestep, clamped to 0.25
```

<div class="lines"><i></i><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> <code>make</code> says <code>Makefile:12: *** missing separator. Stop.</code> What is wrong, and why is the message so unhelpful?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> This compiles, but the linker complains that <code>WIDTH</code> is defined more than once. Why &mdash; and why does the <code>const int</code> version work?

```cpp
// screen.h
#pragma once
int WIDTH = 46;
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The game runs at roughly half speed. The frame rate is fine. What is wrong?

```cpp
accumulator += frame_time;
if (accumulator >= STEP) {
    game_update(STEP);
    accumulator = 0.0;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

This is the capstone. 85 minutes. You may start from the project in `code/` and extend it, or build
your own arcade game from scratch.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Split your lesson 5 Pong into at least <code>screen.h</code>/<code>screen.cpp</code> and <code>main.cpp</code>. Get it compiling with one long <code>clang++</code> command.</li>
<li><strong>Checkpoint 2.</strong> Write a Makefile. Prove it works incrementally: change one <code>.cpp</code>, run <code>make</code>, and check only that file rebuilds.</li>
<li><strong>Checkpoint 3.</strong> Add <code>terminal.h</code>/<code>terminal.cpp</code> so the raw-mode code lives in one place and nothing else mentions <code>termios</code>.</li>
<li><strong>Checkpoint 4.</strong> Build the game itself in <code>game.h</code>/<code>game.cpp</code>, keeping <code>main.cpp</code> to just the loop. Aliens or asteroids, bullets, a player, collisions, a score.</li>
<li><strong>Checkpoint 5.</strong> Replace delta time with a <strong>fixed timestep</strong>, with the accumulator and the clamp.</li>
<li><strong>Checkpoint 6.</strong> Add waves that get harder (with a <em>floor</em>), lives, a menu and a game-over screen. Then <strong>change something to make it yours.</strong></li>
</ul>

<div class="note">
<span class="note-label">How this is marked</span>
<p>Not on features. On: does it build with <code>make</code> and run; is it genuinely split, with
headers declaring and sources defining; can you explain any function I point at; and
<strong>did you change something to make it yours?</strong></p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Your project has four `.cpp` files. **Could you reuse any of them, unchanged, in a completely
different game?** Which, and what makes the difference between the reusable ones and the rest?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** `screen.cpp` keeps its buffer `static`, so no other file can touch it directly. **Why is that
better than making it available everywhere?** What would go wrong if any file could write to it?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** **Design the file split for a different game** — a platformer, say. What files, and what goes
in each?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4. The big one.** You have built five games in C++ now. **Design the part that is left over when
you take the game out of the game.** What would be in your reusable skeleton? What must always stay
specific to one game?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Power-ups dropped by destroyed aliens.
2. A boss wave every fifth wave.
3. Save the high score, surviving a missing or damaged file.
4. A `--debug` flag that draws hitboxes. (Look up `argc` and `argv`.)
5. **Split it further** into `aliens.h`/`aliens.cpp`. Did that help, or is it just more files? Be
   honest.
6. **Make it yours.**
