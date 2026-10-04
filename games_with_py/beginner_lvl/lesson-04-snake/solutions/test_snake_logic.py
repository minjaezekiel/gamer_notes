"""Test Snake's game logic by driving the real module, with the window stubbed.

TEACHER-FACING. Run it with:   python3 test_snake_logic.py

WHY THIS CAN EXIST AT ALL
Because 02-snake.py keeps its LOGIC (move_snake, set_direction, place_food)
separate from its DRAWING (draw, draw_square). That separation is what makes
the game testable without a screen: we stub out the window, then call the game
functions directly and check the numbers.

A game whose logic is tangled into its drawing code cannot be tested this way.
That is one of the practical reasons the course keeps insisting on the
separation - it is not only tidiness.

This is also a preview of the advanced level, which covers testing properly.
It is here so a teacher can confirm the reference game is correct before
teaching from it.
"""
import importlib.util, pathlib, sys, turtle

for n in ("exitonclick", "mainloop", "done", "bye"):
    for cls in (turtle.Screen, turtle.TurtleScreen):
        if hasattr(cls, n): setattr(cls, n, lambda self, *a, **k: None)
turtle.TurtleScreen.ontimer = lambda self, f=None, t=0: None

path = str(pathlib.Path(__file__).resolve().parent.parent / "code" / "02-snake.py")
spec = importlib.util.spec_from_file_location("snake", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

fails = []
def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f"  (expected {want!r})"))
    if not ok: fails.append(label)

m.start_game()
check("starts PLAYING", m.state, "PLAYING")
check("starts length 3", len(m.snake), 3)
head0 = m.snake[0]

# --- normal move: length unchanged, head advances right ---
m.move_snake()
check("length after plain move", len(m.snake), 3)
check("head moved right", m.snake[0], (head0[0] + 1, head0[1]))

# --- eating: put food directly ahead, then move ---
h = m.snake[0]
m.food = (h[0] + 1, h[1])
before = len(m.snake)
m.move_snake()
check("grew by 1 after eating", len(m.snake), before + 1)
check("score is 10", m.score, 10)
check("food moved elsewhere", m.food != (h[0] + 1, h[1]), True)

# --- wall collision ---
m.start_game()
m.snake = [(m.COLUMNS - 1, 5)]
m.direction = m.RIGHT; m.next_direction = m.RIGHT
m.move_snake()
check("wall ends the game", m.state, "GAME_OVER")

# --- self collision: a 3x2 coil the head turns back into ---
m.start_game()
m.snake = [(5, 5), (6, 5), (6, 6), (5, 6), (4, 6)]
m.direction = m.LEFT; m.next_direction = m.LEFT
m.next_direction = m.DOWN          # turn down into our own body at (5,6)
m.move_snake()
check("self collision ends the game", m.state, "GAME_OVER")

# --- cannot reverse into yourself ---
m.start_game()
m.direction = m.RIGHT
m.set_direction(m.LEFT)
check("reversal rejected", m.next_direction, m.RIGHT)
m.set_direction(m.UP)
check("perpendicular turn accepted", m.next_direction, m.UP)

# --- food never lands on the snake ---
m.start_game()
m.snake = [(c, 5) for c in range(m.COLUMNS)]
clash = any(m.place_food() in m.snake for _ in range(400))
check("food never spawns on the snake", clash, False)

print()
print("ALL SNAKE LOGIC TESTS PASSED" if not fails else f"{len(fails)} FAILURES: {fails}")
sys.exit(1 if fails else 0)
