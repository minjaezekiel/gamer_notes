# Lesson 6 — The Camera

> **Web Games · Intermediate level · Lesson 6 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A world **bigger than the screen**, that scrolls to follow your player — smoothly, without making
anybody feel sick, with distant hills drifting slowly behind, and with a score in the corner that
stays put while everything else moves.

```
      THE WORLD (2400 wide)                     THE SCREEN (640 wide)
  ┌──────────────────────────────────┐        ┌──────────────┐
  │  ╱╲    ┌────────┐      ╱╲   ╱╲   │        │   ┌────────┐ │
  │ ╱  ╲   │ camera │  ☺  ╱  ╲ ╱  ╲  │   →    │ ☺ │        │ │
  │────────│────────│───────────────-│        │   └────────┘ │
  └──────────────────────────────────┘        └──────────────┘
         the camera is a RECTANGLE,              you only ever
         not an object in the world              see inside it
```

## Where this fits

- **Back:** [lesson 5](../lesson-05-tilemaps/notes.md) built a level. It fitted on the screen, which
  will not be true for much longer.
- **Forward:** [lesson 9](../lesson-09-particles-and-juice-engineering/notes.md) shakes this camera,
  and [lesson 12](../lesson-12-capstone-a-platformer/notes.md) needs it for a level worth exploring.
- **Other tracks:** Python's intermediate lesson 7 does the same subtraction by hand; C++'s
  intermediate lesson 9 uses raylib's `Camera2D`, which does it for you. Knowing the subtraction is why
  `Camera2D` will make sense rather than being magic.

---

## The idea, in plain words

### There is no camera

This is the sentence to hold on to. Nothing in your game moves a camera, because no such object
exists. What you have is **one pair of numbers that you subtract from everything before you draw it.**

```js
const screenX = worldX - camera.x;
const screenY = worldY - camera.y;
```

That is the lesson. Everything else today is a decision about what `camera.x` should be.

### Two coordinate systems, and the discipline of keeping them apart

From today your game has **two** kinds of position, and mixing them up is the source of nearly every
bug in this lesson.

| | What it means | Example |
|---|---|---|
| **World space** | Where something really is in the level | the player is at x = 1840 |
| **Screen space** | Where it appears on the canvas | the player is at x = 320 |

The player is at 1840 **and** at 320, at the same moment, and both are correct. A useful habit: name
your variables for which space they are in. `worldX`, `screenX`. It looks fussy for a week and then
saves you repeatedly.

Three rules that follow:

- **Game logic uses world space.** Collision, physics, distances between enemies — all world space. None
  of it should know a camera exists.
- **Drawing converts to screen space.** At the last moment, when you draw.
- **The mouse arrives in screen space and must be converted back.** `worldX = screenX + camera.x`. Click
  to place a block and forget this, and your block lands in the wrong place as soon as you scroll.

### The camera-as-window analogy, and where it breaks

Think of the screen as a window you slide over a large painting. The painting does not move; your view
of it does.

Where it breaks: **the painting is not finished, and the window has opinions.** A real game camera does
not simply sit on the player. It leads them, lags behind them, refuses to move for small movements,
stops at the edges of the level, and sometimes shakes. It is a character in its own right, and getting
it wrong makes a game that is otherwise fine feel unpleasant.

### Why "camera = player" is wrong, and what to do instead

The obvious version:

```js
camera.x = player.x - canvas.width / 2;      // centre the player
```

Try it. It works and it feels bad, for two reasons:

1. **Every tiny movement moves the whole world.** The player steps left; 90% of the screen jerks right.
   For some people this is genuinely nauseating.
2. **You cannot see where you are going.** The player is pinned to the exact middle, so you always have
   the same amount of warning in both directions, even though you are only moving one way.

Three fixes, which stack:

**1. A dead zone.** Do nothing until the player is far enough from the middle.

