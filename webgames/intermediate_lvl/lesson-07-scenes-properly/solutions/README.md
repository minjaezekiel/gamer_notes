# Lesson 7 — Solutions and marking notes

---

## Section A

**A1.** [3] `2⁵ = 32` combinations — one mark. Any illegal one with its consequence, two marks. The best
answer is "all five false": nothing draws and nothing responds, so the game appears to have frozen, with
no error anywhere. Accept also `isPaused && isGameOver`, `inMenu && isPlaying`.

**A2.** [2] "If a state cannot be written down, it cannot happen." One mark. One variable holding one of
four values has nowhere to put the other twelve combinations — they are not checked for and rejected,
they simply do not exist — one mark.

**A3.** [3] Because `enter` runs **every** time the scene becomes current, while code at the top of the
file runs once when the page loads — two marks. Symptom: the second game starts where the first one
ended — same score, same dead player, enemies where you left them — one mark.

**A4.** [3] Update the **top** scene only; draw **all** of them, bottom to top. Two marks. Update-top
means the game below is frozen; draw-all means it is still visible — one mark. Full marks require
noticing that those two rules together *are* the pause feature, with no freezing code anywhere.

**A5.** [2] `keys["p"]` is true on every frame the key is held, so at 60 fps a half-second press toggles
the pause about thirty times — one mark — leaving the state effectively random and the screen flickering —
one mark.

**A6.** [2] Otherwise both the pause menu and the game see the same key press and fight over it — one
mark. It happens by itself because input is read in `update`, and only the top scene's `update` is called
— one mark. Credit anyone who adds that this is a sign the design is right: the rule enforces itself.

**A7.** [2] The rest of `update` carries on running against a scene that has already been left, possibly
after `exit` has cleared things it uses — one mark. It is the same hazard as modifying a list while
looping over it, which is why items are removed backwards — one mark.

---

## Section B

**B1.** [3] `update`: **pause only**. `draw`: **play, then pause**. Two marks. The player sees the frozen
game with the pause overlay on top — one mark.

**B2.** [3] The game keeps running behind the pause menu. The player can be killed while paused, and
enemies move. Two marks. One mark for noticing the screen *looks* right, which is why this bug gets
shipped.

**B3.** [3] A black translucent rectangle and the word PAUSED over a **blank canvas** — the game is no
longer drawn at all. Two marks. One mark for noting the game is still *there*, just not drawn: the bug is
in the drawing, not in the game.

**B4.** [4] About 60 toggles, one per frame. Two marks. At the end it is paused only if the number of
frames was odd, which nobody can control — so the result is effectively random, and the screen flickers
between the two states throughout. Two marks.

**B5.** [3] t = 0 → 0. t = 0.25 → 0.5. t = 0.6 → 1.2. Two marks. It needs clamping because an alpha above
1 is not meaningful; browsers clamp it for you, but the number also often gets reused for other things
(a scale, a sound volume) where it will not be — one mark.

---

## Section C

**C1.** [3] `score` and `lives` are set once, in the object literal, when the file loads. `enter` is empty,
so nothing is reset. Two marks. Fix: move the setup into `enter` —
`enter: function () { this.score = 0; this.lives = 3; }` — one mark.

**C2.** [4] Every scene in the stack is being updated, so the play scene keeps running underneath. Two
marks. Fix, two marks:

```js
update: function (dt) { this.current.update(dt); }
```

**C3.** [4] `Scenes.current.update` has been pulled off its object, so when it is called as `u(dt)` there
is no receiver and `this` is `undefined` inside it. Two marks. Fixes, two marks for any one: call it as
`Scenes.current.update(dt)`; use `u.call(Scenes.current, dt)`; or build the scene from closures so that
`this` is never needed:

```js
function makeTitleScene() {
  let blink = 0;                      // a plain variable, captured
  return {
    enter() { blink = 0; },
    update(dt) { blink += dt; },
    draw(ctx) { /* uses blink */ }
  };
}
```

This closure version is worth showing the class: it removes an entire category of bug, and it is how a lot
of professional JavaScript is written.

