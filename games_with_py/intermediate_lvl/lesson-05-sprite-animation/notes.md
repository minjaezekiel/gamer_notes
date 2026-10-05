# Lesson 5 — Sprite Animation

> **Games with Python · Intermediate level · Lesson 5 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A character that **walks**: legs moving, facing the way they are going, standing still when you stop,
and a separate pose while jumping. The spritesheet will be generated in code, so there is nothing to
download and every pose is a number you can change.

```
   the sheet: ONE Surface                     self.image, 8 times a second
   ┌────┬────┬────┬────┬────┬────┐
   │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │  idle            ███
   ├────┼────┼────┼────┼────┼────┤                 ██ ██
   │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │  walk    →       ███
   ├────┼────┼────┼────┼────┼────┤                 ██ ██
   │ 0  │                        │  jump           ╱   ╲
   └────┴────┴────┴────┴────┴────┘
```

Lesson 4 said a Sprite has an `image`. Today that `image` **changes over time**, and the whole lesson
is about *which clock decides when*.

## Where this fits

- **Back:** [lesson 2](../lesson-02-rects-images-and-the-display/notes.md) made Surfaces and blitted
  parts of them; [lesson 4](../lesson-04-sprites-and-groups/notes.md) made `self.image` a requirement.
- **Forward:** lesson 9 *(not yet written)* gives this character gravity and a
  jump, and the animation states are already waiting for it.
- **Other tracks:** `webgames` intermediate lesson 4 is this lesson with `drawImage` instead of
  `subsurface`. The two clocks are the same two clocks.

---

## The idea, in plain words

### A walking character is one Surface and a moving rectangle

The instinct is one file per pose. Real games do not, because loading thirty files is thirty waits, and
because switching image is slow compared with drawing. So the poses go side by side in **one** Surface,
and "which pose?" becomes "which rectangle of it?".

In pygame there are two ways to take a piece, and the difference is worth knowing:

```python
# 1. blit with a source rectangle: copy those pixels, now, onto the screen
screen.blit(sheet, (x, y), pygame.Rect(col * W, row * H, W, H))

# 2. subsurface: a Surface that SHARES the sheet's pixels. No copying at all.
frame = sheet.subsurface(pygame.Rect(col * W, row * H, W, H))
```

`subsurface` is the one you want for a Sprite, because `self.image` has to *be* a Surface. It is also
free — nothing is copied, it is a window onto the sheet.

Two things it will do to you:

- **The sheet must stay alive.** A subsurface holding a reference to a sheet you have thrown away is
  fine (Python keeps it), but a subsurface of a Surface you later draw over will change.
- **You cannot blit a subsurface onto its own parent.** pygame refuses, because the pixels would be
  both source and destination.

If either of those matters, use `.copy()` and accept the memory.

### Slice the sheet **once**, at load time

```python
def slice_sheet(sheet, frame_width, frame_height):
    """One list per row. Done once, at startup - never in the loop."""
    rows = []
    for row in range(sheet.get_height() // frame_height):
        frames = []
        for col in range(sheet.get_width() // frame_width):
            rect = pygame.Rect(col * frame_width, row * frame_height,
                               frame_width, frame_height)
            frames.append(sheet.subsurface(rect))
        rows.append(frames)
    return rows
```

Now an animation is a **list of Surfaces** and `self.image = frames[self.frame]`. That is the whole
drawing side of this lesson; everything else is about time.

### The two clocks

Your game runs at 60 frames a second. A walk cycle should run at about 8 poses a second. Advance one
pose per game frame — which is what nearly everybody writes first — and the character vibrates rather
than walks, at a speed nobody chose.

```python
FRAME_TIME = 1 / 8          # hold each pose for an eighth of a second

self.timer += dt
while self.timer >= FRAME_TIME:
    self.timer -= FRAME_TIME                    # SUBTRACT, do not zero
    self.frame = (self.frame + 1) % len(self.frames)
self.image = self.frames[self.frame]
```

Three details, all load-bearing:

- **`while`, not `if`.** A slow frame may owe you two poses. `if` silently drops them, so the animation
  runs slow exactly when the machine is struggling.
- **Subtract, do not zero.** `self.timer = 0` throws the leftover away, and the animation drifts a few
  per cent slow — invisible for ten seconds, obvious after a minute.
- **`% len(self.frames)`** wraps without an `if`, and keeps working when you change the number of poses.

### Let the state choose the animation

Do not write "when the right arrow is pressed, play the walk animation". Write:

```python
# 1. the game decides what the character is DOING. No pictures here.
if not self.on_ground:
    self.state = "jump"
elif abs(self.velocity.x) > 10:
    self.state = "walk"
else:
    self.state = "idle"

# 2. the state picks an animation. This is the ONLY place that knows about rows.
ANIMATIONS = {
    "idle": {"row": 0, "fps": 2},
    "walk": {"row": 1, "fps": 8},
    "jump": {"row": 2, "fps": 1},
}

# 3. a CHANGE of state restarts the animation
if self.state != self.last_state:
    self.frame = 0
    self.timer = 0.0
    self.last_state = self.state
```

