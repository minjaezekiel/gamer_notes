/* ===========================================================================
   config.js — every number you might want to tune, in one place.

   This file DEPENDS ON NOTHING. That is why it can safely load first, and it is
   the best possible property for a file to have.

   One global name (Config) with everything hanging off it, because plain script
   tags all share the same global space and two files declaring the same loose
   variable would collide.
   ======================================================================== */
const Config = {
  PADDLE_SPEED: 430,          // pixels per second
  BALL_SPEED: 260,            // pixels per second
  LIVES_AT_START: 3,
  POINTS_PER_BRICK: 10,

  BRICK_ROWS: 4,
  BRICK_COLS: 8,
  BRICK_H: 20,
  BRICK_GAP: 4,
  BRICK_TOP: 50,

  // Colours by row. Changing the look of the game now means editing one array
  // in one file, instead of hunting through the brick-building loop.
  ROW_COLOURS: ["#ff6b6b", "#ffd43b", "#51cf66", "#4dabf7"],
  INK: "#e7ecf3"
};
