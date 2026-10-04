# Lesson 5 — Solutions and marking notes

---

## Section A

**A1.** [3] Four true/false flags give 2⁴ = **16** combinations, of which only about four make sense
— the rest are nonsense like "in the menu *and* paused *and* dead". One state variable gives exactly
**four** possibilities and all four are valid. Two marks for the numbers, one for the key point: the
bad states are not *fixed*, they are made **impossible to write**.

**A2.** [2] A transition is a permitted move from one state to another. A key press with no
transition for the current state is **ignored**, and that is correct behaviour rather than a missing
feature.

**A3.** [2] `save` remembers the canvas transform and `restore` puts it back. Without the restore,
each frame's shake offset is added on top of the last one, so the whole game drifts off the screen
within about a second.

**A4.** [2] About **100 milliseconds** (a tenth of a second). Longer becomes distracting and, for
some players, genuinely nauseating; it also delays their view of what happened next.

**A5.** [3] `alpha = life / totalLife` = `0.12 / 0.45` ≈ **0.27**. Two marks for the expression, one
for the number (accept 0.26–0.27).

---

## Section B

**B1.** [4] **Three are left.** This is the single most common array bug there is.

Walk through it:

| i | array before | splice removes | array after | next i |
|---|---|---|---|---|
| 0 | [A B C D E F] | A | [B C D E F] | 1 → but B is now at index 0, so B is skipped |
| 1 | [B C D E F] | C | [B D E F] | 2 → D skipped |
| 2 | [B D E F] | E | [B D F] | 3 → length is 3, loop ends |

So B, D and F survive: **three left**. Removing an item shifts everything after it down one index,
so the loop steps over the next element every time.

Two marks for "three", two for the explanation. Fix: loop backwards.

**B2.** [3] The game **slides off the screen**. Each frame's `translate` is applied on top of all the
previous ones, so the offsets accumulate. With random offsets it will wander; with a constant one it
leaves in a straight line. Within a second or so the canvas is blank.

**B3.** [3] The paddle **still moves**, because that `if` does not check the state. Only the ball is
stopped. This is exactly the mistake described in C1 — the state check is in the wrong place.

**B4.** [4] Two marks each:

- **Version A** produces an even **circle**, because every angle is equally likely and the speed is
  the same in all directions.
- **Version B** produces a **square**, and has **more particles heading diagonally**, because the
  corners of a square are further from the centre (about 1.41× further) than the middles of its
  edges. The spray looks subtly lumpy, with four bulges.

Students who only say "A is a circle, B is a square" get three; the diagonal bias is the fourth mark.

---

## Section C

**C1.** [4] The approach makes pausing depend on **remembering a line in every single object** — the
ball, each paddle, each particle, each enemy, the timer, the score popup. There will be twenty such
places by the end of the project and you will miss one, which is exactly what has happened here.

The correct approach is to check **once**, in the loop, and simply not call the update functions at
all. Then a newly added object is paused automatically, with no code and nothing to remember.

Two marks for identifying the scattering, two for the general principle. The best answers note that
this is the same idea as the state machine itself: make the wrong thing impossible rather than
relying on discipline.

**C2.** [4] The `AudioContext` is created when the page loads, before the user has interacted with
the page. Browsers start it in a **suspended** state and it never produces sound. No error is thrown.

Two marks for the diagnosis. Two for the reason the browsers do it: it is a deliberate policy to stop
pages — especially advertisements — from playing sound at you the instant they open. Creating the
context lazily inside the first `beep` works because the first beep always follows a key press.

(Accept `audio.resume()` on first interaction as an alternative fix; it is what larger games do.)

**C3.** [3] The volume fade. Without
`vol.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + duration)` the oscillator is cut
off mid-wave, and a sudden jump in the waveform is heard as a click. Accept any answer describing an
envelope, fade or ramp.

---

## Section D — marking the build

Checkpoint 4 is a full pass. Most students will spend most of the build on juice, and that is the
right use of the time.

**Checkpoint 3 — the classic.** Students forget to reset the scores in `startGame()`, so the second
game begins at 5–3 and ends instantly. Let them find it; it is a good example of state that needs
explicit clearing.

**Checkpoint 4 — the eyes-shut test** is worth insisting on. If the three sounds are distinguishable
by ear alone, the sound design is doing real work. If they all sound the same, it is decoration.

**Checkpoint 5.** Expect at least one student to produce an unplayable earthquake. This is a *good*
mistake and teaches the 100 ms rule far better than being told it. Put their screen on the projector
with their permission and ask the class what is wrong.

**Checkpoint 6.** Watch for particles continuing to move while paused — the classic consequence of
putting the state check in the wrong place.

**Protect the show-and-tell time.** Thirty seconds each, everyone demos their juice. It is the best
twenty minutes of the beginner course: students see twenty different interpretations of the same
brief and immediately start borrowing from each other.

---

## Section E — marking notes, not answers

**E1/E2 — state diagrams.** Mark on completeness and honesty rather than neatness. Good diagrams
include the forgotten states. Good answers to E2 usually find something like:

- PAUSED → GAME_OVER would mean the game could end while frozen, so the player never sees what killed
  them.
- MENU → GAME_OVER makes no sense: there is no score to show.
- Skipping a loading state means the game starts before its assets exist.

**E3.** Looking for three genuinely different channels. A good answer for, say, taking damage:
**seen** (a red flash and the health bar dropping), **heard** (a grunt and a lower-pitched music
layer), **felt** (controller rumble, or a brief loss of control, or hitstop). Weak answers give three
visual effects and call them three senses.

**E4 — the ethics question.** There is no answer and that is the point. Things worth drawing out:

- Feedback that tells the truth about the game state (a hit flash, a damage number) helps the player
  play. Feedback designed to produce a feeling unconnected to anything real (a slot machine's
  near-miss animation, loot-box reveal sequences) is doing something else.
- The honest difficulty: *where exactly* is the line? A satisfying reload animation conveys nothing
  mechanical and nobody objects to it.
- Whether the player can tell matters, but it is not sufficient. People know slot machines are
  designed that way and it works anyway.
- The strongest answers notice that the same technique can be either, depending on what it is
  attached to — screen shake on a critical hit informs; screen shake on a purchase confirmation does
  not.

Let the argument run. Students care about this one, especially those who play games with loot boxes
or battle passes, and they often have sharper opinions than adults expect.

---

## Stretch goals

1. **Hitstop** is the best one. Four lines:
   ```js
   let freezeTime = 0;
   // on hit: freezeTime = 0.04;
   // in frame(): if (freezeTime > 0) { freezeTime -= dt; render(); requestAnimationFrame(frame); return; }
   ```
   The counter-intuitive result — that stopping the game briefly makes it feel *more* responsive — is
   worth discussing. The usual explanation is that the pause gives the player's eye time to register
   the impact before the world moves on.
5. **Accessibility.** If a student implements the shake toggle, take thirty seconds to point out that
   this is not a nicety. Vestibular disorders are common, and screen shake with no off switch makes a
   game unplayable for those people. Good follow-up question: what else in their game assumes the
   player can see colour, hear sound, or react in under 200 ms?
