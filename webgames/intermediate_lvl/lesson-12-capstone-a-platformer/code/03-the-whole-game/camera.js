/* ===========================================================================
   camera.js — two numbers you subtract. From lesson 6, plus lesson 9's shake.

   Depends on: config, level.

   The shake is a separate OFFSET applied at draw time, never written into the
   camera's position - or the follow code and the shake fight each other and the
   view drifts permanently.
   ======================================================================== */
import * as C from "./config.js";
import { WORLD_WIDTH, WORLD_HEIGHT } from "./level.js";

export function create(viewWidth, viewHeight) {
  return {
    x: 0, y: 0,
    viewWidth: viewWidth,
    viewHeight: viewHeight,
    shake: 0,
    offsetX: 0, offsetY: 0
  };
}

export function addShake(camera, amount) {
  camera.shake = Math.min(C.SHAKE_MAX, camera.shake + amount);
}

export function update(camera, dt, targetX, targetY, targetVX) {
  /* look-ahead: aim at where they will be, a quarter of a second from now */
  const wantedX = targetX + targetVX * 0.22 - camera.viewWidth / 2;
  const wantedY = targetY - camera.viewHeight / 2;

  camera.x = applyAxis(camera.x, wantedX, C.CAMERA_DEAD_ZONE_X, dt);
  camera.y = applyAxis(camera.y, wantedY, C.CAMERA_DEAD_ZONE_Y, dt);

  /* clamp AFTER smoothing, or it judders at the edges. And handle the case where
     the world is narrower than the view, which would otherwise push it off. */
  camera.x = clampAxis(camera.x, WORLD_WIDTH, camera.viewWidth);
  camera.y = clampAxis(camera.y, WORLD_HEIGHT, camera.viewHeight);

  /* the shake, as an offset, decaying per second */
  camera.shake *= Math.exp(-C.SHAKE_DECAY * dt);
  if (camera.shake < 0.1) { camera.shake = 0; }
  camera.offsetX = (Math.random() * 2 - 1) * camera.shake;
  camera.offsetY = (Math.random() * 2 - 1) * camera.shake;
}

function applyAxis(current, wanted, deadZone, dt) {
  const gap = wanted - current;
  if (Math.abs(gap) <= deadZone / 2) { return current; }   /* inside: do nothing */
  const target = current + (gap > 0 ? gap - deadZone / 2 : gap + deadZone / 2);
  const t = 1 - Math.exp(-C.CAMERA_SMOOTH * dt);           /* frame-rate safe */
  return current + (target - current) * t;
}

function clampAxis(value, worldSize, viewSize) {
  if (worldSize <= viewSize) { return (worldSize - viewSize) / 2; }
  return Math.max(0, Math.min(worldSize - viewSize, value));
}

/* Rounded, so tiles do not show shimmering hairline seams. */
export function drawX(camera) { return Math.round(camera.x - camera.offsetX); }
export function drawY(camera) { return Math.round(camera.y - camera.offsetY); }
