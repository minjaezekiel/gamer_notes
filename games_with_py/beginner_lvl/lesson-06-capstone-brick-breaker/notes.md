# Lesson 6 — Capstone: Brick Breaker

> **Games with Python · Beginner level · Lesson 6 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**Brick Breaker**, by yourself: multiple levels, lives, a score, and a high score that survives
closing the program.

```
      +--------------------------------+
      | score 1240   lives ♥♥   lvl 2  |
      | ███ ███ ███ ███ ███ ███ ███    |
      | ███ ███     ███ ███     ███    |
      | ███     ███ ███     ███        |
      |                                |
      |              ●                 |
      |         ▬▬▬▬▬▬▬▬               |
      +--------------------------------+
                      best: 3400
```

Two genuinely new ideas today: **classes**, and **saving to a file**. Everything else you already
have.

## Where this fits

- **Back:** [lesson 5](../lesson-05-a-real-window-tkinter/notes.md) gave you a real window and
  retained-mode drawing.
- **Forward:** the intermediate level, which starts with `pygame-ce`.
- **Today:** the last lesson of the beginner track, and the one where your code starts to look like
  the code in books.

---

## The idea, in plain words

### Idea 1: a dictionary wants to be a class

Your fruit in lesson 5 were dictionaries:

```python
fruit = {"x": 100, "y": 0, "speed": 90, "item": 7}
```

That works. But it has three annoyances that get worse as a game grows:

1. **Typos are silent.** `fruit["spede"]` raises `KeyError` only when that line runs — possibly
   minutes into a game.
2. **The behaviour lives somewhere else.** `move_fruit(fruit)` and `draw_fruit(fruit)` are separate
   functions, far away from the data they work on.
3. **Nothing says what a fruit *is*.** You have to read every function that touches one to find out
   which keys it has.

A **class** is a dictionary that also knows what it is and what it can do:

```python
class Brick:
    def __init__(self, canvas, x, y, w, h, hits):
        """Runs when you make a new Brick. 'self' is the brick being made."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hits = hits
        self.alive = True
        self.item = canvas.create_rectangle(x, y, x + w, y + h,
                                            fill=self.colour(), outline="")

    def colour(self):
        return "#ff9246" if self.hits >= 2 else "#4a9eff"

    def box(self):
        """Where this brick is, for collision tests."""
        return (self.x, self.y, self.w, self.h)
```

Making one looks like calling a function:

```python
brick = Brick(canvas, 40, 60, 68, 24, hits=1)
print(brick.x)          # 40
print(brick.box())      # (40, 60, 68, 24)
```

> **What `self` actually is.** When you write `brick.colour()`, Python calls
> `Brick.colour(brick)` — it passes the brick in as the first argument, and that argument is
> conventionally named `self`. So `self` is just "the particular brick this method was called on".
> It is not magic, and it is not a keyword. You could call it anything; everyone calls it `self`.

**Classes are not better than dictionaries.** They are better *here*, because a brick has both data
and behaviour and there are sixty of them. For a one-off bag of values, a dictionary is still the
right answer.

### Idea 2: levels are data

Exactly the same idea as lesson 1's rooms, and the web track's Breakout:

```python
# 0 = nothing, 1 = normal brick, 2 = tough brick
LEVELS = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
    ],
]
```

You can **see** the level. Adding a fifth means adding an array. The code that builds bricks never
changes:

```python
def build_level(layout):
    bricks = []
    for row in range(len(layout)):
        for column in range(len(layout[row])):
            kind = layout[row][column]       # ROW first, then column
            if kind == 0:
                continue
            x = MARGIN + column * (BRICK_W + GAP)
            y = TOP + row * (BRICK_H + GAP)
            bricks.append(Brick(canvas, x, y, BRICK_W, BRICK_H, kind))
    return bricks
```

`layout[row][column]`, **not** `layout[column][row]`. The outer list holds rows, so the first index
picks which row. Getting it backwards gives a level mirrored along the diagonal — or a crash, if the
level is not square.

### Idea 3: which side of the brick did it hit?

The naive answer — always flip the vertical speed — is wrong, and it shows the moment the ball clips
a brick from the side: it carves straight through the whole row sideways.

Work out which side by comparing how much the boxes overlap on each axis:

