# Lesson 3 — Solutions and marking notes

---

## Section A

**A1.** [2] **"target minus me."** One mark. The result is a **movement** (a direction with a length),
not a position — one mark. Credit anyone who notes that subtracting two positions is the one case where
mixing the two meanings is not only allowed but is the point.

**A2.** [3] It returns a new vector with the same direction and length exactly 1 — one mark. On a zero
vector it **raises `ValueError: Can't normalize Vector of length zero`** — one mark. JavaScript divides
by zero and returns `NaN`, which never throws, spreads to everything it touches, and leaves the sprite
gone for ever with a clean console — one mark.

**A3.** [3] `ship.pos` is an object, and `=` makes a second **name** for it rather than a copy — one
mark. So moving the bullet with `+=` moves the ship too, because `+=` on a `Vector2` changes the object
in place — one mark. Fix: `bullet.pos = Vector2(ship.pos)` — one mark.

**A4.** [2] **Degrees** — one mark. A positive angle turns **clockwise on screen**, because y points
down: `Vector2(1, 0).rotate(90)` is `(0, 1)`, which is downwards — one mark.

**A5.** [2] It modifies the vector it was called on, rather than returning a new one — one mark — and it
returns **`None`** — one mark. (Which is why `v = v.normalize_ip()` sets `v` to `None`.)

**A6.** [2] When comparing distances or testing a radius, because it skips the square root, which is the
expensive part — one mark. It is valid because squaring preserves order for non-negative numbers, so
`a² < b²` exactly when `a < b`. Remember to compare against `range * range` — one mark.

**A7.** [3] `Vector2.rotate` turns clockwise on screen (positive y is down), while
`pygame.transform.rotate` turns **anticlockwise**, the way a mathematician would draw it — two marks. So
the two disagree by a sign, and negating the angle makes the picture match the movement — one mark.

---

## Section B

**B1.** [3] `length = √(81 + 144) = √225 = 15`. Two marks. Normalised: `(9/15, 12/15) = (0.6, 0.8)` —
one mark. (A 3-4-5 triangle scaled by three, which is why the numbers are tidy.)

**B2.** [4] First `print`: **`[5, 1]`** — `q` is the same object as `p`, and `+=` changed it in place.
Two marks. Second `print`: **`[1, 1]`** — `Vector2(a)` made a copy, so `b` was unaffected. Two marks.

**B3.** [3] `(0, 1)` — two marks — which points **downwards** on screen, because y increases downwards —
one mark. Accept `[-0, 1]`, which is what pygame prints.

**B4.** [4] `to_player = (60, 80)`; `length = 100`; `direction = (0.6, 0.8)`;
`step = direction * 200 * 0.1 = (12, 16)`; new position `(112, 116)`. One mark per stage up to four.

**B5.** [3] `normalize_ip()` returns `None`, so `v` becomes `None` — two marks — and the crash happens on
the **third** line, `AttributeError: 'NoneType' object has no attribute 'length'`, not on the line that
caused it — one mark.

---

## Section C

**C1.** [3] `ValueError: Can't normalize Vector of length zero`, because the two positions are identical
so the subtraction gives `(0, 0)` — two marks. Fix: guard with
`if (player.pos - self.pos).length_squared() > 0:`, or stop the chaser a little short of the player —
one mark. Best answers do both.

**C2.** [4] `bullet.pos = ship.pos` makes the bullet's position **the same object** as the ship's — two
marks. The bullet's own `+= velocity * dt` then moves the ship as well — one mark. Fix:
`bullet.pos = Vector2(ship.pos)` — one mark.

Worth saying to the class: nothing on the lines that misbehave is wrong. The bug is an assignment in a
different file, and that is why it is worth meeting once in a lesson rather than alone at home.

**C3.** [3] Every `Enemy` is given **the same** `Vector2` object, so the first `+=` changes it for all of
them — two marks. Fix: `self.velocity = Vector2(0, 0)` inside `__init__`, a fresh object per enemy — one
mark.

Credit anyone who connects this to Python's mutable-default-argument trap; it is the same hazard.

