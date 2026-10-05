# Lesson 4 — Solutions and marking notes

---

## Section A

**A1.** [3] `self.image` and `self.rect`, with exactly those names — two marks — and
`super().__init__()` as the first line of `__init__` — one mark.

**A2.** [2] It removes the sprite from **every group it belongs to**, wherever those groups are — one
mark. It is worth more than it looks because it removes the whole class of bugs around deleting from a
list you are iterating over, and nothing else in the program needs to know the sprite existed — one mark.

**A3.** [3] A group answers a question quickly rather than owning the thing — one mark. Example and
line, two marks: `enemies` answers "what should a bullet check?", asked by
`groupcollide(bullets, enemies, ...)`; or `solid` answers "what can the player not walk through?", asked
by `spritecollide(player, solid, False)`.

Full marks need the consequence: a sprite can be in several groups at once, so adding a new question
later costs one group and one `add`.

**A4.** [2] It calls `sprite.update(dt, wind)` on every sprite in the group — one mark — which requires
every sprite in that group to accept that exact signature — one mark.

**A5.** [3] It returns **that sprite as well**, because a rectangle always overlaps itself — two marks.
So the list is never empty, and any score or damage based on `len(hits)` is wrong by one for every
sprite, every frame — one mark.

**A6.** [2] **No** — one mark. Either use several groups and draw them in sequence, or use
`LayeredUpdates` with `add(sprite, layer=n)` — one mark.

**A7.** [3] Any three, one mark each: every sprite in a group must take the same `update` arguments ·
`image` and `rect` are required even for things with no picture · no guaranteed draw order · the game
logic and the drawing live in the same class, which makes testing without a screen harder.

---

## Section B

**B1.** [3] `40 × 25 = 1,000`. One mark. `400 × 250 = 100,000`. One mark. One more for noticing that
multiplying both by ten multiplied the work by a hundred.

**B2.** [3] **1** — two marks. The sprite collides with itself, because its own rectangle overlaps
itself; none of the other four is touching it — one mark.

**B3.** [4] It prints a single line, **3** — two marks — because `groupcollide` returns one entry per
*bullet*, with a list of everything that bullet hit. The score goes up by **150** — two marks.

Common wrong answer: three lines of `1`. Worth discussing, because it shows the shape of the returned
dictionary.

**B4.** [3] `AttributeError: 'Rock' object has no attribute 'image'` — one mark. The traceback's last
line comes from **inside pygame**, in `sprite.py`, at the `draw` method — one mark — because that is
where `sprite.image` is read. Their own file appears higher up, at the `all_sprites.draw(screen)` call —
one mark.

**B5.** [3] `TypeError: update() takes 1 positional argument but 2 were given` — two marks — raised from
inside pygame's `Group.update`, not from their own code, which is what makes it confusing the first
time — one mark.

---

## Section C

**C1.** [3] `super().__init__()` is missing, so the sprite never got the internal group list that
`Sprite` sets up — two marks. Fix: make it the first line of `__init__` — one mark.

**C2.** [4] Each enemy is being tested against a group **that contains it**, so every enemy collides
with itself — two marks. With 5 enemies that is 5 × 50 = 250 points every frame — one mark. Fixes, one
mark for either: filter the sprite out (`[h for h in hits if h is not enemy]`), or do not test a sprite
against its own group.

**C3.** [3] The two `dokill` flags are positional: the **first** applies to the first group (bullets),
the **second** to the second (enemies) — two marks. Fix: `groupcollide(bullets, enemies, True, True)` —
one mark.

**C4.** [4] `self.rect.x` is an **integer**, and `12 * dt` is about 0.2, which truncates to 0 every
frame — three marks. No error is produced because nothing is wrong, arithmetically — one mark. Fix: keep
a float `self.pos` and assign `self.rect.x = round(self.pos.x)`.

This is the third appearance of lesson 2's trap. If a student recognises it unaided, say so.

**C5.** [3] `all_sprites.remove(coin)` removes it from **one** group only; it is still in `coins`, so
bullets still find it — two marks. Fix: `coin.kill()`, which removes it from every group — one mark.

