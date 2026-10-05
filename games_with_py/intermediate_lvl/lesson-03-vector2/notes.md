# Lesson 3 — Vector2

> **Games with Python · Intermediate level · Lesson 3 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A ship that flies in **any** direction, turns to face where it is going, fires along whatever line it
is pointing down, and is chased by things that home in on it.

```
                  ·
            ·      ╲
       ▲            ╲        bullets leave along the nose,
      ╱ ╲            ·        not along x or y
     ╱   ╲
    ───────         ◆  ◆     chasers, all heading for the ship
                      ◆
```

pygame gives you `Vector2` already written, so today is less about building it than about **knowing
what is inside it** — including two traps that the documentation does not warn you about and that this
lesson will show you on your own machine.

## Where this fits

- **Back:** [lesson 2](../lesson-02-rects-images-and-the-display/notes.md) gave you `Rect` and the
  float trap. Today's positions are vectors, and the same trap is waiting in a new place.
- **Forward:** everything. [Lesson 4](../lesson-04-sprites-and-groups/notes.md) gives every sprite a
  `Vector2` position, and nothing after this lesson stops using them.
- **Other tracks:** `webgames` intermediate lesson 2 *writes* this class by hand, method by method.
  If you have done that lesson, you already know what is inside `Vector2` — and that is the right order
  to learn it in. C++'s intermediate lesson 5 uses raylib's version, which is the same object again.

---

## The idea, in plain words

### Two numbers that belong together

You have been writing this since the beginner level:

```python
self.x += self.speed_x * dt
self.y += self.speed_y * dt
```

Two lines, almost identical, and you must remember to change both. A **vector** is the admission that
`x` and `y` are not two separate facts but one fact with two parts.

```python
from pygame.math import Vector2

self.pos += self.velocity * dt        # one line, and it cannot get out of step
```

### The arrow picture, and where it stops being true

Think of a vector as an **arrow**: it has a direction and a length, and no position — the arrow meaning
"30 right, 40 down" is the same arrow wherever you draw it.

Where that stops being true, and it catches everybody: **the same two numbers do two different jobs.**
`Vector2(100, 50)` can be

- *a place* — the ship is at x=100, y=50; or
- *a movement* — go 100 right and 50 down.

Adding two positions is almost always a bug. Adding a movement to a position is the most common line in
game programming. **Subtracting** two positions gives a movement, and that is the single most useful
operation there is:

> **target − me = the way to the target.**

Every chasing enemy, homing missile, "look at the mouse" and knockback starts there.

### The three steps you will use constantly

```python
to_target = target_pos - self.pos      # 1. SUBTRACT: which way?
if to_target.length() > 0:             #    (the guard — see below)
    direction = to_target.normalize()  # 2. NORMALISE: direction only
    self.pos += direction * SPEED * dt # 3. SCALE, then add
```

**Subtract, normalise, scale.** Say it out loud; you will write it a hundred times this term.

Why normalise? Because `to_target` is as long as the gap happens to be. Use it directly as a speed and
your enemy rockets in from far away and crawls when close — the opposite of what anyone wants.
`normalize()` keeps the direction and forces the length to exactly **1**, so multiplying by `SPEED`
gives you the speed you asked for.

### Trap one: normalising a zero vector **raises**

In JavaScript, normalising `(0, 0)` gives `NaN`, which spreads silently and makes the sprite vanish for
ever with a clean console. Python is better behaved and louder:

```python
>>> Vector2(0, 0).normalize()
ValueError: Can't normalize Vector of length zero
```

A crash, with a line number, the moment it happens. That is a **gift** — but it will still end your
game, so guard it:

```python
gap = target - self.pos
if gap.length_squared() > 0:          # cheap: no square root
    self.pos += gap.normalize() * SPEED * dt
```

`length_squared()` avoids the square root, which matters when you are testing hundreds of enemies —
and comparing squared lengths is valid because squaring preserves order for non-negative numbers.

> **When does it actually happen?** When the chaser arrives exactly on the player. Which it will,
> because it is aiming for that exact point. Guard it, or stop the enemy a little short:
> `if gap.length() > 20:`. Best answers do both.

### Trap two: `Vector2` is **mutable**, and `+=` changes it in place

This is the one that costs people an afternoon, and it does not exist in the JavaScript version at all.

