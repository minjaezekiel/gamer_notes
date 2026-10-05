"""
03-delta-time.py — the same intended speed, two ways, at a frame rate you control.

WHAT THIS DEMONSTRATES
    The blue square multiplies by dt. The red one adds a fixed amount per frame.
    Both are "supposed" to travel 240 pixels a second. Press 1, 2, 3 to change the
    frame cap and watch what each one actually does.

    The MEASURED speed of each square is on screen - worked out from how far it
    really moved, not from what we intended.

HOW TO RUN IT
    python3 03-delta-time.py
      1  cap at 60 fps      2  cap at 30 fps      3  cap at 10 fps
      R  put both back at the start

WHAT TO CHANGE FIRST
    Nothing, the first time. Press 3 and watch the red square crawl. Then ask
    yourself which of the two you would rather ship to somebody whose computer you
    have never seen.
"""

import os
import pygame

WIDTH, HEIGHT = 700, 360
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

INTENDED_SPEED = 240          # pixels per second, for both squares
PER_FRAME_STEP = 4            # pixels per FRAME: right only at exactly 60 fps

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - delta time")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 21)
big = pygame.font.SysFont(None, 26)

START_X = 40
good_x = START_X              # multiplied by dt
bad_x = START_X               # a fixed step per frame
good_measured = 0.0
bad_measured = 0.0
frame_cap = 60
elapsed = 0.0
frames = 0

running = True
while running:
    dt = clock.tick(frame_cap) / 1000.0
    elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                frame_cap = 60
            elif event.key == pygame.K_2:
                frame_cap = 30
            elif event.key == pygame.K_3:
                frame_cap = 10
            elif event.key == pygame.K_r:
                good_x = bad_x = START_X
                elapsed = 0.0

    before_good, before_bad = good_x, bad_x

    # ---- the two versions -------------------------------------------------
    good_x += INTENDED_SPEED * dt      # pixels per SECOND, scaled by the frame
    bad_x += PER_FRAME_STEP            # pixels per FRAME, whatever a frame is

    # measure what actually happened, rather than trusting what we meant
    if dt > 0:
        good_measured = (good_x - before_good) / dt
        bad_measured = (bad_x - before_bad) / dt

    for value in (good_x, bad_x):
        pass
    if good_x > WIDTH - 60:
        good_x = START_X
    if bad_x > WIDTH - 60:
        bad_x = START_X

    # ---- render -----------------------------------------------------------
    screen.fill((20, 24, 32))

    screen.blit(big.render("both are meant to travel %d px per second" % INTENDED_SPEED,
                           True, (231, 236, 243)), (20, 18))

    pygame.draw.line(screen, (40, 48, 60), (START_X, 120), (WIDTH - 20, 120), 2)
    pygame.draw.line(screen, (40, 48, 60), (START_X, 220), (WIDTH - 20, 220), 2)

    pygame.draw.rect(screen, (77, 171, 247), (good_x, 96, 40, 40))
    pygame.draw.rect(screen, (255, 107, 107), (bad_x, 196, 40, 40))

    screen.blit(font.render("x += SPEED * dt", True, (77, 171, 247)), (20, 70))
    screen.blit(font.render("measured %4.0f px/s" % good_measured,
                            True, (77, 171, 247)), (220, 70))

    screen.blit(font.render("x += 4   (per frame)", True, (255, 107, 107)), (20, 170))
    bad_colour = (255, 107, 107) if abs(bad_measured - INTENDED_SPEED) > 20 else (81, 207, 102)
    screen.blit(font.render("measured %4.0f px/s" % bad_measured, True, bad_colour), (220, 170))

    screen.blit(font.render("frame cap  %d   (press 1, 2, 3)" % frame_cap,
                            True, (255, 212, 59)), (20, HEIGHT - 76))
    screen.blit(font.render("dt         %.4f s" % dt, True, (135, 147, 164)),
                (20, HEIGHT - 54))
    screen.blit(font.render("real fps   %.1f" % clock.get_fps(), True, (135, 147, 164)),
                (20, HEIGHT - 32))

    if frame_cap != 60:
        screen.blit(font.render("the red square is now wrong by a factor of %.1f" %
                                (60.0 / frame_cap), True, (255, 107, 107)),
                    (300, HEIGHT - 54))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
