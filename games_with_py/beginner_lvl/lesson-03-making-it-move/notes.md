# Lesson 3 — Making It Move

> **Games with Python · Beginner level · Lesson 3 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A player you steer around the screen with the arrow keys — smoothly, continuously, and without the
game ever stopping to wait for you.

```
      +------------------------------+
      |                              |
      |        ●                     |
      |          ↘                   |
      |                              |
      +------------------------------+
         arrow keys to move
```

This is the lesson where lesson 1's loop and lesson 2's drawing finally meet, and where a text game
becomes a real-time one.

## Where this fits

- **Back:** [lesson 1](../lesson-01-the-loop-without-pixels/notes.md) built a loop that **waited**.
  [Lesson 2](../lesson-02-drawing-with-turtle/notes.md) drew pictures that did not **move**.
- **Forward:** [lesson 4](../lesson-04-snake/notes.md) is Snake.
- **Today is the hinge of the whole track.** One change — the loop stops waiting — and everything
  after it is possible.

---

## The idea, in plain words

### The problem with `input()`

Your lesson 1 adventure had a loop. But it **stopped** at `input()` and waited, possibly forever.

That is fine for a text game. It is useless for anything real-time, because while the program is
waiting:

- enemies cannot move,
- timers cannot count down,
- nothing can fall, drift, chase or explode.

The world only exists while the player is typing, which means there is no world.

### The fix: stop waiting, and run anyway

A real-time game does **not** ask "what did the player type?". It asks **"which keys are held down
right now?"** — and then carries on regardless of the answer.

```python
# Lesson 1: STOP and wait. Nothing happens until they press enter.
command = input("> ")

# Lesson 3: do not wait. Something separate keeps a record of the keys, and
# the loop reads that record and carries on whatever it says.
if holding_right:
    player_x = player_x + 5
```

Nothing else about the structure changes. Input, update, render — same three jobs, same order. Only
the *input* job stops blocking.

> This is the single most important idea in the Python track, and it is worth saying plainly:
> **a real-time game loop never waits for the player.** It runs sixty times a second whether you
> touch anything or not. The player is an *influence* on the world, not a *precondition* for it.

### How turtle runs a loop

You cannot use a plain `while True:` loop with turtle. If you did, your code would never give turtle
a chance to actually draw anything, and the window would freeze.

Instead you ask the window to call your function again, a little later:

```python
def game_loop():
    update()                        # change the numbers
    draw()                          # draw the world
    screen.update()                 # show it
    screen.ontimer(game_loop, 16)   # ask to be called again in 16 milliseconds

game_loop()        # start it off
screen.mainloop()  # hand control to turtle, which will keep calling us back
```

`ontimer(function, milliseconds)` means *"call this function again after this many milliseconds"*.
16 ms is about 1/60 of a second, so this gives roughly 60 frames per second.

Notice that `game_loop` asks for *itself* to be called again. That is what makes it a loop, and there
is no `while` anywhere.

### You have seen this before

> **Cross-track callback.** Students on the web track wrote this in their lesson 2:
>
> ```javascript
> function frame() {
>   update();
>   render();
>   requestAnimationFrame(frame);   // call me again
> }
> ```
>
> And here is Python:
>
> ```python
> def game_loop():
>     update()
>     draw()
>     screen.ontimer(game_loop, 16)   # call me again
> ```
>
> **These are the same thing.** Different language, different function name, identical idea: do one
> frame's work, then ask to be called again. If you later learn C++, JavaScript, Lua or C#, you will
> find the same shape waiting for you. The loop is an idea, not a feature of a language.

### Keys: record, do not act

Turtle tells you when a key goes down. The tempting thing is to move the player right there:

```python
# THIS LOOKS RIGHT AND IS WRONG
def go_right():
    global player_x
    player_x = player_x + 20

screen.onkey(go_right, "Right")
```

Run it and hold the right arrow. The player moves once, **pauses for about half a second**, then
jerks along in steps.

That pause is your operating system's **key repeat** — the same thing that makes `aaaa` appear when
you hold a letter in a text box. It was designed for typing, and it is wrong for a game.

The fix is the same idea as `input()`: **the handler records, the loop acts.**

```python
# A dictionary remembering which keys are held down.
keys = {}

def press(name):
    """Return a function that records this key as pressed."""
    def handler():
        keys[name] = True
    return handler

def release(name):
    def handler():
        keys[name] = False
    return handler

for name in ["Up", "Down", "Left", "Right"]:
    screen.onkeypress(press(name), name)     # key goes down
    screen.onkeyrelease(release(name), name) # key comes up

screen.listen()      # tell the window to actually watch the keyboard
```

Then, in `update()`:

```python
if keys.get("Right"):
    player_x = player_x + SPEED
if keys.get("Left"):
    player_x = player_x - SPEED
```

Every problem disappears: no stutter, and you can hold two keys at once to move diagonally.

> **`keys.get("Right")` rather than `keys["Right"]`.** A key nobody has touched is not in the
> dictionary at all, and `keys["Right"]` would raise `KeyError`. `.get()` returns `None` instead,
> which Python treats as false in an `if`. So you never have to set the dictionary up in advance.

