# Lesson 8 — Solutions and marking notes

---

## Section A

**A1.** [2] One number saying where the speaker cone should be at one instant — one mark. About 48,000 per
second — one mark. Accept 44,100.

**A2.** [3] Without an envelope the wave goes from silence to full height between one sample and the next
— two marks — so the speaker cone is asked to jump instantly, which it cannot do; the attempt is the click
— one mark. Credit anyone who says "a discontinuity in the waveform".

**A3.** [2] oscillator → gain (the envelope) → master gain (the volume) → destination (the speakers). One
mark for the right four, one for the right order.

**A4.** [3] Check `audio.state` — two marks. It will be `"suspended"`, because browsers refuse to produce
sound until the user has interacted with the page, and `resume()` has not been called — one mark. Credit
anyone who notes that the worst part is that it produces silence with **no error**.

**A5.** [3] Because the gaps between frames wobble by a few milliseconds, and a note a few milliseconds
late is audible — people detect rhythmic errors at around 10 ms. Two marks. The same wobble is invisible in
graphics because `dt` absorbs it: the object is drawn in the right place for the time that has actually
passed, whereas a note cannot be played in the right place after the moment has gone — one mark.

**A6.** [2] Because an exponential ramp multiplies by a factor each step, and no amount of multiplying
reaches zero — one mark — so it throws; ramp to a tiny value like `0.0001` instead — one mark.

**A7.** [2] The combined signal is louder than the speaker can produce, so the peaks are flattened and you
hear a harsh crackle — one mark. Any two of: lower the master gain to leave headroom; cap the number of
simultaneous sounds; do not play the same sound several times in one frame; use a compressor — one mark.

---

## Section B

**B1.** [3] One octave above 220 is **440**; two octaves is **880**. One mark. Seven semitones above 440 is
`440 × 2^(7/12) = 440 × 1.498 ≈ **659 Hz**` — two marks. (That is an E, and 440 to 659 is the interval that
makes the first two notes of most coin sounds.)

**B2.** [3] `48,000 × 0.25 = 12,000` samples.

**B3.** [4] The window is `currentTime + 0.15 = 2.15`. Notes are scheduled while `nextNote < 2.15`, giving
2.050, 2.175? No — check each: 2.050 < 2.15 ✓ (schedule, next becomes 2.175); 2.175 < 2.15 ✗ (stop). So
**one note**, at **2.050**. Two marks for the number, two for the time and for showing the loop condition.

Students who answer "two" have added the step before testing. That is worth discussing, because it is the
difference between a scheduler that works and one that drifts.

**B4.** [3] A 0.2-second tone with a **click at both ends** — two marks — because the wave starts and
stops at full amplitude — one mark.

**B5.** [3] The sum is far above what the speaker can produce, so it clips: a harsh crackle rather than ten
sounds — two marks. A master gain of 0.3 leaves headroom, so ten sounds at once add up to about 3 rather
than 10, which is still clipping but far less of it — one mark. Credit anyone who says the real fix is to
cap the count as well.

---

## Section C

**C1.** [3] The context is created suspended, and the first `keydown` plays a sound **before** anything has
resumed it. Two marks. Fix: call `audio.resume()` in that handler before playing, or add a separate unlock
listener — one mark. The reason later sounds work is that the browser resumes the context after the first
real interaction anyway, which makes this one of the most confusing bugs in the lesson.

**C2.** [3] `exponentialRampToValueAtTime` cannot take 0 — two marks. Fix: `0.0001` — one mark.

**C3.** [4] One oscillator is created and reused. Oscillators are **one-shot**: once started and stopped
they cannot be restarted, and calling `start()` twice throws. Two marks. Fix: create a new oscillator (and
a new gain) inside `beep()` every time — two marks.

Worth saying out loud: this feels wasteful and is not. Oscillators are cheap and the browser collects them.
Several students will try to "optimise" by reusing one, which is how they meet this error.

**C4.** [4] `setTimeout` is the bug: it is not accurate, it is delayed whenever the page is busy, and each
delay is **added to the next**, so the error accumulates. Two marks. Fix: schedule against the audio clock
with a look-ahead loop, computing each note time by adding to the previous *scheduled* time rather than to
"now" — two marks.

The accumulation point is the one worth drawing out. A single 20 ms delay is survivable; 100 of them in a
row is a different tune.

