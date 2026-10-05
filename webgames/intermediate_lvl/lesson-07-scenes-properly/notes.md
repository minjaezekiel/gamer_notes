# Lesson 7 — Scenes, Properly

> **Web Games · Intermediate level · Lesson 7 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

The part of a game that is not the game: a **title screen**, a **pause overlay** that shows the frozen
game behind it, a **game over screen**, and smooth **fades** between all of them.

```
   TITLE ──press space──▶ PLAYING ──press P──▶ PAUSED
     ▲                      │  ▲                  │
     │                      │  └──────press P─────┘
     └──press space──── GAME OVER ◀── you died
```

This is the least glamorous lesson in the level and the one that most often decides whether a student's
game is finishable. A game with no title screen and no pause is a demo; the same game with them is a
*game*.

## Where this fits

- **Back:** beginner [lesson 5](../../beginner_lvl/lesson-05-rules-score-and-feel/notes.md) introduced a
  state machine with a `mode` variable. That was the right first answer. Today it grows up.
- **Forward:** [lesson 11](../lesson-11-saving-and-loading/notes.md) adds a settings screen to this
  structure, and the [capstone](../lesson-12-capstone-a-platformer/notes.md) needs every bit of it.
- **Other tracks:** Python's intermediate lesson 11 builds the same manager; C++'s intermediate lesson 11
  does it with an `enum class`, where the compiler can check you have handled every case.

---

## The idea, in plain words

### Why booleans stop working

Here is how it always starts, and it is not unreasonable:

```js
let isPlaying = true;
let isPaused = false;
let isGameOver = false;
let inMenu = false;
```

Four booleans. Count the combinations: **16**. How many of them make sense? About four. The other twelve
are states your program can get into and that nobody has ever thought about:

- `isPaused` and `isGameOver` both true — paused on the game over screen?
- `inMenu` and `isPlaying` both true — which one draws?
- all four false — the game draws nothing and responds to nothing, for ever.

The last one is the real killer, because it is what you get when somebody forgets *one* line in *one*
branch. There is no error. The game simply stops, and the console is clean.

> **The principle, and it is worth more than this lesson:** make illegal states impossible to
> represent. Not "check for them" — impossible. If there is one variable that holds one of four values,
> the other twelve states cannot happen, because there is nowhere to put them.

```js
let scene = "title";      // "title" | "playing" | "paused" | "gameover"
```

Four states. Not sixteen. Every line that reads `scene` knows exactly where it stands.

### From one variable to real scenes

A string works until each state needs its own *data*. The title screen wants a blinking cursor; the
game wants a player and a level; the game over screen wants the final score and a timer before it
accepts input. Hanging all of that off one set of global variables brings back the mess by a different
route.

So make each scene an object that owns its own data and its own three jobs:

```js
const titleScene = {
  name: "title",

  /* called ONCE, when this scene becomes the current one. Set up here, not at
     the top of the file, so that coming back to a scene starts it afresh. */
  enter: function () {
    this.blink = 0;
  },

  update: function (dt) {
    this.blink += dt;
    if (Input.wasPressed(" ")) { Scenes.go(playScene); }
  },

  draw: function (ctx) {
    ctx.fillText("MY GAME", 200, 150);
    if (this.blink % 1 < 0.6) { ctx.fillText("press SPACE", 210, 200); }
  },

  /* called once as we leave. Stop sounds, clear timers, tidy up. */
  exit: function () {}
};
```

Then the loop stops knowing anything about your game at all:

```js
function frame(now) {
  const dt = Math.min(0.05, (now - lastTime) / 1000);
  lastTime = now;

  Scenes.current.update(dt);
  Scenes.current.draw(ctx);

  requestAnimationFrame(frame);
}
```

Two lines. Whatever the game is doing, those two lines do not change — and adding a scene does not touch
them.

### `enter` is the part people leave out

Without `enter`, playing a second time starts you where the last game ended: the score is still 400, the
enemies are where you left them, and you are already dead. Students then add "reset" code in whichever
place they happen to notice the problem, usually three places.

