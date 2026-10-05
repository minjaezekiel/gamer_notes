# Lesson 5 — Sprite Animation

## Cheat sheet

### Slice once, at load time

```python
def slice_sheet(sheet, w, h):
    rows = []
    for row in range(sheet.get_height() // h):
        frames = [sheet.subsurface(pygame.Rect(c*w, row*h, w, h))
                  for c in range(sheet.get_width() // w)]
        rows.append(frames)
    return rows
```

`subsurface` **shares** pixels — free, no copy. The parent must stay valid, and
you cannot blit a subsurface onto its own parent. Use `.copy()` if that matters.

### The frame timer

```python
self.timer += dt
while self.timer >= FRAME_TIME:
    self.timer -= FRAME_TIME        # SUBTRACT, not = 0
    self.frame = (self.frame + 1) % len(self.frames)
self.image = self.frames[self.frame]
```

- **`while`** — a slow frame may owe you two poses
- **subtract** — zeroing loses the leftover and drifts slow
- **`%`** — wraps with no `if`, and survives changing the frame count

### State chooses the animation

```python
ANIMATIONS = {"idle": {"row": 0, "fps": 2},
              "walk": {"row": 1, "fps": 8},
              "jump": {"row": 2, "fps": 1}}

if self.state != self.last_state:    # != not ==
    self.frame = 0
    self.timer = 0.0
    self.last_state = self.state
```

`if state == "walk": frame = 0` resets **every frame** and the animation never
leaves pose 0.

### Flip once

```python
self.left = [[pygame.transform.flip(f, True, False)
              for f in row] for row in self.right]
```

### Anchor at the feet

```python
self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
```

So a taller pose grows **upwards** instead of sinking into the floor.

### Speed-matched fps — clamp both ends

```python
fps = BASE * max(0.4, min(2.0, speed / WALK_SPEED))
```

No lower clamp → standing still freezes the character mid-stride.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Give two reasons a game puts many poses in one Surface instead of one file per pose.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> What does <code>subsurface</code> do that <code>blit</code> with a source rect does not? Name one thing it will not let you do.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why <code>while</code> rather than <code>if</code> in the frame timer, and when does the difference show?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why subtract <code>FRAME_TIME</code> rather than setting the timer to 0?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why test <code>state != last_state</code> rather than <code>state == "walk"</code>? What is the symptom of the wrong one?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why anchor a standing character at <code>midbottom</code> rather than <code>topleft</code>?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> Why must a speed-matched frame rate be clamped at the <em>low</em> end?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> A sheet is 192 &times; 96 with 32 &times; 32 cells. How many columns and rows? What rect does <code>slice_sheet</code> use for row 2, column 4?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The game runs at 60 fps and <code>FRAME_TIME</code> is <code>1/8</code>. How many game frames pass per pose? How many poses in three seconds?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> <code>FRAME_TIME</code> is 0.125 s and <code>dt</code> is 0.01667. The author wrote <code>timer = 0</code>. How long is each pose actually held for, and how far behind is the animation after one minute?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> A row has 6 frames and the <code>%</code> has been removed. What happens on the seventh advance, and what is the error message?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> <code>WALK_SPEED</code> is 200 and the clamp is <code>max(0.4, min(2.0, speed / WALK_SPEED))</code>. Give the factor at speeds 0, 80, 200 and 600.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The character vibrates instead of walking, and it is worse on a faster computer.

```python
def update(self, dt):
    self.frame = (self.frame + 1) % len(self.frames)
    self.image = self.frames[self.frame]
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> However long the player walks, the character stays on pose 0.

```python
if self.state == "walk":
    self.frame = 0
    self.timer = 0.0
self.timer += dt
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> <code>ValueError: subsurface rectangle outside surface area</code>, but only sometimes.

```python
FRAME_W, FRAME_H = 32, 32
sheet = pygame.Surface((190, 96), pygame.SRCALPHA)
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The character sinks into the floor whenever they jump, and pops back up on landing. The jump pose is 6 pixels taller than the walk poses.

```python
self.image = frames[self.frame]
self.rect = self.image.get_rect(topleft=self.rect.topleft)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> With six animated characters the frame rate drops to 20.

```python
def update(self, dt):
    ...
    image = self.frames[self.frame]
    if self.facing < 0:
        image = pygame.transform.flip(image, True, False)
    self.image = image
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Write <code>make_sheet()</code> that draws three rows &mdash; idle, walk, jump &mdash; onto one Surface. Display it magnified with a grid so you can see the cells.</li>
<li><strong>Checkpoint 2.</strong> Write <code>slice_sheet()</code> and print the number of rows and frames. Draw one frame on its own and step through them with two keys, by hand.</li>
<li><strong>Checkpoint 3.</strong> Add the frame timer. Put the pose number, the timer and the game frame count on screen &mdash; and keep that readout for the rest of the lesson.</li>
<li><strong>Checkpoint 4.</strong> Add an <code>ANIMATIONS</code> table and a state machine. Make the state change reset the frame, and deliberately write the <code>==</code> version first so you see what it does.</li>
<li><strong>Checkpoint 5.</strong> Flip the frames once at startup and face the way you are moving. Stop moving &mdash; you should keep facing the way you last went.</li>
<li><strong>Checkpoint 6.</strong> Anchor at <code>midbottom</code>. Make the jump pose 8 pixels taller and confirm the feet stay put.</li>
<li><strong>Checkpoint 7.</strong> Tie the walk's frame rate to the actual speed, with both clamps. Then remove the lower clamp and stand still.</li>
<li><strong>Checkpoint 8.</strong> Add a switch that advances one pose per game frame, so you can show somebody the difference. Keep it.</li>
</ul>

<div class="note">
<span class="note-label">If a pose looks wrong</span>
<p>Draw the whole sheet in the corner of the screen with a box around the current
cell. Nearly every animation bug is visible in one glance that way, and invisible
in the code.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** `subsurface` shares pixels; `.copy()` does not. Name a case where sharing
is exactly right, and one where it would cause a very hard bug.

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** Where should the animation table live — in the class, a separate module, a
JSON file, or passed in? What does each make easy, and which would you choose if a
non-programmer needed to change the frame rates?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design an attack animation that **interrupts** walking, plays once, and
returns to whatever was happening. What does the state machine need that it has
not got? What if the player attacks again halfway through?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. Tying the animation to speed fixes sliding feet — and breaks
when the character is carried by a moving platform, pushed by an explosion, or
walking into a wall. What should "speed" actually mean here, and how would you get
it?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. A ping-pong animation: 0,1,2,3,2,1. `%` alone cannot do it.
2. Recolour the sheet at load time into two team colours.
3. An animation **event**: a footstep sound on poses 0 and 3. This is lesson 8's
   footsteps question, answered properly.
4. Onion skin: the previous two poses, faint, behind the current one.
5. Slice a real spritesheet whose cells are not quite evenly spaced.
