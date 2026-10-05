/* fixed-hud.js — imports nothing at all.
   It is now testable on its own, reusable in any game, and impossible to
   involve in a cycle. */
export function drawHud(score) {
  return "score " + score;
}
