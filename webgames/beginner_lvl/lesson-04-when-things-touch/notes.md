# Lesson 4 — When Things Touch

> **Web Games · Beginner level · Lesson 4 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**Pong.** Not finished Pong — there is no score and no way to win yet — but a ball, two paddles,
and a ball that genuinely bounces off them.

```
┌──────────────────────────────────────┐
│ ▮                                    │
│ ▮          ●                       ▮ │
│ ▮            ↘                     ▮ │
│                                    ▮ │
└──────────────────────────────────────┘
   you                            the wall
```

## Where this fits

- **Back:** [lesson 3](../lesson-03-player-in-control/notes.md) gave you a paddle you can steer.
- **Forward:** [lesson 5](../lesson-05-rules-score-and-feel/notes.md) adds score, winning, losing
  and the things that make it feel good.
- **Today's idea — "are these two things in the same place?" — is the most-used question in all of
  2D game programming.**

---

## The idea, in plain words

### Everything is a box

Your paddle is a rectangle, so that is easy. But your ball is a circle, and the bricks in lesson 6
will be rectangles, and a spaceship is a complicated shape with wings.

Games almost always cheat: they wrap each object in an invisible **rectangle** and test the
rectangles instead. That rectangle is called a **hitbox** or a **bounding box**, and it is usually
not the same shape as the picture you see.

Why cheat?

- It is **fast**. Four comparisons, no multiplication, no square roots.
- It is **predictable**. Players learn how a box behaves.
- It is often **fairer**. Making the player's hitbox slightly *smaller* than their sprite means near
  misses feel like misses, which players enjoy. Making an enemy's hitbox slightly *larger* makes
  your shots feel generous.

The full name is **AABB**: *Axis-Aligned Bounding Box*. "Axis-aligned" means the box is never
rotated — its sides always run parallel to the screen edges. That restriction is exactly what makes
the test so cheap.

### The four conditions

Two boxes overlap when **all four** of these are true:

```js
a.x < b.x + b.w      // 1. a's left edge is left of b's right edge
a.x + a.w > b.x      // 2. a's right edge is right of b's left edge
a.y < b.y + b.h      // 3. a's top edge is above b's bottom edge
a.y + a.h > b.y      // 4. a's bottom edge is below b's top edge
```

Four conditions, joined with `and`. That is the whole test.

### The trick for remembering it

Do not try to work out when two boxes **do** overlap. That has lots of cases: one inside the other,
corner clipping corner, one much wider than the other. You will miss one.

Ask the opposite question instead: **when is it obvious they cannot possibly touch?**

There are only four ways to be certain:

1. `a` is entirely to the **left** of `b`.
2. `a` is entirely to the **right** of `b`.
3. `a` is entirely **above** `b`.
4. `a` is entirely **below** `b`.

If *none* of those four escape routes is true, the boxes must be overlapping. The four conditions
above are simply those four escape routes, flipped around.

> Turning a hard question into its easy opposite is a technique you will reuse for the rest of your
> life as a programmer. Remember this one — it is not really about rectangles.

### Circles, when you want them

For two circles, the test is even simpler. They touch when the distance between their centres is
less than their radii added together:

```js
const dx = b.x - a.x;
const dy = b.y - a.y;
const distance = Math.sqrt(dx * dx + dy * dy);
return distance < a.radius + b.radius;
```

That `Math.sqrt(dx*dx + dy*dy)` is **Pythagoras' theorem**, doing a real job. More on that below.

Circles are better than boxes when the thing really is round and when rotation matters — a round
bomb, a shockwave, an "is the enemy close enough to notice me?" check. Boxes are better for almost
everything else.

---

## The idea, in pictures

### Boxes

Open [the AABB explainer](../../../shared/visualizers/aabb-collision.html).

**What to look for:** drag the orange box around and watch the four lights change *one at a time*.
Then deliberately hunt for a position where **three are green and one is red**. That position is
exactly the case your game gets wrong if you forget a condition — and it is the reason the test needs
all four.

### Circles

Open [the circle explainer](../../../shared/visualizers/circle-collision.html).

**What to look for:** the grey right-angled triangle is the one from your maths book. `dx` along the
bottom, `dy` up the side, and the distance as the sloping side. Watch the two numbers — *distance*
and *r1 + r2* — and see which is bigger. Then tick the "no square root" box and watch both versions
agree on every position.

---

## The idea, in code

### Step 1: the test itself

```js
// Each box is {x, y, w, h}, where x and y are the TOP-LEFT corner.
function boxesOverlap(a, b) {
  return (
    a.x < b.x + b.w &&
    a.x + a.w > b.x &&
    a.y < b.y + b.h &&
    a.y + a.h > b.y
  );
}
```

