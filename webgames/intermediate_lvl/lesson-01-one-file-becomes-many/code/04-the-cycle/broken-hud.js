/* broken-hud.js — the other half.

   This file reaches UPWARDS: it imports from the module that imports it. The
   import line itself is accepted. The problem is the line after it, which runs
   while broken-game.js is still only half-built. */
import { state } from "./broken-game.js";

/* TOP-LEVEL code, so it runs the moment this module is evaluated - and that is
   BEFORE broken-game.js has finished creating `state`. */
const startingScore = state.score;

export function drawHud() {
  return "score " + startingScore;
}
