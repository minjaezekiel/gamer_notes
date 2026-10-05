/* ===========================================================================
   scenes.js — a scene stack, from lesson 7.

       update the TOP scene      -> the game below is frozen
       draw ALL the scenes       -> the game below is still visible

   Those two lines are the whole pause feature. Nothing freezes anything.

   Depends on: input, store, game, render, level, config.
   ======================================================================== */
import * as Input from "./input.js";
import * as Store from "./store.js";
import * as Game from "./game.js";
import * as Render from "./render.js";
import * as Level from "./level.js";

const stack = [];
let best = { score: 0, coins: 0 };
let world = null;
let pending = null;              /* a deferred scene change */
let levelProblem = null;

export function init(viewWidth, viewHeight) {
  Store.init();
  best = Store.loadBest();
  levelProblem = Level.check();
  go(titleScene(viewWidth, viewHeight));
}

export function current() { return stack[stack.length - 1]; }

/* Scene changes are RECORDED and applied after update and draw have both
   finished, so nothing is ever walking through a stack that is being rebuilt. */
export function go(scene) { pending = { kind: "go", scene: scene }; }
export function push(scene) { pending = { kind: "push", scene: scene }; }
export function pop() { pending = { kind: "pop" }; }

export function applyPending() {
  if (!pending) { return; }
  const p = pending;
  pending = null;
  if (p.kind === "go") {
    while (stack.length) { const s = stack.pop(); if (s.exit) { s.exit(); } }
    stack.push(p.scene);
    if (p.scene.enter) { p.scene.enter(); }
  } else if (p.kind === "push") {
    stack.push(p.scene);
    if (p.scene.enter) { p.scene.enter(); }
  } else if (p.kind === "pop") {
    if (stack.length > 1) { const s = stack.pop(); if (s.exit) { s.exit(); } }
  }
}

export function update(dt) {
  if (stack.length) { current().update(dt); }
}

export function draw(ctx) {
  for (let i = 0; i < stack.length; i++) { stack[i].draw(ctx); }
}

/* =========================================================================
   TITLE
   ====================================================================== */
function titleScene(viewWidth, viewHeight) {
  return {
    name: "title",
    enter: function () { this.blink = 0; },
    update: function (dt) {
      this.blink += dt;
      if (Input.confirmPressed()) { go(playScene(viewWidth, viewHeight)); }
    },
    draw: function (ctx) {
      ctx.fillStyle = "#0d1219";
      ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      const lines = [
        { text: "CAPSTONE", big: true },
        { text: "arrows to run   ·   space to jump (hold for higher)", colour: "#a9b4c4" },
        { text: "down drops through a thin platform   ·   P pauses", colour: "#a9b4c4" },
        { text: best.score > 0 ? "best score " + best.score : " ", colour: "#ffd43b" }
      ];
      if (this.blink % 1 < 0.6) {
        lines.push({ text: "press SPACE", bold: true, colour: "#4dabf7" });
      } else {
        lines.push({ text: " " });
      }
      Render.drawCentred(ctx, lines);

      if (levelProblem) {
        ctx.font = "13px ui-monospace, Menlo, monospace";
        ctx.fillStyle = "#ff6b6b";
        ctx.fillText("LEVEL PROBLEM: " + levelProblem, 20, ctx.canvas.height - 18);
      } else if (!Store.isAvailable()) {
        ctx.font = "12px system-ui, sans-serif";
        ctx.fillStyle = "#f08c00";
        ctx.fillText("storage is unavailable, so the best score will not be kept — " +
                     "the game is otherwise unaffected", 20, ctx.canvas.height - 18);
      }
    }
  };
}

/* =========================================================================
   PLAY — all of its state is built in enter(), so a second game is identical
   to the first.
   ====================================================================== */
function playScene(viewWidth, viewHeight) {
  return {
    name: "play",
    enter: function () {
      world = Game.create(viewWidth, viewHeight);
    },
    update: function (dt) {
      if (Input.pausePressed()) { push(pauseScene()); return; }

      Game.update(world, dt);

      if (world.outcome === "won" || world.outcome === "lost") {
        if (world.score > best.score) {
          best = { score: world.score, coins: world.coinsTaken };
          Store.saveBest(best);          /* saving on an EVENT, not every frame */
        }
        push(overScene(world.outcome));
      }
    },
    draw: function (ctx) {
      Render.drawWorld(ctx, world, world.camera);
      Render.drawHud(ctx, world, best, Store.isAvailable());
    }
  };
}

/* =========================================================================
   PAUSE — six lines of substance, and it knows nothing about the game
   ====================================================================== */
function pauseScene() {
  return {
    name: "pause",
    update: function () {
      if (Input.pausePressed()) { pop(); }
    },
    draw: function (ctx) {
      Render.dimScreen(ctx, 0.62);
      Render.drawCentred(ctx, [
        { text: "PAUSED", big: true, colour: "#ffd43b" },
        { text: "P to continue", colour: "#a9b4c4" }
      ]);
    }
  };
}

/* =========================================================================
   GAME OVER / WON — ignores input for half a second, on purpose, because the
   player arrived here by pressing something.
   ====================================================================== */
function overScene(outcome) {
  return {
    name: "over",
    enter: function () { this.t = 0; },
    update: function (dt) {
      this.t += dt;
      if (this.t > 0.5 && Input.confirmPressed()) {
        go(titleScene(world.camera.viewWidth, world.camera.viewHeight));
      }
    },
    draw: function (ctx) {
      Render.dimScreen(ctx, 0.66);
      const won = outcome === "won";
      const lines = [
        { text: won ? "YOU MADE IT" : "OUT OF LIVES", big: true,
          colour: won ? "#51cf66" : "#ff6b6b" },
        { text: "score " + world.score + "   coins " + world.coinsTaken +
                " / " + world.coinsTotal, bold: true },
        { text: "best " + best.score, colour: "#ffd43b" }
      ];
      if (this.t > 0.5) {
        lines.push({ text: "press SPACE", colour: "#a9b4c4" });
      } else {
        lines.push({ text: "(input locked for half a second)", colour: "#4a5362" });
      }
      Render.drawCentred(ctx, lines);
    }
  };
}

export function stackNames() {
  return stack.map(function (s) { return s.name; });
}

/* Exposed for selftest.html, which plays the game headlessly and then checks that
   the player's numbers are finite and in bounds. A small, deliberate door is
   better than a test that cannot see anything. */
export function currentWorld() { return world; }
