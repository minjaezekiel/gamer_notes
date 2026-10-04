# Lesson 1 — Closer To The Metal

## Cheat sheet

### Compile, then run. Two steps.

```bash
clang++ -std=c++17 -Wall file.cpp -o file
./file
```

| Part | Means |
|---|---|
| `clang++` | the compiler (`g++` works the same) |
| `-std=c++17` | the 2017 language version |
| `-Wall` | **warn me about everything** |
| `-o file` | what to name the result |
| `./file` | run it, from this folder |

**Change the file → compile again.** Running without recompiling runs the OLD program.

### The smallest program

```cpp
#include <iostream>

int main() {
    std::cout << "Hello\n";
    return 0;
}
```

- `#include` — paste in another file, before compiling
- `int main()` — where every program starts
- `std::` — the standard library's namespace
- `;` — ends every statement
- `return 0;` — finished with no problem

### Types

```cpp
int    score    = 0;      // whole number
double accuracy = 0.0;    // decimal
bool   playing  = true;   // true / false
char   grade    = 'A';    // ONE character
std::string name = "";    // text
```

**Always give a starting value.** An uninitialised variable holds junk, not zero.

### Whole-number division

```cpp
7 / 2        // 3,  not 3.5  - it TRUNCATES
7.0 / 2      // 3.5
7 % 2        // 1   (the remainder)
```

One side must be a decimal, or the fraction is thrown away.

### Random, done properly

```cpp
std::random_device seed;
std::mt19937 generator(seed());
std::uniform_int_distribution<int> die(1, 6);

int roll = die(generator);
```

`rand() % 6 + 1` works and is slightly **biased**.

### The loop

```cpp
while (playing) {
    show();            // RENDER
    std::cin >> cmd;   // INPUT  (this WAITS)
    handle(cmd);       // UPDATE
}
```

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What does a compiler do? Name two things you get in return for having to compile.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> Write the full command to compile <code>game.cpp</code> into a program called <code>game</code>, with all warnings on.
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> What does <code>-Wall</code> do, and why should you always use it?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> A game runs at 60 frames per second. How many milliseconds does one frame get? Show your working, and say what has to happen in that time.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why must you declare the type of every variable in C++, when Python does not?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

**Write your answer down before compiling anything.**

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> What does each line print?

```cpp
std::cout << 7 / 2 << "\n";
std::cout << 7.0 / 2 << "\n";
std::cout << 7 % 2 << "\n";
std::cout << 1000 / 60 << "\n";
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The player's score is 87 out of 100. What does this print, and why is it almost certainly not what the author wanted?

```cpp
int score = 87;
double accuracy = score / 100;
std::cout << accuracy;
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> What is printed?

```cpp
bool playing = true;
std::cout << playing << "\n";
std::cout << (3 > 5) << "\n";
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> A student types <code>banana</code> when asked for a number. What is in <code>guess</code> afterwards, and what does the program print?

```cpp
int guess = 0;
std::cout << "Pick a number: ";
std::cin >> guess;
std::cout << "You picked " << guess << "\n";
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> This will not compile. There are <strong>two</strong> mistakes. Name both.

```cpp
int main() {
    std::cout << "Hello"
    return 0;
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> A student insists their change is not working. The code is correct. What have they almost certainly forgotten to do?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> This compiles and prints a different nonsense number every time it is run. Why?

```cpp
int main() {
    int total;
    for (int i = 1; i <= 10; i++) {
        total = total + i;
    }
    std::cout << total << "\n";
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Compile and run a hello-world program. <strong>Do not move on until this works.</strong></li>
<li><strong>Checkpoint 2.</strong> Ask the player their name and read it with <code>getline</code>. Ask for a number and read it with <code>&gt;&gt;</code>. Print both back.</li>
<li><strong>Checkpoint 3.</strong> Roll one die with <code>uniform_int_distribution</code> and print it. Run the program five times and check you get different numbers.</li>
<li><strong>Checkpoint 4.</strong> Build a <code>while</code> loop that keeps playing rounds until the player types <code>quit</code>. Keep a score in a variable outside the loop.</li>
<li><strong>Checkpoint 5.</strong> Make it a duel: you and an opponent each roll two dice, higher total wins the round, first to three wins the game.</li>
<li><strong>Checkpoint 6.</strong> Add a <code>stats</code> command that rolls 100,000 dice and prints how often each face came up as a percentage. Are they even?</li>
</ul>

<div class="note">
<span class="note-label">The two-step habit</span>
<p>Every single time you change the file: <strong>compile, then run.</strong> If your change seems to
have done nothing, you are almost certainly running the old program. This happens to everybody, this
week and forever.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1. The error message game.** Break your program in five different ways, one at a time, and write
down the message you get. Which were helpful? Which pointed at the wrong line, and why?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Python needs no compile step. C++ does. What does each one buy you? Think about *writing* a
game, and then about *shipping* one to a player who does not have Python installed.

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** If C++ is so fast, why are almost all game *tools* — level editors, build scripts, asset
pipelines — usually written in Python or C#? What is different about those jobs?

<div class="lines wide"><i></i><i></i><i></i></div>

---

## Stretch goals

1. Best of five instead of best of three.
2. Let the player choose the number of sides. What if they pick 1? Or 0? Or −4? Handle it.
3. Compare `uniform_int_distribution` with `rand() % 6 + 1` over a million rolls. Can you see the
   bias?
4. Time a million rolls with `<chrono>`, then do the same in Python. The ratio is the answer to "why
   C++?".
5. Make the goblin cheat, but only when losing. Is the game more fun? Should the player be able to
   tell?