Write it once, use it everywhere. Ball against paddle, ball against brick, player against enemy,
bullet against anything. One function.

### Step 2: making the ball fit

Your ball has a centre and a radius, not a corner and a size. So give it a box:

```js
function ballBox(ball) {
  return {
    x: ball.x - ball.radius,     // left edge is a radius left of the centre
    y: ball.y - ball.radius,
    w: ball.radius * 2,          // the box is a full diameter wide
    h: ball.radius * 2
  };
}
```

This is the hitbox idea in action: the ball *is drawn* as a circle, and *collides* as a square. For a
ball this small nobody will ever notice.

### Step 3: responding

Detecting a collision is only half the job. What should happen?

```js
if (boxesOverlap(ballBox(ball), paddle)) {
  // 1. PUT THE BALL BACK somewhere legal, just above the paddle.
  //    Lesson 2 taught you this: fix the position BEFORE the velocity, or the
  //    ball gets stuck inside and vibrates.
  ball.y = paddle.y - ball.radius;

  // 2. THEN turn it around.
  ball.speedY = -ball.speedY;
}
```

Same rule as the walls in lesson 2, and for exactly the same reason.

### Step 4: making it a game, not a physics demo

Real Pong does something that is not physics at all: **where you hit the paddle changes where the
ball goes**. Hit it near the edge and the ball flies off at a sharper angle.

```js
// How far from the paddle's centre did we hit? -1 is the far left edge,
// 0 is dead centre, +1 is the far right edge.
const paddleCentre = paddle.x + paddle.w / 2;
const hitOffset = (ball.x - paddleCentre) / (paddle.w / 2);

// Use that to steer the ball sideways.
ball.speedX = hitOffset * 320;
ball.speedY = -Math.abs(ball.speedY);   // always send it back upward
```

This is not how a real ball behaves. It is better than how a real ball behaves, because it hands the
player **control**. Without it, Pong is a game about standing in the right place. With it, Pong is a
game about *aiming*, and the whole thing comes alive.

That gap — between what is realistic and what is good — is most of game design.

---

## The maths you just used

### Pythagoras, finally doing something

In a right-angled triangle, **a² + b² = c²**, where c is the longest side.

When you want the distance between two points, `dx` and `dy` are the two short sides, and the
distance you want is the long one:

> **distance = √(dx² + dy²)**

You have almost certainly used this to find the missing side of a triangle in a textbook. This is the
same formula doing a real job: it is how every game in the world measures "how far away is that?"

JavaScript has a shortcut, `Math.hypot(dx, dy)`, which does exactly this and is named after the
hypotenuse.

### The professional trick: skip the square root

Square roots are one of the slower things a computer does. And notice: if
`distance < limit`, then `distance² < limit²` as well — both sides are positive, so squaring keeps
the answer the same.

```js
const distanceSquared = dx * dx + dy * dy;
const limit = a.radius + b.radius;
return distanceSquared < limit * limit;    // same answer, no square root
```

For two circles nobody could measure the difference. For ten thousand particles it is real. But the
general lesson is worth far more than the trick:

> **If you only need to compare two things, you often do not need to fully calculate either of them.**

---

## Break it on purpose

