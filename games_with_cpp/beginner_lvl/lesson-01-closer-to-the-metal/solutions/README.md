# Lesson 1 — Solutions and marking notes

---

## Section A

**A1.** [3] A compiler translates your `.cpp` source into machine instructions the processor runs
directly, as a separate step before the program runs. One mark.

Two marks for any two of: **speed** (nothing is interpreting while the game runs); **errors caught
early** (many bugs become compile errors instead of crashes later); **a standalone executable** that
runs on a machine with no language installed.

**A2.** [2] `clang++ -std=c++17 -Wall game.cpp -o game` (accept `g++`).

**A3.** [2] Turns on all the ordinary warnings — legal code the compiler thinks is probably a
mistake, such as an unused variable or a function that forgets to return. They are free bug reports,
and fixing them before running saves time.

**A4.** [3] `1000 ms ÷ 60 = **16.7 ms**`. Two marks (one for the method). One for what has to happen
in it: read input, update every object, check every collision, and draw the entire screen — all of
it, not per object.

**A5.** [2] Because the compiler must know how much memory each variable needs and which operations
are valid, in advance, so it can produce machine instructions. Python works it out while running,
which costs time on every operation.

---

## Section B

**B1.** [4] One mark each:
`7 / 2` → **3** (whole-number division truncates — it does not round)
`7.0 / 2` → **3.5**
`7 % 2` → **1**
`1000 / 60` → **16**

**B2.** [3] It prints **0**. Both `score` and `100` are whole numbers, so C++ does whole-number
division: `87 / 100` is 0 with remainder 87, and the fraction is discarded. Assigning that to a
`double` afterwards is too late — the damage is already done.

Fix: `score / 100.0`.

**B3.** [3] It prints:
```
1
0
```
`bool` prints as **1** for true and **0** for false, unless you use `std::boolalpha`. Two marks for
the values, one for knowing why.

**B4.** [4] `guess` is **0** — the value it was given when declared — and the program prints
`You picked 0`. The read **fails**, leaving `guess` untouched, and `std::cin` goes into an error
state so every later read also fails silently.

Two marks for the value, two for explaining that the read failed rather than storing something odd.

This is a good moment to point out the value of initialising variables: had `guess` been declared
without `= 0`, it would have printed whatever junk was in that memory.

---

## Section C

**C1.** [3] Two mistakes:

1. Missing `;` after `std::cout << "Hello"`.
2. Missing `#include <iostream>`, so `std::cout` is not declared.

Two marks for both, one for noticing that the semicolon error is reported on the line with `return`
— the compiler reads on until it finds something that cannot possibly follow, which is one line
later.

**C2.** [3] **They did not recompile.** They are running the previous executable. The habit is:
change → compile → run, every single time.

Worth saying out loud that this happens to professionals too, which is why build systems exist.

**C3.** [4] `int total;` is **uninitialised**. In C++ an uninitialised local variable contains
whatever happened to be in that piece of memory — not zero. The loop then adds 55 to that junk, so
the answer is "55 plus something unpredictable", and it changes between runs.

Fix: `int total = 0;`.

Two marks for identifying the uninitialised variable, one for "it is not zero", one for the fix.

This is one of the most important differences between C++ and Python, and it is worth labouring.
Compile it with `-Wall` and the compiler will usually warn — another argument for the flag.

---

## Section D — marking the build

**Checkpoint 1 is the lesson.** A student who leaves lesson 1 unable to compile has learned nothing,
no matter what else they did. A student who leaves with *only* checkpoint 1 working has learned the
most important thing in it.

Checkpoint 4 is a full pass.

**Checkpoint 3.** Running it five times and getting different numbers is the test. A student who
seeded with a constant will get the same sequence every run — a good discussion about what "random"
means to a computer.

**Checkpoint 6.** The percentages should all be close to 16.67. Students are often surprised that
they are not *exactly* equal; that is a nice opening about sample size — with 100 rolls the spread is
large, with 100,000 it is small, and with infinite rolls it would be exact.

---

## Section E — marking notes, not answers

**E1.** Collect the class's messages on the board. The ones worth discussing:

| Mistake | Message | Why it is confusing |
|---|---|---|
| missing `;` | `expected ';' before ...` on the **next** line | the compiler reads on until something cannot follow |
| missing `#include` | `'cout' was not declared in this scope` | it is a *name* problem, not a typing problem |
| `void main()` | varies, often accepted with a warning | the standard says `int`, and compilers are lenient |
| missing `}` | an error at the very **end** of the file | it read the whole file waiting for the brace |
| wrong type | a wall of template output | the worst messages in C++, and worth warning them about |

The point: **the first error is the one to fix.** Later errors are often knock-on effects, and
recompiling after fixing one often clears ten.

**E2.** Compiling buys speed, early error-catching, and a **standalone executable** — you can hand a
player a file and it runs, with nothing installed. Not compiling buys a faster edit-and-try cycle:
change a line, run, see the result, with no wait.

The strongest answers notice this is about **when** you want to find out you were wrong. A compiler
tells you before running; Python tells you when that line is reached, possibly only in the hands of a
player.

**E3.** Tools are usually run once, by a developer, on a fast machine, and are not in the frame
budget. What matters for them is **how quickly you can write and change them**, not how fast they
execute. A level editor that takes 200 ms instead of 2 ms to save is fine; a game that takes 200 ms
per frame is not.

Strong answers notice that large studios genuinely do this split on purpose — the engine in C++, the
tools and often the gameplay scripting in something quicker to write. Mentioning that Unity uses C#
for gameplay over a C++ core, or that many engines embed Lua, is well above the expected level and
worth praising.

---

## Teacher note: the setup is the lesson

Budget real time for getting compilers working, and check before the first class:

- **macOS:** `xcode-select --install`
- **Linux:** `sudo apt install g++`
- **Windows:** MSYS2 or WSL. Visual Studio works but hides the compile command, which is the thing
  being taught — if you use it, show them the command line at least once.

Have a fallback for the student whose machine refuses: pair them with someone, or use an online
compiler for this lesson only. Do not let a toolchain problem cost them the whole first session.
