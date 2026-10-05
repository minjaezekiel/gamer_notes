/* ===========================================================================
   config.js — every number you might want to tune. Depends on NOTHING.

   The jump is expressed in the units of the DESIGN - how high, and how long to
   the top - and gravity is worked out from those. So changing the jump height is
   one edit, and nothing else in the game has to be re-tuned.
   ======================================================================== */
export const TILE = 30;

/* ---- the jump, in design units ---- */
export const JUMP_HEIGHT = TILE * 3.1;     // pixels
export const TIME_TO_APEX = 0.32;          // seconds

/* ---- worked out from the two above ---- */
export const GRAVITY_UP = (2 * JUMP_HEIGHT) / (TIME_TO_APEX * TIME_TO_APEX);
export const JUMP_SPEED = GRAVITY_UP * TIME_TO_APEX;
export const GRAVITY_DOWN = GRAVITY_UP * 1.9;      // fast fall
export const APEX_THRESHOLD = 110;                 // |vy| counting as "near the top"
export const APEX_SCALE = 0.55;
export const RELEASE_CUT = 0.45;                   // variable jump height
export const COYOTE_TIME = 0.10;
export const JUMP_BUFFER = 0.12;
export const MAX_FALL_SPEED = 900;                 // so a long fall cannot tunnel

/* ---- running ---- */
export const RUN_SPEED = 215;
export const RUN_ACCEL = 1600;
export const GROUND_DRAG = 12;
export const AIR_DRAG = 2.2;

/* ---- enemies (lesson 10) ---- */
export const ENEMY_SPEED = 72;
export const ENEMY_CHASE_SPEED = 118;
export const ENEMY_SIGHT = 150;
export const ENEMY_GIVE_UP_GAP = 70;               // the hysteresis band

/* ---- camera (lesson 6) ---- */
export const CAMERA_DEAD_ZONE_X = 130;
export const CAMERA_DEAD_ZONE_Y = 110;
export const CAMERA_SMOOTH = 7;                    // per second

/* ---- juice (lesson 9) ---- */
export const SHAKE_LAND = 2.0;
export const SHAKE_COIN = 1.2;
export const SHAKE_HIT = 7.0;
export const SHAKE_MAX = 12;
export const SHAKE_DECAY = 8;
export const HITSTOP_COIN = 0.02;
export const HITSTOP_HIT = 0.08;
export const MAX_PARTICLES = 500;

/* ---- scoring ---- */
export const COIN_SCORE = 10;
export const START_LIVES = 3;

export const INK = "#e7ecf3";
