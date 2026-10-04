# Lesson 4 — Snake

## Cheat sheet

### A snake is a list

```python
snake = [(5, 5), (4, 5), (3, 5)]
#         head    body    tail
```

### Moving: add a head, drop a tail

```python
snake.insert(0, new_head)   # grow at the FRONT
snake.pop()                 # drop the BACK
```

No other segment is touched.

### Growing: just skip the pop

```python
if new_head == food:
    score += 10
    food = place_food()
    # NO pop() - that is the whole growth mechanic
else:
    snake.pop()
```

### Directions are pairs

```python
RIGHT = (1, 0);  LEFT = (-1, 0)
DOWN  = (0, 1);  UP   = (0, -1)

dc, dr = direction
new_head = (head[0] + dc, head[1] + dr)
```

No `if` statements about direction, anywhere.

### No reversing

```python
if (new[0] == -direction[0] and
    new[1] == -direction[1]):
    return          # reject it
next_direction = new
```

Store the **request**; apply it when the snake **moves**. Otherwise two fast presses let the snake
reverse into itself.

### Walls and self

```python
if not (0 <= x < COLUMNS and 0 <= y < ROWS):
    state = "GAME_OVER"

if new_head in snake:     # BEFORE insert!
    state = "GAME_OVER"
```

### Food on a free square

```python
while True:
    spot = (randint(0, COLUMNS-1),
            randint(0, ROWS-1))
    if spot not in snake:
        return spot
```

### Tick slower than you draw

```python
move_timer += dt
if move_timer >= MOVE_DELAY:
    move_timer -= MOVE_DELAY   # not = 0
    move_snake()
```

Render at 60 fps; step the snake a few times a second.

### Why a grid has no collision bugs

Two squares are either **equal or not**. No overlap test, no rounding, no tunnelling.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Describe, in words, what the two lines that move the snake do. Why is no other segment touched?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> How does the snake grow? Give the one-line answer.
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why does the game store direction as <code>(1, 0)</code> rather than the string <code>"right"</code>?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Why does Snake need no overlap test, when the web track's Pong needed four conditions?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why <code>move_timer -= MOVE_DELAY</code> rather than <code>move_timer = 0</code>?
<div class="lines"><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> The snake is <code>[(5,5), (4,5), (3,5)]</code> and the direction is <code>DOWN</code>. Write the list after one normal move, and then after one move where it eats.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What happens, and why? Be precise about which square causes it.

```python
snake.insert(0, new_head)
if new_head in snake:
    state = "GAME_OVER"
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> <code>MOVE_DELAY</code> is 0.12 and the game loop runs at 60 fps. Roughly how many frames pass between snake steps? How many squares does the snake move per second?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> The snake is moving <strong>right</strong>. A player presses <strong>Up</strong> and then <strong>Left</strong> very quickly, both between two ticks. Describe what happens with each version, and which is correct.

```python
# version A
def set_direction(new):
    global direction
    direction = new

# version B
def set_direction(new):
    global next_direction
    next_direction = new
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The snake grows by one square on every single move, whether it eats or not. What is wrong?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Food sometimes appears and seems to vanish instantly, or cannot be eaten at all. What is missing from <code>place_food</code>, and why does it produce <em>that</em> symptom?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> This raises <code>TypeError: 'tuple' object does not support item assignment</code>. Why, and what should it be?

```python
head = snake[0]
head[0] = head[0] + 1
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Draw a grid of squares from a list of <code>(column, row)</code> positions. Write <code>grid_to_pixels</code> and check that square <code>(0, 0)</code> is in the top-left corner.</li>
<li><strong>Checkpoint 2.</strong> Make the snake move: <code>insert</code> a new head, <code>pop</code> the tail, on a timer. It should glide across the screen at a readable speed.</li>
<li><strong>Checkpoint 3.</strong> Add the arrow keys using direction pairs, and reject reversals. Use <code>next_direction</code>, not <code>direction</code>.</li>
<li><strong>Checkpoint 4.</strong> Add food, eating and growth. Make sure food never spawns on the snake.</li>
<li><strong>Checkpoint 5.</strong> Add wall and self-collision, a score, and a game-over screen with a restart.</li>
<li><strong>Checkpoint 6.</strong> Make the head a different colour from the body, and make the snake speed up slightly as it grows.</li>
</ul>

<div class="note">
<span class="note-label">Order matters in this lesson</span>
<p>Check self-collision <strong>before</strong> <code>insert</code>, not after. Afterwards, the new
head is in the list, so it finds itself and the game ends on the first move.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** `place_food` guesses until it finds an empty square. If the snake filled 99% of the board,
roughly how many guesses would it need? Design a method that **never** guesses, and say what that one
costs.

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** `new_head in snake` checks every segment, so a 200-long snake does 200 comparisons per move.
At what length would you start to care? What could you store **instead** to make the check instant?
(You know a Python type that does this.)

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Snake traditionally has no win condition. What *should* happen when the snake fills the whole
board? Can your code even detect it?

<div class="lines"><i></i><i></i></div>

**E4.** Design a difficulty curve. There are at least **four** different things you could change as
the game goes on. Find them, then say which you think feels best and why.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Speed up as the snake grows. Find a curve that stays fun rather than becoming impossible.
2. Wrap-around walls using `%`.
3. A high score saved to a file.
4. Obstacles inside the playing area. How much code had to change?
5. **Two players.** What happens if both heads enter the same square on the same tick? You will have
   to decide something the rules do not cover.
6. Food that moves.