**C4.** [4] `Scenes.go()` is called in the middle of `update`, and then `moveEnemies` and
`checkCollisions` still run — against a scene that has been exited, after `exit` has cleared `player`.
Two marks. Fix, two marks: `return` immediately after the scene change, or record the change and apply it
after update and draw have finished. Credit the deferred version as the better answer, because it does not
rely on remembering.

**C5.** [3] Nothing ever updates `previous`, so it stays empty and `!this.previous[k]` is always true. Two
marks. Fix: call `Input.endFrame()` — which copies `keys` into `previous` — at the end of every frame, after
update and draw — one mark.

---

## Section D — marking the build

1. **The loop is two lines** (checkpoint 2). If the loop still mentions the player, the refactor is
   incomplete.
2. **All setup is in `enter`** — test by playing twice in a row (checkpoint 3). This is the single most
   common failure.
3. **Pause freezes and still draws** (checkpoint 4). Both halves. Many students get one.
4. **The stack is visible on screen** (checkpoint 5). Insist on it; it makes checkpoint 6 straightforward
   instead of confusing.
5. **Three scenes deep works** (checkpoint 6). If settings-over-pause-over-play draws correctly and only
   settings responds, the design is right.

Checkpoint 2 is the hardest and takes the longest, because it is a refactor of working code — the same
discipline as lesson 1. Remind them: move code, do not improve code.

---

## Section E — marking notes

**E1.** All three are defensible; the costs are the content.

- **In the play scene** — tidy while playing, and the game over screen cannot reach it without a reference
  to a scene it should not know about.
- **A global (`const Game = { score: 0 }`)** — easy, everything can read it, and you are back to the
  problem lesson 1 was about: anything can also *write* it, from anywhere.
- **Passed from scene to scene** (`Scenes.go(gameOverScene, { score: 400 })`) — explicit, each scene
  declares what it needs, and it is more code and slightly awkward when four scenes need the same thing.

The best answers distinguish **run data** (this level's enemies — belongs to the scene) from **session
data** (score, lives, which level — outlives any single scene, so it needs a home of its own). Full credit
for reaching that distinction, in any words; it is exactly what E4 is about.

**E2.** Because the player arrived by **pressing something**. They were probably hammering the jump key as
they died, and that key press would otherwise dismiss the game over screen before they had read it. The
half-second is an input lockout. One mark for "they are still holding a key", full marks for the general
version: an interface that appears in response to an action should not accept that same action
immediately. Credit anyone who notices that this is also why "are you sure?" dialogues put the dangerous
option away from where your cursor already is.

**E3.** The stack almost solves it. `push(settings)` then `pop()` returns to whatever was below — title or
pause — with no code that cares which. That is the point of a stack.

What is left to decide, and this is the mark: **the settings screen looks different in the two places.**
Over the title it can be opaque and full-screen; over a paused game it probably should not hide the game
entirely. So either the scene takes a parameter, or there are two thin wrappers around one shared body.
Credit anyone who spots that the *navigation* problem is solved and the *presentation* problem is not.

**E4.** This is the question the lesson was built towards. A good answer separates three things:

- **Scenes:** `playScene` (for the level), `fadeScene` (pushed on top, a timer and a rectangle), possibly a
  `loadScene`.
- **Data that belongs to the level:** the tilemap, the enemies, the coins. Created in `enter`, thrown away
  in `exit`. It *should* be destroyed.
- **Data that outlives the level:** score, health, lives, which level is next, and the settings. This
  cannot live in any scene, because every scene that holds it will be exited.

So the answer to "where does the data live while no scene owns it?" is: **in something that is not a
scene** — a `Session` or `GameState` object the scene manager does not touch. Full marks for arriving at
that, by any name.

The sequence is worth drawing on the board:

```
play (level 1)  ──door──▶  push fade-out
                           on finish: Session.level = 2
                                      Scenes.go(play)   ← enter() builds level 2
                                      push fade-in
```

Notice the score was never passed anywhere. It did not have to be, because it was never inside a scene.
Students who reach this have understood the difference between state and storage, which is a genuinely
advanced idea arrived at from a concrete problem.

---

## If you only mark one thing

Play their game twice in a row without reloading the page. If the second game is identical to the first,
`enter` is doing its job and the scene structure is sound. If it is not, nothing else in the lesson has
landed, however good the pause screen looks.
