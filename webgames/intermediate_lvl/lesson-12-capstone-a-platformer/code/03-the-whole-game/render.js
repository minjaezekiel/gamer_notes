/* ===========================================================================
   render.js — the ONLY file in this program that touches the canvas.

   Depends on: config, level, camera, particles.

   Search the other files for "ctx" and you will not find it. That is what makes
   it possible to test the game's rules without a browser, and to change how the
   whole game looks by editing one file.

   The world is drawn INSIDE a translate, so it scrolls. The HUD is drawn OUTSIDE
   it, so it does not. That one distinction is lesson 6.
   ======================================================================== */
import * as C from "./config.js";
import * as Level from "./level.js";
import * as Camera from "./camera.js";
import * as Particles from "./particles.js";

export function drawWorld(ctx, world, camera) {
  const camX = Camera.drawX(camera);
  const camY = Camera.drawY(camera);

  ctx.fillStyle = "#0d1219";
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  /* parallax: one multiplication per layer (lesson 6) */
  drawBackdrop(ctx, camX, camY);

  ctx.save();
  ctx.translate(-camX, -camY);

  /* only the visible tiles: the four lines from lesson 5 */
  const firstCol = Math.max(0, Math.floor(camX / C.TILE));
  const lastCol = Math.min(Level.COLS - 1, Math.floor((camX + camera.viewWidth) / C.TILE) + 1);
  const firstRow = Math.max(0, Math.floor(camY / C.TILE));
  const lastRow = Math.min(Level.ROWS - 1, Math.floor((camY + camera.viewHeight) / C.TILE) + 1);

  for (let row = firstRow; row <= lastRow; row++) {
    for (let col = firstCol; col <= lastCol; col++) {
      drawTile(ctx, world, col, row);
    }
  }

  drawEnemies(ctx, world.enemies);
  drawPlayer(ctx, world.player);
  drawParticles(ctx);

  ctx.restore();
}

function drawBackdrop(ctx, camX, camY) {
  for (let i = 0; i < 26; i++) {
    const hx = (i * 190 - camX * 0.25) % (ctx.canvas.width + 400) - 200;
    const h = 60 + ((i * 53) % 110);
    ctx.fillStyle = "#141c26";
    ctx.beginPath();
    ctx.moveTo(hx - 90, ctx.canvas.height);
    ctx.lineTo(hx, ctx.canvas.height - h - camY * 0.08);
    ctx.lineTo(hx + 90, ctx.canvas.height);
    ctx.fill();
  }
}

function drawTile(ctx, world, col, row) {
  const ch = Level.charAt(col, row);
  const x = col * C.TILE, y = row * C.TILE;

  if (ch === "#") {
    ctx.fillStyle = "#3a4555";
    ctx.fillRect(x, y, C.TILE, C.TILE);
    ctx.fillStyle = Level.isSolid(col, row - 1) ? "#3a4555" : "#4d5c70";
    ctx.fillRect(x, y, C.TILE, 4);
  } else if (ch === "=") {
    ctx.fillStyle = "#b58900";
    ctx.fillRect(x, y, C.TILE, 6);
  } else if (ch === "^") {
    ctx.fillStyle = "#5e2222";
    ctx.fillRect(x, y, C.TILE, C.TILE);
    ctx.fillStyle = "#ff6b6b";
    for (let k = 0; k < 3; k++) {
      ctx.beginPath();
      ctx.moveTo(x + 2 + k * 9, y + C.TILE);
      ctx.lineTo(x + 6 + k * 9, y + C.TILE - 11);
      ctx.lineTo(x + 10 + k * 9, y + C.TILE);
      ctx.fill();
    }
  } else if (ch === "o") {
    if (world.takenCoins[col + "," + row]) { return; }
    const bob = Math.sin(world.time * 4 + col) * 2;
    ctx.fillStyle = "#ffd43b";
    ctx.beginPath();
    ctx.arc(x + C.TILE / 2, y + C.TILE / 2 + bob, 6, 0, Math.PI * 2);
    ctx.fill();
  } else if (ch === "F") {
    ctx.fillStyle = "#2b8a3e";
    ctx.fillRect(x + 6, y, 4, C.TILE);
    const wave = Math.sin(world.time * 5) * 2;
    ctx.fillStyle = "#51cf66";
    ctx.fillRect(x + 10, y + 2 + wave, 16, 11);
  }
}