```python
def bounce_off(self, brick):
    ball = self.box()
    k = brick.box()

    overlap_x = min(ball[0] + ball[2], k[0] + k[2]) - max(ball[0], k[0])
    overlap_y = min(ball[1] + ball[3], k[1] + k[3]) - max(ball[1], k[1])

    # The SMALLER overlap tells you which way it came in. A ball that has just
    # poked in from above overlaps a lot horizontally and barely at all
    # vertically - so it arrived vertically, and should bounce vertically.
    if overlap_y < overlap_x:
        self.speed_y = -self.speed_y
    else:
        self.speed_x = -self.speed_x
```

Draw it on paper before you write it.

### Idea 4: saving, which is four lines

```python
import json
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "highscore.json"

def load_high_score():
    try:
        return json.loads(SAVE_FILE.read_text())["high_score"]
    except Exception:
        return 0        # no file yet, or it is damaged. Either way, start at 0.

def save_high_score(value):
    try:
        SAVE_FILE.write_text(json.dumps({"high_score": value}))
    except Exception:
        pass            # a read-only disk should not crash the game
```

> **Why the `try` blocks?** Because the file might not exist yet (first run), might be corrupted,
> might be on a read-only disk, or might have been edited by a curious student. **A game that crashes
> because it cannot save is worse than a game that quietly does not save.** Deciding what should
> happen when something goes wrong is part of designing the feature, not an afterthought.

`Path(__file__).parent` means "the folder this script is in", so the save file lands next to your
game rather than in whatever folder you happened to run it from.

---

## The idea, in pictures

Open [the grids and flat arrays explainer](../../../shared/visualizers/tilemap-indexing.html).

**What to look for:** moving one square right changes the index by 1; one square down changes it by a
whole row. Your `build_level` loops do exactly that conversion — and `layout[row][column]` is the
same "row first" rule the explainer shows.

Then open [the box collision explainer](../../../shared/visualizers/aabb-collision.html) and drag a
box so it only just clips a corner. That is the case your `bounce_off` has to get right.

---

## The maths you just used

### Overlap on one axis

> **overlap = min(right edges) − max(left edges)**

The shared region starts wherever the *rightmost* left edge is, and ends wherever the *leftmost*
right edge is. If that comes out negative, the boxes are not overlapping at all — which is the AABB
test written another way.

Comparing the two overlaps tells you which direction the ball came from, because it will have barely
poked in along the axis it was travelling.

### Steering the ball

```python
centre = paddle.x + paddle.w / 2
offset = (ball.x - centre) / (paddle.w / 2)     # -1 .. 0 .. +1
ball.speed_x = offset * STEER_STRENGTH
```

Dividing by *half the paddle width* turns "how far from the middle, in pixels" into a number from −1
to +1, regardless of how wide the paddle is. That pattern — **divide by the maximum to get a
fraction** — is everywhere: health bars, progress bars, volume sliders, fades.

---

## Break it on purpose

Use `code/02-brick-breaker.py`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Swap `layout[row][column]` for `layout[column][row]` | | |
| Always flip `speed_y` in `bounce_off` | | |
| Remove the `break` after a brick is hit | | |
| Delete the `highscore.json` file while the game is running | | |
| Put nonsense text into `highscore.json` and restart | | |
| Add a row to a level that is shorter than the others | | |
| Remove `self` from a method's arguments | | |

The fourth and fifth are the point of the `try` blocks. The last one gives an error message worth
reading carefully — it tells you exactly what `self` is.

---

## Think like an engineer

1. **When is a class worth it?** You now have `Brick`, `Ball` and `Paddle` as classes and `keys` as a
   dictionary. What made each the right choice? Name something in your game that should **stay** a
   dictionary.
2. **Your save file is plain text a student could edit.** Is that a problem? When would it be? What
   would you do about a player who edits their high score to 999999 — and is "nothing" an acceptable
   answer?
3. **Levels as data.** Your layouts are 8 columns wide. What would need to change for a 20-wide
   level? If the answer is "nothing", your code is good. If it is "several numbers", find them.
4. **Design a level format** that can also say "this brick is red", "this brick drops a power-up",
   "this brick cannot be broken". What does it look like, and what did you give up?
5. **The big one.** You have built four games in this track: a text adventure, a steerable player,
   Snake, and now Brick Breaker. **What is the same in all four?** Design the leftover part — the
   thing that would be useful in the fifth game too. What must always stay specific to one game?

