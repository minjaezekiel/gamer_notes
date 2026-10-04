# Lesson 1 — What Is A Game, Really?

> **Web Games · Beginner level · Lesson 1 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A black rectangle on a web page with a blue square sliding across it, driven by a
**real game loop** — the same structure used by every game you have ever played, from
Minecraft to Mario to Fortnite.

```
┌──────────────────────────────────────┐
│                                      │
│                                      │
│        ■  ───────────────→           │
│                                      │
│                                      │
└──────────────────────────────────────┘
       your square, moving on its own
```

It will not be impressive to look at. It will be the most important thing you build in this
course, because everything else is this with more stuff added.

## Where this fits

- **Back:** nothing. This is lesson 1.
- **Forward:** [lesson 2](../lesson-02-moving-pictures/notes.md) makes that movement smooth and
  fair on any computer.
- **Sideways:** students on the Python and C++ tracks are writing the *same loop* today in a
  different language. That is deliberate, and by lesson 6 you will see why.

---

## The idea, in plain words

### A game is not like other programs

Think about a calculator. You type `7 × 8`, it answers `56`, and it stops. It does its job once
and waits. Most programs you have written probably work like that: run, print something, finish.

A game cannot work like that. Mario does not wait politely for you to press a key and then move
one step. The world keeps going. Goombas walk, the timer counts down, the music plays — and all
of that happens whether you touch the controller or not.

So a game is a program that **never finishes**. It does the same small amount of work over and
over, extremely fast, until you quit.

### The flipbook

Have you ever drawn a flipbook — a stick figure in the corner of a notebook, slightly different
on each page, so that riffling the pages makes it move?

A game is exactly that. The screen shows a still picture. Then it is replaced with another still
picture where everything has moved a tiny bit. Then another. About **60 times every second**.

Nothing on your screen is actually moving. You are looking at a very fast slideshow, and your eyes
do the rest.

> **Where the analogy stops.** In a flipbook, all the pages are drawn in advance. In a game, each
> page is drawn *just before you see it*, which is why the game can react to the button you pressed
> a fraction of a second ago. That difference is what makes it a game rather than a video.

### The three jobs

To make each new page, the game does three jobs, always in this order:

| Job | In plain words | If you skipped it |
|---|---|---|
| **1. INPUT** | What is the player asking for? Which keys are held down? | The game ignores the player entirely. |
| **2. UPDATE** | Change the numbers. Move things, check collisions, add to the score. | Nothing ever changes. A frozen picture. |
| **3. RENDER** | Erase the screen, then draw everything where it is now. | Things move, but you never see it. |

Then it goes back to job 1 and does all three again. And again. Forever.

That repeating cycle has a name: the **game loop**. It is the single most important idea in this
entire course.

### What the game remembers

Between one page of the flipbook and the next, the game has to remember things: where the player
is, how many lives are left, what the score is. All of those remembered numbers together are
called the game's **state**.

That is really all a game is:

> **A game is some numbers (state), a rule for changing them (update), and a way of showing them to
> you (render) — repeated forever.**

Everything else — graphics, sound, physics, enemies — is detail layered on top of that sentence.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:**

1. Press **Step 1 frame** three times, slowly. Each press does **one job**, not one whole frame.
   Watch which box lights up.
2. During **UPDATE**, look closely at the screen on the right. The square's `x` number has already
   changed, but the picture still shows it in the old place. *The number moved; the pixels have
   not.* That gap is the whole reason we keep update and render separate.
3. During **RENDER**, the picture catches up and the frame counter goes up by one.
4. Now press **Play**. The same three jobs are still happening in the same order — just too fast
   for you to see them. That is the only difference between a stepping game and a playing game.

---

## The idea, in code

### Step 1: a place to draw

A web page cannot draw shapes on its own. You have to ask for a drawing area, called a
**canvas**.

Open `code/01-blank-canvas.html` in your browser. All it does is put a dark grey rectangle on the
page, but this is where the whole game will live.

```html
<!-- The canvas is the drawing area. The width and height are in PIXELS -
     dots on the screen. Our game world is 600 dots wide and 400 dots tall. -->
<canvas id="game" width="600" height="400"></canvas>

<script>
  // Find the canvas element on the page, by the id we gave it.
  const canvas = document.getElementById("game");

  // Ask it for a "2D drawing context". This object is the thing that actually
  // draws. Everyone calls it ctx, short for context, and so will we.
  const ctx = canvas.getContext("2d");

  // Pick a colour, then fill a rectangle with it.
  // The four numbers are: x, y, width, height.
  ctx.fillStyle = "#222222";
  ctx.fillRect(0, 0, 600, 400);
</script>
```

