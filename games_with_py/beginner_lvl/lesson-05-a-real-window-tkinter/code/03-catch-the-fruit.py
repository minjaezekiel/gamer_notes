# ============================================================================
# 03 - CATCH THE FALLING FRUIT  (the finished lesson 5 result)
# Lesson 5, Games with Python, Beginner
#
# Everything so far, on a real tkinter canvas:
#   L1  state and a loop        L4  lists of game objects
#   L2  drawing                 L5  retained-mode canvas, y pointing DOWN
#   L3  a loop that never waits, polled input
#
# RUN IT:           python3 03-catch-the-fruit.py
# CONTROLS:         left/right arrows or A/D. Space to start. P pauses.
#
# CHANGE ME FIRST:  GRAVITY on line 44. Try 150 (floaty) and 900 (brutal).
#
# BREAK IT:         change "fruit['y'] += ..." to "-=" and watch the fruit fall
#                   upwards. In tkinter, y grows DOWNWARDS.
# ============================================================================

import random
import time
import tkinter

# ---- CONSTANTS -------------------------------------------------------------
WIDTH = 640
HEIGHT = 480

BASKET_W = 92
BASKET_H = 18
BASKET_SPEED = 520        # pixels per SECOND
BASKET_Y = HEIGHT - 50

FRUIT_SIZE = 22
GRAVITY = 320             # pixels per second, per second
START_FALL_SPEED = 90
STARTING_LIVES = 3

# ---- WINDOW ----------------------------------------------------------------
window = tkinter.Tk()
window.title("Catch the Falling Fruit")
window.resizable(False, False)

canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT,
                        bg="#15181d", highlightthickness=0)
canvas.pack()

# ---- STATE -----------------------------------------------------------------
state = "MENU"            # MENU | PLAYING | PAUSED | GAME_OVER
basket_x = WIDTH / 2 - BASKET_W / 2
fruits = []               # each is a dict, including its canvas item id
score = 0
lives = STARTING_LIVES
spawn_timer = 0.0
last_time = time.time()

# ---- CANVAS ITEMS, created ONCE --------------------------------------------
# The canvas REMEMBERS these. We create them here and only ever MOVE them.
# Creating new ones inside the loop is the headline bug of this lesson - see
# 02-move-dont-recreate.py.
basket_item = canvas.create_rectangle(0, 0, 0, 0, fill="#4a9eff", outline="")
score_item = canvas.create_text(14, 12, anchor="nw", fill="#8b94a0",
                                font=("Courier", 15), text="")
lives_item = canvas.create_text(WIDTH - 14, 12, anchor="ne", fill="#8b94a0",
                                font=("Courier", 15), text="")
title_item = canvas.create_text(WIDTH / 2, HEIGHT / 2 - 20, fill="#e8ebee",
                                font=("Arial", 34, "bold"), text="")
subtitle_item = canvas.create_text(WIDTH / 2, HEIGHT / 2 + 24, fill="#8b94a0",
                                   font=("Arial", 15), text="")


def set_box(item, x, y, w, h):
    """Position an item using x, y, width, height - what we actually think in.

    tkinter wants LEFT, TOP, RIGHT, BOTTOM. Doing the conversion once here
    means never doing it in your head again.
    """
    canvas.coords(item, x, y, x + w, y + h)


# ---- INPUT: record only ----------------------------------------------------
keys = {}
# ---- QUITTING CLEANLY ------------------------------------------------------
# A real bug, and one every tkinter game hits.
#
# window.after(16, game_loop) schedules the NEXT frame. If the player quits
# while one of those is already queued, the callback still fires - but the
# window and canvas are gone, so every canvas.coords() call raises
#     _tkinter.TclError: invalid command name ".!canvas"
# and the player gets a wall of red text on the way out.
#
# Two guards fix it:
#   1. a "running" flag that game_loop checks BEFORE touching the canvas
#   2. after_cancel() on the frame we know is queued
#
# Note that exception handling is NOT the right tool here. Wrapping the loop in
# try/except would hide the error rather than prevent it, and would keep
# hiding it when something genuinely went wrong.
running = True
after_id = None


def quit_game():
    """Stop the loop first, THEN take the window away."""
    global running
    running = False
    if after_id is not None:
        window.after_cancel(after_id)    # unschedule the queued frame
    window.destroy()




def on_press(event):
    keys[event.keysym] = True
    if event.keysym == "space" and state in ("MENU", "GAME_OVER"):
        start_game()
    if event.keysym in ("p", "P"):
        toggle_pause()
    if event.keysym == "Escape":
        quit_game()


def on_release(event):
    keys[event.keysym] = False


# One handler for every key, so there is no closure trap this time.
# The X button on the window bypasses our Escape handler entirely - the window
# manager tears the window down without telling our code. This tells tkinter to
# call quit_game() instead of destroying the window behind our back.
window.protocol("WM_DELETE_WINDOW", quit_game)

window.bind("<KeyPress>", on_press)
window.bind("<KeyRelease>", on_release)
window.focus_force()        # make sure the window actually receives keys


def toggle_pause():
    global state
    if state == "PLAYING":
        state = "PAUSED"
    elif state == "PAUSED":
        state = "PLAYING"


