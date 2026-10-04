# Lesson 3 — Player In Control

## Cheat sheet

### Never move things in the handler

**Wrong** — stutters, ignores `dt`, no two keys at once:

```js
document.addEventListener("keydown", e => {
  if (e.key === "ArrowRight") x += 10;
});
```

**Right** — the handler only records:

```js
const keys = {};
document.addEventListener("keydown", e => {
  keys[e.key] = true;
  if (e.key.startsWith("Arrow")) e.preventDefault();
});
document.addEventListener("keyup", e => {
  keys[e.key] = false;
});
```

Then, once per frame:

```js
function update(dt) {
  if (keys["ArrowRight"]) x += SPEED * dt;
  if (keys["ArrowLeft"])  x -= SPEED * dt;
}
```

### Why the wrong way stutters

The OS repeats a held key for **typing**: one press, a pause of about half a second, then a repeat
rate. Your game loop runs 60 times a second regardless. Poll, do not react.

### Intent, not keys

```js
const wantsRight =
  keys["ArrowRight"] || keys["d"];
```

One place to change when you add WASD, a gamepad, or touch.

### Clamping

```js
if (x < 0) x = 0;
if (x + w > canvas.width)
  x = canvas.width - w;
```

### Mouse

```js
const b = canvas.getBoundingClientRect();
mouseX = event.clientX - b.left;
```

`clientX` is relative to the **window**, so you must subtract the canvas position.

### Words

**Polling** — asking every frame. Games do this.
**Event-driven** — reacting instantly. Web pages do this.
**`event.key`** — the character: `"a"`, `"ArrowLeft"`.
**`event.code`** — the physical key: `"KeyA"`.

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> Why does moving the paddle inside a <code>keydown</code> handler make it stutter?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What is the difference between <em>polling</em> and <em>event-driven</em> input? Which do games use?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> What does the <code>keys</code> object actually store? Give an example of what it might look like mid-game.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why is <code>event.preventDefault()</code> needed for the arrow keys?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Explain the difference between an input and an <em>intent</em>, and give one practical reason to keep them apart.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> The player presses the right arrow and holds it for exactly two seconds. <code>PADDLE_SPEED</code> is 420. How far does the paddle travel? Does your answer depend on the computer's frame rate?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What happens when the player presses the right arrow, holds it, and releases it? Describe the paddle's behaviour precisely.

```js
document.addEventListener("keydown", e => { keys[e.key] = true; });
// no keyup listener at all
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> The player holds <strong>both</strong> arrow keys at once. What does the paddle do, and why?

```js
if (keys["ArrowRight"]) { paddle.x += SPEED * dt; }
if (keys["ArrowLeft"])  { paddle.x -= SPEED * dt; }
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> A player moves right at 300 px/s and down at 300 px/s at the same time. How fast are they actually travelling? Show your working, and say why this is a problem for the game.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The paddle never moves at all, and the console shows no errors. What is wrong?

```js
document.addEventListener("keydown", e => { keys[e.key] = true; });
document.addEventListener("keyup",   e => { keys[e.key] = false; });

function update(dt) {
  if (keys["arrowright"]) { paddle.x += SPEED * dt; }
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The paddle moves correctly but can be driven completely off the right-hand side of the screen, where it disappears. The author thought they had handled it. What is wrong, and what should the second line be?

```js
if (paddle.x < 0) { paddle.x = 0; }
if (paddle.x > canvas.width) { paddle.x = canvas.width; }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> This mouse-controlled paddle is always offset to the right of the pointer by exactly the same amount, and the offset changes if the page is scrolled. Name both bugs.

```js
canvas.addEventListener("mousemove", function (event) {
  paddle.x = event.clientX;
});
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your lesson 2 bouncing ball, or from `code/02-the-keys-object.html`.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Add the <code>keys</code> object with both <code>keydown</code> and <code>keyup</code> listeners. Draw the list of currently-held keys on the canvas so you can see it working. Do not move anything yet.</li>
<li><strong>Checkpoint 2.</strong> Draw a paddle near the bottom of the canvas, with its numbers in a <code>paddle</code> object.</li>
<li><strong>Checkpoint 3.</strong> Make the arrow keys move it, <strong>inside <code>update</code></strong>, multiplied by <code>dt</code>. Hold the key down &mdash; it should glide, with no pause and no stutter.</li>
<li><strong>Checkpoint 4.</strong> Clamp it so it cannot leave the screen. Test by holding a key for several seconds.</li>
<li><strong>Checkpoint 5.</strong> Add WASD as a second control scheme, using the <em>intent</em> pattern &mdash; so <code>update</code> never mentions a key name directly.</li>
<li><strong>Checkpoint 6.</strong> Bring back your bouncing ball from lesson 2, so a ball bounces around while you steer the paddle. They will pass straight through each other; that is lesson 4's job.</li>
</ul>

<div class="note">
<span class="note-label">If the paddle gets stuck moving</span>
<p>Your <code>keyup</code> listener is missing or misspelled, so the key never gets set back to
<code>false</code>. Add a temporary line that draws the held-key list on screen and you will see it
immediately.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on your reasoning, and on whether you name what your idea costs.</p>
</div>

Your paddle starts at full speed the instant a key goes down and stops dead the instant it comes up.
That is maximally *responsive*. It is not obviously *good*.

**E1.** Think of a platform game character. When you let go of right, do they stop instantly? Why not?
What would it feel like if they did?

<div class="lines"><i></i><i></i><i></i></div>

**E2.** In a rhythm game or a fighting game, instant response is essential and any smoothing would be
a defect. What makes those different?

<div class="lines"><i></i><i></i></div>

**E3.** Design it. Sketch how you would make the paddle speed up over about a quarter of a second,
and slide a little after release. What extra numbers would the paddle have to remember?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. A player presses jump a few milliseconds *before* they land. Nothing happens,
the jump is lost, and it feels like the game ignored them. Almost every good platform game solves
this. How would you? What would you store, and for how long?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Two players on separate keys.
2. Support mouse and keyboard together — and decide what happens if both are used at once.
3. Acceleration and friction, tuned until it feels good.
4. **Just-pressed:** teleport the paddle to the centre when space is pressed, but only once per
   press, not continuously while held.
5. Draw every held key on screen, then find out how many your keyboard can report at once.
