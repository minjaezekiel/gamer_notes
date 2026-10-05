# Lesson 8 — Sound Design With Web Audio

> **Web Games · Intermediate level · Lesson 8 of 12 · 2 hours 30 minutes**

## By the end of today you will have built

A complete sound system for your game, with **no audio files at all** — jumps, coins, hits,
explosions, a laser, a menu beep, and a short piece of music that loops in time. All of it made out of
numbers, so it works offline, loads instantly, and can be changed by editing a value rather than by
opening an audio editor.

```
   coin          jump            explosion        laser
   ▁▇▆▅▃▁        ▁▃▅▇▅▃▁         ▇▆▅▄▃▂▁         ▇▅▃▂▁
   two short     a rising        filtered         a falling
   sine notes    sweep           noise            sweep
```

You will also fix the single most common complaint about home-made game audio: the **click** at the
start of every sound.

## Where this fits

- **Back:** beginner [lesson 5](../../beginner_lvl/lesson-05-rules-score-and-feel/notes.md) made one
  beep with an oscillator. Today that becomes a system.
- **Forward:** [lesson 9](../lesson-09-particles-and-juice-engineering/notes.md) is the rest of game
  feel, and sound is more than half of it. [Lesson 11](../lesson-11-saving-and-loading/notes.md) saves
  the volume setting.
- **Other tracks:** Python's intermediate lesson 8 uses `pygame.mixer`, and C++'s intermediate lesson 10
  uses raylib's audio with a careful look at who unloads a sound. Both of those load files; this track
  generates sound, which is a genuinely different and useful skill.

---

## The idea, in plain words

### Sound is a number, 48,000 times a second

A speaker cone pushes air. To make it move, your computer sends it a stream of numbers — typically
**48,000 per second** — each saying where the cone should be. Draw those numbers as a graph and you have
a waveform.

That is all audio is. A "sound file" is a list of those numbers. An **oscillator** is a way of producing
them from a formula instead, which is why this lesson needs no files:

| Shape | Sounds like | Good for |
|---|---|---|
| `sine` | pure, soft, flute-like | coins, menu beeps, anything gentle |
| `square` | buzzy, hollow, retro | 8-bit jumps, lasers, alarms |
| `sawtooth` | harsh, bright, aggressive | engines, big weapons |
| `triangle` | between sine and square | bass notes, soft retro |

Choosing the shape is most of a sound's character, and it is one string.

### Pitch is a frequency, and the maths is friendlier than you expect

How many times per second the wave repeats is the **frequency**, in hertz. 440 Hz is the A that
orchestras tune to.

The useful fact: **doubling the frequency goes up exactly one octave.** 440 → 880 is the same note,
higher. That one rule means you can build a usable scale with one line of arithmetic rather than a
lookup table (see the maths section).

### Loudness over time: the envelope, and the click

Here is the part everybody gets wrong first. Start an oscillator, stop it 200 ms later, and you hear a
**click** at both ends.

The reason is physical. At the moment you start, the wave jumps from silence to full height
*instantly*. A speaker cone cannot move like that, and the attempt is a click — the same sound as
plugging in a cable.

The fix is to change the loudness *gradually*, over a few milliseconds. That shape is called an
**envelope**, and it is also where almost all of a sound's personality lives:

```
 1 ┤    ╱╲                          1 ┤        ╱▔▔▔╲
   │   ╱  ╲___                        │      ╱       ╲___
 0 ┴──╱       ╲──                   0 ┴────╱             ╲──
    attack  decay                       slow attack, slow decay
    a pluck, a coin, a hit              a swell, a warning, a pad
```

Same note. Completely different sound. **Change the envelope before you change the note** — it is the
faster route to a sound you like.

### The audio graph

Web Audio is built out of **nodes** you connect together, like plugging boxes into each other:

```
   oscillator  ──▶  gain  ──▶  master gain  ──▶  speakers
   (the tone)       (the         (the volume      (destination)
                   envelope)      setting)
```

Each arrow is a `.connect()`. Two things fall out of this shape and both are useful:

- **A master gain gives you a volume control for the whole game, for free.** Everything already goes
  through it.
- **A new oscillator per sound.** Oscillators are one-shot: once stopped, they cannot be restarted. That
  feels wasteful and is not — they are extremely cheap, and the browser cleans them up.

### The thing that will waste your first hour: the autoplay rule

```js
const audio = new AudioContext();
playBeep();        // nothing happens. No error. Silence.
```

