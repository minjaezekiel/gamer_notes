# Lesson 1 — One File Becomes Many

> **Web Games · Intermediate level · Lesson 1 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

Your Breakout from the beginner capstone, rebuilt as **six small files** — and a game that plays
exactly as it did before. Not one thing the player can see will change.

```
breakout/
├── index.html        the page. Loads things. Contains no game.
├── config.js         every number you might want to tune
├── input.js          keyboard in, intent out. Knows nothing about Breakout.
├── entities.js       the ball, the paddle, the bricks — data and behaviour
├── render.js         everything that touches the canvas
├── game.js           the rules: what happens, and in what order
└── main.js           the loop. Three lines of real work.
```

That "nothing changes" is the hard part and the whole discipline. A refactor that also adds a
feature is two changes tangled together, and when it breaks you will not know which half did it.

## Where this fits

- **Back:** [Breakout](../../beginner_lvl/lesson-06-capstone-breakout/notes.md) was about 300 lines in
  one file. It worked. That is exactly why it is worth taking apart — you already know what it does.
- **Forward:** every remaining lesson in this level adds a file to this shape. By lesson 12 you will
  have about fifteen, and you will still be able to find anything in under ten seconds.
- **Other tracks:** Python's intermediate lesson 2 and C++'s intermediate lesson 3 open with the same
  problem and reach almost the same answer, with different syntax. The shape is not a JavaScript idea.

---

## The idea, in plain words

### What is actually wrong with one big file

Nothing, while it is small. The beginner Breakout is fine. The trouble starts in a way that is easy
to miss, because none of these are error messages:

1. **You scroll to think.** Finding `updateBall` means hunting. You have started navigating your
   program instead of reading it.
2. **You are afraid of the file.** You want to change how bricks are laid out, and you are not
   certain that nothing else depends on it, so you leave it alone. Fear is a design smell.
3. **Names start colliding.** You already have `x`, so the paddle's gets called `px`, and later you
   cannot remember which is which.
4. **Two people cannot work on it.** Everybody edits the same lines.
5. **You cannot test any part on its own**, because no part exists on its own.

### The toolbox analogy, and exactly where it fails

A drawer with every tool in it works until it does not. A toolbox with trays — screwdrivers here,
sockets there — is not tidier for its own sake; it is faster to use, because the *place* tells you
what the thing is.

Here is where that analogy stops being true, and it matters: **a socket does not need a
screwdriver. Your code does need other code.** Trays are independent. Modules are not. Which means
splitting a program is not really about where things go. It is about **who is allowed to know about
whom**, and that is the actual lesson today.

### The one rule: dependencies point one way

Draw an arrow from a file to each file it needs. For Breakout:

```
        main.js
           │
           ▼
        game.js  ──────────┐
       ╱   │   ╲           │
      ▼    ▼    ▼          ▼
 input  entities  render   config
   .js     .js      .js      .js
```

Read it out loud: `main` needs `game`; `game` needs `input`, `entities`, `render` and `config`;
`config` needs nothing at all.

Two properties of that picture are worth more than the picture:

- **`input.js` does not know Breakout exists.** It reports which keys are down. You could drop that
  file into a racing game without editing a character. A file that knows nothing is a file you can
  reuse, and a file you can reuse is a file you understood well enough to isolate.
- **No arrow ever points back up.** `entities.js` must not need `game.js`. The moment it does, those
  two files are one file wearing two names: you cannot read, move, test or reuse either without the
  other.

When arrows do form a loop, that is a **circular dependency**, and it is the one genuinely nasty
failure in this lesson. We will build one on purpose later so that you recognise the symptoms, which
are strange: not an error about imports, but a value that is mysteriously `undefined`.

### How to decide where the line goes

A useful question, and a bad one.

The bad question is "what are the nouns in my game?" — it leads to a file per noun, which gives you
twenty files that all need each other.

The useful question is: **"what would I have to change together?"** Things that change together
belong together. Things that change for different reasons belong apart. Brick layout and brick
drawing change for completely different reasons — one when you design a level, the other when you
restyle the game — so they sit in different files.

Those two ideas have names, and they are the two most useful words in software design:

- **Cohesion** — how much the things inside one file belong together. You want this high.
- **Coupling** — how much one file depends on the insides of another. You want this low.

A file with high cohesion and low coupling can be understood on its own. That is the whole goal.

---

## The idea, in pictures

Open [the module dependency explainer](../../../shared/visualizers/module-dependencies.html).

**What to look for:** click an arrow to add or remove a dependency. The panel on the right works out
a safe **load order** — which file must be ready before which. Now make `input` depend on `game`,
which already depends on `input`. The order disappears, because there is no answer: each one needs
the other to go first. That is not the tool failing. That is a genuine impossibility, and it is what
a circular dependency *is*. Then watch what the suggested fixes do to the arrows.

