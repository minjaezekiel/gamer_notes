# Lesson 2 — Rects, Images And The Display

> **Games with Python · Intermediate level · Lesson 2 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A game with **pictures** in it — a player you steer, coins to collect and walls you cannot pass
through — and you will have made every one of those pictures **in code**, with no image files at all.

```
   ┌────────────────────────────────────┐
   │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
   │  ▓                  ●           ▓  │
   │  ▓      ☻                  ●    ▓  │   drawn onto Surfaces,
   │  ▓           ▓▓▓▓▓              ▓  │   collided with Rects
   │  ▓   ●                          ▓  │
   │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
   └────────────────────────────────────┘
```

The real subject is two objects that between them are most of pygame: **`Surface`**, which is pixels,
and **`Rect`**, which is a box with opinions.

## Where this fits

- **Back:** [lesson 1](../lesson-01-hello-pygame-ce/notes.md) gave you the loop and `dt`. Everything
  today happens inside it.
- **Forward:** [lesson 4](../lesson-04-sprites-and-groups/notes.md) gets pygame to manage hundreds of
  these for you; [lesson 6](../lesson-06-tilemaps/notes.md) builds a world out of them.
- **Other tracks:** `Rect` is the AABB from the beginner levels with a name and thirty helper methods.
  `blit` is `drawImage` from `webgames` intermediate lesson 4. If you have done that lesson, today is
  mostly new spelling.

---

## The idea, in plain words

### `Rect`: a box that knows things about itself

```python
box = pygame.Rect(100, 80, 40, 60)       # left, top, width, height
```

That is the AABB you have been writing by hand since the beginner level, except that pygame's version
comes with the useful parts already attached:

```python
box.left, box.right, box.top, box.bottom      # the four edges
box.centerx, box.centery, box.center          # the middle
box.topleft, box.midbottom, box.bottomright   # nine named corners and edges
box.width, box.height, box.size
```

And — this is the part worth noticing — **those are not read-only**. Assigning to one *moves the whole
rectangle*:

```python
box.centerx = 320        # the box slides so that its centre is at 320
box.bottom = 400         # the box slides so that its bottom edge is at 400
box.midbottom = (160, 300)
```

That is how you place things in pygame, and it is much better than arithmetic you have to get right
every time. `player.rect.bottom = floor_y` is the whole of "stand on the floor".

Three methods do the work you used to write out:

```python
a.colliderect(b)                 # do these two overlap?  (the AABB test)
rect.collidepoint(mouse_pos)     # is this point inside?
rect.clamp_ip(screen_rect)       # move me so I am inside that, in place
```

`rect.colliderect(other)` **is** the four-condition test from the beginner lesson. You already know
exactly what it does inside, which is the right order to learn it in.

> **The trap, and it catches everybody once: `Rect` holds integers.** Assign `rect.x = 10.7` and it
> becomes `10`. So if you store your position in the rect and move by `SPEED * dt`, small movements are
> silently thrown away and a slow-moving object never moves at all.
>
> **Keep the real position in floats, and copy it into the rect for drawing and collision:**
>
> ```python
> self.x += SPEED * dt           # a float. The truth.
> self.rect.x = round(self.x)    # an int. For drawing and colliding.
> ```
>
> This is the same split as "round when you draw, not when you move" from the web track, arriving for a
> different reason.

### `Surface`: pixels you can draw on

Lesson 1 said the window is a Surface. So is everything else drawable, and you can make your own:

```python
# A Surface with transparency. SRCALPHA is the flag that makes the
# background genuinely see-through rather than black.
sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(sprite, (255, 212, 59), (16, 16), 14)
pygame.draw.circle(sprite, (255, 255, 255), (12, 12), 4)
```

Then **blit** it — copy its pixels onto another Surface:

```python
screen.blit(sprite, (x, y))             # top-left at (x, y)
screen.blit(sprite, sprite_rect)        # or use a Rect's position
screen.blit(sheet, (x, y), source_rect) # or copy only PART of it
```

That third form is the one that matters later: a **source rectangle**, exactly like the spritesheet in
the web track. Lesson 5 is built on it.

### Why this course draws its sprites in code

No `.png` files anywhere. Three reasons, and only the first is about this repository:

1. **A lesson cannot break because a file is missing** or because the Wi-Fi is down.
2. **A sprite made of numbers can be tuned by changing a number.** Want the player bigger? One edit, no
   art program.
3. **It is a real technique.** Pre-drawing something expensive onto a Surface once, instead of drawing
   it from scratch every frame, is one of the most effective optimisations in 2D games. You will use it
   in lesson 4 without being told to.

```python
def make_player_surface(size, body, shirt):
    """Everything about the player's appearance, in one place, as numbers."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surface, shirt, (size * 0.2, size * 0.35, size * 0.6, size * 0.4))
    pygame.draw.circle(surface, body, (size // 2, int(size * 0.25)), int(size * 0.2))
    return surface
```

When you do have real images, the call is one line, and it has a second half people forget:

```python
image = pygame.image.load("hero.png").convert_alpha()
```

