# Lesson 6 — Capstone: ASCII Arcade

> **Games with C++ · Beginner level · Lesson 6 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**ASCII Invaders** — a complete arcade game, split across **several files**, built with a
**Makefile**, and running on a **fixed timestep**.

```
  ##############################################
  #   score 1240      lives @@@       wave 3   #
  #                                            #
  #    WWW   WWW   WWW   WWW   WWW   WWW       #
  #    WWW   WWW   WWW         WWW             #
  #           |                                #
  #                      |                     #
  #                                            #
  #                /^\                         #
  ##############################################
```

Two new ideas, both about **building software** rather than about games: splitting a program across
files, and a loop whose physics does not depend on the frame rate.

## Where this fits

- **Back:** [lesson 5](../lesson-05-many-things-at-once/notes.md) gave you vectors and smooth
  movement.
- **Forward:** the intermediate level, which adds `raylib` and real graphics.
- **Today:** the last lesson of the beginner track, and the first time your program is more than one
  file.

---

## The idea, in plain words

### One file stops working

Your Pong is about 300 lines. This game is more like 600. At that size, one file has real problems:

- You cannot find anything.
- Changing one line means **recompiling everything**, which gets slow.
- Two people cannot work on it at once.
- Nothing tells you which parts are meant to be used by which other parts.

### Headers and source files

C++ splits a program in two kinds of file:

| File | Holds | Think of it as |
|---|---|---|
| `screen.h` | **declarations** — what exists | the menu |
| `screen.cpp` | **definitions** — how it works | the kitchen |

```cpp
// ---- screen.h : WHAT EXISTS ----
#pragma once                  // only include this file once per compile

const int WIDTH = 46;
const int HEIGHT = 20;

void clear(char background);
void put(int x, int y, char c);
void present(const std::string& status);
```

```cpp
// ---- screen.cpp : HOW IT WORKS ----
#include "screen.h"

static char buffer[WIDTH * HEIGHT];   // "static" = private to this file

void put(int x, int y, char c) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) { return; }
    buffer[y * WIDTH + x] = c;
}
```

Any other file that wants to draw writes `#include "screen.h"` and can call `put()` — without knowing
or caring how it works. That separation is the point: **the header is a promise about what is
available; the .cpp is the fulfilment.**

> `#include <iostream>` with angle brackets means "look in the standard library".
> `#include "screen.h"` with quotes means "look next to this file first". Use quotes for your own
> files.

### `#pragma once`

If two files both include `screen.h`, the compiler would see those declarations twice and complain.
`#pragma once` at the top says *"only read this file once per compilation"*. Put it at the top of
every header, always.

(You will also see the older form — `#ifndef SCREEN_H` / `#define SCREEN_H` / `#endif` — called an
*include guard*. It does the same job and works everywhere; `#pragma once` is shorter and is
supported by every compiler you will realistically meet.)

### Compiling several files

```bash
clang++ -std=c++17 -Wall main.cpp game.cpp screen.cpp terminal.cpp -o invaders
```

That works, and it recompiles everything every time. The better way is a **Makefile**:

```makefile
CXX = clang++
CXXFLAGS = -std=c++17 -Wall
OBJECTS = main.o game.o screen.o terminal.o

invaders: $(OBJECTS)
	$(CXX) $(OBJECTS) -o invaders

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) invaders
```

Then you type `make`, and it **only recompiles the files that changed**. Change `game.cpp` and it
rebuilds `game.o` and relinks; it does not touch the other three.

> **Warning: Makefiles require tab characters.** The indented lines must start with a real tab, not
> spaces. This is a notorious trap, the error message is unhelpful, and most editors will silently
> convert tabs to spaces unless told otherwise. If `make` says `missing separator`, that is what
> happened.

### Compiling and linking are two different steps

This is worth getting straight, because the error messages are completely different:

1. **Compiling** turns each `.cpp` into a `.o` *object file*, separately. The compiler only needs the
   **declarations** from headers to do this.
2. **Linking** joins all the `.o` files into one executable, matching up every call with its
   definition.

So:

- `error: use of undeclared identifier 'put'` → a **compile** error. You forgot to `#include` the
  header.
- `Undefined symbols for architecture ...: "put(int, int, char)"` → a **link** error. The declaration
  exists, but no `.cpp` actually defines it, or you forgot to pass that `.cpp` to the compiler.

Students lose a lot of time here because the two look similar and are not. Read which step failed.

### The fixed timestep

Your games so far have used **delta time**: multiply everything by how long the last frame took. That
works, and it has a flaw.

