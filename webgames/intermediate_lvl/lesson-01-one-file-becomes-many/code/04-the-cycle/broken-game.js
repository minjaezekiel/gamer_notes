/* broken-game.js — half of a circular dependency.
   game needs hud (to draw the HUD) and hud needs game (to read the score). */
import { drawHud } from "./broken-hud.js";

export const state = { score: 7, lives: 3 };

export function start() {
  return drawHud();
}
