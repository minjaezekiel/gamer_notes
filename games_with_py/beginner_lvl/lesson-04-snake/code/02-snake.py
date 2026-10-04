# ============================================================================
# 02 - SNAKE  (the finished lesson 4 result)
# Lesson 4, Games with Python, Beginner
#
# Everything from lessons 1 to 4:
#   L1  state and a loop
#   L2  drawing with turtle, tracer/update
#   L3  a loop that never waits, polled input
#   L4  lists as game objects, grid movement, rules
#
# RUN IT:           python3 02-snake.py
# CONTROLS:         arrow keys or WASD. Space to start / restart. Escape quits.
#
# CHANGE ME FIRST:  MOVE_DELAY on line 40. It is seconds between steps.
#                   Try 0.3 (sleepy) and 0.04 (chaos).
#
# BREAK IT:         delete the "else: snake.pop()" and watch the snake grow
#                   forever. That one line is the whole growth mechanic.
# ============================================================================

import random
import time
import tkinter
import turtle

# ---- THE GRID --------------------------------------------------------------
# The game thinks entirely in SQUARES, never in pixels. Pixels appear only at
# the moment of drawing. That is why Snake has no collision bugs: two squares
# are either the same square or they are not. No overlap test, no rounding, no
# "close enough".
CELL = 22
COLUMNS = 25
ROWS = 20

WIDTH = COLUMNS * CELL
HEIGHT = ROWS * CELL

MOVE_DELAY = 0.12        # seconds between snake steps (NOT between frames)
START_LENGTH = 3

# Directions are PAIRS OF NUMBERS, so moving needs no "if" statements at all.
RIGHT = (1, 0)
LEFT = (-1, 0)
DOWN = (0, 1)            # rows increase downwards
UP = (0, -1)

# ---- SETUP -----------------------------------------------------------------
screen = turtle.Screen()
screen.setup(width=WIDTH + 80, height=HEIGHT + 120)
screen.bgcolor("#15181d")
screen.title("Snake")
screen.tracer(0)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.penup()

# ---- STATE -----------------------------------------------------------------
state = "MENU"           # MENU | PLAYING | GAME_OVER
snake = []
direction = RIGHT
next_direction = RIGHT
food = (0, 0)
score = 0
high_score = 0
move_timer = 0.0
last_time = time.time()
running = True


def grid_to_pixels(column, row):
    """Turn a grid square into the turtle position of its BOTTOM-LEFT corner.

    Turtle puts (0,0) in the middle with y growing UP, but our rows count
    DOWNWARDS from the top - hence the minus. This one function is the only
    place in the whole game that has to think about that.
    """
    x = -WIDTH / 2 + column * CELL
    y = HEIGHT / 2 - (row + 1) * CELL
    return x, y


def place_food():
    """Find an empty square for the food.

    Guess a square, and if the snake is on it, guess again. This is called
    REJECTION SAMPLING. It is simple and obviously correct, and on a mostly
    empty board it nearly always succeeds first try.

    Its weakness: if the snake filled almost the whole board, this could take
    a very long time. See the Think Like An Engineer section.
    """
    while True:
        spot = (random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1))
        if spot not in snake:
            return spot


def start_game():
    global snake, direction, next_direction, food, score, move_timer, state
    middle_row = ROWS // 2
    # Built head-first, so snake[0] is the head.
    snake = [(START_LENGTH - 1 - i, middle_row) for i in range(START_LENGTH)]
    direction = RIGHT
    next_direction = RIGHT
    score = 0
    move_timer = 0.0
    food = place_food()
    state = "PLAYING"


# ---- INPUT -----------------------------------------------------------------
def set_direction(new_direction):
    """Record a direction REQUEST. It is applied when the snake next moves.

    Why not just set `direction` here? Because key presses arrive at any
    moment, but the snake only moves on a tick. If we changed direction
    immediately, a player could press Up and then Left BETWEEN two moves - and
    the snake would reverse into itself through a direction it never actually
    travelled in.

    Decide at the moment of ACTING, not at the moment of ASKING.
    """
    global next_direction
    # Reject the exact opposite of the way we are currently going.
    if new_direction[0] == -direction[0] and new_direction[1] == -direction[1]:
        return
    next_direction = new_direction


def on_space():
    if state in ("MENU", "GAME_OVER"):
        start_game()


def on_escape():
    global running
    running = False
    screen.bye()


for key, vector in [("Up", UP), ("Down", DOWN), ("Left", LEFT), ("Right", RIGHT),
                    ("w", UP), ("s", DOWN), ("a", LEFT), ("d", RIGHT)]:
    # The default argument v=vector captures the value NOW. Without it, every
    # handler would share one variable and all eight keys would do the same
    # thing - the closure trap from lesson 3.
    screen.onkey(lambda v=vector: set_direction(v), key)

screen.onkey(on_space, "space")
screen.onkey(on_escape, "Escape")
screen.listen()          # WITHOUT this, no key is ever noticed


