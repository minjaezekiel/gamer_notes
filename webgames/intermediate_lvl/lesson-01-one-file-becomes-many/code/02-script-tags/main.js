/* ===========================================================================
   main.js — the ENTRY POINT. The loop, and nothing else.

   Depends on: Game, Render, Input.

   Count the lines that do real work. There are about five. That is the goal for
   an entry point: it wires things together and gets out of the way. Everything
   it is tempted to do itself belongs to somebody else.

   This file must load LAST, because it is the only one that needs all the
   others.
   ======================================================================== */
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

Input.start();
const state = Game.create(canvas.width, canvas.height);

let lastTime = 0;
function frame(now) {
  let dt = (now - lastTime) / 1000;
  lastTime = now;
  // Clamp dt: one enormous frame (a tab left in the background) would otherwise
  // teleport the ball through a wall. Beginner lesson 2.
  if (dt > 0.05) { dt = 0.05; }

  Game.update(state, dt);
  Render.draw(ctx, state);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