That third block is the one people get wrong, and the bug is subtle: writing
`if self.state == "walk": self.frame = 0` resets the frame on **every** frame they are walking, so the
animation never gets past pose 0. The test is for the state having *changed*, not for what it *is*.

The payoff: adding a "hurt" animation is one line in `ANIMATIONS` and one condition in step 1. Your
input code, your physics and your drawing are untouched.

### Facing the other way, for free

You do not draw a left-facing walk. You flip the right-facing one — **once, at startup**:

```python
self.frames_right = slice_sheet(sheet, W, H)
self.frames_left = [[pygame.transform.flip(f, True, False) for f in row]
                    for row in self.frames_right]
```

`pygame.transform.flip` makes a **new Surface** every call, so doing it per frame is one of the easiest
ways to make a pygame game slow for no reason. Build both sets once; choosing between them at draw time
is a list lookup.

### The anchor: where a sprite is drawn *from*

A `Rect` has nine named positions, and which one you treat as "the character's position" matters more
than it sounds. For something that stands on the ground, use **`midbottom`**:

```python
self.rect = self.image.get_rect(midbottom=self.pos)
```

Then "standing on the floor" is `self.rect.bottom = floor_y`, and when a pose is taller than the others
— a jump, a stretch — the character grows **upwards** instead of sinking into the ground. Anchor at the
top-left and every change of pose moves their feet.

And because the frames in a sheet are all the same size, re-anchoring on each new `image` keeps
everything lined up:

```python
self.image = frames[self.frame]
self.rect = self.image.get_rect(midbottom=self.rect.midbottom)   # keep the feet
```

### Tying the animation to speed

Walking on the spot at 8 poses a second looks right at one speed and wrong at every other. The fix is
one line:

```python
speed_factor = abs(self.velocity.x) / WALK_SPEED
fps = BASE_FPS * max(0.4, min(2.0, speed_factor))
```

Clamp it. Without the clamp, standing still gives an fps of zero and a frame time of infinity, and the
character freezes mid-step — which looks broken rather than still. Lesson 9 needs this, because a
platformer character is pushed, carried and slowed constantly.

---

## The idea, in pictures

Open [the spritesheet explainer](../../../shared/visualizers/sprite-animation.html).

**What to look for:** two clocks, and they are not the same clock. Press **Step 1 frame** repeatedly:
the game frame counter rises every press, but the pose only changes when the timer bar fills. Several
game frames per pose is *correct*. Then switch on "advance every game frame" and watch the character
vibrate — that is the bug this lesson exists to prevent, and it is the first thing almost everybody
writes.

---

## The idea, in code

1. `code/01-make-a-spritesheet.py` — build a three-row sheet in code and look at it magnified, with the
   grid and the cell numbers drawn on.
2. `code/02-slicing-and-timing.py` — `subsurface` versus `blit` with a source rect, then the frame
   timer, with switches for the one-pose-per-frame bug and for `timer = 0` so you can watch the drift.
3. `code/03-state-driven.py` — `ANIMATIONS` as a table, the state machine, the `!=` versus `==` bug, and
   flipping done once.
4. `code/04-a-walking-character.py` — the lesson assembled: move, jump, animate, face the right way,
   anchored at the feet, with both clocks on screen.

---

## The maths you just used

**1. Modulo as a wrap.** `(frame + 1) % count` counts 0, 1, 2, …, count−1, 0, … with no `if`. You met
`%` in the beginner C++ track for turning a flat index back into a grid position; here it makes a loop
with no end.

**2. Where a cell starts.** `col * frame_width` — because every cell is the same width. Most of graphics
programming is arithmetic this ordinary, and noticing that is worth more than the formula.

**3. An accumulator.** `timer += dt`, then spend it in whole poses. This is the same shape as delta time
itself, and the advanced level's fixed timestep is the same shape again. Three appearances of one idea:
*collect a continuous quantity, spend it in discrete units, keep the remainder.*

**4. Clamping a ratio.** `max(0.4, min(2.0, speed / WALK_SPEED))` keeps the speed-matched animation
sensible at both ends. The lower clamp is not tidiness — without it a stationary character divides by
zero and freezes mid-stride.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Advance the pose once per game frame | | |
| Change `while self.timer >= FRAME_TIME` to `if`, then drop the frame cap to 15 | | |
| Replace `self.timer -= FRAME_TIME` with `self.timer = 0` and run for a minute | | |
| Remove `% len(self.frames)` | | |
| Reset the frame with `if state == "walk"` instead of `if state != last_state` | | |
| Call `pygame.transform.flip` every frame instead of once | | |
| Anchor the rect at `topleft` and switch to a taller jump pose | | |
| Remove the lower clamp from the speed-matched fps and stand still | | |

The `timer = 0` one needs patience and is worth it: the animation looks perfectly fine, and over a
minute it falls several seconds behind where it should be. Some bugs are only visible if you wait.

---

