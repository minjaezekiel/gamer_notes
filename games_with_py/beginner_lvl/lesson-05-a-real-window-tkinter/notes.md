# Lesson 5 — A Real Window: tkinter

> **Games with Python · Beginner level · Lesson 5 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**Catch the Falling Fruit** — a basket you steer, fruit falling at increasing speed, a score, lives,
and a game-over screen.

```
      +------------------------------+
      | score 120          lives ♥♥♥ |
      |        *                     |
      |              *               |
      |   *                          |
      |                     *        |
      |          ▬▬▬▬▬▬              |
      +------------------------------+
```

And one thing that will catch you out: **tkinter's y axis points downwards**, which is the opposite
of turtle. Lesson 2 warned you about this. Today it arrives.

## Where this fits

- **Back:** [lesson 4](../lesson-04-snake/notes.md) built Snake with turtle.
- **Forward:** [lesson 6](../lesson-06-capstone-brick-breaker/notes.md) is the capstone.
- **Today:** a real windowing toolkit, and the discovery that everything you learned still applies.

---

## The idea, in plain words

### Why move off turtle?

Turtle is excellent for learning and it has two real limits:

1. **It is slow.** It was built to draw lines, not to redraw a hundred moving things sixty times a
   second. Snake is about as much as it comfortably handles.
2. **It is not a real toolkit.** You cannot add buttons, menus, text boxes or dialogs.

`tkinter` is what turtle is *built on top of*. Moving to it is not learning a new thing so much as
removing a layer. It also ships with Python, so there is still nothing to install.

The good news: **almost nothing you know changes.** The loop, the state, the input pattern, the
erase-then-draw rule — all identical. What changes is two things, and they are worth real attention.

### Change 1: y points DOWN

This is the big one.

| | turtle | **tkinter** |
|---|---|---|
| `(0, 0)` | the middle | **top-left corner** |
| y grows | **upwards** | **downwards** |

So in tkinter, to move something **up** you **subtract**:

```python
basket_y = basket_y - 5     # moves UP the screen
basket_y = basket_y + 5     # moves DOWN
```

And gravity — which pulls things down — **adds**:

```python
fruit_y = fruit_y + FALL_SPEED * dt      # falls downwards
```

That is now the same convention as the web canvas, pygame, SDL, raylib and your phone. **Turtle was
the odd one out**, and from here on you are in the normal world.

> If you took the web track, you already know this. If you did not, it is worth a minute with the
> [coordinates explainer](../../../shared/visualizers/coordinates.html) — the right-hand grid is the
> one you are now in.

### Change 2: the canvas remembers what you drew

This is genuinely different, and it is better.

With turtle you **cleared and redrew everything, every frame**. With a tkinter canvas you **create
an item once** and then **move it**:

```python
# Create it ONCE, before the loop. This returns an ID - a plain integer.
basket = canvas.create_rectangle(100, 400, 180, 420, fill="#4a9eff")

# Then, each frame, just move it.
canvas.coords(basket, x, y, x + 80, y + 20)
```

`create_rectangle` does not give you an object. It gives you an **integer handle** — the canvas keeps
the real thing and hands you a number to refer to it by. That surprises people, so it is worth
stating plainly:

```python
print(basket)       # prints something like: 3
```

The canvas redraws itself. You are not managing pixels any more; you are managing a *list of shapes
the canvas knows about*. That is called **retained mode**, and it is a genuinely different idea from
turtle's **immediate mode** where you redraw everything yourself.

| | Immediate mode (turtle, web canvas) | Retained mode (tkinter canvas) |
|---|---|---|
| Each frame you… | clear and redraw everything | move the things that moved |
| The system remembers | nothing | every shape |
| Good for | lots of things changing constantly | a moderate number of distinct objects |

Neither is better. Knowing which one you are in is what matters — and getting it wrong is why a
student who keeps calling `create_oval` every frame ends up with ten thousand invisible ovals and a
game that slows to a crawl.

> **The classic bug in this lesson:** creating a new item every frame instead of moving the existing
> one. The game looks fine for two seconds and then grinds to a halt. If that happens, count your
> items with `len(canvas.find_all())` and watch the number climb.

### Change 3: `after()` instead of `ontimer()`

