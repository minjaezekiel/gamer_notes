# Lesson 5 — Rules, Score And Feel

> **Web Games · Beginner level · Lesson 5 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

**Finished Pong.** A title screen, a score, a winner, a game-over screen, and a restart — plus
sound, screen shake and particles that make hitting the ball genuinely satisfying.

```
╔══════════════════════════════════════╗
║   3                              1   ║
║ ▮                                    ║
║ ▮            ● ✦ ✦                 ▮ ║
║                                    ▮ ║
╚══════════════════════════════════════╝
      first to 5 wins
```

## Where this fits

- **Back:** [lesson 4](../lesson-04-when-things-touch/notes.md) made the ball bounce off paddles.
  You have a toy.
- **Forward:** [lesson 6](../lesson-06-capstone-breakout/notes.md) is the capstone — Breakout, built
  by you.
- **Today turns a toy into a game.** Two separate ideas: **rules** (what counts as winning) and
  **feel** (why hitting things is fun). Both matter, and most people only think about the first.

---

## The idea, in plain words

### Part 1: a game is never doing just one thing

Right now your Pong starts instantly and never ends. Real games have **modes**: a title screen,
playing, paused, game over.

The obvious approach is a flag for each one, and it goes wrong fast:

```js
// DO NOT DO THIS
let started = false;
let paused = false;
let dead = false;
let inMenu = true;

if (started && !paused && !dead) { updatePlayer(); }
if (!started && inMenu && !dead) { drawMenu(); }
// ...and what does it mean if started AND inMenu are both true? Nobody knows.
```

With four true/false flags there are 2×2×2×2 = **16** combinations, and only four of them make
sense. The other twelve are bugs waiting to happen.

The fix is one variable:

```js
let state = "MENU";      // one of: MENU, PLAYING, GAME_OVER
```

Now there are exactly **four** possibilities and all four are valid. You did not fix those twelve
bugs — you made them **impossible to write**.

> That is a much stronger kind of fix than catching a bug, and looking for chances to do it is one of
> the most valuable habits in programming. Make the wrong thing *unrepresentable* rather than merely
> unlikely.

This design is called a **state machine**: the game is in exactly one named state at a time, and only
certain moves between states are allowed.

### Using it

The state decides what runs:

```js
function update(dt) {
  if (state === "PLAYING") {
    updatePaddles(dt);
    updateBall(dt);
  }
  // In MENU and GAME_OVER nothing moves. Not because we remembered to stop
  // each thing, but because we never called them.
}

function render() {
  if (state === "MENU")      { drawTitleScreen(); }
  if (state === "PLAYING")   { drawGame(); }
  if (state === "GAME_OVER") { drawGame(); drawWinnerOverlay(); }
}
```

Notice `GAME_OVER` draws the game *and* an overlay. States do not have to be completely different
screens.

> **A mistake almost everyone makes.** Students often put the check inside every object instead:
> `if (!paused) { this.x += this.vx * dt; }` in the ball, and the paddle, and the particles. Now
> pausing depends on remembering that line in twenty places, and you will forget one — so one enemy
> keeps walking while the game is paused. **Check the state once, in the loop, and simply do not
> call update at all.**

### Part 2: feel

Here is something that will sound wrong: **the rules of Pong are not what makes Pong fun.**

Watch somebody play a version with no sound, no screen shake and no particles, and then the same game
with them. The code that decides who wins is identical. One feels dead and one feels great.

The industry word for this is **juice** — the feedback a game gives you for your actions. A game with
good juice tells you, instantly and in several ways at once, that something happened.

| Technique | What it does | Cost |
|---|---|---|
| **Sound** | The single biggest improvement available. A 10 ms click on every hit. | ~15 lines |
| **Screen shake** | Shift everything a few pixels for ~0.1 s. Makes impacts feel heavy. | ~8 lines |
| **Particles** | A spray of small dots that fade out. Says "something happened *here*". | ~25 lines |
| **Flash / squash** | Briefly change a colour or stretch a shape. | ~5 lines |
| **Speed-up** | Ball gets slightly faster each hit, so rallies build tension. | 1 line |

