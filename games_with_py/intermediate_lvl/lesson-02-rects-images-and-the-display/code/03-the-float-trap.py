"""
03-the-float-trap.py — one square moves, the other does not, and the code is the
same speed.

WHAT THIS DEMONSTRATES
    pygame's Rect holds INTEGERS. Assign 10.7 to rect.x and it becomes 10.

    The red square stores its position in the Rect, so at 30 px/s and 60 fps it
    tries to move 0.5 px per frame - which truncates to 0, every single frame. It
    never moves at all.

    The blue square keeps the real position in a float and copies a rounded value
    into the Rect for drawing. It moves correctly.

    Both have SPEED = 30. Use the slider keys to raise the speed and watch the red
    square suddenly start working above 60 px/s, which is what makes this bug so
    confusing: it only appears when things move SLOWLY.

HOW TO RUN IT
    python3 03-the-float-trap.py
      UP / DOWN   change the speed
      R           reset both to the left

WHAT TO CHANGE FIRST
    Set the speed to 61 and watch the red square start to work. Then set it to 59
    and watch it stop. Nothing about the code changed.
"""

import os
import pygame

WIDTH, HEIGHT = 700, 400
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - the float trap")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 21)
big = pygame.font.SysFont(None, 26)

START_X = 40
speed = 30.0

# The broken one: its position IS the rect.
bad_rect = pygame.Rect(START_X, 120, 40, 40)

# The correct one: a float is the truth, the rect is a copy for drawing.
good_x = float(START_X)
good_rect = pygame.Rect(START_X, 240, 40, 40)

elapsed = 0.0
frames = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                bad_rect.x = START_X
                good_x = float(START_X)
                elapsed = 0.0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speed = min(400.0, speed + 40 * dt)
    if keys[pygame.K_DOWN]:
        speed = max(1.0, speed - 40 * dt)

    # ---- the broken version ----------------------------------------------
    # rect.x is an int. 30 * (1/60) = 0.5, which truncates to 0. For ever.
    bad_rect.x += speed * dt

    # ---- the correct version ---------------------------------------------
    good_x += speed * dt                 # float: the truth
    good_rect.x = round(good_x)          # int: for drawing and colliding

    if bad_rect.x > WIDTH - 60:
        bad_rect.x = START_X
    if good_x > WIDTH - 60:
        good_x = float(START_X)

    # ---- render -----------------------------------------------------------
    screen.fill((20, 24, 32))

    per_frame = speed * dt
    screen.blit(big.render("both squares have SPEED = %.0f px/s" % speed,
                           True, (231, 236, 243)), (20, 20))
    screen.blit(font.render("%.3f px per frame at %.0f fps" % (per_frame, clock.get_fps()),
                            True, (135, 147, 164)), (20, 48))

    pygame.draw.rect(screen, (255, 107, 107), bad_rect)
    pygame.draw.rect(screen, (77, 171, 247), good_rect)

    screen.blit(font.render("rect.x += SPEED * dt", True, (255, 107, 107)), (20, 92))
    screen.blit(font.render("rect.x = %4d   (travelled %d px)" %
                            (bad_rect.x, bad_rect.x - START_X),
                            True, (255, 107, 107)), (260, 92))

    screen.blit(font.render("self.x += SPEED * dt; rect.x = round(self.x)",
                            True, (77, 171, 247)), (20, 212))
    screen.blit(font.render("self.x = %7.2f   (travelled %d px)" %
                            (good_x, good_x - START_X),
                            True, (77, 171, 247)), (400, 212))

    note_y = HEIGHT - 70
    if per_frame < 1.0:
        screen.blit(font.render("%.3f px per frame truncates to 0: the red square "
                                "cannot move at all" % per_frame,
                                True, (255, 107, 107)), (20, note_y))
        screen.blit(font.render("hold UP until it passes 1.0 px per frame",
                                True, (255, 212, 59)), (20, note_y + 22))
    else:
        screen.blit(font.render("above 1 px per frame the red square works - which is "
                                "why this bug hides", True, (81, 207, 102)), (20, note_y))
        screen.blit(font.render("hold DOWN to go back under 1.0 and watch it stop",
                                True, (255, 212, 59)), (20, note_y + 22))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
