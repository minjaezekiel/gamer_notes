# Lesson 3 — Drawing With Letters

## Cheat sheet

### The three steps, every frame

1. **Clear** the buffer
2. **Draw** into the buffer
3. **Show** it, all at once

Nothing reaches the screen until the frame is finished. That is **double buffering**.

### A grid is one long line

```cpp
char screen[WIDTH * HEIGHT];

int index = y * WIDTH + x;   // skip y rows, then x across
int x = index % WIDTH;       // the remainder
int y = index / WIDTH;       // the whole part
```

### Always bounds-check

```cpp
void put(int x, int y, char c) {
    if (x < 0 || x >= WIDTH ||
        y < 0 || y >= HEIGHT) return;
    screen[y * WIDTH + x] = c;
}
```

**Python raises IndexError. C++ does not.** It writes into memory it does not own and fails
somewhere else, later.

### Showing it

```cpp
std::string out = "\033[H";   // cursor home, no clear
for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++)
        out += screen[y * WIDTH + x];
    out += '\n';
}
std::cout << out << std::flush;
```

`\033[2J` clears (more flicker) · `\033[H` homes (less)

### Frame timing

```cpp
using Clock = std::chrono::steady_clock;
auto start = Clock::now();
// ...do the frame...
auto elapsed = Clock::now() - start;
if (elapsed < target)
    std::this_thread::sleep_for(target - elapsed);
```

`steady_clock`, **not** `system_clock` — the system clock can jump.

### Delta time

```cpp
std::chrono::duration<double> d = now - last;
double dt = d.count();
if (dt > 0.1) dt = 1.0 / 60.0;   // clamp
```

### Gentle repeating motion

```cpp
sin(time * SPEED) * SIZE
```

Input multiplier = how fast. Output multiplier = how far.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What are the three steps of a frame when you use a screen buffer? What is the technique called?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Write the formula that converts <code>(x, y)</code> into an index, and both formulas for the reverse.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> What happens in C++ if you write past the end of an array? How is that different from Python, and why is it worse?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why <code>steady_clock</code> rather than <code>system_clock</code>?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> In <code>sin(time * 3.0) * 5.0</code>, what does each number control?
<div class="lines"><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> <code>WIDTH</code> is 32. What index is the square at <code>(5, 3)</code>? And which <code>(x, y)</code> is index 101? Show your working.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> <code>WIDTH = 32</code>, <code>HEIGHT = 7</code>. What does <code>put(4, 2, '#')</code> do with this formula, and what should it have done?

```cpp
screen[x * WIDTH + y] = c;
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> The frame's work takes 4 ms and the target is 16 ms. How long does the program sleep, and what is the resulting frame rate? Now the work takes 25 ms &mdash; what happens?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> The bat is drawn with <code>sin(frame * 0.9)</code> instead of <code>sin(total_time * 0.9)</code>. Describe what happens when <code>TARGET_FPS</code> changes from 30 to 60. What is this bug called?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The last column of the dungeon is never drawn. What is wrong?

```cpp
for (int x = 0; x < WIDTH - 1; x++) {
    put(x, y, DUNGEON[y][x]);
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> This appears to work on one student's machine, prints garbage on another's, and crashes on a third. Why do all three things happen, and what should be added?

```cpp
void put(int x, int y, char c) {
    screen[y * WIDTH + x] = c;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The animation is a blur and the frame rate reads in the hundreds of thousands. What is missing?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Make a <code>char screen[WIDTH * HEIGHT]</code> buffer, a <code>clear()</code> that fills it, and a <code>present()</code> that prints it as rows. Show a screen full of dots.</li>
<li><strong>Checkpoint 2.</strong> Write <code>put(x, y, c)</code> <strong>with the bounds check</strong>. Test it by deliberately calling <code>put(-5, 0, 'X')</code> and <code>put(999, 0, 'X')</code> and checking nothing breaks.</li>
<li><strong>Checkpoint 3.</strong> Draw a dungeon from an array of strings. Edit the strings, recompile, and confirm the drawing code did not change.</li>
<li><strong>Checkpoint 4.</strong> Add the frame timer with <code>steady_clock</code> and <code>sleep_for</code>. Draw the measured frame rate on screen.</li>
<li><strong>Checkpoint 5.</strong> Animate something with <code>sin(total_time * speed)</code> &mdash; rippling water, a flickering torch, or a creature moving back and forth.</li>
<li><strong>Checkpoint 6.</strong> Change <code>TARGET_FPS</code> from 30 to 10 and back. Your animation should run at the <strong>same real-world speed</strong> either way. If it does not, you are driving it from the frame count.</li>
</ul>

<div class="note">
<span class="note-label">Checkpoint 6 is the test that matters</span>
<p>Anything driven by <code>frame</code> instead of <code>total_time</code> will speed up and slow
down with the frame rate. It is the same bug the web and Python tracks met as <em>delta time</em>,
wearing different clothes.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Your buffer holds one `char` per square. What if you wanted **colour** as well? Design the
data. How much memory would a 200×60 dungeon take then?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** You clear and redraw **every** square every frame, even though the walls never change. For
32×7 that is nothing; for 200×60 it is 12,000 characters a frame. **Design a way to redraw only what
changed.** What does it cost you?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** You sleep for the leftover time. What happens if the frame's work takes **longer** than the
budget? Does the game slow down, skip ahead, or something else? What would you *want* it to do, and
is that always the same answer?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** You have now met double buffering three times: turtle's `tracer(0)`, the web canvas's
erase-then-draw, and today building it yourself out of a plain array. **What did building it teach
you that being handed it did not?**

<div class="lines"><i></i><i></i><i></i></div>

---

## Stretch goals

1. **Colour** with ANSI codes (`"\033[31m"` red, `"\033[0m"` reset). Careful — the codes are several
   characters, so they do not fit in a one-`char`-per-square buffer. How will you solve that?
2. More things to animate: a dripping ceiling, a patrolling guard, a pulsing portal.
3. **Load the dungeon from a text file** so you can edit levels without recompiling.
4. A bigger dungeon that scrolls, showing only the part near the player. That is a **camera**.