Two things worth noticing straight away:

- `ctx.fillStyle` is set **before** `ctx.fillRect`. The context works like a pen: you choose the
  colour, *then* you draw. If you set the colour afterwards, it affects the next thing you draw,
  not the thing you just drew. This trips up almost everyone once.
- The position `(0, 0)` is the **top-left corner** of the canvas, not the middle and not the
  bottom. You will meet that properly in lesson 2, and it is stranger than it sounds.

### Step 2: draw something

Now add a square. Open `code/02-first-square.html`.

```javascript
// The game's STATE: everything it needs to remember.
// Right now that is just where the square is.
let squareX = 50;
let squareY = 180;

ctx.fillStyle = "#222222";
ctx.fillRect(0, 0, 600, 400);      // the background

ctx.fillStyle = "#4a9eff";
ctx.fillRect(squareX, squareY, 40, 40);   // the square, 40 by 40 pixels
```

Notice that the square's position lives in **variables**, not in the `fillRect` call. That looks
like extra work right now. It is the reason the next step is possible at all: a number in a
variable is a number you can change, and a game is nothing but numbers being changed.

### Step 3: make it a loop

Here is the whole idea. Open `code/03-the-loop.html`.

```javascript
let squareX = 50;        // the state
const squareY = 180;

function update() {
  // JOB 2: change the numbers.
  squareX = squareX + 2;          // move 2 pixels to the right
}

function render() {
  // JOB 3: draw everything where it is NOW.
  ctx.fillStyle = "#222222";
  ctx.fillRect(0, 0, 600, 400);                 // erase by painting over it
  ctx.fillStyle = "#4a9eff";
  ctx.fillRect(squareX, squareY, 40, 40);       // then draw the square
}

// This function is one frame: one page of the flipbook.
function frame() {
  update();
  render();

  // Ask the browser to call frame() again for the next page.
  // THIS is what makes it a loop.
  requestAnimationFrame(frame);
}

frame();      // start it off
```

`requestAnimationFrame` is a long name for a simple request: *"call this function again when you
are ready to draw the next picture."* The browser answers about 60 times a second, which is why
games run at about 60 frames per second.

Notice that `frame()` calls `requestAnimationFrame(frame)`, which will later call `frame()` again,
which will ask again... That is the loop. There is no `while` anywhere, and yet it never stops.

> **Why not just use a `while (true)` loop?**
> Because a browser runs your code and draws the page using the same single worker. If you sat in a
> `while (true)` loop, you would never give the browser a turn to actually put anything on screen,
> and the tab would freeze. `requestAnimationFrame` means *"I'm done for now, call me back"*, which
> hands control back to the browser between frames. On the Python and C++ tracks you will write a
> real `while` loop, because there the situation is different.

### Step 4: why you must erase

Open `code/04-forgetting-to-erase.html` and run it. The square smears across the screen in a long
streak.

Delete this one line and you get that bug:

```javascript
ctx.fillRect(0, 0, 600, 400);     // the line that erases the old picture
```

The canvas does not clean itself. Whatever you drew last frame is still there. If you draw the
square in a new position without erasing, you now have two squares. After 200 frames you have 200
squares.

This is why RENDER is one job and not two: **erase, then draw everything**. Every frame. In that
order.

---

## The maths you just used

Almost none, and that is on purpose.

The only arithmetic in this lesson is `squareX = squareX + 2`, which reads as *"the new x is the
old x plus 2"*. The `=` here does **not** mean "equals" the way it does in maths class. In maths,
`x = x + 2` is nonsense, because nothing can be two more than itself. In programming, `=` means
**"work out the right-hand side, then store the answer in the thing on the left"**.

If that bothers you, it should — it is one of the genuinely confusing things about programming
notation, and it has confused every programmer who ever lived. Some languages write it `x := x + 2`
to be clearer about it. Read `=` as *"becomes"* and it will stop feeling wrong.

The real maths arrives in lesson 2, where it turns out that moving `2` each frame is actually a bug.

---

## Break it on purpose

Open `code/03-the-loop.html` in a text editor. Make one change at a time, **write down your
prediction first**, then reload the page and see.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| `squareX + 2` → `squareX + 10` | | |
| `squareX + 2` → `squareX - 2` | | |
| Delete the `ctx.fillRect(0, 0, 600, 400)` line in `render` | | |
| Swap the order so `render()` runs before `update()` | | |
| Delete the `requestAnimationFrame(frame)` line | | |
| Move `frame()` at the bottom *above* the `function frame()` definition | | |

The last two are the interesting ones. One of them makes the game draw exactly one frame and stop
— which tells you something about what the loop is really doing. The other still works, and the
reason why is a genuine quirk of JavaScript worth asking about.

