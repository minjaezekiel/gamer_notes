/* ===========================================================================
   vec2.js — from lesson 2, unchanged.

   The platformer itself works in plain x and y, because a tile collision is
   naturally two separate axes. The particles use Vec2, which is a reasonable
   split: use it where "a direction" is a single idea, and do not use it where the
   two axes are deliberately handled apart.
   ======================================================================== */
export class Vec2 {
  constructor(x, y) { this.x = x; this.y = y; }
  add(o)   { return new Vec2(this.x + o.x, this.y + o.y); }
  sub(o)   { return new Vec2(this.x - o.x, this.y - o.y); }
  scale(k) { return new Vec2(this.x * k, this.y * k); }
  length() { return Math.hypot(this.x, this.y); }
  normalise() {
    const len = this.length();
    if (len === 0) { return new Vec2(0, 0); }      // the NaN guard
    return new Vec2(this.x / len, this.y / len);
  }
  static fromAngle(r) { return new Vec2(Math.cos(r), Math.sin(r)); }
}
