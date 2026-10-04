# Lesson 4 — Input And Movement

> **Games with C++ · Beginner level · Lesson 4 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A maze you walk around **in real time** — the game never stops to wait for you, there is no Enter key
to press, and a torch flickers and a timer counts down whether you move or not.

```
  ##############################
  #@...#........#..........#...#
  #.##.#.######.#.########.#.#.#
  #.#..............#.....*.#.#.#
  #.#.####.######.#.#####..#.#.#
  #...#..........#.......#.....#
  ##############################
   keys 1/3    time 42s    WASD or arrows, q to quit
```

This is the lesson where C++ becomes a real-time game, and it needs the one genuinely awkward piece
of code in the whole beginner track.

## Where this fits

- **Back:** [lesson 3](../lesson-03-drawing-with-letters/notes.md) gave you a screen buffer and a
  frame timer.
- **Forward:** [lesson 5](../lesson-05-many-things-at-once/notes.md) adds many moving things at once.
- **Today:** input that does not block, and collision in a grid.

---

## The idea, in plain words

### The problem with `std::cin`

Everything you have written so far reads input like this:

```cpp
std::string command;
std::cin >> command;        // the program STOPS here
```

The program stops and waits. Nothing happens — no animation, no timer, no enemy movement — until the
player types something **and presses Enter**.

For a real-time game that is useless. You need to ask **"has a key been pressed?"** and carry on
regardless of the answer.

### Two things have to change

The terminal is doing two unhelpful things by default, and both have names:

1. **Line buffering** (*canonical mode*). The terminal collects what you type and only hands it to
   your program when you press Enter — so you can use backspace to fix typos. A game wants each key
   the instant it is pressed.
2. **Echo.** The terminal prints what you type. In a game, pressing `w` should move the player, not
   put a `w` on screen.

So you ask the terminal to switch both off. That is called **raw mode**.

### The awkward part: it is different on every system

This is the one place in the beginner track where the code has to be different for different
operating systems, and it is worth being honest about why: **reading a key without waiting is not
part of standard C++.** The language says nothing about terminals. So you use whatever the operating
system provides.

```cpp
#ifdef _WIN32
  #include <conio.h>              // Windows gives you _kbhit() and _getch()
#else
  #include <termios.h>            // Unix: terminal settings
  #include <unistd.h>             // read()
  #include <fcntl.h>              // non-blocking mode
#endif
```

`#ifdef` is a **preprocessor** instruction, like `#include`. It means "only compile this part if that
name is defined". `_WIN32` is defined automatically by Windows compilers, so each machine compiles
only the half that works for it.

On Unix (macOS and Linux) it looks like this:

```cpp
static termios original_terminal;

void start_raw_mode() {
    tcgetattr(STDIN_FILENO, &original_terminal);     // remember the settings
    termios raw = original_terminal;
    raw.c_lflag &= ~(ICANON | ECHO);                 // switch off both
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);
    // and make read() return immediately instead of waiting
    fcntl(STDIN_FILENO, F_SETFL, fcntl(STDIN_FILENO, F_GETFL, 0) | O_NONBLOCK);
}

void stop_raw_mode() {
    tcsetattr(STDIN_FILENO, TCSANOW, &original_terminal);   // PUT IT BACK
}

int read_key() {
    char c;
    if (read(STDIN_FILENO, &c, 1) == 1) {
        return (unsigned char)c;
    }
    return 0;        // nothing was pressed. Carry on anyway.
}
```

> **The same idea as the Python track's lesson 5.** There, a tkinter game that quits while a frame is
> queued crashes with a `TclError`. Here, a C++ game that exits without restoring the terminal leaves
> the user's shell broken. Both are the same problem: **your program has to clean up after itself,
> including on the way out.**
>
> **`stop_raw_mode()` is not optional.** The terminal belongs to the whole system, not to your
> program. If you exit without putting the settings back, the user's terminal is left with no echo
> and no line editing — they type and see nothing. They will have to close the window or type `reset`
> blind. **Always restore what you changed.** This is the first time in the course that your program
> can leave a mess behind after it ends, and it is worth taking seriously.

`&=` and `~` are bit operations. `~(ICANON | ECHO)` means "everything except those two flags", and
`&=` keeps only what is in both. You do not need to understand bit manipulation today; you need to
know that this line means *switch those two settings off*.

### The pattern is the same as every other track

Once `read_key()` exists, the structure is one you already know:

