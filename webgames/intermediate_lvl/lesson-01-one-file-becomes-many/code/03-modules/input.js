/* ===========================================================================
   input.js — as a module.

   `keys` is NOT exported. The rest of the game can only ask the four questions
   below, which means the day you add a gamepad you edit this file and no other.
   In the script-tag version `Input.keys` was reachable from anywhere; here the
   boundary is enforced by the language instead of by good manners.
   ======================================================================== */
const keys = {};
let restartRequested = false;

export function start() {
  document.addEventListener("keydown", function (event) {
    keys[event.key] = true;
    if (event.key.startsWith("Arrow") || event.key === " ") {
      event.preventDefault();
    }
    if (event.key === "r" || event.key === "R") { restartRequested = true; }
  });
  document.addEventListener("keyup", function (event) {
    keys[event.key] = false;
  });
}

export function wantsLeft()   { return keys["ArrowLeft"]  || keys["a"] || keys["A"]; }
export function wantsRight()  { return keys["ArrowRight"] || keys["d"] || keys["D"]; }
export function wantsLaunch() { return keys[" "]; }

export function takeRestart() {
  const was = restartRequested;
  restartRequested = false;
  return was;
}
