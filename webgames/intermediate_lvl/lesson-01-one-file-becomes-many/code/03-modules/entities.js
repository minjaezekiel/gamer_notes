/* ===========================================================================
   entities.js — as a module.

   The import list at the top is a readable, checkable statement of exactly what
   this file depends on. Compare it with the script-tag version, where you had to
   read the whole file to find out.

   Still no canvas anywhere in here.
   ======================================================================== */
import {
  PADDLE_SPEED, BALL_SPEED,
  BRICK_ROWS, BRICK_COLS, BRICK_H, BRICK_GAP, BRICK_TOP, ROW_COLOURS
} from "./config.js";
/* The "./" is required: a bare "config.js" is reserved for package names, which
   this course does not use. The ".js" is required too — browsers do not guess. */

export function makePaddle(worldWidth, worldHeight) {
  return { x: worldWidth / 2 - 46, y: worldHeight - 30, w: 92, h: 12 };
}

export function makeBall() {
  return { x: 0, y: 0, r: 7, speedX: 0, speedY: 0, stuck: true };
}

export function makeBricks(worldWidth) {
  const bricks = [];
  const brickW = (worldWidth - BRICK_GAP) / BRICK_COLS - BRICK_GAP;
  for (let row = 0; row < BRICK_ROWS; row++) {
    for (let col = 0; col < BRICK_COLS; col++) {
      bricks.push({
        x: BRICK_GAP + col * (brickW + BRICK_GAP) + BRICK_GAP / 2,
        y: BRICK_TOP + row * (BRICK_H + BRICK_GAP),
        w: brickW,
        h: BRICK_H,
        alive: true,
        colour: ROW_COLOURS[row % ROW_COLOURS.length]
      });
    }
  }
  return bricks;
}

export function movePaddle(paddle, direction, dt, worldWidth) {
  paddle.x = paddle.x + direction * PADDLE_SPEED * dt;
  if (paddle.x < 0) { paddle.x = 0; }
  if (paddle.x + paddle.w > worldWidth) { paddle.x = worldWidth - paddle.w; }
}

export function stickBallToPaddle(ball, paddle) {
  ball.stuck = true;
  ball.x = paddle.x + paddle.w / 2;
  ball.y = paddle.y - ball.r - 1;
  ball.speedX = 0;
  ball.speedY = 0;
}

export function launchBall(ball) {
  ball.stuck = false;
  ball.speedX = BALL_SPEED * 0.45;
  ball.speedY = -BALL_SPEED;
}

export function moveBall(ball, dt, worldWidth, worldHeight) {
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
}

export function bounceOffPaddle(ball, paddle) {
  const touching = ball.y + ball.r > paddle.y &&
                   ball.y - ball.r < paddle.y + paddle.h &&
                   ball.x > paddle.x &&
                   ball.x < paddle.x + paddle.w;
  if (!touching || ball.speedY <= 0) { return false; }

  ball.y = paddle.y - ball.r;
  ball.speedY = -Math.abs(ball.speedY);
  const hitOffset = (ball.x - (paddle.x + paddle.w / 2)) / (paddle.w / 2);
  ball.speedX = BALL_SPEED * 0.75 * hitOffset;
  return true;
}

export function hitBrick(ball, bricks) {
  for (let i = 0; i < bricks.length; i++) {
    const b = bricks[i];
    if (!b.alive) { continue; }
    if (ball.x + ball.r > b.x && ball.x - ball.r < b.x + b.w &&
        ball.y + ball.r > b.y && ball.y - ball.r < b.y + b.h) {
      return b;
    }
  }
  return null;
}

export function anyBricksLeft(bricks) {
  for (let i = 0; i < bricks.length; i++) {
    if (bricks[i].alive) { return true; }
  }
  return false;
}
