# Lesson 2 — Rects, Images And The Display

## Cheat sheet

### Rect

```python
r = pygame.Rect(left, top, width, height)
```

Reading **and writing** these moves the box:

```
left right top bottom
centerx centery center
topleft midtop topright
midleft        midright
bottomleft midbottom bottomright
width height size
```

```python
r.bottom = floor_y        # "stand on the floor"
r.center = (320, 240)     # "put me in the middle"
```

```python
a.colliderect(b)          # the AABB test, already written
r.collidepoint(mouse)
r.clamp_ip(screen_rect)   # move me inside that
```

### ⚠ Rect holds INTEGERS

```python
self.x += SPEED * dt         # float — the truth
self.rect.x = round(self.x)  # int — for drawing and colliding
```

Store the position only in the rect and slow movement **silently vanishes**.
`Rect` truncates, so `-3.7` becomes `-3`.

### Surface

```python
s = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(s, (255,212,59), (16,16), 14)

screen.blit(s, (x, y))
screen.blit(s, rect)
screen.blit(sheet, (x, y), source_rect)   # part of it
```

No `SRCALPHA` = a black box behind your sprite.

### Loading, when you do have files

```python
img = pygame.image.load("hero.png").convert_alpha()
```

Without `convert_alpha()` pygame converts on **every blit**.

### Text

```python
font = pygame.font.SysFont(None, 28)
label = font.render("SCORE 120", True, (231,236,243))
screen.blit(label, (14, 14))
```

`render` makes a **new Surface** every call. Do not call it for unchanged text
every frame.

### Transform — once, not per frame

```python
big = pygame.transform.scale(s, (64, 64))
flip = pygame.transform.flip(s, True, False)
turned = pygame.transform.rotate(s, 30)
```

A rotated Surface is **bigger**, so re-centre it:

```python
rect = turned.get_rect(center=old_rect.center)
```

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Name five attributes of a <code>Rect</code>, and say what happens when you <em>assign</em> to one.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> What does <code>Rect</code> store its numbers as, and what is the symptom of storing a position only in the rect?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> What is a <code>Surface</code>? Name three things in a pygame program that are one.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> What does <code>pygame.SRCALPHA</code> do, and what do you see without it?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why call <code>.convert_alpha()</code> when loading an image, and when does the cost of skipping it appear?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why should <code>pygame.transform.rotate</code> not be called every frame?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A7.</span> A rotated Surface drifts across the screen as it turns. Why, and what fixes it?
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> <code>r = pygame.Rect(100, 50, 40, 60)</code>. Give <code>r.right</code>, <code>r.bottom</code>, <code>r.center</code> and <code>r.midbottom</code>.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> Same rect. After <code>r.center = (200, 200)</code>, what are <code>r.left</code> and <code>r.top</code>?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> <code>SPEED</code> is 30 and the game runs at 60 fps. Describe what each version does over one second.

```python
# version A
rect.x += SPEED * dt

# version B
self.x += SPEED * dt
self.rect.x = round(self.x)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> <code>r.x = -3.7</code>. What does <code>r.x</code> hold? What would <code>round(-3.7)</code> have given?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> A 32&times;32 Surface is rotated by 45&deg;. Roughly how big is the Surface that comes back, and why?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> Every sprite has a solid black rectangle around it.

```python
sprite = pygame.Surface((32, 32))
pygame.draw.circle(sprite, (255, 212, 59), (16, 16), 14)
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The player does not move at all. The keys are definitely being read &mdash; a print inside the <code>if</code> fires. <code>SPEED</code> is 40.

```python
if keys[pygame.K_RIGHT]:
    player_rect.x += SPEED * dt
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> <code>TypeError: argument 1 must be pygame.Surface, not tuple</code>.

```python
screen.blit((255, 0, 0), (100, 100))
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The game runs at 12 fps with only thirty things on screen. Two separate causes are visible here.

```python
for enemy in enemies:
    sprite = pygame.transform.rotate(enemy.base, enemy.angle)
    label = font.render(str(enemy.hp), True, (255, 255, 255))
    screen.blit(sprite, enemy.rect)
    screen.blit(label, (enemy.rect.x, enemy.rect.y - 18))
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> The player can be pushed half-way off the right-hand edge of the window.

```python
player.rect.right = min(player.rect.right, WIDTH)
player.rect.x = min(player.rect.x, WIDTH)
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write <code>make_sprite(size, colour)</code> that returns a Surface with <code>SRCALPHA</code>, drawn from numbers that are all fractions of <code>size</code>. Blit it. Then double <code>size</code> and check it still looks right.</li>
<li><strong>Checkpoint 2.</strong> Give your player a float <code>x</code>, <code>y</code> <em>and</em> a <code>Rect</code>. Move the floats, <code>round()</code> them into the rect, and draw using the rect. Then try moving at 20 px/s and confirm it works.</li>
<li><strong>Checkpoint 3.</strong> Draw every <code>Rect</code> attribute of the player on screen as text, updating live. Keep this; it answers most of the questions in the next four lessons.</li>
<li><strong>Checkpoint 4.</strong> Add walls as a list of <code>Rect</code>s, and stop the player passing through them using <code>colliderect</code>. Resolve <strong>one axis at a time</strong> &mdash; move x, fix x, move y, fix y &mdash; as in the beginner track.</li>
<li><strong>Checkpoint 5.</strong> Add coins as Surfaces made in code, and collect them with <code>colliderect</code>. Remove them from the list <strong>backwards</strong>, or use a list comprehension that keeps the ones not collected.</li>
<li><strong>Checkpoint 6.</strong> Draw a score with <code>font.render</code>. Then make it render <em>only when the score changes</em>, and keep the Surface in between.</li>
<li><strong>Checkpoint 7.</strong> Flip the player's sprite when they change direction &mdash; but do the flip <strong>once at startup</strong>, keeping both Surfaces.</li>
<li><strong>Checkpoint 8.</strong> Put <code>clock.get_fps()</code> on screen. Then add a key that rotates every coin every frame, and watch the number fall. Fix it by rotating once into a list of pre-turned Surfaces.</li>
</ul>

<div class="note">
<span class="note-label">If something does not move</span>
<p>Print the float position and the rect position next to each other. If the float
is changing and the rect is not, you have found the trap &mdash; and you will never
be caught by it again.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** `Rect` holds integers. pygame could have used floats. Why might the
designers have chosen integers, and what would change if they had not?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** Your sprites are drawn in code. When does that stop being a good idea?
Describe the game where you would switch to image files, and say what you lose.

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Design `make_sprite(kind, size, colour)` covering every sprite in your
game. What goes in the parameters, what stays hard-coded, and where does the idea
start to fight you?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. `font.render` makes a new Surface every call, and your score
changes every frame — so you cannot cache it. Or can you? Describe a scheme that
renders only when the score actually changes, say what it must track, and say how
you would find out whether it was worth doing.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. A sprite factory (E3), then double every size and check nothing breaks.
2. A nine-slice panel: a UI box of any size from one small Surface.
3. A text cache keyed by the string. Count the hits.
4. Pre-render the background onto one Surface. Time both versions.
5. Load a real image and prove `convert_alpha()` matters, with numbers.
