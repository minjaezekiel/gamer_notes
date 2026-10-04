# ============================================================================
# 02 - BRICK BREAKER  (the finished Python beginner track)
# Lesson 6, Games with Python, Beginner
#
# Every idea from the whole two weeks:
#   L1  state, a loop, and a world described as DATA
#   L2  drawing, and grid-to-pixel conversion
#   L3  a loop that never waits, polled input, delta time
#   L4  lists of game objects, and rules
#   L5  a real tkinter canvas, retained mode, y pointing DOWN
#   L6  classes, levels as data, and saving to a file
#
# RUN IT:      python3 02-brick-breaker.py
# CONTROLS:    left/right arrows or A/D, or the mouse.
#              SPACE launches the ball and restarts. P pauses. Escape quits.
#
# CHANGE ME FIRST:
#   The LEVELS lists below. Type different digits and run it again. You are
#   designing levels without touching one line of game logic.
# ============================================================================

import json
import random
import time
import tkinter
from pathlib import Path

# ---- CONSTANTS -------------------------------------------------------------
WIDTH = 640
HEIGHT = 520

BRICK_W = 68
BRICK_H = 24
GAP = 6
MARGIN = 32
BRICK_TOP = 70

PADDLE_W = 104
PADDLE_H = 14
PADDLE_Y = HEIGHT - 44
PADDLE_SPEED = 560          # pixels per SECOND

BALL_R = 8
BALL_SPEED = 330
STEER_STRENGTH = 300
STARTING_LIVES = 3

# Next to this script, not wherever you happened to run it from.
SAVE_FILE = Path(__file__).parent / "highscore.json"

# ---- THE LEVELS - data, not code -------------------------------------------
# 0 = nothing, 1 = normal brick, 2 = tough brick (two hits)
LEVELS = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 1, 1],
    ],
    [
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 2, 1, 1, 2, 1, 0],
        [1, 2, 1, 1, 1, 1, 2, 1],
        [0, 1, 1, 0, 0, 1, 1, 0],
    ],
]

# ---- WINDOW ----------------------------------------------------------------
window = tkinter.Tk()
window.title("Brick Breaker")
window.resizable(False, False)
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT,
                        bg="#15181d", highlightthickness=0)
canvas.pack()


# ============================================================================
# CLASSES
# ============================================================================
class Brick:
    """One brick: where it is, how tough it is, and how to draw itself."""

    def __init__(self, x, y, w, h, hits):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hits = hits
        self.alive = True
        self.item = canvas.create_rectangle(x, y, x + w, y + h,
                                            fill=self.colour(), outline="")

    def colour(self):
        return "#ff9246" if self.hits >= 2 else "#4a9eff"

    def box(self):
        return (self.x, self.y, self.w, self.h)

    def hit(self):
        """Take one hit. Returns the score earned."""
        self.hits -= 1
        if self.hits <= 0:
            self.alive = False
            canvas.delete(self.item)      # the canvas's record too
            return 100
        # Still alive, but now weaker - so CHANGE ITS COLOUR. Without that
        # feedback the player thinks the game is broken.
        canvas.itemconfig(self.item, fill=self.colour())
        return 25

    def destroy(self):
        canvas.delete(self.item)


class Paddle:
    def __init__(self):
        self.w = PADDLE_W
        self.h = PADDLE_H
        self.x = WIDTH / 2 - self.w / 2
        self.y = PADDLE_Y
        self.item = canvas.create_rectangle(0, 0, 0, 0,
                                            fill="#e8ebee", outline="")

    def box(self):
        return (self.x, self.y, self.w, self.h)

    def update(self, dt, keys, mouse_x):
        if keys.get("Left") or keys.get("a") or keys.get("A"):
            self.x -= PADDLE_SPEED * dt
        elif keys.get("Right") or keys.get("d") or keys.get("D"):
            self.x += PADDLE_SPEED * dt
        elif mouse_x is not None:
            self.x = mouse_x - self.w / 2

        # Clamp inside the window.
        self.x = max(0, min(WIDTH - self.w, self.x))

    def draw(self):
        canvas.coords(self.item, self.x, self.y,
                      self.x + self.w, self.y + self.h)


