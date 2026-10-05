# Lesson 4 — Sprites And Groups

> **Games with Python · Intermediate level · Lesson 4 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A small shooter with **hundreds of things in it** — bullets, enemies, pickups, explosions — where
updating them all is one line and drawing them all is one line, and where "which bullets hit which
enemies" is also one line.

```
   all_sprites.update(dt)          ← every single thing moves
   all_sprites.draw(screen)        ← every single thing is drawn
   hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
```

You will also find out where pygame's sprite system stops helping, which is a more useful thing to
know than how to use it.

## Where this fits

- **Back:** [lesson 2](../lesson-02-rects-images-and-the-display/notes.md) gave you `Surface` and
  `Rect` — which turn out to be exactly what a `Sprite` is made of.
- **Forward:** everything from here uses groups. Lesson 10 *(not yet written)*
  spawns waves into them and lesson 12 *(not yet written)* is built on them.
- **Other tracks:** the web and C++ tracks keep plain arrays of entities and write the loops by hand.
  This is the first time this course uses a library's own system rather than building one — so the
  interesting question today is *what you gave up in exchange*.

---

## The idea, in plain words

### A Sprite is an image and a rectangle. That is the whole contract.

```python
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, velocity):
        super().__init__()                 # DO NOT forget this line
        self.image = make_bullet_surface() # required, and must be called `image`
        self.rect = self.image.get_rect(center=pos)   # required, called `rect`
        self.pos = Vector2(pos)            # floats: the real position
        self.velocity = velocity

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos        # ints, for drawing and colliding
        if not screen_rect.colliderect(self.rect):
            self.kill()                    # remove me from every group I am in
```

Two attributes, with those exact names: **`self.image`** and **`self.rect`**. A group's `draw()` does
`surface.blit(sprite.image, sprite.rect)` and nothing else, so if either is missing or misspelled you
get an `AttributeError` from inside pygame, which is confusing the first time.

`super().__init__()` is the line people leave out. Without it the sprite has no internal list of the
groups it belongs to, and `add`, `kill` and `groups()` all fail.

### `kill()` is the good part

`self.kill()` removes the sprite from **every group it is in**, wherever those groups are. No searching
through lists, no removing while iterating, no index bookkeeping. A bullet that leaves the screen can
delete itself, and nothing else in your program has to know.

That one method is most of the reason to use this system at all.

### A Group is a set, and groups are **queries**

```python
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

enemy = Enemy(...)
all_sprites.add(enemy)
enemies.add(enemy)             # the SAME sprite, in two groups
```

A sprite can be in as many groups as you like, and that is the idea worth taking away: a group is not a
container you put a thing *into*, it is a **question you can ask quickly**. `all_sprites` means "draw
me"; `enemies` means "a bullet should check me"; `solid` means "the player cannot walk through me".

Adding a new query later is one group and one `add()`, and nothing that already works has to change.

Then:

```python
all_sprites.update(dt)          # calls update(dt) on every sprite
all_sprites.draw(screen)        # blits every sprite's image at its rect
```

`update()` passes on whatever arguments you give it, so `all_sprites.update(dt, wind)` calls
`sprite.update(dt, wind)`. Every sprite in the group must accept that signature — which is a real
constraint, and the first place this system starts to pinch.

### Collision, four ways

```python
# 1. one sprite against a group. The third argument is "kill the ones that hit".
hits = pygame.sprite.spritecollide(player, coins, True)
score += len(hits) * 10

# 2. group against group. Returns a dict: {bullet: [enemies it hit]}
hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
for bullet, hit_enemies in hits.items():
    score += len(hit_enemies) * 50

# 3. any collision at all?
if pygame.sprite.spritecollideany(player, hazards):
    lose_a_life()

# 4. a different test, instead of rectangles
hits = pygame.sprite.spritecollide(player, rocks, False,
                                   pygame.sprite.collide_circle)
```

`collide_circle` needs each sprite to have a **`self.radius`**; `collide_mask` needs a `self.mask`
(built with `pygame.mask.from_surface(self.image)`) and is pixel-perfect and much slower. Rectangles are
right nearly always.

> **The trap, and it is a good one.** If the sprite you are testing is **in the group you are testing
> against**, it collides with itself — every time, because a rectangle always overlaps itself. So
> `spritecollide(enemy, enemies, False)` always returns at least that enemy. Keep the sprite out of the
> group, or filter it out afterwards.

### Draw order

`Group` does **not** promise an order. If you need the player drawn in front of the scenery, either use
several groups and draw them in sequence, or use `LayeredUpdates`:

```python
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(background_thing, layer=0)
all_sprites.add(player, layer=2)
all_sprites.add(ui_thing, layer=5)
```

The simple answer — a background group, a main group and a UI group, drawn in that order — is usually
better, because it makes the layering visible in the draw code rather than hidden in an argument.

