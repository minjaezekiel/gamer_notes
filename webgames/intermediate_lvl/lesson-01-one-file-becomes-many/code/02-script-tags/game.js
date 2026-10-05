/* ===========================================================================
   game.js — THE RULES. What happens, and in what order.

   Depends on: Config, Input, Entities.
   Does NOT depend on: render.js, main.js, or the canvas.

   This file is where the decisions live. entities.js knows HOW to move a ball;
   this file knows WHAT IT MEANS when that ball falls off the bottom. Keeping
   those two apart is the single most useful split in a game.

   Note the shape of create(): it takes a width and a height, not a canvas. The
   rules of Breakout need to know how big the world is. They do not need to know
   that the world happens to be drawn on an HTML element.
   ======================================================================== */
const Game = {

  create: function (worldWidth, worldHeight) {
    const state = {
      worldWidth: worldWidth,
      worldHeight: worldHeight,
      paddle: Entities.makePaddle(worldWidth, worldHeight),
      ball: Entities.makeBall(),
      bricks: Entities.makeBricks(worldWidth),
      score: 0,
      lives: Config.LIVES_AT_START,
      mode: "playing"              // "playing" | "won" | "lost"
    };
    Entities.stickBallToPaddle(state.ball, state.paddle);
    return state;
  },

  update: function (state, dt) {
    // Restart is allowed from any mode, so it is tested first.
    if (Input.takeRestart()) {
      const fresh = Game.create(state.worldWidth, state.worldHeight);
      // Copy the new state over the old one, so main.js keeps the same object.
      Object.keys(fresh).forEach(function (key) { state[key] = fresh[key]; });
      return;
    }

    if (state.mode !== "playing") { return; }

    /* ---- 1. input becomes intent, intent becomes a direction ---- */
    let direction = 0;
    if (Input.wantsLeft())  { direction -= 1; }
    if (Input.wantsRight()) { direction += 1; }
    Entities.movePaddle(state.paddle, direction, dt, state.worldWidth);

    /* ---- 2. a stuck ball rides the paddle until it is launched ---- */
    if (state.ball.stuck) {
      state.ball.x = state.paddle.x + state.paddle.w / 2;
      state.ball.y = state.paddle.y - state.ball.r - 1;
      if (Input.wantsLaunch()) { Entities.launchBall(state.ball); }
      return;
    }

    /* ---- 3. move the ball, and decide what the result MEANS ---- */
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

    /* ---- 4. collisions ---- */
    Entities.bounceOffPaddle(state.ball, state.paddle);

    const brick = Entities.hitBrick(state.ball, state.bricks);
    if (brick) {
      brick.alive = false;
      state.score = state.score + Config.POINTS_PER_BRICK;
      state.ball.speedY = -state.ball.speedY;
    }

    /* ---- 5. have we won? ---- */
    if (!Entities.anyBricksLeft(state.bricks)) { state.mode = "won"; }
  }
};