---

## Think like an engineer

A game runs its loop about 60 times a second whether or not anything is happening. A chess program
does not: it waits, possibly for several minutes, until you move a piece. Both are games.

1. Write down three games that need a continuous loop, and three that could just wait for input.
2. Now try to state the rule in one sentence. What exactly is the difference between the two
   groups?
3. Here is the hard part. A chess program *could* be written with a 60-times-a-second loop that
   mostly does nothing. What would that cost? And a continuous game *could* be written to only
   update when a key is pressed — what would break?
4. Think about a phone running on battery. Does that change your answer?

There is no single right answer here. Real engines make this choice differently depending on what
they are for, and a good answer names the trade-off rather than picking a winner.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Frame** | One trip around the loop. One picture. One page of the flipbook. |
| **Frame rate** | How many frames happen per second. Written **fps**. Usually about 60. |
| **Game loop** | The input → update → render cycle that repeats forever. |
| **State** | All the numbers the game is currently remembering. |
| **Canvas** | The rectangle on a web page that you are allowed to draw in. |
| **Context** (`ctx`) | The object that does the actual drawing. Works like a pen. |
| **Render** | To draw the current state onto the screen. |

---

## Recap

- A game is a program that **never finishes**: it repeats three jobs forever.
- Those jobs are **input, update, render**, in that order, and keeping them separate prevents a
  whole category of confusing bugs.
- **State** is everything the game remembers between frames.
- The canvas does not clear itself. **Erase first, then draw.**
- Smooth motion is an illusion built from about 60 still pictures a second.

---

## Stretch goals

Only if you finished early. None of these are required.

1. **Two squares.** Add a second square that moves in the opposite direction. How many new
   variables did you need? Could you have done it with fewer?
2. **Bounce.** Make the square turn around when it reaches the right edge instead of disappearing.
   You will need an `if` and a variable holding which way it is going. (This is lesson 2's job, so
   you are working ahead — good.)
3. **A trail.** Instead of erasing completely, erase with a *see-through* black:
   `ctx.fillStyle = "rgba(0, 0, 0, 0.08)"`. Explain why this produces a fading trail, and why it
   is not actually a bug fix for lesson 4's smearing problem.
4. **Count the frames.** Add a counter that goes up each frame and draw it on screen with
   `ctx.fillText(count, 10, 30)`. Leave it running for ten seconds. Roughly what number do you get,
   and what does that tell you about your computer?

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Play 60 seconds of any well-known game on the projector. Ask: "how many pictures do you think you just looked at?" Let them guess, then tell them: about 3,600. |
| 10–25 | **Concept.** The game loop visualizer. Laptops closed. Step before you play. |
| 25–40 | **Live-code** `01` → `03` together, everyone typing. Do not paste; type it, with mistakes. |
| 40–50 | Break. |
| 50–120 | **Build.** Exercises section D. Circulate. |
| 120–140 | **Break it on purpose** table, then share-outs: "who made something weird happen?" |
| 140–150 | Recap, vocabulary, point at stretch goals. |

**What usually goes wrong**

1. **Nothing appears at all.** Nine times out of ten the `<script>` tag is *above* the `<canvas>`
   in the HTML, so `getElementById` runs before the canvas exists and returns `null`. Teach them to
   open the console (<kbd>F12</kbd>) and read the red text — this is the single most valuable habit
   of the whole course, and lesson 1 is the right time to install it.
2. **The square smears.** They deleted or never added the erase line. Let this happen. It is on the
   lesson plan as a discovery, not a mistake.
3. **`fillStyle` set after `fillRect`.** The square is the wrong colour. Ask "when does the pen
   change colour?"
4. **Typing `ctx.fillrect`** — JavaScript is case-sensitive and the error message is unhelpfully
   vague. Point at the console.
5. Someone will ask whether 60 fps is enough. It is a great question. The honest answer is "most
   people stop noticing around 60, competitive players disagree, and we will measure it in lesson
   2."

**If you are running short on time** — cut step 4 (the erase demonstration) from the live-code and
let them discover the smear themselves during the build. Cut the *Think like an engineer* discussion
to a single show-of-hands and set it as homework.

**For the student who finishes at minute 90** — stretch goal 2 (bounce) leads straight into lesson
2 and will keep them busy. If they finish that, ask them to make the square move in a circle. They
will need `Math.sin` and `Math.cos`, will not have met them, and working out what those do from
experiment is a genuinely good use of 30 minutes.

**One thing worth saying out loud at the end of this lesson:** everything they build for the rest
of the course is this file with more inside the `update()` and `render()` functions. Not a
different structure — the same one. Say it now and say it again in lesson 6.
