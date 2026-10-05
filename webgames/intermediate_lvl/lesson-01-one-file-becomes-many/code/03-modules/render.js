/* ===========================================================================
   render.js — as a module. Still the only file that touches the canvas.

   This one uses `import * as Config`, which brings in the whole module under one
   name. Both forms are fine; the named form documents what you use, and this
   form is shorter when you use most of it.
   ======================================================================== */
import * as Config from "./config.js";

export function draw(ctx, state) {
  const w = ctx.canvas.width;
  const h = ctx.canvas.height;

  ctx.clearRect(0, 0, w, h);

  for (let i = 0; i < state.bricks.length; i++) {
    const b = state.bricks[i];
    if (!b.alive) { continue; }
    ctx.fillStyle = b.colour;
    ctx.fillRect(b.x, b.y, b.w, b.h);
  }

  ctx.fillStyle = Config.INK;
  ctx.fillRect(state.paddle.x, state.paddle.y, state.paddle.w, state.paddle.h);

  ctx.beginPath();
  ctx.arc(state.ball.x, state.ball.y, state.ball.r, 0, Math.PI * 2);
  ctx.fill();

  ctx.font = "bold 16px system-ui, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("SCORE " + state.score, 10, 30);
  ctx.textAlign = "right";
  ctx.fillText("LIVES " + state.lives, w - 10, 30);

  ctx.textAlign = "center";
  if (state.mode !== "playing") {
    ctx.font = "bold 30px system-ui, sans-serif";
    ctx.fillText(state.mode === "won" ? "CLEARED" : "GAME OVER", w / 2, 200);
    ctx.font = "15px system-ui, sans-serif";
    ctx.fillText("press R", w / 2, 230);
  } else if (state.ball.stuck) {
    ctx.font = "15px system-ui, sans-serif";
    ctx.fillText("press SPACE to launch", w / 2, 250);
  }
  ctx.textAlign = "left";
}
