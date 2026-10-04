# Lesson 1 — Solutions and marking notes

**Teacher-facing.** Section E has marking notes rather than answers, on purpose.

---

## Section A

**A1.** [3] INPUT, UPDATE, RENDER — in that order. One mark each; accept
"read the keyboard / change the numbers / draw it" as the names if the order is right.

**A2.** [2] Everything the game remembers between one frame and the next: positions, score, lives,
which level you are on. Accept any answer that conveys "the numbers the game is holding onto".

**A3.** [2] 4 minutes = 240 seconds. 240 × 60 = **14,400 frames**. One mark for the method, one for
the answer. Students who write 4 × 60 = 240 have found the seconds and stopped — give the method
mark.

**A4.** [2] The **top-left** corner of the canvas. Taking a mark off for "the corner" without
specifying which is harsh; ask them which corner instead.

**A5.** [3] Two marks for the comparison: the screen shows a still picture, which is replaced about
60 times a second, and your eyes turn that into movement. One mark for a difference. The one in the
notes is that a flipbook's pages are drawn in advance whereas a game's are drawn just before you see
them, which is why a game can react to you. Also accept: a flipbook is always the same length; a
game never ends; a flipbook cannot change based on what you do.

---

## Section B

**B1.** [3] A **black** rectangle at (10, 10), 100 wide and 50 tall. Black because no `fillStyle`
was set before the `fillRect`, and black is the default. The `"red"` on the second line affects
whatever is drawn *next* — which is nothing. The common wrong answer is "a red rectangle"; this is
exactly the mistake the question exists to catch, so mark it generously but make sure they
understand the pen metaphor afterwards.

**B2.** [3] `squareX` is 60. It has moved **10 pixels**. Watch for students who answer 10 for the
first part — they have given the distance moved rather than the value of the variable.

**B3.** [4] One single frame is drawn, and then everything stops. The square appears at its starting
position (having moved 2 pixels) and never moves again. The `requestAnimationFrame` line is what
asks for the *next* frame; with it commented out, `frame()` runs once and returns, and there is
nothing left to run. Good answers notice that the program has not crashed — it has simply finished.

**B4.** [4] It does work, and it looks almost identical. The difference is that every frame is drawn
using the state from *before* this frame's update, so the picture is exactly one frame behind — a
delay of about 1/60th of a second. Full marks for "it draws the old position, so everything is one
frame late". Strong answers point out that you would never notice with a square moving at 2 px per
frame, but that you very much would with fast input response, and that this is a real source of
"the controls feel laggy" bugs in student games.

---

## Section C

**C1.** [4] The erase is missing: there is no `ctx.fillRect(0, 0, 600, 400)` filling the background
before the square is drawn. Two marks for spotting it. Two more for *why a streak specifically*: the
canvas keeps whatever was drawn on it, so last frame's square is still there, and the frame before
that, and so on. The square is drawn every frame 2 pixels further along, and the old ones are never
removed, so the result is a solid bar. Students who say "it doesn't clear" get 2; push them to
explain the streak.

**C2.** [4] The message means `document.getElementById("game")` returned `null` — it found no
element with that id — and you cannot call `.getContext` on nothing. The cause is that the
`<script>` runs *before* the `<canvas>` exists, because the browser reads the file from top to
bottom. Fix: move the script below the canvas (or wrap it in a `DOMContentLoaded` listener, or add
`defer` to the script tag — accept any of these).

This question is worth spending time on. Reading an error message instead of being frightened by it
is the single most useful habit in the course.

**C3.** [3] `let squareX` inside `update` creates a **brand new variable** that exists only inside
that function, and it shadows the outer one. The outer `squareX` is never touched, so the drawing
never changes. (As a bonus, this specific code actually throws a `ReferenceError`, because the new
`squareX` is being read on the same line that declares it.) Fix: drop the `let`, so the line becomes
`squareX = squareX + 2;` and refers to the outer variable.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 4, the subtle bit.** Resetting to `squareX = 0` makes the square *pop* into existence
at the left edge. Resetting to `squareX = -SQUARE_SIZE` (that is, `-40`) starts it just off-screen
so it slides in smoothly. Students who notice this unprompted have understood something real about
game feel; say so.

**Checkpoint 5.** The expected answer is "three new variables" (x, y, speed) or two if they reuse the
size. The question underneath — which nobody will ask until lesson 6 — is whether this is a good way
to add a second thing. It is not, and the fact that a third square would need three more variables
again is exactly the pressure that makes arrays and objects feel necessary later. Plant the seed; do
not resolve it.

**Checkpoint 6.** Bouncing needs a *direction* variable, usually `speedY`, flipped with
`speedY = -speedY` at the edge. This is lesson 2's content arriving early, which is fine.

---

## Section E — marking notes, not answers

Mark on reasoning, not on conclusion. A student who disagrees with everything below and argues it
well gets full marks.

**E1/E2.** The distinction most students find is "does the world change when the player does
nothing?" That is a good answer. The more precise version is about whether the game has any
**time-dependent state**. Chess has none: the board is identical a minute from now unless someone
moves. A racing game has velocities, so it is different a sixtieth of a second from now.

Watch for the interesting edge cases students raise, because they are the best part of the
discussion:
- **Chess with a clock** — now it does change with time, and does need a loop (or at least a timer).
- **Animated menus** — the *game* is waiting, but the *screen* is not.
- **Turn-based games with animations** — Pokémon is turn-based, but the attack animations need a loop.

**E3.** Costs of looping unnecessarily: battery, heat, fan noise, and CPU that other programs could
be using. On a phone this is the whole argument — a chess app that pinned a core at 60 fps would be
uninstalled by lunchtime. Strong answers mention that most real applications are *event-driven* for
exactly this reason, and that games are the unusual case, not the normal one.

**E4.** The player would see the world freeze completely whenever they were not pressing something.
Let go of the accelerator and the car stops mid-air; enemies stand still; the lap timer pauses. Best
answers notice that this is essentially what a *turn-based* game is, and that some games — including
the excellent *Superhot* — make "time only moves when you do" the entire point. That is a genuinely
good observation and worth sharing with the class.

---

## Stretch goals

1. **Trail.** Each frame paints a thin, 8%-opaque black layer over everything. Old squares are not
   removed; they are *faded*, a bit more on each frame, so recent positions are dark and older ones
   are nearly gone. Worth asking: does the oldest square ever fully disappear? (In theory no, it
   just gets exponentially fainter; in practice it hits the limits of 8-bit colour and does.)
2. **Frame counter.** Expect roughly 600 after ten seconds on a 60 Hz display. A student with a
   120 Hz or 144 Hz gaming monitor will get 1,200 or 1,440 and should be asked, loudly, in front of
   the class, what that means for the square's speed. That question *is* lesson 2.
3. **Circle.** `x = centreX + Math.cos(t) * radius`, `y = centreY + Math.sin(t) * radius`, with `t`
   increasing a little each frame. They will not derive this; experimenting their way to it is the
   point, and discovering that sin and cos always stay between −1 and 1 is a real insight.
4. **The hard one.** This is lesson 2 in a sentence: moving "2 pixels per frame" means the speed
   depends on how many frames the computer manages per second. Do not answer it. Write it on the
   board and leave it there until next lesson.
