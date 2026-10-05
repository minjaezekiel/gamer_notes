# Lesson 4 — Sprites And Groups

## Cheat sheet

### The contract

```python
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()          # NEVER leave this out
        self.image = make_surface() # this exact name
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)     # floats: the truth
        self.vel = vel

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if off_screen:
            self.kill()             # leaves EVERY group
```

### Groups are queries, not containers

```python
all_sprites.add(e)   # "draw me"
enemies.add(e)       # "bullets should check me"
solid.add(e)         # "the player cannot pass me"
```

One sprite, many groups. A new query is one group and one `add`.

```python
all_sprites.update(dt)     # calls update(dt) on each
all_sprites.draw(screen)   # blits image at rect
```

Every sprite in a group must accept the **same** update arguments.

### Collision

```python
spritecollide(player, coins, True)        # list; True = kill them
groupcollide(bullets, enemies, True, True) # {bullet: [enemies]}
spritecollideany(player, hazards)          # bool-ish, fast
spritecollide(p, rocks, False,
              pygame.sprite.collide_circle) # needs .radius
```

⚠ **A sprite in the group collides with itself**, always. Keep it out, or filter.

### Draw order

`Group` promises **none**. Use several groups drawn in order, or
`LayeredUpdates` with `add(s, layer=n)`.

### Cost

`spritecollide` is a plain loop: `len(a) × len(b)` tests.
50 × 50 = 2,500 — fine. 500 × 500 = 250,000 — not.

### What you gave up

same update signature · `image` required always · no order · logic and drawing
in one class

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What two attributes must a Sprite have, and what third line must <code>__init__</code> contain?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does <code>kill()</code> do, and why is it worth more than it looks?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Explain &ldquo;a group is a question, not a container&rdquo;, with an example of a group and the line that asks it.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> What does <code>group.update(dt, wind)</code> do, and what does that require of every sprite in the group?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> What does <code>spritecollide</code> return if the sprite you pass is a member of the group you pass? Why?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Does a <code>Group</code> guarantee a draw order? What are the two ways to get one?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A7.</span> Name three things you gave up by using pygame's sprite system rather than your own list.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> There are 40 bullets and 25 enemies. How many rectangle tests does one <code>groupcollide</code> do? Now with 400 and 250?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>enemies</code> contains 5 enemies, none of them overlapping. What does <code>len(pygame.sprite.spritecollide(enemies.sprites()[0], enemies, False))</code> return, and why?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> A bullet hits three enemies on the same frame. What does this print, and what is the score?

```python
hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
for bullet, hit in hits.items():
    print(len(hit))
    score += len(hit) * 50
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> What error does this produce, and from which file does the traceback's last line come?

```python
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.picture = make_rock()
        self.rect = self.picture.get_rect()
# ...
all_sprites.draw(screen)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> <code>group.update(dt)</code> is called, and one sprite's method is <code>def update(self):</code>. What happens?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> <code>AttributeError: 'Coin' object has no attribute '_Sprite__g'</code>.

```python
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.image = make_coin()
        self.rect = self.image.get_rect(center=pos)
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The score goes up by 50 every single frame, even when nothing is near anything.

```python
for enemy in enemies:
    hits = pygame.sprite.spritecollide(enemy, enemies, False)
    score += len(hits) * 50
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> Bullets vanish on contact but enemies never do.

```python
pygame.sprite.groupcollide(bullets, enemies, True, False)
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The enemies move at the right speed. The clouds do not move at all, and there is no error.

```python
class Cloud(pygame.sprite.Sprite):
    def update(self, dt):
        self.rect.x += 12 * dt
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> Collecting a coin removes it from the screen, but bullets still collide with it afterwards.

```python
for coin in pygame.sprite.spritecollide(player, coins, False):
    all_sprites.remove(coin)
    score += 10
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write one <code>Sprite</code> subclass and one <code>Group</code>. Make it move, and <code>kill()</code> itself when it leaves the screen. Draw the group's length on screen and watch it fall.</li>
<li><strong>Checkpoint 2.</strong> Deliberately break it three ways &mdash; no <code>super().__init__()</code>, <code>self.picture</code>, <code>self.box</code> &mdash; and write down each error <em>exactly</em>. You will see all three again.</li>
<li><strong>Checkpoint 3.</strong> Put one sprite in three groups and draw its membership on screen. Then remove it from one group and check the other two still have it.</li>
<li><strong>Checkpoint 4.</strong> Add bullets and enemies, and use <code>groupcollide</code>. Try all four combinations of the two <code>dokill</code> flags and describe what each one does.</li>
<li><strong>Checkpoint 5.</strong> Reproduce the self-collision trap on purpose, count the results, and then fix it two different ways.</li>
<li><strong>Checkpoint 6.</strong> Give every sprite a float <code>pos</code> and copy it into <code>rect.center</code>. Then set an enemy's speed to 20 px/s and confirm it still moves.</li>
<li><strong>Checkpoint 7.</strong> Draw in three passes &mdash; background group, main group, UI group &mdash; and confirm the player is always in front.</li>
<li><strong>Checkpoint 8.</strong> Put the sprite count and the frame time on screen, then spawn sprites until the frame time doubles. Write down the number. That is your machine's limit, measured.</li>
</ul>

<div class="note">
<span class="note-label">Reading a pygame traceback</span>
<p>The <strong>last</strong> line says what went wrong; the lines above it say where.
When the error comes from inside <code>sprite.py</code>, scroll <em>up</em> to the
last line that mentions <em>your</em> file &mdash; that is the call that caused it.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** List four groups a platformer would want, and for each one the line of code
that asks its question.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Your enemies need the player's position in `update()`; your clouds do not.
Give three ways to deal with that, and say what each costs.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design a `Powerup` that vanishes after ten seconds, flashes for the last
two, and is collected on touch. What belongs in `update()`, what in `image`, and
what in the game code outside the sprite?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. 500 bullets against 500 enemies is 250,000 tests a frame.
Describe a scheme that does far fewer *without changing what any sprite does*. What
does it cost in memory and complexity, and how would you decide whether to build it?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. A custom collide function passed to `spritecollide`.
2. `collide_mask` for pixel-perfect collision — then measure what it costs.
3. Three groups drawn in order, instead of `LayeredUpdates`. Pick a side.
4. A sprite pool instead of `kill()`. Measure at 2,000 bullets; be ready for "no
   difference".
5. Enemies that avoid each other — and deal with each one finding itself first.