---

## Section D — marking the build

1. **Checkpoint 2 was really done, with the errors written down.** Three cryptic messages, met on
   purpose in a calm moment rather than at home at 10pm. This is the highest-value ten minutes in the
   lesson.
2. **Checkpoint 4 covered all four `dokill` combinations.** Ask them to describe each; the answer shows
   whether they understand which flag applies to which group.
3. **Checkpoint 5 has two different fixes.** Filtering and not-testing are both valid and have different
   consequences; being able to name both is the point.
4. **Checkpoint 6 tested at 20 px/s.** The float trap, third time.
5. **Checkpoint 8 produced a number** from their own machine. Expect anywhere between 1,500 and 20,000
   depending on the laptop, and treat the variation as the interesting part.

---

## Section E — marking notes

**E1.** A good four for a platformer:

| group | the question | the line |
|---|---|---|
| `all_sprites` | what do I draw? | `all_sprites.draw(screen)` |
| `solid` | what can I not walk through? | `spritecollide(player, solid, False)` |
| `hazards` | what hurts me? | `spritecollideany(player, hazards)` |
| `collectables` | what do I pick up? | `spritecollide(player, collectables, True)` |

Credit also `enemies` (for bullets to check) and `moving_platforms`. Full marks need the *line* for each,
because that is what makes the "question" framing concrete rather than a slogan.

**E2.** Three ways, with costs:

1. **Pass it to everybody**: `all_sprites.update(dt, player.pos)`. Simplest; every cloud now accepts an
   argument it ignores, and adding a fourth argument later touches every class.
2. **Separate groups with separate calls**: `clouds.update(dt)` and `enemies.update(dt, player.pos)`.
   Honest and explicit; the main loop grows a line per group, and a sprite that should be in both is
   awkward.
3. **Give each sprite a reference to the game or the player** at construction. Nothing is passed at all;
   but now every sprite can reach everything, which is the upward-pointing arrow the web track's lesson 1
   warned about, and testing a sprite needs a whole game.

The strongest answers pick 2 and note that it also makes the update *order* explicit, which matters more
than it sounds. Credit anyone who proposes a fourth: an "update context" object holding the few things
sprites need, passed to all of them — which is what larger engines do.

**E3.** The boundary is the question.

- **In `update()`**: the ten-second countdown, the flashing (changing `self.image` between two
  pre-made Surfaces for the last two seconds), and `self.kill()` when the timer runs out.
- **In `image`**: nothing *decided*; just the current picture. Both flash states should be built once in
  `__init__`, not created per frame.
- **Outside the sprite**: what collecting it *means* — the score, the sound, the effect on the player.
  The powerup should not know what a score is.

Full marks for putting the *meaning* of the pickup outside the sprite. That is the same
entities-report-and-the-game-decides split as the web track's capstone, and it is what keeps a sprite
reusable.

**E4.** The answer is a **spatial grid**.

- Divide the world into cells of, say, 64 px. Each frame, put every sprite into the cell its rect falls
  in — a dictionary from `(col, row)` to a list.
- To test a bullet, look only in its own cell and the eight around it.
- With sprites spread over 100 cells, each test looks at roughly 1% of the candidates: 250,000 tests
  becomes a few thousand.

Costs: the dictionary has to be rebuilt every frame (which is itself `O(n)`, but with a tiny constant);
memory for the structure; and real complexity — a sprite larger than a cell spans several, and getting
that wrong produces missed collisions that are maddening to debug.

How to decide: **measure first.** Checkpoint 8 gives them the number at which their frame time doubles.
If the game never approaches it, the grid is a worse program for no benefit. Full marks require that
last point — the honest answer is usually "not yet", and the advanced level builds it when it is
genuinely needed.

---

## If you only mark one thing

Checkpoint 2 — the three broken versions, with the exact error text written down. Those three messages
account for most of the time students lose in this lesson and the next, and meeting them on purpose,
once, is worth more than any amount of careful typing.
