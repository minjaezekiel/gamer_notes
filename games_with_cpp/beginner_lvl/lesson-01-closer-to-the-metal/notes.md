# Lesson 1 — Closer To The Metal

> **Games with C++ · Beginner level · Lesson 1 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A working dice game you can play — and, more importantly, you will have **compiled and run your own
program** and will understand what that sentence actually means.

```
  ===========================================
   DICE DUEL
  ===========================================
   You rolled:  4 and 6  =  10
   Goblin rolled: 3 and 3 = 6
   You win the round!   Score 1 - 0
```

No graphics. That is lesson 3. Today is about the **tools**, and about a question nobody usually
answers: *what does "running a program" actually mean?*

## Where this fits

- **Back:** nothing. This is lesson 1.
- **Forward:** [lesson 2](../lesson-02-a-game-is-data/notes.md) is about types and memory.
- **Sideways:** students on the web and Python tracks built a game loop today. **So will you** — the
  idea is identical, and C++ makes the loop more visible, not less.

---

## The idea, in plain words

### What a compiler actually does

In Python or JavaScript, you write a file and the computer reads it and does what it says. Something
is standing between you and the machine, translating as it goes.

C++ does not work that way. Your `.cpp` file is **translated once, in advance**, into instructions
the processor understands directly — a separate file that the computer runs with nothing in between.
That translation is **compiling**, and the program doing it is a **compiler**.

```
  main.cpp  ──[ the compiler ]──►  main  ──► the processor runs it directly
  (text you wrote)                 (machine instructions)
```

Three real consequences, and they explain most of what C++ feels like:

| Because it compiles first… | …you get |
|---|---|
| The translation already happened | **Speed.** Nothing is interpreting while your game runs. |
| The compiler reads everything before running | **Errors found early** — many bugs become compile errors rather than crashes at 2am |
| The compiler must know the type of everything | **You have to say what things are.** `int score = 0;` not `score = 0` |

That last one is the trade you are making. C++ asks you for more information up front, and gives you
speed and earlier error-catching in return.

### Why games are written in C++

Because of the frame budget.

A game at 60 frames per second has **16.7 milliseconds** to do everything: read input, move every
object, check every collision, and draw the whole screen. Not 16.7 milliseconds per object — for all
of it, every frame.

When you are simulating ten thousand objects, "fast enough" stops being a nice-to-have. That is why
almost every large commercial game, and every major engine — Unreal, Unity's core, Godot's core — is
written in C++.

> **This does not make C++ "better".** The Python track's Snake is a perfectly good game and took
> fewer lines. C++ is the right tool when you need control over speed and memory, and the wrong tool
> when you need to try an idea quickly. A good programmer picks; they do not have a favourite.

### Your first program, line by line

```cpp
#include <iostream>     // bring in the code for printing and reading

int main() {            // every C++ program starts here. ALWAYS.
    std::cout << "Hello!" << std::endl;
    return 0;           // 0 means "finished with no problem"
}
```

- **`#include <iostream>`** — "paste in the standard input/output code". The `#` means it happens
  *before* compiling, which is why it is called a **preprocessor** directive.
- **`int main()`** — the starting point. When you run the program, this function is what runs. The
  `int` says it hands back a whole number when it finishes.
- **`std::cout`** — "character output", the standard output stream. `std::` means it lives in the
  **standard library's namespace**, which is a way of keeping names from clashing.
- **`<<`** — sends the thing on the right into the stream on the left. You can chain them.
- **`std::endl`** — a new line. (`"\n"` also works and is slightly faster; `endl` additionally
  flushes the output, which matters in a game loop.)
- **`;`** — ends a statement. Every statement. Forgetting one is the most common beginner error, and
  the message often points at the **next** line, because that is where the compiler noticed.
- **`return 0;`** — tells whoever ran the program that it finished successfully.

### The loop you will build

Even today, with no graphics, the shape is the same as every other track:

```cpp
bool playing = true;

while (playing) {
    show_score();            // RENDER
    std::cout << "> ";
    std::string command;
    std::cin >> command;     // INPUT  (this one WAITS - lesson 4 fixes that)
    handle(command);         // UPDATE
}
```

C++ gives you a real `while` loop here, which is in some ways *clearer* than JavaScript's
`requestAnimationFrame`. The loop is right there on the page.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:** press **Step 1 frame** three times. Input, update, render. Your dice game today
has exactly these three jobs, in exactly this order, with one difference: it **waits** at the input
step. Lesson 4 is where that changes.

The explainer is a web page and you are writing C++. That is on purpose. **The loop is an idea, not
a feature of a language.**

