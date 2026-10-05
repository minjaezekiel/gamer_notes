# Lesson 2 — Solutions and marking notes

---

## Section A

**A1.** [3] Any five of `left right top bottom centerx centery center topleft midtop topright midleft
midright bottomleft midbottom bottomright width height size` — two marks. Assigning to one **moves the
whole rectangle** so that the named part ends up where you put it — one mark. That last part is the
whole point and is what students miss.

**A2.** [3] **Integers** — one mark. The symptom: a position stored only in the rect loses every
fractional movement, so anything moving slower than about one pixel per frame **does not move at all** —
two marks. Credit the detail that it truncates rather than rounds.

**A3.** [2] A rectangle of pixels you can draw on — one mark. Three examples, one mark: the window from
`set_mode`, a sprite you made, a loaded image, a spritesheet, and the result of `font.render`.

**A4.** [2] It gives the new Surface a real alpha channel, so untouched pixels are transparent — one
mark. Without it, the Surface is filled with opaque black and your sprite arrives in a black box — one
mark.

**A5.** [3] It converts the image into the display's own pixel format once, at load time — one mark.
Without it pygame converts on **every blit** — one mark — so the cost appears later, as a game that is
mysteriously several times slower with no obvious reason, rather than as an error — one mark.

**A6.** [2] Because it creates a **new Surface** every call — one mark — so doing it per frame means
making and discarding sixty Surfaces a second per sprite, which is the slowest thing in the lesson — one
mark.

**A7.** [3] A rotated rectangle needs a larger box to fit inside, so the returned Surface is bigger and
the picture sits in a different place within it — two marks. Fix:
`rect = turned.get_rect(center=old_rect.center)` and blit with that — one mark.

---

## Section B

**B1.** [3] `right = 140`, `bottom = 110`, `center = (120, 80)`, `midbottom = (120, 110)`. Three marks,
roughly one per two answers.

**B2.** [3] `left = 180`, `top = 170`. Two marks. Because the box moved so that its centre is at
(200, 200), and the centre is `(left + 20, top + 30)` — one mark.

**B3.** [4] Version A: `30 × (1/60) = 0.5` px per frame, truncated to **0**, so it never moves at all —
two marks. Version B: the float accumulates 0.5 per frame, and the rect jumps one pixel every other
frame, travelling the full 30 px in a second — two marks.

**B4.** [3] `r.x` holds **−3** — two marks. `round(-3.7)` would give **−4** — one mark. So truncation
moves the box in the *positive* direction for negative numbers, which is a drift rather than a jitter.

**B5.** [3] About 45×45 — `32 × √2 ≈ 45`. Two marks. Because the corners of the original square now
stick out, and the new Surface must be large enough to contain the whole turned square — one mark.

---

## Section C

**C1.** [3] `pygame.SRCALPHA` is missing from the `Surface` call — two marks. Fix:
`pygame.Surface((32, 32), pygame.SRCALPHA)` — one mark.

**C2.** [4] `SPEED * dt` is about `40 / 60 = 0.67` px, and the position lives in `rect.x`, which is an
integer — so each frame adds 0.67, truncates to 0, and the player never moves. Three marks. Fix: keep a
float and round it into the rect — one mark.

The reason this is worth four marks: the `print` firing is what makes it so hard. Everything the author
checked was working.

**C3.** [3] `blit` takes a **Surface**, and a colour tuple has been passed instead — two marks. They
probably wanted `pygame.draw.rect(screen, (255, 0, 0), (100, 100, 40, 40))` — one mark.

**C4.** [4] Two causes, two marks each. (a) `transform.rotate` is called per enemy per frame, creating
thirty Surfaces every frame. (b) `font.render` is called per enemy per frame, creating thirty more.

Fixes: pre-rotate into a list of angles at startup, and cache the hp labels in a dictionary keyed by the
number. Credit anyone who notes that the fix for both is the same idea — do it once, keep the result.

