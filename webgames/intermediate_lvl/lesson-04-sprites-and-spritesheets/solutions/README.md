# Lesson 4 — Solutions and marking notes

---

## Section A

**A1.** [3] One request instead of thirty, so loading is faster · the graphics card never has to switch
image, which is slow compared with drawing · one file to name, find and keep track of. One mark each.

**A2.** [2] `sx, sy, sw, sh` describe the **image** (which piece to copy). `dx, dy, dw, dh` describe the
**canvas** (where to put it, and how big). One mark each.

**A3.** [3] Any two problems, two marks: the animation runs at the frame rate rather than at a chosen
speed, so it is far too fast (60 poses a second instead of 8); and that speed then differs between
machines, so the same code looks different on a 144 Hz monitor. Third mark for the general point: the
game's clock and the animation's clock are separate concerns and should be separate variables.

**A4.** [2] Because a slow frame may have taken long enough for more than one pose to be due. `if`
advances only one and silently drops the rest, so the animation slows down exactly when the computer is
already struggling.

**A5.** [2] It wraps the counter back to 0 after the last frame — one mark — saving an `if (frame >=
FRAMES) frame = 0`, and continuing to work when the number of frames changes — one mark.

**A6.** [3] Because what is drawn should follow what the character is *doing*, not what the hardware is
doing. Two marks. Practical benefit, one mark: adding a new animation is one line in the table and one
condition; the input code, the physics and the drawing code are untouched. Accept also: the same
animation code then works for enemies, which have no keyboard at all — a particularly good answer.

**A7.** [2] Rounding when drawing keeps the sprite on whole pixels, so it stays sharp — one mark.
*Not* rounding the stored position keeps the movement smooth; rounding the real position makes slow
movement stutter, because small sub-pixel steps get thrown away every frame — one mark.

---

## Section B

**B1.** [3] `sx = 4 × 32 = 128`, `sy = 2 × 32 = 64`. Two marks. Sheet is `192 × 96` — one mark.

**B2.** [3] `60 / 8 = 7.5` game frames per pose — so it alternates between 7 and 8, which is fine. Two
marks. 16 poses in two seconds — one mark.

**B3.** [4] The **whole sheet** is drawn, squashed into a 32×32 box at (100, 100). Two marks. Because
the four-argument form means "the whole image, stretched to this size" — the numbers are read as
destination, not source — two marks.

This is the single most common bug in the lesson, and a student who can explain it will not make it.

**B4.** [3] `frame` becomes 6, so `sx = 6 × 32 = 192`, which is past the right-hand edge of a 192-wide
sheet. Two marks. **Nothing is drawn** — the source rectangle is entirely outside the image, which is
not an error, just empty — one mark. Many students expect a crash; the silence is the point.

**B5.** [4] The timer is zeroed after reaching 0.125, so the leftover is thrown away. Steps of 0.01667
reach 0.125 after 8 steps (0.1333), so each pose actually lasts `8 × 0.01667 = 0.1333 s` instead of
0.125 s. Two marks. That is about 6.7% slow, so after 60 seconds the animation is roughly **4 seconds**
behind — two marks.

Accept answers between 3.5 and 4.5 seconds. The number matters less than the method.

---

## Section C

**C1.** [3] The image has not finished loading when `drawImage` runs. Setting `src` starts a download; it
does not wait for one. Two marks. Prove it either by drawing inside `img.onload`, or by logging
`img.complete` just before the draw — one mark. Credit anyone who notes that this draws nothing *and*
reports no error, which is why it is confusing.

**C2.** [3] The reset runs on every frame the character is walking, not on the frame they *started*
walking, so `frame` is set back to 0 before the timer can ever advance it. Two marks. Fix: compare with
the previous state — `if (state !== lastState) { frame = 0; timer = 0; lastState = state; }` — one mark.

**C3.** [4] `scale(-1, 1)` mirrors about **x = 0**, the canvas's left edge, so a sprite at x = 300 is
drawn at x = −300 — off the screen entirely. Two marks. Fix: move the origin to the sprite first, mirror,
then move back:

```js
ctx.translate(x, y);
ctx.scale(-1, 1);
ctx.translate(-x, -y);
```

Two marks. Accept the equivalent version that translates once and draws at a negated offset
(`drawImage(..., -FW, 0, ...)`), which is what a professional would write — give full marks and ask them
to explain it to the class.

**C4.** [3] The position is fractional. Standing still, `x` happens to be a whole number; walking
slowly, it is something like 40.3, and the browser samples between pixels. Two marks. Fix:
`Math.round` at draw time only — one mark.

