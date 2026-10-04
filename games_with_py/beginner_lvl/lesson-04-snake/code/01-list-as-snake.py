# ============================================================================
# 01 - A snake is a list  (no graphics at all)
# Lesson 4, Games with Python, Beginner
#
# WHAT THIS SHOWS:  The whole movement mechanic, printed as text so you can
#                   SEE the list changing. No window, no turtle - just lists.
#
# RUN IT:           python3 01-list-as-snake.py
# CHANGE ME FIRST:  the moves list on line 60. Try your own route.
#
# This file exists because the mechanic is easier to believe when you can read
# the list. Do this one before the graphical version.
# ============================================================================

RIGHT = (1, 0)
LEFT = (-1, 0)
DOWN = (0, 1)
UP = (0, -1)

NAMES = {RIGHT: "RIGHT", LEFT: "LEFT", DOWN: "DOWN", UP: "UP"}

# Each item is one square of the body. The FIRST item is the HEAD.
snake = [(5, 5), (4, 5), (3, 5)]
#         head    body    tail


def show(label):
    print(f"{label:<22} {snake}   length {len(snake)}")


def move(direction, eating=False):
    """Move the snake one square.

    The snake does NOT shuffle every segment along. It does two things:
      1. put a new head on the FRONT
      2. take the last segment off the BACK
    No other segment is touched.
    """
    head_column, head_row = snake[0]
    dc, dr = direction
    new_head = (head_column + dc, head_row + dr)

    snake.insert(0, new_head)        # grow at the front

    if eating:
        # TO GROW, JUST DO NOT REMOVE THE TAIL.
        # That single "if" is the entire growth mechanic of Snake. The thing
        # that feels most complicated turns out to be the thing you STOP doing.
        pass
    else:
        snake.pop()                  # normal move: drop the tail


print("A snake is a list of (column, row) positions.")
print("The first item is the head.\n")
show("start")

moves = [
    (RIGHT, False),
    (RIGHT, False),
    (RIGHT, True),      # <-- eats here
    (DOWN, False),
    (DOWN, True),       # <-- and here
    (LEFT, False),
]

for direction, eating in moves:
    move(direction, eating)
    label = NAMES[direction] + ("  (ate!)" if eating else "")
    show(label)

print("\nNotice: after eating, the list is one longer and nothing else changed.")
print("Notice: no segment was ever shuffled along. Only the ends moved.")
