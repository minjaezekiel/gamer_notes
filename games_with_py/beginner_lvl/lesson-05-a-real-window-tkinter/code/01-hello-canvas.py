# ============================================================================
# 01 - A tkinter window, and the two surprises
# Lesson 5, Games with Python, Beginner
#
# WHAT THIS SHOWS:  (1) y points DOWN, the opposite of turtle.
#                   (2) create_rectangle takes LEFT, TOP, RIGHT, BOTTOM -
#                       not x, y, width, height.
#
# RUN IT:           python3 01-hello-canvas.py
# CHANGE ME FIRST:  the numbers in create_rectangle on line 47 and watch which
#                   corner each one controls.
# ============================================================================

import tkinter

WIDTH = 640
HEIGHT = 420

window = tkinter.Tk()
window.title("01 - Hello canvas")
window.resizable(False, False)

# highlightthickness=0 removes a focus border that otherwise shifts everything
# by a couple of pixels and makes collision maths subtly wrong. A small thing
# that wastes a lot of time.
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT,
                        bg="#15181d", highlightthickness=0)
canvas.pack()

# ---- (0, 0) IS THE TOP-LEFT CORNER ----------------------------------------
canvas.create_oval(-6, -6, 6, 6, fill="#ff6b6b", outline="")
canvas.create_text(14, 14, anchor="nw", fill="#ff6b6b",
                   font=("Arial", 13), text="(0, 0) is HERE - the top-left")

# ---- y GROWS DOWNWARDS -----------------------------------------------------
canvas.create_line(30, 40, 30, 300, fill="#51cf66", width=2, arrow="last")
canvas.create_text(42, 300, anchor="w", fill="#51cf66",
                   font=("Arial", 13), text="y grows DOWN this way")
canvas.create_line(40, 30, 300, 30, fill="#4a9eff", width=2, arrow="last")
canvas.create_text(300, 44, anchor="w", fill="#4a9eff",
                   font=("Arial", 13), text="x grows right")

canvas.create_text(320, 120, fill="#ffd43b", font=("Arial", 15, "bold"),
                   text="turtle was the ODD ONE OUT.")
canvas.create_text(320, 146, fill="#8b94a0", font=("Arial", 13),
                   text="tkinter, pygame, raylib, the web canvas and your\n"
                        "phone all put (0,0) top-left with y going down.")

# ---- RECTANGLES ARE TWO CORNERS -------------------------------------------
# create_rectangle(LEFT, TOP, RIGHT, BOTTOM)
#                   ^      ^     ^      ^
# NOT (x, y, width, height). This catches everybody out once.
box = canvas.create_rectangle(100, 240, 180, 290,
                              fill="#4a9eff", outline="")
canvas.create_text(100, 300, anchor="nw", fill="#8b94a0", font=("Courier", 12),
                   text="create_rectangle(100, 240, 180, 290)\n"
                        "left=100 top=240 right=180 bottom=290\n"
                        "so it is 80 wide and 50 tall")

# ---- AN ITEM IS AN INTEGER, NOT AN OBJECT ---------------------------------
# The canvas keeps the real shape and hands you a number to refer to it by.
print("create_rectangle returned:", box, "- it is a plain integer,",
      "not an object.")
print("The canvas is keeping the shape; this number is just a handle.")

canvas.create_text(320, 370, fill="#555c66", font=("Arial", 12),
                   text="Look at the terminal: the item ID is printed there.")

window.mainloop()
