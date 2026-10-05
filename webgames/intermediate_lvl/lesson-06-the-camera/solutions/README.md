# Lesson 6 — Solutions and marking notes

---

## Section A

**A1.** [2] `screenX = worldX - camera.x` and `worldX = screenX + camera.x`. One mark each.

**A2.** [3] Two reasons, two marks: every small movement moves the entire screen, which some people find
genuinely nauseating; and the player is pinned to the exact centre, so you get no extra warning in the
direction you are actually travelling. Third mark for any clear statement that the camera is doing
*exactly* what was asked and the problem is the design, not a bug.

**A3.** [2] A region around the centre of the screen in which the camera refuses to move at all — one
mark. It solves the first problem in A2: small movements now move the player across the screen and leave
the world still — one mark.

**A4.** [2] Because screen positions change when the camera moves, so the same two objects would pass or
fail a collision test depending on where the camera happens to be — one mark. The world is the truth;
screen space is a presentation of it, produced at the last moment — one mark.

**A5.** [2] Inside the transform, things are drawn in world coordinates and scroll with the camera.
Outside it, they are drawn in screen coordinates and stay put. One mark. The world and the player belong
inside; the score, health bar and pause menu belong outside — one mark.

**A6.** [2] Because a fractional camera means every tile is drawn at a fractional position — one mark —
which produces hairline gaps between tiles that shimmer as the camera moves — one mark.

**A7.** [3] It assumes `worldWidth - canvasWidth` is at least 0. If the level is narrower than the screen
that value is negative — two marks — and the clamp then forces the camera to a negative number, pushing
the small level off to the right rather than showing it — one mark. Accept any description of a sensible
fix (centre it, or clamp to 0).

---

## Section B

**B1.** [3] `1840 − 1520 = 320`. Two marks. The canvas is 640 wide so the centre is 320: they are
**exactly centred** — one mark.

**B2.** [3] `100 + 1520 = 1620`. Two marks. The un-converted version reports `100` — one mark. Worth
noting out loud: it is right only while the camera is at 0, which is exactly why the bug survives the
first test.

**B3.** [4] Frame 1: `0 + 500 × 0.1 = 50`. Frame 2: `50 + 450 × 0.1 = 95`. Frame 3:
`95 + 405 × 0.1 = 135.5`. Three marks. It **never reaches 500** — each step covers a tenth of what is
left, so it gets arbitrarily close and never arrives — one mark.

Credit anyone who notices this is the same exponential curve as the drag in lesson 3, and therefore has
the same frame-rate problem.

**B4.** [3] `worldWidth - canvasWidth = -340`, so `Math.min(-340, camera.x)` gives `-340`, and
`Math.max(0, -340)` gives `0`. Two marks. The level is drawn from the left-hand edge with 340 pixels of
empty space to its right — one mark. (Accept the alternative analysis with the clamp order reversed; the
key point is that the result is not what anyone intended.)

**B5.** [3] At factor 0.3: `1000 − 600 × 0.3 = 1000 − 180 = 820`. Two marks. At factor 1.0:
`1000 − 600 = 400` — one mark. The hill at 0.3 has barely moved, which is the effect.

---

## Section C

**C1.** [3] The camera is being **added** instead of subtracted. Two marks. Fix: `thing.x - camera.x` —
one mark. Good diagnostic question for the class: what should happen to a thing at world x = 0 when the
camera moves right? It should move left, off the screen.

**C2.** [3] `fillText` is inside the transform, so the score is drawn in world coordinates and scrolls
with the level. Two marks. Fix: move it after `ctx.restore()` — one mark.

**C3.** [4] The click is in screen space and is being used as if it were world space. Two marks. The
error is exactly `camera.x`, so it is zero at the start of the level and grows as you scroll — one mark,
and this is the half worth insisting on, because "it worked when I tested it" is why the bug shipped.
Fix: `placeBlock(e.clientX - b.left + camera.x, e.clientY - b.top + camera.y)` — one mark.

**C4.** [4] The collision test has been converted to screen space, so it is comparing a screen position
against a tilemap stored in world coordinates. Two marks. The two agree only while the camera is at (0,0),
so the floor appears to move away as the camera scrolls — one mark. Fix: test with `player.x`, not
`player.screenX`; `screenX` exists only for drawing — one mark.