function drawPlayer(ctx, p) {
  ctx.save();
  /* squash and stretch on landing (lesson 9) */
  const squash = p.landImpact * 0.4;
  ctx.translate(p.x + p.w / 2, p.y + p.h);
  ctx.scale(1 + squash, 1 - squash);
  if (p.invulnerable > 0 && Math.floor(p.invulnerable * 14) % 2 === 0) {
    ctx.globalAlpha = 0.4;
  }
  ctx.fillStyle = "#4dabf7";
  ctx.fillRect(-p.w / 2, -p.h, p.w, p.h);
  ctx.fillStyle = "#e7ecf3";
  ctx.fillRect(-p.w / 2 + (p.facing > 0 ? 11 : 4), -p.h + 6, 5, 5);
  ctx.restore();
}

function drawEnemies(ctx, enemies) {
  for (let i = 0; i < enemies.length; i++) {
    const e = enemies[i];
    if (!e.alive) { continue; }
    ctx.fillStyle = e.mode === "chase" ? "#ff6b6b" : "#c06a9a";
    ctx.fillRect(e.x, e.y, e.w, e.h);
    if (e.flash > 0.02) {
      ctx.globalAlpha = Math.min(1, e.flash);
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(e.x, e.y, e.w, e.h);
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = "#11151c";
    const eyeX = e.vx > 0 ? e.x + e.w - 9 : e.x + 4;
    ctx.fillRect(eyeX, e.y + 7, 5, 5);
  }
}

function drawParticles(ctx) {
  ctx.save();
  Particles.forEachAlive(function (p, t) {
    ctx.globalAlpha = t;
    ctx.fillStyle = p.colour;
    const s = p.size * t;
    ctx.fillRect(p.x - s / 2, p.y - s / 2, s, s);
  });
  ctx.restore();          /* resets globalAlpha, or the HUD fades too */
}

/* ---------------------------------------------------------------------------
   The HUD. Drawn OUTSIDE the camera transform, so it never scrolls.
   ------------------------------------------------------------------------ */
export function drawHud(ctx, world, best, storageOk) {
  ctx.fillStyle = "rgba(10,13,18,0.86)";
  ctx.fillRect(10, 10, 224, 72);
  ctx.strokeStyle = "#2b3240";
  ctx.lineWidth = 1;
  ctx.strokeRect(10, 10, 224, 72);

  ctx.font = "bold 16px system-ui, sans-serif";
  ctx.fillStyle = C.INK;
  ctx.fillText("SCORE " + world.score, 22, 32);

  ctx.font = "12px ui-monospace, Menlo, monospace";
  ctx.fillStyle = "#8793a4";
  ctx.fillText("coins " + world.coinsTaken + " / " + world.coinsTotal, 22, 52);
  ctx.fillText("best  " + best.score + (storageOk ? "" : "  (not saved)"), 22, 68);

  /* lives, as pips */
  for (let i = 0; i < world.lives; i++) {
    ctx.fillStyle = "#ff6b6b";
    ctx.fillRect(150 + i * 14, 24, 10, 10);
  }

  ctx.font = "12px ui-monospace, Menlo, monospace";
  ctx.fillStyle = "#4a5362";
  ctx.fillText("particles " + Particles.countAlive(), ctx.canvas.width - 130, 26);
}

export function drawCentred(ctx, lines) {
  ctx.textAlign = "center";
  let y = ctx.canvas.height / 2 - (lines.length - 1) * 18;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    ctx.font = (l.big ? "bold 34px " : (l.bold ? "bold 17px " : "15px ")) +
               "system-ui, sans-serif";
    ctx.fillStyle = l.colour || C.INK;
    ctx.fillText(l.text, ctx.canvas.width / 2, y);
    y += l.big ? 46 : 28;
  }
  ctx.textAlign = "left";
}

export function dimScreen(ctx, alpha) {
  ctx.fillStyle = "rgba(6, 9, 14, " + alpha + ")";
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}