### Why `press(name)` returns a function

That bit of code is genuinely strange the first time you see it, and it is worth understanding rather
than copying.

`screen.onkeypress` wants a function that takes **no arguments**. But we want *different* behaviour
for each key. So `press("Right")` **builds and returns** a small function that remembers which key it
was made for.

The obvious alternative does not work:

```python
# BROKEN - every handler ends up using the LAST value of name
for name in ["Up", "Down", "Left", "Right"]:
    screen.onkeypress(lambda: keys.update({name: True}), name)
```

All four handlers share the same `name` variable, and by the time anyone presses a key the loop has
finished and `name` is `"Right"`. So every arrow key sets `"Right"`. This is called a **closure
trap**, it catches professionals regularly, and it produces a bug with no error message.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:** press **Step 1 frame**. Watch the INPUT box: it lights up *every frame*, even
when nothing has changed, and it moves nothing. The movement happens later, in UPDATE. That gap
between *noticing* and *acting* is exactly what you built today.

Then open [the delta-time explainer](../../../shared/visualizers/delta-time.html).

**What to look for:** drag the frame-rate slider. Your `ontimer(game_loop, 16)` asks for 60 frames a
second, but it does not *guarantee* them — a slow computer gives you fewer. See the maths section
below for what that means for you.

---

## The idea, in code

### The whole structure

```python
import turtle

# ---- SETUP ----
screen = turtle.Screen()
screen.setup(width=700, height=560)
screen.bgcolor("#15181d")
screen.tracer(0)                 # we will call update() ourselves

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

# ---- STATE ----
player_x = 0
player_y = 0
SPEED = 5                        # pixels per frame
running = True

# ---- INPUT: record only ----
keys = {}

def press(name):
    def handler():
        keys[name] = True
    return handler

def release(name):
    def handler():
        keys[name] = False
    return handler

for name in ["Up", "Down", "Left", "Right"]:
    screen.onkeypress(press(name), name)
    screen.onkeyrelease(release(name), name)

screen.listen()                  # without this, no key is ever noticed

# ---- UPDATE ----
def update():
    global player_x, player_y
    if keys.get("Right"): player_x += SPEED
    if keys.get("Left"):  player_x -= SPEED
    if keys.get("Up"):    player_y += SPEED     # turtle: y grows UP
    if keys.get("Down"):  player_y -= SPEED

    # Clamp, so the player cannot leave the window.
    half_w, half_h = 330, 260
    player_x = max(-half_w, min(half_w, player_x))
    player_y = max(-half_h, min(half_h, player_y))

# ---- RENDER ----
def draw():
    drawer.clear()               # ERASE first - turtle does not clean itself
    drawer.penup()
    drawer.goto(player_x, player_y - 15)
    drawer.pendown()
    drawer.color("#4a9eff")
    drawer.begin_fill()
    drawer.circle(15)
    drawer.end_fill()
    drawer.penup()

# ---- THE LOOP ----
def game_loop():
    if not running:
        return
    update()
    draw()
    screen.update()              # show the finished frame
    screen.ontimer(game_loop, 16)

game_loop()
screen.mainloop()
```

### `drawer.clear()` is the erase step

Turtle does not clean the screen for you, exactly as the canvas does not in the web track.
`drawer.clear()` removes everything *that turtle drew*. Without it, you get a solid trail of circles
across the screen — which, incidentally, is how you make a deliberate trail effect.

---

## The maths you just used

### `ontimer(game_loop, 16)` is a request, not a promise

16 milliseconds is 1/60 of a second, so this asks for about 60 frames per second. But it is only a
request. If the computer is busy, or your `draw()` is slow, frames take longer and the game runs
**slower**.

So moving `SPEED = 5` pixels per frame means:

| Frames per second | Actual speed |
|---|---|
| 60 | 300 pixels per second |
| 30 | **150 pixels per second** |

Same code, different computer, different game. This is the **frame-rate dependence** bug, and the web
track meets it in their lesson 2.

**The proper fix** is to measure the time each frame actually took and multiply by it:

```python
import time

last_time = time.time()

def game_loop():
    global last_time
    now = time.time()
    dt = now - last_time          # seconds since the last frame
    last_time = now
    if dt > 0.1:                  # clamp: a huge gap means something unusual
        dt = 1 / 60

    update(dt)                    # and inside: player_x += SPEED * dt
    ...
```

with `SPEED = 300` meaning *pixels per second*.

For this lesson, moving a fixed amount per frame is acceptable and simpler. **In lesson 5 you will
need the proper version**, and `code/04-delta-time.py` has it ready. Know that the shortcut is a
shortcut.

### Clamping with `max` and `min`

```python
player_x = max(-330, min(330, player_x))
```

Read it inside out: `min(330, player_x)` is "never more than 330", and `max(-330, ...)` is "never
less than −330". Together: keep it between the two. You will write this constantly.

---

## Break it on purpose

