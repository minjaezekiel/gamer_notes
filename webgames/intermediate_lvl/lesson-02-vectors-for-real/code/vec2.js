/* ===========================================================================
   vec2.js — two numbers that travel together.

   WHAT THIS IS
   The file you keep. Every remaining lesson in this level uses it, and the
   Python and C++ tracks use somebody else's version of exactly this.

   HOW TO USE IT
   It is a module, so:
       import { Vec2 } from "./vec2.js";
   and serve the folder (python3 -m http.server 8000), because modules cannot be
   imported from file:// — see lesson 1.

   The single-file examples in this folder paste this class in instead, so that
   they run by double-clicking. In your own project, import it.

   A DESIGN DECISION, STATED OUT LOUD
   Every method returns a NEW Vec2 instead of changing this one. That is called
   being IMMUTABLE. It makes more objects than a professional engine would
   tolerate, and it buys something worth having while you are learning: nothing
   can be modified behind your back, so a bug in one place cannot appear in
   another. Lesson 9 measures what it costs.
   ======================================================================== */
export class Vec2 {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  /* "and then also move by other" */
  add(other) { return new Vec2(this.x + other.x, this.y + other.y); }

  /* "from other, how do I get to this?"  -  THE useful one.
     Say it out loud when you use it: target minus me. */
  sub(other) { return new Vec2(this.x - other.x, this.y - other.y); }

  /* same direction, different amount */
  scale(k) { return new Vec2(this.x * k, this.y * k); }

  /* how long the arrow is. Pythagoras: sqrt(x^2 + y^2) */
  length() { return Math.hypot(this.x, this.y); }

  /* Comparing two distances does not need the square root, and the square root
     is the slow part. If a^2+b^2 is bigger then so is sqrt(a^2+b^2). */
  lengthSquared() { return this.x * this.x + this.y * this.y; }

  /* Same direction, length exactly 1: a UNIT VECTOR, i.e. a pure direction.

     The length === 0 check is not politeness. Without it this returns
     (NaN, NaN), NaN spreads to every number it touches, and the thing you were
     moving disappears for ever with no error message at all. */
  normalise() {
    const len = this.length();
    if (len === 0) { return new Vec2(0, 0); }
    return new Vec2(this.x / len, this.y / len);
  }

  distanceTo(other) { return this.sub(other).length(); }

  /* Cheap distance comparison: "is it within RANGE?" without a square root. */
  isWithin(other, range) {
    return this.sub(other).lengthSquared() <= range * range;
  }

  /* Multiply the x parts, multiply the y parts, add. For two UNIT vectors:
        1 = same way,  0 = at right angles,  -1 = opposite.
     Which makes "is the guard facing the player?" one line. */
  dot(other) { return this.x * other.x + this.y * other.y; }

  /* Which way does this arrow point? Note the argument order: Y FIRST.
     Getting it backwards is the commonest mistake in this whole lesson. */
  angle() { return Math.atan2(this.y, this.x); }

  /* Partway from this to other. t = 0 gives this, t = 1 gives other. */
  lerp(other, t) {
    return new Vec2(this.x + (other.x - this.x) * t,
                    this.y + (other.y - this.y) * t);
  }

  /* Angle -> direction. The partner of angle(). cos gives the x part, sin the y
     part, and for a unit vector that is all there is to it. */
  static fromAngle(radians) {
    return new Vec2(Math.cos(radians), Math.sin(radians));
  }

  static zero() { return new Vec2(0, 0); }

  /* Handy when printing one while debugging. */
  toString() { return "(" + this.x.toFixed(1) + ", " + this.y.toFixed(1) + ")"; }
}
