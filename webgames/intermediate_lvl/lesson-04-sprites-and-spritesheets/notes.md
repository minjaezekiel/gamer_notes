# Lesson 4 — Sprites And Spritesheets

> **Web Games · Intermediate level · Lesson 4 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A character that **walks**. Not a rectangle sliding along — a figure whose legs move, who faces the
way they are going, who stands still when you stop, and who is drawn as crisp pixel art rather than a
blurry smear.

```
   the spritesheet: ONE image                 what the player sees
   ┌────┬────┬────┬────┬────┬────┐
   │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │   idle          ███
   ├────┼────┼────┼────┼────┼────┤                ██ ██
   │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │   walk   →      ███
   └────┴────┴────┴────┴────┴────┘                ██ ██
          ↑ a rectangle slides along              ╱   ╲
```

You will also make your own spritesheet **in code**, with no art program and no image file, because a
canvas is an image as far as the browser is concerned. That turns out to be a genuinely useful trick
and not a workaround.

## Where this fits

- **Back:** [lesson 3](../lesson-03-acceleration-friction-and-drag/notes.md) gave you something that
  moves well. Today it stops being a triangle.
- **Forward:** [lesson 5](../lesson-05-tilemaps/notes.md) draws a whole world out of small square
  images, using exactly the same `drawImage` call you learn today.
- **Other tracks:** Python's intermediate lesson 5 and C++'s intermediate lesson 7 do this with
  `pygame.Surface` and raylib's `DrawTextureRec`. Both take the same four numbers: which part of the
  sheet, and where to put it.

---

## The idea, in plain words

### A walking character is one picture, not many

The instinct is one file per pose: `walk1.png`, `walk2.png`, `walk3.png`. It works, and real games do
not do it, for three reasons that matter:

1. **Loading.** Each file is a separate request. Thirty poses is thirty waits.
2. **Switching.** Asking the graphics card to change image is slow compared with drawing. One image
   means it never has to.
3. **Keeping track.** One file is one thing to name, find and not lose.

So the poses go side by side in one image, called a **spritesheet** (or an atlas). Then "which pose am
I showing?" becomes "which rectangle of this one image am I copying?" — and a rectangle is four
numbers, which is a much easier thing to change sixty times a second than a filename.

### The flipbook analogy, and where it breaks

A spritesheet is a flipbook with the pages laid out flat instead of stacked. You are not turning
pages; you are sliding a window along.

Where it breaks: **a flipbook has one speed, and your game has two clocks.** The game runs at 60
frames a second. The walk cycle should run at about 8 poses a second. If you advance one pose per game
frame — which is what nearly everybody writes first — the character vibrates rather than walks, and the
speed of the vibration depends on the computer.

Those two clocks staying separate is the real content of this lesson. The drawing part is one function
call.

### The one function call

```js
ctx.drawImage(image,  sx, sy, sw, sh,   dx, dy, dw, dh);
//            ↑       ↑ which part of   ↑ where on the
//            source    the image         canvas, and how big
```

Nine arguments is a lot, and they are in a sensible order once you see the split: **four say where to
copy *from*, four say where to put it.** `s` is for source, `d` is for destination.

There are two shorter forms, and knowing all three stops you guessing:

```js
ctx.drawImage(img, dx, dy);                    // whole image, natural size
ctx.drawImage(img, dx, dy, dw, dh);            // whole image, stretched
ctx.drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh);   // one piece, any size
```

The nine-argument form is the only one that can take a piece of a sheet. The others are the ones that
cause the "why is my whole spritesheet on screen?" bug, which every single person writes once.

### Which rectangle? Arithmetic you already know

For a sheet laid out in a grid of equal cells:

```js
const sx = column * FRAME_WIDTH;
const sy = row    * FRAME_HEIGHT;
```

That is the same `y * WIDTH + x` grid thinking from the beginner levels, used for pixels instead of
array slots. If the sheet is one row, the row never changes and only the column moves.

### The frame timer: two clocks, kept apart

```js
const FRAME_TIME = 1 / 8;     // hold each pose for an eighth of a second

sprite.timer = sprite.timer + dt;
while (sprite.timer >= FRAME_TIME) {
  sprite.timer = sprite.timer - FRAME_TIME;        // subtract, do not zero
  sprite.frame = (sprite.frame + 1) % FRAME_COUNT; // wrap round the sheet
}
```

Three details, all of them load-bearing:

- **`while`, not `if`.** On a slow frame, more than one pose may be due. `if` would silently drop them
  and the animation would run slow exactly when the computer is struggling.
