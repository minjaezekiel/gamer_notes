# ============================================================================
# 01 - Your first turtle drawing
# Lesson 2, Games with Python, Beginner
#
# WHAT THIS SHOWS:  The turtle model - forward, turn, and a pen that can be
#                   lifted. And what "slow" looks like before we fix it.
#
# RUN IT:           python3 01-first-drawing.py
#                   (Run from a terminal. Some editors swallow the window.)
#
# CHANGE ME FIRST:  t.speed(3) on line 24. Try speed(0) for as fast as
#                   possible, and speed(1) for painfully slow.
# TRY THIS:         change left(90) to left(89) and run it again. One degree.
# ============================================================================

import turtle

screen = turtle.Screen()
screen.setup(width=700, height=600)
screen.bgcolor("midnightblue")
screen.title("01 - First drawing")

t = turtle.Turtle()
t.speed(3)              # 1 is slowest, 10 is fast, 0 is instant
t.pensize(3)
t.color("gold")

# ---- A SQUARE --------------------------------------------------------------
# Four sides, turning 90 degrees each time. Four turns of 90 is 360 - a full
# circle - so the turtle finishes facing exactly where it started.
for _ in range(4):
    t.forward(120)
    t.left(90)

# "_" is a Python convention meaning "I have to repeat this, but I do not care
# about the number". It is a normal variable; the name just says to ignore it.

# ---- MOVING WITHOUT DRAWING ------------------------------------------------
t.penup()               # lift the pen
t.goto(-200, -100)      # jump straight there, drawing nothing
t.pendown()             # put it back down
#
# Forget the penup() and you get a line connecting everything you draw. Try it
# once: it is a memorable mistake.

t.color("tomato")

# ---- A TRIANGLE ------------------------------------------------------------
# Three sides, so each turn must be 360 / 3 = 120 degrees.
for _ in range(3):
    t.forward(120)
    t.left(120)

# ---- turtle uses MATHS coordinates ----------------------------------------
# (0, 0) is the MIDDLE of the window, and y grows UPWARDS.
# Nearly every other graphics system - tkinter, pygame, the web canvas, your
# phone - puts (0, 0) in the TOP-LEFT with y growing DOWNWARDS.
# Turtle is the odd one out, on purpose, because it was built for teaching.
t.penup()
t.goto(0, 0)
t.pendown()
t.color("white")
t.dot(12)
t.penup()
t.goto(10, 10)
t.write("(0, 0) is here - the MIDDLE", font=("Arial", 13, "normal"))

t.penup()
t.goto(0, 200)
t.write("y grows UP this way", font=("Arial", 12, "normal"))

t.hideturtle()

# Keep the window open until someone clicks it. WITHOUT a line like this the
# script ends, and the window closes instantly - which is the most common
# "my turtle program does not work" problem there is.
screen.exitonclick()
