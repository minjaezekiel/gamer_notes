# Lesson 2 — A Game Is Data

## Cheat sheet

### A struct bundles related variables

```cpp
struct Fighter {
    std::string name;
    int health;
    int max_health;
    int attack;
    int defence;
};          // <- the semicolon matters
```

```cpp
Fighter troll;
troll.name = "Cave troll";
troll.health = 120;
```

A third fighter is **one line**.

### `&` means THE ACTUAL ONE

```cpp
void hurt(Fighter f)  { f.health -= 10; }  // a PHOTOCOPY - changes vanish
void hurt(Fighter& f) { f.health -= 10; }  // THE REAL ONE - changes stick
```

Getting this wrong gives **no error and no warning**. The program runs and does nothing.

| Written | Means | Use when |
|---|---|---|
| `Fighter f` | a copy | read-only and small |
| `Fighter& f` | the real one | you want to change it |
| `const Fighter& f` | the real one, read-only | read-only and big |

### Clamping

```cpp
#include <algorithm>
health = std::max(0, health - damage);
health = std::min(max_health, health + heal);
```

### Integer division: multiply FIRST

```cpp
int filled = (health * WIDTH) / max_health;   // right
int filled = (health / max_health) * WIDTH;   // ALWAYS 0
```

With whole numbers, `health / max_health` is 0 for anything less than full.

### What data costs

```cpp
sizeof(char)    // 1
sizeof(int)     // usually 4
sizeof(double)  // usually 8
sizeof(Fighter) // the whole bundle
```

100,000 particles using `double` vs `float`: **3 MB vs 1.5 MB** — and the smaller one may run twice
as fast, because it fits in the cache.

### Overflow

An `int` holds about ±2.1 billion. Add one past the top and it wraps to the bottom.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What is a <code>struct</code>? Give two reasons to use one rather than loose variables.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Explain what <code>&</code> does in <code>void hurt(Fighter&amp; f)</code>. What happens if you leave it out?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> When would you use <code>const Fighter&amp;</code> rather than <code>Fighter</code>?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> A fighter has 45 health out of 200, and the bar is 16 wide. How many <code>#</code> should it show? Give the expression and the answer.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why might a game choose <code>float</code> over <code>double</code> for 100,000 particles? Give the reason that is <em>not</em> about running out of memory.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> What does this print, and why?

```cpp
void heal(Fighter f) { f.health += 50; }

Fighter troll;
troll.health = 100;
heal(troll);
std::cout << troll.health << "\n";
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> A fighter has 80 health out of 100 and the bar is 16 wide. What does each version print, and why is one of them always empty?

```cpp
int a = (80 * 16) / 100;
int b = (80 / 100) * 16;
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> What is printed?

```cpp
int score = 2147483647;
std::cout << score << "\n";
std::cout << score + 1 << "\n";
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> Does this compile? If not, what is the error, and is the compiler right to complain?

```cpp
void describe(const Fighter& f) {
    f.health = 999;
    std::cout << f.name;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The battle runs forever. Nobody ever takes any damage. The program compiles with <strong>no errors and no warnings</strong>. What is wrong?

```cpp
void do_attack(Fighter attacker, Fighter defender) {
    defender.health -= attacker.attack;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> This does not compile, and the error message points at whatever comes after it. What is missing?

```cpp
struct Fighter {
    std::string name;
    int health;
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> A fighter is created and immediately shows a health bar full of nonsense &mdash; sometimes enormous, sometimes negative, different every run. Why?

```cpp
Fighter goblin;
goblin.name = "Goblin";
draw_health_bar(goblin);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write a <code>Fighter</code> struct with name, health, max_health, attack and defence. Make one and print its fields.</li>
<li><strong>Checkpoint 2.</strong> Write <code>make_fighter(name, health, attack, defence)</code> that returns a filled-in <code>Fighter</code> with <code>max_health</code> set automatically.</li>
<li><strong>Checkpoint 3.</strong> Write <code>draw_health_bar(const Fighter&amp;)</code> using <code>#</code> and <code>-</code>. Check it is right at full health, half health and zero.</li>
<li><strong>Checkpoint 4.</strong> Write <code>do_attack(Fighter&amp; attacker, Fighter&amp; defender)</code>. <strong>Write it without the <code>&amp;</code> first</strong>, run it, and watch nobody take damage. Then add the ampersands.</li>
<li><strong>Checkpoint 5.</strong> Build the battle loop: attack, defend, potion and run, with the enemy taking its turn. End the fight when either side reaches 0.</li>
<li><strong>Checkpoint 6.</strong> Add a third fighter that joins the battle. Count how many lines it took.</li>
</ul>

<div class="note">
<span class="note-label">Checkpoint 4 is not a mistake in the instructions</span>
<p>You are being asked to write the bug on purpose. Seeing a program compile cleanly, run perfectly,
and do absolutely nothing is the most valuable thirty seconds in this lesson. You will meet this bug
for real later, and you will recognise it.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Design the data for an **item** — a sword, a potion, a key — so that all of them can live in
the same inventory. What fields does `Item` need? What goes wrong if you give it every field that any
item might ever need?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Your `Fighter` holds a `std::string`. Print `sizeof(Fighter)`, then make the name very much
longer and print it again. The number does not change. **Work out why.** What is actually stored
inside the struct?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Copies are safe and slow. References are fast, and let a function change your data behind your
back. Python makes this choice for you and never mentions it. Which do you prefer, and what does
C++'s way let you do that Python's does not?

<div class="lines wide"><i></i><i></i><i></i></div>

---

## Stretch goals

1. A third fighter. How many lines?
2. An `Item` struct and a small inventory.
3. Critical hits — a small chance of double damage, with a message so the player knows.
4. A `std::vector<Fighter>` and a loop taking everyone's turn. (That is lesson 5 arriving early.)
5. **Measure it.** Time a million calls by value against a million by `const&`. Then make the struct
   much bigger and try again.