- **Subtract, do not zero.** `timer = 0` throws away the leftover, so the animation drifts a little
  slower than you asked for. This is the same reasoning as the accumulator you will meet again in the
  advanced level.
- **`% FRAME_COUNT`** wraps 5 back round to 0. Using `if (frame > 5) frame = 0` works and breaks the
  moment you change the number of frames.

### Animation is driven by state, not by the keyboard

Here is the design idea that keeps this from turning into a mess. Do **not** write "when the right
arrow is pressed, play the walk animation". Write:

```js
// 1. The game works out what the character is DOING. This is not about pictures.
if      (!player.onGround)              { player.state = "jump"; }
else if (Math.abs(player.vel.x) > 10)   { player.state = "walk"; }
else                                    { player.state = "idle"; }

// 2. The state chooses a row of the sheet. This is the ONLY place that knows
//    anything about the image.
const ANIMATIONS = {
  idle: { row: 0, frames: 2, fps: 2 },
  walk: { row: 1, frames: 6, fps: 8 },
  jump: { row: 2, frames: 1, fps: 1 }
};

// 3. Changing state starts the new animation from the beginning.
if (player.state !== player.lastState) {
  player.frame = 0;
  player.timer = 0;
  player.lastState = player.state;
}
```

This is the state machine from the beginner level, pointed at a different job. The payoff: adding a
"hurt" animation means adding one line to `ANIMATIONS` and one condition — not touching your input
code, your physics, or your drawing.

### Facing the other way, without a second set of drawings

You do not draw a left-facing walk cycle. You draw the right-facing one backwards:

```js
ctx.save();
if (player.facing === -1) {
  // Move to where the sprite goes, then mirror the canvas horizontally.
  ctx.translate(player.pos.x, player.pos.y);
  ctx.scale(-1, 1);
  ctx.translate(-player.pos.x, -player.pos.y);
}
ctx.drawImage(sheet, sx, sy, FW, FH, player.pos.x - FW / 2, player.pos.y - FH, FW, FH);
ctx.restore();
```

`scale(-1, 1)` multiplies every x by −1, which mirrors everything. The two `translate` calls are there
because the mirror happens about x = 0 — the left edge of the canvas — so without them your sprite
flies off to the left. Mirror *about the sprite*, which means moving the origin to it first.

### Crisp pixels

Draw a 16×16 sprite at 4× size and the browser helpfully blurs it, because it assumes you are
scaling a photograph. Two lines stop that:

```js
ctx.imageSmoothingEnabled = false;      // reset by some canvas operations, so set it in draw()
```

```css
canvas { image-rendering: pixelated; }  /* for scaling the canvas ELEMENT itself */
```

And one habit: **draw sprites at whole-number positions.** A sprite at `x = 40.3` is sampled between
pixels and comes out soft and wobbly even with smoothing off.

```js
const drawX = Math.round(player.pos.x);
```

Keep the *position* fractional — physics needs it — and round only when drawing. Rounding the real
position makes movement stutter at low speeds.

### Loading a real image, when you have one

```js
/* An image is not ready the instant you ask for it. The browser has to fetch
   and decode it, which takes time, so you get an empty box that fills in later.
   Drawing it too early draws nothing - silently, with no error. */
function loadImage(src) {
  return new Promise(function (resolve, reject) {
    const img = new Image();
    img.onload  = function () { resolve(img); };
    img.onerror = function () { reject(new Error("could not load " + src)); };
    img.src = src;              // set src LAST, after the handlers are attached
  });
}

// Wait for everything before the game starts. One wait, not one per image.
const [hero, tiles] = await Promise.all([
  loadImage("hero.png"),
  loadImage("tiles.png")
]);
startGame(hero, tiles);
```

One more thing worth knowing before it costs you an afternoon: **a PNG loaded from `file://` and drawn
to a canvas will work, but reading the pixels back with `getImageData` will throw a security error.**
That is the same origin rule from lesson 1 in a new place. Serving the folder fixes it.

### A sheet with no image file at all

This repository ships no `.png` files on purpose, so the examples build their sheets in code. That is
not a workaround — it is a technique worth having:

```js
/* A canvas you never add to the page is an "offscreen canvas", and drawImage
   accepts it anywhere it accepts an image. So you can DRAW your spritesheet. */
function buildSheet() {
  const sheet = document.createElement("canvas");
  sheet.width = FRAME_W * FRAME_COUNT;
  sheet.height = FRAME_H * ROW_COUNT;
  const sctx = sheet.getContext("2d");

  for (let i = 0; i < FRAME_COUNT; i++) {
    drawWalkPose(sctx, i * FRAME_W, FRAME_H, i / FRAME_COUNT);
  }
  return sheet;        // hand this to ctx.drawImage like any other image
}
```

