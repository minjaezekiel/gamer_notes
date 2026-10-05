# Lesson 7 — Scenes, Properly

## Cheat sheet

### Booleans multiply

4 booleans = **16** states. About 4 are legal.
All four false = a game that draws nothing and responds to nothing, with a clean
console.

```js
let scene = "title";   // one variable, one value
```

**Make illegal states impossible to represent**, not merely checked for.

### A scene

```js
const playScene = {
  name: "play",
  enter() { this.score = 0; /* ALL setup */ },
  update(dt) { /* ... */ },
  draw(ctx) { /* ... */ },
  exit() { /* stop sounds */ }
};
```

Setup goes in `enter`, or playing a second time starts where the first one ended.

### The loop, for ever

```js
Scenes.update(dt);
Scenes.draw(ctx);
```

### The stack IS pause

```js
update(dt) {
  this.current.update(dt);       // TOP ONLY
}
draw(ctx) {
  for (const s of this.stack)
    s.draw(ctx);                 // ALL OF THEM
}
```

- update top only → the game below is frozen
- draw them all → the game below is still visible

```js
go(s)   // replace everything
push(s) // on top, keeping what is below
pop()   // remove the top
```

### Just-pressed

```js
wasPressed(k) {
  return keys[k] && !previous[k];
}
// at the END of every frame:
previous = Object.assign({}, keys);
```

`keys["p"]` pauses and unpauses thirty times a second.

### Do not switch scene mid-update

```js
if (dead) { Scenes.go(over); return; }   // return!
```

or defer the change to the end of the frame.

### A fade is a scene with a timer

```js
draw(ctx) {
  const a = ease(Math.min(1, this.t / TIME));
  ctx.fillStyle = "rgba(0,0,0," + a + ")";
  ctx.fillRect(0, 0, W, H);
}
```

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> Five booleans describe your game's mode. How many combinations are there? Give one illegal combination and say what the player would see.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> State the principle about illegal states in your own words, and say how one variable achieves it.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why does setup belong in <code>enter</code> rather than at the top of the file? What is the symptom if it does not?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Write out the two rules of the scene stack, and say what each one gives you.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why does pausing need <em>just-pressed</em> rather than <em>is held</em>?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why must only the top scene read input, and why does that happen by itself?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> What is the hazard in calling <code>Scenes.go()</code> halfway through <code>update</code>, and what is it the same hazard as?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> The stack is <code>[play, pause]</code>. Which scenes have <code>update</code> called, and which have <code>draw</code> called? What does the player see?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>update</code> is changed to run every scene in the stack. The stack is <code>[play, pause]</code>. Describe exactly what the player now experiences.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> <code>draw</code> is changed to run only the top scene. Stack is <code>[play, pause]</code>, and the pause scene draws a translucent black rectangle and the word PAUSED. What appears?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> The player holds <code>P</code> for one second at 60 fps, using <code>if (keys["p"]) togglePause()</code>. How many times does the state change, and is the game paused at the end? Explain.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> <code>FADE_TIME</code> is 0.5 s. Give the alpha at t = 0, 0.25 and 0.6 for a linear fade. Why is the last one worth clamping?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> Playing a second time, the player starts dead with the previous score still showing.

```js
const playScene = {
  score: 0,
  lives: 3,
  enter: function () {},
  update: function (dt) { /* ... */ }
};
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The pause menu appears, the game behind it is visible, and the game is still running underneath. Name the bug and write the fix.

```js
update: function (dt) {
  for (let i = 0; i < this.stack.length; i++) {
    this.stack[i].update(dt);
  }
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The console says <code>Cannot read properties of undefined (reading 'blink')</code> the moment the title screen appears.

```js
const titleScene = {
  enter: function () { this.blink = 0; },
  update: function (dt) { this.blink += dt; }
};
// in the loop:
const u = Scenes.current.update;
u(dt);
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> On the frame the player dies, the console reports an error about <code>player</code> being <code>null</code>, and one frame of the old scene flashes.

```js
update: function (dt) {
  movePlayer(dt);
  if (player.health <= 0) { Scenes.go(gameOverScene); }
  moveEnemies(dt);
  checkCollisions();
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> <code>wasPressed</code> returns true on every frame the key is held, not just the first.

```js
const Input = {
  keys: {}, previous: {},
  wasPressed: function (k) { return this.keys[k] && !this.previous[k]; }
};
// the loop calls Scenes.update(dt) and Scenes.draw(ctx), and nothing else
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

Use the game you built in lessons 5 and 6.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Add <code>wasPressed</code> to your input code, with the <code>previous</code> copy at the end of every frame. Test it by counting presses on screen &mdash; hold the key and check the number goes up by exactly one.</li>
<li><strong>Checkpoint 2.</strong> Turn your existing game into a <code>playScene</code> object with <code>enter</code>, <code>update</code>, <code>draw</code> and <code>exit</code>. Move <em>all</em> its setup into <code>enter</code>. Your loop should now be two lines.</li>
<li><strong>Checkpoint 3.</strong> Add a title scene and a game over scene. Get the full circle working: title &rarr; play &rarr; game over &rarr; title. Play it twice in a row and check the second game is identical to the first.</li>
<li><strong>Checkpoint 4.</strong> Build the stack: <code>go</code>, <code>push</code>, <code>pop</code>, and the two loops. Add a pause scene that draws a translucent rectangle and the word PAUSED. It should be about six lines and the game should be visible, frozen, behind it.</li>
<li><strong>Checkpoint 5.</strong> Draw the stack on screen as a list of scene names while you play. Keep it &mdash; it is the best debugging aid in this lesson.</li>
<li><strong>Checkpoint 6.</strong> Add a settings scene you can push <em>on top of</em> the pause scene, and pop back from. Three scenes deep, with the game still visible at the bottom.</li>
<li><strong>Checkpoint 7.</strong> Add a fade transition between title and play, using an easing curve rather than a straight line.</li>
<li><strong>Checkpoint 8.</strong> Make a scene change mid-update on purpose, without returning, and write down what happens. Then fix it the way you prefer and say why.</li>
</ul>

<div class="note">
<span class="note-label">If <code>this</code> is undefined</span>
<p>You have pulled a method off its object (<code>const u = scene.update</code>) and lost
the connection. Call it as <code>scene.update(dt)</code>, or use
<code>scene.update.call(scene, dt)</code>. The solutions also show a version built
from closures, with no <code>this</code> anywhere.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** Where should the score live: in the play scene, in a global, or passed from
scene to scene? The game over screen needs to show it. What does each choice cost?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** The game over screen ignores input for half a second after it appears. Why
would anybody do that deliberately? Think about *how* the player arrived there.

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** A settings screen reachable from both the title and the pause menu, which
returns to whichever it came from. Does the stack solve this completely, or is
something left to decide?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** The hard one. A level transition: the player touches a door, the screen
fades out, the next level loads, it fades in, and the score and health carry over.
Which parts are scenes, which are data, and **where does the data live** while no
scene owns it? Draw it before you write it.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. `Scenes.fadeTo(nextScene, 0.4)` as a proper transition manager.
2. A loading scene that waits two seconds and then replaces itself. Where does what
   it loaded go?
3. A dialogue box over the world: text a character at a time, space to advance, the
   world still visible. One `push`.
4. Draw the stack on screen, then try to get it into a state you did not intend.
5. The level transition (E4), for real.
