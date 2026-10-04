# Lesson 5 — Many Things At Once

## Cheat sheet

### `std::vector` — a list that grows

```cpp
#include <vector>

std::vector<Particle> particles;   // empty
particles.push_back(p);            // add to the end
particles.size();                  // how many (UNSIGNED)
particles[3];                      // index into it
particles.erase(particles.begin() + i);
```

An **array** has a fixed size decided at compile time. A **vector** does not.

### Removing: loop BACKWARDS

```cpp
for (int i = (int)v.size() - 1; i >= 0; i--) {
    if (dead) v.erase(v.begin() + i);
}
```

Two traps:
- **Forwards + erase skips items** (4th time you have met this)
- **No `(int)` cast** → `size()` is unsigned, `0 - 1` wraps to ~18 quintillion, infinite loop

### The proper idiom

```cpp
#include <algorithm>
v.erase(std::remove_if(v.begin(), v.end(),
    [](const Particle& p){ return p.life <= 0; }),
    v.end());
```

Recognise it. Use the backwards loop for now.

### Simulate in `double`, draw in `int`

```cpp
struct Ball { double x, y, speed_x, speed_y; };
put((int)ball.x, (int)ball.y, 'o');
```

`(int)` **truncates** — `3.9` → `3`. It does not round.

### Write the decimal point

```cpp
PADDLE_HEIGHT / 2.0   // right
PADDLE_HEIGHT / 2     // whole-number division - subtly wrong
```

Mixing `int` and `double` is a top source of quiet C++ bugs.

### Random directions

```cpp
double angle = random_double(0, 2 * 3.14159);
p.speed_x = cos(angle) * speed;
p.speed_y = sin(angle) * speed;
```

Angle first → an even circle. Random x and y separately → a lumpy square.

### Still true

**Fix the position, then flip the velocity.** (Fourth appearance.)

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What is the difference between an array and a <code>std::vector</code>? Give an example of when you must have a vector.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Why must you loop <em>backwards</em> when erasing from a vector? What happens if you do not?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why does <code>(int)v.size() - 1</code> need the cast? What goes wrong without it?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why does the ball's position need to be a <code>double</code> when the screen only has whole squares?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> What does <code>(int)3.9</code> give? Is that rounding?
<div class="lines"><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> A vector holds <code>[10, 20, 30, 40, 50, 60]</code>. This runs once. What is left, and why?

```cpp
for (std::size_t i = 0; i < v.size(); i++) {
    if (v[i] >= 30) v.erase(v.begin() + i);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The vector is <strong>empty</strong>. What happens?

```cpp
for (std::size_t i = v.size() - 1; i >= 0; i--) { ... }
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> <code>PADDLE_HEIGHT</code> is 4 (an <code>int</code>) and <code>paddle.y</code> is 6.0. What is <code>centre</code> in each version?

```cpp
double a = paddle.y + PADDLE_HEIGHT / 2.0;
double b = paddle.y + PADDLE_HEIGHT / 2;
```

Now try it with <code>PADDLE_HEIGHT = 5</code>.

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> Two balls are at <code>x = 0.1</code> and <code>x = 0.9</code>. Where is each drawn? What does the player see as a ball crosses from 0.0 to 2.0, and is that a bug?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The program compiles with a warning and then appears to hang, using 100% of a processor core. What is wrong, and what was the warning trying to tell you?

```cpp
for (int i = particles.size() - 1; i >= 0; i--) { ... }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> Roughly half the dead particles stay on screen forever. Name the bug &mdash; and say where you have met it before in this course.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> This crashes on some machines, works on others, and sometimes works until the game has been running a while. Why?

```cpp
for (Particle& p : particles) {
    p.life -= dt;
    if (p.life <= 0) particles.erase(...);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Make a <code>std::vector&lt;int&gt;</code>, push six numbers in, print them, then remove some &mdash; <strong>looping backwards</strong>. Prove it works by trying forwards first and seeing what survives.</li>
<li><strong>Checkpoint 2.</strong> Write a <code>Ball</code> struct with <code>double</code> position and speed. Move it with <code>* dt</code> and bounce it off the top and bottom. Draw it with <code>(int)</code>.</li>
<li><strong>Checkpoint 3.</strong> Add two paddles. Move yours with W/S; make the opponent follow the ball <strong>more slowly than the ball can travel</strong>, or it can never be beaten.</li>
<li><strong>Checkpoint 4.</strong> Make the ball bounce off the paddles, with the hit position steering it. Remember <code>/ 2.0</code>, not <code>/ 2</code>.</li>
<li><strong>Checkpoint 5.</strong> Add a <code>std::vector&lt;Particle&gt;</code>. Spray particles on every hit, move them, fade them, and erase the dead ones.</li>
<li><strong>Checkpoint 6.</strong> Add scoring, a win condition, and a particle burst when a point is scored.</li>
</ul>

<div class="note">
<span class="note-label">Do checkpoint 1 the wrong way first</span>
<p>Loop forwards while erasing, print the result, and see which items survived. Thirty seconds, and
you will never write that bug again without noticing.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** A vector keeps its items in one continuous block of memory. When it runs out of room it
allocates a bigger block and **copies everything across**. What does that mean for a game spawning
particles every frame? Look up `reserve()` — what does it do, and when would you call it?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** You have one vector of particles, and separate variables for the ball and the paddles. Why
not put **everything** in one vector of "entities"? What would you gain? What would get harder?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Every particle behaves identically. **Design a particle system** that supports sparks that
fall, smoke that rises, and a shockwave that expands — without writing three separate systems.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** At 50,000 particles the game slows down. **Before optimising anything**, how would you find
out where the time is actually going? Write your guess first, then say how you would check whether
your guess is right.

<div class="lines wide"><i></i><i></i><i></i></div>

---

## Stretch goals

1. The ball speeds up on every paddle hit.
2. Power-ups that drift across and change the paddle size.
3. A second ball after a long rally. Would a vector of balls have been easier?
4. **`reserve()` the particles and measure whether it helps.** Be honest if it does not.
5. Colour the particles by remaining life.
6. Convert to the erase-remove idiom and check nothing changed.