Three real uses for this beyond today: generating sprites from numbers so a tweak is a code change
rather than a trip to an art program; pre-rendering something expensive once instead of every frame;
and recolouring a sheet at load time to make four team colours out of one drawing.

---

## The idea, in pictures

Open [the spritesheet explainer](../../../shared/visualizers/sprite-animation.html).

**What to look for:** two clocks are running and they are not the same clock. Press **Step 1 frame**
repeatedly: the game frame counter goes up every press, but the pose only changes when the timer bar at
the bottom fills. Several game frames per pose is *correct*. Then switch on "advance every game frame"
and watch the character stop walking and start vibrating — that is the bug this lesson exists to
prevent, and it is the first thing almost everybody writes.

---

## The idea, in code

Work through the examples in order; each one adds a single idea.

1. `code/01-make-a-spritesheet.html` — build a sheet in an offscreen canvas and look at it magnified.
2. `code/02-drawimage-and-source-rects.html` — all three forms of `drawImage`, with the numbers shown
   live, and a draggable source rectangle.
3. `code/03-walk-cycle-and-states.html` — the frame timer, states choosing animations, and a
   deliberately broken "one pose per frame" switch to compare against.
4. `code/04-crisp-pixels-and-flipping.html` — smoothing, whole-number positions, and mirroring.

---

## The maths you just used

Almost none, and this is worth saying plainly rather than inventing some.

The one genuinely new thing is **modulo** used as a wrap-around:

```js
frame = (frame + 1) % FRAME_COUNT;
```

`%` gives the remainder after division, so counting 0, 1, 2, 3, 4, 5, 0, 1, … comes out of one
expression with no `if` at all. You met the same operator in the beginner C++ track for turning a flat
array index back into a grid position; here it is making a loop with no end.

Everything else is multiplication: `column × FRAME_WIDTH` is where that column starts, because the
columns are all the same width. It is worth noticing how much of graphics programming is arithmetic
this ordinary.

---

## Break it on purpose