**C5.** [3] The second line undoes the first: it clamps `x` (the **left** edge) to `WIDTH`, which allows
the box to sit entirely off-screen, and because `x` is assigned after `right`, it wins. Two marks. Fix:
delete the second line, or use `player.rect.clamp_ip(screen_rect)` which handles all four edges — one
mark.

---

## Section D — marking the build

1. **Every number in `make_sprite` is a fraction of `size`** (checkpoint 1). Test it: double the size in
   front of them. If the proportions break, the numbers were hard-coded.
2. **A float position AND a rect, with `round()`** (checkpoint 2), tested at 20 px/s. This is the one
   objective test in the lesson.
3. **The rect readout is on screen** (checkpoint 3). It makes checkpoints 4 and 5 straightforward and
   makes lesson 6 much easier.
4. **Collision is resolved one axis at a time** (checkpoint 4). Walk diagonally into a corner; if they
   stop dead instead of sliding, they have resolved both at once — and that is the beginner-level lesson
   returning, so point at it rather than fixing it.
5. **Coins are removed safely** (checkpoint 5). A forward `for` loop with `.remove()` skips items;
   accept backwards iteration or a rebuilt list.
6. **Checkpoint 8 produced a number.** Watching the frame rate fall and then recover is the most
   persuasive thing in this lesson.

---

## Section E — marking notes

**E1.** Good answers reach at least one of:

- **A rectangle is ultimately a region of pixels**, and pixels are whole. A rect with fractional edges
  does not describe a set of pixels without a rounding rule, and pygame would have had to choose one for
  you.
- **Collision answers must be stable.** With floats, two rects that touch exactly may or may not collide
  depending on invisible decimals.
- **Speed and simplicity**: integer comparisons, no epsilon questions.

What would change: every sprite would need a rounding decision at draw time anyway, so the trap would
move rather than disappear — and sub-pixel positions make pixel art blurry, as the web track found.
Credit anyone who notices that modern engines *do* use floats and solve it by rounding at draw time,
which is exactly what we do by hand.

**E2.** It stops being a good idea when the *art* becomes the thing you are iterating on rather than the
code. Concretely: when a sprite needs more than about twenty drawing calls; when somebody who is not a
programmer should be able to change it; when you want shading, texture or a character with a face.

What you lose by switching: the game can break because a file is missing or a path is wrong; sizes stop
being tunable by one number; you need an art pipeline and probably an artist.

The strongest answers note that the two can coexist — placeholder sprites in code during development,
real images later, with the same `make_sprite` interface. That is what studios actually do.

**E3.** A reasonable design: `kind` picks a drawing function from a dictionary; `size` scales everything;
`colour` recolours the main body. Hard-coded: the *shape* of each kind, and the relative proportions.

Where it fights: anything that needs more than one colour, anything asymmetric that must also be
flipped, and anything where the shape itself should vary (a tree, a cloud). At that point the parameters
multiply and the function becomes a small language — which is the moment to switch to data (a list of
shapes per kind) rather than more arguments. Full credit for spotting that transition, which is the same
one lesson 5 of the web track identified for tile tables.

**E4.** The scheme:

```python
if score != last_rendered_score:
    score_surface = font.render("SCORE %d" % score, True, INK)
    last_rendered_score = score
screen.blit(score_surface, (14, 14))
```

What it must track: the last value rendered, and the Surface. Two variables.

Does the score really change every frame? Usually **no** — it changes when something is collected, which
is a handful of times a second at most. The premise of the question is wrong, and spotting that is the
best answer available. Even a timer displayed to one decimal place only changes ten times a second, not
sixty.

How to find out whether it is worth it: count the renders per second with a counter, and measure the
frame time with and without. Full marks need a measurement rather than an opinion — and the honest
conclusion for one label is "it does not matter"; for thirty labels, it does. Credit anyone who says the
cache is worth it mainly because it makes the cost *predictable*.

---

## If you only mark one thing

Checkpoint 2, tested at 20 px/s. A student who has the float-and-rect split working will never lose an
afternoon to the integer trap, and every remaining lesson in this level moves things by `SPEED * dt`.
