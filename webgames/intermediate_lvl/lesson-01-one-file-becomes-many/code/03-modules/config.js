/* ===========================================================================
   config.js — as a module.

   `export` is the whole difference from the script-tag version. A name without
   it is PRIVATE to this file: other modules cannot reach it even by accident.
   ======================================================================== */
export const PADDLE_SPEED = 430;
export const BALL_SPEED = 260;
export const LIVES_AT_START = 3;
export const POINTS_PER_BRICK = 10;

export const BRICK_ROWS = 4;
export const BRICK_COLS = 8;
export const BRICK_H = 20;
export const BRICK_GAP = 4;
export const BRICK_TOP = 50;

export const ROW_COLOURS = ["#ff6b6b", "#ffd43b", "#51cf66", "#4dabf7"];
export const INK = "#e7ecf3";

/* Not exported, so nothing outside this file can see it. Try reaching for it
   from game.js and the error arrives immediately rather than at 2am. */
const INTERNAL_NOTE = "row colours repeat if BRICK_ROWS > ROW_COLOURS.length";
