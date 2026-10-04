# Lesson 3 — Drawing With Letters

> **Games with C++ · Beginner level · Lesson 3 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A dungeon that **animates** — a torch flickering, water rippling, a bat flapping across the room — at
a steady frame rate, drawn entirely out of letters.

```
  ################################
  #......................#.......#
  #..~~~~................#...*...#
  #..~~~~......v.........#.......#
  #......................#########
  #...........@..................#
  ################################
     frame 142    58.9 fps
```

And you will have built a **screen buffer**, which is how every graphics system in the world works —
including the one drawing this page.

## Where this fits

- **Back:** [lesson 2](../lesson-02-a-game-is-data/notes.md) gave you structs and references.
- **Forward:** [lesson 4](../lesson-04-input-and-movement/notes.md) lets the player move.
- **Today:** rendering, frame timing, and the idea that a 2-D picture is really a 1-D line of memory.

---

## The idea, in plain words

### Printing straight to the screen does not work

The obvious approach is to print each row as you work it out:

```cpp
// DO NOT DO THIS in a loop
for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
        std::cout << work_out_character(x, y);
    }
    std::cout << "\n";
}
```

Run that sixty times a second and the result **flickers horribly**. You are watching the picture be
assembled, line by line, and the terminal is scrolling constantly.

### A screen buffer

Instead, keep a grid of characters in memory. Each frame:

1. **Clear** the buffer — fill it with the background character.
2. **Draw** into the buffer — walls, water, the player, everything.
3. **Show** it — print the whole thing in one go.

Nothing reaches the screen until the picture is finished.

> **You have met this before.** This is exactly `tracer(0)` and `update()` in the Python track, and
> exactly "erase, then draw" in the web track. It has a name: **double buffering**, and every
> graphics system does it, from a terminal game to a modern GPU. You are now building it yourself
> rather than being handed it.

### A grid is really one long line

Here is the idea that matters most today.

You could store the buffer as a 2-D array, and C++ lets you. But memory has no concept of a grid —
it is one long line of bytes. So the professional habit is to use a **flat array** and do the maths
yourself:

```cpp
const int WIDTH = 32;
const int HEIGHT = 7;

char screen[WIDTH * HEIGHT];           // one long line of 224 characters

// To get at the square at (x, y):
int index = y * WIDTH + x;
screen[index] = '#';
```

Read `y * WIDTH + x` as: **"skip y whole rows, then count x more across."** Each whole row you skip
is `WIDTH` characters long.

And the reverse:

```cpp
int x = index % WIDTH;        // the remainder: how far across
int y = index / WIDTH;        // the whole part: how many complete rows
```

That is long division, split into its two halves. You met `%` in lesson 1.

Why bother, when a 2-D array exists? Three reasons: it is how files and images actually store pixels;
it is faster, because all the data sits together in memory; and once you can do this conversion, you
can read any image format, any tile map, and any level file ever written.

### Putting a character in the buffer, safely

```cpp
void put(int x, int y, char c) {
    // ALWAYS check the bounds. Writing outside the array does not raise an
    // error in C++ - it quietly corrupts whatever happens to live next to it in
    // memory, and the program misbehaves somewhere else entirely, much later.
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) {
        return;
    }
    screen[y * WIDTH + x] = c;
}
```

> **This is the most important safety habit in C++.** Python raises `IndexError`. JavaScript gives
> you `undefined`. C++ writes into memory it does not own and carries on as though nothing happened.
> The crash, if it comes at all, comes later and somewhere unrelated — which makes it one of the
> hardest kinds of bug to find. Write the bounds check every time, from today.

### Clearing the terminal

```cpp
std::cout << "\033[2J\033[H";
```

That is an **ANSI escape sequence** — a string the terminal interprets as a command rather than
printing. `\033` is the escape character, `[2J` means "clear the screen", `[H` means "put the cursor
back at the top-left".

Alternatively, `\033[H` alone moves the cursor home **without** clearing, so the new frame overwrites
the old one in place. That flickers less, and it is what the example code uses.

### Frames that take the right amount of time

Your drawing is fast. Without something to slow it down, the loop runs thousands of times a second
and the animation is a blur.