```python
>>> p = Vector2(0, 0)
>>> q = p                  # NOT a copy. Both names point at the same object.
>>> p += Vector2(5, 0)
>>> q
[5, 0]                     # q moved too
```

`q = p` does not copy a vector. And `+=` on a `Vector2` **modifies the object in place** rather than
making a new one, so everything that was looking at it sees the change.

Where this bites in a real game:

```python
# the bug
bullet.pos = ship.pos                 # alias! the bullet IS the ship's position
bullet.pos += bullet.velocity * dt    # ...so the ship moves with the bullet
```

```python
# the fix: make a copy
bullet.pos = Vector2(ship.pos)
```

`Vector2(other)` copies. Use it any time you store a vector that came from somewhere else. The same
applies to a shared default: giving every enemy `velocity = SHARED_ZERO` gives them all **one**
velocity between them.

### Trap three: `rotate` takes **degrees**

```python
>>> Vector2(1, 0).rotate(90)
[-0, 1]
```

Not radians. pygame uses degrees for `rotate`, `angle_to` and `as_polar`, and radians nowhere — which
is friendlier than the browser and the opposite of what you will expect if you have done the web track.

And notice the answer: rotating `(1, 0)` — pointing **right** — by +90° gives `(0, 1)`, which points
**down**. So positive degrees rotate **clockwise on screen**, because y points down. That is the same
reason angles went clockwise in the web track.

### The methods worth knowing

Every one of these is real and worth trying in a Python prompt right now:

| Call | What it does |
|---|---|
| `v.length()` | Pythagoras. The length of the arrow. |
| `v.length_squared()` | The same without the square root. For comparisons. |
| `v.normalize()` | A new vector, same direction, length 1. **Raises on zero.** |
| `v.normalize_ip()` | The same, **in place**. Changes `v` itself. |
| `v.rotate(degrees)` | A new vector, turned. Positive is clockwise on screen. |
| `v.angle_to(other)` | The angle between them, in degrees. |
| `v.dot(other)` | For unit vectors: 1 same way, 0 at right angles, −1 opposite. |
| `v.lerp(other, t)` | Partway from `v` to `other`. `t = 0.25` is a quarter of the way. |
| `v.distance_to(other)` | How far apart. There is a `_squared` version too. |
| `v.scale_to_length(n)` | **In place**: keep the direction, set the length to `n`. |
| `v.clamp_magnitude(n)` | A new vector, no longer than `n`. A speed limit in one call. |
| `v.move_towards(other, n)` | A new vector, `n` closer to `other`. Never overshoots. |
| `Vector2().from_polar((r, deg))` | **In place**: build from a length and an angle. |

Anything ending `_ip` changes the vector you called it on and returns `None`. Writing
`v = v.normalize_ip()` sets `v` to `None`, and the error appears somewhere else entirely.

### Vectors and `Rect`, together

`Rect` still holds integers, so the lesson 2 split survives — it just gets tidier:

```python
self.pos = Vector2(x, y)                 # floats: the truth
self.rect.center = self.pos              # ints: for drawing and colliding
```

Assigning a `Vector2` to a `Rect` attribute works and **truncates** — `Vector2(100.7, 50.2)` becomes
`(100, 50)`. Keep the vector as the real position, copy it into the rect for drawing, and never the
other way round.

### Angles, and facing where you are going

```python
# turning: an angle is one number that changes a little each frame
if keys[pygame.K_LEFT]:
    self.angle -= TURN_SPEED * dt          # degrees per second
if keys[pygame.K_RIGHT]:
    self.angle += TURN_SPEED * dt

# the direction the nose points: a unit vector built by rotating "right"
nose = Vector2(1, 0).rotate(self.angle)
self.pos += nose * THRUST * dt
```

And to draw the ship turned, remember lesson 2: `pygame.transform.rotate` takes degrees
**anticlockwise**, which is the opposite of `Vector2.rotate`. So the sprite needs `-self.angle`:

```python
image = pygame.transform.rotate(self.base_image, -self.angle)
rect = image.get_rect(center=self.rect.center)       # re-centre: it grew
screen.blit(image, rect)
```

That sign is the single most common "my ship points the wrong way" bug in pygame, and now you know why
it exists: one function is thinking in screen coordinates and the other in maths coordinates.

---

## The idea, in pictures

Open [the vectors explainer](../../../shared/visualizers/vectors.html).