class Ball:
    def __init__(self):
        self.r = BALL_R
        self.x = WIDTH / 2
        self.y = PADDLE_Y - BALL_R - 2
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.stuck = True
        self.item = canvas.create_oval(0, 0, 0, 0, fill="#ffd43b", outline="")

    def box(self):
        """Drawn as a circle, collides as a square. That is a HITBOX: the
        shape you test need not be the shape you see."""
        return (self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def stick_to(self, paddle):
        self.stuck = True
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.x = paddle.x + paddle.w / 2
        self.y = paddle.y - self.r - 2

    def launch(self):
        self.stuck = False
        self.speed_x = random.uniform(-110, 110)
        self.speed_y = -BALL_SPEED           # NEGATIVE is UP in tkinter

    def update(self, dt, paddle):
        if self.stuck:
            self.x = paddle.x + paddle.w / 2
            self.y = paddle.y - self.r - 2
            return

        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

        # Walls. Position first, THEN velocity - or it sticks and vibrates.
        if self.x - self.r < 0:
            self.x = self.r
            self.speed_x = -self.speed_x
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.speed_x = -self.speed_x
        if self.y - self.r < 0:
            self.y = self.r
            self.speed_y = -self.speed_y

    def bounce_off_paddle(self, paddle):
        self.y = paddle.y - self.r
        self.speed_y = -abs(self.speed_y)

        # Where on the paddle did it hit? -1 left, 0 middle, +1 right.
        # Dividing by HALF the paddle width turns pixels into a fraction,
        # so this works whatever width the paddle happens to be.
        #
        # This is not physics. It is better than physics, because it hands the
        # player control: the game becomes about aiming.
        centre = paddle.x + paddle.w / 2
        offset = (self.x - centre) / (paddle.w / 2)
        self.speed_x = offset * STEER_STRENGTH

    def bounce_off_brick(self, brick):
        """Work out WHICH SIDE the ball came in through.

        Always flipping speed_y instead is the classic bug: a ball clipping a
        brick's side then carves straight through the whole row.
        """
        b = self.box()
        k = brick.box()
        overlap_x = min(b[0] + b[2], k[0] + k[2]) - max(b[0], k[0])
        overlap_y = min(b[1] + b[3], k[1] + k[3]) - max(b[1], k[1])

        # The SMALLER overlap is the axis it arrived along: a ball that has
        # just poked in from above overlaps a lot horizontally and barely at
        # all vertically.
        if overlap_y < overlap_x:
            self.speed_y = -self.speed_y
        else:
            self.speed_x = -self.speed_x

    def draw(self):
        canvas.coords(self.item, self.x - self.r, self.y - self.r,
                      self.x + self.r, self.y + self.r)


# ============================================================================
# SAVING
# ============================================================================
def load_high_score():
    """Read the high score. Any problem at all means "start at zero".

    The file might not exist (first run), might be damaged, might be on a
    read-only disk, or might have been edited by a curious student. A game that
    CRASHES because it cannot load a high score is worse than one that quietly
    starts at zero.
    """
    try:
        return int(json.loads(SAVE_FILE.read_text())["high_score"])
    except Exception:
        return 0


def save_high_score(value):
    try:
        SAVE_FILE.write_text(json.dumps({"high_score": value}))
    except Exception:
        pass        # a read-only disk should not end the game


# ============================================================================
# STATE
# ============================================================================
state = "MENU"            # MENU | PLAYING | PAUSED | LEVEL_DONE | GAME_OVER | WON
score = 0
lives = STARTING_LIVES
level_index = 0
high_score = load_high_score()
bricks = []
keys = {}
mouse_x = None
last_time = time.time()

paddle = Paddle()
ball = Ball()

title_item = canvas.create_text(WIDTH / 2, HEIGHT / 2 - 16, fill="#e8ebee",
                                font=("Arial", 34, "bold"), text="")
subtitle_item = canvas.create_text(WIDTH / 2, HEIGHT / 2 + 24, fill="#8b94a0",
                                   font=("Arial", 15), text="")
hud_item = canvas.create_text(14, 12, anchor="nw", fill="#8b94a0",
                              font=("Courier", 14), text="")
best_item = canvas.create_text(WIDTH - 14, 12, anchor="ne", fill="#8b94a0",
                               font=("Courier", 14), text="")


# ============================================================================
# LEVELS
# ============================================================================
def build_level(layout):
    """Turn a grid of digits into Brick objects.

    This nested-loop pattern appears in every tile-based game ever made.
    """
    result = []
    for row in range(len(layout)):
        for column in range(len(layout[row])):
            kind = layout[row][column]
            #            ^row    ^column
            # ROW first, THEN column. The outer list holds rows, so the first
            # index picks which row. layout[column][row] gives a level mirrored
            # along the diagonal - or a crash, if it is not square.
            if kind == 0:
                continue
            x = MARGIN + column * (BRICK_W + GAP)
            y = BRICK_TOP + row * (BRICK_H + GAP)
            result.append(Brick(x, y, BRICK_W, BRICK_H, kind))
    return result


def clear_bricks():
    for brick in bricks:
        brick.destroy()
    bricks.clear()


def start_game():
    global score, lives, level_index, state
    score = 0
    lives = STARTING_LIVES
    level_index = 0
    load_level(0)
    state = "PLAYING"


def load_level(index):
    global bricks
    clear_bricks()
    bricks = build_level(LEVELS[index])
    ball.stick_to(paddle)


def next_level():
    global level_index, state
    level_index += 1
    if level_index >= len(LEVELS):
        state = "WON"
        remember_score()
        return
    load_level(level_index)
    state = "PLAYING"


def lose_a_life():
    global lives, state
    lives -= 1
    if lives <= 0:
        state = "GAME_OVER"
        remember_score()
    else:
        ball.stick_to(paddle)


def remember_score():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)