Every one of those is cheap. Together they are most of the difference between a school project and
something people want to play.

> **The rule of thumb that matters:** juice should last **about 100 milliseconds**. Long enough to
> notice, short enough that it never gets in the way. A screen shake of half a second is nauseating.
> One of a tenth of a second is invisible as an effect and felt as an impact.

---

## The idea, in pictures

Open [the state machine explainer](../../../shared/visualizers/state-machine.html).

**What to look for:**

1. Press the buttons in any order. Watch which box glows.
2. The **same button does different things** depending on the current state. "Press P" pauses while
   playing and resumes while paused.
3. Most importantly: try pressing **"Press P" while on the menu**. *Nothing happens.* There is no
   rule for that, so it is ignored.

That last point is the whole lesson. A state machine is mostly about what you are **not** allowed to
do, and "nothing happened" is correct behaviour, not a missing feature.

---

## The idea, in code

### Step 1: the state variable and the transitions

```js
let state = "MENU";
let playerScore = 0;
let opponentScore = 0;
const WINNING_SCORE = 5;

document.addEventListener("keydown", function (e) {
  if (e.key === " ") {
    // The SAME key does different things depending on the state.
    if (state === "MENU") {
      startGame();
    } else if (state === "GAME_OVER") {
      startGame();
    }
    // While PLAYING, space does nothing. That is deliberate.
  }
});

function startGame() {
  playerScore = 0;
  opponentScore = 0;
  resetBall();
  state = "PLAYING";      // the transition. One assignment.
}
```

### Step 2: scoring

```js
function updateBall(dt) {
  // ... movement and collisions ...

  if (ball.x < -30) {
    opponentScore = opponentScore + 1;
    checkForWinner();
  }
  if (ball.x > canvas.width + 30) {
    playerScore = playerScore + 1;
    checkForWinner();
  }
}

function checkForWinner() {
  if (playerScore >= WINNING_SCORE || opponentScore >= WINNING_SCORE) {
    state = "GAME_OVER";
  } else {
    resetBall();
  }
}
```

### Step 3: sound, without any files

You do not need an audio file. The browser can generate tones directly, which means your game stays
a single file with nothing to download.

```js
// One AudioContext for the whole game. Making a new one per sound leaks memory.
let audio = null;

function beep(frequency, duration) {
  // Browsers refuse to play sound until the user has interacted with the page.
  // So we create the AudioContext on the first sound, which always happens
  // after a key press. This is a real rule, not a quirk of our code.
  if (!audio) { audio = new AudioContext(); }

  const oscillator = audio.createOscillator();  // makes a tone
  const volume = audio.createGain();            // controls loudness

  oscillator.frequency.value = frequency;       // pitch, in hertz
  oscillator.type = "square";                   // square = retro bleep

  // Fade the volume down to nothing over the duration. Without this fade you
  // get an audible CLICK at the end, because the sound wave stops mid-cycle.
  volume.gain.setValueAtTime(0.08, audio.currentTime);
  volume.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + duration);

  oscillator.connect(volume);
  volume.connect(audio.destination);
  oscillator.start();
  oscillator.stop(audio.currentTime + duration);
}

// Use different pitches for different events, so the player can tell them apart
// without looking.
function soundPaddleHit() { beep(440, 0.06); }
function soundWallHit()   { beep(260, 0.04); }
function soundScore()     { beep(150, 0.25); }
```

### Step 4: screen shake

```js
let shakeTime = 0;           // seconds of shaking left
let shakeStrength = 0;

function addShake(strength, duration) {
  // Take the BIGGER of the two, so a small shake never cancels a big one.
  shakeStrength = Math.max(shakeStrength, strength);
  shakeTime = Math.max(shakeTime, duration);
}

function render() {
  ctx.save();                // remember where the canvas "origin" is

  if (shakeTime > 0) {
    // Random offset, shrinking as the shake runs out.
    const fade = shakeTime / 0.12;
    const offsetX = (Math.random() - 0.5) * 2 * shakeStrength * fade;
    const offsetY = (Math.random() - 0.5) * 2 * shakeStrength * fade;
    ctx.translate(offsetX, offsetY);   // move EVERYTHING drawn from here on
  }

  drawEverything();

  ctx.restore();             // put the origin back, or the shake accumulates
}
```