Use `code/03-walk-cycle-and-states.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Advance the pose every game frame | | |
| Change `while (timer >= FRAME_TIME)` to `if` and then drop the frame rate | | |
| Replace `timer -= FRAME_TIME` with `timer = 0` and run for a minute | | |
| Use the four-argument `drawImage(img, x, y, w, h)` with a sheet | | |
| Remove `% FRAME_COUNT` | | |
| Forget to reset `frame = 0` when the state changes | | |
| Remove the two `translate` calls around `scale(-1, 1)` | | |
| Draw at `pos.x` without rounding, and walk very slowly | | |

The `timer = 0` one is a good argument-settler: the animation looks completely fine, and over a minute
it falls noticeably behind where it should be. Some bugs are only visible if you wait.

---

## Think like an engineer

1. A sprite is drawn from a point. Which point — the top-left corner, the centre, or the middle of the
   character's feet? Pick one for a platform game and say why. (Think about what happens when a
   character's picture gets bigger, and about what the collision box is measured from.)
2. The walk cycle has 6 poses. A player at double speed is still showing 8 poses a second, so their
   feet slide. How would you tie the animation speed to how fast they are actually moving? What breaks
   if you tie it too tightly?
3. **Design something.** A character that can be hurt *while* walking, jumping or standing. Flashing
   red is one option; a separate "hurt" animation that interrupts and then returns is another. Design
   the state machine. What happens if they are hurt twice in quick succession?
4. **The hard one.** Your sheet has grown to 200 poses and loads slowly, and you want to recolour the
   player's shirt for team red and team blue. You could ship two sheets, or recolour at load time, or
   draw a separate "shirt" layer on top. All three are used in real games. Pick one, say what it costs,
   and say what would make you change your mind.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Sprite** | A single image drawn as one object in the game. |
| **Spritesheet / atlas** | One image holding many sprites in a grid. |
| **Source rectangle** | The `sx, sy, sw, sh` part of `drawImage` — which piece to copy. |
| **Destination rectangle** | The `dx, dy, dw, dh` part — where to put it and how big. |
| **Frame** | One pose of an animation. (Also one tick of the game loop. Context tells you which.) |
| **Frame timer** | The accumulator that decides when the next pose is due. |
| **Anchor / origin** | The point on the sprite that its position refers to. |
| **Offscreen canvas** | A canvas never added to the page, used as an image. |
| **`imageSmoothingEnabled`** | Turn off to keep pixel art sharp. |
| **Modulo (`%`)** | Remainder after division. Used to wrap a counter round. |

---

## Recap

- One image with the poses in a grid, and a **rectangle that slides along it**. That is all a
  spritesheet is.
- `drawImage` has **three** forms. Only the nine-argument one can take a piece of a sheet.
- The game clock and the animation clock are **different clocks**. Keep a separate timer, use `while`,
  and **subtract** rather than zeroing.
- Let the character's **state** choose the animation. Never let the keyboard choose it directly.
- `scale(-1, 1)` mirrors — but mirror *about the sprite*, or it flies off the screen.
- Turn off smoothing and **round when you draw**, not when you move.

---

## Stretch goals

1. **Speed-matched feet.** Make the walk animation's fps proportional to the player's actual speed, so
   the feet never slide. Find the constant that makes it look right.
2. **Recolour the sheet.** Load (or build) your sheet, then make a red and a blue version at startup by
   drawing it to two offscreen canvases with `globalCompositeOperation`. Two teams, one drawing.
3. **A ping-pong animation.** Make a swing play 0,1,2,3,2,1 instead of looping. You will need something
   more than `%`.
4. **Pack the sheet yourself.** Write a function that takes a list of offscreen canvases and packs them
   into one sheet, returning a lookup of names to source rectangles. This is what a real atlas packer
   does.
5. **Onion skin.** Draw the previous two poses faintly behind the current one. Animators use this; it
   makes a bad walk cycle obvious immediately.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `03-walk-cycle-and-states.html` with "one pose per frame" switched on. The vibrating character gets a laugh. Ask what is wrong: most will say "it's too fast", which is nearly right and not quite. |
| 10–25 | **Concept.** The spritesheet visualizer, entirely on the two clocks. Step it. Ask the class to predict whether the pose will change on the next press — they will be wrong often enough to pay attention. |
| 25–40 | **Live-code** the frame timer. Four lines, and every one of them has a reason. Then the nine arguments of `drawImage` on the board, split into the two groups of four. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–3 are the core; 4 onwards is polish. |
| 120–140 | Break-it-on-purpose. The `timer = 0` drift one needs a stopwatch and is worth it. |
| 140–150 | Recap. Lesson 5 builds a whole world out of the same call. |

**Before the lesson:** decide whether your class will use the code-generated sheets (works everywhere,
no files) or bring their own PNGs. If PNGs, be ready for `file://` problems — the image will draw but
`getImageData` will not work, and anyone trying stretch goal 2 will hit it.

**What usually goes wrong**

1. **The whole spritesheet appears on screen.** They used the four-argument `drawImage`. The most common
   bug in this lesson by a wide margin, and the picture makes the cause obvious once they see it.
2. **Nothing appears at all.** Either the image had not loaded when they drew it, or the source
   rectangle is off the edge of the sheet (frame index too high). Both draw *nothing*, with no error. Have
   them draw a bright rectangle at the same place first to prove the position is right.
3. **The character vibrates.** One pose per game frame. This is the lesson, so let it happen.
4. **The sprite is blurry.** `imageSmoothingEnabled` not set, or set once outside `draw()` and reset by
   something else, or the position is fractional.
5. **The sprite jumps off the left edge when it turns round.** `scale(-1, 1)` without the two
   `translate` calls. Draw the mirror line at x = 0 on the board; it explains itself.
6. **Animation restarts every frame.** They reset `frame = 0` whenever the state is "walk" rather than
   when it *becomes* "walk". Comparing against `lastState` is the fix, and noticing the difference
   between "is" and "became" is a genuinely useful idea.
7. **The feet slide.** Correct, and it is stretch goal 1. Worth mentioning to everyone — once you point
   it out, nobody can unsee it in other people's games.

**If you are running short on time** — cut `code/04` and the flipping entirely; a character that always
faces right is fine for one lesson. Cut the real-image loading section too if nobody has PNGs. Do
**not** cut the frame timer or the state-driven animation: lesson 12's platformer assumes both.

**For the student who finishes at minute 90** — stretch goal 1 (speed-matched feet) is the one that
teaches the most, because it is a feel problem rather than a code problem and the constant has to be
found by looking. Stretch goal 5 (onion skin) is a good one for anyone who draws.

**The point to land at the end:** the drawing was one function call. Everything else today was about
*time* — keeping the animation's clock separate from the game's, and letting the character's state,
rather than the keyboard, decide what is shown. That split is why a well-built game can add a new
animation in two lines.