`enter` is the one place. **Every scene sets up all of its own state in `enter`,** and then restarting
is `Scenes.go(playScene)` with no further thought.

### Pause needs a *stack*, not a switch

Switching to a "paused" scene loses the game. The screen goes blank, because the play scene is no longer
the current one and nothing is drawing it. Students then make the pause scene redraw the game itself,
which means the pause scene now needs access to everything.

The real answer is that pausing does not *replace* the current scene. It sits **on top** of it:

```js
const Scenes = {
  stack: [],

  get current() { return this.stack[this.stack.length - 1]; },

  go: function (scene) {              // replace everything
    while (this.stack.length) { this.stack.pop().exit(); }
    this.push(scene);
  },

  push: function (scene) {            // put a scene ON TOP, keeping what is below
    this.stack.push(scene);
    scene.enter();
  },

  pop: function () {                  // remove the top one, revealing what was under
    this.stack.pop().exit();
  },

  update: function (dt) {
    /* ONLY THE TOP SCENE UPDATES. That is what "paused" means: the game is still
       there, it is simply not being asked to move. */
    this.current.update(dt);
  },

  draw: function (ctx) {
    /* EVERY scene draws, bottom to top. So the game is still visible behind the
       pause menu, and you did not write a line of code to make that happen. */
    for (let i = 0; i < this.stack.length; i++) {
      this.stack[i].draw(ctx);
    }
  }
};
```

Read those two loops again, because together they *are* pausing: **update the top, draw them all.**
Nothing freezes anything; the frozen game is simply a game that is not being updated. The pause scene is
then about six lines — a translucent rectangle and the word PAUSED.

A stack also gives you, for free: a settings screen over the pause menu over the game; a dialogue box
over the world; a "are you sure?" over a menu. All of them are `push` and `pop`.

### Input belongs to the top scene

With two scenes on the stack, both would see the `P` key. The pause menu unpauses, the game pauses
again, and it flickers once a frame.

The fix is the rule: **only the current scene reads input.** Since only the top scene updates, and input
is read in `update`, this happens by itself — which is a sign the design is right. If you find yourself
reading the keyboard in `draw`, something has gone wrong.

One related thing you need, and it is the stretch goal from beginner lesson 3: a **just-pressed** test.
`keys["p"]` is true for every frame the key is held, so pausing with a held key pauses and unpauses
thirty times.

```js
/* Compare this frame's keys against last frame's. The copy at the end of the
   frame is the whole trick. */
const Input = {
  keys: {}, previous: {},
  wasPressed: function (k) { return this.keys[k] && !this.previous[k]; },
  endFrame: function () { this.previous = Object.assign({}, this.keys); }
};
```

### Switching scenes in the middle of a frame

This one bites once and is memorable. Inside `playScene.update` you notice the player has died and call
`Scenes.go(gameOverScene)`. Then the rest of `playScene.update` carries on running — moving a player who
is now in a scene that no longer exists, possibly reading things `exit` has already cleared.

Two ways to deal with it:

```js
// 1. Return immediately. Simple, and you must remember it every time.
if (player.dead) { Scenes.go(gameOverScene); return; }

// 2. Defer the change to the end of the frame. Remembering is not required.
Scenes.requestGo(gameOverScene);     // just records it
// ... after update and draw have both finished:
Scenes.applyPendingChange();
```

Option 2 is what engines do, for the same reason you remove items from a list backwards: **changing a
collection while you are walking through it is a reliable source of strange bugs.**

### Transitions: a timer, a scene, and a rectangle

A hard cut between scenes feels cheap, and a fade is a timer:

```js
const fadeScene = {
  enter: function () { this.t = 0; },

  update: function (dt) {
    this.t += dt;
    if (this.t >= FADE_TIME) { Scenes.go(this.nextScene); }
  },

  draw: function (ctx) {
    const alpha = Math.min(1, this.t / FADE_TIME);
    ctx.fillStyle = "rgba(0, 0, 0, " + alpha + ")";
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  }
};
```

