/* ===========================================================================
   render.js — the ONLY file in this program that touches the canvas.

   Depends on: Config.

   Why that matters: if you ever want a second way of drawing this game — as
   text characters, scaled up for a projector, or on two canvases at once — you
   write a second version of this one file and change a single line in
   index.html. Nothing else in the game knows or cares how it is drawn.

   Notice that draw() is handed the whole state and returns nothing. It reads;
   it never changes anything. A render function that quietly moves the ball is
   the start of a very long debugging session.
   ======================================================================== */
const Render = {

  draw: function (ctx, state) {
    const w = ctx.canvas.width;
    const h = ctx.canvas.height;

    // Erase. Beginner lesson 1: a frame is "erase, then draw".
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
};
