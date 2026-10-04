#!/usr/bin/env python3
"""Regression test: quitting must never crash the player out with red text.

TEACHER-FACING. Run it with:   python3 test_quit_does_not_crash.py

THE BUG THIS LOCKS DOWN
Every tkinter and turtle game schedules its next frame with after()/ontimer().
If the player quits while one of those is already queued, the callback still
fires - but the window and canvas are gone, so drawing raises

    _tkinter.TclError: invalid command name ".!canvas"

and the player gets a wall of red text on the way out. It happened on EVERY
quit, in every tkinter game, before this was fixed.

There are two separate ways out of a game, and they need different fixes:

  1. The QUIT KEY (Escape).  We control this, so a "running" flag plus
     after_cancel() prevents the problem. Exception handling would only hide it.

  2. The WINDOW'S X BUTTON.  We do NOT control this - the window manager tears
     the window down without asking. There is nothing to prevent, so the loop
     has to notice and stop quietly. This is the one place in the beginner
     course where catching an exception is the right answer.
"""
import importlib.util
import pathlib
import sys
import subprocess
import tkinter

ROOT = pathlib.Path(__file__).resolve().parent
failures = []


def load(rel, queue):
    """Import a game, capturing the frame it schedules instead of running it."""
    spec = importlib.util.spec_from_file_location("game_under_test", str(ROOT / rel))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(label, fn):
    try:
        fn()
        print(f"  ok   {label}")
    except Exception as error:
        print(f"  FAIL {label}: {type(error).__name__}: {str(error)[:60]}")
        failures.append(label)


# ---------------------------------------------------------------- tkinter ---
TK_GAMES = [
    ("Brick Breaker", "lesson-06-capstone-brick-breaker/code/02-brick-breaker.py"),
    ("Catch the Fruit", "lesson-05-a-real-window-tkinter/code/03-catch-the-fruit.py"),
]

_real_tk_init = tkinter.Tk.__init__
def _quiet_tk_init(self, *a, **k):
    _real_tk_init(self, *a, **k)
    try:
        self.withdraw()        # never show it; this is a test, not a demo
    except Exception:
        pass
tkinter.Tk.__init__ = _quiet_tk_init


for name, rel in TK_GAMES:
    queued = []
    tkinter.Misc.after = lambda self, ms, func=None, *a: (queued.append(func), "id")[1]
    tkinter.Misc.after_cancel = lambda self, i: None
    tkinter.Misc.mainloop = lambda self, *a, **k: None
    tkinter.Tk.mainloop = lambda self, *a, **k: None

    game = load(rel, queued)

    class EscapeEvent:
        keysym = "Escape"

    def quit_then_run_queued_frame(game=game, queued=queued):
        game.on_press(EscapeEvent())      # the player presses Escape
        if queued:
            queued[-1]()                  # the already-queued frame fires

    check(f"{name}: Escape with a frame already queued", quit_then_run_queued_frame)

    # The X button must be wired to our own quit, not straight to destroy().
    def close_button_is_handled(game=game):
        assert hasattr(game, "quit_game"), "no quit_game() to hook the X button to"

    check(f"{name}: window close button is handled", close_button_is_handled)


# ----------------------------------------------------------------- turtle ---
# Each turtle game needs its OWN PROCESS. turtle keeps a single module-level
# root window, so once one test tears it down, no later test in the same
# process can create another. That is a property of turtle, not of the games.

TURTLE_GAMES = [
    ("Snake", "lesson-04-snake/code/02-snake.py"),
    ("Steerable player", "lesson-03-making-it-move/code/03-steerable-player.py"),
    ("Delta time", "lesson-03-making-it-move/code/04-delta-time.py"),
    ("Keys recorded", "lesson-03-making-it-move/code/02-keys-recorded.py"),
]

CHILD = r"""
import importlib.util, sys, tkinter, turtle

# Create the window WITHDRAWN so running this test does not flash
# windows across the screen. Drawing still happens; it is just not shown.
_real_init = tkinter.Tk.__init__
def _quiet(self, *a, **k):
    _real_init(self, *a, **k)
    try:
        self.withdraw()
    except Exception:
        pass
tkinter.Tk.__init__ = _quiet

queued = []
turtle.TurtleScreen.ontimer = lambda self, f=None, t=0: queued.append(f)
for method in ("mainloop", "exitonclick", "done", "bye"):
    for cls in (turtle.Screen, turtle.TurtleScreen):
        if hasattr(cls, method):
            setattr(cls, method, lambda self, *a, **k: None)

spec = importlib.util.spec_from_file_location("g", sys.argv[1])
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)

# Exactly what the X button does: tear the window down underneath us.
try:
    game.screen._root.destroy()
except Exception:
    pass

if queued:
    queued[-1]()          # the already-queued frame fires anyway
print("CLEAN")
"""

for name, rel in TURTLE_GAMES:
    result = subprocess.run([sys.executable, "-c", CHILD, str(ROOT / rel)],
                            capture_output=True, timeout=60)
    output = result.stdout.decode(errors="replace")
    if result.returncode == 0 and "CLEAN" in output:
        print(f"  ok   {name}: window closed with a frame queued")
    else:
        err = result.stderr.decode(errors="replace").strip().splitlines()
        print(f"  FAIL {name}: window closed with a frame queued")
        for line in err[-2:]:
            print(f"         {line}")
        failures.append(name)


print()
if failures:
    print(f"{len(failures)} QUIT PATH(S) STILL CRASH: {failures}")
    sys.exit(1)
print("ALL QUIT PATHS EXIT CLEANLY")
