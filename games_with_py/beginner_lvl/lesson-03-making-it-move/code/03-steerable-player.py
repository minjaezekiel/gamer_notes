# ============================================================================
# 03 - A PLAYER YOU STEER  (the finished lesson 3 result)
# Lesson 3, Games with Python, Beginner
#
# WHAT THIS SHOWS:  Lesson 1's loop and lesson 2's drawing, joined together -
#                   and a loop that NEVER WAITS for the player.
#
# RUN IT:           python3 03-steerable-player.py
# CONTROLS:         arrow keys or WASD. Hold them - it glides.
#
# CHANGE ME FIRST:  SPEED on line 36. It is pixels per FRAME, which is a
#                   shortcut - see 04-delta-time.py for the proper version.
#
# TRY THIS:         hold Up and Right together and time how long it takes to
#                   cross the screen diagonally, then straight. The diagonal is
#                   about 41% faster. That is a real bug - see the notes.
# ============================================================================

import tkinter
import turtle

# ---- SETUP -----------------------------------------------------------------
screen = turtle.Screen()
screen.setup(width=700, height=560)
screen.bgcolor("#15181d")
screen.title("03 - Arrow keys or WASD")
screen.tracer(0)              # we will call screen.update() ourselves

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

# ---- STATE -----------------------------------------------------------------
player_x = 0
player_y = 0
PLAYER_RADIUS = 18
SPEED = 5                     # pixels per FRAME (see the note above)
HALF_W = 330
HALF_H = 260
running = True

# ---- INPUT: record only, never move ----------------------------------------
keys = {}


def press(name):
    def handler():
        keys[name] = True
    return handler


def release(name):
    def handler():
        keys[name] = False
    return handler


for key_name in ["Up", "Down", "Left", "Right", "w", "a", "s", "d"]:
    screen.onkeypress(press(key_name), key_name)
    screen.onkeyrelease(release(key_name), key_name)


def quit_game():
    global running
    running = False
    screen.bye()


screen.onkey(quit_game, "Escape")
screen.listen()               # WITHOUT this, no key is ever noticed.
                              # It is the most common "nothing works" cause.


# ---- UPDATE: all movement happens here -------------------------------------
def update():
    global player_x, player_y

    # Turn KEYBOARD FACTS into GAME INTENTIONS in one place. Because of these
    # four lines the game supports arrows and WASD, and the movement code below
    # never mentions a key name. Adding a gamepad later means editing only here.
    wants_right = keys.get("Right") or keys.get("d")
    wants_left = keys.get("Left") or keys.get("a")
    wants_up = keys.get("Up") or keys.get("w")
    wants_down = keys.get("Down") or keys.get("s")
    # keys.get(name) rather than keys[name]: a key nobody has touched is not in
    # the dictionary at all, and [ ] would raise KeyError. get() returns None,
    # which an if treats as false.

    if wants_right:
        player_x += SPEED
    if wants_left:
        player_x -= SPEED
    if wants_up:
        player_y += SPEED       # turtle: y grows UPWARDS
    if wants_down:
        player_y -= SPEED

    # CLAMP so the player cannot leave the window.
    # Read it inside out: min(HALF_W, x) is "never more than HALF_W",
    # and max(-HALF_W, ...) is "never less than -HALF_W".
    player_x = max(-HALF_W, min(HALF_W, player_x))
    player_y = max(-HALF_H, min(HALF_H, player_y))


# ---- RENDER: draw the world as it is now -----------------------------------
def draw():
    # ERASE FIRST. Turtle does not clean up after itself - without this you
    # get a solid trail of circles across the screen.
    drawer.clear()

    # the player
    drawer.penup()
    drawer.goto(player_x, player_y - PLAYER_RADIUS)
    drawer.pendown()
    drawer.color("#4a9eff")
    drawer.begin_fill()
    drawer.circle(PLAYER_RADIUS)
    drawer.end_fill()
    drawer.penup()

    # a little text so the window explains itself
    drawer.goto(0, 250)
    drawer.color("#8b94a0")
    drawer.write("arrow keys or WASD   -   Escape to quit",
                 align="center", font=("Arial", 13, "normal"))
    drawer.goto(-330, -270)
    drawer.color("#555c66")
    drawer.write(f"x={player_x}  y={player_y}", font=("Courier", 12, "normal"))


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
        if not running:
            return

        update()            # INPUT is read in here, every frame
        draw()
        screen.update()     # show the finished frame, all at once

        # Ask to be called again in 16 milliseconds - about 1/60 of a second.
        # THIS is what makes it a loop. There is no "while" anywhere.
        #
        # This is exactly the web track's requestAnimationFrame(frame). Different
        # language, different name, identical idea: do one frame's work, then ask
        # to be called back.
        screen.ontimer(game_loop, 16)
    except (tkinter.TclError, turtle.Terminator):
        return      # the window has gone; stop quietly



game_loop()             # start it off
screen.mainloop()       # hand control to turtle, which calls us back forever