Push that on top and the scene below keeps drawing while the black rectangle grows over it. The whole
transition system is one scene with a timer, which is a good sign that the stack was the right shape.

And use an easing curve from [the easing explainer](../../../shared/visualizers/easing.html) rather than
a straight line: `easeOutQuad` on a fade is noticeably better than linear, for no extra work.

---

## The idea, in pictures

Open [the game states explainer](../../../shared/visualizers/state-machine.html).

**What to look for:** click the buttons and watch which presses get **ignored**. Pressing "pause" on the
game over screen does nothing — and that is correct, not a missing feature. A state machine is as much
about what *cannot* happen as about what can. Count the arrows: there are far fewer than every state
joined to every other, and each missing arrow is a bug you can no longer write.

Then open [easing](../../../shared/visualizers/easing.html) and look at `easeOutQuad` — that is the
curve to put on your fades.

---

## The idea, in code

1. `code/01-flags-get-messy.html` — four booleans, with a live count of how many of the sixteen
   combinations are legal. Buttons let you create the illegal ones on purpose.
2. `code/02-one-scene-at-a-time.html` — scene objects with `enter`/`update`/`draw`/`exit`, and a loop
   that is two lines long.
3. `code/03-a-scene-stack.html` — pause as an overlay, settings over pause, with the stack drawn on
   screen as you push and pop.
4. `code/04-transitions.html` — fades, easing curves, and a switch for the "changed scene mid-update"
   bug.

---

## The maths you just used

**1. Counting states.** `n` booleans give `2ⁿ` combinations: 4 booleans is 16, 10 booleans is 1024. One
variable holding one of `n` values gives exactly `n`. That growth is the whole argument, and it is worth
doing on the board — most students have never counted the states their own code can be in.

**2. A state machine as a graph.** States are nodes, transitions are edges. You met directed graphs in
lesson 1 for dependencies; this is the same idea doing a different job. Here the useful question is not
"are there cycles?" — you *want* cycles — but **"can you reach every state, and can you get back?"** A
state you can enter and never leave is a bug (a pause with no unpause); a state you can never enter is
dead code.

**3. Interpolation again.** A fade is `alpha = t / duration`, clamped to 1 — the `lerp` from lesson 6,
applied to transparency instead of position. With an easing curve on top it is
`alpha = ease(t / duration)`.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| In `02`, delete `enter()` from the play scene and play twice | | |
| In `03`, make `update` run every scene in the stack instead of the top one | | |
| In `03`, make `draw` run only the top scene | | |
| Use `keys["p"]` instead of `wasPressed("p")` to pause | | |
| In `04`, switch scenes mid-update without returning | | |
| Push the same scene object onto the stack twice | | |
| Call `exit()` before `enter()` of the next scene — then the other way round | | |
| Remove `Input.endFrame()` | | |

The second and third are the pair that matter: one of them freezes nothing, the other makes pause draw
nothing. Doing both wrong is how most people's first pause screen behaves.

---

## Think like an engineer

1. Our scenes share a canvas and an `Input`. They do not share a score. Where should the score live —
   in the play scene, in a global, or passed from scene to scene? What does each choice cost when the
   game over screen needs to display it?
2. The game over scene ignores input for half a second after it appears. Why would anybody do that on
   purpose? (Think about *how* the player got there.)
3. **Design something.** A settings screen reachable from both the title screen and the pause menu, which
   returns to whichever one it came from. You have a stack. Does that solve it entirely, or is there
   something left to decide?
4. **The hard one.** Your game needs a level transition: the player touches a door, the screen fades out,
   the next level loads, the screen fades in, and the player keeps the score and the health they had.
   Which parts of this are scenes, which are data, and *where does the data live* while no scene owns it?
   Draw it before you write it.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Scene** | One screen or mode of the game, owning its own data and its own update/draw. |