---

## The idea, in code

Run `code/01-one-big-file.html` first. It is a small game in a single file, and it works. Read the
comment at the top — it points out the three places the file is already fighting you.

### Option A: several `<script>` tags and one shared object

This is the version that needs no tools, no server and no internet. You can split a program today
with nothing but extra `<script>` tags.

```html
<!-- index.html — ORDER MATTERS. The browser runs these top to bottom. -->
<script src="config.js"></script>    <!-- needs nothing -->
<script src="input.js"></script>     <!-- needs nothing -->
<script src="entities.js"></script>  <!-- needs config -->
<script src="render.js"></script>    <!-- needs config -->
<script src="game.js"></script>      <!-- needs all of the above -->
<script src="main.js"></script>      <!-- needs game. Last, always. -->
```

Every one of those files shares the same global space, so a name used twice is a real collision. The
fix is to give each file **one** global and hang everything off it:

```js
/* config.js
   One global object instead of twenty loose variables. Anything that reads
   Config.BALL_SPEED is saying out loud where that number comes from. */
const Config = {
  BALL_SPEED: 260,
  PADDLE_SPEED: 420,
  BRICK_ROWS: 4
};
```

```js
/* input.js
   Notice what is NOT in this file: the word "ball", the word "paddle", the word
   "Breakout". It reports facts about a keyboard. That is all it will ever do. */
const Input = {
  keys: {},

  start: function () {
    document.addEventListener("keydown", (e) => {
      Input.keys[e.key] = true;
      if (e.key.startsWith("Arrow")) { e.preventDefault(); }
    });
    document.addEventListener("keyup", (e) => { Input.keys[e.key] = false; });
  },

  // Intent, not keys — the pattern from beginner lesson 3, now with a home.
  wantsLeft:  function () { return Input.keys["ArrowLeft"]  || Input.keys["a"]; },
  wantsRight: function () { return Input.keys["ArrowRight"] || Input.keys["d"]; }
};
```

Full working version: `code/02-script-tags/index.html`. **It opens by double-clicking**, which is
why it is worth knowing even though the next option is tidier.

### Option B: real modules

Modern JavaScript has actual modules. Two keywords:

```js
/* config.js — `export` means "other files may use this name". */
export const BALL_SPEED = 260;
export const PADDLE_SPEED = 420;

export const LEVEL = [
  [1, 1, 1, 1, 1, 1],
  [1, 2, 2, 2, 2, 1],
  [0, 1, 1, 1, 1, 0]
];
```

```js
/* game.js — `import` names exactly what this file needs. The list at the top of
   a module is a readable statement of its dependencies. */
import { BALL_SPEED, LEVEL } from "./config.js";
import { createBall, updateBall } from "./entities.js";
import * as Render from "./render.js";       // everything, under one name

export function startGame() { /* ... */ }
```

```html
<!-- index.html — ONE script tag now, and the type attribute is not optional. -->
<script type="module" src="main.js"></script>
```

Four things modules do that script tags do not:

| | Script tags | `type="module"` |
|---|---|---|
| Load order | you maintain it by hand | worked out from the `import` lines |
| Names | shared globally, can collide | private to the file unless exported |
| Strict mode | off unless you ask | always on, so typos become errors |
| Runs when | immediately, blocking the page | after the HTML is parsed |

"Always on strict mode" sounds like paperwork and is a real gift: assigning to a variable you never
declared is an error in a module, and that typo is otherwise one of the hardest bugs to find in
JavaScript.

### The thing nobody warns you about: modules need a server

Open `code/03-modules/index.html` by double-clicking it. The game does not start. The console says
something close to:

```
Access to script at 'file:///.../main.js' from origin 'null' has been blocked
by CORS policy
```

Your code is fine. Here is what is happening.

A browser decides what a page is allowed to load using the page's **origin** — roughly, its
protocol, host and port. Pages opened from your disk have `file://` as their protocol, and the
browser treats **every single local file as its own separate origin**. So `main.js` counts as a
different website from `index.html`, and loading another website's script without permission is the
exact thing this rule exists to prevent. Plain `<script src="...">` predates the rule and is
exempt. `import` is not.

The fix takes one command and no internet, because the server runs on your own machine:

```bash
# in the folder that holds index.html
python3 -m http.server 8000
```

Then open <http://localhost:8000> instead of double-clicking. `localhost` means *this computer*; no
network is involved, and it works with the Wi-Fi switched off. Press `Ctrl+C` in the terminal to
stop it.

> **A choice to make honestly.** If your machine will not run that command — a locked-down school
> account, a Chromebook without a terminal — use Option A for the rest of this level. Every exercise
> works either way. You lose the private names and the automatic ordering; you lose nothing else.
> The examples in this level ship in both shapes for exactly that reason.

### A module runs once, no matter how many files import it

