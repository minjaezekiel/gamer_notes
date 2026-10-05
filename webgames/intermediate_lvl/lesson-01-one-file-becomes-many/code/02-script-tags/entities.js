/* ===========================================================================
   entities.js — what the things in the game ARE, and how they move.

   Depends on: Config.
   Depends on NOTHING ELSE — in particular, no canvas and no ctx. Every function
   here takes plain numbers and changes plain numbers.

   That restriction is not tidiness. It is what would let you run these rules
   10,000 times with no browser open, to check the ball can never escape.
   ======================================================================== */
const Entities = {

  makePaddle: function (worldWidth, worldHeight) {
    return { x: worldWidth / 2 - 46, y: worldHeight - 30, w: 92, h: 12 };
  },

  makeBall: function () {
    // speedX / speedY are zero while the ball is stuck to the paddle.
    return { x: 0, y: 0, r: 7, speedX: 0, speedY: 0, stuck: true };
  },

  makeBricks: function (worldWidth) {
    const bricks = [];
    const brickW = (worldWidth - Config.BRICK_GAP) / Config.BRICK_COLS - Config.BRICK_GAP;
    for (let row = 0; row < Config.BRICK_ROWS; row++) {
      for (let col = 0; col < Config.BRICK_COLS; col++) {
        bricks.push({
          x: Config.BRICK_GAP + col * (brickW + Config.BRICK_GAP) + Config.BRICK_GAP / 2,
          y: Config.BRICK_TOP + row * (Config.BRICK_H + Config.BRICK_GAP),
          w: brickW,
          h: Config.BRICK_H,
          alive: true,
          colour: Config.ROW_COLOURS[row % Config.ROW_COLOURS.length]
        });
      }
    }
    return bricks;
  },

  /* direction is -1, 0 or +1. The paddle has no idea a keyboard exists. */
  movePaddle: function (paddle, direction, dt, worldWidth) {
    paddle.x = paddle.x + direction * Config.PADDLE_SPEED * dt;
    if (paddle.x < 0) { paddle.x = 0; }
    if (paddle.x + paddle.w > worldWidth) { paddle.x = worldWidth - paddle.w; }
  },

  stickBallToPaddle: function (ball, paddle) {
    ball.stuck = true;
    ball.x = paddle.x + paddle.w / 2;
    ball.y = paddle.y - ball.r - 1;
    ball.speedX = 0;
    ball.speedY = 0;
  },

  launchBall: function (ball) {
    ball.stuck = false;
    ball.speedX = Config.BALL_SPEED * 0.45;
    ball.speedY = -Config.BALL_SPEED;
  },

  /* Returns "alive", or "lost-ball" when it fell off the bottom. Returning a
     word instead of setting a flag keeps the DECISION in game.js, where the
     rules live. */
  moveBall: function (ball, dt, worldWidth, worldHeight) {
    ball.x = ball.x + ball.speedX * dt;
    ball.y = ball.y + ball.speedY * dt;

    if (ball.x - ball.r < 0) {
      ball.x = ball.r;
      ball.speedX = -ball.speedX;
    }
    if (ball.x + ball.r > worldWidth) {
      ball.x = worldWidth - ball.r;
      ball.speedX = -ball.speedX;
    }
    if (ball.y - ball.r < 0) {
      ball.y = ball.r;
      ball.speedY = -ball.speedY;
    }
    if (ball.y - ball.r > worldHeight) { return "lost-ball"; }
    return "alive";
  },

  bounceOffPaddle: function (ball, paddle) {
    const touching = ball.y + ball.r > paddle.y &&
                     ball.y - ball.r < paddle.y + paddle.h &&
                     ball.x > paddle.x &&
                     ball.x < paddle.x + paddle.w;
    if (!touching || ball.speedY <= 0) { return false; }

    ball.y = paddle.y - ball.r;
    ball.speedY = -Math.abs(ball.speedY);
    // Where on the paddle it hit decides the new angle: -1 at the far left,
    // +1 at the far right. This one line is most of Breakout's feel.
    const hitOffset = (ball.x - (paddle.x + paddle.w / 2)) / (paddle.w / 2);
    ball.speedX = Config.BALL_SPEED * 0.75 * hitOffset;
    return true;
  },

  /* Returns the brick that was hit, or null. Again: it reports, it does not
     decide what a hit is worth. */
  hitBrick: function (ball, bricks) {
    for (let i = 0; i < bricks.length; i++) {
      const b = bricks[i];
      if (!b.alive) { continue; }
      if (ball.x + ball.r > b.x && ball.x - ball.r < b.x + b.w &&
          ball.y + ball.r > b.y && ball.y - ball.r < b.y + b.h) {
        return b;
      }
    }
    return null;
  },

  anyBricksLeft: function (bricks) {
    for (let i = 0; i < bricks.length; i++) {
      if (bricks[i].alive) { return true; }
    }
    return false;
  }
};
