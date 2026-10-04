"""Test Brick Breaker's game logic by driving the real module.

TEACHER-FACING. Run it with:   python3 test_brick_breaker_logic.py

As with the Snake test in lesson 4, this is only possible because the game
keeps its LOGIC (build_level, boxes_overlap, Ball.bounce_off_brick, Brick.hit)
separate from its DRAWING. A game whose logic is tangled into its rendering
cannot be checked without a screen.
"""
import importlib.util
import pathlib
import sys
import tkinter

# Stub the blocking calls so the module can be imported and poked at.
tkinter.Misc.mainloop = lambda self, *a, **k: None
tkinter.Tk.mainloop = lambda self, *a, **k: None
tkinter.Misc.after = lambda self, ms, func=None, *a: "stub"

path = str(pathlib.Path(__file__).resolve().parent.parent / "code" / "02-brick-breaker.py")
spec = importlib.util.spec_from_file_location("bb", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

fails = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}"
          + ("" if ok else f"   (expected {want!r})"))
    if not ok:
        fails.append(label)


# ---- build_level reads [row][column] and skips zeros ----------------------
layout = [
    [1, 0, 2],
    [0, 1, 0],
]
built = m.build_level(layout)
# Three non-zero cells: (0,0)=1, (0,2)=2, (1,1)=1.
check("build_level skips zeros", len(built), 3)
# Row 0 col 0 must be top-left: smallest x AND smallest y.
xs = sorted({b.x for b in built})
ys = sorted({b.y for b in built})
first = [b for b in built if b.x == xs[0] and b.y == ys[0]]
check("row 0 col 0 is top-left", len(first), 1)
check("tough brick kept its hits", sorted(b.hits for b in built), [1, 1, 2])
# A brick one column right is further right; one row down is further down.
check("columns increase x", xs[1] > xs[0], True)
check("rows increase y (downwards)", ys[1] > ys[0], True)
for b in built:
    b.destroy()

# ---- the AABB test --------------------------------------------------------
check("overlapping boxes detected", m.boxes_overlap((0, 0, 10, 10), (5, 5, 10, 10)), True)
check("separated on x", m.boxes_overlap((0, 0, 10, 10), (20, 5, 10, 10)), False)
check("separated on y", m.boxes_overlap((0, 0, 10, 10), (5, 20, 10, 10)), False)
check("touching edges do not overlap", m.boxes_overlap((0, 0, 10, 10), (10, 0, 10, 10)), False)

# ---- brick.hit: tough bricks take two, and score differs ------------------
tough = m.Brick(0, 0, 60, 20, 2)
check("tough brick survives one hit", (tough.hit(), tough.alive), (25, True))
check("tough brick dies on the second", (tough.hit(), tough.alive), (100, False))
normal = m.Brick(0, 0, 60, 20, 1)
check("normal brick dies in one", (normal.hit(), normal.alive), (100, False))

# ---- which side was hit ---------------------------------------------------
brick = m.Brick(100, 100, 60, 20, 1)
ball = m.Ball()

# Coming in from ABOVE: barely overlapping vertically, lots horizontally.
ball.x, ball.y = 130, 100          # centre over the brick, at its top edge
ball.speed_x, ball.speed_y = 0, 300
ball.bounce_off_brick(brick)
check("hit from above flips speed_y", (ball.speed_x, ball.speed_y), (0, -300))

# Coming in from the SIDE: barely overlapping horizontally, lots vertically.
ball.x, ball.y = 100, 110          # at the left edge, mid-height
ball.speed_x, ball.speed_y = 300, 0
ball.bounce_off_brick(brick)
check("hit from the side flips speed_x", (ball.speed_x, ball.speed_y), (-300, 0))
brick.destroy()

# ---- paddle steering: edges send the ball sideways, centre does not -------
paddle = m.Paddle()
paddle.x, paddle.y = 100, 400
b2 = m.Ball()
b2.stuck = False
b2.speed_y = 300
b2.x = paddle.x + paddle.w / 2      # dead centre
b2.bounce_off_paddle(paddle)
check("centre hit goes straight up", (round(b2.speed_x), b2.speed_y < 0), (0, True))
b2.speed_y = 300
b2.x = paddle.x + paddle.w          # far right edge
b2.bounce_off_paddle(paddle)
check("right-edge hit steers right", b2.speed_x > 0, True)

# ---- saving survives nonsense in the file ---------------------------------
m.SAVE_FILE.write_text("this is not json at all")
check("damaged save file does not crash", m.load_high_score(), 0)
m.save_high_score(1234)
check("score round-trips through the file", m.load_high_score(), 1234)
m.SAVE_FILE.unlink(missing_ok=True)
check("missing save file returns 0", m.load_high_score(), 0)

print()
print("ALL BRICK BREAKER LOGIC TESTS PASSED" if not fails
      else f"{len(fails)} FAILURES: {fails}")
sys.exit(1 if fails else 0)
