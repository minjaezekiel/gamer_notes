# Lesson 2 — A Game Is Data

> **Games with C++ · Beginner level · Lesson 2 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A turn-based battle with stats, items, and two fighters that are **the same kind of thing** — so
adding a third takes one line.

```
  ---------------------------------------------
   YOU            hp [##########------]  62/100
   CAVE TROLL     hp [####------------]  31/120
  ---------------------------------------------
   > attack
   You hit the cave troll for 14.
   The cave troll hits you for 9.
```

Today's idea is small to state and large in consequence: **gather related variables into one named
thing**.

## Where this fits

- **Back:** [lesson 1](../lesson-01-closer-to-the-metal/notes.md) got you compiling, and gave you
  types and a loop.
- **Forward:** [lesson 3](../lesson-03-drawing-with-letters/notes.md) puts pictures on the screen.
- **Today:** `struct`, memory, and the difference between a copy and the real thing — which is the
  single most important idea in C++.

---

## The idea, in plain words

### The problem with loose variables

Here is a battle with two fighters, written the obvious way:

```cpp
// DO NOT DO THIS
std::string player_name = "You";
int player_health = 100;
int player_attack = 12;
int player_defence = 5;

std::string troll_name = "Cave troll";
int troll_health = 120;
int troll_attack = 10;
int troll_defence = 3;
```

Eight variables for two fighters. A third fighter needs four more, and every function that handles a
fight needs to know *which set* it is working with:

```cpp
void attack(std::string attacker_name, int attacker_attack,
            int& defender_health, int defender_defence) { ... }
```

That signature is already unpleasant, and we have two fighters. With a party of four and some
monsters, it is unworkable.

### A struct is a named bundle

```cpp
struct Fighter {
    std::string name;
    int health;
    int max_health;
    int attack;
    int defence;
};
```

That creates a **new type**, called `Fighter`, which you use exactly like `int` or `std::string`:

```cpp
Fighter player;
player.name = "You";
player.health = 100;

Fighter troll;
troll.name = "Cave troll";
troll.health = 120;
```

And now a function takes **one** argument per fighter:

```cpp
void attack(Fighter& attacker, Fighter& defender) { ... }
```

Four benefits, and they compound:

1. Related data stays together, so it cannot drift apart.
2. Functions take one thing instead of five.
3. A third fighter is `Fighter goblin;` — one line.
4. The code says `Fighter`, which tells a reader what it is.

> This is the same idea as Python's dictionaries in lesson 1 of that track, and as the `ball` object
> in the web track. Every language has a way to say "these things belong together", because every
> program needs one.

### A better way to fill one in

```cpp
// All at once, in the order the struct declares them:
Fighter troll = {"Cave troll", 120, 120, 10, 3};

// Or, clearer, with designated initialisers (C++20) or just a function:
Fighter make_fighter(std::string name, int health, int attack, int defence) {
    Fighter f;
    f.name = name;
    f.health = health;
    f.max_health = health;     // start at full
    f.attack = attack;
    f.defence = defence;
    return f;
}
```

The function version is worth the extra lines. `max_health` is set from `health` automatically, so
the two can never disagree — and a reader of `make_fighter("Troll", 120, 10, 3)` can see what each
number means.

### The most important idea in C++: copies versus the real thing

This is where C++ differs most from Python, and where beginners lose the most time.

```cpp
void hurt(Fighter fighter) {        // NO ampersand
    fighter.health -= 10;
}

hurt(troll);
std::cout << troll.health;          // UNCHANGED. Still 120.
```

By default, passing a struct to a function gives it **a copy**. The function changes the copy, the
copy is thrown away when the function ends, and the original is untouched. **No error, no warning,
nothing happens.**

Add one character:

```cpp
void hurt(Fighter& fighter) {       // WITH an ampersand
    fighter.health -= 10;
}

hurt(troll);
std::cout << troll.health;          // 110. It worked.
```

The `&` makes it a **reference**: the function works on *the real one*, not a copy.

| Written | Means | Use it when |
|---|---|---|
| `Fighter f` | a **copy** | you only need to read it, and it is small |
| `Fighter& f` | **the real one** | you want to change it |
| `const Fighter& f` | the real one, **read-only** | you only need to read it, and it is big |