Use `code/03-steerable-player.py`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Delete `screen.listen()` | | |
| Delete `drawer.clear()` from `draw()` | | |
| Remove all the `onkeyrelease` lines | | |
| Change `ontimer(game_loop, 16)` to `ontimer(game_loop, 200)` | | |
| Delete the `screen.ontimer(...)` line entirely | | |
| Replace the `press(name)` pattern with `lambda: keys.update({name: True})` | | |
| Hold Up and Right at the same time and watch the speed | | |

The last one is a real bug you have not been told about yet. Measure how long it takes to cross the
screen diagonally versus straight, and work out the ratio.

---

## Think like an engineer

1. **The diagonal problem.** Holding Up and Right moves you 5 across *and* 5 up. By Pythagoras that
   is `√(5² + 5²) ≈ 7.07` — about **41% faster** diagonally. Players find this within a minute. How
   would you fix it? (There are at least three reasonable answers.)
2. Your player stops **dead** the instant you release a key. Is that good? Think about a spaceship, a
   car, and a cursor. Which should stop instantly, and why?
3. **The honest question about `ontimer`.** You asked for a frame every 16 ms. What happens if your
   `update()` and `draw()` take 20 ms? Does the game run at 60 fps, 50 fps, or something else? What
   would you measure to find out?
4. You now have a loop that never waits. **What else could happen in it that has nothing to do with
   the player?** List five things, and notice that none of them were possible in lesson 1.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Polling** | Asking "what is held down right now?" every frame. What games do. |
| **Event-driven** | Reacting the instant something happens. What `input()` and web pages do. |
| **Key repeat** | The operating system re-sending a held key. Designed for typing. |
| **`ontimer`** | "Call this function again after this many milliseconds." |
| **`listen()`** | Tells the turtle window to start watching the keyboard. |
| **Closure** | A function that remembers values from where it was created. |
| **Frame-rate dependent** | A bug where the game behaves differently on faster computers. |

---

## Recap

- A real-time loop **never waits** for the player. That is the whole difference from lesson 1.
- `ontimer(game_loop, 16)` is Python's `requestAnimationFrame`: do one frame, ask to be called again.
- **Record keys in a handler; move things in `update()`.** Never move in the handler.
- `screen.listen()` or no key is ever noticed. `drawer.clear()` or everything smears.
- Moving a fixed amount **per frame** makes your game's speed depend on the computer. Multiply by
  `dt` to fix it properly.

---

## Stretch goals

1. **Fix the diagonal bug.** Any of the three approaches counts. Say which you chose and why.
2. **Momentum.** Give the player a speed that builds up and decays rather than snapping on and off.
   Try a few values until it feels good.
3. **Delta time, properly.** Convert your game to `SPEED * dt` using `code/04-delta-time.py` as a
   guide, then draw the measured frames-per-second on screen.
4. **A chaser.** Add a second circle that moves towards the player a little each frame. You have just
   written your first enemy AI, in three lines.
5. **Wrap instead of clamp.** Going off the right edge brings you back on the left. Which feels
   better for which kind of game?

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run the lesson 1 adventure. Ask: "how would a monster chase you in this?" Let them realise it cannot, because nothing runs while the program waits. |
| 10–30 | **Concept.** The loop that does not wait. Then `ontimer`. **Put the JavaScript and Python side by side on the board** — the cross-track callback lands hard here and is worth the time. |
| 30–45 | **Live-code** the loop and the keys dictionary. Do the "wrong way" first, hold the key down, and let the class hear the stutter. |
| 45–55 | Break. |
| 55–125 | **Build.** Section D. |
| 125–140 | Break-it-on-purpose. The diagonal-speed one is best measured as a race. |
| 140–150 | Recap. Next lesson: Snake. |

**What usually goes wrong**

1. **No keys work at all.** Missing `screen.listen()`. By far the most common, and there is no error
   message. Tell them to check for it *first*, every time.
2. **The player smears across the screen.** Missing `drawer.clear()`.
3. **The player will not stop moving.** Missing `onkeyrelease`, so the key stays `True` forever.
4. **All four arrows do the same thing.** The closure trap — they used a `lambda` in the loop. This is
   genuinely hard and worth explaining properly rather than waving at. Draw the four handlers all
   pointing at one shared `name` box.
5. **`KeyError: 'Right'`.** They used `keys["Right"]` instead of `keys.get("Right")`.
6. **Nothing happens and there is no window.** Missing `screen.mainloop()` at the end.
7. **Running from an editor that swallows the window.** Make sure everyone can run from a terminal.

**If you are running short on time** — give them the `press`/`release` key-handling block as a
paste-in and explain the closure trap briefly, promising to come back to it. Spend the build time on
the loop and movement. Do not cut `listen()` or `clear()`; they are the two things that produce
silent failures.

**For the student who finishes at minute 90** — stretch goal 4 (the chaser) is the most rewarding:
three lines, and they have written an enemy that follows you. Then ask them to make it *avoidable*,
which is a much harder design problem than it sounds and will absorb them completely.

**The thing to land:** put the JavaScript `requestAnimationFrame` loop and the Python `ontimer` loop
on the board together at the end, and ask what is different. The answer is: the words. Students who
go on to another language will recognise the shape immediately, and telling them that now is what
makes the three-track design pay off.