If one frame takes a long time — the machine stalls, the window is dragged, the laptop sleeps — `dt`
becomes large, and everything takes one enormous step. A fast bullet can jump straight **through** an
alien without ever overlapping it. That is **tunnelling**, which the web track meets in its lesson 4.

The fix is to stop letting the physics see a variable `dt` at all:

```cpp
const double STEP = 1.0 / 60.0;     // the physics ALWAYS advances by this
double accumulator = 0.0;

while (running) {
    double frame_time = measure_how_long_since_last_frame();
    if (frame_time > 0.25) { frame_time = 0.25; }   // never catch up more than this

    accumulator += frame_time;

    // Run as many FIXED steps as fit into the time that has passed.
    while (accumulator >= STEP) {
        update(STEP);              // ALWAYS exactly 1/60 of a second
        accumulator -= STEP;
    }

    draw();
}
```

Now `update()` always receives exactly the same `dt`. A slow frame runs the update **twice** instead
of once with a doubled step — so the steps never get bigger, and tunnelling cannot happen.

Three things worth understanding about it:

- **The accumulator keeps the leftovers.** Subtracting `STEP` rather than zeroing it means no time is
  lost, so the game stays exactly in step with the real world.
- **The clamp prevents the "spiral of death".** Without it, a ten-second stall would try to run 600
  updates in one frame, which takes even longer, which makes the next gap bigger, and the game never
  recovers.
- **The game becomes repeatable.** Given the same inputs, it produces exactly the same result every
  time — which is what makes replays and online multiplayer possible at all.

> This is the first lesson of the **advanced** level, arriving early. You do not need to master it
> today. You need to have seen it, and to know what problem it solves.

---

## The idea, in pictures

Open [the delta-time explainer](../../../shared/visualizers/delta-time.html).

**What to look for:** drag the frame rate slider and watch the frame-counting ball fall apart. Delta
time fixed *that*. The fixed timestep fixes the next problem along — what happens when one frame is
enormous.

Then open [the box collision explainer](../../../shared/visualizers/aabb-collision.html).

**What to look for:** drag the boxes so they only just touch. Now imagine the orange box jumping
from one side to the other in a single frame, never passing through this position. That is what the
fixed timestep prevents.

---

## The maths you just used

### The accumulator

> **steps this frame = how much time has built up ÷ STEP**, with the remainder kept for next time.

With `STEP = 1/60` and a frame that took 0.05 seconds:
`0.05 ÷ 0.0167 = 2.99`, so **two** updates run and `0.0167` seconds stays in the accumulator for next
frame. Nothing is lost and nothing is double-counted.

### Waves that get harder, with a floor

```cpp
double alien_speed = 2.0 + wave * 0.6;
double shoot_delay = std::max(0.45, 1.6 - wave * 0.15);
```

Same shape as every difficulty curve in this course: a slope, and a **limit**. Design them together,
or the game eventually becomes impossible rather than hard.

---

## Break it on purpose

Use the project in `code/`. Run `make` each time.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Replace the fixed timestep with `update(frame_time)` and stall the game | | |
| Remove the `frame_time > 0.25` clamp and suspend your laptop briefly | | |
| Delete `#pragma once` from a header | | |
| Remove `screen.cpp` from the Makefile's `OBJECTS` | | |
| Replace the tab at the start of a Makefile rule with spaces | | |
| Call a function declared in `game.h` but defined nowhere | | |

Numbers four and six both give **linker** errors, not compiler errors. Read them carefully — learning
to tell the two apart will save you hours over the next few years.

---

## Think like an engineer

1. **Your project has four `.cpp` files.** Could you reuse any of them, unchanged, in a completely
   different game? Which ones, and what makes the difference?
2. `screen.cpp` uses `static char buffer[...]`, so no other file can touch it directly. **Why is that
   better than making it available everywhere?** What would go wrong if any file could write to it?
3. **Design the file split for a different game** — a platformer, say. What files would you make, and
   what goes in each? There is no single right answer, and arguing about it is most of what software
   architecture is.
