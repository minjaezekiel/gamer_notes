# Lesson 1 — Solutions and marking notes

---

## Section A

**A1.** [3] **Input** — `pygame.event.get()` and `pygame.key.get_pressed()`. **Update** — your own
arithmetic, multiplied by `dt`. **Render** — `screen.fill`, the `pygame.draw` calls, and
`pygame.display.flip()`. One mark each.

**A2.** [3] The window stops responding: it greys out, the cursor spins, and the title bar may say "not
responding" — two marks. Because the operating system delivers events into a queue and watches whether
the program takes them; a program that never does is indistinguishable from one that has hung — one
mark.

**A3.** [3] `KEYDOWN` for firing a bullet, jumping, pausing or opening a menu. `get_pressed()` for
movement. Two marks. Swap them and you get either a gun that fires sixty times a second, or movement
that judders at the operating system's key-repeat rate — one mark.

Worth saying out loud: the second symptom is exactly the one the web track met in its third beginner
lesson. It is the same operating system behaviour, in a different language.

**A4.** [3] It **waits**, so the loop runs at most 60 times a second — and it **returns the number of
milliseconds** since the previous call. Two marks for both; the third for noticing that most people only
see the first.

**A5.** [2] `tick` returns milliseconds and all the speeds are written in pixels per second — one mark.
Forget it and everything is 1000× too fast, so the square leaves the window on the first frame and
appears never to have been drawn — one mark.

**A6.** [2] A rectangle of pixels you can draw on — one mark. The window (from `set_mode`), a sprite, a
spritesheet, or any Surface you make yourself — one mark for two examples.

**A7.** [2] So that a half-drawn frame is never visible: everything is drawn off-screen and then shown
in one go — one mark. That technique is called **double buffering**, and the beginner C++ track built one
by hand — one mark.

---

## Section B

**B1.** [3] At 60 fps: `300 / 60 = 5` px per frame. At 30 fps: `10` px per frame. Two marks. **300 px in
one second in both cases** — one mark, and that is the whole point of `dt`.

**B2.** [3] `dt` is now about 16.7 (milliseconds), so the square moves `300 × 16.7 = 5010` px in one
frame — two marks. It leaves the window immediately, so the player sees nothing at all and assumes it
was never drawn — one mark.

**B3.** [3] **Nothing** — or rather, the previous frame. Two marks. `flip()` shows what was drawn
*before* it; the `fill` and the rectangle happen afterwards, so they will not appear until the next
`flip()` — one mark. (With a loop, the effect is a one-frame delay, which is subtle. On a single pass,
the window is blank.)

**B4.** [4] Version A: the square glides smoothly for one second and travels 300 px — two marks.
Version B: it moves 5 px, pauses for about half a second, then moves in jerky 5 px steps at the key
repeat rate, ending up somewhere unpredictable that depends on the machine's keyboard settings — two
marks.

**B5.** [3] It uses `WIDTH` where it should use `WIDTH - 40` — one mark. The largest `x` allowed is
**640** — one mark — at which point the square's left edge is at the right-hand edge of the window, so
it is entirely off-screen — one mark.

---

## Section C

**C1.** [3] There is no `pygame.event.get()`, so the queue is never drained and the window is considered
unresponsive — two marks. Ctrl-C often does not help either, because the interpreter is inside pygame's
C code rather than at a point where it checks for the signal — one mark. Fix: drain the queue, and
handle `QUIT`.

**C2.** [3] There is no loop at all — two marks. The program draws one frame, reaches the end, and
exits, which closes the window. It did not crash; it finished — one mark. Several students will insist
it crashed, which is worth a moment: "finished" and "crashed" look identical from the outside.

**C3.** [3] No `screen.fill()` before drawing — two marks. Each frame is drawn on top of the last, so the
square paints rather than moves — one mark. Accept, and credit, a student who points out that this is the
*forgetting to erase* example from the beginner web track.

**C4.** [4] Two causes, two marks each. (a) `dt` is in **milliseconds** — the `/ 1000.0` is missing — so
the square is thousands of pixels away. (b) Nothing is being shown, because there is no `flip()`, or the
`flip()` comes before the drawing.

A good student will also note that "x and y are sensible" was checked *after* the move, or on the first
frame only, which is why the author believed them.

