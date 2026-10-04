# Lesson 4 — Snake

> **Games with Python · Beginner level · Lesson 4 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**Snake.** Complete, playable, with growth, food, walls, self-collision, a score and a game-over
screen.

```
      +----------------------------+
      |                            |
      |     ████████               |
      |            █          *    |
      |            █               |
      |            ██              |
      +----------------------------+
             score: 40
```

This is the first game in the Python track that is genuinely *a game* — and the whole thing rests on
one idea you already have: **a list**.

## Where this fits

- **Back:** [lesson 3](../lesson-03-making-it-move/notes.md) gave you a loop that never waits, and a
  player you can steer.
- **Forward:** [lesson 5](../lesson-05-a-real-window-tkinter/notes.md) moves to a real window widget.
- **Today:** lists as game objects, grid movement, and your first real *rules*.

---

## The idea, in plain words

### A snake is a list of positions

That is the entire trick, and when you see it the game stops being mysterious.

```python
# Each item is one square of the body. The FIRST item is the head.
snake = [(5, 5), (4, 5), (3, 5)]
#         head    body    tail
```

Now watch how the snake moves. It does **not** shuffle every segment along one at a time. It does
two things:

```python
# 1. Put a new head on the front, one step in the direction we are going.
snake.insert(0, new_head)

# 2. Take the last segment off the back.
snake.pop()
```

Add to the front, remove from the back. The snake has moved, and no segment was touched. That is it.

And growing is even simpler:

> **To grow, just do not remove the tail.**

```python
if ate_food:
    pass              # keep the tail - the snake is now one longer
else:
    snake.pop()       # normal move
```

One `if`. That is the whole growth mechanic of Snake, and it is a genuinely lovely piece of design —
the thing that feels most complicated turns out to be the thing you *stop* doing.

### A grid, not pixels

Snake does not move smoothly. It jumps one whole square at a time, and that is not a limitation —
it is what makes the game readable and fair.

So the game thinks entirely in **grid coordinates**:

```python
CELL = 20             # pixels per grid square
COLUMNS = 25
ROWS = 20

head = (5, 5)         # column 5, row 5 - NOT pixels
```

and converts to pixels only at the moment of drawing. Everything else — movement, collisions, food —
works in whole squares, where comparing two positions is exact:

```python
if head == food:      # EXACTLY equal. No "close enough" needed.
```

That exactness is why Snake has no collision bugs. There is no overlap test, no rounding, no
tunnelling. Two squares are either the same square or they are not.

> Compare this with the web track's lesson 4, which needed four conditions and a tolerance for a ball
> hitting a paddle. **Choosing a grid made an entire category of problem disappear.** Picking a
> representation that makes your problem easy is one of the most valuable things a programmer can do.

### Direction is also a pair of numbers

```python
RIGHT = (1, 0)        # column + 1, row + 0
LEFT  = (-1, 0)
DOWN  = (0, 1)        # row + 1 - rows go DOWN
UP    = (0, -1)

direction = RIGHT

# Moving the head:
head_column, head_row = snake[0]
dc, dr = direction
new_head = (head_column + dc, head_row + dr)
```

Storing the direction as a pair means `update()` has **no `if` statements about direction at all**.
Four directions, one line of arithmetic. Adding diagonal movement would mean adding data, not code.

### The rule that makes it a game

A snake may not reverse into itself. If you are going right and press Left, you would immediately eat
your own neck.

```python
def set_direction(new_direction):
    global next_direction
    # Reject the exact opposite of the way we are going.
    if (new_direction[0] == -direction[0] and
            new_direction[1] == -direction[1]):
        return
    next_direction = new_direction
```

> **Why `next_direction` and not `direction`?**
>
> This is subtle, and it is a real bug that students hit. Key presses arrive at any moment, but the
> snake only moves on a frame. If you change `direction` the instant a key arrives, a player can
> press Up and then Left *between* two moves — and the snake reverses into itself through a direction
> it never actually travelled in.
>
> Storing the request in `next_direction` and only applying it when the snake actually moves makes
> that impossible. **Decide at the moment of acting, not at the moment of asking.**

### Food that does not appear inside the snake

```python
def place_food():
    while True:
        spot = (random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1))
        if spot not in snake:      # "not in" checks the whole list
            return spot
```

Keep guessing until you find a free square. This is called **rejection sampling**, and it is a
perfectly respectable technique — it is simple, it is obviously correct, and for a mostly-empty board
it almost always succeeds on the first try.

It does have a weakness, which is worth knowing about: if the snake fills nearly the whole board,
this loop could run a very long time. It is in the *Think like an engineer* section.