That third row is worth knowing now. Copying a big struct costs time, so for anything larger than a
couple of numbers, `const Fighter&` gives you the speed of a reference with the safety of a copy —
the compiler will refuse to let you change it.

> **How to remember it:** `&` means "**the actual one**". Without it, you get a photocopy. You can
> scribble on a photocopy all you like and the original is unaffected.

### What your data actually costs

C++ lets you ask how much memory something takes:

```cpp
std::cout << sizeof(int);          // usually 4 bytes
std::cout << sizeof(double);       // usually 8
std::cout << sizeof(char);         // always 1
std::cout << sizeof(bool);         // usually 1
std::cout << sizeof(Fighter);      // the whole bundle
```

In Python you never think about this. In C++ you can, and sometimes must.

Why it matters: a game with **100,000 particles**, each holding two `double`s for position, uses
1.6 megabytes. Switch to `float` (4 bytes instead of 8) and it is 800 kilobytes — which fits in the
processor's fast cache, and the game may run twice as fast for that reason alone.

You do not need to care about this today. You need to know that **the question exists**, because it
is one of the real reasons games are written in C++.

### An `int` can overflow

```cpp
int score = 2147483647;    // the biggest an int can hold
score = score + 1;
std::cout << score;        // -2147483648. It wrapped round to the bottom.
```

An `int` is 32 bits, so it holds about ±2.1 billion. Go past the top and it wraps to the bottom.

This is not theoretical. The famous "Nuclear Gandhi" bug in *Civilization* — where the most peaceful
leader in the game suddenly became aggressive — is usually told as an overflow story of exactly this
kind. (The designer has since said the real story is more complicated, but the *bug class* is
entirely real and has shipped in many games.)

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:** watch the UPDATE box. Today, "change the numbers" means changing fields inside
a `Fighter`. Everything the game remembers between turns — both fighters' health, the turn count — is
its **state**, and it now lives in two tidy bundles instead of eight loose variables.

---

## The maths you just used

### Clamping, again

```cpp
defender.health = defender.health - damage;
if (defender.health < 0) {
    defender.health = 0;        // never show negative health
}
```

Or in one line with the standard library:

```cpp
#include <algorithm>
defender.health = std::max(0, defender.health - damage);
```

`std::max(0, x)` means "whichever is bigger". `std::min` clamps the other way. You have now written
this in all three languages.

### Drawing a health bar from a fraction

```cpp
const int BAR_WIDTH = 16;
int filled = (fighter.health * BAR_WIDTH) / fighter.max_health;
```

Read it as: what fraction of full health are we at, scaled up to the bar's width.

**Multiply first, then divide.** Writing `(health / max_health) * BAR_WIDTH` gives you zero every
time, because `health / max_health` is whole-number division and is 0 for anything less than full
health. The order genuinely matters when the numbers are integers, and this is one of the most common
integer-division bugs there is.

---

## Break it on purpose

Use `code/03-battle.cpp`. Compile each time.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the `&` from `attack(Fighter& attacker, Fighter& defender)` | | |
| Change the health bar to `(health / max_health) * BAR_WIDTH` | | |
| Remove the `std::max(0, ...)` clamp and fight to the death | | |
| Set a fighter's `max_health` to 0 and attack | | |
| Add a field to `Fighter` and print `sizeof(Fighter)` before and after | | |
| Set `score = 2147483647` and add 1 | | |

The first one is today's headline: the fight runs, nobody ever takes damage, and **there is no error
message at all**.

---

## Think like an engineer

1. **Where does a fighter's behaviour live?** You have a `Fighter` struct and separate functions that
   act on it. What would it look like if the functions lived *inside* the struct? (They can. That is
   a class, and it is lesson 4 of the intermediate level.)
2. **Design the data for an item.** A sword, a potion, a key. What fields does an `Item` need so that
   a potion and a sword can both be in the same inventory? What goes wrong if you give it every field
   that any item might ever need?