**C5.** [3] Two faults. (a) Every coin plays at exactly `audio.currentTime`, so all of them start on the
same sample and add up — two marks. (b) The master gain is 1.0, so there is no headroom and the sum clips —
one mark.

Good fixes: play one sound for the group, or spread them (`currentTime + i * 0.04`), which turns a crackle
into an arpeggio and sounds deliberate. Credit either.

---

## Section D — marking the build

1. **`audio.state` is on screen** (checkpoint 1). This single readout prevents the most common failure in
   the lesson.
2. **The two beeps are side by side** (checkpoint 2). Make them play both to you. If they cannot hear the
   difference, play it louder — it is unmistakable once noticed.
3. **The semitone formula is used** (checkpoint 3), not two hard-coded frequencies.
4. **Jump and laser are the same code** (checkpoint 4). If they wrote two separate functions, ask what
   differs. The answer is one number, and noticing that is the point.
5. **Checkpoint 6 was done and compared.** Twenty identical sounds versus twenty varied ones is the most
   persuasive thirty seconds in this lesson.
6. **Checkpoint 8 with the game deliberately busy.** This is the only test that distinguishes a working
   scheduler from a lucky one.

Classroom management: this lesson is loud. Agree a hand signal for "volume to zero" before anyone writes a
line, and use it.

---

## Section E — marking notes

**E1.** Gains: a new sound is a line of data, so students iterate far faster; sounds become saveable,
shareable and tweakable at runtime; a sound editor becomes possible (and is a good stretch project).
Losses: some sounds do not fit the shape — two oscillators at once, a filter sweep, a chord — so the table
grows fields that most entries do not use, which is exactly the problem lesson 5's E1 identified for tiles.

Full marks for noticing that the right answer is usually **both**: a table for the ordinary 80%, and plain
functions for the few that are genuinely different. Credit anyone who says "start with functions, move to a
table when you have five that are nearly identical".

**E2.** The question is what the sound is *for*. It tells the player "that worked, and here is how much".
So neither extreme is right:

- **One sound, slightly louder or higher** — honest and simple.
- **An arpeggio**: play all eight, spread 30–40 ms apart and rising in pitch. This is what nearly every
  commercial game does, and it turns the problem into a feature — the player hears "eight" without eight
  overlapping noises.
- **A cap**: play at most three, ignore the rest.

Full marks for the arpeggio *or* for any answer that names what the sound communicates and designs
backwards from that. Credit anyone who notices this is the same question as a damage number: the player
needs the *quantity*, not one event per unit.

**E3.** A good answer covers three things:

- **What varies:** pitch (±6%), volume (±15%), and the filter frequency, so no two steps are identical.
- **Never machine-regular:** either vary the interval slightly, or — much better — drive it from the walk
  animation, so a step happens on the frames where a foot is actually down. That makes it automatically
  match the walking speed.
- **Stops instantly:** the step is triggered by movement rather than scheduled ahead, so standing still
  simply never triggers one. This is the reason footsteps should *not* use the look-ahead scheduler, which
  is a nice distinction: music is scheduled, effects are triggered.

Top marks for arriving at animation-driven steps and explaining why it is better than a timer.

**E4.** Three things that can be changed at runtime, with judgement about each:

- **Tempo** — raise it 10–20%. Effective and very audible. Push it further and it becomes comic.
- **Add a layer** — bring in a drum or a second voice by ramping a gain node. The least annoying option,
  because nothing already playing changes.
- **Filter the whole mix** — open a lowpass as danger rises, so the music becomes brighter. Subtle and
  surprisingly powerful.
- **Change the scale** — swap a few notes from major to minor. Dramatic, and risky: it can read as "wrong
  note" rather than "tension".
- **Volume alone** — the laziest option, and it mostly reads as a mistake.

Full marks for three options plus a judgement on which stays pleasant. The best answers notice that the
change must be **reversible and gradual**: if the player heals, the music has to come back down, and
anything that snaps will be noticed as a glitch. That is the tween idea from lesson 3's E4 again, applied
to sound.

---

## If you only mark one thing

Checkpoint 2, the two beeps on two keys, played in front of you. A student who can hear why the envelope
exists will never ship a clicking sound; a student who copied the envelope as a ritual will remove it the
first time it is inconvenient.
