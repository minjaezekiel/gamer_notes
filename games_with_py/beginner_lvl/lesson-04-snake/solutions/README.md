# Lesson 4 — Solutions and marking notes

There is also a runnable test here: `python3 test_snake_logic.py` exercises the reference game's
growth, walls, self-collision, reversal rejection and food placement. Worth running before you teach
from it, and worth showing the class — it only works *because* the logic is kept separate from the
drawing.

---

## Section A

**A1.** [3] `snake.insert(0, new_head)` puts a new square on the front; `snake.pop()` removes the last
one. No other segment is touched because the body does not actually move — only the two ends change,
and everything between them stays exactly where it was. Two marks for the description, one for the
"only the ends" insight.

**A2.** [2] By **not** removing the tail. `insert` happens as usual, the `pop` is skipped, and the
list is one longer.

**A3.** [3] Because the direction can then be **added** to the position arithmetically, so moving
needs no `if` statements at all — one line handles all four directions. Two marks. One more for
either: checking for a reversal becomes arithmetic (`-dc, -dr`), or adding new directions
(diagonals) would mean adding data rather than code.

**A4.** [3] Because Snake works in **whole grid squares**, which are integers. Two integers are
either equal or they are not — so `head == food` is an exact, complete collision test. Pong moved in
smooth decimal pixel positions, so it needed an overlap test and a tolerance. Two marks for the
distinction, one for naming the general point: choosing a grid made the problem disappear.

**A5.** [2] Subtracting keeps any **leftover** time, so the snake's speed stays exact even when a
frame runs late. Setting it to zero throws that time away, which makes the snake slightly slower than
`MOVE_DELAY` asks for — and the error accumulates.

---

## Section B

**B1.** [4] `DOWN` is `(0, 1)`, so the new head is `(5, 6)`.

- Normal move: `[(5,6), (5,5), (4,5)]` — still length 3.
- Eating: `[(5,6), (5,5), (4,5), (3,5)]` — length 4, tail kept.

Two marks each. Watch for students who move every segment individually and get the right answer the
hard way — correct, but worth pointing out that the list did it for them.

**B2.** [4] **The game ends immediately on the first move.** `insert` has already put `new_head` into
the list, so `new_head in snake` finds it — at index 0, the head itself. The square that triggers it
is the head's own new position.

Fix: do the check **before** the insert. Two marks for the symptom, two for identifying that the head
finds itself.

**B3.** [3] `0.12 / (1/60) = 0.12 × 60 = **7.2 frames**` between steps. The snake moves
`1 / 0.12 ≈ **8.3 squares per second**`. Two marks for the first, one for the second.

**B4.** [4] Two marks each:

- **Version A (wrong).** `direction` becomes `UP` immediately, then `LEFT` immediately — and the
  reversal check compares `LEFT` against `UP`, which is not its opposite, so it is allowed. The snake
  then moves **left** while its body is still to the left of it, and dies instantly. It reversed
  through a direction it never actually travelled in.
- **Version B (correct).** Both presses only set `next_direction`. The snake was moving `RIGHT`, so
  the reversal check at move time compares `LEFT` against `RIGHT` and rejects it. `next_direction`
  ends up as `LEFT` but is never applied, because... *see note below.*

**Teacher note on B4:** version B as written in the exercise rejects the *second* press only if the
check uses `direction` (the direction actually being travelled), which the reference code does. It is
worth showing students the reference implementation, because the check must compare against the
**current** direction, not against `next_direction`. Students who notice this subtlety unprompted
have understood the bug better than the question asked them to.

---

## Section C

**C1.** [3] The `else: snake.pop()` is missing (or the `pop` is inside the eating branch). Without
the `pop` on a normal move, the list grows every time.

**C2.** [4] The `if spot not in snake` check is missing, so food can spawn **underneath the snake's
own body**. Two marks.

Why that symptom, two marks: the food is drawn first and the snake drawn over it, so it looks
invisible or like it flickered and vanished. And it cannot be eaten in the usual way — the head only
"eats" by arriving at the square, and that square is already occupied by the body, so the player
chases food that appears to be missing.

