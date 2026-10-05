/* ===========================================================================
   main.js — the entry point. The only file index.html names.

   A module is DEFERRED automatically: it runs after the HTML has been parsed.
   So document.getElementById works here with no DOMContentLoaded wrapper, which
   is not true of a plain <script> in the <head>.
   ======================================================================== */
import * as Game from "./game.js";
import * as Render from "./render.js";
import { start as startInput } from "./input.js";
/* `as` renames an import. Useful when two modules both export `start`. */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

startInput();
const state = Game.create(canvas.width, canvas.height);

let lastTime = 0;
function frame(now) {
  let dt = (now - lastTime) / 1000;
  lastTime = now;
  if (dt > 0.05) { dt = 0.05; }

  Game.update(state, dt);
  Render.draw(ctx, state);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
