/* ===========================================================================
   store.js — from lesson 11. Storage that cannot crash the game.

   localStorage THROWS in a private window or with site data blocked. Not returns
   null: throws. Every access is wrapped, and the game works without it.
   ======================================================================== */
let available = false;

export function init() {
  try {
    localStorage.setItem("__probe", "1");
    localStorage.removeItem("__probe");
    available = true;
  } catch (err) {
    available = false;              // and that is fine
  }
  return available;
}

export function isAvailable() { return available; }

export function load(key, fallback) {
  if (!available) { return fallback; }
  try {
    const text = localStorage.getItem(key);
    if (text === null) { return fallback; }
    const value = JSON.parse(text);
    return value === null ? fallback : value;
  } catch (err) {
    return fallback;                // corrupt: use the default, do not crash
  }
}

export function save(key, value) {
  if (!available) { return false; }
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (err) {
    return false;                   // full or blocked
  }
}

/* The best score is untrusted input: a player can edit it. */
export function loadBest() {
  const raw = load("capstone-best", { score: 0, coins: 0 });
  const score = typeof raw.score === "number" && isFinite(raw.score) && raw.score >= 0
    ? Math.floor(raw.score) : 0;
  const coins = typeof raw.coins === "number" && isFinite(raw.coins) && raw.coins >= 0
    ? Math.floor(raw.coins) : 0;
  return { score: score, coins: coins };
}

export function saveBest(best) {
  return save("capstone-best", { version: 1, score: best.score, coins: best.coins });
}