```js
const DEAD_ZONE = 120;                  // pixels either side of centre
const wanted = player.x - canvas.width / 2;
const gap = wanted - camera.x;
if (Math.abs(gap) > DEAD_ZONE / 2) {
  // only move by the amount that is OUTSIDE the dead zone
  camera.x += gap > 0 ? gap - DEAD_ZONE / 2 : gap + DEAD_ZONE / 2;
}
```

Now small movements move the player across the screen and leave the world alone. This single change is
the biggest improvement available.

**2. Smoothing.** Move a fraction of the remaining distance each frame, rather than all of it.

```js
camera.x = camera.x + (wanted - camera.x) * 0.1;
```

The camera eases towards the target, and never quite arrives — which nobody notices and everybody
feels. This is `lerp`, and it has the same frame-rate problem as the drag in lesson 3: `0.1` is
*per frame*. The honest version:

```js
const SMOOTH = 6;                                  // per second
const t = 1 - Math.exp(-SMOOTH * dt);
camera.x = camera.x + (wanted - camera.x) * t;
```

**3. Look-ahead.** Offset the target in the direction they are travelling.

```js
const lookAhead = player.vx * 0.25;     // a quarter of a second into the future
const wanted = player.x + lookAhead - canvas.width / 2;
```

Now running right shows you more of what is to the right. Combined with smoothing this is most of what
makes a platformer camera feel professional, and it is one line.

### Clamping to the level

Without this, walking to the left-hand wall shows you a screen of nothing.

```js
camera.x = Math.max(0, Math.min(worldWidth - canvas.width, camera.x));
```

There is an edge case worth handling before it embarrasses you: if the world is **narrower** than the
screen, `worldWidth - canvas.width` is negative, and `Math.min` then forces the camera to a negative
number, pushing your small level off to the right. Decide what you want and say so:

```js
if (worldWidth <= canvas.width) {
  camera.x = (worldWidth - canvas.width) / 2;      // centre the small level
} else {
  camera.x = Math.max(0, Math.min(worldWidth - canvas.width, camera.x));
}
```

### Two ways to apply the camera, and when each is right

**Subtract, per thing:**

```js
ctx.fillRect(thing.x - camera.x, thing.y - camera.y, thing.w, thing.h);
```

**Translate, once:**

```js
ctx.save();
ctx.translate(-Math.round(camera.x), -Math.round(camera.y));
drawEverythingInWorldCoordinates();       // every draw call uses WORLD positions
ctx.restore();

drawHud();          // outside the transform, so it does not scroll
```

The second is tidier, harder to get wrong, and makes one thing *much* clearer: **anything drawn inside
the transform scrolls, and anything outside it does not.** That is exactly the distinction you want for
a score display, so the structure of your draw function becomes a statement about what is part of the
world and what is part of the interface.

Note the `Math.round` on the camera. A camera at `x = 100.4` draws every tile at a fractional
position, and a world of 28-pixel tiles then shows hairline gaps that shimmer as you move. Round the
camera, not the things in the world.

### Parallax: distance, for free

Things far away appear to move more slowly. Copy that by multiplying the camera offset:

```js
drawHills(hill.x - camera.x * 0.3);      // distant: moves at 30% of the camera
drawTrees(tree.x - camera.x * 0.6);      // nearer: 60%
drawWorld(thing.x - camera.x * 1.0);     // the actual world: 100%
drawRain(drop.x - camera.x * 1.4);       // in front: faster than the world
```

Four multiplications and a flat picture gains depth. A factor of `0` is a background that never moves
at all — which is how a sky works.

---

## The idea, in pictures

Open [the camera explainer](../../../shared/visualizers/camera.html).

**What to look for:** two pictures of the *same moment*. On the left, the whole level and where the
player really is. On the right, what the player sees. **The player is at world x = 1200 and screen
x = 240 at the same time** — read both numbers and watch them disagree while the subtraction at the
bottom explains why. Then watch the dead zone: inside it, the camera does not move at all and the
player drifts across the screen. Turn the smoothing up to 100 and feel the difference between a camera
that eases and one that snaps.