```cpp
while (running) {
    int key = read_key();       // INPUT  - does NOT wait
    update(key, dt);            // UPDATE
    draw();                     // RENDER
    sleep_the_rest_of_the_frame();
}
```

Compare that with the web track's `requestAnimationFrame`, the Python track's `ontimer`, and tkinter's
`after`. **Four languages, same shape.** The only thing that was ever different was how you ask "has
anything happened?"

### Moving in a grid, and checking before you move

The maze is a grid of characters, exactly like lesson 3's buffer. Moving is adding to x or y — and
the important part is **checking the destination before you go there**:

```cpp
void try_move(int dx, int dy) {
    int new_x = player_x + dx;
    int new_y = player_y + dy;

    // Work out what is THERE before moving.
    char target = maze_at(new_x, new_y);

    if (target == '#') {
        return;                 // a wall. Do not move at all.
    }

    player_x = new_x;           // the move is allowed
    player_y = new_y;
}
```

> **Check first, then move.** The alternative — move, then check, then move back if it was wrong —
> works for one wall but falls apart as soon as two things could stop you, and it causes a visible
> jitter if anything draws in between. The habit of validating before acting is worth forming now.

Because the maze is a grid of whole squares, there is no overlap test and no rounding: a square either
contains a wall or it does not. The same thing that made Snake free of collision bugs.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:** the INPUT box lights up **every frame**, even when nothing has been pressed, and
it moves nothing by itself. That is exactly what `read_key()` returning 0 means — *"nothing happened,
carry on"*. Until today, your C++ games stopped at that box and waited.

Then open [the grids and flat arrays explainer](../../../shared/visualizers/tilemap-indexing.html).

**What to look for:** moving one square right changes the index by 1; one square down jumps a whole
row. Your maze lookup is exactly that, and so is the wall check.

---

## The maths you just used

### Arrow keys are three characters

This surprises everybody. Pressing the up arrow does not send one character — it sends **three**:
`27`, `91`, `65`. The 27 is the escape character, and the rest is an ANSI sequence, the same family
of codes you used to move the cursor in lesson 3.

So reading arrow keys means reading one key, and if it was 27, reading two more:

```cpp
int key = read_key();
if (key == 27) {               // escape: maybe an arrow key
    int second = read_key();
    int third = read_key();
    if (second == 91) {
        if (third == 65) { return KEY_UP; }
        if (third == 66) { return KEY_DOWN; }
        if (third == 67) { return KEY_RIGHT; }
        if (third == 68) { return KEY_LEFT; }
    }
}
```

This is also why pressing the Escape key alone can be awkward to detect — the program cannot
immediately tell "the user pressed Escape" from "an arrow key is arriving". Real terminal programs
wait a few milliseconds to find out. We offer `q` for quitting instead, which sidesteps it entirely.

**Choosing a design that avoids a hard problem is a legitimate engineering move**, and worth noticing
when you do it.

### Direction as a pair of numbers

```cpp
// Same idea as Snake in the Python track.
if (key == 'w') { try_move(0, -1); }     // up: y DECREASES
if (key == 's') { try_move(0, +1); }     // down
if (key == 'a') { try_move(-1, 0); }     // left
if (key == 'd') { try_move(+1, 0); }     // right
```

Row 0 is the top row, so "up" is **minus** — the same convention as lesson 3's buffer, tkinter, and
the web canvas.

---

## Break it on purpose

Use `code/03-maze-walker.cpp`. Compile each time.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the call to `stop_raw_mode()` at the end, then run and quit | | |
| Remove the wall check from `try_move` | | |
| Remove the `O_NONBLOCK` line from `start_raw_mode` | | |
| Swap `try_move(0, -1)` and `try_move(0, +1)` for w and s | | |
| Move the player first and check for walls afterwards | | |
| Remove the `sleep_for` | | |

**Do the first one deliberately, and know the cure in advance.** Your terminal will stop echoing what
you type. Type `reset` and press Enter — you will not see it as you type, and it will work. That is
exactly what happens to a player when a game does not clean up after itself.

---

## Think like an engineer

1. **Your `read_key()` reads one key per frame.** What happens if the player presses three keys very
   quickly within one frame? Is that a problem? How would you find out?
2. The maze is `const char*[]`, written in the code. **Design how you would load it from a file**, so
   levels could be made without recompiling. What could go wrong with a file that a player has
   edited?
3. **Your program changes a system-wide setting** — the terminal's mode — and must put it back. What
   else might a game change that it has to restore? What happens if the program crashes before the
   restore runs? *(There is a C++ answer to this, and it is lesson 10 of the intermediate level.)*