---

## The idea, in code

### Compiling and running

Open a terminal, go to the folder with your file, and type:

```bash
clang++ -std=c++17 -Wall 01-hello.cpp -o 01-hello
./01-hello
```

Taking that apart:

| Part | Means |
|---|---|
| `clang++` | the compiler. (`g++` works identically — use whichever you have.) |
| `-std=c++17` | use the 2017 version of the language |
| `-Wall` | **"warn me about everything."** Turn this on and leave it on. |
| `01-hello.cpp` | the file to compile |
| `-o 01-hello` | what to call the result. Without it you get a file called `a.out`. |
| `./01-hello` | run it. The `./` means "in this folder". |

**Two steps, every time.** Compile, then run. If you change the file and run it without compiling
again, you run the *old* program — and spend twenty minutes wondering why your change did nothing.
Everybody does this at least once.

> **Always use `-Wall`.** It tells the compiler to warn about things that are legal but almost
> certainly mistakes — an unused variable, a comparison that is always true, a value you forgot to
> return. Those warnings are free bug reports. Code that compiles with no warnings is a reasonable
> standard to hold yourself to, starting today.

### Reading a number from the player

```cpp
#include <iostream>

int main() {
    int guess = 0;                   // declare the TYPE, then the name
    std::cout << "Pick a number: ";
    std::cin >> guess;               // read one number into the variable

    if (std::cin.fail()) {           // they typed something that is not a number
        std::cout << "That was not a number.\n";
        return 1;                    // non-zero means "something went wrong"
    }

    std::cout << "You picked " << guess << "\n";
    return 0;
}
```

`std::cin >> guess` reads a number. If the player types `banana`, the read **fails** and `guess` is
left at 0 — which is why checking `std::cin.fail()` matters, and why you should give variables a
starting value.

### Random numbers that are actually random

```cpp
#include <random>

// One generator for the whole program, seeded once from the system clock.
std::random_device seed;
std::mt19937 generator(seed());
std::uniform_int_distribution<int> dice(1, 6);

int roll = dice(generator);     // a number from 1 to 6, each equally likely
```

That is more typing than Python's `random.randint(1, 6)`, and the extra pieces each do a job:

- `std::random_device` gets a genuinely unpredictable starting number from the operating system.
- `std::mt19937` is the generator — a well-studied algorithm (the Mersenne Twister).
- `uniform_int_distribution<int>(1, 6)` maps its output onto 1–6 **fairly**.

You will see older code using `rand() % 6 + 1`. It works, and it is slightly biased — some numbers
come up a little more often than others, because 6 does not divide evenly into the generator's range.
For dice nobody notices. For loot drops in a game people play for a thousand hours, they do.

---

## The maths you just used

### Integer division throws away the remainder

```cpp
int a = 7 / 2;        // 3, NOT 3.5
double b = 7.0 / 2;   // 3.5
```

When **both** sides are whole numbers, C++ does whole-number division and discards the fraction. It
does not round — it truncates. `7 / 2` is 3 and `-7 / 2` is −3.

This catches everybody. If you want a fraction, at least one side must be a decimal type:

```cpp
double average = total / (double)count;     // the (double) converts it
```

### `%` gives the remainder

```cpp
int leftover = 7 % 2;      // 1
```

You will use this constantly for wrapping things round: `index = (index + 1) % count` cycles through
0, 1, 2, … and back to 0.

---

## Break it on purpose

Use `code/03-dice-duel.cpp`. **Compile each time** and read the error messages carefully — today the
errors *are* the lesson.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Delete a semicolon from the middle of the program | | |
| Change `int main()` to `void main()` | | |
| Remove `#include <iostream>` | | |
| Remove `-Wall` from the compile command, then add an unused variable | | |
| Change `int score` to `score` with no type | | |
| Compile without `-o`, then look for the output file | | |
| Change the file, run `./03-dice-duel` **without** recompiling | | |

The last one is the most important habit in this lesson. The first one is worth doing carefully:
notice that the error often points at the line **after** the mistake, because that is where the
compiler first noticed something was wrong.

---

## Think like an engineer

