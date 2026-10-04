# Lesson 4 — Solutions and marking notes

`test_maze_reachable.py` in this folder checks that every key and the exit can actually be reached
from the start, and that every row of the maze is the same length. **Run it after editing the maze** —
an unreachable key is invisible by inspection and ruins the lesson.

---

## Section A

**A1.** [2] **Blocking** input stops the program until something arrives (`std::cin >>`).
**Non-blocking** returns immediately whether or not anything was pressed. A real-time game needs
non-blocking, because the world must keep moving while the player thinks.

**A2.** [3] One mark each for the two, one for the reasons:

- **`ICANON`** (canonical / line buffering) — the terminal collects a whole line and only hands it
  over when Enter is pressed. A game needs each key the instant it is pressed.
- **`ECHO`** — the terminal prints what you type. Pressing `w` should move the player, not put a `w`
  on screen.

**A3.** [3] The terminal belongs to the whole system, not to your program, and the settings persist
after it exits. One mark.

The user is left typing into a terminal that shows them nothing and does no line editing — their
backspace will not work and they cannot see what they are typing. One mark.

The cure is to type `reset` and press Enter, blind. One mark.

**A4.** [2] Because reading a key without waiting is **not part of standard C++** — the language says
nothing about terminals at all. Each operating system provides its own way, so the code has to pick
the right one at compile time.

**A5.** [2] **Three**: `27`, then `91`, then a letter code (`65` up, `66` down, `67` right,
`68` left).

---

## Section B

**B1.** [3] It checks `(5, 2)` — one **less** in y. Two marks.

It is minus because **row 0 is the top row** and y increases downwards, the same convention as the
lesson 3 buffer, tkinter and the web canvas. One mark.

**B2.** [4] Without `O_NONBLOCK`, `read()` **blocks**. The game freezes on the very first frame and
nothing is drawn or updated until a key is pressed. Then it does exactly one frame's work and freezes
again.

So the player sees: a frozen screen; press a key; one frame of movement; frozen again. The torch does
not flicker and the timer does not count. The game has become turn-based by accident.

Two marks for "it blocks", two for describing the one-frame-per-key behaviour.

**B3.** [3] It prints:
```
27
91
65
```
Three lines because the arrow key sends **three characters**, and this code reads one per call. Two
marks for the values, one for the explanation.

(This is exactly why the reference `read_key()` reads two more characters when it sees 27.)

**B4.** [4] Two marks for the behaviours:

- **Version A:** checks the destination first; if it is a wall, the player does not move at all. The
  position is never invalid, even for an instant.
- **Version B:** moves the player **into the wall**, then notices and moves them back. The end result
  is the same here.

Two marks for which is better. **A**, because:
- If anything draws, saves, or checks a collision between the move and the undo, it sees the player
  inside a wall.
- With two things that could stop you — a wall *and* a locked door, say — the undo gets complicated
  fast.
- "Move and undo" fails completely once movement is more than one square at a time.

The general principle is worth naming: **validate, then act.** Never put your data into a state you
would have to repair.

---

## Section C

**C1.** [3] `O_NONBLOCK` — the `fcntl` line in `start_raw_mode()`. Without it `read()` waits, so the
loop runs exactly once per key press. (Accept "the whole raw-mode setup is missing" as a partial.)

**C2.** [4] It checks the square the player is **already standing on**, not the one they are moving
**to**. Since the player is never standing in a wall, the check is always false and the move always
happens.

Two marks for the diagnosis, two for the fix:

```cpp
char target = maze_at(player_x + dx, player_y + dy);
if (target == '#') return;
player_x += dx;
player_y += dy;
```

This is a lovely bug because the code *looks* like it is doing a wall check. Point out that it would
pass a casual code review.

**C3.** [3] They forgot `stop_raw_mode()` before exiting — or the program left by a path that skips
it (an early `return`, or `exit()`, or a crash). Two marks.

The cure: type `reset` and press Enter. One mark. Worth adding that it works even though nothing
appears as you type.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 1 — the heartbeat matters.** Printing something every twentieth frame proves the loop is
running while nothing is pressed. Without it, a student cannot tell a working non-blocking loop from
a frozen one.