`ctx.save()` and `ctx.restore()` are a matched pair. Forget the `restore` and every frame's offset
adds to the last one, and your game slides off the screen within a second.

### Step 5: particles

```js
const particles = [];       // an ARRAY, because there are many of them

function spawnParticles(x, y, count) {
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;   // a random direction
    const speed = 60 + Math.random() * 180;
    particles.push({
      x: x,
      y: y,
      speedX: Math.cos(angle) * speed,
      speedY: Math.sin(angle) * speed,
      life: 0.4                                  // seconds remaining
    });
  }
}

function updateParticles(dt) {
  // Loop BACKWARDS. If you loop forwards and remove an item, everything after
  // it shuffles down by one and you skip the next particle. Going backwards
  // means removals never affect the indexes you have not reached yet.
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.speedX * dt;
    p.y += p.speedY * dt;
    p.life -= dt;
    if (p.life <= 0) {
      particles.splice(i, 1);     // remove this one
    }
  }
}
```

That backwards loop is a real and important idiom. You will meet it again in lesson 6 with bricks,
and in every language in this course.

---

## The maths you just used

### Random directions, using a circle

```js
const angle = Math.random() * Math.PI * 2;
const speedX = Math.cos(angle) * speed;
const speedY = Math.sin(angle) * speed;
```

`Math.PI * 2` is a full turn, measured in **radians** instead of degrees. Radians are just another
unit for angles, the way centimetres and inches are both lengths: a full turn is 360 degrees or
2π ≈ 6.28 radians.

`Math.cos` and `Math.sin` convert an angle into an x and y direction. You do not need to understand
why yet — you meet them properly in the intermediate level. For now: **cos gives you across, sin
gives you down, and together they point at an angle.**

Try the obvious wrong version to see why this matters:

```js
// WRONG: random x and random y separately
const speedX = (Math.random() - 0.5) * 300;
const speedY = (Math.random() - 0.5) * 300;
```

That scatters particles into a *square*, with more of them heading diagonally than straight. The
cos/sin version gives an even circle. The difference is visible once you know to look.

### Fading out

```js
ctx.globalAlpha = p.life / 0.4;      // 1 when new, 0 when dead
```

Dividing the time remaining by the total lifetime gives a number that slides from 1 to 0. That
pattern — *remaining ÷ total* — is behind every fade, health bar and loading bar you have ever seen.

---

## Break it on purpose

Use `code/04-pong-complete.html`.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove `ctx.restore()` from `render` | | |
| Change shake duration from `0.12` to `1.5` | | |
| Change particle count from `12` to `400` | | |
| Delete `if (state === "PLAYING")` so update always runs | | |
| Remove the volume fade from `beep` | | |
| Loop *forwards* through `particles` while splicing | | |

The first one is spectacular. The last one is subtle and is the single most common array bug there
is — look very closely at how many particles survive.

---

## Think like an engineer

### On states

1. Draw the state diagram for a game you actually play. Include the states people forget: loading,
   settings, the cutscene, the "are you sure you want to quit?" box, level-complete.
2. Find a transition that should **not** be allowed, and say what would go wrong if it were. For
   example: what breaks if you could go from PAUSED straight to GAME_OVER?
3. Where should the music change — is music part of the state, or a reaction to entering one?

### On feel

4. Play your finished Pong with the sound off. Then with sound. Which change made the biggest
   difference per line of code you wrote?
5. **The uncomfortable question.** Juice makes a game feel better without making it fairer, deeper or
   more skilful. A slot machine is almost entirely juice. Where is the line between *good feedback*
   and *manipulation*? Does it matter whether the player can tell?
6. Pick one thing in your game that currently gives no feedback at all. Design feedback for it in
   three different senses — something seen, something heard, something *felt* through the controls.

