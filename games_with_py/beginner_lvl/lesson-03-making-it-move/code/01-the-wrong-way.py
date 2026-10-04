# ============================================================================
# 01 - Moving inside the key handler  (THE WRONG WAY)
# Lesson 3, Games with Python, Beginner
#
# This file is DELIBERATELY WRONG. It is how nearly everybody tries first.
#
# RUN IT:     python3 01-the-wrong-way.py
#             Then HOLD the right arrow key down.
#
# WATCH FOR:  the circle moves once, pauses for about half a second, and then
#             jerks along in steps.
#
# That pause is your OPERATING SYSTEM's key-repeat setting - the same thing
# that makes "aaaa" appear when you hold a letter in a text box. It was
# designed for typing and it is wrong for a game.
#
# ALSO TRY:   hold Right and Up together. Only one of them does anything.
# ============================================================================

import turtle

screen = turtle.Screen()
screen.setup(width=700, height=560)
screen.bgcolor("#15181d")
screen.title("01 - The wrong way (hold a key and watch it stutter)")
screen.tracer(0)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

player_x = 0
player_y = 0


def draw():
    drawer.clear()
    drawer.penup()
    drawer.goto(player_x, player_y - 18)
    drawer.pendown()
    drawer.color("#ff6b6b")
    drawer.begin_fill()
    drawer.circle(18)
    drawer.end_fill()
    drawer.penup()
    drawer.goto(0, 230)
    drawer.color("#8b94a0")
    drawer.write("Hold an arrow key. Notice the pause, then the stutter.",
                 align="center", font=("Arial", 13, "normal"))
    screen.update()


# ---- THE MISTAKE -----------------------------------------------------------
# Moving the player right here, inside the handler.
#
# Four things are wrong with this:
#   1. It only moves as often as the OS repeats the key - hence the pause.
#   2. The game loop's timing is bypassed entirely.
#   3. You cannot hold two keys at once; only the latest one repeats.
#   4. Drawing happens from inside an input handler, mixing up the three jobs.
def go_right():
    global player_x
    player_x = player_x + 20
    draw()


def go_left():
    global player_x
    player_x = player_x - 20
    draw()


def go_up():
    global player_y
    player_y = player_y + 20
    draw()


def go_down():
    global player_y
    player_y = player_y - 20
    draw()


screen.onkey(go_right, "Right")
screen.onkey(go_left, "Left")
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.listen()        # WITHOUT this, no key is ever noticed at all

draw()
screen.mainloop()