**C5.** [4] Two bugs. (a) The timer counts **frames**, not **seconds** — `timer += 1` instead of
`timer += dt` — so the pose speed is tied to the frame rate, and a slow laptop gives a slow animation.
Two marks. (b) There is no `% FRAMES`, so the frame index will eventually run off the end of the sheet
and draw nothing — two marks.

Credit anyone who also spots `timer = 0` as a third, smaller fault (the drift from B5).

---

## Section D — marking the build

1. **Checkpoint 1 was really done in code.** The point is that an offscreen canvas is an image; a student
   who drew the figures straight to the visible canvas has missed it.
2. **The nine-argument form is used.** Grep for `drawImage` — if the call has four arguments and the
   whole sheet is on screen, that is checkpoint 2 incomplete.
3. **The pose number and timer are on screen** (checkpoint 3). Insist on this. Everyone who skips it
   spends twenty minutes guessing.
4. **`state !== lastState`, not `state === "walk"`** (checkpoint 4). This is C2 in their own code, and
   roughly half the class will write the broken version first.
5. **Checkpoint 7 exists.** Having the broken version available on a key is worth more than it looks: it
   turns a fixed bug into a permanent demonstration.

Expect checkpoint 5 to take the longest. Canvas transforms are the first genuinely confusing graphics
idea most of them meet. The thing to say out loud, more than once: *you are moving the paper, not the
pen.*

---

## Section E — marking notes

**E1.** All three anchors are used in real games, and the strongest answer is **the middle of the feet**
for a platform game.

- *Top-left* — simplest arithmetic, matches `drawImage`, and everything breaks subtly when a sprite's
  height changes: the character appears to sink into the floor.
- *Centre* — convenient for rotation and for circular collision; awkward for standing on things.
- *Feet* — the floor test is `pos.y` exactly, and a taller sprite grows upwards, which is what a bigger
  character should do.

Credit anyone who separates the **drawing anchor** from the **collision box**, and notes they do not have
to be the same point. Full marks require naming a cost: the feet anchor makes the draw call's arithmetic
less obvious (`y - FRAME_H`), and it is easy to forget the offset.

**E2.** The mechanism is to make `FRAME_TIME` depend on speed:

```js
const framesPerSecond = BASE_FPS * (Math.abs(vel.x) / BASE_SPEED);
const FRAME_TIME = 1 / Math.max(1, framesPerSecond);
```

What breaks if it is tied too tightly, and this is the half worth most credit:

- a character being **pushed** or carried on a platform has speed but is not walking, so their legs
  windmill;
- at very low speed the frame time goes to infinity and the animation freezes mid-step, which looks
  broken rather than still;
- in the air, horizontal speed has nothing to do with legs at all.

The usual fix is to clamp the range and only apply it in the walk state. Credit the clamp.

**E3.** Two defensible designs, and the question is really about interruption:

- **A separate state** that interrupts: simple, and the character stops walking for a moment, which may
  be exactly right (a flinch) or wrong (in a fast platformer).
- **A layer on top** — keep the walk animation and flash the sprite red, or draw a hurt overlay. The
  character keeps control; good for action games where losing control feels unfair.

The part most students miss, and the part worth the marks: **being hurt twice in quick succession.**
Either the timer restarts (so continuous damage freezes them for ever — a real bug in real games), or
there is an invulnerability window, which is why nearly every platform game has one. A student who
discovers invulnerability frames by reasoning about this has done well.

**E4.** All three are used in shipped games.

- **Two sheets** — simplest, no runtime cost, and doubles the memory and the download. Fine for two
  teams, hopeless for twelve.
- **Recolour at load time** — one sheet shipped, N sheets in memory, a few milliseconds at startup. Needs
  a palette or a known shirt colour, and goes wrong if the art uses that colour anywhere else.
- **Separate shirt layer** — one extra `drawImage` per character per frame and total flexibility; the art
  has to be drawn in layers from the start, which constrains the artist.

Full marks need a stated trigger for changing their mind. Good ones: "if we go past four teams I would
switch from shipping sheets to recolouring"; "if the profiler shows the second draw call costing us, I
would bake them". Reasoning about *when* a decision stops being right is the actual skill.

---

## If you only mark one thing

Checkpoint 3 with the pose number and timer visible on screen. Every subsequent problem in this lesson
becomes a five-second diagnosis with those two numbers showing, and a guessing game without them.