`convert_alpha()` converts the image into the display's own pixel format **once**, at load time.
Without it, pygame converts on *every single blit*, and a game with a hundred sprites can run several
times slower for no visible reason at all. Use `.convert()` for images with no transparency and
`.convert_alpha()` for ones with.

### Text, which is a Surface too

```python
font = pygame.font.SysFont(None, 28)         # None = pygame's default font
label = font.render("SCORE 120", True, (231, 236, 243))
screen.blit(label, (14, 14))
```

`render` makes a **new Surface** every time you call it. That matters: rendering text every frame is
one of the most common reasons a simple pygame game is slow. If the text has not changed, keep the
Surface and blit it again.

The `True` is anti-aliasing (smooth edges). Turn it off for pixel-art games.

### Transforms, and why to do them once

```python
bigger = pygame.transform.scale(sprite, (64, 64))
flipped = pygame.transform.flip(sprite, True, False)    # horizontally
turned = pygame.transform.rotate(sprite, 30)            # degrees, anticlockwise
```

All three return a **new Surface**. Doing them every frame means making and throwing away a Surface
sixty times a second, which is the slowest thing in this lesson. Do them once, at startup, and keep the
result:

```python
self.facing_left = pygame.transform.flip(self.facing_right, True, False)
```

And one thing about `rotate` that surprises people: a rotated rectangle needs a bigger box to fit in,
so the Surface it returns is **larger** than the one you gave it, and the picture is no longer in the
same place inside it. The fix is to re-centre using a `Rect`:

```python
turned = pygame.transform.rotate(original, angle)
turned_rect = turned.get_rect(center=original_rect.center)    # re-centre
screen.blit(turned, turned_rect)
```

`get_rect(center=...)` is the idiom: ask a Surface for its rectangle, and position it in the same
breath.

---

## The idea, in pictures

Open [the spritesheet explainer](../../../shared/visualizers/sprite-animation.html).

**What to look for:** ignore the timer for now — lesson 5 is about that. Watch the **source
rectangle** slide along the sheet, and the copy appear on the right. That rectangle is the third
argument to `blit`, and the arithmetic underneath it (`column × width`) is all there is to a
spritesheet.

Then open [AABB collision](../../../shared/visualizers/aabb-collision.html) and drag the two boxes
together. `rect.colliderect(other)` is those four conditions, already written.

---

## The idea, in code

1. `code/01-surfaces-and-blit.py` — make Surfaces in code, blit them, and see what `SRCALPHA` does by
   switching it off.
2. `code/02-rects.py` — every `Rect` attribute on screen at once, live, as you drag a box about. Click
   to see `collidepoint`, and watch `colliderect` light up.
3. `code/03-the-float-trap.py` — two squares moving at 30 px/s, one storing its position in the `Rect`
   and one in a float. One of them does not move at all.
4. `code/04-collect-the-coins.py` — the lesson assembled: a player made in code, walls you cannot pass,
   coins to collect, a score drawn as text, and the frame time on screen.

---

## The maths you just used

**1. Nine named positions on a rectangle.** `topleft`, `midtop`, `topright`, `midleft`, `center`,
`midright`, `bottomleft`, `midbottom`, `bottomright`. Each is worked out from the left, top, width and
height — `midbottom` is `(left + width / 2, top + height)` — and pygame does the arithmetic so that you
stop getting it wrong. Worth writing two of them out by hand once, to see that there is no magic.

**2. Rounding, and where it belongs.** `Rect` truncates towards zero when given a float, which is
*not* the same as rounding: `-3.7` becomes `-3`, a third of a pixel in the wrong direction. Use
`round()` explicitly when you copy a float position into a rect, and keep the float as the truth.

**3. Proportional drawing.** In `make_player_surface` above, every number is a fraction of `size`
rather than a fixed pixel count. That is the difference between a sprite you can resize with one edit
and a sprite you have to redraw. It is the same idea as tuning in design units from the web track.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove `pygame.SRCALPHA` when making a sprite Surface | | |
| Store the position only in `rect.x` and move by `30 * dt` | | |
| Remove `.convert_alpha()` from a loaded image | | |
| Call `font.render(...)` inside the draw loop every frame, with a hundred labels | | |
| `pygame.transform.rotate` every frame instead of once | | |
| Blit a rotated Surface at the original rect's `topleft` | | |
| Use `rect.right = x` instead of `rect.left = x` | | |
| Compare two rects with `==` instead of `colliderect` | | |

The float trap is the important one, and it is the only bug in this lesson that produces **no movement
at all** rather than wrong movement — which makes people check their input code for twenty minutes.

---

## Think like an engineer

1. `Rect` holds integers. pygame could have made it hold floats. Why might the designers have chosen
   integers, and what would change if they had not? (Think about what a rectangle is *for*.)
2. Your sprites are drawn in code. At what point does that stop being a good idea? Describe the game
   where you would switch to image files, and say what you would lose.
3. **Design something.** A `make_sprite(kind, size, colour)` function that can produce every sprite in
   your game. What goes in the parameters, and what has to stay hard-coded? Where does this approach
   start to feel like fighting?