# ============================================================================
# INPUT
# ============================================================================
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
# Note that exception handling is NOT the right tool here. Wrapping the loop
# in try/except would HIDE the error rather than prevent it - and would keep
# hiding it later, when something genuinely went wrong.
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
    global state
    keys[event.keysym] = True

    if event.keysym == "space":
        if state in ("MENU", "GAME_OVER", "WON"):
            start_game()
        elif state == "LEVEL_DONE":
            next_level()
        elif state == "PLAYING" and ball.stuck:
            ball.launch()
    elif event.keysym in ("p", "P"):
        if state == "PLAYING":
            state = "PAUSED"
        elif state == "PAUSED":
            state = "PLAYING"
    elif event.keysym == "Escape":
        quit_game()


def on_release(event):
    keys[event.keysym] = False


def on_motion(event):
    global mouse_x
    mouse_x = event.x


# The X button on the window bypasses our Escape handler entirely - the window
# manager tears the window down without telling our code. This tells tkinter to
# call quit_game() instead of destroying the window behind our back.
window.protocol("WM_DELETE_WINDOW", quit_game)

window.bind("<KeyPress>", on_press)
window.bind("<KeyRelease>", on_release)
canvas.bind("<Motion>", on_motion)
window.focus_force()


# ============================================================================
# UPDATE - each function does ONE job
# ============================================================================
def check_brick_collisions():
    global score
    for brick in bricks:
        if not brick.alive:
            continue
        if not boxes_overlap(ball.box(), brick.box()):
            continue

        ball.bounce_off_brick(brick)
        score += brick.hit()

        # ONE brick per frame. Without this, a ball between two bricks destroys
        # both and flips its velocity twice - so it carries straight on as if
        # nothing happened. Real Breakout does exactly this.
        break

    if all(not brick.alive for brick in bricks):
        set_level_done()


def set_level_done():
    global state
    state = "LEVEL_DONE"
    remember_score()


def boxes_overlap(a, b):
    """Each box is (x, y, width, height). Four conditions, all joined by and."""
    return (a[0] < b[0] + b[2] and
            a[0] + a[2] > b[0] and
            a[1] < b[1] + b[3] and
            a[1] + a[3] > b[1])


def update(dt):
    # ONE state check, here, rather than scattered through every object.
    if state != "PLAYING":
        return

    paddle.update(dt, keys, mouse_x)
    ball.update(dt, paddle)

    if (not ball.stuck and ball.speed_y > 0
            and boxes_overlap(ball.box(), paddle.box())):
        ball.bounce_off_paddle(paddle)

    check_brick_collisions()

    if ball.y - ball.r > HEIGHT:
        lose_a_life()


# ============================================================================
# RENDER
# ============================================================================
def draw():
    paddle.draw()
    ball.draw()

    playing = state != "MENU"
    canvas.itemconfig(hud_item,
                      text=(f"score {score}   lives {'@' * max(0, lives)}"
                            f"   level {level_index + 1}") if playing else "")
    canvas.itemconfig(best_item, text=f"best {high_score}")

    messages = {
        "MENU": ("BRICK BREAKER", "press SPACE to play"),
        "PAUSED": ("PAUSED", "P to carry on"),
        "LEVEL_DONE": ("LEVEL CLEAR", "SPACE for the next one"),
        "GAME_OVER": ("GAME OVER", f"score {score}  -  SPACE to try again"),
        "WON": ("YOU WIN", f"final score {score}  -  SPACE to play again"),
    }
    title, subtitle = messages.get(state, ("", ""))
    if state == "PLAYING" and ball.stuck:
        subtitle = "press SPACE to launch"
    canvas.itemconfig(title_item, text=title)
    canvas.itemconfig(subtitle_item, text=subtitle)


# ============================================================================
# THE LOOP - unchanged since lesson 3
# ============================================================================
def game_loop():
    global last_time, after_id

    # If we are shutting down, do nothing. A frame may already have been
    # queued before the player quit, and the canvas no longer exists.
    if not running:
        return

    now = time.time()
    dt = now - last_time
    last_time = now
    if dt > 0.1:
        dt = 1 / 60

    update(dt)
    draw()

    # Remember the id so quit_game() can cancel this if the player quits
    # before it fires.
    after_id = window.after(16, game_loop)


game_loop()
window.mainloop()