Browsers refuse to make sound until the user has interacted with the page — a click or a key press. This
is a good rule, badly timed for you, and it produces **silence with no error message**, which is the
hardest kind of bug.

The fix is to resume the context on the first input of any kind:

```js
/* The context starts "suspended". One click or key press is enough to resume it,
   and from then on everything works. */
function unlockAudio() {
  if (audio.state === "suspended") { audio.resume(); }
}
window.addEventListener("pointerdown", unlockAudio);
window.addEventListener("keydown", unlockAudio);
```

Put this in every project from now on, and if a game is ever silent, check
`console.log(audio.state)` before anything else.

### Audio timing is not game timing

This is the part that makes audio feel different from everything else in this course.

Your game loop runs about 60 times a second, and the gaps between frames wobble by a few milliseconds.
You have spent seven lessons learning that this is fine, because `dt` absorbs it.

**Audio does not forgive it.** A note that is 15 ms late is *audibly* late — people detect timing errors
in rhythm at around 10 ms, far below the threshold for noticing anything visual. So music driven by your
game loop sounds drunk.

Web Audio solves this by letting you schedule sounds in the **future**, on its own clock:

```js
// NOT setTimeout. NOT a game-loop counter. The audio clock.
const when = audio.currentTime + 0.5;      // exactly half a second from now
osc.start(when);
osc.stop(when + 0.2);
```

`audio.currentTime` is a high-precision clock running in the audio hardware. Anything you schedule
against it happens at exactly that moment, no matter what your frame rate is doing — even if your game
drops a frame. For one-off effects, scheduling "now" is fine. For anything rhythmic, schedule ahead.

The standard pattern is a **look-ahead scheduler**: every frame, look a little way into the future and
schedule everything due before then.

```js
const LOOK_AHEAD = 0.15;        // schedule anything due in the next 150 ms
let nextNoteTime = 0;

function updateMusic() {
  while (nextNoteTime < audio.currentTime + LOOK_AHEAD) {
    playNote(melody[step], nextNoteTime);      // scheduled, not played
    nextNoteTime += SECONDS_PER_STEP;          // exact, never drifts
    step = (step + 1) % melody.length;
  }
}
```

Read what that does: the game loop is only deciding *what* to schedule. The *when* is arithmetic on the
audio clock, so the music stays in time even if your frame rate is a mess. That split — the loop decides,
the audio clock keeps time — is the whole idea.

### Noise, for anything that is not a note

An explosion is not a pitch. It is noise, which means **random numbers** instead of a wave:

```js
/* Build a buffer of random samples once, then play copies of it. */
function makeNoiseBuffer(seconds) {
  const length = audio.sampleRate * seconds;
  const buffer = audio.createBuffer(1, length, audio.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < length; i++) {
    data[i] = Math.random() * 2 - 1;      // every sample random between -1 and 1
  }
  return buffer;
}
```

Raw noise is a hiss. Put it through a **filter** — which removes some frequencies — and it becomes
something:

| Noise plus | Sounds like |
|---|---|
| a lowpass filter sweeping down | an explosion, a thud |
| a highpass filter | wind, a hiss, steam |
| a very short envelope | a snare drum, a footstep |

That table is most of a sound-effects library.

### Not too many at once

Twenty sounds at full volume at the same instant add up past what a speaker can produce, and the result
is **clipping** — a harsh crackle. Two defences, both one line:

```js
masterGain.gain.value = 0.3;        // leave headroom. Never run at 1.
```

```js
/* Refuse to start a sound if too many are already playing. */
if (activeSounds > 12) { return; }
```

And a third that matters more than either: **do not play the same sound twice in the same frame.** Eight
coins collected on one frame is one coin sound, perhaps slightly louder — not eight, which is a mess.

---

## The idea, in pictures

Open [why sounds need an envelope](../../../shared/visualizers/audio-envelope.html).

**What to look for:** the top graph is loudness over time; the bottom is the actual wave going to the
speaker. Step through it and follow the playhead. Then switch the envelope **off**: the wave jumps from
silence to full height in one step, and that vertical edge is the click. Make the attack very long and
the same note becomes a swell — the tone never changed, only the shape. The graph on the right is the
node chain: oscillator into gain into master into speakers.

---

## The idea, in code

Every example makes sound, so start with the volume low.

1. `code/01-one-sound-and-the-click.html` — a single beep, with and without an envelope, and the
   autoplay-rule message. Listen to the click.