3. **The memory question.** Your `Fighter` holds a `std::string`. Print `sizeof(Fighter)` and compare
   it with the length of the name. The number will not change no matter how long the name is. Work
   out why. *(What is actually stored inside the struct?)*
4. **The honest one.** Copies are safe and slow; references are fast and let a function change your
   data behind your back. Python makes this choice for you and never tells you. Which do you prefer,
   and what does C++'s way let you do that Python's does not?

---

## Vocabulary

| Word | What it means |
|---|---|
| **`struct`** | A bundle of related variables, under one name — a new type. |
| **Field / member** | One variable inside a struct. `fighter.health`. |
| **Pass by value** | The function gets a **copy**. Changes do not escape. |
| **Pass by reference** (`&`) | The function gets **the real one**. Changes stick. |
| **`const`** | "This must not change." The compiler enforces it. |
| **`sizeof`** | How many bytes something takes in memory. |
| **Overflow** | A number going past its maximum and wrapping round. |

---

## Recap

- A **`struct`** bundles related variables into one named type. Use one as soon as you have two
  variables that always travel together.
- **`&` means "the actual one"**. Without it a function gets a copy and your changes vanish silently.
- `const Type&` is the usual way to pass something big you only need to read.
- `sizeof` tells you what your data costs. You rarely need it, but knowing the question exists is
  part of knowing why games use C++.
- With integers, **multiply before you divide**.
- An `int` wraps round at about ±2.1 billion.

---

## Stretch goals

1. **A third fighter.** Add a goblin that joins in. How many lines did it take?
2. **An `Item` struct** and a small inventory. A potion that heals, a sword that raises attack.
3. **Critical hits** — a small chance of double damage, with a message so the player knows.
4. **A `std::vector<Fighter>`** holding every fighter, with a loop that takes everyone's turn. This
   is lesson 5 arriving early, and it is the right instinct.
5. **Measure it.** Write a function taking `Fighter` by value and one taking `const Fighter&`, call
   each a million times, and time them with `<chrono>`. Then make the struct much bigger and try
   again.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Put the eight-loose-variables version on the projector and ask them to add a third fighter. Let them feel it before you offer the fix. |
| 10–30 | **Concept.** `struct`, then copies versus references. The reference bit needs the full time — see below. |
| 30–45 | **Live-code** the `Fighter` struct and one `attack` function. Write it **without** the `&` first, run it, and let the class watch nobody take damage. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. |
| 140–150 | Recap. Next lesson: pictures. |

**Teaching references.** Do the photocopy demonstration physically. Write a number on paper, hand a
student a **photocopy**, ask them to change it, then show the class the original is unchanged. Then
hand over the **original** and do it again. Thirty seconds, and it sticks far better than any
diagram.

Then write the `&` on the board and say: **"this one character is the difference between a photocopy
and the original."**

**What usually goes wrong**

1. **The missing `&`.** The program compiles, runs, and does nothing. No error, no warning, no clue.
   This is today's defining bug and they must meet it.
2. **`(health / max_health) * WIDTH`** giving an empty bar always. Integer division. Comes up in every
   class.
3. **Forgetting the `;` after a struct's closing brace.** `};` not `}`. The error message is unusually
   bad — often pointing at the next function — so warn them in advance.
4. **Uninitialised fields.** `Fighter f;` leaves the numbers as junk. Encourage the `make_fighter`
   function so nothing can be forgotten.
5. **`error: no member named 'helth'`.** A typo, but a *good* one — unlike Python's dictionaries, the
   compiler catches it immediately. Point that out; it is one of the real benefits they are paying
   for.

**If you are running short on time** — give them the `Fighter` struct and `make_fighter` as a
paste-in and spend the build on the battle loop and the references. The `&` is the lesson; the struct
is the setup for it.

**For the student who finishes at minute 90** — stretch goal 5 (timing by-value against
by-reference) is the best one. With a small struct the difference is barely measurable, which is a
useful and slightly deflating result; then have them add a big array to the struct and measure again.
Learning that "it depends, so measure it" is worth more than any rule of thumb.

**The thing to land:** by the end they should be able to say what `&` does in one sentence. If the
class can do that, the lesson worked, whatever state their battle game is in.