```python
# turtle (lesson 3)
screen.ontimer(game_loop, 16)

# tkinter (today)
window.after(16, game_loop)
```

Same idea, different name: *"call this function again in 16 milliseconds."* You have now seen this
pattern three times — `requestAnimationFrame`, `ontimer`, `after`. It will keep appearing.


### Quitting without a wall of red text

There is one more thing `after()` does that will bite you, and it is worth
meeting properly because **it is the only place in this course where catching an
exception is the right answer.**

`window.after(16, game_loop)` schedules the *next* frame. Suppose the player
quits while one of those is already sitting in the queue. The window is
destroyed — and then the queued callback fires anyway, tries to draw on a canvas
that no longer exists, and the player gets:

```
_tkinter.TclError: invalid command name ".!canvas"
```

There are **two different ways out of your game**, and they need different fixes.

#### 1. The quit key — you control this, so prevent it

```python
running = True
after_id = None

def quit_game():
    global running
    running = False                      # stop the loop rescheduling itself
    if after_id is not None:
        window.after_cancel(after_id)    # unschedule the queued frame
    window.destroy()

def game_loop():
    global after_id
    if not running:
        return                           # a frame may already be in flight
    update(dt)
    draw()
    after_id = window.after(16, game_loop)
```

**Do not wrap this in `try`/`except`.** You can prevent the problem entirely, and
catching the error would only hide it — including later, when something
genuinely went wrong.

#### 2. The window's X button — you do *not* control this

The window manager tears the window down without asking your code first, so
there is nothing to prevent. For tkinter you can ask to be told:

```python
window.protocol("WM_DELETE_WINDOW", quit_game)
```

With `turtle` there is no such hook, so the loop has to **notice and stop
quietly**:

```python
def game_loop():
    try:
        update()
        draw()
        screen.update()
        screen.ontimer(game_loop, 16)
    except (tkinter.TclError, turtle.Terminator):
        return          # the window has gone; stop without complaining
```

Notice how **narrow** that `except` is. It names the two specific errors that
teardown produces. A bare `except Exception` would also swallow real bugs in
`update()` and `draw()` — and a game that silently ignores its own bugs is far
worse than one that crashes honestly.

> **The rule worth taking away.** Exception handling is for things you genuinely
> cannot prevent — a file that might not exist, a window someone else closed, a
> network that might drop. It is **not** a substitute for fixing a bug you
> control. If you can stop it happening, stop it happening.

---

## The idea, in pictures

Open [the coordinates explainer](../../../shared/visualizers/coordinates.html).

**What to look for:** this time, the **right-hand** grid is yours. Drag the dot *upwards* and watch
the screen's y get **smaller**. Then watch the ball on the right, told `y = y - 90 * dt`, and see it
rise. That minus sign is today's whole coordinate change.

Then open [the gravity explainer](../../../shared/visualizers/gravity-and-velocity.html).

**What to look for:** your fruit falls because its y *increases*. Press Step and watch the velocity
grow by the same amount each frame while the *distance covered* grows faster. That is why a falling
thing accelerates.

---

## The idea, in code

### The setup

```python
import tkinter

WIDTH = 640
HEIGHT = 480

window = tkinter.Tk()
window.title("Catch the Falling Fruit")
window.resizable(False, False)

canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT,
                        bg="#15181d", highlightthickness=0)
canvas.pack()
```

`highlightthickness=0` removes a focus border that otherwise shifts everything by two pixels and
makes your collision maths subtly wrong. It is a small thing that wastes a lot of time.

### Rectangles are two corners, not a corner and a size

This catches people out:

```python
# turtle / most games:  x, y, width, height
# tkinter:              LEFT, TOP, RIGHT, BOTTOM

canvas.create_rectangle(100, 400, 180, 420)
#                        ^    ^    ^    ^
#                      left  top right bottom
```

So a basket 80 wide and 20 tall at `(100, 400)` is `create_rectangle(100, 400, 180, 420)`.

Writing a small helper saves you from doing that conversion in your head forty times:

```python
def set_box(item, x, y, w, h):
    """Position an item using the x, y, width, height we actually think in."""
    canvas.coords(item, x, y, x + w, y + h)
```

### Input: exactly the pattern from lesson 3

