# Lesson 5 — Many Things At Once

> **Games with C++ · Beginner level · Lesson 5 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**ASCII Pong** — with a ball, two paddles, a score, and a trail of particles that spray out on every
hit and fade away.

```
  ##################################
  #                                #
  #|                          *    #
  #|          o   .  ·             #
  #|                            |  #
  #                             |  #
  ##################################
        3  -  2        particles: 14
```

The new idea is `std::vector`: a list that grows and shrinks while the game runs. It is what lets you
have *however many* of something.

## Where this fits

- **Back:** [lesson 4](../lesson-04-input-and-movement/notes.md) gave you real-time input and grid
  movement.
- **Forward:** [lesson 6](../lesson-06-capstone-ascii-arcade/notes.md) is the capstone.
- **Today:** collections that change size, and smooth movement instead of grid movement.

---

## The idea, in plain words

### An array has a fixed size. A vector does not.

```cpp
char screen[WIDTH * HEIGHT];     // exactly this many, decided when you compile
```

That is fine for a screen. It is useless for particles, because you do not know how many there will
be — it depends on what happens in the game.

```cpp
#include <vector>

std::vector<Particle> particles;        // starts empty

particles.push_back(p);                 // add one to the end
particles.size();                       // how many there are now
particles[3];                           // get the one at index 3
particles.clear();                      // remove them all
```

`std::vector<Particle>` reads as *"a vector of Particles"*. The thing in angle brackets is the type it
holds, and you can have a vector of anything: `std::vector<int>`, `std::vector<std::string>`,
`std::vector<Paddle>`.

> **Why "vector"?** Nothing to do with the arrows in maths. It is a historical name and it is
> unfortunate, because this course also uses "vector" to mean a direction. In C++ they are unrelated:
> `std::vector` is a growable list, and that is all.

### Smooth movement needs `double`, not `int`

Lesson 4's maze moved a whole square at a time. Pong does not — the ball drifts smoothly, so its
position needs decimals:

```cpp
struct Ball {
    double x, y;              // smooth position
    double speed_x, speed_y;  // squares per SECOND
};
```

And then drawing needs a conversion, because the screen only has whole squares:

```cpp
put((int)ball.x, (int)ball.y, 'o');
```

`(int)` **truncates** — it throws the fraction away rather than rounding. So `3.9` becomes `3`, and
`-0.5` becomes `0`. If you want rounding, say so: `(int)(ball.x + 0.5)` for positive numbers, or
`std::lround(ball.x)` properly.

> This split — **simulate in decimals, draw in whole squares** — is how every game works, including
> ones with pixels. The simulation is continuous; the screen is a grid. You have just met the join
> between them.

### Removing things from a vector while looping

Particles die. Bullets leave the screen. You need to remove things, and doing it the obvious way is
a bug you have now seen three times:

```cpp
// WRONG - skips elements
for (std::size_t i = 0; i < particles.size(); i++) {
    if (particles[i].life <= 0.0) {
        particles.erase(particles.begin() + i);
    }
}
```

Erasing element `i` shifts everything after it down one place, so `i++` steps straight over the next
one. About half the dead particles survive.

The simplest fix is to **loop backwards**, exactly as in the Python and JavaScript tracks:

```cpp
for (int i = (int)particles.size() - 1; i >= 0; i--) {
    particles[i].life -= dt;
    if (particles[i].life <= 0.0) {
        particles.erase(particles.begin() + i);
    }
}
```

Note the `(int)` cast. `size()` returns an **unsigned** type, which cannot be negative — so when it
reaches 0 and you subtract 1, it wraps round to an enormous number and the loop runs for ever.
`-Wall` will warn you about comparing signed and unsigned values, which is one more reason to leave
it switched on.

### The way C++ programmers actually do it

There is a neater idiom, and it is worth meeting now because you will see it everywhere:

```cpp
#include <algorithm>

particles.erase(
    std::remove_if(particles.begin(), particles.end(),
                   [](const Particle& p) { return p.life <= 0.0; }),
    particles.end());
```

