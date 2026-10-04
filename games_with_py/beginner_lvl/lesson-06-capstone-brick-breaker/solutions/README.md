# Lesson 6 — Solutions and marking notes

There is a runnable test here too: `python3 test_brick_breaker_logic.py` checks level building,
the AABB test, brick toughness and scoring, side detection, paddle steering, and that a damaged save
file does not crash the game. Run it before teaching from the reference implementation.

---

## Section A

**A1.** [3] `self` is **the particular instance the method was called on**. Writing `brick.colour()`
makes Python call `Brick.colour(brick)` — the instance is passed in as the first argument, and that
argument is conventionally named `self`. Two marks for the explanation, one for making clear it is
not a keyword or anything magical.

**A2.** [3] A class is better when a thing has **both data and behaviour**, and when there are
**many** of them — so the behaviour lives next to the data and the type has a name. Two marks.

One mark for a sensible dictionary: `keys` (an arbitrary, changing set of key names), a config of
settings, a lookup table of colours, JSON loaded from a file. Anything that is a bag of values with
no behaviour of its own.

**A3.** [2] Because the outer list holds **rows** — each inner list is one row's worth of cells — so
the first index chooses which row, which is y.

**A4.** [3] Compare the overlap on each axis; the **smaller** one is the side it came in through, because
a ball that has just poked in along its direction of travel barely overlaps on that axis. Two marks.

One mark for the failure: a ball clipping a brick's *side* that flips `speed_y` is still travelling
sideways, so it immediately hits the next brick along, flips again, and **carves straight through the
whole row**.

**A5.** [3] One mark each, any three:

| Cause | What the game should do |
|---|---|
| The file does not exist yet (first run) | start at 0, silently |
| The file is damaged or hand-edited | start at 0, silently |
| The disk is read-only or full | carry on without saving |
| Someone deleted it mid-game | start at 0 next time |

The point being tested is that **every one of these should be silent**. Crashing because a high score
could not be loaded is worse than having no high score.

---

## Section B

