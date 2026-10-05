# Lesson 1 — Hello pygame-ce

> **Games with Python · Intermediate level · Lesson 1 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A window with a square you steer, which moves at **the same speed on every computer**, and which
closes properly when you ask it to.

That sounds like less than you built in a single beginner lesson. It is not, because for the first
time **you write the loop yourself**. `turtle.ontimer` and `tkinter.after` called your function for
you; from today, nothing calls you. You ask for the events, you decide when to draw, and you say how
long a frame is.

```
   ┌─────────────────────────────┐
   │                             │
   │         ▉                   │   arrow keys to move
   │                             │   Escape to quit
   │                             │
   └─────────────────────────────┘
      pygame-ce · 60 frames a second · delta time from frame one
```

## Where this fits

- **Back:** [beginner lesson 5](../../beginner_lvl/lesson-05-a-real-window-tkinter/notes.md) used
  `tkinter`'s `after()` as a frame timer, and beginner lesson 3 used `turtle`'s `ontimer`. Both of
  those called your function. Today you take that job back.
- **Forward:** [lesson 2](../lesson-02-rects-images-and-the-display/notes.md) puts pictures in the
  window; everything after that is built on today's loop.
- **Other tracks:** this is `webgames` beginner lesson 1's loop, written out longhand. In JavaScript
  the browser calls `requestAnimationFrame(frame)` — it calls you. In pygame **you call**, which is
  exactly what C++ does too. One of these three is the odd one out, and it is not Python.

---

## The idea, in plain words

### Install it first

Read [`../INSTALL.md`](../INSTALL.md) before anything else. The short version:

```bash
python3 -m pip install pygame-ce
python3 -c "import pygame; print(pygame.version.ver)"
```

If the second line prints a version, you are ready.

### The smallest possible pygame program

```python
import pygame

pygame.init()                                   # start the library up
screen = pygame.display.set_mode((640, 480))    # make a window, get its Surface
pygame.display.set_caption("Hello")

running = True
while running:
    # 1. INPUT ------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # the window's close button
            running = False

    # 2. UPDATE -----------------------------------------------------------
    #    (nothing yet)

    # 3. RENDER -----------------------------------------------------------
    screen.fill((20, 24, 32))                   # erase
    pygame.display.flip()                       # show it

pygame.quit()                                   # tidy up
```

Fourteen lines, and every one of them is a decision you now make. Look at the three comments: that is
the loop from beginner lesson 1, in the same order, written out rather than implied.

### `screen` is a Surface, and so is everything else

`set_mode` hands you a **Surface** — a rectangle of pixels you can draw on. That is the only kind of
drawable thing in pygame, and the window's Surface is not special: later you will make your own
Surfaces, draw on them, and copy them onto this one. A sprite is a Surface. A spritesheet is a
Surface. The screen is a Surface.

Knowing that one noun is most of learning pygame.

### The event queue, and why you must empty it

Every key press, mouse move, window resize and close request goes into a **queue**, and
`pygame.event.get()` takes everything out of it.

You are not allowed to ignore this. If you never call it, the operating system stops hearing from your
program, decides it has hung, and greys out the window. On macOS you get a spinning cursor; on Windows
the title bar says "(Not Responding)".

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
```

So: **drain the queue every frame, whether you care about the events or not.** `code/01-a-window.py`
has a switch that stops draining it, so you can watch your own window become unresponsive — it is a
strange experience and worth having once.

### Events versus state: the same distinction as beginner lesson 3

This is the thing that catches people moving from `tkinter`, and it is the same lesson the web track
learned in its third beginner lesson.

```python
# EVENTS: a thing that HAPPENED, once.
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        shoot()                      # exactly one shot per press. Correct.