## Think like an engineer

1. `subsurface` shares pixels; `.copy()` does not. Name a situation where sharing is exactly what you
   want, and one where it would cause a bug that is very hard to find.
2. The animation table lives in the Sprite class. Where else could it live — a separate module, a JSON
   file, a dictionary passed in? What does each make easy, and which would you choose if an artist who
   does not program needed to change the frame rates?
3. **Design something.** An attack animation that **interrupts** walking, plays once, and then returns to
   whatever the character was doing. What does the state machine need that it does not have now? What
   happens if the player attacks again halfway through?
4. **The hard one.** Your character's feet slide: they move 200 px/s but the legs cycle at a fixed 8
   poses a second. Tying the animation to speed fixes walking — and then breaks when the character is
   carried by a moving platform, pushed by an explosion, or walking into a wall. Describe what "speed"
   should actually mean here, and how you would get it.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Spritesheet** | One Surface holding many poses in a grid. |
| **`subsurface`** | A Surface that shares another's pixels. Free; the parent must stay valid. |
| **Source rectangle** | Which part of the sheet to use. |
| **Frame timer** | The accumulator that decides when the next pose is due. |
| **Animation table** | A dictionary from state name to row and frame rate. |
| **Anchor** | Which point of the rect the position refers to. `midbottom` for things that stand. |
| **`transform.flip`** | Mirrors a Surface. Makes a new one, so do it once. |
| **Speed-matched animation** | Frame rate proportional to how fast the character is moving. |

---

## Recap

- One Surface, a grid of poses, and a rectangle that moves along it.
- **Slice once, at load time**, into lists of Surfaces. `subsurface` is free; it shares pixels.
- The game clock and the animation clock are **different clocks**. Use `while`, and **subtract** rather
  than zeroing.
- Let the **state** choose the animation, and reset the frame when the state **changes** — `!=`, not `==`.
- **Flip once at startup.** `transform.flip` makes a new Surface every call.
- Anchor at **`midbottom`** for anything that stands on the ground.
- Speed-matched animation needs a **clamp at both ends**, or a stationary character freezes mid-step.

---

## Stretch goals

1. **A ping-pong animation**: 0, 1, 2, 3, 2, 1 rather than looping. `%` alone cannot do it.
2. **Recolour the sheet** at load time into two team colours, using `pygame.PixelArray` or a
   `BLEND_RGBA_MULT` blit. One drawing, two teams.
3. **An animation event**: call a function when a specific pose is reached — a footstep sound on poses 0
   and 3, say. This is how footsteps are done properly, and it is the right answer to lesson 8's E3.
4. **Onion skin.** Draw the previous two poses faintly behind the current one. Animators use this, and it
   makes a bad walk cycle obvious immediately.
5. **Load a real spritesheet**, if you have one, and write the slicing code for *its* layout. Discovering
   that the cells are not quite evenly spaced is a genuine and common experience.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `02-slicing-and-timing.py` with the one-pose-per-frame switch on. The vibrating character gets a laugh. Ask what is wrong: most will say "too fast", which is nearly right and not quite. |
| 10–25 | **Concept.** The spritesheet visualizer, entirely on the two clocks. Step it, and ask for a prediction before each press. |
| 25–40 | **Live-code** the frame timer. Four lines, each with a reason. Then `slice_sheet` with them. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–4 are the core. |
| 120–140 | Break-it-on-purpose. The `timer = 0` drift needs a stopwatch and is worth it. |
| 140–150 | Recap. Lesson 6 builds the world this character will walk around. |

**What usually goes wrong**

1. **The character vibrates.** One pose per game frame. This *is* the lesson, so let it happen first.
2. **The animation never leaves pose 0.** `if state == "walk": frame = 0` rather than `!=`. Extremely
   common, and the fix is one character.
3. **`ValueError: subsurface rectangle outside surface area`.** The frame index ran past the end of the
   row, or the sheet is not an exact multiple of the cell size. The message is unusually clear; point
   that out.
4. **The sprite sinks into the floor** when a taller pose appears. Anchored at `topleft`.
5. **The game is slow with six characters.** `transform.flip` or `subsurface` being called every frame.
6. **The character freezes mid-step** when standing still. Speed-matched fps with no lower clamp.
7. **`self.rect` stops matching `self.image`** after a pose change, so collision is a few pixels out.
   Re-anchor when the image changes.

**If you are running short on time** — cut speed-matched animation and the flipping; a character that
always faces right and walks at a fixed 8 fps is fine for one lesson. Do **not** cut the frame timer or
the state table: lesson 9 assumes both.

**For the student who finishes at minute 90** — stretch goal 3 (an animation event) is the most useful,
because it connects back to lesson 8's footsteps question and forward to lesson 9. Stretch goal 4 is good
for anyone who draws.

**The point to land at the end:** the drawing was a list lookup. Everything else today was about *time* —
keeping the animation's clock separate from the game's, and letting the character's state rather than the
keyboard decide what is shown. That split is why adding a new animation later costs two lines.