That is the **erase-remove idiom**. `std::remove_if` shuffles everything you want to keep to the
front and tells you where the keepers end; `erase` then chops off the rest. It does the whole job in
one pass instead of shifting the vector on every removal.

The `[](const Particle& p) { ... }` part is a **lambda** — a small unnamed function written where it
is used. You do not need to write these yet. You need to recognise one when you see it, because real
C++ code is full of them.

Use the backwards loop today. Know the idiom exists.

### Bouncing, in decimals

```cpp
ball.x += ball.speed_x * dt;
ball.y += ball.speed_y * dt;

if (ball.y < 1.0) {
    ball.y = 1.0;                       // position first
    ball.speed_y = -ball.speed_y;       // then velocity
}
```

Same rule as every other track: **fix the position, then flip the velocity**, or the ball sticks to
the wall and vibrates.

---

## The idea, in pictures

Open [the box collision explainer](../../../shared/visualizers/aabb-collision.html).

**What to look for:** the four conditions. Today's paddle is one square wide and several tall, so the
test simplifies a lot — but it is the same four comparisons underneath, and watching them flip one at
a time is the clearest way to see why all four are needed.

Then open [the gravity explainer](../../../shared/visualizers/gravity-and-velocity.html).

**What to look for:** press Step and watch the numbers table. Your particles do exactly this — a
speed that changes a position, every frame, multiplied by `dt`.

---

## The maths you just used

### Why `(int)` is not rounding

```cpp
(int)3.9      // 3   - the .9 is thrown away
(int)3.1      // 3
(int)-0.5     // 0   - it truncates TOWARDS ZERO, not downwards
```

This matters at the edges of the screen. A ball at `x = 0.6` draws at column 0, and so does a ball at
`x = 0.1` — so the ball appears to pause for a moment before moving on. That is not a bug in your
physics; it is the screen being coarse.

### Steering the ball off the paddle

```cpp
double centre = paddle.y + paddle.height / 2.0;
double offset = (ball.y - centre) / (paddle.height / 2.0);   // -1 .. +1
ball.speed_y = offset * STEER_STRENGTH;
```

Note `2.0` and not `2`. With `paddle.height / 2` and an `int` height, you would get whole-number
division and a centre that is half a square out — and the steering would be subtly wrong in a way
that is very hard to see.

**Mixing `int` and `double` arithmetic is one of the most common sources of quiet bugs in C++.** When
in doubt, write the decimal point.

### A random direction for particles

```cpp
double angle = random_double(0.0, 2.0 * 3.14159265);
double speed = random_double(4.0, 14.0);
p.speed_x = std::cos(angle) * speed;
p.speed_y = std::sin(angle) * speed;
```

Pick an **angle**, then convert. Picking random x and y separately scatters into a *square*, with
more particles heading diagonally — the same point the web track makes in its lesson 5.

---

## Break it on purpose

Use `code/02-ascii-pong.cpp`. Compile each time.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Loop *forwards* through particles while erasing | | |
| Remove the `(int)` from `(int)particles.size() - 1` | | |
| Change `paddle.height / 2.0` to `paddle.height / 2` | | |
| Remove the position fix before flipping `speed_y` | | |
| Spawn 50,000 particles on every hit | | |
| Change `double x, y` in `Ball` to `int x, y` | | |

The second one is spectacular and worth doing: the loop runs for billions of iterations and the
program appears to hang. The last one makes the ball move in jerky whole squares and reveals exactly
why smooth movement needs decimals.

---

## Think like an engineer

1. **`push_back` sometimes has to move everything.** A vector holds its items in one continuous block
   of memory. When it runs out of room it allocates a bigger block and copies everything across. What
   does that mean for a game spawning particles every frame? *(Look up `reserve()` — what does it do,
   and when would you call it?)*
2. **You have one vector of particles and separate variables for the ball and paddles.** Why not put
   everything in one vector of "entities"? What would you gain? What would get harder?
3. **Design a particle system.** Right now every particle behaves identically. How would you support
   sparks that fall, smoke that rises, and a shockwave that expands — without writing three separate
   systems?
