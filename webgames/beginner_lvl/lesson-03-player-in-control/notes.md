# Lesson 3 — Player In Control

> **Web Games · Beginner level · Lesson 3 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A paddle you steer with the arrow keys, which moves **smoothly and instantly**, with no pause and
no stutter — and which cannot be pushed off the edge of the screen.

```
┌──────────────────────────────────────┐
│                                      │
│                                      │
│                                      │
│            ▮▮▮▮▮▮▮▮                  │
│         ←  the paddle  →             │
└──────────────────────────────────────┘
```

Getting that to feel right is harder than it looks, and the way most people try first produces a
paddle that feels broken. That failure is today's lesson.

## Where this fits

- **Back:** [lesson 2](../lesson-02-moving-pictures/notes.md) gave you movement that is fair on any
  machine.
- **Forward:** [lesson 4](../lesson-04-when-things-touch/notes.md) makes things collide, and then
  you have Pong.
- **Today you finally fill in `readInput()`** — the empty function that has been sitting in your
  loop since lesson 1.

---

## The idea, in plain words

### The obvious approach, which does not work

The browser tells you when a key is pressed. So the obvious thing is to move the paddle right there:

```js
// THIS LOOKS RIGHT AND IS WRONG
document.addEventListener("keydown", function (event) {
  if (event.key === "ArrowRight") {
    paddle.x = paddle.x + 10;
  }
});
```

Try it (`code/01-the-wrong-way.html`). Hold the right arrow down. What happens?

1. The paddle moves once.
2. Then it **pauses** for about half a second.
3. Then it starts moving in jerky steps.

That is not a bug in your code. It is your **operating system's key-repeat setting** — the same thing
that makes `aaaa` appear in a text box when you hold a letter down. It was designed for typing, and
it is completely wrong for a game.

There are three more problems with this approach, and they are all worse than the stutter:

- **Movement is tied to the key-repeat rate**, not to your game loop. All of lesson 2's delta-time
  work is bypassed.
- **You cannot press two keys at once.** Try holding right *and* up. On most systems only the most
  recent key repeats, so diagonal movement is impossible.
- **It happens outside your loop.** The paddle can move in the middle of your `render()`, which is
  exactly the mixing-up of jobs that lesson 1 warned about.

### The idea that fixes everything

Stop asking *"what key was just pressed?"* Start asking **"which keys are held down right now?"**

The event handler does one job only: it writes down what changed. It never moves anything.

```js
const keys = {};      // an object that remembers which keys are down

document.addEventListener("keydown", function (event) {
  keys[event.key] = true;      // write it down. Move nothing.
});

document.addEventListener("keyup", function (event) {
  keys[event.key] = false;     // cross it out. Move nothing.
});
```

Then, once per frame, inside `update()`, you **ask**:

```js
function update(dt) {
  if (keys["ArrowRight"]) {
    paddle.x = paddle.x + PADDLE_SPEED * dt;
  }
  if (keys["ArrowLeft"]) {
    paddle.x = paddle.x - PADDLE_SPEED * dt;
  }
}
```

Every single problem disappears at once:

- No stutter: the loop runs 60 times a second, every time, regardless of key repeat.
- Delta time works again, because the movement is back inside `update`.
- Two keys at once is automatic — `keys` can hold any number of `true` values.
- Input, update and render are properly separated, exactly as lesson 1 described.

This has a name. Reading the *current state* of the input each frame is called **polling**.
Reacting the instant something happens is **event-driven**. Games poll.

> **One thing worth noticing.** The event handler and the game loop are now almost completely
> independent. The handler does not know a game exists; it just maintains a little record of reality.
> The loop does not know where the information came from. Swap the keyboard for a gamepad, or for an
> AI, and `update` never changes. That separation is worth more than the bug fix.

### Input is not the same as intent

There is one more idea here, and it is the one that separates a tidy game from a messy one.

`"ArrowRight"` is a fact about a keyboard. *"The player wants to go right"* is a fact about your
game. They are not the same thing, and keeping them apart pays off quickly:

```js
// Turn keyboard facts into game intentions, in one place.
const wantsLeft  = keys["ArrowLeft"]  || keys["a"] || keys["A"];
const wantsRight = keys["ArrowRight"] || keys["d"] || keys["D"];

if (wantsRight) { paddle.x += PADDLE_SPEED * dt; }
if (wantsLeft)  { paddle.x -= PADDLE_SPEED * dt; }
```

You have just added WASD controls to your entire game by editing two lines, and `update` never
mentions a key again. Add a gamepad later and you edit the same two lines.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html) again — but this time
watch only the **INPUT** box.