Use `code/04-pong-part-1.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Delete the `ball.y = paddle.y - ball.radius;` line | | |
| Change one `&&` to `\|\|` in `boxesOverlap` | | |
| Make the ball's speed `1500` | | |
| Remove `Math.abs` from the `ball.speedY` line | | |
| Make the paddle's hitbox 20 pixels wider than it is drawn | | |
| Set `hitOffset * 320` to `hitOffset * 0` | | |

The third one is the most important thing you will discover today. The fifth one is how you make a
game feel generous, and it is used constantly in real games.

---

## Think like an engineer

### The problem you will hit with a fast ball

You have four conditions that correctly answer *"are these two boxes overlapping **right now**?"*

But a game only looks at the world 60 times a second. If the ball moves 40 pixels per frame and the
paddle is 14 pixels thick, then between one frame and the next the ball can go from *in front of* the
paddle to *behind* it, **without ever being inside it**. Your test was never wrong; it was just never
asked at the right moment.

This is called **tunnelling**, and it is why fast-moving things in badly made games go through walls.

1. Sketch the positions of a fast ball on three consecutive frames to show the problem.
2. Invent a fix. You are allowed to change anything.
3. Now critique your own fix — what does it cost? (Every fix for this costs something.)

### The problem you will hit with lots of objects

Lesson 6 is Breakout, with maybe 60 bricks. That is 60 collision tests every frame, which is fine.

But imagine 500 bullets and 200 enemies. That is 100,000 tests **every single frame**, six million a
second.

4. Without looking anything up, invent a way to avoid most of those tests. You can change how objects
   are stored. *Hint: if you knew a bullet was in the top-left corner of the screen, which enemies
   could you skip without testing at all?*

Whatever you come up with has a real name and is in every game engine ever written. You will meet it
in the advanced level — but invent it first. Your version will probably be close.

---

## Vocabulary

| Word | What it means |
|---|---|
| **AABB** | Axis-Aligned Bounding Box: a rectangle that is never rotated. |
| **Hitbox** | The invisible shape used for collisions. Often not the same as the picture. |
| **Overlap test** | Code answering "are these two shapes in the same place?" |
| **Collision response** | What *happens* once a collision is detected. |
| **Tunnelling** | Passing through something because one frame's step was too big. |
| **Euclidean distance** | Ordinary straight-line distance. The Pythagoras one. |
| **Broad phase** | A quick first pass that throws out pairs which obviously cannot touch. |

---

## Recap

- Wrap things in rectangles and test the rectangles. **Four conditions, all joined by `and`.**
- Remember it by asking the *opposite* question: when can they definitely **not** touch?
- Detection is half the job; **response** is the other half. Fix the position, then the velocity.
- Where the ball hits the paddle should change where it goes. That is design, not physics.
- Circles use Pythagoras, and you can skip the square root when you are only comparing.

---

## Stretch goals

1. **Bricks.** Add three rectangles that vanish when the ball hits them. You now have the core of
   Breakout, which is lesson 6.
2. **A better bounce.** Make the ball speed up slightly on every paddle hit. Find a rate that makes
   rallies exciting rather than impossible.
3. **Debug view.** Draw every hitbox as an outline when a key is held. This is how real developers
   debug collisions, and it will save you hours in lesson 6.
4. **Circle versus box.** Write a proper circle-against-rectangle test rather than boxing the ball.
   (Hint: find the point on the rectangle closest to the circle's centre, then measure to it. This is
   genuinely harder than it looks.)
5. **Tunnelling, for real.** Set the ball's speed to 3000 and watch it pass through the paddle. Then
   fix it. Any fix that works counts.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Play 30 seconds of real Pong. Then ask: "what does the computer actually have to work out?" Let them say "if they're touching" and then ask *how*. |
| 10–30 | **Concept.** The AABB visualizer. Spend real time on the "find three green and one red" hunt — it is the whole lesson. Then the opposite-question framing on the board. |
| 30–40 | **Live-code** `boxesOverlap` together. It is only four lines and they should type all four. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D: Pong part 1. |
| 120–140 | Break-it-on-purpose. Do the fast-ball tunnelling one together, on the projector. |
| 140–150 | Recap. Next lesson it becomes a real game with a score. |

**What usually goes wrong**

1. **The ball sticks inside the paddle, vibrating.** They flipped the speed without fixing the
   position. Exactly the lesson 2 wall bug in a new costume — point that out, because noticing that
   two bugs are the same bug is a genuinely valuable skill.
2. **Comparing the ball's centre to the paddle's corner.** Mixing coordinate conventions. Have them
   draw the two boxes on paper with the x values labelled.
3. **`||` instead of `&&`.** The ball bounces off things on the far side of the screen. The AABB
   visualizer makes this obvious if you put it back up.
4. **The ball goes through the paddle occasionally.** Usually genuine tunnelling if they have raised
   the speed, but sometimes they only test one of the two paddles.
5. **The ball bounces but always at the same angle**, so rallies become boring. They have skipped the
   `hitOffset` part. It is the difference between a demo and a game — insist on it.

**If you are running short on time** — one paddle, and bounce the ball off the opposite wall instead
of a second paddle. Cut the `hitOffset` steering to a handout note. Do **not** cut the "fix position
then velocity" rule.

**For the student who finishes at minute 90** — stretch goal 3 (a debug view that draws every
hitbox) is the most valuable one, because it will make lesson 6 dramatically easier for them and
they will show everyone else. Stretch goal 4 (circle versus rectangle) is a genuinely hard problem
and will absorb a strong student for the rest of the lesson.

**The idea to land at the end:** turning a hard question ("when do they overlap?") into an easy
opposite ("when can they definitely not?") is a technique, not a trick about rectangles. Say it
explicitly. It comes back in the advanced level when they meet broad-phase collision, which is the
same move applied to whole groups of objects at once.
