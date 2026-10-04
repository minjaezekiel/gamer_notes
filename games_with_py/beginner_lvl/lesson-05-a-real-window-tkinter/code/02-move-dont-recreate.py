# ============================================================================
# 02 - Move it, do not re-create it
# Lesson 5, Games with Python, Beginner
#
# WHAT THIS SHOWS:  The headline bug of this lesson. The canvas REMEMBERS every
#                   shape you make. Creating a new one each frame instead of
#                   moving the existing one piles up thousands of invisible
#                   shapes until the game grinds to a halt.
#
# RUN IT:           python3 02-move-dont-recreate.py
# TRY THIS:         click the button to switch to the broken way, then watch
#                   the item count and the frame rate.
#
# This is the difference between RETAINED mode (tkinter: the system remembers
# your shapes) and IMMEDIATE mode (turtle, the web canvas: you redraw
# everything yourself). Neither is better. Knowing which you are in is what
# matters.
# ============================================================================

import time
import tkinter

WIDTH = 640
HEIGHT = 380

window = tkinter.Tk()
window.title("02 - Move it, do not re-create it")
window.resizable(False, False)

canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT,
                        bg="#15181d", highlightthickness=0)
canvas.pack()

broken = False
ball_x = 60.0
ball_speed = 220.0
last_time = time.time()
fps = 0.0

# Created ONCE, before the loop. This is the right way.
ball = canvas.create_oval(0, 0, 0, 0, fill="#4a9eff", outline="")
readout = canvas.create_text(16, 16, anchor="nw", fill="#8b94a0",
                             font=("Courier", 13), text="")


def toggle():
    global broken
    broken = not broken
    button.config(text="now: BROKEN (creating every frame)" if broken
                  else "now: correct (moving the one item)")


button = tkinter.Button(window, text="now: correct (moving the one item)",
                        command=toggle, font=("Arial", 13))
button.pack(pady=6)


def update(dt):
    global ball_x
    ball_x += ball_speed * dt
    if ball_x > WIDTH - 30 or ball_x < 30:
        ball_speed_flip()


def ball_speed_flip():
    global ball_speed, ball_x
    ball_speed = -ball_speed
    ball_x = max(30, min(WIDTH - 30, ball_x))


def draw():
    if broken:
        # ---- THE BUG ----
        # A brand new oval, every single frame. The canvas keeps every one of
        # them forever. After a few seconds there are thousands, all stacked up,
        # and the canvas slows to a crawl redrawing them all.
        canvas.create_oval(ball_x - 20, 170, ball_x + 20, 210,
                           fill="#ff6b6b", outline="")
    else:
        # ---- THE FIX ----
        # Move the ONE item we made before the loop started.
        canvas.coords(ball, ball_x - 20, 170, ball_x + 20, 210)

    count = len(canvas.find_all())
    canvas.itemconfig(readout,
                      text=f"items on the canvas: {count:>6}\n"
                           f"frames per second:   {fps:>6.0f}")
    # Keep the readout on top of the pile of ovals.
    canvas.tag_raise(readout)


def game_loop():
    global last_time, fps
    now = time.time()
    dt = now - last_time
    last_time = now
    if dt > 0.1:
        dt = 1 / 60
    if dt > 0:
        fps = fps * 0.9 + (1 / dt) * 0.1

    update(dt)
    draw()

    # Same idea as turtle's ontimer and JavaScript's requestAnimationFrame:
    # "call this function again in 16 milliseconds".
    window.after(16, game_loop)


game_loop()
window.mainloop()
