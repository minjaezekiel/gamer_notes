# ============================================================================
# 02 - One function, many sprites
# Lesson 2, Games with Python, Beginner
#
# WHAT THIS SHOWS:  Writing draw_sprite() ONCE and then using it forty times.
#                   Also tracer(0) and update(), which make turtle fast enough
#                   to be a game.
#
# RUN IT:           python3 02-reusable-sprite.py
#
# CHANGE ME FIRST:  comment out screen.tracer(0) on line 26 and run it again.
#                   Watch how long it takes. That is why the line exists.
#
# THEN TRY:         keep tracer(0) but comment out screen.update() at the
#                   bottom. You get a BLANK WINDOW - every drawing command ran
#                   perfectly, and the result was simply never shown.
# ============================================================================

import random
import turtle

# ---- SETUP (boilerplate - copy this into every turtle program) -------------
screen = turtle.Screen()
screen.setup(width=800, height=620)
screen.bgcolor("#15181d")
screen.title("02 - Reusable sprites")
screen.tracer(0)        # stop redrawing the screen after every single step

t = turtle.Turtle()
t.hideturtle()          # hide the arrow; we are drawing a game
t.speed(0)


def draw_sprite(x, y, size, colour, shape="square"):
    """Draw one sprite CENTRED at (x, y).

    Centred rather than corner-based, because in a game you nearly always
    think about where the middle of something is. Doing that conversion once,
    here, means never thinking about it again anywhere else.
    """
    t.penup()
    t.color(colour)

    if shape == "circle":
        # turtle draws circles upward from where it is standing, so start at
        # the bottom of where we want the circle to be.
        t.goto(x, y - size / 2)
        t.pendown()
        t.begin_fill()
        t.circle(size / 2)
        t.end_fill()
    else:
        t.goto(x - size / 2, y - size / 2)   # bottom-left corner
        # The turtle REMEMBERS which way it is facing between calls. Without
        # this reset, a function that turns will quietly draw crooked shapes
        # later on. Making a function reset what it depends on prevents a whole
        # family of mysterious bugs.
        t.setheading(0)
        t.pendown()
        t.begin_fill()
        for _ in range(4):
            t.forward(size)
            t.left(90)
        t.end_fill()

    t.penup()


# ---- Written once, used forty times ---------------------------------------
COLOURS = ["#4a9eff", "#ff9246", "#51cf66", "#ffd43b", "#ff6b6b"]

for i in range(40):
    x = random.randint(-350, 350)
    y = random.randint(-260, 260)
    size = random.randint(20, 60)
    colour = random.choice(COLOURS)
    shape = random.choice(["square", "circle"])
    draw_sprite(x, y, size, colour, shape)

# And because it is one function, changing how a sprite looks changes all
# forty at once. THAT is what a function is for: not to save typing, but to
# give you one place to change your mind.

t.goto(-380, 280)
t.color("white")
t.write("40 sprites, one function", font=("Arial", 14, "normal"))

screen.update()         # NOW show the finished picture, all in one go.
                        # This is DOUBLE BUFFERING, and every graphics system
                        # in the world does it.
screen.exitonclick()
