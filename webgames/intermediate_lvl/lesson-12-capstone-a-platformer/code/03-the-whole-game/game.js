/* ===========================================================================
   game.js — THE RULES, and the ORDER things happen in.

   Depends on: config, level, player, enemies, particles, camera, sound.
   Does NOT depend on: render, scenes, main. No arrow points upwards.

   player.js knows HOW to move. This file knows WHAT IT MEANS when the player
   lands on a spike.
   ======================================================================== */
import * as C from "./config.js";
import * as Level from "./level.js";
import * as Player from "./player.js";
import * as Enemies from "./enemies.js";
import * as Particles from "./particles.js";
import * as Camera from "./camera.js";
import * as Sound from "./sound.js";

export function create(viewWidth, viewHeight) {
  const world = {
    player: Player.create(),
    enemies: Enemies.create(),
    camera: Camera.create(viewWidth, viewHeight),
    takenCoins: {},                 /* "col,row" -> true. The LEVEL is never edited. */
    coinsTotal: Level.findAll("o").length,
    coinsTaken: 0,
    score: 0,
    lives: C.START_LIVES,
    time: 0,
    hitstop: 0,
    outcome: ""                     /* "" | "won" | "lost" */
  };
  Particles.clear();
  return world;
}

function respawn(world) {
  Player.reset(world.player);
  world.player.invulnerable = 1.2;
}

export function update(world, realDt) {
  /* ---- HITSTOP: the simulation stops, presentation does not (lesson 9) ---- */
  let dt = realDt;
  if (world.hitstop > 0) {
    world.hitstop -= realDt;
    dt = 0;
  }
  world.time += realDt;

  if (world.outcome) {
    /* still let the particles and the camera settle after a win or a loss */
    Particles.update(realDt);
    Camera.update(world.camera, realDt,
                  world.player.x + world.player.w / 2,
                  world.player.y + world.player.h / 2, 0);
    return;
  }

  /* ---- 1. the player. It reports events; this file decides what they mean. ---- */
  const events = Player.update(world.player, dt, { jumped: false, landed: 0, fell: false });

  if (events.jumped) {
    Sound.jump();
    Particles.emit(world.player.x + world.player.w / 2, world.player.y + world.player.h,
                   5, { aim: Math.PI / 2, cone: 1.4, speed: 40, spread: 60,
                        life: 0.3, size: 3, colour: "#8793a4", gravity: 250 });
  }
  if (events.landed > 0) {
    Sound.land();
    Camera.addShake(world.camera, C.SHAKE_LAND * events.landed);
    Particles.emit(world.player.x + world.player.w / 2, world.player.y + world.player.h,
                   Math.round(4 + events.landed * 10),
                   { aim: Math.PI, cone: Math.PI * 1.2, speed: 60 * events.landed + 40,
                     spread: 90, life: 0.35, size: 3, colour: "#9aa7b8", gravity: 600 });
  }
  if (events.fell) {
    loseALife(world);
    return;
  }

  /* ---- 2. coins ---- */
  const coin = Player.touchingKind(world.player, "coin");
  if (coin) {
    const key = coin.col + "," + coin.row;
    if (!world.takenCoins[key]) {
      world.takenCoins[key] = true;
      world.coinsTaken += 1;
      world.score += C.COIN_SCORE;
      world.hitstop = C.HITSTOP_COIN;
      Camera.addShake(world.camera, C.SHAKE_COIN);
      Sound.coin(0);
      Particles.emit(coin.col * C.TILE + C.TILE / 2, coin.row * C.TILE + C.TILE / 2,
                     12, { speed: 90, spread: 120, life: 0.45, size: 3,
                           colour: "#ffd43b", gravity: 420 });
    }
  }

  /* ---- 3. spikes ---- */
  if (Player.touchingKind(world.player, "deadly") && world.player.invulnerable <= 0) {
    loseALife(world);
    return;
  }

  /* ---- 4. the flag ---- */
  if (Player.touchingKind(world.player, "flag")) {
    world.outcome = "won";
    world.score += world.lives * 50 + Math.max(0, 300 - Math.floor(world.time) * 2);
    Sound.win();
    Particles.emit(world.player.x + world.player.w / 2, world.player.y,
                   60, { speed: 160, spread: 200, life: 0.9, size: 4,
                         colour: "#51cf66", gravity: 300 });
    return;
  }

  /* ---- 5. enemies ---- */
  Enemies.update(world.enemies, dt,
                 world.player.x + world.player.w / 2,
                 world.player.y + world.player.h / 2);

  for (let i = 0; i < world.enemies.length; i++) {
    const e = world.enemies[i];
    if (!e.alive) { continue; }
    const p = world.player;
    const overlapping = p.x < e.x + e.w && p.x + p.w > e.x &&
                        p.y < e.y + e.h && p.y + p.h > e.y;
    if (!overlapping) { continue; }

    /* Landing on top of an enemy beats it. Anything else hurts. The test is the
       same "was above, moving down" idea as a one-way platform. */
    if (p.vy > 60 && p.prevBottom <= e.y + 8) {
      e.alive = false;
      e.flash = 1;
      p.vy = -C.JUMP_SPEED * 0.75;          /* a bounce */
      world.score += 25;
      world.hitstop = C.HITSTOP_HIT;
      Camera.addShake(world.camera, C.SHAKE_HIT * 0.6);
      Sound.hurt();
      Particles.emit(e.x + e.w / 2, e.y + e.h / 2, 24,
                     { speed: 140, spread: 160, life: 0.5, size: 4,
                       colour: "#c06a9a", gravity: 700 });
    } else if (p.invulnerable <= 0) {
      loseALife(world);
      return;
    }
  }

  /* ---- 6. presentation, always on REAL time ---- */
  Particles.update(realDt);
  Camera.update(world.camera, realDt,
                world.player.x + world.player.w / 2,
                world.player.y + world.player.h / 2,
                world.player.vx);
}

function loseALife(world) {
  world.lives -= 1;
  world.hitstop = C.HITSTOP_HIT;
  Camera.addShake(world.camera, C.SHAKE_HIT);
  Sound.hurt();
  Particles.emit(world.player.x + world.player.w / 2, world.player.y + world.player.h / 2,
                 26, { speed: 150, spread: 170, life: 0.55, size: 4,
                       colour: "#ff6b6b", gravity: 650 });
  if (world.lives <= 0) { world.outcome = "lost"; } else { respawn(world); }
}
