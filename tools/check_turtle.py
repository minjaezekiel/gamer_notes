#!/usr/bin/env python3
"""
check_turtle.py - actually RUN every turtle and tkinter example.

WHY THIS EXISTS
`python3 -m py_compile` only proves a file parses. It says nothing about
whether the drawing code works: a typo'd method name, a bad colour, a wrong
argument count all compile fine and then blow up the moment a student runs it.

This runs each script to completion with the blocking calls - exitonclick(),
mainloop(), done(), after() - neutralised, so the whole program executes and
then exits instead of sitting there waiting for a click.

WHAT IT PROVES:      every drawing command runs with no exception.
WHAT IT DOES NOT:    that the picture LOOKS right. A human still has to open it.

The windows are created WITHDRAWN - they never appear on screen - so running
this does not flash a dozen windows at you. Everything is still really drawn and
every error still surfaces.

It needs a display (macOS and Windows have one; a headless Linux box needs
xvfb-run). If there is no display it says so and skips, rather than failing.

USAGE
    python3 tools/check_turtle.py                  # every turtle/tkinter example
    python3 tools/check_turtle.py games_with_py    # just one subtree
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The harness that runs inside each child process.
HARNESS = textwrap.dedent('''
    import sys, runpy

    # ---- keep the windows OFF the user's screen ----
    # These examples each open a real window. Verifying 13 of them would
    # otherwise flash 13 windows open and shut across the screen, which is
    # obnoxious and looks like a bug in the games themselves.
    #
    # withdraw() creates the window but never maps it to the display. All the
    # drawing still happens and all the errors still surface - the user just
    # does not have to watch it.
    import tkinter as _tk
    _real_tk_init = _tk.Tk.__init__
    def _quiet_tk_init(self, *a, **k):
        _real_tk_init(self, *a, **k)
        try:
            self.withdraw()
        except Exception:
            pass
    _tk.Tk.__init__ = _quiet_tk_init

    # ---- neutralise anything that would block forever ----
    try:
        import turtle
        for name in ("exitonclick", "mainloop", "done", "bye"):
            if hasattr(turtle.Screen, name):
                setattr(turtle.Screen, name, lambda self, *a, **k: None)
            if hasattr(turtle.TurtleScreen, name):
                setattr(turtle.TurtleScreen, name, lambda self, *a, **k: None)
            if hasattr(turtle, name):
                setattr(turtle, name, lambda *a, **k: None)
    except Exception:
        pass

    try:
        import tkinter
        # mainloop() would block; after() would schedule work we never reach.
        tkinter.Misc.mainloop = lambda self, *a, **k: None
        tkinter.Tk.mainloop = lambda self, *a, **k: None
        # Run an after() callback ONCE immediately, so the first frame of a
        # game loop is exercised, then stop - otherwise it would recurse
        # forever.
        _seen = set()
        _real_after = tkinter.Misc.after
        def _after(self, ms, func=None, *args):
            if func is not None and id(func) not in _seen:
                _seen.add(id(func))
                try:
                    func(*args)
                except Exception:
                    raise
            return "fake-after-id"
        tkinter.Misc.after = _after
    except Exception:
        pass

    runpy.run_path(sys.argv[1], run_name="__main__")
''')


def find_targets(scope: str):
    base = ROOT / scope if scope else ROOT
    out = []
    for p in sorted(base.rglob("*.py")):
        if "__pycache__" in p.parts or "tools" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "import turtle" in text or "import tkinter" in text:
            out.append(p)
    return out


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else ""
    targets = find_targets(scope)

    if not targets:
        print("  (no turtle or tkinter examples found yet)")
        return 0

    # A quick probe: can we open a window at all?
    probe = subprocess.run(
        [sys.executable, "-c", "import tkinter; tkinter.Tk().destroy()"],
        capture_output=True, timeout=30)
    if probe.returncode != 0:
        print("  SKIPPED: no display available, so turtle/tkinter cannot run here.")
        print("  (On a headless Linux machine, try: xvfb-run python3 tools/check_turtle.py)")
        return 0

    harness_path = ROOT / ".check_turtle_harness.py"
    harness_path.write_text(HARNESS, encoding="utf-8")

    failed = 0
    try:
        for target in targets:
            rel = target.relative_to(ROOT)
            try:
                result = subprocess.run(
                    [sys.executable, str(harness_path), str(target)],
                    capture_output=True, timeout=60,
                    cwd=str(target.parent),
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            except subprocess.TimeoutExpired:
                print(f"  FAIL  {rel}\n        timed out - something is still blocking")
                failed += 1
                continue

            if result.returncode != 0:
                err = result.stderr.decode(errors="replace").strip().splitlines()
                print(f"  FAIL  {rel}")
                for line in err[-6:]:
                    print(f"        {line}")
                failed += 1
            else:
                print(f"  ok    {rel}")
    finally:
        harness_path.unlink(missing_ok=True)

    print()
    if failed:
        print(f"  {failed} of {len(targets)} turtle/tkinter example(s) failed to run.")
    else:
        print(f"  All {len(targets)} turtle/tkinter examples ran with no exceptions.")
        print("  (This does not prove the picture looks right - open one and check.)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
