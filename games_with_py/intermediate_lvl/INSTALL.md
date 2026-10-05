# Installing pygame-ce

**Read this before lesson 1.** It takes five minutes on a normal machine, and the rest of this page
exists for the machines that are not normal.

---

## The short version

```bash
python3 -m pip install pygame-ce
```

Then check it:

```bash
python3 -c "import pygame; print(pygame.version.ver)"
```

If that prints a version number, you are finished. Go to
[lesson 1](lesson-01-hello-pygame-ce/notes.md).

---

## `pygame` or `pygame-ce`?

There are two packages with almost the same name, and installing both into one Python causes
genuinely confusing problems, because they provide the same `import pygame`.

- **`pygame-ce`** — "community edition". Actively developed, more features, the same API. **This is
  the one this course uses.**
- **`pygame`** — the original. Still works; some newer functions are missing.

Your code says `import pygame` either way, so the lessons work with both. If something in a lesson is
missing on your machine, check which one you have:

```bash
python3 -c "import pygame; print(pygame.version.ver, pygame.IS_CE if hasattr(pygame, 'IS_CE') else 'not ce')"
```

**If you already have `pygame`**, remove it before installing `pygame-ce`:

```bash
python3 -m pip uninstall pygame
python3 -m pip install pygame-ce
```

---

## A virtual environment, and why you might want one

A **virtual environment** is a private copy of Python's package list, in a folder. Installing into it
cannot affect anything else on the machine, which matters on a shared or school computer.

```bash
python3 -m venv .venv            # make it (once)
```

Then activate it, every time you open a new terminal:

```bash
source .venv/bin/activate        # macOS and Linux
.venv\Scripts\activate           # Windows
```

You will know it worked because your prompt changes. Now:

```bash
pip install pygame-ce
```

To leave it: `deactivate`.

> **Why this course's own checker uses one.** `tools/check_pygame.py` looks for
> `tools/.venv/bin/python` first, so running the repository's checks never installs anything into your
> system Python. If you want to set that up:
>
> ```bash
> python3 -m venv tools/.venv
> tools/.venv/bin/pip install pygame-ce
> ```

---

## If `pip install` is blocked

This is common on school machines, and there are three things to try, in order.

**1. Install for just you, not the whole machine.**

```bash
python3 -m pip install --user pygame-ce
```

**2. Use a virtual environment** in your own documents folder, as above. This needs no special
permissions at all, because it is only a folder.

**3. If neither works**, you have a decision to make rather than a problem to solve. Tell your
teacher, and in the meantime:

- Everything in [`../beginner_lvl/`](../beginner_lvl/) needs no installation at all — it uses
  `turtle` and `tkinter`, which come with Python.
- The [`webgames/`](../../webgames/) track needs nothing but a browser.
- The concepts in this level are the same in both. A student who cannot install `pygame-ce` has not
  lost the course; they have lost one library.

**Do not** spend an hour fighting an IT policy. It is not a programming problem and you will not win.

---

## Error messages you may actually see

| Message | What it means | What to do |
|---|---|---|
| `No module named pygame` | not installed, or installed into a *different* Python | run `python3 -m pip install pygame-ce` using the **same** `python3` you run your game with |
| `No module named pip` | pip is missing from this Python | `python3 -m ensurepip --upgrade` |
| `error: externally-managed-environment` | a Linux Python that refuses system-wide installs on purpose | use a virtual environment. This is the message that most often sends people down a rabbit hole; the venv is the correct answer, not a workaround |
| `Defaulting to user installation` | a warning, not an error | ignore it |
| `pygame.error: No available video device` | there is no display — you are on a server, or over SSH | that is expected; see "running without a window" below |
| the window opens and immediately closes | your program reached the end | that is lesson 1's first exercise, not a bug |
| `AttributeError: module 'pygame' has no attribute '...'` | you probably have old `pygame`, not `pygame-ce` | check the version, then swap as above |

### "It says it installed but Python cannot find it"

Almost always two different Pythons. Check they match:

```bash
which python3
python3 -m pip --version
```

The path printed by the second command should sit inside the same installation as the first. If it
does not, use `python3 -m pip install ...` rather than plain `pip install ...` — the `python3 -m`
form guarantees you are installing into the Python you are about to run.

---

## Running without a window

You will not normally need this, and it is worth knowing because it is how this repository checks
itself. SDL — the library underneath pygame — can be told to draw to nothing at all:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 my_game.py
```

The program runs, every drawing call executes, and no window appears. That is the whole trick behind
`tools/check_pygame.py`, which runs every example in this level for 150 frames to prove that nothing
throws. On Windows, set the variables first:

```
set SDL_VIDEODRIVER=dummy
python my_game.py
```

Each example in this level checks one environment variable so that it can be run this way:

```python
# at the top
selftest = int(os.environ.get("SELFTEST_FRAMES", "0"))

# in the loop
frames += 1
if selftest and frames >= selftest:
    running = False
```

Four lines, visible to you, and the reason the whole level can be verified without anybody clicking
anything. A hidden hook would have been worse.

---

## What you do not need

- **No IDE.** Any editor. IDLE comes with Python and is fine.
- **No assets.** This course ships no images or sound files, and no lesson downloads any. Every
  sprite in this level is drawn in code onto a `Surface`, which is a genuinely useful technique and
  not a workaround — see lesson 5.
- **No internet, after the install.** Nothing here fetches anything at runtime.
