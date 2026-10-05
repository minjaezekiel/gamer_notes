"""
01-vector-basics.py — every Vector2 method, on two vectors you drag.

WHAT THIS DEMONSTRATES
    The picture and the numbers, moving together. Drag the red and blue tips and
    watch length, normalize, dot, angle_to, lerp and the rest update live.

    Drag both tips to the same place and the normalise row turns red: that is the
    ValueError this lesson is really about, caught and reported rather than
    allowed to end the program.

HOW TO RUN IT
    python3 01-vector-basics.py
      drag the red or blue tip with the mouse
      G  switch the zero-length guard off (then overlap the tips)

WHAT TO CHANGE FIRST
    Drag the red tip until its length reads exactly 50 with whole-number parts.
    There are several: (30,40), (40,30), (50,0), (14,48). Then check the normalised
    version really does have length 1 every time.
"""

import os
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 780, 470
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - Vector2 basics")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 25)

ORIGIN = Vector2(210, 300)
UNIT_DRAW = 60                   # a length-1 arrow would be invisible

red = Vector2(130, -100)         # stored as OFFSETS from the origin
blue = Vector2(70, 80)
dragging = None
guard = True
frames = 0


def arrow(surface, start, end, colour, width=3):
    """A line with a head. Uses Vector2 for the head, which is the point."""
    d = end - start
    if d.length_squared() < 1:
        return
    direction = d.normalize()
    back = end - direction * 13
    # "sideways" without any trigonometry: swap the parts and negate one
    side = Vector2(-direction.y, direction.x)
    pygame.draw.line(surface, colour, start, back, width)
    pygame.draw.polygon(surface, colour,
                        [end, back + side * 6, back - side * 6])


def row(label, value, y, colour=(231, 236, 243)):
    screen.blit(font.render(label, True, (135, 147, 164)), (430, y))
    screen.blit(font.render(value, True, colour), (610, y))


running = True
while running:
    dt = clock.tick(60) / 1000.0
    mouse = Vector2(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_g:
                guard = not guard
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (mouse - (ORIGIN + red)).length() < 18:
                dragging = "red"
            elif (mouse - (ORIGIN + blue)).length() < 18:
                dragging = "blue"
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    if dragging == "red":
        red = mouse - ORIGIN          # a NEW vector: subtraction does not mutate
    elif dragging == "blue":
        blue = mouse - ORIGIN

    # ---- the numbers ------------------------------------------------------
    total = red + blue
    red_len = red.length()
    blue_len = blue.length()

    unit_red = None
    unit_blue = None
    normalise_error = ""
    try:
        if guard and red.length_squared() == 0:
            raise ValueError("Can't normalize Vector of length zero")
        unit_red = red.normalize()
    except ValueError as err:
        normalise_error = str(err)
    try:
        if guard and blue.length_squared() == 0:
            raise ValueError("Can't normalize Vector of length zero")
        unit_blue = blue.normalize()
    except ValueError as err:
        normalise_error = str(err)

    dot = unit_red.dot(unit_blue) if (unit_red and unit_blue) else None

    # ---- render -----------------------------------------------------------
    screen.fill((20, 24, 32))

    pygame.draw.line(screen, (34, 40, 52), (0, ORIGIN.y), (410, ORIGIN.y))
    pygame.draw.line(screen, (34, 40, 52), (ORIGIN.x, 40), (ORIGIN.x, HEIGHT))

    # head-to-tail addition
    arrow(screen, ORIGIN + red, ORIGIN + total, (85, 95, 110), 2)
    arrow(screen, ORIGIN, ORIGIN + total, (81, 207, 102), 3)
    arrow(screen, ORIGIN, ORIGIN + red, (255, 107, 107), 3)
    arrow(screen, ORIGIN, ORIGIN + blue, (77, 171, 247), 3)
    if unit_red is not None:
        arrow(screen, ORIGIN, ORIGIN + unit_red * UNIT_DRAW, (255, 212, 59), 2)

    for vec, colour in ((red, (255, 107, 107)), (blue, (77, 171, 247))):
        pygame.draw.circle(screen, colour, ORIGIN + vec, 9)

    screen.blit(big.render("THE NUMBERS", True, (231, 236, 243)), (430, 44))
    row("red", "(%.0f, %.0f)" % (red.x, red.y), 76, (255, 107, 107))
    row("red.length()", "%.2f" % red_len, 98, (255, 107, 107))
    row("red.length_squared()", "%.0f" % red.length_squared(), 120, (255, 107, 107))
    if unit_red is not None:
        row("red.normalize()", "(%.2f, %.2f)" % (unit_red.x, unit_red.y), 142, (255, 212, 59))
        row("  its length", "%.3f" % unit_red.length(), 164, (255, 212, 59))
    else:
        row("red.normalize()", "ValueError", 142, (255, 107, 107))
        row("", normalise_error[:28], 164, (255, 107, 107))

    row("blue", "(%.0f, %.0f)" % (blue.x, blue.y), 196, (77, 171, 247))
    row("blue.length()", "%.2f" % blue_len, 218, (77, 171, 247))

    row("red + blue", "(%.0f, %.0f)" % (total.x, total.y), 250, (81, 207, 102))
    row("red - blue", "(%.0f, %.0f)" % ((red - blue).x, (red - blue).y), 272)
    row("red.distance_to(blue)", "%.1f" % red.distance_to(blue), 294)
    row("red.angle_to(blue)", "%.1f deg" % red.angle_to(blue), 316)
    row("red.lerp(blue, 0.25)", "(%.0f, %.0f)" % (red.lerp(blue, 0.25).x,
                                                  red.lerp(blue, 0.25).y), 338)
    if dot is not None:
        row("unit dot unit", "%.3f" % dot, 360, (255, 212, 59))
        if dot > 0.9:
            meaning = "pointing nearly the SAME way"
        elif dot > 0.25:
            meaning = "roughly the same way"
        elif dot > -0.25:
            meaning = "close to RIGHT ANGLES"
        elif dot > -0.9:
            meaning = "roughly opposite"
        else:
            meaning = "nearly OPPOSITE"
        screen.blit(font.render(meaning, True, (169, 180, 196)), (430, 382))

    screen.blit(font.render("guard (G)  %s" % ("on" if guard else "OFF"),
                            True, (81, 207, 102) if guard else (255, 107, 107)),
                (430, 414))
    screen.blit(font.render("rotate() is in DEGREES, clockwise on screen",
                            True, (74, 83, 98)), (430, 436))

    screen.blit(font.render("drag the red or blue tip", True, (74, 83, 98)), (20, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
