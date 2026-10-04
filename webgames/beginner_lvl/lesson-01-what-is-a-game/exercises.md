# Lesson 1 — What Is A Game, Really?

## Cheat sheet

### The three jobs, every frame

| | |
|---|---|
| **INPUT** | what is the player asking for? |
| **UPDATE** | change the numbers |
| **RENDER** | erase, then draw |

Then repeat. Forever. That is the **game loop**.

### The skeleton

```js
function update() {
  // change numbers only
}

function render() {
  // erase first
  ctx.fillStyle = "#222";
  ctx.fillRect(0, 0, 600, 400);
  // then draw
  ctx.fillStyle = "#4a9eff";
  ctx.fillRect(x, y, 40, 40);
}

function frame() {
  update();
  render();
  requestAnimationFrame(frame);
}
frame();
```

### Getting a canvas

```js
const canvas =
  document.getElementById("game");
const ctx = canvas.getContext("2d");
```

### Drawing

```js
ctx.fillStyle = "#4a9eff";   // colour FIRST
ctx.fillRect(x, y, w, h);    // then draw
```

`(0, 0)` is the **top-left** corner.

### Words

**Frame** — one trip round the loop, one picture.
**State** — everything the game remembers.
**fps** — frames per second, usually about 60.
**ctx** — the drawing context; works like a pen.

### The three rules worth memorising

1. Update changes numbers. Render draws. Never mix them.
2. The canvas never cleans itself. **Erase, then draw.**
3. Set the colour **before** you draw, not after.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Name the three jobs a game does every frame, in the correct order.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does the word <strong>state</strong> mean when we are talking about a game?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> A game runs at 60 frames per second. How many pictures does a player look at during a four-minute level? Show your working.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> On a canvas, where is the point <code>(0, 0)</code>?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Explain the flipbook comparison in your own words. Then say one way a game is <em>not</em> like a flipbook.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

**Write your prediction down before you run anything.** Being wrong on paper is where the learning
happens — nobody is marking whether you guessed right.

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> What does this draw? Be precise about the colour.

```js
ctx.fillRect(10, 10, 100, 50);
ctx.fillStyle = "red";
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> The square starts at <code>squareX = 50</code>. What is <code>squareX</code> after five frames, and how far has the square moved on screen?

```js
function update() {
  squareX = squareX + 2;
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> What appears on screen here, and why is it not what the author intended?

```js
function frame() {
  update();
  render();
  // requestAnimationFrame(frame);
}
frame();
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> This swaps two lines. Describe exactly what the player would see, and explain why it is nearly but not quite the same as the correct version.

```js
function frame() {
  render();
  update();
  requestAnimationFrame(frame);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> A student reports: &ldquo;my square leaves a long streak behind it, like a paint smear.&rdquo; Here is their <code>render</code>. What is missing, and why does that cause a streak rather than, say, nothing at all?

```js
function render() {
  ctx.fillStyle = "#4a9eff";
  ctx.fillRect(squareX, squareY, 40, 40);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Nothing appears at all, and the browser console says <code>Cannot read properties of null (reading 'getContext')</code>. What does that message mean in plain English, and what is wrong with this page?

```html
<script>
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
</script>

<canvas id="game" width="600" height="400"></canvas>
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> This square never moves, even though <code>update</code> looks correct. Why not?

```js
let squareX = 50;

function update() {
  let squareX = squareX + 2;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Work through these in order. Tick each checkpoint when it works. Reaching checkpoint 4 is a full
pass — 5 and 6 are there for people who are flying.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Make a new file called <code>mygame.html</code>. Get a canvas on the page, 600&times;400, with a dark background. Nothing else.</li>
<li><strong>Checkpoint 2.</strong> Draw a coloured square at a position held in two variables, <code>squareX</code> and <code>squareY</code>. Prove the variables are really being used by changing their values and reloading.</li>
<li><strong>Checkpoint 3.</strong> Add <code>update()</code>, <code>render()</code> and <code>frame()</code>, and get the square moving to the right on its own. Remember the erase.</li>
<li><strong>Checkpoint 4.</strong> When the square goes off the right edge, make it reappear on the left. <em>Careful:</em> if you reset it to <code>0</code> it will visibly pop. What value gives a smooth wrap-around?</li>
<li><strong>Checkpoint 5.</strong> Add a second square of a different colour, at a different height, moving at a different speed. How many new variables did you need?</li>
<li><strong>Checkpoint 6.</strong> Make one of the squares move diagonally &mdash; down as well as across &mdash; and bounce off the bottom edge.</li>
</ul>

<div class="note">
<span class="note-label">If you get stuck</span>
<p>Open the browser console with <kbd>F12</kbd> and read the red text. It tells you the file and the
line number. That one habit will save you more time this term than anything else in this handout.</p>
<p>And if nothing at all happens: are you editing the same file you are looking at in the browser?
Did you save it? Did you reload the page?</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>This is marked on your reasoning, not on reaching any particular conclusion. Say what your idea
costs as well as what it gains.</p>
</div>

A racing game runs its loop 60 times a second, non-stop. A chess program sits and waits, perhaps for
several minutes, until someone moves a piece. Both are games.

**E1.** List three games that need a continuous loop and three that could just wait for input.

<div class="lines"><i></i><i></i></div>

**E2.** In one sentence, what is the real difference between the two groups?

<div class="lines"><i></i><i></i></div>

**E3.** A chess program *could* be written with a 60-per-second loop that mostly does nothing at all.
What would that cost? Now think about a phone running on battery — does that change your answer?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** Going the other way: suppose you wrote a racing game that only updated when a key was
pressed. Describe exactly what the player would experience.

<div class="lines wide"><i></i><i></i><i></i></div>

---

## Stretch goals

Never required.

1. **Trail.** Erase with a see-through black (`ctx.fillStyle = "rgba(0,0,0,0.08)"`) instead of a
   solid one. Explain why this gives a fading trail.
2. **Frame counter.** Count frames, draw the number with
   `ctx.fillText(count, 10, 30)`, and leave it running for exactly ten seconds. What number do you
   get? What does that tell you about your computer?
3. **Circle.** Make a square travel in a circle. You will need `Math.sin` and `Math.cos`, which you
   have not been taught. Experiment: what does `Math.sin(t)` give you as `t` goes up?
4. **The hard one.** Two students' squares move at visibly different speeds on different laptops,
   with identical code. Why might that be? (This is lesson 2.)