1. **The error message game.** Introduce one mistake at a time and collect the messages. Which were
   helpful? Which pointed at the wrong line? Build yourself a translation table — "`expected ';'
   before` really means…" — and keep it.
2. Python needs no compile step. C++ does. **What does each one buy you?** Think about writing a game,
   and then about *shipping* one to a player who does not have Python installed.
3. A frame at 60 fps is 16.7 ms. Estimate how many simple additions a modern processor does in that
   time. (It is more than you think.) What does that tell you about when speed actually matters?
4. **The honest question.** If C++ is so fast, why is almost every *tool* — level editors, build
   scripts, asset pipelines — usually written in Python or C#? What is different about those jobs?

---

## Vocabulary

| Word | What it means |
|---|---|
| **Compiler** | The program that translates your `.cpp` into machine instructions. |
| **Compile** | To do that translation. A separate step before running. |
| **Executable** | The result: a file the processor can run directly. |
| **`#include`** | "Paste in this other file" — handled before compiling. |
| **`main()`** | Where every C++ program starts. |
| **Namespace** (`std::`) | A way of grouping names so they do not clash. |
| **Type** | What kind of thing a variable holds: `int`, `double`, `bool`, `std::string`. |
| **Warning** | Legal code the compiler thinks is probably a mistake. |

---

## Recap

- C++ is **compiled**: translated once, in advance, then run directly by the processor.
- **Compile, then run. Two steps, every time.** Forgetting is universal.
- Always use **`-Wall`**. Warnings are free bug reports.
- Every program starts at `int main()`. Every statement ends with `;`.
- You must say what **type** each variable is. That is the price of the speed.
- `7 / 2` is **3**. Whole-number division truncates.
- The game loop is the same idea as in every other track — and here you can see the `while`.

---

## Stretch goals

1. **Best of five.** Play rounds until someone wins three.
2. **Different dice.** Let the player choose how many sides. What happens if they pick 1? Or 0? Or a
   negative number? Handle it.
3. **A statistics mode.** Roll 100,000 dice and count how often each number comes up. Are they even?
   Now try it with `rand() % 6 + 1` and compare. Can you see the bias?
4. **Time it.** Use `<chrono>` to measure how long a million rolls takes. Then try the same in
   Python. The ratio is the answer to "why C++?".
5. **Make the goblin cheat**, but only sometimes, and only when it is losing. Is the game more fun?
   Should the player be able to tell?

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Show the `.cpp` file and then the compiled binary in a hex viewer or `xxd | head`. "This is the same program. One of these you can read." |
| 10–25 | **Concept.** What compiling is, and why games use C++. Draw the source → compiler → executable diagram. |
| 25–45 | **Everybody compiles.** Do not move on until every single student has compiled and run hello world. This is the real content of lesson 1. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D: the dice game. |
| 125–140 | **The error message game** — deliberately break things and collect the messages. |
| 140–150 | Recap. |

**The setup is the lesson. Budget for it.**

Check before the first class:

```bash
clang++ --version        # or g++ --version
```

- **macOS:** `xcode-select --install` installs the command line tools.
- **Linux:** `sudo apt install g++`
- **Windows:** MSYS2 or WSL are the least painful. Visual Studio works but is a large install and
  hides the compile command, which is the thing being taught.

If a student cannot compile, they cannot do anything else today. Have a plan: pair them up, or use an
online compiler as a fallback for the first lesson only.

**What usually goes wrong**

1. **Running the old program.** They changed the file and forgot to recompile. Teach the two-step
   habit explicitly and repeat it all lesson.
2. **`command not found: ./03-dice-duel`.** They are in the wrong folder, or compiled without `-o`
   and have an `a.out`.
3. **Missing semicolon**, with an error pointing at the *next* line. Explain *why* the message is
   misleading — it is not the compiler being unhelpful, it is the compiler reporting the first point
   at which it knew something was wrong.
4. **`'cout' was not declared in this scope.`** Missing `#include <iostream>`, or missing `std::`.
5. **`7 / 2` giving 3.** Whole-number division. Comes up in the stretch goals.
6. Someone will ask about `using namespace std;`. It exists, it saves typing, and it is why many
   tutorials look different from these notes. Worth one minute: it dumps every standard-library name
   into your program, which causes real name clashes in larger projects. We write `std::` in this
   course, and once they know the trade-off they can choose.

**If you are running short on time** — cut the dice game to a single round and spend the time on
compiling. A student who leaves lesson 1 unable to compile has learned nothing; a student who leaves
with only a one-round dice game has learned everything that matters today.

**For the student who finishes at minute 90** — stretch goal 3 (the bias in `rand() % 6`) is
genuinely interesting and produces real data. Stretch goal 4 (timing it against Python) is the one
that makes the case for C++ concretely instead of by assertion, and students enjoy the result.

**The thing to land:** C++ is not the "serious" language and Python the "toy" one. They are tools
with different trade-offs. Today they paid a price — declaring types, compiling before running — and
in lesson 3 they will see what it buys.