4. **The hard one.** `font.render` makes a new Surface every call. Your score changes every frame, so
   you cannot cache it — or can you? Describe a scheme that renders the score only when it actually
   changes, and say what it has to keep track of. Then say whether it is worth it, and how you would
   find out.

---

## Vocabulary

| Word | What it means |
|---|---|
| **`Surface`** | A rectangle of pixels. The window is one; so is every sprite. |
| **`blit`** | Copy one Surface onto another. |
| **Source rectangle** | The optional third argument to `blit`: which part to copy. |
| **`Rect`** | A box with named edges and corners, and collision methods. Holds **integers**. |
| **`colliderect`** | The AABB overlap test, already written. |
| **`SRCALPHA`** | The flag that gives a new Surface real transparency. |
| **`convert_alpha()`** | Convert a loaded image to the display's format, once. Do not skip it. |
| **`get_rect(center=…)`** | Ask a Surface for its rectangle, positioned where you want it. |
| **Anti-aliasing** | Smooth edges on text. The `True` in `font.render`. |
| **Pre-rendering** | Drawing something once onto a Surface instead of every frame. |

---

## Recap

- **`Rect` is the AABB with helpers.** Assigning to `center`, `bottom` or `midleft` *moves* the box, and
  that is how you place things.
- **`Rect` holds integers.** Keep the real position in a float and `round()` it into the rect, or slow
  movement silently vanishes.
- **Everything drawable is a `Surface`**, including text and the window itself.
- **Make sprites in code** where you can: no missing files, tunable by number, and the same technique as
  pre-rendering.
- `.convert_alpha()` on every loaded image, at load time.
- `transform` and `font.render` make **new Surfaces**. Do them once, not every frame.
- A rotated Surface is bigger than the original — re-centre it with `get_rect(center=…)`.

---

## Stretch goals

1. **A sprite factory.** Question 3, built: one function, every sprite in your game, every number a
   fraction of `size`. Then double `size` and check nothing breaks.
2. **A nine-slice panel.** Draw a UI box of any size from one small Surface by blitting its corners,
   stretching its edges and tiling its middle. This is how every game's dialogue box works.
3. **Cache your text.** Keep a dictionary of rendered Surfaces keyed by the string, and only render a
   string you have not seen. Then count the cache hits.
4. **Pre-render the background.** Draw your walls onto one big Surface at startup and blit it once per
   frame instead of drawing every wall. Time both with `clock.get_fps()` and report real numbers.
5. **Load a real image**, if you have one, and prove `convert_alpha()` matters by timing a hundred blits
   with it and without.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `03-the-float-trap.py`. One square moves, the other does not, and both have the same speed in the code. Let them stare at it. Nobody guesses `Rect` holds integers. |
| 10–25 | **Concept.** `Rect` on the board: the nine positions, and the fact that assigning to one moves the box. Then `Surface` and `blit`, with the source-rect form shown but not dwelt on. |
| 25–40 | **Live-code** `make_player_surface` from nothing, with every number a fraction of `size`. Then double `size` in front of them. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. |
| 120–140 | Break-it-on-purpose. The `SRCALPHA` one and the float trap together. |
| 140–150 | Recap. Lesson 3 makes things move at angles. |

**What usually goes wrong**

1. **The sprite has a black box around it.** No `SRCALPHA`. The commonest visual bug in this lesson, and
   instantly fixed once seen.
2. **Slow movement does nothing at all.** The float trap. They will suspect their keyboard handling,
   their `dt`, and their eyesight before they suspect the rectangle.
3. **`TypeError: argument 1 must be pygame.Surface, not tuple`** — they passed a colour where a Surface
   was expected, usually by mixing up `blit` and `draw.rect`.
4. **Text does not appear.** They forgot `pygame.font.init()` — which `pygame.init()` does for them, so
   this only happens if they skipped `pygame.init()` — or they rendered the text and never blitted it.
5. **A rotated sprite drifts across the screen** as it turns. The Surface grew; they are still using the
   old rect. `get_rect(center=…)` fixes it, and the explanation needs a drawing.
6. **The game is mysteriously slow** with twenty sprites. Rotating or scaling every frame, or rendering
   text every frame. This is a good moment to introduce `clock.get_fps()` as evidence rather than
   opinion.
7. **`rect.center = x`** rather than `rect.centerx = x`. The error message is unhelpful; the fix is one
   character.

**If you are running short on time** — cut `transform` entirely and keep it for lesson 5 where flipping
is needed. Do **not** cut the float trap: everything in this level moves by `SPEED * dt`, and a student
who has not met this will meet it alone, in lesson 6, with a tilemap on top.

**For the student who finishes at minute 90** — stretch goal 1 (a sprite factory) is the most useful,
because they will use it for the rest of the level. Stretch goal 4 (pre-render the background) is the
one that produces a number they can be proud of.

**The point to land at the end:** two objects — `Surface` and `Rect` — and almost everything in pygame
is one of them. The library is much smaller than it looks, and the bug that cost them twenty minutes was
not in their code; it was in an assumption about what a rectangle is made of.