# STATE: what is true RIGHT NOW.
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player_x -= SPEED * dt           # every frame the key is held. Also correct.
```

Movement wants **state**. Firing a bullet, jumping and opening a menu want **events**. Using the wrong
one gives you either a player who moves in juddering steps (the operating system's key-repeat rate,
exactly as in the web track) or a gun that fires sixty times a second.

Both live in the same loop, and both are correct — for different jobs.

### Delta time, from the first lesson

`pygame.time.Clock` does two jobs, and it is easy to notice only the first:

```python
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0
```

- `tick(60)` **waits** long enough that the loop runs at most 60 times a second. Without it, your loop
  spins as fast as the computer can manage, pointlessly, with the fan on.
- It **returns how many milliseconds** passed since the last call. Divide by 1000 to get seconds, and
  that is your `dt`.

The `/ 1000.0` is the trap. Forget it and every speed in your game is a thousand times too big, so the
square leaves the window in the first frame — which looks like it never appeared at all.

And `tick(60)` is a *limit*, not a promise. A slow frame takes as long as it takes, so `dt` varies, so
you multiply by it:

```python
player_x += SPEED * dt        # SPEED is in pixels per SECOND
```

> **Why this is in lesson 1 rather than lesson 3.** In the beginner track, `ontimer(16)` hid this
> problem well enough to get away with for a while. pygame does not hide it at all, and a habit formed
> on the first day costs nothing. Every single example in this level multiplies by `dt`.

### Drawing, and the order that matters

```python
screen.fill((20, 24, 32))                               # 1. erase everything
pygame.draw.rect(screen, (77, 171, 247), (x, y, 40, 40))  # 2. draw this frame
pygame.display.flip()                                   # 3. show it
```

Colours are `(red, green, blue)` tuples, 0 to 255. Rectangles are `(left, top, width, height)`. And
**y points down**, exactly as on a canvas and exactly as in the C++ track's screen buffer — the
opposite of `turtle`, which was the odd one out all along.

`flip()` is the moment the player sees anything. Everything before it happens off-screen, which is why
a half-drawn frame is never visible. That technique has a name — **double buffering** — and the
beginner C++ track built one by hand.

> `pygame.display.update()` does the same thing, and can take a list of rectangles to redraw only
> part of the window. That was an important optimisation in 1998. Use `flip()`.

### Quitting properly

```python
pygame.quit()        # after the loop
```

Two things go wrong without a clean quit, and the second one is the one that will annoy you:

1. On some systems the window lingers after the program ends.
2. Running your game from IDLE, or from inside an editor, can leave the interpreter in a state where
   the next run fails with a confusing error — because `pygame.init()` was never undone.

The habit to form: **the loop ends, then `pygame.quit()`**. One line, always the last line.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:** step through a few frames and watch the three phases light up in order. Today is
the first time *you* are the one writing that order out — `pygame.event.get()`, then your own update,
then `fill` and `flip`. Notice that the explainer's loop looks identical to the one in the web track
and the C++ track, because it is.

Then open [delta time](../../../shared/visualizers/delta-time.html) and drag the frame rate down to 20.
One ball falls apart and the other does not. `code/03-delta-time.py` is that page, in Python, on your
machine.

---

## The idea, in code

Run them in order. Each one is a single file and adds one idea.

1. `code/01-a-window.py` — the fourteen-line program, plus a key that stops draining the event queue
   so you can watch the window stop responding.
2. `code/02-events-and-state.py` — every event printed as it arrives, next to a live display of which
   keys are held. The difference becomes obvious in about ten seconds.
3. `code/03-delta-time.py` — two squares, one multiplied by `dt` and one not, with keys that change the
   frame cap. The measured speed of each is on screen.
4. `code/04-a-square-you-steer.py` — the whole lesson: polled input, delta time, clamping to the
   window, a clean quit, and the four-line self-test hook.

---

## The maths you just used

**1. Milliseconds to seconds.** `dt = clock.tick(60) / 1000.0`. That is the whole of it, and it is the
single most common mistake in this lesson. If your square moves 1000× too fast, this is why.

**2. Pixels per second.** Writing `SPEED = 300` and multiplying by `dt` means 300 pixels every second,
regardless of frame rate. At 60 fps each frame moves `300 / 60 = 5` pixels; at 30 fps each frame moves
10. The distance over one second is the same, which is the entire point.

**3. Clamping.** `x = max(0, min(WIDTH - SIZE, x))`. Python's `min` and `max` take any number of
arguments, so this reads better than the two `if`s you wrote at beginner level. Note `WIDTH - SIZE`,
not `WIDTH`: the position is the square's *left edge*, so stopping it at `WIDTH` lets it leave the
window entirely.

No new mathematics beyond that today — and that is worth saying rather than inventing some. The hard
part of this lesson is that you are now responsible for the shape of the program, not the arithmetic.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Delete the `for event in pygame.event.get():` loop entirely | | |
| Remove `/ 1000.0` from the `dt` line | | |
| Use `clock.tick(5)` instead of `tick(60)` | | |
| Remove `clock.tick()` altogether | | |
| Remove `screen.fill(...)` | | |
| Remove `pygame.display.flip()` | | |
| Move `flip()` to **before** the drawing | | |
| Use `event.type == pygame.KEYDOWN` to move the square instead of `get_pressed()` | | |
| Delete `pygame.quit()` and run the file twice from IDLE | | |

The missing `fill` is the nicest one: you have accidentally built a drawing program, which is exactly
the bug the beginner web lesson called *forgetting to erase*. The missing `tick` is worth watching
with the fan audible.

---

## Think like an engineer

1. `tkinter`'s `after()` called your function. pygame makes you write `while running:`. Neither is
   wrong. What does each one make easy, and what does each make awkward? (Think about what happens when
   you want to pause, or run the game faster than real time.)
2. You must drain the event queue every frame or the window freezes. Why would a library be designed
   that way, rather than handling it for you? What would it cost to do it automatically?
3. **Design something.** Your loop currently runs at 60 fps and draws every frame. A chess program does
   not need to redraw sixty times a second. Sketch a loop that only draws when something has actually
   changed. What would it need to keep track of, and what would break about delta time?
4. **The hard one.** `dt` can be large — if the window is dragged, or the machine sleeps, or a slow
   frame happens. A `dt` of 2 seconds moves your square 600 pixels in one step, straight through
   anything in the way. What would you do about it? Give two different answers and say which you would
   use for a platformer and which for a card game.

---

## Vocabulary

| Word | What it means |
|---|---|
| **`pygame.init()`** | Starts the library. Call it before anything else. |
| **Surface** | A rectangle of pixels you can draw on. The window is one. So is a sprite. |
| **`set_mode((w, h))`** | Makes the window and returns its Surface. |
| **Event queue** | The list of things that have happened. Must be emptied every frame. |
| **`QUIT`** | The event from the window's close button. |
| **`get_pressed()`** | Which keys are held down *right now*. Polled state, not events. |
| **`Clock.tick(fps)`** | Waits to cap the frame rate, and returns the milliseconds since last time. |
| **Delta time (`dt`)** | How long the last frame took, in **seconds**. |
| **`flip()`** | Shows everything you have drawn. The moment the player sees it. |
| **Double buffering** | Drawing off-screen and showing it all at once, so no half-drawn frame appears. |
| **`pygame.quit()`** | Undoes `init()`. The last line of your program. |

---

## Recap

- **You write the loop.** Nothing calls your function any more, and that is the same arrangement the
  web and C++ tracks have.
- `screen` is a **Surface**, and every drawable thing in pygame is one.
- **Drain the event queue every frame**, or the operating system decides your program has hung.
- **Events** for things that happen once; **`get_pressed()`** for things that are true now. Movement
  needs state.
- `dt = clock.tick(60) / 1000.0`. The `/ 1000.0` is not optional, and `tick` is a limit rather than a
  promise.
- **Erase, draw, flip** — in that order, every frame.
- `pygame.quit()` is the last line.

---

## Stretch goals

1. **Show the real frame rate** on screen with `clock.get_fps()`, and watch it while you drag the
   window about. The number tells you more about `dt` than any explanation.
2. **Two squares, two control schemes** — arrows and WASD — using the intent pattern from the beginner
   level, so the movement code never mentions a key name.
3. **A resizable window.** `pygame.RESIZABLE`, and handle `pygame.VIDEORESIZE`. Then decide what should
   happen to your square's clamping, which is a real design question.
4. **Mouse control.** `pygame.mouse.get_pos()` for the square's position. Then make both work at once
   and decide what happens when somebody uses both.
5. **A pause.** Press `P` and the square stops. You will discover that pausing is not "stop calling
   update" — the window still has to be drawn and the events still have to be drained. This is lesson
   11's whole subject, arriving early.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `01-a-window.py` and press the key that stops draining the queue. The window greys out and the cursor spins. Ask what is wrong — nobody guesses "the operating system thinks we have hung". |
| 10–25 | **Concept.** The fourteen-line program on the board, with the three phases labelled. Then the events-versus-state distinction, which half the class will have met in the web track. |
| 25–40 | **Live-code** it from an empty file. Do not paste. Then add `dt` and say the `/ 1000.0` out loud. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Most of the class will finish early; push them at the stretch goals rather than at a bigger program. |
| 120–140 | Break-it-on-purpose. The missing `fill` and the missing `tick` are the two to do together. |
| 140–150 | Recap. Lesson 2 puts pictures in the window. |

**Before the lesson: install `pygame-ce` on the actual classroom machines yourself.** Not on your
laptop — on theirs. Half of this lesson's possible failures are install failures, and discovering them
with thirty students waiting is a lost lesson.

Have ready on the board:

```bash
python3 -m pip install pygame-ce
python3 -c "import pygame; print(pygame.version.ver)"
```

**What usually goes wrong**

1. **`No module named pygame`** when it is definitely installed. Two different Pythons. The fix that
   always works: run it as `python3 -m pip install pygame-ce`, using the same `python3` that runs the
   game. Worth putting on the board before anybody asks.
2. **`error: externally-managed-environment`** on Linux. The answer is a virtual environment, and
   `INSTALL.md` has it. Do not let students fight this one.
3. **The window appears and vanishes instantly.** No loop, or the loop ended immediately. It will look
   like a crash and is not.
4. **The square moves a thousand times too fast**, so it is never visible. Missing `/ 1000.0`.
5. **The window will not close.** No `QUIT` handling. They will reach for the mouse, then for Ctrl-C,
   then for you.
6. **The square leaves a trail.** No `fill`. Several students will prefer this and want to keep it; let
   them, then ask how they would clear it when they want to.
7. **Juddery movement.** They used `KEYDOWN` instead of `get_pressed()`. This is the web track's
   beginner lesson 3 appearing in Python, and the explanation is identical: that is the operating
   system's key-repeat rate.
8. **Nothing is drawn at all.** They drew after `flip()`.

**If you are running short on time** — cut `code/02` and talk about events versus state at the board
instead. Do **not** cut delta time: every example in this level assumes it, and the habit is much
harder to add in lesson 6 than in lesson 1.

**For the student who finishes at minute 80** — stretch goal 5 (pause) is the best, because it looks
trivial and is not: they will try `while paused: pass` and freeze the window, which is this lesson's
main idea arriving from a different direction.

**The point to land at the end:** nothing in this lesson was new *conceptually* — it is the same loop
from the beginner levels and the same loop as the other two tracks. What changed is that the library
stopped making decisions on their behalf. That is more code and much less mystery, and every lesson
after this one is easier because of it.
