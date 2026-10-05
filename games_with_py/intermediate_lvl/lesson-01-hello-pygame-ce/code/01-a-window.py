"""
01-a-window.py — the smallest pygame program that is not broken.

WHAT THIS DEMONSTRATES
    The loop, written out by you: input, update, render. Fourteen lines of real
    work, and every one of them is a decision the library used to make for you.

    It also contains a switch (press F) that STOPS DRAINING THE EVENT QUEUE, so
    you can watch your own window stop responding. That is worth doing once: the
    operating system cannot tell the difference between a program that ignores its
    events and a program that has crashed.

HOW TO RUN IT
    python3 01-a-window.py

    Escape or the window's close button quits.
    F  stop draining the event queue (the window freezes; close the terminal)
    T  drop the frame cap to 5 fps, so you can see `dt` grow

WHAT TO CHANGE FIRST
    Delete the `screen.fill(...)` line. The square leaves a trail, because a frame
    is "erase, then draw" and you have just removed the erase. That is the same bug
    the web track meets in its very first lesson.
"""

import os
import pygame

WIDTH, HEIGHT = 640, 420
BACKGROUND = (20, 24, 32)
SQUARE = (77, 171, 247)
SPEED = 260                      # pixels per SECOND, not per frame

# ---------------------------------------------------------------------------
# The self-test hook. Four lines, visible to you, and the only reason
# tools/check_pygame.py can run this file without a window or a person.
#   SDL_VIDEODRIVER=dummy SELFTEST_FRAMES=150 python3 01-a-window.py
# ---------------------------------------------------------------------------
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - a window")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

x = WIDTH / 2 - 20
y = HEIGHT / 2 - 20
direction = 1

frame_cap = 60
drain_events = True
frames = 0

running = True
while running:
    # -----------------------------------------------------------------------
    # dt: how long the last frame took, in SECONDS.
    # tick() WAITS (so the loop is capped) and RETURNS MILLISECONDS.
    # The / 1000.0 is not optional.
    # -----------------------------------------------------------------------
    dt = clock.tick(frame_cap) / 1000.0

    # ---- 1. INPUT ---------------------------------------------------------
    if drain_events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    # From here on the queue fills up and is never emptied. The
                    # window will stop responding within a second or two.
                    drain_events = False
                elif event.key == pygame.K_t:
                    frame_cap = 5 if frame_cap == 60 else 60

    # ---- 2. UPDATE --------------------------------------------------------
    x += SPEED * direction * dt
    if x < 0:
        x = 0
        direction = 1
    if x + 40 > WIDTH:
        x = WIDTH - 40
        direction = -1

    # ---- 3. RENDER --------------------------------------------------------
    screen.fill(BACKGROUND)                                   # erase
    pygame.draw.rect(screen, SQUARE, (x, y, 40, 40))          # draw
    lines = [
        "dt        %.4f s" % dt,
        "frame cap %d  (T)" % frame_cap,
        "fps       %.1f" % clock.get_fps(),
        "events    %s  (F)" % ("drained" if drain_events else "IGNORED"),
    ]
    for i, text in enumerate(lines):
        colour = (255, 107, 107) if (i == 3 and not drain_events) else (135, 147, 164)
        screen.blit(font.render(text, True, colour), (14, 14 + i * 20))
    if not drain_events:
        screen.blit(font.render("the window has stopped responding - close the terminal",
                                True, (255, 107, 107)), (14, HEIGHT - 28))
    pygame.display.flip()                                     # show it

    # ---- the self-test exit ----------------------------------------------
    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()        # always the last line