**What to look for:** step through a few frames. Notice that INPUT happens *every single frame*, even
when nothing has changed, and that it does not move anything. It only records "the right arrow is
held down". The movement happens later, in UPDATE. That gap between *noticing* and *acting* is the
whole lesson, and it is why your paddle will feel smooth.

---

## The idea, in code

### Step 1: the keys object

```js
// An empty object. We will fill it in as keys go up and down.
const keys = {};

document.addEventListener("keydown", function (event) {
  keys[event.key] = true;
  // Stop the arrow keys from scrolling the page while you play.
  if (event.key.startsWith("Arrow")) { event.preventDefault(); }
});

document.addEventListener("keyup", function (event) {
  keys[event.key] = false;
});
```

`event.key` is a string: `"ArrowLeft"`, `"a"`, `" "` for the space bar. So `keys` ends up looking
like `{ ArrowLeft: false, ArrowRight: true }`.

> **A key that is not in the object at all** gives `undefined`, which JavaScript treats as false in
> an `if`. So you never have to set up the object in advance — asking about a key nobody has touched
> simply answers "no".

### Step 2: move in update, not in the handler

```js
const paddle = { x: 260, y: 350, width: 80, height: 14 };
const PADDLE_SPEED = 420;      // pixels per SECOND

function update(dt) {
  if (keys["ArrowRight"] || keys["d"]) {
    paddle.x = paddle.x + PADDLE_SPEED * dt;
  }
  if (keys["ArrowLeft"] || keys["a"]) {
    paddle.x = paddle.x - PADDLE_SPEED * dt;
  }
}
```

### Step 3: keep it on the screen

Without this, the player can drive the paddle straight off the edge of the screen.

```js
  // Clamp: never less than 0, never further right than the canvas allows.
  if (paddle.x < 0) {
    paddle.x = 0;
  }
  if (paddle.x + paddle.width > canvas.width) {
    paddle.x = canvas.width - paddle.width;
  }
```

That is the same **clamping** idea you used on `dt` in lesson 2: force a number to stay inside
sensible limits. You will use it constantly.

### Step 4: the mouse, which is easier

```js
canvas.addEventListener("mousemove", function (event) {
  // event.clientX is where the mouse is on the whole PAGE. We want where it
  // is on the CANVAS, so we subtract the canvas's own position.
  const bounds = canvas.getBoundingClientRect();
  const mouseX = event.clientX - bounds.left;

  // Centre the paddle on the pointer rather than putting its left edge there.
  paddle.x = mouseX - paddle.width / 2;
});
```

Notice this one *does* set the position directly in the handler, and that is acceptable here:
`mousemove` reports a position rather than a repeating button, so there is no stutter to avoid. Even
so, the tidier version stores `mouseX` and lets `update` use it — and that is what you will want
once the paddle needs to be clamped, or slowed down, or frozen while the game is paused.

---

## The maths you just used

### The diagonal problem

Suppose you let the paddle move in all four directions:

```js
if (keys["ArrowRight"]) { player.x += 300 * dt; }
if (keys["ArrowDown"])  { player.y += 300 * dt; }
```

Hold both and the player moves 300 across **and** 300 down. How fast are they actually going?

By Pythagoras, their real speed is:

```
√(300² + 300²) = √180000 ≈ 424 pixels per second
```

That is about **41% faster diagonally**. Players discover this within about a minute and then run
everywhere diagonally, because you accidentally rewarded it.

You will fix this properly in the intermediate level with vectors. The quick version, if you want it
today, is to divide by `√2 ≈ 1.414` when both directions are active.

Today's paddle only moves along one axis, so the bug cannot bite yet — but now you know it is
waiting.

---

## Break it on purpose