### Where this system stops helping

This is the part most tutorials leave out, and it is the reason to pay attention today.

1. **Every sprite in a group must accept the same `update()` arguments.** The moment one enemy needs the
   player's position and another does not, you are passing things that most sprites ignore — or keeping
   a reference to the game inside every sprite, which is the upward-pointing arrow that lesson 1 of the
   web track warned about.
2. **`image` and `rect` are required even when they make no sense.** A trigger zone with no picture
   still needs an `image`.
3. **The order is not yours** unless you ask for it.
4. **Logic and drawing end up in the same class.** `update()` and `image` live together, so a sprite
   knows how it looks, which makes testing the rules without a screen harder. The web track's lesson 1
   and this course's advanced level both go the other way.

None of these makes the system wrong. They are the price, and the useful habit is to **know what you
paid**. For a game of this size it is a good trade; `kill()` alone is worth it.

### Is it fast?

`Group` is a dictionary underneath, so adding, removing and iterating are all quick. `spritecollide` is
a plain loop over the group — there is no clever spatial structure — so bullets against enemies is
`len(bullets) × len(enemies)` rectangle tests.

With 50 bullets and 50 enemies that is 2,500 tests a frame, which is nothing. With 500 and 500 it is
250,000, which is not. `code/03-a-hundred-things.py` measures it on your machine at sizes from 100 to
5,000 and prints real milliseconds, so you can find out where *your* laptop stops coping rather than
guessing. The advanced level fixes it properly with a spatial grid.

---

## The idea, in pictures

Open [AABB collision](../../../shared/visualizers/aabb-collision.html).

**What to look for:** `spritecollide` and `groupcollide` are this test, run in a loop. Drag the two
boxes until exactly one of the four conditions is red — that is the near-miss your game will do
thousands of times a second. Nothing clever is happening inside pygame; it is doing what you can see.

Then open [the sprite animation explainer](../../../shared/visualizers/sprite-animation.html) and notice
the source rectangle — lesson 5 adds that to the `image` attribute you are setting today.

---

## The idea, in code

1. `code/01-your-first-sprite.py` — one `Sprite` subclass and one `Group`, with the three mistakes
   (missing `super().__init__()`, misspelled `image`, misspelled `rect`) each on a key so you can read
   the error each one produces.
2. `code/02-groups-are-queries.py` — one sprite in four groups, with the membership drawn on screen.
   `spritecollide`, `groupcollide` and the self-collision trap, on switches.
3. `code/03-a-hundred-things.py` — up to 5,000 sprites, timing update, draw and collision separately,
   against a plain list doing the same work.
4. `code/04-shooter.py` — the lesson assembled: a player, waves of enemies, bullets, pickups,
   explosions, and the whole update-draw-collide in six lines.

---

## The maths you just used

**1. Pairs.** Testing every bullet against every enemy is `len(a) × len(b)` tests. That product is the
whole performance story of this lesson: doubling both quadruples the work. The formal name is quadratic
growth, usually written **O(n²)**, and recognising it is more useful than the notation.

**2. Why a grid helps.** If you divided the screen into 10 × 10 cells and only tested things in the same
cell, each test would look at roughly `n / 100` candidates instead of `n`. That is the advanced level's
spatial hash, and you now have the arithmetic that motivates it.

**3. Squared radii, again.** `collide_circle` compares the sum of the radii against the distance — and
pygame does the square root for you. Writing it yourself, you would compare squared values and skip the
root, as you did in lesson 3.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove `super().__init__()` from a Sprite | | |
| Rename `self.image` to `self.picture` | | |
| Rename `self.rect` to `self.box` | | |
| Call `spritecollide(enemy, enemies, False)` and count the results | | |
| Use `remove()` from a list you are looping over, instead of `kill()` | | |
| Give one sprite an `update(self)` with no `dt` and call `group.update(dt)` | | |
| Set `dokill=True` on the wrong side of `groupcollide` | | |
| Put the player in `all_sprites` and `enemies` by mistake | | |
| Run `03-a-hundred-things.py` at 5,000 | | |

The `update(self)` one produces `TypeError: update() takes 1 positional argument but 2 were given`, from
a line inside pygame rather than in your file — which is worth seeing once so that you recognise it.

---

## Think like an engineer

1. A group is "a question you can ask quickly". List four groups a platformer would want, and for each
   one say which line of code asks that question.
2. Every sprite in a group must accept the same `update()` arguments. Your enemies need the player's
   position; your clouds do not. Name three ways to deal with that, and say what each costs.
3. **Design something.** A `Powerup` sprite that disappears after ten seconds, flashes for the last two,
   and is collected on touch. Which parts belong in `update()`, which in `image`, and which in the game
   code outside the sprite? Where exactly is the boundary?
