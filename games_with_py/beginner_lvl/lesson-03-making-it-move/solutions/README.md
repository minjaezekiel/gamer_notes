# Lesson 3 — Solutions and marking notes

---

## Section A

**A1.** [3] Lesson 1's loop **stopped and waited** at `input()`; nothing happened until the player
typed. Lesson 3's loop **never waits** — it runs about 60 times a second whether or not anything is
pressed, so enemies can move, timers can run and things can fall. Two marks for the distinction, one
for noting that the three jobs are otherwise unchanged.

**A2.** [2] "Call `game_loop` again after 16 milliseconds." It is Python's equivalent of JavaScript's
`requestAnimationFrame`.

**A3.** [2] The handler only runs as often as the operating system repeats a held key — one press,
a pause of about half a second, then a slow repeat — because key repeat was designed for typing.

**A4.** [3] One mark each:

| Missing | Symptom |
|---|---|
| `screen.listen()` | no key does anything at all |
| `drawer.clear()` | the player smears across the screen |
| `screen.onkeyrelease` | the player never stops moving |

(Accept `screen.mainloop()` → "the window never opens or closes instantly".)

**A5.** [2] A key nobody has pressed is **not in the dictionary at all**, so `keys["Right"]` raises
`KeyError`. `.get()` returns `None` instead, which an `if` treats as false.

---

## Section B

**B1.** [4] All four handlers are `lambda`s that share **one** `name` variable. By the time anybody
presses a key the loop has finished and `name` holds its last value, `"Right"`. So every arrow key
sets `keys["Right"] = True`.

It is called the **closure trap** (accept "late binding"). Two marks for the mechanism, one for the
name, one for noting there is no error message.

The fix is either the `press(name)` factory from the notes, or a default argument:
`lambda n=name: keys.update({n: True})`, which captures the value at creation time.

**B2.** [3] 16 ms per frame is about 62.5 frames per second, so roughly 60. `5 × 60 = **300 pixels
per second**`. At 30 fps it becomes `5 × 30 = **150 pixels per second**` — the game runs at **half
speed**. Two marks for 300, one for the halving.

**B3.** [4] Moving 5 across and 5 up means the real distance is
`√(5² + 5²) = √50 ≈ **7.07 pixels**`.
That is `7.07 / 5 ≈ 1.41`, so about **41% faster**. Two marks for the working, one for 7.07, one for
41%.

**B4.** [3] One single frame is drawn and then everything stops. The player appears and no key has
any effect, because `update()` is never called again. The `ontimer` line is what asks for the *next*
frame; without it `game_loop` runs once and returns.

Note that the program has not crashed — it has simply finished its work.

---

## Section C

**C1.** [3] `screen.listen()` is missing. Without it the turtle window never starts watching the
keyboard, so no handler is ever called. There is no error, which is what makes it so frustrating.

Insist students learn to check this **first**.

**C2.** [3] `drawer.clear()` is missing from the start of `draw()`. Turtle does not clean the screen
for you, so every frame's circle is added on top of all the previous ones.

(Worth mentioning: this is how you would deliberately make a trail effect — the same code is a bug or
a feature depending on what you wanted.)

**C3.** [4] Two marks for the explanation: `keys` starts empty, so before any key has been pressed
there is no `"Right"` entry, and `keys["Right"]` raises `KeyError` immediately.

Two marks for any two fixes:
1. `keys.get("Right")` — returns `None` instead of raising.
2. Pre-fill the dictionary: `keys = {"Right": False, "Left": False, ...}`.
3. `"Right" in keys and keys["Right"]`.
4. Use `collections.defaultdict(bool)`.

Option 1 is the idiomatic Python answer and the one the lesson uses.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 1.** The frame counter is worth insisting on: it proves the loop is running *before*
they add anything that could be blamed for not working. Debugging is far easier when you have
established what already works.

**Checkpoint 2.** Same idea — displaying the held keys gives them a tool that makes the two most
common bugs (no `listen`, no `onkeyrelease`) immediately visible rather than mysterious.

**Checkpoint 3.** Watch for anyone who left the movement in the handler. It is audible from across
the room: their player stutters.

**Checkpoint 5.** `update()` should read `if wants_right:` with no key names in it. A student writing
`if keys.get("Right") or keys.get("d"):` inline has the right behaviour but missed the idea; ask what
they would do to add a gamepad.

**Checkpoint 6 — the chaser.** Three lines:

```python
if enemy_x < player_x: enemy_x += ENEMY_SPEED
if enemy_x > player_x: enemy_x -= ENEMY_SPEED
# and the same for y
```

Students are genuinely delighted by this, and it is worth pausing to point out that they have just
written enemy AI, that it took three lines, and that a great many commercial games do not do anything
much cleverer.

---

## Section E — marking notes, not answers

**E1.** Three real approaches:

1. **Normalise.** Work out the length of the movement and scale it back to `SPEED`. The general and
   correct answer; it is what vectors are for, and it arrives properly at intermediate level.
2. **Divide by √2** when both axes are active. Simple, works for exactly eight directions, and breaks
   the moment you add analogue input.
3. **Only allow one direction at a time** — the most recent key wins. Not a fix so much as a design
   decision, and it is what many grid-based games (including Snake, next lesson) actually do.

Full marks for three plausible approaches with a justified choice. Option 3 is worth praising,
because "change the design so the problem cannot arise" is a legitimate engineering move that
students rarely consider.

**E2.** The cursor should stop instantly: it is a pointer, and any lag feels broken. The car should
not: it has mass, and instant stopping destroys the sense of weight. The spaceship is the interesting
one — in space there is no friction at all, so a *realistic* spaceship would never stop, which most
players find horrible to control. Nearly every space game therefore adds fake friction.

The principle worth drawing out: **smoothing communicates weight; instant response communicates
precision.** Choose according to what the game is about, not according to physics.

**E3.** If the work takes 20 ms, the game cannot run at 60 fps. Depending on the implementation,
`ontimer(16)` either schedules from the *end* of the work (giving roughly 36 ms per frame, about
28 fps) or tries to keep to 16 ms and falls behind. Either way the answer is **not** 60.

What to measure: record `time.time()` at the top of each frame and print the difference — exactly
what `04-delta-time.py` does. The broader point is the valuable one: **do not guess at performance,
measure it.** Students who say "I would time it" have the right instinct even without the details.

**E4.** Looking for five things that do not depend on the player: enemies moving and chasing; a
countdown timer; animations playing; projectiles travelling; particles fading; items respawning;
music; day turning to night; the score ticking up; an enemy spawner.

The point to land: **none of these were possible in lesson 1**, because the program spent its entire
life sitting inside `input()` waiting. One change — a loop that does not wait — made an entire
category of game possible. That is why this lesson is the hinge of the whole track.

---

## Teacher note: the closure trap

Budget ten minutes for B1, because it is genuinely hard and students will hit it.

On the board, draw one box labelled `name` with four arrows pointing at it from four handler
functions. Then run the loop, updating the box: `"Up"`, `"Down"`, `"Left"`, `"Right"`. Now press a
key — all four arrows read the same box, which says `"Right"`.

Then show `press(name)`: each call creates its *own* box, so each handler reads a different one.

This is worth doing properly rather than telling them to copy the pattern. It is one of the few
genuinely subtle things in the beginner course, professionals get caught by it regularly, and
understanding it is the difference between copying code and being able to write it.
