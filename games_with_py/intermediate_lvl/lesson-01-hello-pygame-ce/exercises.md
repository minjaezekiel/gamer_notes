# Lesson 1 — Hello pygame-ce

## Cheat sheet

### The whole program

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000.0      # SECONDS

    # INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # UPDATE
    if keys[pygame.K_LEFT]:
        x -= SPEED * dt

    # RENDER
    screen.fill((20, 24, 32))
    pygame.draw.rect(screen, (77,171,247), (x, y, 40, 40))
    pygame.display.flip()

pygame.quit()
```

### The install

```bash
python3 -m pip install pygame-ce
python3 -c "import pygame; print(pygame.version.ver)"
```

`No module named pygame` when it *is* installed = two different Pythons. Always
`python3 -m pip install`, never bare `pip install`.

### Events or state?

| want | use |
|---|---|
| move while held | `pygame.key.get_pressed()` |
| fire once per press | `KEYDOWN` event |
| close the window | `QUIT` event |

Using `KEYDOWN` to move gives juddering: that is the **key-repeat rate**.

### Delta time

```python
dt = clock.tick(60) / 1000.0
x += SPEED * dt        # SPEED is px per SECOND
```

- `tick(60)` **waits** (caps the rate) **and** returns **milliseconds**
- `/ 1000.0` is not optional — without it everything is 1000× too fast
- `tick(60)` is a limit, not a promise, so `dt` varies

### Drawing order

```
fill   →   draw   →   flip
```

No `fill` = a trail. No `flip` = nothing at all. `flip` before drawing = nothing.

Colours are `(r, g, b)`, 0–255. Rects are `(left, top, width, height)`.
**y points down.**

### Clamping

```python
x = max(0, min(WIDTH - SIZE, x))
```

`WIDTH - SIZE`, not `WIDTH`: `x` is the left edge.

### The last line

```python
pygame.quit()
```

### Running without a window

```bash
SDL_VIDEODRIVER=dummy SELFTEST_FRAMES=150 python3 game.py
```

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What are the three phases of the loop, in order, and which pygame call belongs to each?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> What happens if you never call <code>pygame.event.get()</code>, and <em>why</em> does it happen?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Give one job that needs a <code>KEYDOWN</code> event and one that needs <code>get_pressed()</code>, and say what goes wrong if you swap them.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> What are the <em>two</em> things <code>clock.tick(60)</code> does?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why divide by 1000, and what is the symptom of forgetting?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> What is a <em>Surface</em>? Name two different things in pygame that are one.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> Why does <code>flip()</code> exist at all, rather than each drawing call appearing immediately?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> <code>SPEED</code> is 300 and the game runs at a steady 60 fps. How far does the square move each frame? At 30 fps? How far in one second in each case?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The <code>/ 1000.0</code> is missing and the game runs at 60 fps. <code>SPEED</code> is 300. How far does the square move in one frame, and what will the player see?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> What does this draw?

```python
pygame.display.flip()
screen.fill((20, 24, 32))
pygame.draw.rect(screen, (255, 0, 0), (100, 100, 40, 40))
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> The player holds the right arrow for exactly one second. Describe what the square does in each version.

```python
# version A
if keys[pygame.K_RIGHT]:
    x += 300 * dt

# version B
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        x += 5
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> <code>WIDTH</code> is 640 and the square is 40 wide. The clamp is <code>x = max(0, min(WIDTH, x))</code>. What is wrong, and what is the largest <code>x</code> it allows?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The window appears, is completely black, and nothing responds. Ctrl-C in the terminal does nothing either.

```python
while running:
    screen.fill((20, 24, 32))
    pygame.display.flip()
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The window flashes up and disappears immediately. The author is sure it crashed.

```python
pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((20, 24, 32))
pygame.display.flip()
pygame.quit()
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The square leaves a solid trail behind it wherever it goes.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The square is invisible. There is no error, the loop is running, and the author has checked that <code>x</code> and <code>y</code> are sensible numbers. Name two possible causes.

```python
dt = clock.tick(60)
...
x += 300 * dt
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> The fan spins up and the laptop gets hot, although the game does almost nothing.

```python
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((20, 24, 32))
    pygame.display.flip()
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Install <code>pygame-ce</code> and print its version. Do not continue until this works &mdash; and if it will not, read the last section of <code>INSTALL.md</code> rather than fighting it.</li>
<li><strong>Checkpoint 2.</strong> Type the fourteen-line program from scratch, without copying. Window, loop, <code>QUIT</code>, fill, flip, quit. Close it with the window button <em>and</em> with Escape.</li>
<li><strong>Checkpoint 3.</strong> Add a <code>Clock</code>, and put <code>dt</code> and <code>clock.get_fps()</code> on screen as text. Keep that readout for the rest of the level.</li>
<li><strong>Checkpoint 4.</strong> Draw a square and move it with <code>get_pressed()</code>, multiplying by <code>dt</code>. Hold a key &mdash; it should glide, with no pause and no stutter.</li>
<li><strong>Checkpoint 5.</strong> Clamp it inside the window. Test by holding a key for several seconds against each of the four edges.</li>
<li><strong>Checkpoint 6.</strong> Add a <code>KEYDOWN</code> handler that teleports the square to the centre when space is pressed &mdash; <em>once per press</em>. Then try the same thing with <code>get_pressed()</code> and watch it fire every frame.</li>
<li><strong>Checkpoint 7.</strong> Add the four-line self-test hook from <code>INSTALL.md</code>, then run your game with <code>SDL_VIDEODRIVER=dummy SELFTEST_FRAMES=100</code> and confirm it exits by itself.</li>
<li><strong>Checkpoint 8.</strong> Add a key that drops the frame cap to 10 fps. Check your square still crosses the window in the same time. If it does not, your <code>dt</code> is wrong somewhere.</li>
</ul>

<div class="note">
<span class="note-label">If the window will not close</span>
<p>You have no <code>QUIT</code> handling. Close the terminal window, or press
Ctrl-C there &mdash; and note that Ctrl-C often will not work either, because the
program is sitting inside pygame rather than inside Python. That is worth noticing:
a program that ignores its events is genuinely hard to get rid of.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** `tkinter`'s `after()` called your function; pygame makes you write the loop.
What does each make easy, and each make awkward? Think about pausing, and about
running the game faster than real time.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Why would a library make you drain the event queue yourself rather than
doing it for you? What would it cost to do it automatically?

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** A chess program does not need sixty frames a second. Sketch a loop that
only draws when something has changed. What must it track, and what breaks about
delta time?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. `dt` can be huge — a dragged window, a sleeping laptop. A
`dt` of 2 seconds moves your square 600 px in one step, straight through anything
in the way. Give **two** different answers, and say which you would use for a
platformer and which for a card game.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Show `clock.get_fps()` and watch it while dragging the window.
2. Two squares, two control schemes, using the intent pattern.
3. A resizable window — and decide what happens to your clamping.
4. Mouse control as well as keys. Decide what happens if both are used.
5. A pause key. It is harder than it looks, and it is lesson 11's subject.