4. **The honest question.** At 50,000 particles the game slows down. Before optimising anything, how
   would you find out *where* the time is actually going? What would you guess, and how would you
   check whether your guess is right?

---

## Vocabulary

| Word | What it means |
|---|---|
| **`std::vector`** | A list that can grow and shrink while the program runs. |
| **`push_back`** | Add one item to the end. |
| **`erase`** | Remove an item at a position. |
| **`size()`** | How many items there are. Returns an **unsigned** type. |
| **Cast** (`(int)x`) | Convert a value to another type. `(int)` truncates. |
| **Lambda** | A small unnamed function written where it is used. |
| **Erase-remove idiom** | The standard way to delete many items from a vector at once. |

---

## Recap

- `std::vector<T>` is a list that grows. Use it when you do not know how many there will be.
- **Simulate in `double`, draw in `int`.** `(int)` truncates; it does not round.
- **Loop backwards when erasing**, and cast `size()` to `int` first or the loop never ends.
- `erase` + `remove_if` is how it is done properly. Recognise it; use the backwards loop for now.
- **Fix the position, then flip the velocity.** Fourth time you have met this rule.
- Write `2.0` not `2` when dividing, or whole-number division will bite you.

---

## Stretch goals

1. **Make the ball speed up** on every paddle hit. Find a rate that makes rallies exciting rather
   than impossible.
2. **Power-ups** that drift across the screen and change the paddle size when hit.
3. **A second ball** after a rally of five. How much code changed? Would a vector of balls have been
   easier?
4. **`reserve()` the particles vector** at the start and measure whether it makes any difference.
   Be honest about the result — it may well not.
5. **Colour the particles** by how much life they have left, using ANSI codes.
6. **Convert to the erase-remove idiom** and check the game still behaves identically.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Ask how you would store 200 particles when you do not know in advance how many there will be. Let them propose a big array and find the problem themselves. |
| 10–30 | **Concept.** `std::vector`, then the backwards-erase bug. Do the erase bug on the board with six boxes and indexes — it is the fourth appearance of this bug in the course, and worth saying so. |
| 30–45 | **Live-code** the particle struct, spawn, update and draw. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. The unsigned-underflow one is dramatic. |
| 140–150 | Recap. Next week: the capstone. |

**What usually goes wrong**

1. **Half the particles never disappear.** Forward loop with erase. Fourth appearance — point that
   out explicitly, because recognising a repeated bug is a real skill.
2. **The program hangs.** `particles.size() - 1` without the `(int)` cast. `size()` is unsigned, so
   `0 - 1` wraps to about 18 quintillion and the loop runs essentially for ever. `-Wall` warns about
   the signed/unsigned comparison — show them the warning they ignored.
3. **The ball moves in visible jumps.** They used `int` for position. Good discovery; let it happen.
4. **The paddle steering is subtly wrong.** `height / 2` instead of `height / 2.0`. Hard to spot,
   which makes it worth demonstrating.
5. **Everything disappears after a few seconds.** They are erasing inside a range-based `for`, which
   invalidates the iterator. The behaviour is undefined — it may crash, may not, and may differ
   between machines.
6. **`-Wall` warnings about comparing signed and unsigned.** Do not let them ignore these. It is
   exactly the bug in point 2, reported in advance.

**If you are running short on time** — give them the `Particle` struct and `spawn_particles` as a
paste-in, and spend the build on the vector loop and the Pong mechanics. The vector is the lesson.

**For the student who finishes at minute 90** — stretch goal 4 (`reserve()` and measure) is the best
one, because the honest answer is often "no measurable difference at this scale". A student who
carefully measures an optimisation and finds it did nothing has learned something more valuable than
one who applies it on faith. Stretch goal 6 (the erase-remove idiom) suits a student who wants to
read real C++.

**The thing to land:** the backwards-erase bug has now appeared in **four** languages — JavaScript
particles, Python fruit, Python bricks, and C++ particles. Put that on the board. It is not a C++
problem, or a Python problem. It is a *lists* problem, and they will meet it again in whatever
language they use next.
