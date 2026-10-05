/* ===========================================================================
   input.js — keys in, INTENT out. Depends on nothing.

   Read it and notice the words that are missing: player, coin, guard, platformer.
   This file could be dropped into a different game unchanged, which is the whole
   point of lesson 1.
   ======================================================================== */
const keys = {};
let previous = {};

export function start() {
  document.addEventListener("keydown", function (event) {
    keys[event.key] = true;
    if (event.key.startsWith("Arrow") || event.key === " ") { event.preventDefault(); }
  });
  document.addEventListener("keyup", function (event) { keys[event.key] = false; });
  /* If the window loses focus mid-key, the keyup never arrives and the player
     runs for ever. Clearing on blur is two lines and saves a confusing bug. */
  window.addEventListener("blur", function () {
    Object.keys(keys).forEach(function (k) { keys[k] = false; });
  });
}

function down(k) { return !!keys[k]; }
function pressed(k) { return !!keys[k] && !previous[k]; }

/* The game asks THESE. Adding a gamepad means editing this file and no other. */
export function wantsLeft()  { return down("ArrowLeft") || down("a") || down("A"); }
export function wantsRight() { return down("ArrowRight") || down("d") || down("D"); }
export function wantsDrop()  { return down("ArrowDown") || down("s") || down("S"); }
export function jumpHeld()   { return down(" ") || down("ArrowUp") || down("w"); }
export function jumpPressed() {
  return pressed(" ") || pressed("ArrowUp") || pressed("w");
}
export function pausePressed() { return pressed("p") || pressed("P") || pressed("Escape"); }
export function confirmPressed() { return pressed(" ") || pressed("Enter"); }

/* Called at the END of every frame, after update and draw. wasPressed needs last
   frame's keys, so this has to be the last thing that happens. */
export function endFrame() { previous = Object.assign({}, keys); }
