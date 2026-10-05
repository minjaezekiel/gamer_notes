#!/usr/bin/env bash
# =============================================================================
# check_all.sh - verify everything in the course repository.
#
#   bash tools/check_all.sh           full run (includes a real Chrome pass)
#   bash tools/check_all.sh --quick   skip Chrome; fast enough for a tight loop
#
# What it checks:
#   1. every .cpp compiles with the exact flags the lessons tell students to use
#   2. every .py byte-compiles, and every turtle/tkinter example RUNS
#   3. every .js and every inline <script> parses
#   4. every HTML page loads in real Chrome with no console errors
#   5. every relative link in .md and .html resolves
#
# What it CANNOT check, and you must do by hand:
#   - that a visualizer actually animates, steps and resets (click it)
#   - that a PDF is laid out properly (look at it)
#   - that a lesson's build section fits in 70 minutes (time it)
# =============================================================================
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1
ROOT="$PWD"
QUICK=""
[ "${1:-}" = "--quick" ] && QUICK="--quick"

RED=$'\033[31m'; GREEN=$'\033[32m'; BOLD=$'\033[1m'; OFF=$'\033[0m'
FAILED=0
note() { printf '\n%s== %s ==%s\n' "$BOLD" "$1" "$OFF"; }
bad()  { printf '  %sFAIL%s  %s\n' "$RED" "$OFF" "$1"; FAILED=$((FAILED+1)); }
good() { printf '  ok    %s\n' "$1"; }

# ---------------------------------------------------------------------------
# 1. C++
# ---------------------------------------------------------------------------
note "C++ (clang++ -std=c++17 -Wall, the same command the lessons give students)"
CXX="$(command -v clang++ || command -v g++ || true)"
if [ -z "$CXX" ]; then
  echo "  SKIPPED: no C++ compiler found"
else
  COUNT=0
  while IFS= read -r f; do
    COUNT=$((COUNT+1))
    if OUT=$("$CXX" -std=c++17 -Wall -fsyntax-only "$f" 2>&1); then
      [ -n "$OUT" ] && { good "${f#./} (with warnings)"; printf '        %s\n' "$OUT" | head -3; } \
                    || good "${f#./}"
    else
      bad "${f#./}"
      printf '        %s\n' "$OUT" | head -6
    fi
  done < <(find . -name '*.cpp' -not -path './.git/*' -not -path './tools/.venv/*' | sort)
  [ "$COUNT" -eq 0 ] && echo "  (no .cpp files yet)"
fi

# ---------------------------------------------------------------------------
# 2. Python
# ---------------------------------------------------------------------------
note "Python (byte-compile)"
COUNT=0
while IFS= read -r f; do
  COUNT=$((COUNT+1))
  if OUT=$(python3 -m py_compile "$f" 2>&1); then
    good "${f#./}"
  else
    bad "${f#./}"
    printf '        %s\n' "$OUT" | head -6
  fi
done < <(find . -name '*.py' -not -path './.git/*' -not -path '*/__pycache__/*' \
           -not -path './tools/.venv/*' | sort)
[ "$COUNT" -eq 0 ] && echo "  (no .py files yet)"
find . -name '__pycache__' -type d -not -path './.git/*' -not -path './tools/.venv/*' \
     -exec rm -rf {} + 2>/dev/null

# ---------------------------------------------------------------------------
# 2b. turtle / tkinter examples - actually RUN them
# ---------------------------------------------------------------------------
note "turtle / tkinter (run to completion, blocking calls neutralised)"
if ! python3 tools/check_turtle.py; then
  FAILED=$((FAILED+1))
fi

# ---------------------------------------------------------------------------
# 2bb. pygame examples - actually RUN them, with SDL's dummy drivers
# ---------------------------------------------------------------------------
note "pygame (run headlessly)"
if ! python3 tools/check_pygame.py; then
  FAILED=$((FAILED+1))
fi

# ---------------------------------------------------------------------------
# 2c. logic tests (any test_*.py in the repo)
# ---------------------------------------------------------------------------
note "Logic tests"
FOUND_TESTS=0
while IFS= read -r f; do
  FOUND_TESTS=1
  if OUT=$(python3 "$f" 2>&1); then
    good "${f#./}"
  else
    bad "${f#./}"
    printf '        %s\n' "$OUT" | tail -8
  fi
done < <(find . -name 'test_*.py' -not -path './.git/*' -not -path '*/__pycache__/*' \
           -not -path './tools/.venv/*' | sort)
[ "$FOUND_TESTS" -eq 0 ] && echo "  (no test_*.py files yet)"

# ---------------------------------------------------------------------------
# 3-5. pages and links (JS syntax, Chrome load, relative links)
# ---------------------------------------------------------------------------
if ! node tools/check_pages.js $QUICK; then
  FAILED=$((FAILED+1))
fi

# ---------------------------------------------------------------------------
# 6. a few repo-wide conventions from docs/COURSE_SPEC.md
# ---------------------------------------------------------------------------
note "Conventions"

# No CDN script tags anywhere: a lesson must not fail when the Wi-Fi is down.
# --exclude-dir keeps tools/.venv out of this: pygame ships its own HTML docs,
# which do use CDN script tags, and they are not course content.
if CDN=$(grep -rlE '<script[^>]+src="https?://' --include='*.html' \
           --exclude-dir=.venv --exclude-dir=node_modules . 2>/dev/null); then
  if [ -n "$CDN" ]; then
    bad "external <script src> found - lessons must work offline:"
    printf '        %s\n' "$CDN"
  else
    good "no external script tags (lessons work offline)"
  fi
else
  good "no external script tags (lessons work offline)"
fi

# COURSE_SPEC rule 8.3: never belittle the reader.
# COURSE_SPEC rule 8.3 bans belittling the READER'S TASK - "simply add a
# line", "it's easy", "obviously". It does NOT ban "simply" meaning "merely"
# ("simply do not call it"), so the pattern targets the instructing forms only.
BELITTLE=$(grep -rniE \
  '\b(simply|just) (add|type|write|change|put|use|call|set|make|do|create|open)\b|\bobviously\b|\btrivially\b|\bit.?s easy\b|\ball you have to do\b|\bof course,? (you|just|simply)\b' \
  --include='*.md' docs/ webgames/ games_with_py/ games_with_cpp/ 2>/dev/null \
  | grep -viE 'COURSE_SPEC|AUTHORING_GUIDE|CLAUDE' || true)
if [ -n "$BELITTLE" ]; then
  printf '  %snote%s  wording to reconsider (COURSE_SPEC rule 8.3):\n' "$BOLD" "$OFF"
  printf '        %s\n' "$BELITTLE" | head -8
else
  good "no belittling wording found"
fi

# ---------------------------------------------------------------------------
printf '\n%s\n' "$(printf '=%.0s' {1..62})"
if [ "$FAILED" -eq 0 ]; then
  printf '%sALL CHECKS PASSED%s\n' "$GREEN" "$OFF"
  [ -n "$QUICK" ] && printf 'Note: --quick skipped the Chrome pass.\n'
  exit 0
else
  printf '%s%d CHECK GROUP(S) FAILED%s\n' "$RED" "$FAILED" "$OFF"
  exit 1
fi
