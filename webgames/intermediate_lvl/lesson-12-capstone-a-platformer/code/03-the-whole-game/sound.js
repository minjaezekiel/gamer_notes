/* ===========================================================================
   sound.js — oscillators and envelopes, no files. From lesson 8.

   Depends on: nothing.

   The context is created LAZILY, on the first sound, which is after the first
   input - so there is nothing suspended and nothing to resume. Every sound has an
   envelope, because without one it clicks.
   ======================================================================== */
let audio = null;
let master = null;
let muted = false;

/* A real feature, and also what selftest.html uses: a synthetic key press is not
   a "user gesture" as far as a browser is concerned, so an automated test that
   drives the game would otherwise trip the autoplay rule on every sound. That the
   warning appears at all is useful evidence that the rule is real. */
export function setMuted(on) {
  muted = !!on;
  if (master) { master.gain.value = muted ? 0 : 0.22; }
}
export function isMuted() { return muted; }

function ensure() {
  if (muted) { return false; }
  if (audio) {
    if (audio.state === "suspended") { audio.resume(); }
    return true;
  }
  try {
    const Ctor = window.AudioContext || window.webkitAudioContext;
    if (!Ctor) { return false; }
    audio = new Ctor();
    master = audio.createGain();
    master.gain.value = 0.22;        // headroom. Never 1.
    master.connect(audio.destination);
    return true;
  } catch (err) {
    return false;                    // no audio: the game still plays
  }
}

function tone(type, f1, f2, attack, decay, peak) {
  if (!ensure()) { return; }
  const now = audio.currentTime + 0.005;
  const osc = audio.createOscillator();
  const gain = audio.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(f1, now);
  if (f2 !== f1) { osc.frequency.linearRampToValueAtTime(f2, now + attack + decay); }
  osc.connect(gain);
  gain.connect(master);
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.linearRampToValueAtTime(peak, now + Math.max(0.001, attack));
  /* exponentialRamp cannot reach 0 - you cannot get there by multiplying. */
  gain.gain.exponentialRampToValueAtTime(0.0001, now + attack + decay);
  osc.start(now);
  osc.stop(now + attack + decay + 0.02);
}

function wobble() { return 0.94 + Math.random() * 0.12; }

export function jump() { tone("square", 170 * wobble(), 540, 0.005, 0.16, 0.45); }
export function land() { tone("triangle", 150 * wobble(), 90, 0.004, 0.1, 0.4); }

export function coin(index) {
  const w = wobble();
  const base = 988 * Math.pow(2, ((index || 0) * 2) / 12) * w;
  tone("sine", base, base, 0.004, 0.11, 0.42);
  window.setTimeout(function () {
    tone("sine", base * 1.335, base * 1.335, 0.004, 0.11, 0.34);
  }, 70);
}

export function hurt() {
  tone("square", 300 * wobble(), 80, 0.002, 0.2, 0.5);
}

export function win() {
  const steps = [0, 4, 7, 12];
  for (let i = 0; i < steps.length; i++) {
    window.setTimeout(function () {
      const f = 523 * Math.pow(2, steps[i] / 12);
      tone("triangle", f, f, 0.005, 0.18, 0.4);
    }, i * 90);
  }
}
