/* fixed-game.js — the same two files, one arrow deleted.

   The fix: hud does not need to reach for the score. Whoever calls it already
   has the score, so it gets PASSED IN. The arrow from hud to game disappears,
   and hud becomes a file that knows nothing - which makes it reusable. */
import { drawHud } from "./fixed-hud.js";

export const state = { score: 7, lives: 3 };

export function start() {
  return drawHud(state.score);          // pass the value, do not import it
}
