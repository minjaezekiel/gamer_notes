/* ===========================================================================
   level.js — the world as text, and the table that says what each character
   means. From lesson 5.

   Depends on: config (for TILE).

   '#' solid   '=' one-way (solid only from above)   '^' deadly
   'o' coin    '@' the player start                  'E' an enemy start
   'F' the flag
   ======================================================================== */
import { TILE } from "./config.js";

export const ROWS_TEXT = [
  "..........................................",
  "..........................................",
  ".........o...........o.o.o................",
  "........====........=======...............",
  "....o.....................................",
  "...====........o..................o.o.o...",
  "..............====...........====#########",
  ".@...........................E............",
  "####.......E.....o........................",
  "...#....########====####.......o..........",
  "...#...............................====...",
  "...#######^^^^^#########....o.............",
  "..................#####................F.",
  "...............^^^^^^^^^^^^^^^^^^^^^^^^###",
  "##########################################"
];

export const TILES = {
  ".": { solid: false, oneWay: false },
  "@": { solid: false, oneWay: false },
  "o": { solid: false, oneWay: false, coin: true },
  "E": { solid: false, oneWay: false },
  "F": { solid: false, oneWay: false, flag: true },
  "#": { solid: true,  oneWay: false },
  "=": { solid: false, oneWay: true },
  "^": { solid: false, oneWay: false, deadly: true }
};

export const COLS = ROWS_TEXT[0].length;
export const ROWS = ROWS_TEXT.length;
export const WORLD_WIDTH = COLS * TILE;
export const WORLD_HEIGHT = ROWS * TILE;

/* A startup check. A short row returns an EMPTY STRING for the missing columns,
   which is not "#", so that part of the world silently has no floor. */
export function check() {
  for (let row = 0; row < ROWS; row++) {
    if (ROWS_TEXT[row].length !== COLS) {
      return "row " + row + " is " + ROWS_TEXT[row].length + " chars, not " + COLS;
    }
  }
  return null;
}

export function charAt(col, row) {
  /* OUT OF BOUNDS IS SOLID, except above the world - so a high jump is allowed
     but walking off the side is not. */
  if (col < 0 || col >= COLS) { return "#"; }
  if (row < 0) { return "."; }
  if (row >= ROWS) { return "#"; }
  return ROWS_TEXT[row].charAt(col);
}

export function info(col, row) { return TILES[charAt(col, row)] || TILES["."]; }
export function isSolid(col, row) { return info(col, row).solid; }
export function isOneWay(col, row) { return info(col, row).oneWay; }

export function findAll(ch) {
  const out = [];
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      if (charAt(col, row) === ch) { out.push({ col: col, row: row }); }
    }
  }
  return out;
}