2. `code/02-a-sound-library.html` — eight game sounds built from oscillators, sweeps and noise, each on
   a button, each with its parameters on sliders so you can hear what every number does.
3. `code/03-music-on-the-audio-clock.html` — a looping melody, with a switch between `setTimeout` timing
   and the look-ahead scheduler. The difference is immediately audible.
4. `code/04-sound-in-a-game.html` — a small game wired up: one sound per event, a master volume, a limit
   on simultaneous sounds, and a counter that proves the limit is working.

---

## The maths you just used

**1. Octaves are doubling.** Multiply a frequency by 2 and you get the same note one octave up. That is
an exponential relationship, not a linear one: the gap from 220 to 440 is one octave, and so is the gap
from 440 to 880, even though one is 220 Hz wide and the other 440 Hz.

**2. A scale from one formula.** Western music divides an octave into 12 equal steps, so each step
multiplies the frequency by the twelfth root of 2 (about 1.0595):

```js
/* semitones above the A at 440 Hz. 12 gives 880, which is the octave. */
function noteToFrequency(semitones) {
  return 440 * Math.pow(2, semitones / 12);
}
```

That one line replaces a table of 88 numbers, and it is why a tune can be written as
`[0, 4, 7, 12]` — which is a chord — instead of as frequencies.

**3. Why ramps are exponential.** Human hearing works in ratios, not differences: 0.1 to 0.2 sounds like
the same jump as 0.4 to 0.8. So a volume fade that *sounds* even is a multiplication each step, not a
subtraction. That is why Web Audio offers `exponentialRampToValueAtTime`, and why it **cannot ramp to
exactly 0** — you can never reach zero by multiplying. Ramp to `0.0001` instead:

```js
gain.gain.exponentialRampToValueAtTime(0.0001, when + 0.2);   // not 0
```

Passing 0 throws an error, and it is a confusing one the first time.

**4. Samples and seconds.** `sampleRate` is how many numbers per second — usually 48,000. So the number
of samples in half a second is `audio.sampleRate * 0.5`. Every buffer length in this lesson is that
multiplication.

---

## Break it on purpose

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Remove the envelope entirely from a sound | | |
| Make the attack 0 instead of 0.005 | | |
| Ramp the gain to exactly `0` with `exponentialRampToValueAtTime` | | |
| Set `masterGain.gain.value = 1` and fire ten sounds at once | | |
| Schedule music with `setTimeout` instead of the audio clock, then drag a window about | | |
| Reuse one oscillator for every sound instead of making a new one | | |
| Play the coin sound once per coin, then collect eight at once | | |
| Remove the `resume()` on first input, and reload the page | | |

The `setTimeout` one needs you to make the browser busy — scroll, resize, open a menu — and then the
rhythm falls apart. The audio-clock version does not.

---

## Think like an engineer

1. Sound effects in this lesson are built from **parameters** — a shape, a start frequency, an end
   frequency, an attack and a decay. That is a small data structure. What would you gain by putting all
   your sounds in one table, as you did with tiles in lesson 5? What would you lose?
2. A player collects eight coins in one frame. Playing eight coin sounds is wrong. Playing one is a lie.
   What *should* happen? Design it. (Think about what the player is trying to learn from the sound.)
3. **Design something.** Footsteps. The player walks, and you need a step sound that is never identical
   twice, never machine-regular, and stops the instant they stop. What varies, by how much, and what
   decides *when* a step happens? (Tying it to a timer and tying it to the walk animation give
   noticeably different results.)
4. **The hard one.** Your game's music should get more intense as the player's health drops — not
   switch tracks, but change. With oscillators and a scheduler, you can do things a recorded track
   cannot. Name three musical things you could change at runtime, and say which would be audible without
   being annoying.

---

## Vocabulary

| Word | What it means |
|---|---|
| **Sample** | One number describing the speaker position at one instant. |
| **Sample rate** | How many samples per second. Usually 48,000. |
| **Oscillator** | A node that produces a wave from a formula. One-shot. |
| **Frequency** | Repeats per second, in hertz. Doubling is one octave up. |
| **Envelope** | How loudness changes over time. Attack, then decay. |
| **Attack** | How long the sound takes to reach full volume. |
| **Gain node** | A volume control. Multiplies everything passing through it. |
| **`audio.currentTime`** | The audio clock. Schedule against this, never `setTimeout`. |
| **Look-ahead scheduler** | Every frame, schedule everything due in the next 150 ms. |
| **Filter** | Removes some frequencies. Turns noise into a sound. |
| **Clipping** | Harsh crackle when the total is louder than a speaker can produce. |
| **Autoplay rule** | No sound until the user has interacted. Causes silence with no error. |