---

## The idea, in code

1. `code/01-scroll-by-hand.html` — a world four screens wide, with `camera = player` and nothing else.
   It works, and it feels wrong. The readout shows both coordinate systems.
2. `code/02-follow-and-deadzone.html` — snap, smooth, dead zone and look-ahead, each on its own switch,
   with sliders.
3. `code/03-translate-and-the-hud.html` — the two ways of applying the camera, and what happens when
   the score is drawn inside the transform by mistake.
4. `code/04-parallax-and-the-mouse.html` — four parallax layers, and clicking to place a block, which
   needs the conversion back to world space.

---

## The maths you just used

**1. One subtraction.** `screen = world − camera`. Everything in this lesson is that, used in different
places. The reverse, for the mouse, is `world = screen + camera`.

**2. Linear interpolation.** `a + (b − a) × t` gives you a point partway from `a` to `b`. With `t = 0`
you get `a`, with `t = 1` you get `b`, with `t = 0.1` you get a tenth of the way. Applied every frame to
the *remaining* distance, it produces a curve that approaches the target and never reaches it — the same
exponential decay as the drag in lesson 3, which is why it needs the same `Math.exp` treatment to be
frame-rate independent.

You will reuse `lerp` for health bars, menus, difficulty and colour fades. It is worth putting in your
`Vec2` file.

**3. Clamping, with a trap.** `Math.max(lo, Math.min(hi, v))` only makes sense when `lo <= hi`. When the
world is narrower than the screen, it is not, and the clamp silently does something absurd. Any time you
clamp between two computed numbers, ask whether they can cross.

**4. Scaling an offset.** Parallax is `camera.x × factor`. A factor below 1 is further away, above 1 is
nearer, and 0 never moves. There is no more to it than that.

---

## Break it on purpose