```cpp
#include <chrono>
#include <thread>

using Clock = std::chrono::steady_clock;

auto frame_start = Clock::now();

// ... do the frame's work ...

auto frame_end = Clock::now();
auto elapsed = frame_end - frame_start;
auto target = std::chrono::milliseconds(16);     // about 60 fps

if (elapsed < target) {
    std::this_thread::sleep_for(target - elapsed);
}
```

Read it as: note the time, do the work, see how long it took, and **sleep for whatever is left** of
the frame's budget.

Note `steady_clock`, not `system_clock`. The system clock can jump — if the machine syncs with a time
server, or the user changes the clock, or daylight saving begins. `steady_clock` only ever moves
forward at a steady rate, which is what you want for measuring a duration.

### Delta time, in C++

```cpp
auto now = Clock::now();
std::chrono::duration<double> delta = now - last_time;
last_time = now;
double dt = delta.count();         // seconds, as a decimal

if (dt > 0.1) { dt = 1.0 / 60.0; } // clamp, exactly as in the other tracks
```

`duration<double>` asks for the gap measured in seconds as a decimal number, and `.count()` gets that
number out. Same idea as `time.time()` in Python and `requestAnimationFrame`'s timestamp in
JavaScript, with more types involved.

---

## The idea, in pictures

Open [the grids and flat arrays explainer](../../../shared/visualizers/tilemap-indexing.html).

**What to look for:** drag the marker around the grid and watch the formula fill in with real
numbers. Move **one square right** and the index changes by **1**; move **one square down** and it
jumps by a whole **WIDTH**. The coloured strip underneath is your `screen` array — the grid's rows,
cut out and laid end to end. That strip *is* what your buffer looks like in memory.

Then open [the coordinates explainer](../../../shared/visualizers/coordinates.html).

**What to look for:** the right-hand grid. Your buffer's row 0 is the **top** row and y grows
**downwards** — the same convention as tkinter, the web canvas and every graphics system except
turtle.

---

## The maths you just used

### `y * WIDTH + x`, and its reverse

> **index = y × WIDTH + x**
> **x = index % WIDTH**  ·  **y = index ÷ WIDTH**

Check it with real numbers. With `WIDTH = 32`, the square at `(5, 3)` is at
`3 × 32 + 5 = 101`. And back: `101 % 32 = 5`, `101 / 32 = 3`. ✓

### Making things wobble with `sin`

```cpp
#include <cmath>
int wobble = (int)(std::sin(time * 3.0) * 4.0);
```

`std::sin` takes an angle and gives a number that slides smoothly between **−1 and +1**, over and
over, forever. You do not need to know why yet. What matters is the shape of its behaviour:

- Multiply by `4.0` and it slides between −4 and +4 — the size of the wobble.
- Multiply the *input* by `3.0` and it wobbles three times as fast — the speed.

That pattern — `sin(time * speed) * size` — is behind almost every gentle repeating motion in games:
bobbing items, breathing lights, swaying grass, floating platforms. It is worth memorising long
before you understand the trigonometry.

---

## Break it on purpose

Use `code/03-animated-dungeon.cpp`. Compile each time.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the bounds check from `put()` and draw at x = 999 | | |
| Change `y * WIDTH + x` to `x * WIDTH + y` | | |
| Remove the `sleep_for` entirely | | |
| Remove the clear step from the start of the frame | | |
| Change the target frame time from 16 ms to 200 ms | | |
| Use `system_clock` instead of `steady_clock` | | |

The first one is the dangerous one, and worth doing **once**, carefully: it may appear to work, it
may print garbage, it may crash, and it may do something different each run. That unpredictability
*is* the lesson.

---

## Think like an engineer

1. **Your buffer holds one `char` per square.** What if you wanted colour as well? Design the data.
   How much memory would your dungeon take then?
2. You clear and redraw **every** square, every frame, even though the walls never change. For a
   32×7 dungeon that is nothing. For a 200×60 one it is 12,000 characters a frame. **Design a way to
   redraw only what changed.** What does it cost you? *(This has a name, and you will meet it.)*
3. **The honest question about `sleep_for`.** You sleep for the leftover time. What happens if your
   frame's work takes *longer* than the budget? Does the game slow down, skip, or something else?
   What would you want it to do?
