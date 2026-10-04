# ============================================================================
# 02 - Recording keys instead of reacting to them
# Lesson 3, Games with Python, Beginner
#
# WHAT THIS SHOWS:  The keys dictionary, displayed live. Nothing moves yet -
#                   this file is only about the idea of REMEMBERING input
#                   rather than REACTING to it.
#
# RUN IT:           python3 02-keys-recorded.py
# TRY THIS:         hold three or four keys at once. Then try five or six.
#                   Many cheap keyboards physically cannot report more than
#                   about three, which is a real limit in local multiplayer.
# ============================================================================

import tkinter
import turtle

screen = turtle.Screen()
screen.setup(width=700, height=460)
screen.bgcolor("#15181d")
screen.title("02 - What is held down right now?")
screen.tracer(0)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

# ---- THE RECORD ------------------------------------------------------------
# One dictionary saying which keys are currently down. That is the whole idea.
keys = {}

WATCHED = ["Up", "Down", "Left", "Right", "space", "a", "d", "w", "s"]


def press(name):
    """Build and return a handler that records THIS key as pressed.

    Why a function that returns a function? Because onkeypress wants a handler
    taking no arguments, but we need different behaviour for each key. Calling
    press("Right") creates a small function that remembers it was made for
    "Right".

    The obvious alternative is broken:
        for name in WATCHED:
            screen.onkeypress(lambda: keys.update({name: True}), name)
    All those handlers share ONE name variable, and by the time anyone presses
    a key the loop has finished and name is the LAST item. So every key sets
    the same entry. That is the CLOSURE TRAP, it catches professionals, and it
    produces a bug with no error message.
    """
    def handler():
        keys[name] = True
    return handler


def release(name):
    def handler():
        keys[name] = False
    return handler


for key_name in WATCHED:
    screen.onkeypress(press(key_name), key_name)
    screen.onkeyrelease(release(key_name), key_name)

screen.listen()     # WITHOUT this, nothing is ever noticed


def draw():
    drawer.clear()
    drawer.penup()
    drawer.color("#8b94a0")
    drawer.goto(-320, 180)
    drawer.write("Keys currently held down:", font=("Arial", 15, "normal"))

    # Only the ones whose value is currently True.
    held = [name for name in keys if keys[name]]

    drawer.goto(-300, 130)
    if held:
        drawer.color("#51cf66")
        drawer.write("\n".join(held), font=("Courier", 20, "normal"))
    else:
        drawer.color("#555c66")
        drawer.write("(nothing)", font=("Courier", 20, "normal"))

    drawer.goto(-320, -190)
    drawer.color("#555c66")
    drawer.write("A key nobody has touched is not in the dictionary at all,\n"
                 "so use keys.get(name) - keys[name] would raise KeyError.",
                 font=("Arial", 12, "normal"))
    screen.update()


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
        draw()
        screen.ontimer(game_loop, 16)    # call me again in 16 ms (about 60 fps)
    except (tkinter.TclError, turtle.Terminator):
        return      # the window has gone; stop quietly



game_loop()
screen.mainloop()
