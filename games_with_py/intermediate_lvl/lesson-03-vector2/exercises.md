# Lesson 3 — Vector2

## Cheat sheet

### The recipe

```python
to_target = target - self.pos        # 1. SUBTRACT
if to_target.length_squared() > 0:   #    the guard
    d = to_target.normalize()        # 2. NORMALISE
    self.pos += d * SPEED * dt       # 3. SCALE
```

Say step 1 out loud: **target minus me**.

### Three traps pygame will not warn you about

**1. normalising zero RAISES**

```python
Vector2(0, 0).normalize()
# ValueError: Can't normalize Vector of length zero
```

Better than JavaScript's silent `NaN` — and it still ends your game. Guard it.

**2. Vector2 is MUTABLE and `+=` is in place**

```python
q = p            # NOT a copy — one object, two names
p += Vector2(5, 0)
q                # [5, 0]  ← q moved too
```

```python
bullet.pos = Vector2(ship.pos)    # copy!
```

**3. rotate takes DEGREES, and the two rotations disagree**

```python
Vector2(1, 0).rotate(90)  →  [0, 1]   # clockwise on screen
pygame.transform.rotate(img, -angle)  # anticlockwise → needs the minus
```

### The methods

```
length()          length_squared()
normalize()       normalize_ip()      ← _ip returns None
rotate(deg)       angle_to(other)
dot(other)        lerp(other, t)
distance_to(o)    distance_squared_to(o)
scale_to_length(n)   ← in place
clamp_magnitude(n)   ← a speed limit
move_towards(o, n)
Vector2().from_polar((r, deg))
```

### With Rect

```python
self.pos = Vector2(x, y)      # floats: the truth
self.rect.center = self.pos   # ints: truncated, for drawing
```

### Vision cone, one line

```python
facing.dot(to_player.normalize()) > 0.7     # ±45°
```

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> Write the sentence that tells you which way round a subtraction goes, and say what the result <em>is</em>.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> What does <code>normalize()</code> do, what does it do on a zero vector, and how is that different from the JavaScript version?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Explain what is wrong with <code>bullet.pos = ship.pos</code>, and give the fix.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> What units does <code>Vector2.rotate</code> take, and which way does a positive angle turn on screen? Why that way?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> What does a method ending <code>_ip</code> do, and what does it return?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> When would you use <code>length_squared()</code> rather than <code>length()</code>, and why is it allowed?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A7.</span> Why does drawing a rotated sprite need <code>-self.angle</code> rather than <code>self.angle</code>?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> Give the length and the normalised form of <code>Vector2(9, 12)</code>. Show your working.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What is printed?

```python
p = Vector2(1, 1)
q = p
p += Vector2(4, 0)
print(q)

a = Vector2(1, 1)
b = Vector2(a)
a += Vector2(4, 0)
print(b)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> What does <code>Vector2(1, 0).rotate(90)</code> give, and where does that point on the screen?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> An enemy is at <code>(100, 100)</code>, the player at <code>(160, 180)</code>, <code>SPEED</code> is 200 and <code>dt</code> is 0.1. Where is the enemy after one frame of the recipe?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> What happens here, and on which line?

```python
v = Vector2(3, 4)
v = v.normalize_ip()
print(v.length())
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The game crashes the moment a chaser reaches the player. Name the exception and the fix.

```python
d = (player.pos - self.pos).normalize()
self.pos += d * SPEED * dt
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Firing a bullet makes the <em>ship</em> fly off. The firing code looks fine and the bullet code looks fine.

```python
bullet = Bullet()
bullet.pos = ship.pos
bullet.velocity = nose * BULLET_SPEED
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> Every enemy in the wave moves as one, as though they were a single object.

```python
ZERO = Vector2(0, 0)

class Enemy:
    def __init__(self):
        self.velocity = ZERO
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C4.</span> The enemy creeps along at about a pixel a second. <code>SPEED</code> is 240.

```python
d = (player.pos - self.pos).normalize()
self.pos += d
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C5.</span> The ship travels correctly but the sprite points 90&deg; away from the direction of travel. Two separate things could cause this &mdash; name both.

```python
nose = Vector2(1, 0).rotate(self.angle)
self.pos += nose * THRUST * dt
image = pygame.transform.rotate(self.base, self.angle)
screen.blit(image, self.rect)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> In a Python prompt, try every method in the cheat sheet on <code>Vector2(3, 4)</code>. Write down what <code>normalize()</code> on <code>Vector2(0, 0)</code> does, in the exact words of the error.</li>
<li><strong>Checkpoint 2.</strong> Prove the aliasing trap to yourself: two names, one <code>+=</code>, and a <code>print</code>. Then do it again with <code>Vector2(other)</code>.</li>
<li><strong>Checkpoint 3.</strong> Give your player from lesson 2 a <code>Vector2</code> position and velocity. Move with <code>self.pos += self.velocity * dt</code>, and copy into <code>rect.center</code> for drawing.</li>
<li><strong>Checkpoint 4.</strong> Add an <code>angle</code> and turn with the left and right keys. Draw a line out of the nose so you can see the direction before you move along it.</li>
<li><strong>Checkpoint 5.</strong> Thrust along the nose. Then draw the sprite rotated &mdash; and get the minus sign right by testing, not by guessing.</li>
<li><strong>Checkpoint 6.</strong> Fire bullets from the nose. Copy the ship's position with <code>Vector2(...)</code>, then deliberately remove the copy and watch what happens.</li>
<li><strong>Checkpoint 7.</strong> Add three chasers using subtract&ndash;normalise&ndash;scale, with the zero guard. Then make one of them flee by changing exactly one thing.</li>
<li><strong>Checkpoint 8.</strong> Add a speed limit with <code>clamp_magnitude</code>. Then try limiting <code>velocity.x</code> and <code>velocity.y</code> separately instead, and measure whether diagonal movement is faster.</li>
</ul>

<div class="note">
<span class="note-label">If something moves when it should not</span>
<p>Print <code>id(a), id(b)</code> for the two vectors. The same number means one
object with two names, and you have found an aliasing bug &mdash; which is almost
never on the line where the symptom appears.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** pygame's `Vector2` is **mutable**; the web track's hand-written version is
**immutable**. Give one advantage of each. Which would you choose for ten thousand
particles, and why?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Python raises on a zero normalise; JavaScript returns `NaN`. Which would
you rather have while building, and which would you rather ship? Is that the same
answer?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Design a homing missile that *turns* towards its target rather than
snapping. What must it remember beyond a position? What limits the turn? Write the
update in words, then in code.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. A ball bounces off a flat wall by flipping one component.
Now the wall is at 30&deg;. With a unit vector along the wall, one at right angles,
and `dot`, what does "the part of my velocity heading into the wall" mean, and what
would you do to it?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. A chaser that turns at most 180&deg;/second, using `angle_to`. Mind the wrap.
2. `clamp_magnitude` as a speed limit; prove the per-axis version is wrong.
3. Knockback: one line, with the subtraction reversed.
4. A fading trail of the last fifteen positions. You will find out whether you
   copied them.
5. The 30&deg; wall (E4), with a slope you can drag.