4. Compare this with the Python track's `tracer(0)`/`update()` and the web track's "erase then draw".
   You have now built double buffering by hand, having been handed it twice. **What did building it
   teach you that being handed it did not?**

---

## Vocabulary

| Word | What it means |
|---|---|
| **Screen buffer** | A grid of characters in memory, holding the frame being built. |
| **Double buffering** | Draw the whole frame invisibly, then show it in one go. |
| **Flat array** | A 1-D array used as a grid, via `y * WIDTH + x`. |
| **Row-major order** | Storing a grid one row after another. |
| **Bounds check** | Making sure an index is inside the array before using it. |
| **ANSI escape** | A string the terminal reads as a command, not as text. |
| **`steady_clock`** | A clock that only moves forward, for measuring durations. |

---

## Recap

- Build the frame in a **buffer**, then print it all at once. That is **double buffering**.
- A grid is really one long line: **`index = y * WIDTH + x`**.
- **Always bounds-check.** C++ will not stop you writing outside an array; it will quietly corrupt
  memory and fail somewhere else, later.
- `\033[H` moves the cursor home without clearing, which flickers less.
- Use `steady_clock` for durations, and sleep for the **leftover** time in the frame.
- `sin(time * speed) * size` is the standard recipe for gentle repeating motion.

---

## Stretch goals

1. **Colour**, with ANSI codes: `"\033[31m"` is red, `"\033[0m"` resets. Beware — the colour codes
   are characters too, so they do not fit in a one-`char`-per-square buffer. How will you solve that?
2. **More things to animate** — a flickering torch, a dripping ceiling, a patrolling guard.
3. **Load the dungeon from a text file** instead of writing it in the code. Then edit the file and
   rerun without recompiling, which is the entire point of data-driven design.
4. **Draw the frame rate** and watch it change as you add things.
5. **A larger dungeon that scrolls**, showing only the part near the player. That is a *camera*, and
   it is an intermediate-level topic you can reach today.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run the flicker version — printing directly, with no buffer — on the projector. Then run the buffered one. No explanation needed between them. |
| 10–30 | **Concept.** The buffer, then `y * WIDTH + x` with the tilemap visualizer. Spend the time here; everything else today follows from it. |
| 30–45 | **Live-code** `clear()`, `put()` and `present()`. Write `put()` **without** the bounds check, then add it and explain why. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. Do the out-of-bounds one together, on the projector. |
| 140–150 | Recap. Next lesson they can move. |

**What usually goes wrong**

1. **Terrible flicker.** They are clearing with `\033[2J` every frame instead of just homing the
   cursor with `\033[H`, or printing character by character rather than building a string.
2. **The picture is sideways or a diagonal mess.** `x * WIDTH + y` instead of `y * WIDTH + x`. The
   tilemap visualizer fixes this in seconds.
3. **Writing out of bounds.** The symptom is anything at all — garbage characters, a crash, or
   apparently working fine. Worth showing them that "it seemed to work" is the *worst* outcome,
   because the bug is still there.
4. **The animation is a blur.** No `sleep_for`, so the loop runs thousands of times a second.
5. **Off-by-one on the last row or column**, from `<=` instead of `<` in a loop. Classic, and `-Wall`
   will not catch it.
6. **Windows terminals and ANSI codes.** Modern Windows Terminal handles them; the old `cmd.exe` may
   not. If a student sees literal `[2J` text, that is why — they should use Windows Terminal or WSL.

**If you are running short on time** — give them `clear()`, `put()` and `present()` as a paste-in and
spend the build on the dungeon and the animation. The buffer concept is the lesson; typing the
boilerplate is not.

**For the student who finishes at minute 90** — stretch goal 1 (colour) is excellent, and
*deliberately* has a trap in it: ANSI colour codes are several characters long, so they do not fit in
a `char` buffer. Working out a solution — a parallel colour array, or building the output string
differently — is a genuine design problem with several valid answers, and it will absorb a strong
student completely.

**The thing to land:** they have now met double buffering three times — turtle's `tracer(0)`, the web
canvas's erase-then-draw, and today building it themselves out of a plain array. Ask what the
difference was between being handed it and building it. The point of the C++ track is that here, the
machinery is visible.
