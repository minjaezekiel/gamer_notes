"""
02-the-aliasing-trap.py — the bug whose symptom is in a different file.

WHAT THIS DEMONSTRATES
    Vector2 is MUTABLE, and `+=` changes the object in place rather than making a
    new one. So this:

        bullet.pos = ship.pos          # NOT a copy - one object, two names
        bullet.pos += velocity * dt    # ...and now the SHIP has moved

    Press 1 to fire a correctly-copied bullet. Press 2 to fire an aliased one and
    watch the ship get dragged across the screen by its own bullet.

    The readout shows id() for both, which is how you diagnose this for real: the
    same number means one object.

HOW TO RUN IT
    python3 02-the-aliasing-trap.py
      1  fire a bullet with Vector2(ship.pos)   - correct
      2  fire a bullet with ship.pos            - aliased
      R  put the ship back

WHAT TO CHANGE FIRST
    Nothing. Press 2 and watch. Then look at the two id() numbers and notice they
    are identical - that is the whole diagnosis, and it takes five seconds once you
    know to look.
"""

import os
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 760, 430
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - the aliasing trap")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 26)

ship_start = Vector2(140, HEIGHT / 2)
ship_pos = Vector2(ship_start)
bullets = []          # each: {"pos": Vector2, "vel": Vector2, "aliased": bool}
last_fire = ""
frames = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                # CORRECT: a copy. The bullet gets its own object.
                bullets.append({"pos": Vector2(ship_pos),
                                "vel": Vector2(320, 0), "aliased": False})
                last_fire = "fired with Vector2(ship_pos)  - a copy"
            elif event.key == pygame.K_2:
                # THE BUG: an alias. The bullet's position IS the ship's.
                bullets.append({"pos": ship_pos,
                                "vel": Vector2(320, 0), "aliased": True})
                last_fire = "fired with ship_pos  - the same object"
            elif event.key == pygame.K_r:
                ship_pos = Vector2(ship_start)
                bullets.clear()
                last_fire = "ship reset"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ship_pos.y -= 220 * dt
    if keys[pygame.K_DOWN]:
        ship_pos.y += 220 * dt

    for b in bullets:
        # `+=` MUTATES the object. If that object is also the ship's position,
        # this line moves the ship.
        b["pos"] += b["vel"] * dt

    bullets = [b for b in bullets if b["pos"].x < WIDTH + 40]

    screen.fill((20, 24, 32))

    pygame.draw.polygon(screen, (77, 171, 247),
                        [(ship_pos.x + 20, ship_pos.y),
                         (ship_pos.x - 14, ship_pos.y + 12),
                         (ship_pos.x - 14, ship_pos.y - 12)])
    for b in bullets:
        colour = (255, 107, 107) if b["aliased"] else (255, 212, 59)
        pygame.draw.circle(screen, colour, b["pos"], 5)

    screen.blit(big.render("press 1 (copy) or 2 (alias)", True, (231, 236, 243)), (20, 20))
    screen.blit(font.render("up / down move the ship", True, (135, 147, 164)), (20, 50))

    y = HEIGHT - 120
    screen.blit(font.render(last_fire, True, (255, 212, 59)), (20, y))
    screen.blit(font.render("ship_pos        %s   id %d" %
                            ("(%.0f, %.0f)" % (ship_pos.x, ship_pos.y), id(ship_pos)),
                            True, (77, 171, 247)), (20, y + 24))
    if bullets:
        b = bullets[-1]
        same = id(b["pos"]) == id(ship_pos)
        screen.blit(font.render("newest bullet   %s   id %d" %
                                ("(%.0f, %.0f)" % (b["pos"].x, b["pos"].y), id(b["pos"])),
                                True, (255, 107, 107) if same else (81, 207, 102)),
                    (20, y + 46))
        screen.blit(font.render("same object?    %s" % ("YES - this is the bug" if same else "no"),
                                True, (255, 107, 107) if same else (81, 207, 102)),
                    (20, y + 68))
    else:
        screen.blit(font.render("no bullets yet", True, (74, 83, 98)), (20, y + 46))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