4. **The big one.** You have now built four games in C++: dice, a battle, a maze, and Pong — and
   today a fifth. **Design the part that is left over when you take the game out of the game.** What
   would be in your reusable skeleton? What must always stay specific? *(That is what a game engine
   is, and it is what `raylib` is somebody else's answer to.)*

---

## Vocabulary

| Word | What it means |
|---|---|
| **Header** (`.h`) | Declarations: what exists. |
| **Source** (`.cpp`) | Definitions: how it works. |
| **`#pragma once`** | Only read this header once per compile. |
| **Object file** (`.o`) | One compiled `.cpp`, before linking. |
| **Linking** | Joining object files into one executable. |
| **`static`** (at file scope) | Private to this file. |
| **Makefile** | A recipe saying how to build, and what depends on what. |
| **Fixed timestep** | Physics always advances by the same amount. |
| **Accumulator** | The built-up time waiting to be spent on fixed steps. |

---

## Recap

- Split a growing program into **headers** (what exists) and **source files** (how it works).
- `#pragma once` at the top of every header. Quotes for your files, angle brackets for the library.
- **Compiling and linking are different steps** with different error messages. Read which one failed.
- A **Makefile** rebuilds only what changed — and its rules must start with a **tab**.
- A **fixed timestep** gives `update()` the same `dt` every time, which prevents tunnelling and makes
  the game repeatable.
- **Clamp the accumulator**, or a long stall becomes a spiral the game never recovers from.

---

## Stretch goals

1. **Power-ups** dropped by destroyed aliens: a faster gun, a shield, a second cannon.
2. **A boss wave** every fifth wave, with more health and a different movement pattern.
3. **Save the high score** to a file, handling a missing or damaged file without crashing.
4. **A `--debug` command-line flag** that draws hitboxes and the frame timing. Look up how `main`
   receives `argc` and `argv`.
5. **Split it further.** Pull the alien logic into `aliens.h`/`aliens.cpp`. Did that make it clearer
   or just more files? Be honest.
6. **Make it yours.** Change the theme, the rules, the shape of the waves. This is the real one.

---

## Teacher notes

**Timing**

This is mostly a long build. Resist teaching.

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Show the finished game, then `ls` the folder and show that it is six files. Run `make`, change one line, run `make` again and let them see only one file rebuild. |
| 10–30 | **Concept.** Headers versus source, then compile versus link. Do the error-message comparison on the projector — it is the thing they will actually need. |
| 30–40 | **Live-code** a two-file split of something tiny, and a four-line Makefile. |
| 40–50 | Break. |
| 50–135 | **Build.** They will need all of it. |
| 135–145 | **Show-and-tell.** Protect this. |
| 145–150 | Where next: the intermediate level and `raylib`. |

**The fixed timestep is a bonus, not a requirement.** It is genuinely an advanced-level topic. Give
them the loop, explain the problem it solves, and let them use it. A student who leaves understanding
*why* it exists has got what they need; one who can derive it is ahead of schedule.

**What usually goes wrong**

1. **`make: *** missing separator. Stop.`** Spaces instead of a tab. Notorious, unhelpful, and
   near-universal. Tell them before they hit it and show them how to make their editor show
   whitespace.
2. **Undefined symbols at link time.** A `.cpp` missing from the Makefile, or a function declared and
   never defined. Teach them to read the symbol name in the error — it names exactly what is missing.
3. **"Redefinition" errors.** A missing `#pragma once`, or a variable *defined* in a header rather
   than declared. Defining a non-`const` variable in a header is a classic and the error is confusing.
4. **Changes that seem to do nothing.** They edited a file not in the Makefile, or an old build is
   being run. `make clean && make` settles it.
5. **Everything in `main.cpp` anyway.** The commonest outcome if you do not check. Circulate early.
6. **The game runs at the wrong speed after adding the fixed timestep.** Usually `accumulator = 0`
   instead of `accumulator -= STEP`, which throws away the leftovers.

**If you are running short on time** — give them the whole `code/` folder as a starting point and have
them *extend* it: add a power-up, a boss, a new alien type. Reading and modifying a multi-file project
is a genuinely valuable skill, and it is closer to what they will actually do later than building one
from nothing.

**For the student who finishes at minute 90** — stretch goal 5 (split it further) is the most
instructive, precisely because the honest answer is often "that made it worse". Learning that more
files is not automatically better organisation is a real and slightly surprising lesson.

**Marking a capstone.** Not on features. On:
- Does it build with `make` and run?
- Is it genuinely split, with headers declaring and sources defining?
- Can they explain any function you point at?
- **Did they change something to make it theirs?**

**What to say at the end of the C++ track.** Put lesson 1's `01-hello.cpp` next to today's project.
Six lines next to six files. Then point out that the *shape* never changed: state, a loop, input,
update, render — the same structure they met on day one of whichever track they started with.

Then tell them the honest truth about what comes next: `raylib` at intermediate level will give them
pixels, textures and sound, and will not give them a single new idea about how a game is
*structured*. They already have that.
