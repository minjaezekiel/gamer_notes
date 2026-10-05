/* ===========================================================================
   main.js — the entry point. The loop, and nothing else.

   Depends on: input, scenes.

   Count the lines that do real work: about five. Everything this file is tempted
   to do belongs to somebody else. It must be the only file index.html names, and
   it is the only file that knows a loop exists.
   ======================================================================== */
import * as Input from "./input.js";
import * as Scenes from "./scenes.js";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

Input.start();
Scenes.init(canvas.width, canvas.height);
Scenes.applyPending();          /* put the title scene on the stack before frame 1 */

let lastTime = 0;

function frame(now) {
  let dt = (now - lastTime) / 1000;
  lastTime = now;
  /* Clamp: one enormous frame - a tab left in the background - would otherwise
     teleport the player through the floor. Beginner lesson 2. */
  if (dt > 0.05) { dt = 0.05; }

  Scenes.update(dt);
  Scenes.draw(ctx);

  Scenes.applyPending();        /* deferred changes, after the frame is finished */
  Input.endFrame();             /* AFTER update: wasPressed needs last frame */
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
