/* ===========================================================================
   enemies.js — decide, then act. From lesson 10.

   Depends on: config, level.
   Does NOT depend on: the player's type. It is handed a position.

   Two thresholds for one boundary: it notices you at ENEMY_SIGHT and gives up at
   ENEMY_SIGHT + ENEMY_GIVE_UP_GAP. One number for both would make it change its
   mind every frame at the edge.
   ======================================================================== */
import * as C from "./config.js";
import * as Level from "./level.js";

export function create() {
  return Level.findAll("E").map(function (spot) {
    return {
      x: spot.col * C.TILE + 3,
      y: spot.row * C.TILE + 2,
      w: 24, h: 28,
      vx: C.ENEMY_SPEED,
      mode: "patrol",
      flash: 0,
      alive: true
    };
  });
}

function solidAt(px, py) {
  return Level.isSolid(Math.floor(px / C.TILE), Math.floor(py / C.TILE));
}

/* Can it see the player? Distance, then a ray that walks the line in steps
   smaller than a tile. */
function canSee(e, px, py) {
  const dx = px - (e.x + e.w / 2);
  const dy = py - (e.y + e.h / 2);
  const distance = Math.hypot(dx, dy);
  if (distance > C.ENEMY_SIGHT + C.ENEMY_GIVE_UP_GAP) { return { seen: false, distance: distance }; }

  const step = C.TILE / 2;
  const steps = Math.floor(distance / step);
  for (let i = 1; i < steps; i++) {
    const t = (i * step) / distance;
    if (solidAt(e.x + e.w / 2 + dx * t, e.y + e.h / 2 + dy * t)) {
      return { seen: false, distance: distance };
    }
  }
  return { seen: true, distance: distance };
}

export function update(enemies, dt, playerX, playerY) {
  for (let i = 0; i < enemies.length; i++) {
    const e = enemies[i];
    if (!e.alive) { continue; }
    e.flash *= Math.exp(-10 * dt);

    const look = canSee(e, playerX, playerY);

    /* ---- DECIDE. Nothing here moves anything. ---- */
    if (e.mode === "patrol" && look.seen && look.distance < C.ENEMY_SIGHT) {
      e.mode = "chase";
    } else if (e.mode === "chase" &&
               (!look.seen || look.distance > C.ENEMY_SIGHT + C.ENEMY_GIVE_UP_GAP)) {
      e.mode = "patrol";
    }

    /* ---- ACT. One branch per state. ---- */
    const speed = e.mode === "chase" ? C.ENEMY_CHASE_SPEED : C.ENEMY_SPEED;
    if (e.mode === "chase") {
      e.vx = Math.sign(playerX - (e.x + e.w / 2)) * speed;
    } else {
      e.vx = Math.sign(e.vx || 1) * speed;
    }

    e.x += e.vx * dt;

    /* turn round at a wall, or at a ledge - the ledge test is what stops a
       patrolling enemy walking off every platform in the level */
    const ahead = e.vx > 0 ? e.x + e.w + 2 : e.x - 2;
    const wall = solidAt(ahead, e.y + e.h / 2);
    const floorAhead = solidAt(ahead, e.y + e.h + 4);
    if (wall || (!floorAhead && e.mode === "patrol")) {
      e.x -= e.vx * dt;
      e.vx = -e.vx;
    }

    /* a simple fall, so an enemy that is nudged off something lands */
    e.y += 260 * dt;
    if (solidAt(e.x + e.w / 2, e.y + e.h)) {
      e.y = Math.floor((e.y + e.h) / C.TILE) * C.TILE - e.h;
    }
  }
}