4. **The honest question.** Non-blocking input needed different code for Windows and Unix, because
   standard C++ says nothing about terminals. Why would the language leave something so obviously
   useful out? What would it cost to put it in?

---

## Vocabulary

| Word | What it means |
|---|---|
| **Blocking** | Code that stops and waits. `std::cin >>` blocks. |
| **Non-blocking** | Code that returns immediately, even with nothing to report. |
| **Raw mode** | Terminal settings with line-buffering and echo switched off. |
| **Canonical mode** | The normal mode, where input arrives a line at a time. |
| **Echo** | The terminal printing what you type. |
| **`#ifdef`** | Compile this part only on certain systems. |
| **Escape sequence** | Several characters meaning one thing, starting with 27. |

---

## Recap

- A real-time game **never waits** for input. `read_key()` returns 0 for "nothing happened".
- Switch the terminal to **raw mode** — and **always put it back**, or you leave the user's terminal
  broken.
- Non-blocking input is **not standard C++**, so it needs `#ifdef` for different systems.
- **Check the destination before moving.** Validate, then act.
- In a grid there is no overlap test: a square is a wall or it is not.
- Arrow keys arrive as **three** characters starting with 27.

---

## Stretch goals

1. **Push blocks.** A crate you can shove, but only into empty space. Now you have Sokoban.
2. **Load the maze from a file**, so levels need no recompiling.
3. **A patrolling guard** that moves on its own timer and catches you. Nothing about your input code
   changes — which is the point of a loop that does not wait.
4. **A visible field of view**, so you only see squares near the torch. (Hint: the distance from the
   player, as in the circle-collision lesson.)
5. **Hold-to-move.** At the moment one key press is one square. Make holding a key move you
   continuously, with a short delay before the repeat starts. You will need a timer and a "which key
   is currently held" variable — and you will discover why this is genuinely awkward in a terminal.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run lesson 2's battle. Ask: "how would a timer count down in this?" It cannot — the program is asleep inside `std::cin`. |
| 10–30 | **Concept.** Blocking versus non-blocking, raw mode, and why it needs `#ifdef`. Be honest that this is the ugliest code in the track and say why. |
| 30–45 | **Live-code** `read_key()` and the movement. Demonstrate forgetting `stop_raw_mode()` **yourself**, on the projector, and then fix it with `reset`. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. |
| 140–150 | Recap. Next lesson: many things moving at once. |

**The terminal-restore demonstration is worth doing deliberately.** Run a program without
`stop_raw_mode()`, quit it, and then type into the broken terminal so the class can see that nothing
appears. Then type `reset` blind and press Enter. It takes forty seconds, it is memorable, and it
makes "always restore what you changed" concrete rather than a slogan.

**What usually goes wrong**

1. **The terminal is left broken.** Expect this several times. Teach `reset` in the first ten minutes
   and write it on the board.
2. **Nothing responds to keys.** Missing `O_NONBLOCK`, so `read()` blocks and the game freezes; or
   they are running inside an IDE console that does not pass keys through. **Run from a real
   terminal.**
3. **The player walks through walls.** No check, or checking the square they are *on* rather than the
   one they are moving *to*.
4. **w and s are swapped.** Row 0 is the top, so up is −1. Same as lesson 3.
5. **Arrow keys print strange characters.** They are reading the escape sequence as three separate
   keys. The notes cover it; WASD works without any of this, which is why the examples offer both.
6. **Windows students.** `conio.h` works in MSYS2 and Visual Studio. In WSL they are on Linux and use
   the Unix branch. Check which one each student is actually on before the lesson.

**If you are running short on time** — give them the whole raw-mode block as a paste-in with the
comments intact, and spend the build on movement and collision. The input code is genuinely
system-specific plumbing; the *idea* that input should not block is the lesson, and that takes two
minutes to explain.

**For the student who finishes at minute 90** — stretch goal 1 (push blocks) turns the maze into
Sokoban and is a genuinely good design exercise: deciding what happens when a crate is pushed into
another crate, or into a wall, or onto the goal, is real game design and there is no single right
answer.

**The thing to land:** put all four loops side by side at the end —
`requestAnimationFrame`, turtle's `ontimer`, tkinter's `after`, and today's `while` with
`read_key()`. Four languages, three graphics systems, one shape. By now the class should find that
unsurprising, and that is exactly the outcome the three-track design is for.