# ---- GAME ------------------------------------------------------------------
def start_game():
    global state, score, lives, spawn_timer, basket_x
    for fruit in fruits:
        canvas.delete(fruit["item"])      # tell the canvas to forget them too
    fruits.clear()
    score = 0
    lives = STARTING_LIVES
    spawn_timer = 0.0
    basket_x = WIDTH / 2 - BASKET_W / 2
    state = "PLAYING"


def spawn_fruit():
    x = random.uniform(10, WIDTH - FRUIT_SIZE - 10)
    golden = random.random() < 0.12
    item = canvas.create_oval(0, 0, 0, 0,
                              fill="#ffd43b" if golden else "#ff6b6b",
                              outline="")
    fruits.append({
        "x": x,
        "y": -FRUIT_SIZE,
        "speed": START_FALL_SPEED,
        "golden": golden,
        "item": item,
    })


def boxes_overlap(a, b):
    """Each box is (x, y, width, height). The same four conditions as always."""
    return (a[0] < b[0] + b[2] and
            a[0] + a[2] > b[0] and
            a[1] < b[1] + b[3] and
            a[1] + a[3] > b[1])


def spawn_delay():
    """Fruit arrives faster as the score rises - but never faster than 0.35s.

    That floor is doing real work. Without it the game eventually spawns faster
    than anyone can react to, and becomes unplayable rather than hard. Design
    the limit at the same time as the slope.
    """
    return max(0.35, 1.2 - score * 0.004)


def update(dt):
    global basket_x, spawn_timer, score, lives, state

    if state != "PLAYING":
        return

    # ---- basket ----
    wants_left = keys.get("Left") or keys.get("a") or keys.get("A")
    wants_right = keys.get("Right") or keys.get("d") or keys.get("D")
    if wants_left:
        basket_x -= BASKET_SPEED * dt
    if wants_right:
        basket_x += BASKET_SPEED * dt
    basket_x = max(0, min(WIDTH - BASKET_W, basket_x))      # clamp

    # ---- spawning ----
    spawn_timer += dt
    if spawn_timer >= spawn_delay():
        spawn_timer = 0.0
        spawn_fruit()

    basket_box = (basket_x, BASKET_Y, BASKET_W, BASKET_H)

    # ---- fruit ----
    # BACKWARDS, because we remove items as we go. Forwards + remove skips
    # elements - the same bug you have now met three times.
    for i in range(len(fruits) - 1, -1, -1):
        fruit = fruits[i]

        # Gravity changes the SPEED; the speed changes the POSITION.
        # Both ADD, because in tkinter y grows DOWNWARDS.
        fruit["speed"] += GRAVITY * dt
        fruit["y"] += fruit["speed"] * dt

        fruit_box = (fruit["x"], fruit["y"], FRUIT_SIZE, FRUIT_SIZE)

        if boxes_overlap(fruit_box, basket_box):
            score += 25 if fruit["golden"] else 10
            remove_fruit(i)
        elif fruit["y"] > HEIGHT:
            if not fruit["golden"]:     # missing a golden one costs nothing
                lives -= 1
            remove_fruit(i)
            if lives <= 0:
                state = "GAME_OVER"


def remove_fruit(index):
    """Remove from BOTH records: ours and the canvas's.

    In retained mode you are keeping two sets of books. Forget the
    canvas.delete and the fruit disappears from the game logic but stays on
    screen forever.
    """
    canvas.delete(fruits[index]["item"])
    fruits.pop(index)


# ---- RENDER ----------------------------------------------------------------
def draw():
    set_box(basket_item, basket_x, BASKET_Y, BASKET_W, BASKET_H)

    for fruit in fruits:
        set_box(fruit["item"], fruit["x"], fruit["y"], FRUIT_SIZE, FRUIT_SIZE)

    playing = state in ("PLAYING", "PAUSED", "GAME_OVER")
    canvas.itemconfig(score_item, text=f"score {score}" if playing else "")
    canvas.itemconfig(lives_item,
                      text=("lives " + "@" * max(0, lives)) if playing else "")

    if state == "MENU":
        canvas.itemconfig(title_item, text="CATCH THE FRUIT")
        canvas.itemconfig(subtitle_item, text="press SPACE to play")
    elif state == "PAUSED":
        canvas.itemconfig(title_item, text="PAUSED")
        canvas.itemconfig(subtitle_item, text="P to carry on")
    elif state == "GAME_OVER":
        canvas.itemconfig(title_item, text="GAME OVER")
        canvas.itemconfig(subtitle_item, text=f"score {score}  -  SPACE to play again")
    else:
        canvas.itemconfig(title_item, text="")
        canvas.itemconfig(subtitle_item, text="")


# ---- THE LOOP --------------------------------------------------------------
def game_loop():
    global last_time, after_id

    # If we are shutting down, do nothing. A frame may already have been
    # queued before the player quit, and the canvas no longer exists.
    if not running:
        return

    now = time.time()
    dt = now - last_time
    last_time = now
    if dt > 0.1:            # clamp: the window was dragged, or the machine was busy
        dt = 1 / 60

    update(dt)
    draw()

    # Same idea as turtle's ontimer and JavaScript's requestAnimationFrame.
    # The id lets quit_game() cancel this frame if the player quits first.
    after_id = window.after(16, game_loop)


game_loop()
window.mainloop()
