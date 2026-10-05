/* ===========================================================================
   input.js — keyboard in, INTENT out.

   Read this file and notice what is missing: the words "ball", "paddle",
   "brick" and "Breakout" do not appear. It does not know what game it is in.

   That is what makes it reusable. You could drop this file into a racing game
   without editing one character of it. A file that knows nothing is a file you
   understood well enough to isolate.

   It also depends on nothing, so it can load second.
   ======================================================================== */
const Input = {
  keys: {},
  restartRequested: false,

  start: function () {
    document.addEventListener("keydown", function (event) {
      Input.keys[event.key] = true;
      // The browser scrolls the page on arrow keys and space. Not in a game.
      if (event.key.startsWith("Arrow") || event.key === " ") {
        event.preventDefault();
      }
      if (event.key === "r" || event.key === "R") {
        // A one-shot flag: set here, cleared by whoever reads it. That keeps
        // "restart" from happening 60 times while the key is held down.
        Input.restartRequested = true;
      }
    });
    document.addEventListener("keyup", function (event) {
      Input.keys[event.key] = false;
    });
  },

  /* These four functions are the only thing the rest of the game is allowed to
     ask. Add a gamepad later and you edit this file and nothing else. */
  wantsLeft:  function () { return Input.keys["ArrowLeft"]  || Input.keys["a"] || Input.keys["A"]; },
  wantsRight: function () { return Input.keys["ArrowRight"] || Input.keys["d"] || Input.keys["D"]; },
  wantsLaunch: function () { return Input.keys[" "]; },

  takeRestart: function () {
    const was = Input.restartRequested;
    Input.restartRequested = false;      // read it once, then forget it
    return was;
  }
};
