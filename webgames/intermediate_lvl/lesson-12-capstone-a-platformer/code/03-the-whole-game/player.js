/* ===========================================================================
   player.js — the six-part jump and the two-step collision.

   Depends on: config, level, input.
   Knows nothing about: the canvas, the camera, scenes, sound.

   This file is the heart of the game, and it is about 120 lines. Read the update
   function top to bottom: it is the order from lesson 12's notes.
   ======================================================================== */
import * as C from "./config.js";
import * as Level from "./level.js";
import * as Input from "./input.js";

export function create() {
  const start = Level.findAll("@")[0] || { col: 1, row: 1 };
  return {
    x: start.col * C.TILE + 4,
    y: start.row * C.TILE,
    w: 20, h: 26,
    vx: 0, vy: 0,
    onGround: false,
    coyote: 0,
    buffer: 0,
    dropTimer: 0,
    prevBottom: 0,
    facing: 1,
    squash: 0,
    landImpact: 0,
    invulnerable: 0
  };
}

export function reset(player) {
  const fresh = create();
  Object.keys(fresh).forEach(function (k) { player[k] = fresh[k]; });
}

/* Which tiles does this box touch? At most four. From lesson 5, including the
   epsilon that stops a box whose edge is exactly on a boundary counting the next
   tile along. */
function range(box) {
  return {
    c0: Math.floor(box.x / C.TILE),
    c1: Math.floor((box.x + box.w - 0.001) / C.TILE),
    r0: Math.floor(box.y / C.TILE),
    r1: Math.floor((box.y + box.h - 0.001) / C.TILE)
  };
}

/* A one-way tile is solid only when we are moving DOWN and our bottom edge was
   above its top edge before this frame's move. Both halves are needed. */
function blocking(player, col, row, movingDown) {
  if (Level.isSolid(col, row)) { return true; }
  if (!Level.isOneWay(col, row)) { return false; }
  if (player.dropTimer > 0) { return false; }
  if (!movingDown) { return false; }
  return player.prevBottom <= row * C.TILE + 1;
}

function firstBlocking(player, movingDown) {
  const r = range(player);
  for (let row = r.r0; row <= r.r1; row++) {
    for (let col = r.c0; col <= r.c1; col++) {
      if (blocking(player, col, row, movingDown)) { return { col: col, row: row }; }
    }
  }
  return null;
}

export function touchingKind(player, key) {
  const r = range(player);
  for (let row = r.r0; row <= r.r1; row++) {
    for (let col = r.c0; col <= r.c1; col++) {
      if (Level.info(col, row)[key]) { return { col: col, row: row }; }
    }
  }
  return null;
}

/* `events` is filled in and returned, so the caller decides what a landing or a
   jump MEANS. This file reports; game.js decides. */
export function update(player, dt, events) {
  if (player.dropTimer > 0) { player.dropTimer -= dt; }
  if (player.invulnerable > 0) { player.invulnerable -= dt; }

  /* ---- 1. horizontal intent (lesson 3) ---- */
  let wantX = 0;
  if (Input.wantsLeft())  { wantX -= 1; player.facing = -1; }
  if (Input.wantsRight()) { wantX += 1; player.facing = 1; }
  player.vx += wantX * C.RUN_ACCEL * dt;
  if (wantX === 0) {
    const drag = player.onGround ? C.GROUND_DRAG : C.AIR_DRAG;
    player.vx *= Math.exp(-drag * dt);
  }
  if (Math.abs(player.vx) > C.RUN_SPEED) {
    player.vx = Math.sign(player.vx) * C.RUN_SPEED;
  }

  /* ---- 2. jump buffering: the press remembers itself ---- */
  if (Input.jumpPressed()) { player.buffer = C.JUMP_BUFFER; }
  else { player.buffer -= dt; }

  /* ---- 3. coyote time: the ground remembers itself ---- */
  if (player.onGround) { player.coyote = C.COYOTE_TIME; }
  else { player.coyote -= dt; }

  /* ---- 4. the jump fires when both windows overlap, in either order ---- */
  if (player.buffer > 0 && player.coyote > 0) {
    player.vy = -C.JUMP_SPEED;
    player.buffer = 0;
    player.coyote = 0;              /* BOTH, or it fires again next frame */
    events.jumped = true;
  }

  /* ---- 5. variable height: CUT the rise, do not stop it ---- */
  if (!Input.jumpHeld() && player.vy < 0) {
    player.vy *= Math.pow(C.RELEASE_CUT, dt * 60);
  }

  /* ---- 6. which gravity: apex hang, then fast fall ---- */
  let gravity = player.vy < 0 ? C.GRAVITY_UP : C.GRAVITY_DOWN;
  if (Math.abs(player.vy) < C.APEX_THRESHOLD) { gravity *= C.APEX_SCALE; }
  player.vy += gravity * dt;
  if (player.vy > C.MAX_FALL_SPEED) { player.vy = C.MAX_FALL_SPEED; }

  /* dropping through a one-way platform */
  if (Input.wantsDrop() && player.onGround) { player.dropTimer = 0.18; }

  player.prevBottom = player.y + player.h;

  /* ---- the two-step move (lesson 5). X first, then Y. ---- */
  player.x += player.vx * dt;
  const hitX = firstBlocking(player, false);
  if (hitX) {
    player.x = player.vx > 0 ? hitX.col * C.TILE - player.w : (hitX.col + 1) * C.TILE;
    player.vx = 0;
  }

  const wasFalling = player.vy;
  player.onGround = false;
  player.y += player.vy * dt;
  const hitY = firstBlocking(player, player.vy > 0);
  if (hitY) {
    if (player.vy > 0) {
      player.y = hitY.row * C.TILE - player.h;
      player.onGround = true;
      /* THIS is where "landed" comes from, and how hard. */
      if (wasFalling > 220) {
        events.landed = Math.min(1, wasFalling / 700);
        player.landImpact = events.landed;
      }
    } else {
      player.y = (hitY.row + 1) * C.TILE;
    }
    player.vy = 0;
  }

  /* presentation decay (lesson 9) */
  player.landImpact *= Math.exp(-9 * dt);

  /* fell out of the world */
  if (player.y > Level.WORLD_HEIGHT + 80) { events.fell = true; }

  return events;
}