**Checkpoint 2 — make them test the restore.** Quit the game, then type something and check it
appears. Several students will discover they have an early `return` or a `break` that skips the
restore.

**Checkpoint 4.** Watch for C2's bug — checking the current square. It is common and looks correct.

**Circulating advice:** the single most useful question is "is your program running at all, or
waiting?" Students cannot usually tell, and the heartbeat from checkpoint 1 answers it instantly.

---

## Section E — marking notes, not answers

**E1.** With one `read_key()` per frame, the extra key presses **stay in the operating system's
buffer** and are read on the following frames. So they are not lost — they are delayed by a frame or
two, which at 30 fps is unnoticeable.

It becomes a problem if a lot of input arrives faster than frames (a key repeating fast, or pasted
text), because the queue grows and the game lags behind the player.

**How to find out** is the real question. Good answers: read in a loop until `read_key()` returns 0,
and count how many you got per frame; or press keys very fast and see whether the moves arrive late.
A student who says "I would measure it" rather than guessing has answered well.

The usual fix is to drain the queue each frame:

```cpp
int key;
while ((key = read_key()) != KEY_NONE) { handle(key); }
```

**E2.** Expected shape: open the file, read lines into a vector of strings, work out the width and
height from what you read.

What can go wrong, and good answers name several:

| Problem | What to do |
|---|---|
| The file is missing | fall back to a built-in maze, or report it clearly and exit |
| Rows are different lengths | pad them, or refuse to load — never read past the end of a row |
| A character you do not recognise | treat it as floor, or as a wall, but **decide** |
| No player start marker | report it; the game is unplayable without one |
| An enormous file | cap the size, or you will try to allocate gigabytes |
| The exit is walled off | you cannot easily detect this — which is why the test script here exists |

The ragged-rows case is the important one: reading `MAZE[y][x]` past the end of a short row is
exactly the out-of-bounds read lesson 3 warned about, and the file comes from outside your program,
so you cannot assume it is well-formed. **Anything a user can edit is untrusted input.**

**E3.** Other things a game might change and must restore: the cursor's visibility; the terminal
colours; the screen resolution or full-screen mode; the mouse being captured or hidden; the system
volume; keyboard repeat rate.

If the program **crashes** before the restore, none of it happens — which is exactly why the terminal
ends up broken when a student hits Ctrl-C.

The C++ answer is **RAII**: put the restore in a destructor, so it runs automatically when the object
goes out of scope, including when an exception unwinds the stack.

```cpp
struct RawMode {
    RawMode()  { start_raw_mode(); }
    ~RawMode() { stop_raw_mode(); }   // runs no matter how we leave
};
```

That is lesson 10 of the intermediate level. Do not teach it today, but if a student invents it,
tell them what it is called — it is one of the genuinely elegant ideas in C++.

(Honest caveat worth mentioning if asked: a hard crash or `kill -9` still skips destructors. Nothing
saves you from that, which is why terminals have `reset`.)

**E4.** Mark on reasoning. Things worth drawing out:

- C++ runs on machines with **no terminal at all** — microwaves, car engines, spacecraft. A language
  that required terminal support could not run there.
- The standard library only includes things that make sense **everywhere** C++ runs. Files and
  streams just about qualify; raw keyboard modes do not.
- The cost of including it: every C++ implementation on every device would have to provide it, even
  where it is meaningless.
- The cost of leaving it out: every program that wants it writes the same awkward `#ifdef`, or uses a
  library that did it for them — which is precisely what `raylib` does, and why the intermediate level
  starts using it.

A student who connects this to "and that is why libraries exist" has got the point exactly.

---

## Teacher note: break the terminal on purpose, first

In the first ten minutes, run a program without `stop_raw_mode()`, quit it, and then type into the
broken terminal so the class watches nothing appear. Then type `reset` blind and press Enter.

Forty seconds. It converts "always restore what you changed" from a slogan into something they have
seen, and it means the first student who does it accidentally knows the cure instead of panicking.
