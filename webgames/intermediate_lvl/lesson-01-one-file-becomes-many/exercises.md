# Lesson 1 — One File Becomes Many

## Cheat sheet

### The one rule

Draw an arrow from each file to every file it needs. **No loops allowed.**

```
main.js → game.js → { input.js, entities.js, render.js } → config.js
```

`config.js` needs nothing. `input.js` needs nothing. Those two are the most
reusable files you own, and that is *why*.

### Option A — script tags (works by double-clicking)

```html
<script src="config.js"></script>
<script src="input.js"></script>
<script src="entities.js"></script>
<script src="render.js"></script>
<script src="game.js"></script>
<script src="main.js"></script>
```

Order is forced, not chosen. One global name per file:

```js
const Config = { BALL_SPEED: 260 };
```

### Option B — modules (needs a local server)

```js
// config.js
export const BALL_SPEED = 260;

// game.js
import { BALL_SPEED } from "./config.js";
import * as Render from "./render.js";
```

```html
<script type="module" src="main.js"></script>
```

The `./` and the `.js` are both required.

### Modules need a server

Double-clicking gives you:

```
blocked by CORS policy
```

Because every local file is its own origin. Fix:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. No internet involved.

### What modules give you that script tags do not

| | tags | modules |
|---|---|---|
| order | by hand | worked out |
| names | global | private |
| strict mode | off | always on |

### A cycle

`game.js` imports `hud.js`, `hud.js` imports `game.js`:

```
ReferenceError: Cannot access
'state' before initialization
```

Fix, in order of preference: **pass the value in** · move the shared thing to a
third file · admit they are one file.

### Words

**Coupling** — how much A relies on B's insides. Low is good.
**Cohesion** — how much one file's contents belong together. High is good.
**Entry point** — the single file the page loads.
**Topological order** — an order where nothing comes before what it needs.

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> Give two symptoms of a file that has grown too large. Neither may be an error message.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does an arrow from <code>game.js</code> to <code>config.js</code> mean, in words?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> <code>input.js</code> never mentions the ball, the paddle or Breakout. Why is that worth having?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Name three things <code>type="module"</code> gives you that six <code>&lt;script&gt;</code> tags do not.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why can a module not be <code>import</code>ed from a file opened by double-clicking? Name the fix.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Define <em>coupling</em> and <em>cohesion</em>, and say which you want high.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

**Write your answer down before you run anything.**

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> These tags are in this order. What happens, and what does the console say?

```html
<script src="main.js"></script>
<script src="config.js"></script>
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>audio.js</code> has <code>console.log("starting up")</code> at the top level. Four different modules import it. How many times does the message print, and why?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> What does this print, and what would the same two lines have done in a plain <code>&lt;script&gt;</code>?

```js
// inside a module
scoer = 10;
console.log("ok");
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> Work out a safe load order for these five files, or explain why there is not one.

```
a.js needs b.js, c.js
b.js needs d.js
c.js needs d.js
d.js needs nothing
e.js needs a.js
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> Now <code>d.js</code> also needs <code>a.js</code>. What changes about your answer to B4?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The console says <code>Failed to resolve module specifier "config.js"</code>. There is nothing wrong with <code>config.js</code> itself. What is wrong?

```js
import { BALL_SPEED } from "config.js";
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> <code>render.js</code> loads, with no error, and <code>Config.INK</code> is <code>undefined</code>. Both files are listed in <code>index.html</code>. Name two different possible causes.

```html
<script src="render.js"></script>
<script src="config.js"></script>
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> This is in <code>entities.js</code>. The game runs, but the author has made a design mistake that will cost them later. What is it, and what should they do instead?

```js
import { ctx } from "./main.js";

export function drawBall(ball) {
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
  ctx.fill();
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> <code>hud.js</code> throws <code>ReferenceError: Cannot access 'state' before initialization</code>, and nobody has edited <code>hud.js</code> for a week. What has happened, and what is the smallest fix?

```js
// hud.js
import { state } from "./game.js";
const startingLives = state.lives;
export function drawHud() { /* ... */ }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Take **your own Breakout** from the beginner capstone — or `code/01-one-big-file.html`
if you would rather start from ours — and split it up.

The rule for today: **move code, do not change code.** When you finish, the game
must play exactly as it did at the start. If you spot something you want to
improve, write it on a sticky note and improve it tomorrow.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Before touching anything: write the list of files you intend to end up with, and draw the arrows between them. Show somebody. Two minutes here saves twenty later.</li>
<li><strong>Checkpoint 2.</strong> Make <code>config.js</code> and move every tuning number into it. Reload. The game still works and your main file is shorter.</li>
<li><strong>Checkpoint 3.</strong> Make <code>input.js</code>. When you have finished, search it for the words "ball", "paddle" and "brick". If you find any, the boundary is in the wrong place.</li>
<li><strong>Checkpoint 4.</strong> Make <code>render.js</code>. It must be the <em>only</em> file containing the text <code>ctx.</code> — search the others and prove it.</li>
<li><strong>Checkpoint 5.</strong> Make <code>entities.js</code> and <code>game.js</code>. The split: entities know <em>how</em> to move, game knows <em>what it means</em>. A ball falling off the bottom is <code>entities</code> reporting and <code>game</code> deciding.</li>
<li><strong>Checkpoint 6.</strong> Get <code>main.js</code> under fifteen lines. Then play the game for a full minute and compare it against the original, side by side, on two tabs.</li>
<li><strong>Checkpoint 7.</strong> Draw the arrows again, from the real <code>&lt;script&gt;</code> or <code>import</code> lines. Compare with checkpoint 1. Where you disagreed is where you learned something.</li>
</ul>

<div class="note">
<span class="note-label">If you have a terminal</span>
<p>Convert your split to modules afterwards: add <code>export</code>, add the
<code>import</code> lines, replace the six tags with one
<code>&lt;script type="module" src="main.js"&gt;&lt;/script&gt;</code>, and serve the folder with
<code>python3 -m http.server 8000</code>. If you do not have a terminal, stop at
checkpoint 7 — you have done the part that matters.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on your reasoning, and on whether you name what your idea costs as well
as what it gains.</p>
</div>

**E1.** Should `entities.js` know how to *draw* a ball, or should `render.js` know how
to draw a ball? Argue both sides, then pick one and say what it costs you.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** You are adding a second game mode: the paddle is at the top and the ball
falls upwards. Which of your files would you have to edit? If the answer is "most
of them", propose better boundaries.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** `config.js` holds both `BALL_SPEED` and the level layout. Use the
change-together test on that decision. What happens when you have twelve levels?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** The hard one. You want to run 10,000 frames of your Breakout with **no
browser window at all**, to prove the ball can never escape the walls. Which of
your files could run with no canvas, and which could not? What would you move?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Get `main.js` under ten lines.
2. Write a second `render.js` that draws the game with text characters, and switch
   between them by editing one line.
3. Add mouse control to `input.js` without editing `game.js` at all.
4. Draw your dependency graph, then create a cycle on purpose and watch what the
   browser says.
5. Attempt E4 for real: run your game rules in Node, with no browser.
