"""
02-events-and-state.py — two different questions, both answered in one loop.

WHAT THIS DEMONSTRATES
    EVENTS  — "this happened, once."      pygame.event.get()
    STATE   — "this is true right now."   pygame.key.get_pressed()

    The left-hand column lists events as they arrive. The right-hand column shows
    which keys are held this instant. Hold a key down and watch: ONE KEYDOWN event
    appears, and the state stays true for as long as you hold it.

    Then look at the two counters at the bottom. One counts presses; the other
    counts frames-while-held. Movement wants the second. Firing a bullet wants the
    first.

HOW TO RUN IT
    python3 02-events-and-state.py

WHAT TO CHANGE FIRST
    Hold the space bar for two seconds and compare the two counters. Then imagine
    each one is a gun.
"""

import os
import pygame

WIDTH, HEIGHT = 720, 440
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

# A few of the key constants, so the display can name what it sees.
WATCHED = [
    (pygame.K_LEFT, "LEFT"), (pygame.K_RIGHT, "RIGHT"),
    (pygame.K_UP, "UP"), (pygame.K_DOWN, "DOWN"),
    (pygame.K_SPACE, "SPACE"), (pygame.K_a, "A"), (pygame.K_d, "D"),
    (pygame.K_LSHIFT, "LSHIFT"),
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - events and state")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 21)
big = pygame.font.SysFont(None, 26)

event_log = []          # the last few events, newest last
space_presses = 0       # counted from KEYDOWN events
space_frames = 0        # counted from get_pressed()
frames = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0

    # ---- EVENTS: things that happened since the last frame ---------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                space_presses += 1
            event_log.append("KEYDOWN   %s" % pygame.key.name(event.key))
        elif event.type == pygame.KEYUP:
            event_log.append("KEYUP     %s" % pygame.key.name(event.key))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event_log.append("MOUSEDOWN button %d" % event.button)
        elif event.type == pygame.MOUSEMOTION:
            # There are a LOT of these. Only log occasionally, or the list is
            # nothing but mouse movement - which is itself worth noticing.
            if frames % 20 == 0:
                event_log.append("MOUSEMOTION %s" % (event.pos,))
        if len(event_log) > 12:
            event_log.pop(0)

    # ---- STATE: what is true at this instant -----------------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        space_frames += 1

    # ---- RENDER ----------------------------------------------------------
    screen.fill((20, 24, 32))

    screen.blit(big.render("EVENTS  (things that happened)", True, (255, 212, 59)), (20, 18))
    for i, line in enumerate(event_log):
        screen.blit(font.render(line, True, (169, 180, 196)), (20, 52 + i * 21))
    if not event_log:
        screen.blit(font.render("press something", True, (74, 83, 98)), (20, 52))

    screen.blit(big.render("STATE  (what is true now)", True, (81, 207, 102)), (400, 18))
    for i, (key, name) in enumerate(WATCHED):
        held = keys[key]
        colour = (81, 207, 102) if held else (74, 83, 98)
        mark = "[x]" if held else "[ ]"
        screen.blit(font.render("%s %s" % (mark, name), True, colour), (400, 52 + i * 21))

    y = HEIGHT - 86
    screen.blit(big.render("hold SPACE and compare:", True, (231, 236, 243)), (20, y))
    screen.blit(font.render("KEYDOWN events (one per press)      %d" % space_presses,
                            True, (255, 212, 59)), (20, y + 30))
    screen.blit(font.render("frames while held (one per frame)   %d" % space_frames,
                            True, (81, 207, 102)), (20, y + 52))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