**What to look for:** drag the two arrow tips and watch the **length** number. Find positions where an
arrow is exactly `(0.6, 0.8)` or `(1, 0)` — those are unit vectors. Then use the normalise control: the
arrow keeps its direction and snaps to the same length every time. That snapping-to-one is the whole
idea. Finally drag both tips to the same place and watch the numbers break — in Python that moment is a
`ValueError` rather than a silent `NaN`.

---

## The idea, in code

1. `code/01-vector-basics.py` — every method in the table above, on screen, on two vectors you drag
   with the mouse. The numbers and the picture move together.
2. `code/02-the-aliasing-trap.py` — two bullets, one copied and one aliased. Only one of them behaves.
   The ship moves when it should not, and the readout shows the shared object.
3. `code/03-aim-and-shoot.py` — the ship: turning, thrust along the nose, bullets, rocks, and the
   `transform.rotate` sign.
4. `code/04-chase-and-flee.py` — subtract-normalise-scale four ways: chase, flee, orbit and a vision
   cone from one dot product. Includes the zero-length guard, on a switch.

---

## The maths you just used

**1. Pythagoras.** `length()` is `√(x² + y²)` — the same theorem as the beginner level's circle
collision, doing the same job.

**2. Unit vectors.** Dividing both parts by the length leaves the direction and forces the length to 1.
Check it: `(30, 40)` has length 50, and `(0.6, 0.8)` gives `√(0.36 + 0.64) = √1 = 1`.

**3. Degrees, and why pygame chose them.** A full turn is 360°, which most people can picture, where
`2π` is a number you have to think about. The cost is that `math.cos` and `math.sin` still want radians,
so if you mix pygame's vector maths with the `math` module you will need `math.radians()`. Pick one and
be consistent.

**4. The dot product.** `v.dot(w)` is `v.x*w.x + v.y*w.y`. For two **unit** vectors it is the cosine of
the angle between them: 1 means the same way, 0 at right angles, −1 opposite. So a vision cone is one
line with no angle arithmetic and no awkwardness about 359° being next to 1°:

```python
if facing.dot(to_player.normalize()) > 0.7:     # 0.7 ≈ cos 45°, so ±45°
```

**5. Squared lengths.** `length_squared()` skips the square root. Comparing `a² < b²` gives the same
answer as `a < b` for non-negative numbers, so use it for every "is it within range?" test and compare
against `range * range`.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the zero-length guard, then drive a chaser onto the player | | |
| Write `bullet.pos = ship.pos` instead of `Vector2(ship.pos)` | | |
| Swap the subtraction: `self.pos - target` | | |
| Give every enemy the same `Vector2` as a starting velocity | | |
| Use `rotate(math.pi / 2)` instead of `rotate(90)` | | |
| Drop the minus sign in `transform.rotate(image, -self.angle)` | | |
| Write `v = v.normalize_ip()` | | |
| Normalise and then forget to multiply by `SPEED` | | |
| Store the position only in `rect.center` and move by 20 px/s | | |

The aliasing one is the most valuable in this whole lesson, because the symptom — *the ship moves when
you fire* — points nowhere near the cause.

---

## Think like an engineer

1. `Vector2` is **mutable** and JavaScript's hand-written version in the web track is **immutable**
   (every method returns a new object). Name one advantage of each. Which would you choose for a game
   with ten thousand particles, and why?
2. Python *raises* when you normalise a zero vector; JavaScript returns `NaN`. Which behaviour would you
   rather have while building a game, and which would you rather ship to players? Is that the same
   answer?
3. **Design something.** A homing missile that *turns* towards its target rather than snapping to face
   it, so it can overshoot, loop round and come back. What must it remember beyond a position? What
   limits how fast it turns? (`angle_to` and `rotate` are both useful here.)
4. **The hard one.** A ball bounces off a flat wall by flipping one component of its velocity. What
   about a wall at 30°? You have a unit vector along the wall, a unit vector at right angles to it, and
   `dot`. What does "the part of my velocity heading into the wall" mean, and what would you do to it?

---

## Vocabulary

| Word | What it means |
|---|---|
| **Vector** | Two numbers treated as one thing: a direction and a length. |
| **Magnitude / length** | How long the arrow is. `√(x² + y²)`. |
| **Unit vector** | Length exactly 1. A pure direction. |
| **`normalize()`** | Make a unit vector. **Raises** on a zero vector. |
| **`_ip`** | "In place" — changes the vector itself and returns `None`. |
| **Aliasing** | Two names for one object. `q = p` does not copy. |
| **`dot`** | For unit vectors: 1 same way, 0 at right angles, −1 opposite. |
| **Degrees** | What pygame's `rotate` and `angle_to` use. Not radians. |
| **`length_squared`** | Length without the square root. For comparisons. |
| **`clamp_magnitude`** | A speed limit, in one call. |