```js
/* audio.js */
console.log("audio.js is starting up");
export const ctx = new AudioContext();
```

Import that from four different files and the message prints **once**. The second import gets the
same object as the first. This is enormously convenient — it is how every file can share one audio
context without passing it around — and it is also a trap worth naming: a module's top-level code is
shared state. If two parts of your game change `Config.BALL_SPEED` at runtime, they are changing the
same thing, and whichever ran last wins. A single shared instance like this is called a
**singleton**.

### Building a circular dependency on purpose

`code/04-the-cycle/` contains two modules that import each other. Run it and read what it prints.

The message is **not** "circular import detected". It is:

```
ReferenceError: Cannot access 'state' before initialization
```

Here is why. To finish `game.js`, the browser must first finish `hud.js`. To finish `hud.js` it must
first finish `game.js` — which it has already started and cannot restart. So it carries on with a
**half-built** `game.js`, in which `state` has been reserved but not yet given a value. Reading it
there is the error above.

Two details that make these bugs slippery:

- **The error blames the wrong file.** It is raised in `hud.js`, the file that was waiting. The file
  that caused it is `game.js`, which is not mentioned.
- **The same cycle can be completely harmless.** Move that one line *inside* `drawHud()` and the
  program works. Nothing reads the half-built module until both files have finished loading, so the
  loop never shows. Function declarations are also hoisted, so a cycle where the two files only ever
  import each other's *functions* usually runs fine for months — until someone adds a `const` at the
  top of one of them, and then a file nobody touched starts throwing.

Three ways out, in order of how often they are the right answer:

1. **One of them should not need the other.** Usually the lower-level file is reaching upwards. Here,
   `hud.js` wants the score — so let whoever calls it *pass the score in*: `drawHud(score)`. The
   arrow disappears. This is the answer about four times out of five.
2. **Move the shared thing to a third file.** If both genuinely need the same data, that data belongs
   somewhere both can point down at — `state.js`. Two arrows down, no loop.
3. **Merge them.** If you honestly cannot separate them, they were one module all along, and the
   split was wishful thinking.

---

## The maths you just used

That arrow diagram is a **directed graph**: files are *nodes*, dependencies are *edges*, and the
edges have a direction. A loop of edges is a **cycle**.

A dependency graph has to have **no cycles at all** — mathematicians call that a *directed acyclic
graph*, or **DAG**. The reason is not aesthetic. Only an acyclic graph can be put in an order where
everything comes after the things it needs, and that ordering is called a **topological order**. It
is exactly the order your `<script>` tags have to be in.

So "which order do my script tags go in?" and "is my design sound?" turn out to be the same
question. If no order exists, there is a cycle, and the cycle is a design mistake rather than a
typing mistake. Your browser solves this for you with `import`; it cannot invent an order that does
not exist.

---

## Break it on purpose

Use `code/02-script-tags/` and `code/03-modules/`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| In Option A, move `<script src="main.js">` to the top | | |
| In Option A, declare `const Config = {}` in two files | | |
| Open the Option B folder by double-clicking `index.html` | | |
| In Option B, delete `type="module"` from the script tag | | |
| In Option B, import `BALL_SPEED` without exporting it | | |
| In Option B, add `import { startGame } from "./game.js"` to `input.js` | | |
| In a module, assign to a variable you never declared: `scor = 5` | | |
| In `04-the-cycle`, move `const startingScore = …` inside `drawHud()` | | |

The last one is the quiet hero of this lesson. In a plain script that line silently makes a new
global and your typo runs for weeks. In a module it stops the program on the spot.

---

## Think like an engineer

Splitting a file has no single correct answer, which is why it is a design skill rather than a rule.

1. Should `entities.js` know how to **draw** a ball, or should `render.js` know how to draw a ball?
   Argue both. (Hint: ask what you would have to change to add a second way of drawing — a
   scoreboard-only view, say, or a minimap.)
2. `config.js` currently holds `BALL_SPEED` and the level layout. Those are both "numbers you might
   tune", so one file looks reasonable. Using the change-together test, is that right? What happens
   when you have twelve levels?
3. **Design something.** You want to add a second game mode — the same Breakout, but the paddle is at
   the top and gravity pulls the ball upwards. Which of your six files would you touch? If the answer
   is "five of them", your lines are in the wrong places. Propose better ones.
4. **The hard one.** You want to write an automatic test that plays 10,000 frames of Breakout with no
   browser window at all, to check the ball can never escape the walls. Which files can run without a
   canvas, and which cannot? What would you have to move to make that possible? (This question is the
   reason professionals separate game *logic* from *rendering*, and you are about to discover the
   rule for yourself.)