That last question is what a game *engine* is. Your answer is more interesting than it sounds.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Class** | A description of a kind of thing: its data and what it can do. |
| **Instance** | One actual thing made from a class. One brick. |
| **Method** | A function that belongs to a class. |
| **`self`** | The particular instance a method was called on. |
| **`__init__`** | The method that runs when a new instance is made. |
| **Attribute** | A piece of data belonging to an instance: `brick.x`. |
| **JSON** | A plain-text format for saving data. |
| **Persistence** | Data that survives the program closing. |

---

## Recap

- A **class** is a dictionary that also knows what it is and what it can do. Use one when a thing has
  both data and behaviour, and there are many of them.
- `self` is not magic: it is the instance the method was called on.
- **Levels are data.** `layout[row][column]` — rows first.
- Find which side of a brick was hit by comparing the two **overlaps**.
- **Saving is four lines of `json`** — and the `try` blocks are part of the feature, not an
  afterthought.
- You can now build games nobody has taught you.

---

## Stretch goals

1. **Power-ups.** A brick drops something: a wider paddle, a slower ball, an extra life.
2. **A level editor.** Click a grid to toggle bricks and print the array so you can paste it back.
   About 30 lines, and a genuinely useful tool.
3. **Save the whole game**, not just the score — level, lives, brick states — so you can quit and
   resume.
4. **Tough bricks that look tough.** Change the colour after the first hit. Without that feedback the
   player thinks the game is broken.
5. **Sound** with `winsound` on Windows or `os.system("afplay ...")` on macOS. (This is genuinely
   awkward in plain Python, which is one honest reason `pygame-ce` exists — it is the first thing the
   intermediate level fixes.)
6. **Make it yours.** Brick Breaker with gravity. With moving bricks. For two players. This is the
   real stretch goal.

---

## Teacher notes

**Timing**

This is mostly a long build. Resist teaching.

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Show the finished game, then show a `LEVELS` array beside it and edit digits live. |
| 10–30 | **Concept.** Classes — convert a dictionary into a class on the board, side by side, so they see it is the same data. Then levels as data. |
| 30–40 | **Live-code** `class Brick` and `build_level`. Nothing else is new. |
| 40–50 | Break. |
| 50–135 | **Build.** They will need all of it. |
| 135–145 | **Show-and-tell.** Protect this. |
| 145–150 | Where next: the intermediate level. |

**Teaching classes without the jargon.** Put a dictionary on the left of the board and the equivalent
class on the right. Same attributes, same values. Then add a method to the class and ask where the
equivalent would live for the dictionary — "a function somewhere else, that you have to remember to
pass the dictionary to". That contrast does more than any definition.

**Do not** teach inheritance, `super()`, class variables, properties or dunder methods today. They
need `__init__`, attributes and methods. Everything else is intermediate-level material and will only
dilute what they are learning.

**What usually goes wrong**

1. **`TypeError: colour() takes 0 positional arguments but 1 was given.`** They forgot `self`. The
   error message is actually excellent — read it with them, because it explains exactly what `self`
   is.
2. **`layout[column][row]`.** Mirrored level, or `IndexError` on a non-square one.
3. **The ball carves sideways through a whole row.** They always flip `speed_y`. Draw it on the board.
4. **Bricks vanish in pairs.** No `break` after the first hit per frame.
5. **`AttributeError: 'Brick' object has no attribute 'alive'.`** They set it outside `__init__`, or
   misspelled it. Worth noting that Python lets you add attributes anywhere, which is flexible and
   also why the typo is not caught earlier.
6. **The high score resets every run.** They are saving to a relative path and running from a
   different folder. `Path(__file__).parent` fixes it.

**If you are running short on time** — give them the `Brick` class and `build_level` as a paste-in,
with one hard-coded level, and have them build the ball, paddle and collisions. The classes are the
lesson; the level loader is scaffolding.

**For the student who finishes at minute 90** — the level editor. It is about 30 lines, it is a real
tool, and the student who builds one will supply levels to the whole class.

**Marking a capstone.** Not on features. On: does it run; are the levels separate from the logic; can
they explain any method you point at; and **did they change something to make it theirs?** The last
one matters most. A rougher game with an original idea beats a flawless copy.

**What to say at the end of the beginner track.** Put lesson 1's text adventure next to today's game
on the projector. One has no graphics at all. Both have: state, a loop, input, update, render. Point
out that they have now written that same structure four times, in three different drawing systems
(`print`, turtle, tkinter), and adapted to each in a single lesson.

Then tell them what the intermediate level adds — and that it is not a new structure, just more
inside the one they already have.
