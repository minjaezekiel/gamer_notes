/* ===========================================================================
   particles.js — a POOL, from lesson 9.

   Depends on: config, vec2.

   Built once, reused for ever. The array never changes length, nothing is ever
   allocated during play, and a full pool DROPS the request - which puts a hard
   ceiling on the work per frame, so a hundred explosions cannot slow the game.
   ======================================================================== */
import { MAX_PARTICLES } from "./config.js";
import { Vec2 } from "./vec2.js";

const pool = [];
let nextFree = 0;

for (let i = 0; i < MAX_PARTICLES; i++) {
  pool.push({ x: 0, y: 0, vx: 0, vy: 0, life: 0, maxLife: 1,
              size: 0, colour: "#ffffff", gravity: 0, alive: false });
}

export function clear() {
  for (let i = 0; i < pool.length; i++) { pool[i].alive = false; }
  nextFree = 0;
}

function take() {
  for (let step = 0; step < pool.length; step++) {
    const i = (nextFree + step) % pool.length;
    if (!pool[i].alive) {
      nextFree = (i + 1) % pool.length;
      return pool[i];
    }
  }
  return null;         // full: drop it, on purpose
}

/* One emitter. Different effects are different NUMBERS, not different code. */
export function emit(x, y, count, options) {
  const o = options || {};
  const speed = o.speed === undefined ? 150 : o.speed;
  const spread = o.spread === undefined ? 120 : o.spread;
  const aim = o.aim === undefined ? -Math.PI / 2 : o.aim;
  const cone = o.cone === undefined ? Math.PI * 2 : o.cone;
  const life = o.life === undefined ? 0.5 : o.life;
  const size = o.size === undefined ? 3 : o.size;
  const gravity = o.gravity === undefined ? 700 : o.gravity;
  const colour = o.colour || "#ffd43b";

  for (let i = 0; i < count; i++) {
    const p = take();
    if (!p) { return; }
    /* a random ANGLE, not random vx and vy - which would cluster on the diagonals */
    const angle = aim + (Math.random() - 0.5) * cone;
    const dir = Vec2.fromAngle(angle).scale(speed + Math.random() * spread);
    p.x = x; p.y = y;
    p.vx = dir.x; p.vy = dir.y;
    p.maxLife = life * (0.7 + Math.random() * 0.6);
    p.life = p.maxLife;
    p.size = size * (0.7 + Math.random() * 0.7);
    p.colour = colour;
    p.gravity = gravity;
    p.alive = true;
  }
}

export function update(dt) {
  for (let i = 0; i < pool.length; i++) {
    const p = pool[i];
    if (!p.alive) { continue; }
    p.vy += p.gravity * dt;
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.life -= dt;
    if (p.life <= 0) { p.alive = false; }     /* a flag, not a splice */
  }
}

export function forEachAlive(fn) {
  for (let i = 0; i < pool.length; i++) {
    if (pool[i].alive) { fn(pool[i], pool[i].life / pool[i].maxLife); }
  }
}

export function countAlive() {
  let n = 0;
  for (let i = 0; i < pool.length; i++) { if (pool[i].alive) { n += 1; } }
  return n;
}