Question 4 has a name you will meet in the advanced level. Try to state the rule in your own words
before you look for it.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Module** | A file with private names, which shares only what it `export`s. |
| **`export`** | Marks a name as usable by other files. |
| **`import`** | Names what this file needs, and from where. |
| **Entry point** | The one file the page loads; everything else arrives through imports. |
| **Dependency** | "A needs B." Drawn as an arrow from A to B. |
| **Coupling** | How much one file relies on another's insides. Keep it low. |
| **Cohesion** | How much the contents of one file belong together. Keep it high. |
| **Circular dependency** | A loop of arrows. Produces `undefined`, not a clear error. |
| **Origin** | Protocol + host + port. The browser's unit of "same website". |
| **CORS** | The rule that blocks one origin from loading another's code without permission. |
| **Singleton** | One shared instance, however many files ask for it. Modules are singletons. |
| **Strict mode** | Stricter JavaScript rules. Always on inside a module. |
| **Directed graph** | Nodes joined by arrows that have a direction. |
| **Topological order** | An order where everything comes after what it depends on. |

---

## Recap

- Splitting a file is not about tidiness. It is about **who may know about whom**.
- Draw the arrows. If they ever form a loop, that is a design error, not a syntax error.
- Two tools for the same job: **`<script>` tags plus one object per file** (works by double-clicking),
  or **`type="module"`** (private names, automatic order, needs a local server).
- Things that **change together** belong together. That beats "one file per noun" every time.
- A file that knows nothing about your game — like `input.js` — is a file you can reuse forever.

---

## Stretch goals

1. **Put `main.js` on a diet.** Get the entry point down to under ten lines. Everything it still does
   is something it should probably be handing to somebody else.
2. **Draw your own graph.** Sketch the arrows for your split Breakout, then check it against the real
   `import` lines. Most people's drawing and code disagree, which is itself worth knowing.
3. **Swap an implementation.** Write a second `render.js` that draws everything as text characters
   instead of rectangles, and switch between them by changing one line in `index.html`. If that is
   hard, `game.js` knows too much about drawing.
4. **Make the input file earn its keep.** Add mouse and touch support to `input.js` without `game.js`
   changing at all. If you have to edit `game.js`, the boundary is in the wrong place.
5. **The honest test.** Attempt question 4 from *Think like an engineer*: move enough logic out of
   `render.js`'s way that you can run your ball-and-wall rules in Node with no browser involved.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Project the beginner Breakout source and scroll it slowly, in silence, looking for `updateBall`. Let that take 20 uncomfortable seconds. Then ask what they would change to move the paddle to the top. |
| 10–25 | **Concept.** The dependency visualizer. Build the arrow diagram on the board *with the class*, then create the cycle and let them discover that no load order exists. |
| 25–40 | **Live-code** the Option A split. Do `config.js` and `input.js` together and stop; they do the rest in section D. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D: split their own Breakout. Circulate — this is where boundary arguments happen, and those arguments are the lesson. |
| 120–140 | Break-it-on-purpose. Do the `file://` CORS one as a whole class; it is the one that will otherwise eat somebody's evening. |
| 140–150 | Recap. Set up lesson 2: vectors are about to become a file. |

**Before the lesson: decide which option your room uses.** Try `python3 -m http.server 8000` on one
of the actual classroom machines the day before. If it works, teach Option B and mention Option A. If
it does not, teach Option A and show Option B on your own laptop. Do not discover this live.

**What usually goes wrong**

1. **Modules opened from `file://`.** Universal, and the error message mentions CORS rather than
   anything a student has heard of. Expect it; have the server command on the board already.
2. **A missing `./` in an import.** `import { x } from "config.js"` fails — bare names are reserved
   for package managers, which this course does not use. It must be `"./config.js"`.
3. **A forgotten `.js`.** Node lets you drop the extension; browsers do not.
4. **Script tags in the wrong order** in Option A, giving `Config is not defined`. This is a good
   failure: it is the topological order lesson arriving by itself.
5. **The refactor also "improves" something.** Half the class will rename variables while they move
   them, and then the game is broken and nobody knows which change did it. Say in advance:
   *move code today, change code tomorrow.* Then make them `git diff` or compare side by side.
6. **Everything ends up in `game.js`.** It becomes the old big file with five small friends. Ask:
   "what in here mentions the canvas? what in here mentions a key?" Those are the seams.

**If you are running short on time** — cut Option B entirely and teach only the script-tag split. The
dependency-direction idea, which is the real content, is identical in both. The cycle demo can also go;
keep the visualizer instead, which makes the same point faster.

**For the student who finishes at minute 90** — stretch goal 3 (a second `render.js`) is the one that
teaches the most, because it fails loudly and immediately if their boundary was wrong. Stretch goal 5
is for anyone who has met Node before.

**The point to land at the end:** they rewrote the structure of a 300-line program and the game is
byte-for-byte identical to play. That is what a refactor is, and being able to do one without fear is
most of what separates someone who can maintain a large program from someone who can only write a
small one.