# ---- UPDATE ----------------------------------------------------------------
def move_snake():
    """One step of the snake. This is the entire game, in twenty lines."""
    global direction, food, score, state, high_score

    direction = next_direction          # apply the request NOW

    head_column, head_row = snake[0]
    dc, dr = direction
    new_head = (head_column + dc, head_row + dr)

    # ---- walls ----
    # Python lets you chain comparisons the way maths does:
    #   0 <= x < COLUMNS  means  0 <= x AND x < COLUMNS
    if not (0 <= new_head[0] < COLUMNS and 0 <= new_head[1] < ROWS):
        state = "GAME_OVER"
        high_score = max(high_score, score)
        return

    # ---- itself ----
    # Check BEFORE inserting, or the new head finds itself in the list and the
    # game ends immediately. Order matters here.
    if new_head in snake:
        state = "GAME_OVER"
        high_score = max(high_score, score)
        return

    snake.insert(0, new_head)           # grow at the front

    if new_head == food:
        score += 10
        food = place_food()
        # NO pop() here. Keeping the tail is what makes the snake grow.
    else:
        snake.pop()                     # normal move: drop the tail


def update(dt):
    global move_timer
    if state != "PLAYING":
        return

    # The LOOP runs about 60 times a second so input stays responsive and the
    # screen stays smooth. But the snake only STEPS a few times a second.
    # Render fast, simulate slowly.
    move_timer += dt
    if move_timer >= MOVE_DELAY:
        move_timer -= MOVE_DELAY
        # Subtracting rather than setting to 0 keeps any leftover time, so the
        # snake's speed stays exact even when a frame runs late.
        move_snake()


# ---- RENDER ----------------------------------------------------------------
def draw_square(column, row, colour, inset=1):
    x, y = grid_to_pixels(column, row)
    size = CELL - inset * 2
    drawer.goto(x + inset, y + inset)
    drawer.color(colour)
    drawer.setheading(0)
    drawer.pendown()
    drawer.begin_fill()
    for _ in range(4):
        drawer.forward(size)
        drawer.left(90)
    drawer.end_fill()
    drawer.penup()


def write_centred(text, y, size, colour):
    drawer.goto(0, y)
    drawer.color(colour)
    drawer.write(text, align="center", font=("Arial", size, "bold"))


def draw():
    drawer.clear()           # ERASE first - turtle does not clean itself

    # playing field
    drawer.goto(-WIDTH / 2 - 2, -HEIGHT / 2 - 2)
    drawer.color("#2a3039")
    drawer.setheading(0)
    drawer.pendown()
    for _ in range(2):
        drawer.forward(WIDTH + 4)
        drawer.left(90)
        drawer.forward(HEIGHT + 4)
        drawer.left(90)
    drawer.penup()

    if state == "MENU":
        write_centred("SNAKE", 30, 34, "#e8ebee")
        write_centred("press SPACE to play", -20, 15, "#8b94a0")
        write_centred("arrow keys or WASD", -50, 13, "#555c66")
    else:
        draw_square(food[0], food[1], "#ffd43b", inset=4)

        for index, (column, row) in enumerate(snake):
            # The head is a different colour, so the player can see which end
            # is which. Without that the game is genuinely hard to read.
            colour = "#51cf66" if index == 0 else "#2f9e44"
            draw_square(column, row, colour)

        drawer.goto(-WIDTH / 2, HEIGHT / 2 + 14)
        drawer.color("#8b94a0")
        drawer.write(f"score {score}    length {len(snake)}",
                     font=("Courier", 14, "normal"))
        drawer.goto(WIDTH / 2 - 110, HEIGHT / 2 + 14)
        drawer.write(f"best {high_score}", font=("Courier", 14, "normal"))

        if state == "GAME_OVER":
            write_centred("GAME OVER", 10, 30, "#ff6b6b")
            write_centred(f"score {score}  -  SPACE to play again", -28, 14, "#8b94a0")


# ---- THE LOOP --------------------------------------------------------------
def game_loop():
        # The window can be closed at ANY moment by the user, and the
        # teardown happens outside our control - so a frame that is already
        # queued will try to draw on a canvas that has gone.
        #
        # This is the one place in this course where exception handling IS the
        # right tool. We cannot PREVENT the window disappearing, so the only
        # option is to notice it has happened and stop quietly instead of
        # showing the player a wall of red text.
        #
        # Note how narrow it is: it catches the specific teardown errors, not
        # everything. A bare "except Exception" here would also swallow real
        # bugs in update() and draw(), which would be much worse than the crash
        # it was trying to hide.
    try:
        global last_time
        if not running:
            return

        now = time.time()
        dt = now - last_time
        last_time = now
        if dt > 0.1:          # clamp - a huge gap means the window was busy
            dt = 1 / 60

        update(dt)
        draw()
        screen.update()
        screen.ontimer(game_loop, 16)
    except (tkinter.TclError, turtle.Terminator):
        return      # the window has gone; stop quietly



game_loop()
screen.mainloop()
