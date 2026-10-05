# Lesson 8 — Sound Design With Web Audio

## Cheat sheet

### The graph

```
oscillator → gain → masterGain → speakers
 (tone)     (envelope) (volume)
```

```js
const audio = new AudioContext();
const master = audio.createGain();
master.gain.value = 0.3;      // headroom
master.connect(audio.destination);
```

### One sound

```js
function beep(freq, when, length) {
  const osc = audio.createOscillator();
  const g = audio.createGain();
  osc.type = "square";
  osc.frequency.setValueAtTime(freq, when);
  osc.connect(g);
  g.connect(master);

  // THE ENVELOPE. Without it: a click.
  g.gain.setValueAtTime(0, when);
  g.gain.linearRampToValueAtTime(1, when + 0.005);
  g.gain.exponentialRampToValueAtTime(0.0001, when + length);

  osc.start(when);
  osc.stop(when + length);
}
```

A **new oscillator every time**. They are one-shot and cheap.

`exponentialRampToValueAtTime(0, …)` **throws** — you cannot reach zero by
multiplying. Use `0.0001`.

### The autoplay rule

Silence, no error → check `audio.state`.

```js
function unlock() {
  if (audio.state === "suspended") audio.resume();
}
addEventListener("pointerdown", unlock);
addEventListener("keydown", unlock);
```

### Timing

```js
const when = audio.currentTime + 0.5;   // exact
```

**Never `setTimeout` for anything rhythmic.** 15 ms late is audible; 15 ms of
visual lag is not.

```js
while (nextNote < audio.currentTime + 0.15) {
  playNote(melody[step], nextNote);
  nextNote += STEP_SECONDS;     // never drifts
  step = (step + 1) % melody.length;
}
```

### Noise

```js
const buf = audio.createBuffer(1, n, audio.sampleRate);
const d = buf.getChannelData(0);
for (let i = 0; i < n; i++)
  d[i] = Math.random() * 2 - 1;
```

noise + lowpass sweeping down = **explosion**
noise + highpass = **wind**
noise + very short envelope = **snare, footstep**

### Notes from numbers

```js
freq = 440 * Math.pow(2, semitones / 12);
```

Doubling = one octave. 12 semitones = doubling.

### Shapes

`sine` soft · `square` retro · `sawtooth` harsh · `triangle` between

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> What is a <em>sample</em>, and roughly how many are sent to the speaker each second?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Why does a sound with no envelope click? Explain in terms of what the speaker is being asked to do.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> Name the four nodes in the chain from tone to speaker, in order.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Your game is completely silent and the console is empty. What is the first thing to check, and why does this problem exist?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why must music be scheduled against <code>audio.currentTime</code> rather than driven from the game loop? Why is the same wobble harmless for graphics?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A6.</span> Why can <code>exponentialRampToValueAtTime</code> not ramp to exactly 0?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A7.</span> What is clipping, and name two things that reduce it.
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> A note is 220 Hz. What frequency is one octave above it? Two octaves? Seven semitones above 440 Hz, to the nearest hertz?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> How many samples are in a 0.25-second noise buffer at a sample rate of 48,000?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> The melody has 8 steps and <code>STEP_SECONDS</code> is 0.125. <code>audio.currentTime</code> is 2.00 and <code>nextNote</code> is 2.05, with a look-ahead of 0.15. How many notes get scheduled this frame, and at what times?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> Describe what the player hears.

```js
osc.start(audio.currentTime);
osc.stop(audio.currentTime + 0.2);
// no gain envelope at all
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B5.</span> Ten sounds fire on the same frame, each with a gain of 1, into a master gain of 1. What happens, and what would a master gain of 0.3 change?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The first sound in the game never plays. Every sound after it is fine.

```js
const audio = new AudioContext();
window.addEventListener("keydown", function () { jump(); });
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The console says <code>Failed to execute 'exponentialRampToValueAtTime'</code>.