**C5.** [3] There is no `clock.tick()`, so the loop runs as fast as the processor allows — perhaps
thousands of times a second — doing nothing useful with any of it. Two marks. Fix: `clock.tick(60)` —
one mark.

---

## Section D — marking the build

1. **It was typed, not pasted** (checkpoint 2). Watch for this. The fourteen lines are the shape of
   every program in this level and typing them once is worth more than reading them ten times.
2. **Escape *and* the window button both work** (checkpoint 2). Many students do one.
3. **`dt` and the frame rate are on screen** (checkpoint 3). Ask them to keep it. It is the readout that
   answers almost every question in the next eleven lessons.
4. **Movement uses `get_pressed()`, not `KEYDOWN`** (checkpoint 4). The test is to hold the key: if it
   stutters, it is the wrong one.
5. **Checkpoint 6 was done both ways round.** Seeing "teleport once" become "teleport every frame" is
   the clearest demonstration of events versus state there is.
6. **Checkpoint 8 actually passes.** Dropping to 10 fps and still crossing the window in the same time
   is the only objective proof that their `dt` is right, and it takes ten seconds to check.

Expect the install to eat the first fifteen minutes for someone. Have `INSTALL.md` open on the projector
and triage: two different Pythons, or an externally-managed environment. Those two account for nearly
everything.

---

## Section E — marking notes

**E1.** Both designs are reasonable, and the comparison is the content.

*`after()` / callback:* the library owns the clock, so you cannot forget to cap the frame rate, and a
program that does nothing costs nothing. Awkward: you have no single place that is "the frame", so
pausing means not scheduling the next callback, and running faster than real time is close to
impossible. The order of your program is scattered across callbacks.

*An explicit `while` loop:* you can see the whole frame in one place, pause by simply not calling
update, run the loop 10,000 times with no drawing for a test, and step one frame at a time in a
debugger. Awkward: you must remember `tick`, you must drain events, and a mistake freezes the window.

Full marks for noticing that the explicit loop is what makes a **test** possible — running the game with
no window at all, which is exactly what `check_pygame.py` does. That connection is the best available
answer.

**E2.** Good answers reach one of these:

- The library cannot know *which* events you care about, or in what order you want them handled relative
  to your own update. Draining them for you would mean calling your code back — and now it is `tkinter`.
- Automatic draining would need a background thread, and that makes every piece of game state shared
  between two threads, which is a much larger problem than the one it solves.
- It keeps the loop honest: there is exactly one place where time passes.

Credit any answer that identifies the trade as "who is in control", which is the same question as E1.

**E3.** A reasonable sketch:

```python
dirty = True
while running:
    for event in pygame.event.get():
        ...
        dirty = True            # anything that changes what is on screen
    if dirty:
        draw()
        pygame.display.flip()
        dirty = False
    clock.tick(30)
```

What it must track: whether anything visible changed — and that is harder than it sounds, because an
animation, a blinking cursor or a hover highlight all count.

What breaks about delta time: `dt` becomes meaningless, because the time between *draws* is no longer
the time between *updates*. For a chess program that is fine, because nothing moves on its own. The
general rule, and the marks: **continuous motion needs a continuous loop; discrete state does not.**

Credit anyone who notices that every desktop application works this way and that games are the unusual
case.

**E4.** Two answers, and the choice is the interesting part.

**(a) Clamp `dt`.** `dt = min(dt, 0.05)`. Simple, and it means a slow frame makes the game run in slow
motion rather than teleporting. Everything stays correct and nothing is skipped.

**(b) Divide the frame into fixed steps** — run the update several times with a small `dt` until the
time is used up. More code, and nothing is ever moved a large distance in one go, so collisions cannot
be missed.

Which for which:

- a **platformer** wants (b), or (a) with a tight clamp, because moving 600 px in one step means passing
  straight through a floor. This is the fixed timestep, and it is the advanced level's first lesson.
- a **card game** can ignore the problem entirely, or use (a) with a generous clamp. Nothing moves fast
  enough for a large step to break anything.

Full marks need a stated reason tied to *what could be skipped over*. Students who answer "always use
(b) because it is more correct" should be asked what it costs — and the answer is complexity they do not
yet need.

---

## If you only mark one thing

Checkpoint 8: drop the frame cap to 10 fps and check the square still crosses the window in the same
time. It is a ten-second test, it is objective, and a student who passes it has understood the one idea
that every remaining lesson in this level depends on.
