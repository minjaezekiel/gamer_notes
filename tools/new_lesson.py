#!/usr/bin/env python3
"""
new_lesson.py - scaffold a lesson folder from templates/.

Always use this rather than copying a previous lesson by hand. A stale relative
path back to shared/ is the commonest way to break a lesson page, and this works
the depth out for you.

USAGE
    python3 tools/new_lesson.py <level-path> <number> "<Title>"

EXAMPLES
    python3 tools/new_lesson.py webgames/beginner_lvl 1 "What is a game, really?"
    python3 tools/new_lesson.py games_with_cpp/intermediate_lvl 7 "Textures and sprites"

It creates:
    <level-path>/lesson-NN-slugified-title/
        notes.md          from templates/notes.md
        exercises.md      from templates/exercises.md
        visualizer.html   from templates/visualizer.html   (--no-visualizer to skip)
        code/
        solutions/
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

TRACK_LABELS = {
    "webgames": "Web Games",
    "games_with_py": "Games with Python",
    "games_with_cpp": "Games with C++",
}
LEVEL_LABELS = {
    "beginner_lvl": "Beginner",
    "intermediate_lvl": "Intermediate",
    "advanced_lvl": "Advanced",
}
LESSON_TOTALS = {"beginner_lvl": 6, "intermediate_lvl": 12, "advanced_lvl": 12}


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("level", help="e.g. webgames/beginner_lvl")
    ap.add_argument("number", type=int, help="lesson number, 1-12")
    ap.add_argument("title", help='lesson title, in quotes')
    ap.add_argument("--no-visualizer", action="store_true",
                    help="skip visualizer.html (the lesson links a shared one instead)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing folder")
    args = ap.parse_args()

    level_dir = ROOT / args.level
    if not level_dir.is_dir():
        sys.exit(f"No such level directory: {args.level}\n"
                 f"Expected something like webgames/beginner_lvl")

    parts = Path(args.level).parts
    track = parts[0]
    level = parts[1] if len(parts) > 1 else ""

    slug = slugify(args.title)
    name = f"lesson-{args.number:02d}-{slug}"
    dest = level_dir / name

    if dest.exists() and not args.force:
        sys.exit(f"{dest.relative_to(ROOT)} already exists. Use --force to overwrite.")

    # How far up from the lesson folder is the repo root? That is how we build a
    # correct relative path to shared/ regardless of nesting depth.
    depth = len(dest.relative_to(ROOT).parts)
    shared = "/".join([".."] * depth) + "/shared"

    subs = {
        "{{NUM}}": str(args.number),
        "{{TITLE}}": args.title,
        "{{SLUG}}": slug,
        "{{TRACK_LABEL}}": TRACK_LABELS.get(track, track),
        "{{LEVEL_LABEL}}": LEVEL_LABELS.get(level, level),
        "{{TOTAL}}": str(LESSON_TOTALS.get(level, 6)),
        "{{SHARED}}": shared,
    }

    def render(template_name: str) -> str:
        text = (TEMPLATES / template_name).read_text(encoding="utf-8")
        for k, v in subs.items():
            text = text.replace(k, v)
        return text

    (dest / "code").mkdir(parents=True, exist_ok=True)
    (dest / "solutions").mkdir(parents=True, exist_ok=True)

    written = []
    for tpl, out in [("notes.md", "notes.md"), ("exercises.md", "exercises.md")]:
        (dest / out).write_text(render(tpl), encoding="utf-8")
        written.append(out)

    if not args.no_visualizer:
        (dest / "visualizer.html").write_text(render("visualizer.html"), encoding="utf-8")
        written.append("visualizer.html")

    print(f"Created {dest.relative_to(ROOT)}/")
    for w in written:
        print(f"  {w}")
    print("  code/")
    print("  solutions/")
    print(f"\nPath back to shared/ is: {shared}")
    print("\nNext: fill in notes.md, then see docs/AUTHORING_GUIDE.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
