# ============================================================================
# 03 - THE GAME BOARD  (the finished lesson 2 result)
# Lesson 2, Games with Python, Beginner
#
# WHAT THIS SHOWS:  Converting GRID positions (column, row) into SCREEN
#                   positions (x, y) - the conversion every tile-based game
#                   needs - plus the board data that drives it.
#
# RUN IT:           python3 03-game-board.py
#
# CHANGE ME FIRST:  The BOARD list below. Type different characters and run it
#                   again. You are designing a level without touching any of
#                   the drawing code.
#
# BREAK IT:         Change "TOP - row * CELL" to "TOP + row * CELL" in
#                   cell_to_pixels() and run it. The board comes out upside
#                   down, because turtle's y grows UP while row numbers go DOWN.
# ============================================================================

import turtle

# ---- THE BOARD - this is DATA, not code ------------------------------------
# You can SEE the level by looking at it. That is the entire point.
#   .  empty      #  wall       @  player
#   *  treasure   o  enemy
BOARD = [
    "########",
    "#@.....#",
    "#.##.*.#",
    "#..#...#",
    "#.*..o.#",
    "########",
]

COLOURS = {
    "#": "#3d4654",     # wall
    ".": "#1d2129",     # floor
    "@": "#4a9eff",     # player
    "*": "#ffd43b",     # treasure
    "o": "#ff6b6b",     # enemy
}

CELL = 60
ROWS = len(BOARD)
COLUMNS = len(BOARD[0])

# ---- SETUP -----------------------------------------------------------------
screen = turtle.Screen()
screen.setup(width=COLUMNS * CELL + 120, height=ROWS * CELL + 160)
screen.bgcolor("#15181d")
screen.title("03 - Game board")
screen.tracer(0)                 # stop redrawing after every step

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# ---- GRID TO SCREEN --------------------------------------------------------
# Work out where the grid starts so the whole thing ends up centred.
# The grid is COLUMNS * CELL wide, so start half of that to the left of the
# middle - then add half a cell, because we want the CENTRE of the first cell.
LEFT = -(COLUMNS * CELL) / 2 + CELL / 2
TOP = (ROWS * CELL) / 2 - CELL / 2


def cell_to_pixels(column, row):
    """Turn a grid square into the screen position of its centre."""
    x = LEFT + column * CELL
    y = TOP - row * CELL
    #   ^ MINUS. Row numbers increase DOWNWARDS (row 0 is the top row), but
    #   turtle's y increases UPWARDS. So moving down a row means subtracting.
    #   That one character is the whole coordinate conversation.
    return x, y


def draw_sprite(x, y, size, colour, shape="square"):
    """Draw one sprite CENTRED at (x, y)."""
    t.penup()
    t.color(colour)

    if shape == "circle":
        t.goto(x, y - size / 2)      # circles are drawn upward from here
        t.pendown()
        t.begin_fill()
        t.circle(size / 2)
        t.end_fill()
    else:
        t.goto(x - size / 2, y - size / 2)
        t.setheading(0)              # reset the facing, or shapes come out crooked
        t.pendown()
        t.begin_fill()
        for _ in range(4):
            t.forward(size)
            t.left(90)
        t.end_fill()

    t.penup()


def draw_board():
    """Two nested loops turn the BOARD data into a picture.

    This pattern appears in every tile-based game ever made. Read it twice.
    """
    for row in range(ROWS):
        for column in range(COLUMNS):
            character = BOARD[row][column]
            #                 ^row    ^column
            # ROW first, then column - BOARD is a list of ROWS, so the first
            # index chooses which row. Swapping these gives a board mirrored
            # along the diagonal, or a crash if it is not square.

            x, y = cell_to_pixels(column, row)

            # Always draw the floor, so everything sits on a background.
            draw_sprite(x, y, CELL - 2, COLOURS["."])

            if character == "#":
                draw_sprite(x, y, CELL - 4, COLOURS["#"])
            elif character == "@":
                draw_sprite(x, y, CELL - 18, COLOURS["@"], "circle")
            elif character == "*":
                draw_sprite(x, y, CELL - 32, COLOURS["*"], "circle")
            elif character == "o":
                draw_sprite(x, y, CELL - 22, COLOURS["o"], "circle")


def draw_label():
    t.penup()
    t.goto(0, -(ROWS * CELL) / 2 - 46)
    t.color("#8b94a0")
    t.write(f"{COLUMNS} x {ROWS} board, {COLUMNS * ROWS} cells, drawn from "
            f"{ROWS} lines of text",
            align="center", font=("Arial", 13, "normal"))


# ---- DRAW IT ---------------------------------------------------------------
draw_board()
draw_label()

screen.update()        # show the finished picture, all at once.
                       # Comment this out and you get a BLANK WINDOW - every
                       # drawing command above ran perfectly, and the result
                       # was simply never displayed.

screen.exitonclick()   # keep the window open until clicked. Without a line
                       # like this the script ends and the window vanishes.
