/* =============================================================================
   vec.js — a 2-D vector, written to be READ by a student.

   Two jobs:
     1. The visualizers in shared/visualizers/ use it.
     2. It is the reference version of the Vec2 that students write themselves in
        webgames/intermediate_lvl lesson 2. When they get there, they are asked
        to write this file from scratch and then compare. So it is deliberately
        plain: no cleverness, no chaining tricks, every method does one thing.

   WHAT IS A VECTOR, IN ONE SENTENCE?
   It is a pair of numbers that means "an arrow": how far across, and how far
   down. The SAME pair of numbers can mean a position (an arrow from the corner
   of the screen to a point) or a movement (an arrow from where you are to where
   you will be next). That double meaning is the whole idea, and it is what
   confuses people at first.
   ========================================================================== */

(function (global) {
  'use strict';

  function Vec(x, y) {
    this.x = x || 0;
    this.y = y || 0;
  }

  /* ---- making one ---- */
  Vec.of = function (x, y) { return new Vec(x, y); };

  /* An arrow of length 1 pointing at an angle. Useful for "fire a bullet
     this way". Angle is in DEGREES because degrees are friendlier than
     radians when you are 13. */
  Vec.fromAngle = function (degrees, length) {
    var r = degrees * Math.PI / 180;
    var len = length == null ? 1 : length;
    return new Vec(Math.cos(r) * len, Math.sin(r) * len);
  };

  Vec.prototype = {
    constructor: Vec,

    copy: function () { return new Vec(this.x, this.y); },

    /* ---- arithmetic. Each returns a NEW vector and leaves this one alone,
       which avoids the commonest vector bug: accidentally changing a position
       when you only meant to read it. ---- */
    add: function (v) { return new Vec(this.x + v.x, this.y + v.y); },
    sub: function (v) { return new Vec(this.x - v.x, this.y - v.y); },
    scale: function (k) { return new Vec(this.x * k, this.y * k); },

    /* ---- how long is this arrow? ----
       Straight from Pythagoras: the arrow is the hypotenuse of a right-angled
       triangle whose other two sides are x and y. */
    length: function () { return Math.sqrt(this.x * this.x + this.y * this.y); },

    /* Comparing lengths without the square root is faster, because square roots
       are slow. If you only want to know "which is closer", compare the squared
       lengths - the answer is the same. This trick matters in the advanced
       collision lessons. */
    lengthSquared: function () { return this.x * this.x + this.y * this.y; },

    /* ---- same direction, length exactly 1 ----
       Called NORMALISING. You do it when you care about which way, not how far:
       "move 5 pixels in the direction of the mouse" needs the direction on its
       own, then scaled by 5. */
    normalise: function () {
      var len = this.length();
      if (len === 0) { return new Vec(0, 0); }   // a zero arrow has no direction
      return new Vec(this.x / len, this.y / len);
    },

    /* Never longer than max. Stops a diagonal-moving player going 1.41x faster
       than one moving straight, which is a bug in a great many student games. */
    limit: function (max) {
      return this.length() > max ? this.normalise().scale(max) : this.copy();
    },

    /* Which way is this arrow pointing, in degrees. 0 is to the right, and the
       numbers increase CLOCKWISE, because on a screen y points down. */
    angle: function () { return Math.atan2(this.y, this.x) * 180 / Math.PI; },

    distanceTo: function (v) { return this.sub(v).length(); },

    /* Partway from this vector to another. t = 0 gives this one, t = 1 gives
       the other, t = 0.5 gives the midpoint. This single function is behind
       smooth camera follow, colour fades, and most easing. */
    lerp: function (v, t) {
      return new Vec(this.x + (v.x - this.x) * t, this.y + (v.y - this.y) * t);
    },

    /* Bounce off a flat surface. For a surface facing straight up, that is just
       "flip the y". The general version is what lesson 4 builds up to. */
    reflect: function (normal) {
      var n = normal.normalise();
      var d = this.x * n.x + this.y * n.y;        // the dot product
      return this.sub(n.scale(2 * d));
    },

    /* The dot product: a single number saying how much two arrows agree.
       Positive means roughly the same direction, zero means at right angles,
       negative means roughly opposite. */
    dot: function (v) { return this.x * v.x + this.y * v.y; },

    toString: function () {
      return '(' + this.x.toFixed(1) + ', ' + this.y.toFixed(1) + ')';
    }
  };

  global.Vec = Vec;
}(window));