4. **The hard one.** `spritecollide` tests every member of the group. With 500 bullets and 500 enemies
   that is 250,000 tests a frame. Describe a scheme that does far fewer — without changing what any
   sprite does — and say what it costs in memory and in complexity. Then say how you would decide
   whether to build it.

---

## Vocabulary

| Word | What it means |
|---|---|
| **`Sprite`** | A class with `self.image` and `self.rect`. Both names are required. |
| **`Group`** | A set of sprites. Can `update`, `draw` and be collided against. |
| **`super().__init__()`** | Sets up the sprite's group bookkeeping. Never leave it out. |
| **`kill()`** | Remove this sprite from every group it is in. |
| **`spritecollide`** | One sprite against a group. Returns a list. |
| **`groupcollide`** | Group against group. Returns a dict of `{sprite: [hits]}`. |
| **`dokill`** | The flag that removes whatever collided. |
| **`collide_circle`** | A circle test. Needs `self.radius` on both sprites. |
| **`collide_mask`** | Pixel-perfect. Needs `self.mask`. Slow. |
| **`LayeredUpdates`** | A group that draws in a layer order you choose. |
| **Quadratic (O(n²))** | Work that grows with the *product* of two sizes. |

---

## Recap

- A `Sprite` needs **`self.image`** and **`self.rect`**, with those names, and
  **`super().__init__()`**.
- **`kill()`** removes a sprite from every group at once. That alone justifies the system.
- A sprite can be in **many groups**, and a group is best thought of as **a query**, not a container.
- `group.update(*args)` passes its arguments to every sprite — so they must all accept the same ones.
- `spritecollide` returns the sprite itself if it is **in** the group you tested against.
- Collision is a **plain loop**: `len(a) × len(b)` tests. Fine at 50, not fine at 500.
- Know what you gave up: shared `update` signatures, required `image`, no order, and logic living next
  to drawing.

---

## Stretch goals

1. **Custom collide functions.** Write your own and pass it to `spritecollide` — for example, one that
   only counts a hit if the bullet is also moving *towards* the enemy.
2. **`collide_mask`.** Add `self.mask = pygame.mask.from_surface(self.image)` and compare the feel of
   pixel-perfect collision with rectangles. Then measure the cost.
3. **A layered draw** without `LayeredUpdates`: three groups, drawn in order. Decide which you prefer and
   why.
4. **A sprite pool.** Instead of `kill()`-ing bullets, move them to an `inactive` group and reuse them.
   Measure whether it helps at 2,000 bullets — and be prepared for the answer to be "no".
5. **Deliberate self-collision.** Make enemies avoid each other using `spritecollide(enemy, enemies)` —
   and deal with the fact that each one finds itself first.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `04-shooter.py`, then show the six lines of the main loop on the projector. Hundreds of objects, six lines. Ask what those lines are hiding. |
| 10–25 | **Concept.** The `Sprite` contract on the board — `image`, `rect`, `super().__init__()` — then groups as *queries* rather than containers. That reframing is the lesson. |
| 25–40 | **Live-code** one `Bullet` class and one group, and `kill()` it off the edge of the screen. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. |
| 120–140 | Break-it-on-purpose. The three missing-attribute errors first, then the self-collision one. |
| 140–150 | Recap. Lesson 5 makes the `image` change over time. |

**What usually goes wrong**

1. **`AttributeError: 'Bullet' object has no attribute 'rect'`** from inside pygame's own code. The
   traceback points at `group.py`, not at their file, which is confusing the first time. Teach them to
   read the *bottom* of a traceback for the error and the *top* for their own code.
2. **Missing `super().__init__()`.** The error (`AttributeError: ... has no attribute '_Sprite__g'`) is
   genuinely cryptic. Put it on the board before they meet it.
3. **`TypeError: update() takes 1 positional argument but 2 were given.`** One sprite's `update` does not
   take `dt`.
4. **Everything collides with itself**, so the score rockets. The sprite is in the group being tested.
5. **Sprites disappear when they should not.** `dokill` on the wrong side of `groupcollide`. Remind them
   the first flag kills from the first group.
6. **The player is drawn behind the enemies**, intermittently. Group order is not guaranteed.
7. **A sprite keeps its position in `self.rect` only**, so slow movement does nothing. Lesson 2's trap,
   third appearance. It will not be the last.

**If you are running short on time** — cut `LayeredUpdates` and the custom collide functions. Do **not**
cut the "where this stops helping" discussion: a student who can only use a library, and cannot say what
it costs, has learned half the lesson.

**For the student who finishes at minute 90** — stretch goal 5 (enemies avoiding each other) is the best,
because the self-collision trap becomes a problem they have to solve rather than a fact they were told.

**The point to land at the end:** six lines did the work of about eighty. That is what a library is for,
and today was the first time this course used somebody else's system instead of building one. The
question to leave them with is not "is it good?" but "what did we hand over, and would we want it back?"
