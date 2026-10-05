/* ===========================================================================
   game.js — as a module. The rules, and only the rules.

   Read the three import lines and you know everything this file can possibly
   touch. It cannot reach the canvas, because it never imported anything that
   has one.
   ======================================================================== */
import { LIVES_AT_START, POINTS_PER_BRICK } from "./config.js";
import * as Input from "./input.js";
import * as Entities from "./entities.js";

export function create(worldWidth, worldHeight) {
  const state = {
    worldWidth: worldWidth,
    worldHeight: worldHeight,
    paddle: Entities.makePaddle(worldWidth, worldHeight),
    ball: Entities.makeBall(),
    bricks: Entities.makeBricks(worldWidth),
    score: 0,
    lives: LIVES_AT_START,
    mode: "playing"
  };
  Entities.stickBallToPaddle(state.ball, state.paddle);
  return state;
}

export function update(state, dt) {
  if (Input.takeRestart()) {
    const fresh = create(state.worldWidth, state.worldHeight);
    Object.keys(fresh).forEach(function (key) { state[key] = fresh[key]; });
    return;
  }

  if (state.mode !== "playing") { return; }

  let direction = 0;
  if (Input.wantsLeft())  { direction -= 1; }
  if (Input.wantsRight()) { direction += 1; }
  Entities.movePaddle(state.paddle, direction, dt, state.worldWidth);

  if (state.ball.stuck) {
    state.ball.x = state.paddle.x + state.paddle.w / 2;
    state.ball.y = state.paddle.y - state.ball.r - 1;
    if (Input.wantsLaunch()) { Entities.launchBall(state.ball); }
    return;
  }

  const result = Entities.moveBall(state.ball, dt, state.worldWidth, state.worldHeight);
  if (result === "lost-ball") {
    state.lives = state.lives - 1;
    if (state.lives <= 0) {
      state.mode = "lost";
    } else {
      Entities.stickBallToPaddle(state.ball, state.paddle);
    }
    return;
  }

  Entities.bounceOffPaddle(state.ball, state.paddle);

  const brick = Entities.hitBrick(state.ball, state.bricks);
  if (brick) {
    brick.alive = false;
    state.score = state.score + POINTS_PER_BRICK;
    state.ball.speedY = -state.ball.speedY;
  }

  if (!Entities.anyBricksLeft(state.bricks)) { state.mode = "won"; }
}