---

## Recap

- `x` and `y` are **one fact**. Treat them as one thing and a class of bug disappears.
- **target − me** is the direction to the target. Say the sentence; the order is not arbitrary.
- **Subtract, normalise, scale** — chasing, aiming, shooting and knockback are all this recipe.
- `normalize()` on a zero vector **raises**. Guard it with `length_squared() > 0`.
- `Vector2` is **mutable**: `q = p` is an alias, and `+=` changes the object in place. Copy with
  `Vector2(other)`.
- `rotate` takes **degrees**, positive is clockwise on screen, and `transform.rotate` goes the other
  way — hence the minus sign.
- Keep the real position in a `Vector2`; copy it into the `Rect` for drawing.

---

## Stretch goals

1. **Turn, do not snap.** A chaser whose facing turns at a maximum of 180°/second. Use `angle_to`, and
   watch for the ±180° wrap.
2. **`clamp_magnitude` as a speed limit**, applied to the whole velocity rather than to x and y
   separately. Then prove to yourself that the per-axis version lets diagonal movement be faster.
3. **Knockback.** On a hit, push the player away from the thing that hit them. One line, using the
   subtraction the other way round.
4. **A trail.** Keep the last fifteen positions as copied vectors and draw them fading. You will find out
   quickly whether you copied them.
5. **The 30° wall.** Question 4, for real, with a slope you can drag.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `02-the-aliasing-trap.py`. Fire a bullet; the ship jumps. Ask what is wrong with the firing code. Nothing is — the bug is one missing `Vector2(...)` and it is not on the line that misbehaves. |
| 10–25 | **Concept.** The vectors visualizer, spending most of it on *normalise*. Then subtract-normalise-scale on the board as a recipe with a name. |
| 25–40 | **Live-code** a chaser in six lines, including the guard. Then delete the guard and let it crash in front of them — the `ValueError` is a good thing to have seen once. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. |
| 120–140 | Break-it-on-purpose. The aliasing one and the `transform.rotate` sign. |
| 140–150 | Recap. Lesson 4 hands the bookkeeping to pygame's sprite system. |

**What usually goes wrong**

1. **`ValueError: Can't normalize Vector of length zero`**, the first time a chaser arrives exactly on
   the player. This is the lesson working as intended; make sure they fix it with a guard rather than a
   `try`.
2. **The ship drifts when a bullet is fired.** Aliasing. Expect this one and let it run — it is the best
   bug in the lesson, because the symptom and the cause are in different files.
3. **The ship points 90° away from where it travels.** The missing minus in `transform.rotate`, or
   mixing degrees and radians.
4. **`AttributeError: 'NoneType' object has no attribute 'x'`.** They wrote `v = v.normalize_ip()`.
   Worth a minute on the convention: `_ip` methods return `None` on purpose, to stop exactly this.
5. **Everything moves at one pixel per second.** They normalised and forgot to multiply by `SPEED`. Ask
   what units a unit vector is in. (None. That is the point of it.)
6. **All the enemies share a velocity.** A `Vector2` used as a default or a module-level constant and
   then mutated with `+=`. The same mutability trap in a new place, and genuinely confusing.
7. **The chaser moves in steps of one pixel.** They stored the position in `rect.center`, which is
   integers. Lesson 2's trap, returning.

**If you are running short on time** — cut the dot product and the vision cone; lesson 10 can introduce
them where enemies need them. Cut `code/04` too. Do **not** cut the zero guard or the aliasing demo:
those are the two things that will otherwise cost a student a whole evening.

**For the student who finishes at minute 90** — stretch goal 1 (turn, do not snap) produces visibly
better movement than the lesson's own version, which is motivating. Stretch goal 3 (knockback) takes
two minutes and improves any game they have.

**The point to land at the end:** pygame handed them a class the web track writes by hand, and it is
*better* in one way — it shouts instead of silently producing `NaN` — and *more dangerous* in another,
because it is mutable and `+=` changes things other people are looking at. Using somebody else's
library well means knowing which of those two it is, and the only way to find out is to try it.