---

## The idea, in pictures

Open [the grids and flat arrays explainer](../../../shared/visualizers/tilemap-indexing.html).

**What to look for:** drag the marker and watch how moving one square right changes the index by 1,
while moving one square down changes it by a whole row. Snake lives entirely in that grid — its head
is a `(column, row)` pair exactly like the one you are dragging.

Then open [the box collision explainer](../../../shared/visualizers/aabb-collision.html) and notice
what you are **not** having to do today. No overlap test, no four conditions, no edge cases. In a
grid, `head == food` is the whole collision system.

---

## The idea, in code

### The move, in full

```python
def move_snake():
    global snake, food, score, state, direction

    direction = next_direction            # apply the request NOW, not earlier

    head_column, head_row = snake[0]
    dc, dr = direction
    new_head = (head_column + dc, head_row + dr)

    # ---- did we hit a wall? ----
    if not (0 <= new_head[0] < COLUMNS and 0 <= new_head[1] < ROWS):
        state = "GAME_OVER"
        return

    # ---- did we hit ourselves? ----
    # Check BEFORE adding the new head, or the head would find itself.
    if new_head in snake:
        state = "GAME_OVER"
        return

    snake.insert(0, new_head)             # grow at the front

    if new_head == food:
        score += 10
        food = place_food()
        # Note: NO pop(). Keeping the tail is what makes the snake grow.
    else:
        snake.pop()                       # normal move: drop the tail
```

Read that twice. Twenty lines, and it is the entire game.

### `0 <= x < COLUMNS` is two comparisons at once

Python lets you chain comparisons the way maths does:

```python
if 0 <= new_head[0] < COLUMNS:       # means: 0 <= x AND x < COLUMNS
```

Most languages make you write `x >= 0 && x < COLUMNS`. Python's version reads like the maths and is
one of the genuinely nice things about the language.

### Snake does not run at 60 frames per second

A snake moving 60 squares a second would be unplayable. The game *loop* still runs at 60 fps, but the
snake only **steps** a few times a second:

```python
move_timer = move_timer + dt
if move_timer >= MOVE_DELAY:          # MOVE_DELAY = 0.12 seconds
    move_timer = move_timer - MOVE_DELAY
    move_snake()
```

So the loop runs constantly (so input stays responsive and the screen stays smooth), but the *game
logic* ticks at its own slower rate. That separation — **render fast, simulate slowly** — is used in
a great many real games.

Note `move_timer = move_timer - MOVE_DELAY` rather than `move_timer = 0`. Subtracting keeps any
leftover time, so the snake's speed stays exact even if a frame runs late. Setting it to zero quietly
throws that time away and makes the snake slightly slower than you asked for.

---

## The maths you just used

### Adding a direction to a position

```python
new_head = (head_column + dc, head_row + dr)
```

This is **vector addition**, and you have just used it without being told the word. A position is a
pair of numbers; a direction is a pair of numbers; adding them pair-wise moves the position. The
intermediate level gives it a name and a class. You already understand it.

### Opposites

```python
if new_direction[0] == -direction[0] and new_direction[1] == -direction[1]:
```

Reversing a direction means negating both numbers. `RIGHT = (1, 0)` becomes `(-1, 0)`, which is
`LEFT`. Direction-as-numbers makes "is this the opposite?" a piece of arithmetic rather than four
special cases.

### Why a grid removes rounding problems

A position in a grid is two **integers**. Two integers are either equal or they are not — there is no
"nearly". With smooth movement you would be comparing decimals, where `3.0000001` and `2.9999999`
look different to the computer and identical to a human, and you would need a tolerance.

Choosing integers made that whole class of problem not exist.

---

## Break it on purpose

Use `code/03-snake.py`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the `else: snake.pop()` | | |
| Change `MOVE_DELAY` to `0.02` | | |
| Set `direction` directly in the key handler instead of `next_direction` | | |
| Move the self-collision check to *after* `snake.insert` | | |
| Remove the `if spot not in snake` check from `place_food` | | |
| Change `move_timer -= MOVE_DELAY` to `move_timer = 0` | | |

The third one is the subtle one. To see it, you must press two keys very fast — Up then Left while
moving right. Most students will not manage it by accident, which is exactly why the bug survives
into finished games.

---

## Think like an engineer

1. **Food placement.** `place_food` keeps guessing until it finds a free square. If the snake filled
   99% of the board, roughly how many guesses would it need? Is that a problem in practice? Design a
   method that never guesses, and say what *it* costs.
2. **Winning.** Snake traditionally has no win condition. What *should* happen when the snake fills
   the entire board? Can your code even detect it?