```python
keys = {}

def on_press(event):
    keys[event.keysym] = True

def on_release(event):
    keys[event.keysym] = False

window.bind("<KeyPress>", on_press)
window.bind("<KeyRelease>", on_release)
```

`event.keysym` is the key's name: `"Left"`, `"Right"`, `"space"`, `"a"`. One handler covers every
key, so there is no closure trap this time.

And in `update`, exactly as before — **record in the handler, move in the loop**:

```python
if keys.get("Right") or keys.get("d"):
    basket_x += BASKET_SPEED * dt
```

### Collision: the four conditions again

```python
def boxes_overlap(a, b):
    """a and b are (x, y, width, height)."""
    return (a[0] < b[0] + b[2] and
            a[0] + a[2] > b[0] and
            a[1] < b[1] + b[3] and
            a[1] + a[3] > b[1])
```

This is the same AABB test the web track writes in its lesson 4, in Python. Four conditions, all
joined by `and`, and you remember it by asking when the boxes definitely **cannot** touch.

### Removing fruit: loop backwards

```python
for i in range(len(fruits) - 1, -1, -1):
    fruit = fruits[i]
    fruit["y"] += fruit["speed"] * dt

    if caught or off_the_bottom:
        canvas.delete(fruit["item"])    # tell the canvas to forget the shape
        fruits.pop(i)                   # and remove it from our list
```

`range(len(fruits) - 1, -1, -1)` counts **down**: start at the last index, stop before −1, step by
−1. Loop forwards while removing and you skip items — the same bug as the web track's particles, in
a new costume.

And note `canvas.delete(...)` **as well as** `fruits.pop(i)`. In retained mode you are keeping two
records — your list and the canvas's — and they must stay in step. Forget the `delete` and the fruit
vanishes from your logic but stays on screen forever.

---

## The maths you just used

### Falling, and why it accelerates

```python
fruit["speed"] += GRAVITY * dt      # gravity changes the SPEED
fruit["y"] += fruit["speed"] * dt   # the speed changes the POSITION
```

Two levels of adding, exactly as in the gravity explainer. Gravity does not say how fast the fruit
goes; it says *how fast the speed increases*. So each frame the speed is a little bigger, and each
frame the fruit covers a little more ground than the last.

### Difficulty that rises smoothly

```python
spawn_delay = max(0.35, 1.2 - score * 0.004)
```

Start at 1.2 seconds between fruits, get 0.004 seconds faster per point, and **never go below
0.35 seconds**. That `max` is doing real work: without it the game eventually spawns faster than the
screen can show, and becomes unplayable rather than hard.

Every difficulty curve needs a floor. Design the limit at the same time as the slope.

---

## Break it on purpose

Use `code/03-catch-the-fruit.py`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Change `fruit["y"] += speed` to `-=` | | |
| Call `canvas.create_oval(...)` inside the loop instead of `canvas.coords(...)` | | |
| Remove `canvas.delete(fruit["item"])` but keep `fruits.pop(i)` | | |
| Loop *forwards* through `fruits` while removing | | |
| Remove the `max(0.35, ...)` from the spawn delay | | |
| Remove `highlightthickness=0` and look closely at the edges | | |
| Delete the `if not running: return` from `game_loop`, then press Escape | | |

The second one is today's headline bug. Add `print(len(canvas.find_all()))` to watch the item count
climb into the thousands.

---

## Think like an engineer

1. **Retained versus immediate.** Turtle made you redraw everything; tkinter remembers your shapes.
   For each of these, say which you would rather have, and why: a Snake game; a particle effect with
   500 sparks; a chess board; a scrolling platform level.
2. **Two records, one truth.** You keep a Python list of fruit *and* the canvas keeps items. What
   goes wrong when they disagree? Design a way to make it impossible for them to disagree.
3. **Difficulty.** Your fruit speeds up as the score rises. At some point it will exceed human
   reaction time. How would you find that point without guessing? What would you change instead of
   speed?
4. **The honest question.** `after(16, game_loop)` asks for 60 fps. What happens to your game if the
   window is dragged, or another program hogs the computer for half a second? What does `dt` do, and
   what does the clamp protect you from? What does the clamp *cost* you?

---

## Vocabulary