Use `code/02-follow-and-deadzone.html` and `code/03-translate-and-the-hud.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Set the dead zone to 0 and smoothing to 100 | | |
| Set the dead zone to 600 (wider than the screen) | | |
| Remove the camera clamp and walk to the left wall | | |
| Make the world 300 px wide, narrower than the screen | | |
| Draw the score **inside** `ctx.translate` | | |
| Forget `ctx.restore()` | | |
| Remove `Math.round(camera.x)` and scroll slowly | | |
| Click to place a block, with the mouse **not** converted to world space | | |
| Set every parallax factor to 1 | | |

The last-but-one is the most instructive: the block lands correctly while the camera is at 0 and gets
worse the further you scroll, which is a very recognisable shape of bug.

---

## Think like an engineer

1. The camera currently follows the player. Name three other things a camera might follow or do, and say
   what each is for. (Think about a boss arriving, two players on one screen, or a cut-scene.)
2. Two players, one screen, and they can walk apart. The camera cannot centre on both. Design something.
   What happens when they are further apart than the screen is wide? (Your answer will involve a decision
   nobody can avoid making.)
3. **Design something.** A camera that zooms out when the player moves fast and in when they stop. What
   would you have to change about the drawing? What breaks about your tile culling? What breaks about the
   dead zone, which is measured in pixels?
4. **The hard one.** Your game has a camera that follows the player, a screen shake, and a cut-scene
   camera that moves to fixed points. All three want to control `camera.x`. How do you structure that so
   they do not fight, and so you can add a fourth next month? (There is a general answer; it is also the
   answer to question 1.)

---

## Vocabulary

| Word | What it means |
|---|---|
| **World space** | Where things really are in the level. |
| **Screen space** | Where things appear on the canvas. |
| **Camera** | Two numbers you subtract. Not an object in the world. |
| **Dead zone** | A region around the centre where the camera refuses to move. |
| **Look-ahead** | Offsetting the camera towards where the player is heading. |
| **Lerp** | `a + (b − a) × t`. Partway from a to b. |
| **Clamping the camera** | Stopping it showing the outside of the level. |
| **Parallax** | Backgrounds that move more slowly, to suggest distance. |
| **HUD** | The score and bars, drawn in screen space so they do not scroll. |
| **`ctx.translate`** | Moves the canvas's origin. Applies the camera to everything at once. |

---

## Recap

- There is no camera. There is **one subtraction**: `screen = world − camera`.
- Your game now has **two coordinate systems**. Name your variables accordingly and convert at the last
  moment.
- `camera = player` is nauseating. **Dead zone**, then **smoothing**, then **look-ahead** — in that order
  of importance.
- **Clamp** the camera to the level, and handle the world-narrower-than-the-screen case on purpose.
- `ctx.translate` applies the camera once. Anything drawn **outside** it does not scroll — which is
  exactly what a HUD wants.
- **Round the camera**, or tiles show shimmering seams.
- The mouse arrives in screen space. Convert it back, or clicks land in the wrong place.

---

## Stretch goals

1. **Vertical dead zone, different size.** Platformers usually allow much more vertical slack than
   horizontal, because jumping is normal and should not move the world. Find the numbers that feel right.
2. **Snap on landing.** When the player lands, let the camera catch up quickly; while they are in the
   air, let it lag. This is a real technique and it feels noticeably better.
3. **A camera that leads a turn.** When the player changes direction, let the look-ahead swing across
   smoothly rather than jumping.
4. **Edge triggers.** Instead of following continuously, move the camera a whole screen at a time when
   the player reaches the edge. This is how the first Zelda worked. Build it, then argue about which is
   better.
5. **Zoom** (question 3). Hardest of these, and `ctx.scale` is only the start of it.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `01-scroll-by-hand.html` on the projector with `camera = player`. Walk left and right in small steps. Ask them what is unpleasant about it. Somebody will say "it makes me feel ill", which is the honest answer and the reason for the rest of the lesson. |
| 10–25 | **Concept.** The camera visualizer. Read out both of the player's x positions and let the contradiction sit for a moment. Then the dead zone. |
| 25–40 | **Live-code** the subtraction, then `ctx.translate`, then draw the score in the wrong place on purpose and let them spot it. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. |
| 120–140 | Break-it-on-purpose. The un-converted mouse click is the best one for a class, because the error grows with distance. |
| 140–150 | Recap. Lesson 7 organises menus and pausing. |

**What usually goes wrong**

1. **Everything scrolls, including the score.** Drawn inside the transform. Visually obvious and
   instantly fixed, and it teaches the world/interface split better than any explanation.
2. **The world scrolls the wrong way.** They added the camera instead of subtracting it. Ask them to
   say out loud what should happen to a thing at world x = 0 when the camera moves right.
3. **Clicks land in the wrong place, worse the further you scroll.** The mouse was not converted.
4. **Collision breaks after adding the camera.** They converted to screen space too early, so the physics
   is now comparing screen positions with world positions. The fix is the discipline, not a line of code:
   logic in world space, convert only when drawing.
5. **Shimmering gaps between tiles.** Fractional camera position. `Math.round` on the camera.
6. **The camera juddery at the level edges.** Smoothing fighting the clamp. Clamp *after* smoothing, and
   only clamp the camera, never the target.
7. **A tiny level is pushed off the right-hand side.** The narrower-than-the-screen case.

**If you are running short on time** — cut parallax and `code/04` entirely; it is the most fun and the
least necessary. Cut look-ahead too. Do **not** cut the dead zone or the HUD-outside-the-transform
point: the first is the whole reason the lesson exists, and the second will otherwise break lesson 7.

**For the student who finishes at minute 90** — stretch goal 2 (snap on landing) is the best, because the
improvement is large and the code is small. Stretch goal 4 is good for anyone interested in game history;
have them play both and defend a preference.

**The point to land at the end:** the camera is two numbers and a subtraction, and *every single thing*
that makes it feel good is a decision about those two numbers rather than more code. Your students now
have a dead zone, smoothing and look-ahead — the same three ideas a commercial platformer uses, with the
same names.
