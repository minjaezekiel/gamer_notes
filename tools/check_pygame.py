#!/usr/bin/env python3
"""
check_pygame.py - actually RUN every pygame example, headlessly.

WHY THIS EXISTS
    `python3 -m py_compile` proves a file parses. It does not prove that a surface
    was created with the right argument count, that a Rect method exists, that a
    colour tuple has three numbers in it, or that the collision call is spelled
    correctly. Every one of those is a runtime error, and every one of them would
    first appear in front of a class.

    So this runs each example for real, with SDL pointed at its dummy video and
    audio drivers, so no window appears and no sound plays.

HOW AN EXAMPLE COOPERATES
    Each example's loop checks one environment variable:

        SELFTEST_FRAMES=120 python3 03-sprites.py

    and exits after that many frames. The lessons use a tiny helper for this:

        frames = 0
        selftest = int(os.environ.get("SELFTEST_FRAMES", "0"))
        while running:
            ...
            frames += 1
            if selftest and frames >= selftest:
                running = False

    That is four lines in each example, it is visible to the student, and it is the
    only reason this script can exist. A hidden hook would be worse.

USAGE
    python3 tools/check_pygame.py              every example
    python3 tools/check_pygame.py --only snake
    python3 tools/check_pygame.py --frames 240

WHICH PYTHON
    tools/.venv/bin/python if it exists (so the system Python is never touched),
    otherwise whatever `python3` is. If pygame is not importable, this skips with a
    message rather than failing - it is a check, not a dependency of the course.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = ROOT / "tools" / ".venv" / "bin" / "python"

GREEN = "\033[32m"
RED = "\033[31m"
BOLD = "\033[1m"
OFF = "\033[0m"

SKIP_DIRS = {".git", "__pycache__", ".venv", "solutions-private"}


def interpreter() -> str:
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable or "python3"


def pygame_available(python: str) -> tuple[bool, str]:
    try:
        # pygame prints a banner on import. PYGAME_HIDE_SUPPORT_PROMPT silences
        # it; taking the last line as well means an older pygame that ignores the
        # variable still reports a clean version number.
        env = dict(os.environ, PYGAME_HIDE_SUPPORT_PROMPT="1")
        out = subprocess.run(
            [python, "-c", "import pygame; print(pygame.version.ver)"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        if out.returncode == 0:
            lines = [l for l in out.stdout.strip().splitlines() if l.strip()]
            return True, lines[-1] if lines else "unknown"
        return False, out.stderr.strip().splitlines()[-1] if out.stderr else "import failed"
    except Exception as err:            # noqa: BLE001 - reporting, not handling
        return False, str(err)


def find_examples(only: str | None) -> tuple[list[Path], list[Path]]:
    """Returns (runnable examples, shared modules)."""
    found: list[Path] = []
    modules: list[Path] = []
    for path in sorted(ROOT.glob("games_with_py/**/*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith("test_"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "import pygame" not in text:
            continue
        # --only must be applied BEFORE the module/example split, or shared
        # modules slip past the filter and the counts stop matching the request.
        if only and only not in str(path):
            continue
        # A shared content module (see COURSE_SPEC section 9) opens no window, so
        # running it proves only that it imports. That is still worth doing, and
        # it is labelled differently so the output does not claim more than it did.
        if "set_mode" not in text:
            modules.append(path)
            continue
        found.append(path)
    return found, modules


def run_one(python: str, path: Path, frames: int, timeout: float) -> str | None:
    """Return None on success, or a short description of what went wrong."""
    env = dict(os.environ)
    # The dummy drivers are what make this headless. Without them SDL tries to
    # open a window and fails on a machine with no display.
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"
    env["SELFTEST_FRAMES"] = str(frames)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

    try:
        done = subprocess.run(
            [python, path.name],
            cwd=path.parent,
            capture_output=True, text=True, timeout=timeout, env=env,
        )
    except subprocess.TimeoutExpired:
        return (f"did not exit within {timeout:.0f}s — does its loop check "
                f"SELFTEST_FRAMES?")

    if done.returncode != 0:
        lines = [l for l in done.stderr.strip().splitlines() if l.strip()]
        tail = lines[-3:] if lines else ["no output"]
        return "exit code %d\n        %s" % (done.returncode, "\n        ".join(tail))

    # A traceback printed without a non-zero exit code still counts as broken.
    if "Traceback (most recent call last)" in done.stderr:
        return "printed a traceback:\n        " + done.stderr.strip().splitlines()[-1]
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="only paths containing this text")
    ap.add_argument("--frames", type=int, default=150,
                    help="how many frames each example runs (default 150)")
    ap.add_argument("--timeout", type=float, default=60.0)
    args = ap.parse_args()

    python = interpreter()
    ok, version = pygame_available(python)

    print(f"\n{BOLD}== pygame examples (run headlessly, SDL dummy drivers) =={OFF}")
    if not ok:
        print(f"  SKIPPED: pygame is not importable by {python}")
        print(f"           ({version})")
        print("           install it with:")
        print("             python3 -m venv tools/.venv")
        print("             tools/.venv/bin/pip install pygame-ce")
        return 0

    examples, modules = find_examples(args.only)
    if not examples and not modules:
        print("  (no pygame examples yet)")
        return 0

    print(f"  using {python}  ·  pygame {version}  ·  {args.frames} frames each")

    failures = 0
    for path in modules:
        rel = path.relative_to(ROOT)
        problem = run_one(python, path, args.frames, args.timeout)
        if problem is None:
            print(f"  ok    {rel}  (shared module: imports cleanly, opens no window)")
        else:
            failures += 1
            print(f"  {RED}FAIL{OFF}  {rel}\n        {problem}")

    for path in examples:
        rel = path.relative_to(ROOT)
        problem = run_one(python, path, args.frames, args.timeout)
        if problem is None:
            print(f"  ok    {rel}")
        else:
            failures += 1
            print(f"  {RED}FAIL{OFF}  {rel}\n        {problem}")

    print()
    if failures:
        print(f"{RED}{failures} of {len(examples) + len(modules)} pygame file(s) failed{OFF}")
        return 1
    print(f"{GREEN}all {len(examples)} pygame example(s) ran cleanly"
          f"{f', plus {len(modules)} shared module(s)' if modules else ''}{OFF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