| Word | What it means |
|---|---|
| **Canvas** | A tkinter widget you can draw shapes on. |
| **Item ID** | The integer the canvas gives you to refer to a shape. |
| **Retained mode** | The system remembers your shapes; you move them. (tkinter) |
| **Immediate mode** | You redraw everything each frame. (turtle, web canvas) |
| **`after(ms, fn)`** | "Call this function again in this many milliseconds." |
| **`keysym`** | The name of the key in a tkinter key event. |
| **Widget** | One piece of a window: a canvas, a button, a label. |
| **`after_cancel`** | Unschedule a frame you asked for but no longer want. |
| **`WM_DELETE_WINDOW`** | The hook that tells you the X button was pressed. |

---

## Recap

- tkinter's `(0, 0)` is **top-left** and **y grows downwards**. Turtle was the odd one out.
- `create_rectangle` takes **left, top, right, bottom** — not x, y, width, height.
- The canvas **remembers your shapes**. Create once, then `coords()` to move. Do not create in the
  loop.
- Keep your list and the canvas in step: `canvas.delete` **and** `list.pop`.
- `window.after(16, game_loop)` is the same idea as `ontimer` and `requestAnimationFrame`.
- Loop **backwards** when removing from a list.
- **Quit cleanly.** A `running` flag for the quit key; a narrow `except` for the window being
  closed. Exception handling is for what you cannot prevent, not for bugs you control.

---

## Stretch goals

1. **Bad fruit.** Something you must *avoid*, which costs a life if caught. Suddenly the game is
   about choosing, not just moving.
2. **Golden fruit** worth more, falling faster, appearing rarely.
3. **A combo counter** — catching several in a row without missing multiplies the score.
4. **Mouse control.** Bind `<Motion>` and steer the basket with the pointer. Which feels better?
5. **A real pause**, on the P key, that stops everything including the spawn timer.
6. **Measure your frame rate** and draw it on screen. Then add 500 fruit and watch what happens.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Show Snake from last lesson, then the finished fruit game. Ask what is different — someone will say "it looks like a real program". That is tkinter. |
| 10–30 | **Concept.** The y-axis flip first (coordinates visualizer, right-hand grid). Then retained versus immediate mode, which is the genuinely new idea today. |
| 30–45 | **Live-code** the window, one rectangle, and moving it with `coords`. Deliberately write the `create_oval`-in-the-loop bug and let the class watch the item count climb. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. |
| 140–150 | Recap. Next week is the capstone. |

**Setup check:** `python3 -c "import tkinter; print('ok')"`. On some Linux installs this needs
`sudo apt install python3-tk`. Check this **before** the lesson, not during it.

**What usually goes wrong**

1. **Everything is upside down.** The y-flip. They subtract to fall and add to rise. The coordinates
   visualizer fixes it in seconds; put it on the projector and leave it there.
2. **The game grinds to a halt after a few seconds.** They are calling `create_oval` every frame.
   Today's headline bug. `print(len(canvas.find_all()))` makes it undeniable.
3. **Fruit disappears from the logic but stays on screen.** They popped from the list without
   `canvas.delete`.
4. **Rectangles come out the wrong size.** They passed x, y, width, height instead of two corners.
   The `set_box` helper in the notes prevents this; encourage it.
5. **Keys do nothing.** The window does not have focus, or they bound to the canvas rather than the
   window. `window.focus_force()` helps.
6. **Half the fruit never gets removed.** Forward loop with removal — the lesson 5 particles bug from
   the web track, and the lesson 4 bug from Breakout. Point out that this is the *third* time.

**If you are running short on time** — give them the window setup and the `set_box` helper as a
paste-in. The lesson is the y-flip and retained mode; the boilerplate is not.

**For the student who finishes at minute 90** — stretch goal 3 (a combo counter) is the most
interesting, because it is a *design* change rather than a technical one, and it immediately raises
the question of what should break a combo. Stretch goal 6 is the better one for a student who likes
systems: adding 500 fruit and watching tkinter struggle is a concrete, memorable demonstration of why
pygame exists, and sets up the intermediate level perfectly.

**The thing to land:** nothing about the *structure* changed today. Same loop, same state, same
input pattern, same collision test, same backwards-removal idiom. What changed was the drawing system
underneath — and that is the third drawing system they have met. Point out that they adapted to it in
one lesson, and that this is what the course has been training for all along.