**C5.** [3] The clamp runs **before** the smoothing, so smoothing immediately pulls the camera back out of
bounds, and next frame the clamp pushes it in again. Two marks. Fix: smooth first, clamp afterwards —
one mark. Credit anyone who adds that the *target* should not be clamped, only the camera, or the dead
zone fights the clamp as well.

---

## Section D — marking the build

1. **Both coordinate systems are on screen** (checkpoint 2). Everything else in the lesson is diagnosable
   in seconds with that readout and a guessing game without it.
2. **The HUD survives `restore()`** (checkpoint 3). Walk to the far end of the level; if the score has
   gone, it is drawn in the wrong place.
3. **The dead zone can be switched off** (checkpoint 5). The comparison is the lesson. A student who has
   only ever seen the good version has not learned anything.
4. **Smoothing uses `dt`.** If they wrote `* 0.1` with no `dt`, point at lesson 3 rather than correcting
   it, and let them recognise the same bug in a new place.
5. **The click test at the far end of the level** (checkpoint 8). This is the one test that catches the
   whole class of world/screen confusion.

Checkpoint 4's narrow-level case is worth ten seconds of everyone's attention: it is the first time many
of them will have met a clamp whose bounds can cross, and the habit of asking "can `lo` ever exceed `hi`?"
is worth more than this lesson.

---

## Section E — marking notes

**E1.** Plenty of good answers. Credit any three with a purpose attached:

- **Follow a different target** — a boss as it arrives, a thrown object, a vehicle the player has entered.
- **Move to fixed points** for a cut-scene or an establishing shot.
- **Frame two or more things at once** — see E2.
- **Lead to where the player is going** rather than where they are (a racing game looks into the corner).
- **Shake**, which is lesson 9.
- **Stay still** in a single-screen arena, which is a deliberate choice and not an absence of one.

**E2.** The standard approach is to aim at the **midpoint** and zoom out until both fit:

```js
const midX = (p1.x + p2.x) / 2;
const needed = Math.abs(p1.x - p2.x) + MARGIN;
const zoom = Math.min(1, canvas.width / needed);
```

The decision that cannot be avoided, and the thing worth most credit for spotting: **what happens when
they are too far apart to show at any sensible zoom?** Real games choose one of:

- a hard limit on how far apart players can get — an invisible wall;
- a split screen;
- let the trailing player die or be teleported to the leader (common in party games);
- show off-screen players as arrows at the edge.

Every one of those is a design decision with consequences for how the game plays, and a student who
realises that the camera has just forced a *gameplay* decision has understood something real.

**E3.** What changes: `ctx.scale(zoom, zoom)` before the translate, and the camera must now centre on the
player in *scaled* coordinates, so the arithmetic changes (`camera.x = player.x - canvas.width / (2 *
zoom)`).

What breaks, and these are the marks:

- **Culling.** The visible tile range depends on the zoom; at zoom 0.5 you can see twice as much, and a
  culling calculation that assumes `canvas.width` worth of world will leave blank strips.
- **The dead zone**, which is in pixels. Zoom out and a 120-pixel dead zone covers twice as much of the
  world, so the camera becomes sluggish exactly when the player is moving fastest — the opposite of what
  was wanted. The fix is to measure it in world units.
- **Line widths and text** scale too, so a 1-pixel outline becomes half a pixel and disappears.

Full marks for any two of those three, with the dead-zone one counting double because it is the
non-obvious one.

**E4.** The general answer is **compose the camera from independent contributions** rather than letting
anyone assign to it:

```js
// each part reports an OFFSET; nothing owns camera.x
const base  = followTarget(player, dt);   // where the camera wants to be
const shake = shakeOffset(dt);            // a small random nudge, decaying
const scene = cutsceneOffset(dt);         // zero unless a cut-scene is running
camera.x = base.x + shake.x + scene.x;
```

Credit the key insight in any wording: **one thing decides the position, and everything else is added on
top.** The shake must be an offset rather than a position, or it fights the follow code. A cut-scene is
best handled by swapping the *target*, not by overwriting the camera — which connects straight back to
E1, and is why the two questions were asked together.

Strong answers also mention that a stack of named camera behaviours with priorities is what commercial
engines provide, and that the reason is exactly this: so that adding the fourth one does not require
editing the other three.

---

## If you only mark one thing

Checkpoint 8's click test, performed at the far end of the level. It fails for anyone who has confused the
two coordinate systems anywhere in their program, and it passes only for someone who has kept them apart
— which is the actual content of this lesson.