---

## Recap

- Sound is a stream of numbers. An **oscillator** makes them from a formula, so you need no files.
- A sound's character is mostly its **envelope**, not its note. Change the shape first.
- No envelope means a **click**, because the wave jumps instantly. Ramp over a few milliseconds.
- Everything goes through a **master gain**, which is your volume control for free.
- **Schedule against `audio.currentTime`**, never `setTimeout`. Audio timing errors are audible at 10 ms.
- **Noise plus a filter** is every explosion, footstep and gust of wind you will need.
- Leave **headroom** (master around 0.3), cap simultaneous sounds, and never play one sound eight times
  in one frame.
- If there is no sound and no error, check `audio.state` — the autoplay rule.

---

## Stretch goals

1. **A sound table.** Move every effect into one data structure, as in question 1, and make a new sound a
   line of data rather than a function.
2. **Pitch variation.** Multiply every sound's frequency by a random number between 0.94 and 1.06. One
   line, and repeated sounds immediately stop being grating.
3. **A drum pattern.** Three noise-based sounds and a 16-step grid of booleans. Then make the grid
   editable by clicking.
4. **Two-layer music.** A bass line always playing, and a melody that fades in when the player is in
   danger. Use two gain nodes and a `linearRampToValueAtTime`.
5. **Draw what you hear.** Add an `AnalyserNode` and draw the live waveform on your canvas. This makes
   every other experiment in the lesson easier to understand.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** `01-one-sound-and-the-click.html` on a speaker the whole room can hear. Play the no-envelope version a few times. Ask what the extra noise is. Then switch the envelope on. |
| 10–25 | **Concept.** The envelope visualizer, and the vertical edge. Then the node graph on the board, and the autoplay rule — tell them about it before they lose an hour to it. |
| 25–40 | **Live-code** one sound end to end: context, oscillator, gain, connect, envelope, start, stop. |
| 40–50 | Break. |
| 50–120 | **Build.** Section D. Headphones if you have them, or this is a loud seventy minutes. |
| 120–140 | **Listening gallery.** Everyone plays their explosion. Vote. This is the audio equivalent of lesson 3's tuning gallery and works just as well. |
| 140–150 | Recap. Lesson 9 is the rest of game feel. |

**Before the lesson: sort out the noise problem.** Thirty students generating explosions is genuinely
unworkable without headphones. If you have none, run it as a whole-class exercise on the projector for
the first half and have them work muted, checking their waveform on screen (stretch goal 5) rather than
by ear. Say at the start that everyone drops to volume zero when you raise a hand.

**What usually goes wrong**

1. **No sound at all, no error.** The autoplay rule. Expect it from at least a third of the class in the
   first five minutes. Have `console.log(audio.state)` on the board.
2. **Everything clicks.** No envelope, or an attack of 0.
3. **`exponentialRampToValueAtTime(0, ...)` throws.** The error message does not explain why. Tell them
   the reason — you cannot reach zero by multiplying — rather than just the fix.
4. **Reusing one oscillator.** `start()` on an already-stopped oscillator throws, and students conclude
   that Web Audio is broken. A new oscillator each time is correct and cheap.
5. **Music drifts.** They used `setTimeout`, or added a fixed amount to a game-loop counter.
6. **It sounds awful when several things happen.** Clipping. Lower the master gain to 0.3 and the
   difference is startling.
7. **A sound stops a frame after it should.** They called `stop()` from the game loop instead of
   scheduling it. Schedule the stop at the same moment you schedule the start.

**If you are running short on time** — cut the music scheduler and `code/03` entirely; effects alone are
worth the lesson. Cut noise and filters too if you must, keeping oscillators and envelopes. Do **not**
cut the envelope or the autoplay fix.

**For the student who finishes at minute 90** — stretch goal 2 (random pitch) takes one minute and
improves their game more than anything else here, so give it to everybody. Then stretch goal 5 (draw the
waveform) for anyone who wants to understand rather than just use.

**The point to land at the end:** they made eight recognisable game sounds out of arithmetic, with no
files, no downloads and no audio editor. Sound is not a separate discipline that happens elsewhere — it
is numbers over time, exactly like everything else in this course.