**C4.** [3] The direction is a **unit** vector, so adding it moves exactly one pixel per frame, and
nothing is multiplied by `SPEED` or by `dt` — two marks. Fix: `self.pos += d * SPEED * dt` — one mark.

**C5.** [4] Two causes, two marks each. (a) The missing minus:
`pygame.transform.rotate(self.base, -self.angle)`, because the two rotations run in opposite
directions. (b) The rotated image is **larger** than the original and is being blitted at the old rect,
so it is offset as well — it needs `image.get_rect(center=self.rect.center)`.

Accept a third: drawing a base sprite that points up rather than right, so angle 0 is already 90° out.

---

## Section D — marking the build

1. **Checkpoint 1 produced the exact error text.** Having read `Can't normalize Vector of length zero`
   once is what makes it recognisable at 10pm.
2. **Checkpoint 2 was actually run.** Two `print`s, two different answers. It takes a minute and it
   inoculates them against the worst bug in the lesson.
3. **The position is a `Vector2`, copied into `rect.center`** (checkpoint 3), not the other way round.
   Test by moving at 20 px/s.
4. **Checkpoint 6 was done both ways.** Removing the copy on purpose, seeing the ship fly off, and
   putting it back is worth more than being told.
5. **The zero guard is present** (checkpoint 7). Make them drive a chaser onto the player in front of
   you.
6. **Checkpoint 8 produced a measurement**, not an opinion.

---

## Section E — marking notes

**E1.**

*Mutable (pygame):* fewer objects created, so less work for the garbage collector — which matters with
thousands of particles. `pos += velocity * dt` does not allocate a new position every frame.
**Cost:** aliasing bugs, as C2 and C3 showed, and you can never be sure a vector you were handed will
not change underneath you.

*Immutable (the web track's):* nothing can change behind your back, so a bug in one place cannot appear
in another. **Cost:** an object per operation; three per chaser per frame.

For ten thousand particles: **mutable**, and preferably reusing the same vectors from a pool. Full marks
require naming the aliasing cost of that choice, and strong answers note that the real answer is to
measure rather than assume — which is what the web track's lesson 9 does.

**E2.** The honest answer is that they are **not** the same.

*While building:* raising is better. It stops at the line, with a message, and you fix it in thirty
seconds. `NaN` gives you a vanished sprite and an empty console.

*While shipping:* an uncaught `ValueError` ends the player's game. You want the guard, so that neither
happens — or a top-level handler that saves and apologises.

Full marks for distinguishing the two situations and for concluding that the real answer is the guard,
so the question never arises. Credit anyone who says "raise during development, return a safe value in a
release build", which is a real technique.

**E3.** A good answer lists:

- it must remember **its own facing**, as an angle or a unit vector, separately from where the target is;
- a **turn rate** in degrees per second limits it;
- each frame: find the desired angle (`self.facing.angle_to(to_target)`), clamp that difference to
  `turn_rate * dt`, and `rotate` by the clamped amount;
- then fly along **its own facing**, not towards the target.

The subtlety worth hunting for: `angle_to` can return a value near ±180, and clamping without thinking
about the wrap makes a missile at 179° turn the long way round. Students discover this by watching a
missile spin. Credit anyone who predicts it.

**E4.** This is the reflection formula.

- Let `n` be the unit vector at right angles to the wall (the **normal**).
- `v.dot(n)` is **how much of the velocity is heading into the wall**. That is the part to reverse; the
  part along the wall should be untouched.
- Subtracting it once removes it (a slide along the wall). Subtracting it **twice** reverses it:

```python
velocity = velocity - n * (2 * velocity.dot(n))
```

Check it against a case they know: a floor has `n = (0, -1)`, so `v.dot(n) = -vy`, and the formula gives
`vy' = -vy` with `vx` untouched — exactly the beginner-level bounce. Full marks for reaching "subtract
twice", with or without the notation, and strong credit for testing it against the flat-wall case, which
is a habit worth more than the formula.

---

## If you only mark one thing

Checkpoint 2 — the aliasing demonstration, run, with two different answers printed. It is a minute's
work, it is the only trap in this lesson whose symptom appears nowhere near its cause, and it is the one
they will otherwise meet alone.