Question 5 has no answer and is worth arguing about. People design games professionally for years
without resolving it.

---

## Vocabulary

| Word | What it means |
|---|---|
| **State machine** | A design where something is in exactly one named state at a time. |
| **Transition** | A permitted move from one state to another. |
| **Juice** | Feedback that makes actions feel satisfying. |
| **Screen shake** | Briefly offsetting everything drawn, to suggest impact. |
| **Particle** | A small short-lived object spawned for visual effect. |
| **Oscillator** | The thing that generates a tone in the Web Audio API. |
| **Radians** | A unit for angles. A full turn is 2π ≈ 6.28. |

---

## Recap

- One `state` variable beats four flags, because it makes nonsense states **impossible to write**.
- Check the state **once**, in the loop. Do not scatter `if (!paused)` through every object.
- **Juice is cheap and transformative.** Sound first, then shake, then particles.
- Effects should last about **100 ms**. Longer is annoying.
- Loop **backwards** when removing items from an array.
- `ctx.save()` and `ctx.restore()` are a pair. Always.

---

## Stretch goals

1. **Pause.** Add a PAUSED state on the P key. Check that nothing moves — including particles.
2. **Hitstop.** On a paddle hit, freeze the whole game for 40 milliseconds. This is used in almost
   every fighting and action game and is astonishingly effective. Try 20 ms, 40 ms, 150 ms.
3. **Trail.** Give the ball a fading trail from its last 10 positions.
4. **Better sound.** Make the paddle-hit pitch depend on where the ball struck. Now the sound tells
   you something about the game rather than just marking an event.
5. **Best of five.** Add a match system: rounds, a running tally, and a different message for winning
   the match versus a round.
6. **Shake responsibly.** Add an option to turn screen shake off. Many real players need this —
   motion effects cause genuine nausea for some people. Then think about what else in your game
   should be optional.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Play the finished Pong with all the juice **switched off**, then with it on. Do not explain between the two. The reaction does the teaching. |
| 10–25 | **Concept.** State machine visualizer. Spend time on the *ignored* button press. |
| 25–40 | **Live-code** the state variable and the score. Leave juice for the build. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Most students will spend most of this on juice and enjoy it enormously. |
| 120–140 | **Show-and-tell.** Everyone demos their juice for 30 seconds. This is the best part of the lesson — protect the time for it. |
| 140–150 | Recap. Next week is the capstone: they build Breakout themselves. |

**What usually goes wrong**

1. **The screen slides away and never comes back.** Missing `ctx.restore()`. Dramatic and memorable;
   let it happen.
2. **No sound at all, and no error.** Browsers block audio until the user has interacted with the
   page. Creating the `AudioContext` lazily, inside the first sound, fixes it. Worth explaining as a
   deliberate browser policy rather than a bug — it exists because of autoplaying advertisements.
3. **Half the particles never disappear.** They looped forwards while splicing. Draw the array on the
   board and walk through the indexes by hand; it is much clearer than describing it.
4. **Everything still moves on the game-over screen.** They added the state but kept calling the
   update functions unconditionally.
5. **The game is unplayable because of the shake.** They used a strength of 30 and a duration of one
   second. This is a *good* mistake — it teaches the 100 ms rule far better than being told.
6. Someone will ask why we do not use a `switch`. Fine answer: we could, and `if` is clearer for
   three states. Mention that `enum class` in the C++ track makes the compiler check it for you.

**If you are running short on time** — do states and score only, and give them the juice code as a
file to paste and experiment with. Sound alone, if you must choose one, has by far the best ratio of
effect to effort.

**For the student who finishes at minute 90** — stretch goal 2 (hitstop) is the one. It is four lines
and it is the single most surprising technique in the lesson: freezing the game *briefly* makes it
feel more responsive rather than less, which sounds like nonsense until you try it.

**The thing to land:** the code that decides who wins at Pong is maybe fifteen lines, and it was
finished at the start of the build. Everything else today was about how it *feels*. That ratio —
rules cheap, feel expensive — is roughly what it looks like in professional game development too, and
it surprises people who assume games are mostly about rules.