**C3.** [3] Tuples are **immutable** — they cannot be changed after they are made. You build a new one
instead:

```python
head = snake[0]
new_head = (head[0] + 1, head[1])
```

Two marks for the explanation, one for the fix. This is a good moment to mention *why* tuples are
immutable: it is what lets them be used as dictionary keys and put in sets, which matters for E2.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Do the snake with people first.** Five students in a line. To move: the person at the front adds
someone new in front of them, and the person at the back sits down. Everyone else does nothing. Then:
"now it eats" — nobody sits down.

Two minutes, no slides, and the entire mechanic is understood. It is the single most effective
explanation in this course.

**Checkpoint 1.** Check `(0, 0)` is top-left. Students who get it bottom-left have the turtle y-axis
sign wrong, which is lesson 2's bug returning.

**Checkpoint 3.** The reversal check must compare against `direction`, not `next_direction`.
Comparing against `next_direction` lets the two-fast-presses bug straight back in.

**Checkpoint 5.** Watch for the self-collision check landing after `insert`. Instantly diagnosable:
the game ends on move one.

---

## Section E — marking notes, not answers

**E1.** On a 99%-full board, roughly **1 in 100** guesses succeeds, so about **100 guesses** on
average — and it is unbounded, so it could in principle take far longer. In practice this only bites
at the very end of a winning game, which is exactly when you least want a stall.

The non-guessing method: **build a list of all empty squares and pick one at random.**

```python
free = [(c, r) for r in range(ROWS) for c in range(COLUMNS)
        if (c, r) not in snake]
return random.choice(free)
```

What it costs: it scans the whole board every time food is placed — `COLUMNS × ROWS` work — whereas
rejection sampling usually succeeds on the first guess and does almost nothing. So the "better"
method is **slower in the common case and faster in the worst case**.

That trade-off is the real content of this question. Students who spot it have found something
genuinely important: the best algorithm depends on what usually happens, not only on what could
happen.

**E2.** The answer is a **`set`**. Checking `in` on a list is a scan of every item; checking `in` on
a set is effectively instant regardless of size.

```python
snake = [...]            # the list, for order (we need to know the tail)
snake_squares = set()    # the same squares, for fast lookup
```

The cost: you now have the same information in two places and must keep them in step — add to both on
insert, remove from both on pop. Get that wrong and you have a bug that is invisible until the snake
is long.

As for when to care: honestly, not at Snake's size. A 200-item scan per tick, eight times a second,
is nothing. A strong answer says so — **"I would not do this yet, and here is the length at which I
would"** is better engineering than optimising immediately.

**E3.** Filling the board is detectable: `len(snake) == COLUMNS * ROWS`. In practice `place_food`
would fail first (it would loop forever), which is a nice illustration of a bug and a win condition
being the same event.

What *should* happen is a design question. Options students offer: a win screen; the board clears and
a new level starts; the snake keeps going and the score keeps rising. Worth noting that the original
Nokia Snake simply became unplayable, because nobody expected anyone to get that far.

**E4.** At least four knobs:

1. **Speed** — reduce `MOVE_DELAY`. The obvious one, and it becomes unplayable fast.
2. **Board size** — shrink the playing area.
3. **Obstacles** — add walls as the score rises.
4. **Food value or scarcity** — food that times out, or is worth more the further away it is.
5. **Length gained per food** — grow by three instead of one.

The good answers notice that **speed alone is a bad difficulty curve**, because it eventually exceeds
human reaction time and the game stops being about skill. Changing the *board* keeps the challenge
about planning rather than reflexes. That distinction — difficulty from reaction time versus
difficulty from decision-making — is a real and useful one, and worth naming for them.

---

## Teacher note: the thing to land at the end

Ask the class why Snake has no collision bugs, when Pong on the web track needed four conditions, a
careful ordering, and a direction check.

The answer is that **choosing a grid made an entire category of problem not exist**. No overlap test,
no rounding, no tunnelling — because two integers are either equal or they are not.

Picking a representation that makes your problem easy is one of the most valuable things a programmer
can do, and it almost never appears in a tutorial. Say it out loud; it is worth more than the game.
