# ============================================================================
# 04 - Delta time: making the speed the same on every computer
# Lesson 3, Games with Python, Beginner
#
# WHAT THIS SHOWS:  Why "move 5 pixels per frame" is a bug, and the fix.
#                   Two circles are told to cross at the same speed. The red
#                   one counts frames; the green one measures seconds.
#
# RUN IT:           python3 04-delta-time.py
# TRY THIS:         change FAKE_SLOWDOWN to 0.02 (a deliberately slow frame) and
#                   run it again. The red circle crawls. Nobody changed its
#                   speed setting - only the computer got slower.
#
# This is the proper version of the loop. Use it from lesson 5 onwards.
# ============================================================================

import time
import tkinter
import turtle

screen = turtle.Screen()
screen.setup(width=760, height=420)
screen.bgcolor("#15181d")
screen.title("04 - Delta time")
screen.tracer(0)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

START_X = -330
FINISH_X = 320

PER_FRAME = 5         # pixels per FRAME   - the shortcut. Wrong.
PER_SECOND = 300      # pixels per SECOND  - correct.
# These two agree only at 60 fps, because 5 x 60 = 300. That coincidence is
# why the bug hides on the machine you wrote the game on.

FAKE_SLOWDOWN = 0.0   # seconds of pretend work per frame. Try 0.02.

bad_x = START_X
good_x = START_X
last_time = time.time()
measured_fps = 0.0
running = True


def quit_game():
    global running
    running = False
    screen.bye()


def restart():
    global bad_x, good_x
    bad_x = START_X
    good_x = START_X


screen.onkey(quit_game, "Escape")
screen.onkey(restart, "space")
screen.listen()


def update(dt):
    global bad_x, good_x

    # Counts frames. It has no idea how long a frame lasted.
    if bad_x < FINISH_X:
        bad_x += PER_FRAME

    # Multiplies by how long the frame actually took.
    #   distance = speed x time
    # At 60 fps, dt is about 0.0167 s, so 300 x 0.0167 is about 5 pixels -
    # which is where the 5 came from in the first place.
    if good_x < FINISH_X:
        good_x += PER_SECOND * dt


def draw():
    drawer.clear()

    for y, x, colour, label in [
        (90, bad_x, "#ff6b6b", f"x += 5 per FRAME   ->  {PER_FRAME * max(1, round(measured_fps))} px/sec"),
        (-60, good_x, "#51cf66", "x += 300 * dt per SECOND  ->  300 px/sec, always"),
    ]:
        # the track
        drawer.penup()
        drawer.goto(START_X - 10, y - 30)
        drawer.color("#2a3039")
        drawer.pendown()
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(FINISH_X - START_X + 60)
            drawer.left(90)
            drawer.forward(60)
            drawer.left(90)
        drawer.end_fill()
        drawer.penup()

        # finish line
        drawer.goto(FINISH_X, y - 34)
        drawer.color("#8b94a0")
        drawer.pendown()
        drawer.goto(FINISH_X, y + 34)
        drawer.penup()

        # the circle
        drawer.goto(x, y - 16)
        drawer.color(colour)
        drawer.pendown()
        drawer.begin_fill()
        drawer.circle(16)
        drawer.end_fill()
        drawer.penup()

        drawer.goto(START_X - 10, y + 42)
        drawer.color(colour)
        drawer.write(label, font=("Courier", 13, "normal"))

    drawer.goto(0, 170)
    drawer.color("#8b94a0")
    drawer.write(f"measured: {measured_fps:.0f} frames per second"
                 f"   -   space to restart, Escape to quit",
                 align="center", font=("Arial", 13, "normal"))


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
        global last_time, measured_fps
        if not running:
            return

        # ---- WORK OUT DELTA TIME ----
        now = time.time()
        dt = now - last_time          # seconds since the previous frame
        last_time = now

        # CLAMP. On the very first frame, or after the window has been dragged or
        # the machine has been busy, dt can be enormous - and everything teleports.
        if dt > 0.1:
            dt = 1 / 60
        if dt > 0:
            # Smooth the reading, or the number flickers too fast to read.
            measured_fps = measured_fps * 0.9 + (1 / dt) * 0.1

        if FAKE_SLOWDOWN > 0:
            time.sleep(FAKE_SLOWDOWN)     # pretend the computer is slow

        update(dt)
        draw()
        screen.update()
        screen.ontimer(game_loop, 16)
    except (tkinter.TclError, turtle.Terminator):
        return      # the window has gone; stop quietly



game_loop()
screen.mainloop()