```js
g.gain.setValueAtTime(1, when);
g.gain.exponentialRampToValueAtTime(0, when + 0.3);
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> The first beep works and every later one throws <code>cannot call start more than once</code>.

```js
const osc = audio.createOscillator();
osc.connect(master);

function beep() {
  osc.frequency.value = 600;
  osc.start();
  osc.stop(audio.currentTime + 0.1);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C4.</span> The music is in time while nothing else is happening, and falls apart whenever the game is busy. Name the bug and the fix.

```js
function playNextNote() {
  playNote(melody[step]);
  step = (step + 1) % melody.length;
  setTimeout(playNextNote, 125);
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C5.</span> Collecting a row of coins produces a horrible crackle rather than a pleasant run of notes. Two separate things are wrong.

```js
for (const coin of touchedCoins) {
  playCoinSound(audio.currentTime);   // master gain is 1.0
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Start from your game, or from `code/01-one-sound-and-the-click.html`.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Create the context and a master gain at 0.3, and add the <code>resume()</code> unlock on first input. Print <code>audio.state</code> on screen &mdash; keep it there all lesson.</li>
<li><strong>Checkpoint 2.</strong> Write one <code>beep(freq, when, length)</code> with an envelope. Then make a version with no envelope and put them on two keys. Listen to both several times.</li>
<li><strong>Checkpoint 3.</strong> Build a <strong>coin</strong>: two short sine notes, the second a few semitones above the first, using the semitone formula.</li>
<li><strong>Checkpoint 4.</strong> Build a <strong>jump</strong>: a square wave sweeping upwards, using <code>frequency.linearRampToValueAtTime</code>. Then a <strong>laser</strong> by sweeping downwards instead. Same code, one number different.</li>
<li><strong>Checkpoint 5.</strong> Build a noise buffer, and from it an <strong>explosion</strong> (lowpass filter sweeping down) and a <strong>footstep</strong> (very short envelope). Put the filter frequency on a slider and find the value you like.</li>
<li><strong>Checkpoint 6.</strong> Add random pitch variation to every sound &mdash; multiply the frequency by <code>0.94 + Math.random() * 0.12</code>. Play the same sound twenty times in a row before and after.</li>
<li><strong>Checkpoint 7.</strong> Wire the sounds into your game: one per event. Add a count of currently-playing sounds on screen, and a cap.</li>
<li><strong>Checkpoint 8.</strong> Add a four-note looping bass line with the look-ahead scheduler. Then make the game deliberately busy (hold a key that spawns a hundred particles) and check the music stays in time.</li>
</ul>

<div class="note">
<span class="note-label">If there is no sound</span>
<p>In this order: is <code>audio.state</code> <code>"running"</code>? Is the master gain
above 0? Is the oscillator connected to the master, and the master to
<code>audio.destination</code>? Is the computer's own volume up? Four checks, in that
order, finds it almost every time.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
<p>Marked on reasoning, and on naming the cost.</p>
</div>

**E1.** Your sounds are built from parameters: shape, start frequency, end
frequency, attack, decay. What would you gain by putting them all in one table, as
you did with tiles in lesson 5? What would you lose?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** Eight coins are collected in one frame. Eight sounds is a mess; one is a
lie. What *should* happen? Think about what the player is meant to learn from the
sound.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Design footsteps: never identical twice, never machine-regular, and silent
the instant the player stops. What varies, by how much, and what decides *when* a
step happens?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E4.** The hard one. The music should become more intense as health drops —
changing, not switching tracks. Name three musical things you could change at
runtime, and say which would be audible without becoming annoying.

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. All sounds in one data table.
2. Random pitch variation everywhere. One line, big improvement.
3. A clickable 16-step drum grid.
4. Two-layer music: a bass line always, a melody that fades in when in danger.
5. An `AnalyserNode` drawing the live waveform on your canvas.
