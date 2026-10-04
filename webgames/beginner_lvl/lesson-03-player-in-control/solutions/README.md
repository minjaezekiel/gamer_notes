# Lesson 3 — Solutions and marking notes

---

## Section A

**A1.** [2] The handler only runs as often as the operating system repeats a held key — one press,
a pause of roughly half a second, then a slow repeat — because key repeat was designed for typing.
The game loop runs 60 times a second regardless.

**A2.** [2] Polling = asking "what is the state right now?" every frame. Event-driven = reacting the
moment something happens. **Games poll.**

**A3.** [2] Which keys are currently held down, as a key-name → true/false map. Example:
`{ ArrowLeft: false, ArrowRight: true, a: false }`. Accept any sensible illustration.

**A4.** [2] The browser's default behaviour for the arrow keys is to scroll the page. Without
`preventDefault()` the page jumps around while you play.

**A5.** [3] An *input* is a fact about hardware (`"ArrowRight"` is down). An *intent* is a fact about
the game (the player wants to go right). Two marks. One mark for a practical reason — adding WASD,
a gamepad, touch controls, or remappable keys becomes a one-line change instead of a hunt through the
whole codebase.

---

## Section B

**B1.** [3] `420 × 2 = 840 pixels`. And **no**, it does not depend on the frame rate — that is the
entire point of multiplying by `dt`. Two marks for the number, one for the second part. (In practice
it will stop early, clamped at the screen edge; a student who spots that deserves credit.)

**B2.** [4] The paddle starts moving when the key goes down, and **never stops**. `keys["ArrowRight"]`
is set to `true` and nothing ever sets it back to `false`, so `update` keeps moving the paddle on
every frame forever. It will slide to the edge and stay jammed there against the clamp.

Full marks need "never stops", not just "it breaks".

**B3.** [3] **Nothing — the paddle stays still.** Both `if`s run: the first adds `SPEED * dt`, the
second subtracts the same amount, and they cancel exactly. Note this is not a crash or a bug, just a
consequence of the structure. Whether it is the *right* behaviour is a design question — see the
teaching note below.

**B4.** [4] `√(300² + 300²) = √180000 ≈ 424 px/s`. Two marks for the working, one for the number.
One mark for the problem: the player moves about **41% faster diagonally**, so players discover this
within a minute and run everywhere diagonally. The fix (vectors, normalising) comes at intermediate
level; dividing by `√2` is the quick version.

---

## Section C

**C1.** [3] Case. `event.key` gives `"ArrowRight"` with capital A and R, but the code tests
`"arrowright"`. JavaScript string comparison is case-sensitive, and an object lookup for a key that
does not exist returns `undefined`, which is falsy — so the `if` is simply never true and nothing
errors.

Teach the diagnostic rather than the answer: `console.log(event.key)` inside the handler, press a
key, read what it actually says. That habit solves this entire class of problem permanently.

**C2.** [4] It compares `paddle.x`, which is the paddle's **left edge**, against the right-hand wall.
So the paddle is only stopped once its *left* edge reaches the far side — by which point the whole
paddle is off screen. Two marks for identifying this.

Two marks for the fix:
```js
if (paddle.x + paddle.width > canvas.width) {
  paddle.x = canvas.width - paddle.width;
}
```
This is the same "which part of the object are you measuring?" mistake as lesson 2's C2, and it is
worth pointing out that it has now appeared twice.

**C3.** [4] Two separate bugs, two marks each:

1. `event.clientX` is measured from the left edge of the **window**, not the canvas. Subtract the
   canvas position: `event.clientX - canvas.getBoundingClientRect().left`. This also explains why
   scrolling changes the offset — the canvas moves within the window.
2. Setting `paddle.x` directly puts the paddle's **left corner** under the pointer, so it always
   appears offset to the right by half its width. Subtract `paddle.width / 2`.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 1** is worth insisting on even though it moves nothing. Students who can see the
`keys` object working have a debugging tool for the rest of the lesson, and the two most common bugs
(missing `keyup`, wrong capitalisation) become instantly visible instead of mysterious.

**Checkpoint 3.** Watch for anyone who has left the movement in the handler — easy to spot from
across the room, because their paddle stutters.

**Checkpoint 5.** The point is that `update` should read like
`if (wantsRight) { ... }` with no key names in sight. Students who write
`if (keys["ArrowRight"] || keys["d"]) { ... }` inline have the right behaviour but have missed the
idea; ask them what they would have to do to add a gamepad.

**Checkpoint 6** sets up lesson 4 and is worth reaching if there is time. The ball passing straight
through the paddle is a good cliffhanger — let them be annoyed by it.

---

## Section E — marking notes, not answers

**E1.** Real characters have **momentum**: they accelerate up to speed and decelerate down from it.
Instant stopping feels robotic and makes precise platforming oddly harder, because there is no
"feel" to read. Good answers mention that the smoothing is a *lie* — real people do not have
acceleration curves either — and that it is there because it feels right, not because it is accurate.

Accept the counter-argument too: *Celeste* and many precision platformers deliberately use very
short acceleration times, nearly instant, because precision matters more than weight.

**E2.** In rhythm and fighting games, the player's timing *is* the skill being tested, and any delay
between press and action is interference. Also these games are played at a level where a few
milliseconds are perceptible and competitively meaningful. Strong answers point out the general rule:
smoothing is good when it communicates *weight*, bad when it obscures *timing*.

**E3.** They need the paddle to remember a **current speed** as well as a position. Expected shape:

```js
if (wantsRight) { paddle.speed += ACCEL * dt; }
else if (wantsLeft) { paddle.speed -= ACCEL * dt; }
else { paddle.speed *= 0.85; }          // friction when nothing is held
paddle.speed = clamp(paddle.speed, -MAX, MAX);
paddle.x += paddle.speed * dt;
```

Full marks for realising that one new number (speed) is enough. Do not require the exact code.

**E4.** This is **input buffering** (sometimes "jump buffering"). The expected design: when the jump
key is pressed, store the time. On landing, check whether a jump was requested within the last ~100
milliseconds, and if so, jump immediately.

```js
if (justPressed("jump")) { jumpBufferedAt = now; }
if (onGround && now - jumpBufferedAt < 0.1) { jump(); jumpBufferedAt = -999; }
```

The matching trick in the other direction is **coyote time**: let the player jump for a short moment
*after* walking off a ledge. Both are in essentially every well-regarded platformer, and in neither
case does the game do what the player literally did — it does what they obviously *meant*.

**Do not give either name until after they have tried.** Students routinely invent buffering
unprompted, and telling them afterwards that it is standard practice with a name is a genuinely good
moment. Coyote time appears in lesson 12 of the intermediate level.

---

## Note on B3 for class discussion

"Both keys cancel out" is the behaviour this code happens to produce, not a decision anyone made.
Most commercial games instead make the **most recently pressed** key win, because a player
mid-direction-change briefly holds both and expects to turn, not to stop dead. Implementing that
needs remembering the order keys went down.

It is worth two minutes at the board, because it is a clean example of something that is not a bug,
is not a feature, and is simply an unexamined consequence — which describes a great deal of
real software.
