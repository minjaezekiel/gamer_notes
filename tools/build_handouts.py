#!/usr/bin/env python3
"""
build_handouts.py - turn every lesson's exercises.md into a printable PDF.

THE PIPELINE
    exercises.md  ->  HTML (with shared/css/print.css inlined)  ->  Chrome  ->  PDF

WHY IT IS BUILT THIS WAY
Only Google Chrome is required. No LaTeX, no pandoc, no wkhtmltopdf, and no pip
packages - not even a Markdown library. A teacher who clones this repo onto a
school laptop can rebuild every handout, and the CSS that styles the PDF is the
same file that styles the lesson pages, so handouts cannot drift out of sync
with the notes.

The Markdown converter below handles the subset the exercise files use. Raw HTML
passes straight through, which is how exercises.md gets at the question furniture
in print.css: ruled answer lines, sketch boxes, checkpoint tick-boxes.

USAGE
    python3 tools/build_handouts.py                      # everything
    python3 tools/build_handouts.py webgames             # one track
    python3 tools/build_handouts.py webgames/beginner_lvl # one level
    python3 tools/build_handouts.py --html-only          # skip Chrome, keep the HTML

If Chrome is not installed, the print-ready HTML is still written and you can
open it and print to PDF from the browser by hand.
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRINT_CSS = ROOT / "shared" / "css" / "print.css"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

COURSE_NAME = "Game Dev Bootcamp"


# ---------------------------------------------------------------------------
# A small Markdown -> HTML converter.
#
# Deliberately covers only what the exercise files use. Keeping it small and
# obvious is worth more here than covering every Markdown feature, because it
# means there is no dependency to install and nothing to go wrong on a machine
# we do not control.
# ---------------------------------------------------------------------------

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def inline(text: str) -> str:
    """Convert inline Markdown. Code spans are protected first so that
    **bold** inside a code span is not treated as formatting."""
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = INLINE_CODE.sub(stash, text)
    text = html.escape(text, quote=False)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    text = LINK.sub(r'<a href="\2">\1</a>', text)

    def unstash(m):
        return "<code>" + html.escape(spans[int(m.group(1))], quote=False) + "</code>"

    return re.sub(r"\x00(\d+)\x00", unstash, text)


def is_raw_html(line: str) -> bool:
    """A line that starts a block-level HTML tag is passed through untouched."""
    return bool(re.match(r"\s*</?(div|table|tr|td|th|thead|tbody|ul|ol|li|p|span|"
                         r"pre|br|hr|h[1-6]|blockquote|i|b|strong|em|code|img)\b", line))


def markdown_to_html(src: str) -> str:
    out = []
    lines = src.split("\n")
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # ---- fenced code block ----
        if line.strip().startswith("```"):
            i += 1
            body = []
            while i < n and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            code = html.escape("\n".join(body), quote=False)
            # A long snippet is allowed to break across pages rather than leave
            # most of a page blank.
            cls = ' class="long"' if len(body) > 28 else ""
            out.append(f"<pre{cls}><code>{code}</code></pre>")
            continue

        # ---- raw HTML passthrough ----
        if is_raw_html(line):
            out.append(line)
            i += 1
            continue

        # ---- blank ----
        if not line.strip():
            i += 1
            continue

        # ---- horizontal rule ----
        if re.fullmatch(r"\s*([-*_])\s*(\1\s*){2,}", line):
            out.append("<hr>")
            i += 1
            continue

        # ---- heading ----
        m = re.match(r"(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2).strip())}</h{level}>")
            i += 1
            continue

        # ---- table ----
        if line.lstrip().startswith("|") and i + 1 < n and re.match(
                r"\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>"
                       + "".join(f"<th>{inline(c)}</th>" for c in header)
                       + "</tr></thead><tbody>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue

        # ---- blockquote ----
        if line.lstrip().startswith(">"):
            body = []
            while i < n and lines[i].lstrip().startswith(">"):
                body.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(body)) + "</blockquote>")
            continue

        # ---- list (unordered or ordered, one level of nesting) ----
        bullet = re.match(r"(\s*)([-*+]|\d+\.)\s+(.*)", line)
        if bullet:
            ordered = bool(re.match(r"\d+\.", bullet.group(2)))
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>")
            depth = 0
            while i < n:
                m2 = re.match(r"(\s*)([-*+]|\d+\.)\s+(.*)", lines[i])
                if not m2:
                    # A plain indented line continues the previous bullet.
                    if lines[i].startswith("  ") and lines[i].strip():
                        out.append(" " + inline(lines[i].strip()))
                        i += 1
                        continue
                    break
                this_depth = 1 if len(m2.group(1)) >= 2 else 0
                if this_depth > depth:
                    out.append(f"<{tag}>")
                    depth = this_depth
                elif this_depth < depth:
                    out.append(f"</{tag}>")
                    depth = this_depth
                out.append(f"<li>{inline(m2.group(3))}</li>")
                i += 1
            while depth > 0:
                out.append(f"</{tag}>")
                depth -= 1
            out.append(f"</{tag}>")
            continue

        # ---- paragraph ----
        body = []
        while i < n and lines[i].strip() and not is_raw_html(lines[i]) \
                and not re.match(r"(#{1,6})\s|\s*```|\s*\||\s*>|(\s*)([-*+]|\d+\.)\s", lines[i]):
            body.append(lines[i].strip())
            i += 1
        if body:
            out.append("<p>" + inline(" ".join(body)) + "</p>")
        else:
            i += 1

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

TRACK_NAMES = {
    "webgames": "Web Games (HTML / CSS / JavaScript)",
    "games_with_py": "Games with Python",
    "games_with_cpp": "Games with C++",
}
LEVEL_NAMES = {
    "beginner_lvl": "Beginner",
    "intermediate_lvl": "Intermediate",
    "advanced_lvl": "Advanced",
}


def split_cheat_sheet(src: str):
    """Pull the '## Cheat sheet' section out of the Markdown.

    The spec says page 1 of every handout is a one-page cheat sheet. Rather than
    make every author remember to wrap it in the right divs, we find the section
    here and wrap it automatically: two columns, and a page break after it, so
    the questions always start on a fresh sheet.

    Returns (cheat_markdown_or_None, the_rest).
    """
    m = re.search(r"^##\s+Cheat\s*sheet\s*$", src, re.M | re.I)
    if not m:
        return None, src
    start = m.end()
    nxt = re.search(r"^##\s+", src[start:], re.M)
    end = start + nxt.start() if nxt else len(src)
    cheat = src[start:end]
    rest = src[:m.start()] + src[end:]
    # A trailing horizontal rule inside the cheat section is redundant once the
    # section is on a page of its own.
    cheat = re.sub(r"\n\s*-{3,}\s*\n*\s*$", "\n", cheat)
    return cheat, rest


def build_html(md_path: Path) -> str:
    src = md_path.read_text(encoding="utf-8")

    # The first H1 is the handout title; it is removed from the body so it is not
    # printed twice.
    m = re.search(r"^#\s+(.*)$", src, re.M)
    title = m.group(1).strip() if m else md_path.parent.name
    if m:
        src = src[:m.start()] + src[m.end():]

    parts = md_path.relative_to(ROOT).parts
    track = TRACK_NAMES.get(parts[0], parts[0])
    level = LEVEL_NAMES.get(parts[1], parts[1]) if len(parts) > 1 else ""

    css = PRINT_CSS.read_text(encoding="utf-8")

    cheat_md, rest_md = split_cheat_sheet(src)
    body = ""
    if cheat_md and cheat_md.strip():
        body += ('<div class="sheet">\n<h2>Cheat sheet</h2>\n<div class="cheat">\n'
                 + markdown_to_html(cheat_md)
                 + '\n</div>\n</div>\n')
    body += markdown_to_html(rest_md)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
{css}
</style>
</head>
<body>
<div class="handout-head">
  <p class="course">{html.escape(COURSE_NAME)} &middot; {html.escape(track)} &middot; {html.escape(level)}</p>
  <h1>{html.escape(title)}</h1>
  <p class="meta">One lesson: 2 hours 30 minutes &middot; keep this sheet</p>
</div>

<div class="nameline"><span>Name</span><span>Class</span><span>Date</span></div>

{body}

<p class="footer-note">{html.escape(COURSE_NAME)} &mdash; {html.escape(title)}.
Licensed MIT: copy it, change it, share it.</p>
</body>
</html>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def to_pdf(chrome: str, html_path: Path, pdf_path: Path, timeout: float = 60.0) -> bool:
    """Print one HTML file to PDF with headless Chrome.

    WHY THIS IS NOT JUST subprocess.run()
    On several Chrome builds (macOS especially), `--print-to-pdf` writes a
    complete, correct PDF and then the headless process simply never exits. Every
    flag combination we tried behaves the same way, and all of them produce a
    byte-identical file. So waiting for Chrome to finish means waiting forever.

    Instead we watch for the output file to appear and for its size to stop
    changing, and then stop the process ourselves. Two consecutive equal,
    non-zero sizes means the write has completed.
    """
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        pdf_path.unlink()

    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
            f"--user-data-dir={profile}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        deadline = time.time() + timeout
        last_size = -1
        settled = False

        while time.time() < deadline:
            if proc.poll() is not None:
                break                       # Chrome exited on its own: fine too
            time.sleep(0.35)
            size = pdf_path.stat().st_size if pdf_path.exists() else 0
            if size > 0 and size == last_size:
                settled = True              # size stable: the PDF is written
                break
            last_size = size

        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

    if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
        sys.stderr.write(f"  ! Chrome produced no usable PDF for {html_path.name}\n")
        if not settled:
            sys.stderr.write(f"    (gave up after {timeout:.0f}s)\n")
        return False
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    html_only = "--html-only" in sys.argv
    scope = args[0] if args else ""

    search_root = ROOT / scope if scope else ROOT
    if not search_root.exists():
        sys.exit(f"No such path: {search_root}")

    targets = sorted(search_root.rglob("lesson-*/exercises.md"))
    if not targets:
        print(f"No exercises.md found under {search_root.relative_to(ROOT) or '.'}")
        print("(Nothing to do - this is not an error.)")
        return 0

    chrome = None if html_only else find_chrome()
    if not html_only and not chrome:
        sys.stderr.write(
            "Chrome was not found, so no PDFs can be generated.\n"
            "The print-ready HTML is still written next to each handout; open it in\n"
            "any browser and use File > Print > Save as PDF.\n\n")

    built = failed = 0
    for md in targets:
        lesson_dir = md.parent
        level_dir = lesson_dir.parent
        # "lesson-04-when-things-touch" -> "lesson-04"
        num = re.match(r"(lesson-\d+)", lesson_dir.name)
        stem = num.group(1) if num else lesson_dir.name

        out_dir = level_dir / "handouts"
        out_dir.mkdir(parents=True, exist_ok=True)
        html_path = out_dir / f"{stem}-handout.html"
        pdf_path = out_dir / f"{stem}-handout.pdf"

        html_path.write_text(build_html(md), encoding="utf-8")
        rel = pdf_path.relative_to(ROOT)

        if chrome:
            # One retry. Chrome occasionally fails to produce a PDF when
            # several instances are already running (for example while
            # tools/check_pages.js is doing its parallel pass). It is a
            # transient resource problem, not a problem with the document.
            okay = to_pdf(chrome, html_path, pdf_path)
            if not okay:
                sys.stderr.write("    retrying once...\n")
                time.sleep(1.5)
                okay = to_pdf(chrome, html_path, pdf_path)
            if okay:
                size = pdf_path.stat().st_size // 1024
                print(f"  built  {rel}  ({size} KB)")
                built += 1
            else:
                failed += 1
        else:
            print(f"  html   {html_path.relative_to(ROOT)}  (print it by hand)")
            built += 1

    print(f"\n{built} handout(s) built" + (f", {failed} failed" if failed else "."))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