| **Scene manager** | The thing that knows which scene is current. |
| **Scene stack** | Scenes on top of each other. Update the top, draw them all. |
| **`enter` / `exit`** | Called once on arrival and once on departure. Where setup and teardown belong. |
| **`go` / `push` / `pop`** | Replace everything · add on top · remove the top. |
| **Illegal state** | A combination your variables allow and your game does not mean. |
| **Just-pressed** | True only on the first frame a key is held. Needs last frame's keys. |
| **Deferred change** | Recording a scene change and applying it after the frame. |
| **Transition** | A scene whose only job is a timer and a rectangle. |

---

## Recap

- Booleans multiply: `n` of them is `2ⁿ` states, most of which you never meant. **One variable, one
  value.**
- A scene owns **its own data** and has `enter`, `update`, `draw`, `exit`. Setup belongs in `enter`, or
  playing twice goes wrong.
- The loop becomes **two lines** and never changes again.
- Pause is a **stack**: update the top, draw them all. Nothing freezes anything.
- Only the top scene reads input — which happens automatically, because only the top scene updates.
- Pausing needs **just-pressed**, not "is held".
- Changing scene in the middle of `update` is the same hazard as editing a list while looping over it.
  Return immediately, or defer.

---

## Stretch goals

1. **A real transition manager.** `Scenes.fadeTo(nextScene, 0.4)`, with the easing curve of your choice.
2. **A loading scene.** Push a scene that waits for something slow — pretend with a two-second timer —
   and then replaces itself. Where does the thing it loaded go?
3. **A dialogue box** over the world: the game pauses, text appears a character at a time, space advances
   it, and the world is still visible. All of that is one `push`.
4. **Make the manager debuggable.** Draw the stack on screen, bottom to top, with each scene's name. Then
   try to get it into a state you did not intend, and see whether you can.
5. **The level transition** (question 4), for real. The hardest thing in this lesson, and the thing the
   capstone will need.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Open `01-flags-get-messy.html` and press the buttons until the game is in an impossible state — all four booleans false, drawing nothing, responding to nothing. Ask what is broken. Nothing is broken; every line is doing what it says. |
| 10–25 | **Concept.** Count `2ⁿ` on the board. Then the state-machine visualizer, concentrating on the presses that are *ignored*. |
| 25–40 | **Live-code** the scene object and the two-line loop. The moment the loop stops mentioning the game is worth pausing on. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Checkpoints 1–5 are the core; the stack is checkpoint 4 and is the part most worth their time. |
| 120–140 | Break-it-on-purpose. Do the update-all / draw-top pair as a class. |
| 140–150 | Recap. Lesson 8 is sound, which needs this structure to know when to start the music. |

**What usually goes wrong**

1. **Pausing flickers.** `keys["p"]` instead of just-pressed. Universal. It is also the beginner-level
   stretch goal finally becoming necessary, which is a nice moment to point out.
2. **Pause draws nothing.** They drew only the top scene. Fix one loop.
3. **Pause does not pause.** They updated the whole stack.
4. **The second game starts broken.** No `enter`, or setup done at the top of the file where it runs once.
5. **`this` is undefined inside a scene method.** They extracted the function (`const u = scene.update`)
   or used an arrow function in a way that lost the binding. Worth ten minutes on `this` if your class has
   not met it, and worth considering closures instead — see the solutions for a version that avoids `this`
   entirely.
6. **Everything is a global again.** The scenes exist, and all the data is still in globals outside them.
   Ask them what `playScene.enter` would have to do if the scene owned its own data. That question usually
   does it.
7. **Scene changed mid-update, then the rest of update ran.** The symptom is strange rather than fatal —
   a frame of the old scene leaking through, or a `null` where the player used to be.

**If you are running short on time** — cut transitions and `code/04` entirely. A hard cut between scenes
is fine. Do **not** cut the stack: pause is what students most want and least often manage.

**For the student who finishes at minute 90** — stretch goal 3 (a dialogue box) is the one that shows off
what the stack bought them, and takes about fifteen minutes once the stack works.

**The point to land at the end:** two loops — update the top, draw them all — are the entire pause
feature. That is what a good structure buys: not less code, but features that arrive for free because the
shape was right.