Use `code/03-paddle.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Move the `paddle.x +=` lines into the `keydown` handler | | |
| Delete the `keyup` listener | | |
| Remove the clamping | | |
| Change `PADDLE_SPEED` to `2` (forgetting `* dt` means seconds) | | |
| Use `event.code` instead of `event.key`, keeping `"ArrowRight"` | | |
| Hold left and right at the same time | | |

The second one is worth sitting with: without `keyup`, every key you press stays `true` forever, so
the paddle gets stuck moving. The last one has an answer that depends on the exact order of your
`if`s, and it is a genuine design decision rather than a bug.

---

## Think like an engineer

You now have a paddle that moves at a constant speed the moment you press a key, and stops dead the
moment you let go. That is *responsive*. Is it *good*?

1. Think about a character in a platform game. When you let go of right, do they stop instantly? Why
   not? What would it feel like if they did?
2. Now the opposite: in a fighting game or a rhythm game, instant response is essential and any
   smoothing would be a defect. Why the difference?
3. **Design something.** Sketch how you would make the paddle speed up over about a quarter of a
   second instead of starting at full speed, and slide a little after you release. What new numbers
   would the paddle need to remember? (Hint: it already remembers a position. What else is there?)
4. **The hard one.** A player presses the jump button a few milliseconds *before* landing, and
   nothing happens, so the jump is lost and it feels like the game ignored them. Almost every good
   platform game solves this. How would you? What would you have to store, and for how long?

Question 4 has a real name and a real implementation used in essentially every well-regarded
platformer. Try to invent it before you look it up — your version will probably be close.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Polling** | Asking "what is the state right now?" every frame. What games do. |
| **Event-driven** | Reacting the instant something happens. What web pages do. |
| **Key repeat** | The operating system re-sending a held key, designed for typing. |
| **Clamping** | Forcing a value to stay within limits. |
| **Intent** | What the player *wants*, as opposed to which key they pressed. |
| **`event.key`** | The character the key produces, e.g. `"a"`, `"ArrowLeft"`. |
| **`event.code`** | The physical key's location, e.g. `"KeyA"`. Unaffected by keyboard layout. |

---

## Recap

- Never move things inside the event handler. **Record the state; move in `update`.**
- A `keys` object plus `keydown` / `keyup` is all you need, and it handles multiple keys for free.
- Games **poll** input once per frame. Web pages are event-driven. Know which you are writing.
- **Clamp** the player's position so they cannot leave the screen.
- Translate keys into **intent** in one place, and adding new control schemes becomes trivial.

---

## Stretch goals

1. **Two players.** Add a second paddle on W/S or A/D. How much did you have to change?
2. **Mouse and keyboard together.** Support both, and decide what happens if someone uses both at
   once. There is no obviously correct answer — justify yours.
3. **Acceleration.** Give the paddle a `speed` that builds up and decays rather than snapping to full
   speed. Try a few values and find one that feels good. This is *game feel*, and it is a real skill.
4. **Just-pressed.** Make the paddle teleport to the centre when the space bar is pressed — but only
   **once per press**, not continuously while held. You will need to remember what `keys` looked like
   last frame. (This is genuinely tricky and extremely useful.)
5. **Key viewer.** Draw every currently-held key name on screen. Then press several at once and find
   out how many your keyboard can actually report. Most cheap keyboards give up at three, which is a
   real constraint in local multiplayer games.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Run `01-the-wrong-way.html` on the projector. Hold the arrow key. Let them watch the stutter. Ask what is wrong — they will blame the code. |
| 10–25 | **Concept.** Explain key repeat (demo it in a text box — that is the moment it clicks). Then the `keys` object idea on the board. |
| 25–40 | **Live-code** the keys object and the update-based movement. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D: the paddle. |
| 120–140 | Break-it-on-purpose. The missing-`keyup` one is the most instructive. |
| 140–150 | Recap. Lesson 4 is Pong — tell them. |

**What usually goes wrong**

1. **The paddle never stops.** No `keyup` listener, so the key stays `true` forever. Very common.
2. **`keys["ArrowRight"]` never fires but `keys["arrowright"]` was typed.** Case-sensitive, and the
   capital letters in `ArrowRight` are not obvious. Suggest they `console.log(event.key)` and press
   keys — that habit answers this class of question permanently.
3. **The page scrolls while they play.** Needs `event.preventDefault()`. Worth explaining rather than
   just handing over: the browser has a default behaviour for arrow keys and you are overriding it.
4. **The paddle moves at a bizarre speed.** They kept lesson 1 numbers (`+ 5`) alongside `* dt`, so
   the paddle crawls at 5 pixels per second. Ask them what units their number is in.
5. **Holding left and right does nothing / does something odd.** Depends on their `if` order. This is
   a genuine design decision — most games let the most recent key win. Worth two minutes.

**If you are running short on time** — skip the mouse section entirely; it is in the code examples
for anyone who wants it. Cut the intent-mapping discussion and just use arrow keys.

**For the student who finishes at minute 90** — stretch goal 4 ("just pressed") is the best one.
It needs a `previousKeys` snapshot compared against `keys`, which is a genuinely new idea and is
exactly how real engines implement `wasPressedThisFrame`. Several students will try to solve it with
a flag and discover why that gets messy with more than one key.

**The point to land at the end:** `update()` does not know a keyboard exists. It asks "does the
player want to go right?" and something else answers. That is why swapping in a gamepad, a touch
screen, or a computer-controlled opponent in lesson 5 will be almost free.