**B1.** [3] Count the non-zero cells: row 0 has 2, row 1 has 2, row 2 has 4. **Eight bricks.**
Shape: a chequerboard of two rows (with the second row's bricks being tough/orange) over a solid row.
Two marks for the number, one for the shape.

**B2.** [4] `TypeError: Brick.colour() takes 0 positional arguments but 1 was given.`

What it tells you: Python passed **one** argument — the instance — even though the method declared
none. That is exactly what `self` is: the instance, handed in automatically as the first argument.
The fix is `def colour(self):`.

Two marks for the error, two for the explanation. This error message is genuinely one of Python's
better ones, and reading it carefully with the class is worth more than defining `self` abstractly.

**B3.** [4] Clipping the **left edge** while travelling right means the ball has barely penetrated
horizontally and overlaps a lot vertically. So **`overlap_x` is smaller**, and **`speed_x`** should
flip. Two marks.

If the code always flips `speed_y`, the ball keeps its rightward motion, is immediately inside the
next brick along, destroys that one too, flips vertically again, and so on. The player sees the ball
**carve sideways through the entire row**, zig-zagging up and down as it goes. Two marks.

**B4.** [3] `json.loads("hello")` raises a `JSONDecodeError`, which the bare `except Exception` in
`load_high_score` catches, so the function returns **0**. The game starts normally with a high score
of zero, and nothing is reported to the player.

That is the correct behaviour and it is exactly what the `try` is there for.

---

## Section C

**C1.** [4] Two separate mistakes:

1. Inside `__init__`, `x = x` assigns the parameter to itself — a local variable, thrown away when
   the method ends. It should be `self.x = x`.
2. `x = 0` and `y = 0` at class level are **class attributes**, shared by every instance. So every
   brick reads the same `0`, which is why they all report the same position.

Two marks each. The second part is subtle and worth explaining: class-level assignments belong to the
class, not to each instance.

**C2.** [3] The `break` after handling a brick hit. Without it, one frame can process several
overlapping bricks: all of them are destroyed, and the velocity is flipped once per brick. Flipping
twice returns it to the original direction, so the ball sails on as though nothing happened.

**C3.** [4] The **canvas's** record was cleaned (`canvas.delete`) but **ours** was not — the brick is
still in the `bricks` list with `alive` still `True`, so the collision test keeps finding it. (Or, if
written the other way round: `alive` was set but `canvas.delete` was not called, giving the opposite
symptom.)

Two marks for identifying the split, two for a fix: set `self.alive = False` **and** call
`canvas.delete(self.item)` together, ideally in one `hit()` method so no caller can do one without
the other.

The general principle is worth stating: **when two records must stay in step, give exactly one piece
of code the job of changing them.**

---

## Section D — marking the capstone

Mark on four things, not feature count:

1. Does it run without errors?
2. Is the level data separate from the game logic?
3. Can they explain any method you point at?
4. **Did they change something to make it theirs?**

Checkpoint 4 is a full pass; 5 and 6 are distinction.

**Say point 4 out loud before they start**, or they will aim for an exact copy of the example.

**Common structural problems while circulating:**

- `self.x = x` written as `x = x`. The symptom is `AttributeError` later, far from the cause.
- `layout[column][row]`. Mirrored level or an `IndexError` on a non-square one.
- Brick positions hard-coded rather than computed from the grid. Ask how they would add a fourth
  level.
- `canvas.delete` and `alive` handled in different places, so they drift apart.

---

## Section E — marking notes, not answers

**E1.** Mark on reasoning. The honest position is that for a single-player offline game, **"nothing"
is a perfectly good answer** — a player cheating their own high score harms nobody, and effort spent
preventing it is effort not spent on the game.

It starts to matter when the score is **shared**: an online leaderboard, a class competition, a
tournament. Then the usual answers are: keep the authoritative score on a server, sign it with a
secret, or accept that a determined cheat will always win and design the leaderboard so it does not
matter much.

Students sometimes propose encrypting or obfuscating the file. Worth pointing out gently that this
only slows someone down, because the game itself has to be able to read it — the key is sitting right
there in the code. That realisation is a genuinely useful first security lesson.

**E2.** For most students' code the answer will be "a few numbers": `BRICK_W` would need shrinking,
and `MARGIN` recalculating, or the bricks run off the screen.

The good follow-up is to ask whether the brick width should be **computed** from the level width:

```python
columns = len(layout[0])
BRICK_W = (WIDTH - 2 * MARGIN - (columns - 1) * GAP) / columns
```

A student who arrives at that has understood the real lesson of data-driven design: the data should
drive as much as possible, not only the layout.

**E3.** Expect one of these, and mark on naming the cost:

| Format | Cost |
|---|---|
| Bigger numbers (`11` = red, `12` = power-up) | the grid stops lining up visually |
| Letters (`"R"`, `"P"`, `"X"`) | still one character wide, still readable — usually the best answer |
| A dictionary per cell | fully general, completely unreadable as a picture |
| Two parallel grids | readable, but they must be kept in step |

The thing to draw out: the current format is readable **because** each cell is one character, so the
array looks like the level. Every extension threatens that, and the letter-based version is the usual
professional compromise.

**E4 — the engine question.** The best question in the track. Look for the division:

**The same in all four:** a loop with delta time and a clamp; state in named variables; a state
machine (menu/playing/over); input recorded then acted on; a collision test; a score; a
save/load; "levels are data".

**Always specific:** what the entities are; what a collision *means*; the win and lose rules; the
level data; how it feels.

The best answers notice the hard part — the boundary keeps moving. Is "paddle" general or specific?
Is "lives"? Every engine answers differently, and over-generalising produces engines harder to use
than writing the game directly.

A student who says "the skeleton is whatever was identical in Snake and Brick Breaker, and the game
is whatever differed" has understood it exactly. Tell them that is what a game engine is, and that
`pygame-ce` — which the intermediate level starts with — is somebody else's answer to this question.

---

## End of the Python beginner track

Put lesson 1's text adventure next to today's Brick Breaker on the projector.

One has no graphics at all. Both have: state, a loop, input, update, render. They have now written
that same structure **four times**, in **three different drawing systems** — `print`, turtle, tkinter
— and adapted to each in a single lesson.

That is the point of the whole track. The structure was never about turtle, and it will not be about
`pygame-ce` either.