3. **`in` is not free.** `new_head in snake` checks every segment, so a 200-long snake does 200
   comparisons every move. At what length would you start to care? What could you store instead to
   make the check instant? *(You know a Python type that answers this.)*
4. **Design a difficulty curve.** Right now the snake moves at a constant speed. Design how the
   difficulty should increase. There are at least four knobs — find them, and say which one you think
   feels best and why.
5. **The honest one.** The real Snake on old Nokia phones let you pass through walls and come out the
   other side. Which is the better game, and does the answer depend on who is playing?

---

## Vocabulary

| Word | What it means |
|---|---|
| **Grid coordinates** | Positions in whole squares, not pixels. |
| **`insert(0, x)`** | Put something at the **front** of a list. |
| **`pop()`** | Remove and return the **last** item of a list. |
| **Tuple** | An unchangeable pair, like `(5, 3)`. Used here for positions. |
| **Rejection sampling** | Guess, check, and guess again until it is valid. |
| **Tick** | One step of the game logic, which may be slower than one frame. |
| **Vector addition** | Adding two pairs of numbers pair-wise. |

---

## Recap

- A snake is **a list of positions**. The first item is the head.
- Move by `insert(0, new_head)` and `pop()`. **Grow by skipping the `pop()`.**
- Work in **grid squares**, not pixels, and collisions become `==` with no edge cases.
- Store direction as a **pair of numbers**, and movement needs no `if` statements.
- Apply a direction change **when the snake moves**, not when the key is pressed.
- The game loop can run fast while the game logic ticks slowly.

---

## Stretch goals

1. **Speed up as you grow.** Reduce `MOVE_DELAY` each time food is eaten. Find a curve that stays
   fun rather than becoming impossible.
2. **Wrap-around walls.** Going off one edge brings you back on the other. Use `%`.
3. **High score** saved to a file, so it survives restarting the game.
4. **Obstacles.** Walls inside the playing area. Where do you store them, and how much code changed?
5. **Two players.** Two snakes, two sets of keys, and they can collide with each other. This is
   harder than it sounds — what happens if both heads enter the same square on the same tick?
6. **A food that moves.** Suddenly the game is about prediction rather than planning.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Play Snake for two minutes on the projector. Then ask: "how does the computer store the snake?" Let them guess — someone will say a list, and the lesson is launched. |
| 10–30 | **Concept.** The insert/pop move, done physically. See below. |
| 30–45 | **Live-code** `move_snake()`. It is twenty lines and is the whole game. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. The `move_timer = 0` one is a nice subtle finish. |
| 140–150 | Recap. Next lesson: a real window. |

**Do the snake with people.** Five students stand in a line. To move: the person at the front
*adds* someone new in front of them, and the person at the back sits down. Everyone else does
nothing. Then: "now the snake eats" — nobody sits down.

Two minutes, no slides, and the entire mechanic is understood. It is by far the most effective
explanation in this course, and students remember it for weeks.

**What usually goes wrong**

1. **The snake grows forever.** Missing or misplaced `pop()`.
2. **Instant game over.** The self-collision check runs *after* `insert`, so the head finds itself in
   the list. Order matters, and this is a good example of why.
3. **The snake can reverse into itself.** They set `direction` in the handler rather than
   `next_direction`. Hard to trigger deliberately — demonstrate it yourself by pressing two keys very
   fast on the projector, or students will not believe it exists.
4. **Food spawning on the snake.** Missing the `not in snake` check. Looks like the food is invisible.
5. **`TypeError: 'tuple' object does not support item assignment.`** They tried
   `head[0] = head[0] + 1`. Tuples cannot be changed — you build a new one. This is a good
   introduction to why some types are immutable, and they will meet it again.
6. **The snake moves at 60 squares a second.** No `MOVE_DELAY`, so the game logic runs every frame.
   Spectacular and instantly diagnosable.

**If you are running short on time** — give them `place_food()` and the drawing code, and have them
build only `move_snake()` and the input. That is the lesson; everything else is scaffolding.

**For the student who finishes at minute 90** — stretch goal 5 (two players) is genuinely difficult
in an interesting way. The question "what happens if both heads enter the same square on the same
tick?" has no obvious right answer, and watching a 14-year-old discover that they have to *decide*
something the rules do not cover is worth a great deal.

**The thing to land:** ask the class why Snake has no collision bugs when the web track's Pong needed
four conditions and careful ordering. The answer is that **choosing a grid made the problem
disappear**. Picking a representation that makes your problem easy is one of the most valuable moves
in programming, and it almost never appears in a tutorial.
