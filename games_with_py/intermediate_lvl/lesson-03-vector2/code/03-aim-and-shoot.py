"""
03-aim-and-shoot.py — any direction at all.

WHAT THIS DEMONSTRATES
    * an angle is one number that changes a little each frame
    * Vector2(1, 0).rotate(angle) turns that number into a direction - in DEGREES,
      clockwise on screen
    * bullets leave along the nose: pos = copy of ship, vel = nose * SPEED
    * pygame.transform.rotate goes the OTHER way, which is why the sprite is drawn
      with -angle. Press F to drop the minus and see the ship point 90 degrees off.

HOW TO RUN IT
    python3 03-aim-and-shoot.py
      LEFT / RIGHT  turn        UP  thrust        SPACE  fire
      F  remove the minus sign in transform.rotate (the classic bug)
      R  new rocks

WHAT TO CHANGE FIRST
    Press F. The ship still FLIES correctly - only the picture is wrong. That split
    between where a thing goes and where it looks is worth noticing, because it
    tells you which half of the code to go and read.
"""

import os
import random
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 760, 480
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

TURN_SPEED = 200          # DEGREES per second
THRUST = 240              # pixels per second while UP is held
BULLET_SPEED = 430
BULLET_LIFE = 1.3
FIRE_GAP = 0.16

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - aim and shoot")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 28)


def make_ship(size=34):
    """Drawn pointing RIGHT, because angle 0 points right. Drawing it pointing up
    is the other way people end up 90 degrees out."""
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(s, (77, 171, 247),
                        [(size - 2, size / 2), (2, size - 4),
                         (size * 0.35, size / 2), (2, 4)], 0)
    return s


SHIP_IMAGE = make_ship()

ship_pos = Vector2(WIDTH / 2, HEIGHT / 2)
ship_angle = -90.0        # -90 degrees = pointing UP, because 0 points right
bullets = []
rocks = []
fire_cooldown = 0.0
score = 0
flip_sign = True          # the correct behaviour; F turns it off
frames = 0


def new_rocks(count=7):
    out = []
    for i in range(count):
        # a random ANGLE plus a random speed gives an even spread of directions.
        # Random x and y speeds would cluster them on the diagonals.
        heading = random.uniform(0, 360)
        out.append({
            "pos": Vector2(random.uniform(40, WIDTH - 40), random.uniform(40, HEIGHT - 40)),
            "vel": Vector2(1, 0).rotate(heading) * random.uniform(30, 80),
            "r": random.uniform(16, 30),
            "spin": random.uniform(-90, 90),
            "turn": 0.0,
        })
    return out


rocks = new_rocks()


def wrap(v):
    if v.x < -20:
        v.x = WIDTH + 20
    if v.x > WIDTH + 20:
        v.x = -20
    if v.y < -20:
        v.y = HEIGHT + 20
    if v.y > HEIGHT + 20:
        v.y = -20


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f:
                flip_sign = not flip_sign
            elif event.key == pygame.K_r:
                rocks = new_rocks()
                score = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_angle -= TURN_SPEED * dt
    if keys[pygame.K_RIGHT]:
        ship_angle += TURN_SPEED * dt

    # The nose: a UNIT vector built by rotating "right" by the ship's angle.
    nose = Vector2(1, 0).rotate(ship_angle)

    if keys[pygame.K_UP]:
        ship_pos += nose * THRUST * dt
    wrap(ship_pos)

    fire_cooldown -= dt
    if keys[pygame.K_SPACE] and fire_cooldown <= 0:
        fire_cooldown = FIRE_GAP
        bullets.append({
            # Vector2(...) COPIES. Without it the bullet would drag the ship.
            "pos": Vector2(ship_pos) + nose * 18,
            "vel": nose * BULLET_SPEED,
            "life": BULLET_LIFE,
        })

    for b in bullets:
        b["pos"] += b["vel"] * dt
        b["life"] -= dt
        wrap(b["pos"])
    bullets = [b for b in bullets if b["life"] > 0]

    for r in rocks:
        r["pos"] += r["vel"] * dt
        r["turn"] += r["spin"] * dt
        wrap(r["pos"])

    # hits, with no square root
    surviving = []
    for r in rocks:
        hit = False
        for b in list(bullets):
            if (r["pos"] - b["pos"]).length_squared() < r["r"] * r["r"]:
                bullets.remove(b)
                hit = True
                score += 10
                break
        if not hit:
            surviving.append(r)
    rocks = surviving

    # ---- render -----------------------------------------------------------
    screen.fill((10, 13, 19))

    for r in rocks:
        points = []
        for k in range(7):
            wobble = r["r"] * (1.0 if k % 2 == 0 else 0.76)
            points.append(r["pos"] + Vector2(1, 0).rotate(r["turn"] + k * 360 / 7) * wobble)
        pygame.draw.polygon(screen, (122, 134, 152), points, 2)

    for b in bullets:
        pygame.draw.circle(screen, (255, 212, 59), b["pos"], 3)

    # the nose direction, drawn, so the maths is visible before it is trusted
    pygame.draw.line(screen, (43, 138, 62), ship_pos, ship_pos + nose * 70, 1)

    # transform.rotate turns ANTICLOCKWISE; Vector2.rotate turns clockwise on
    # screen. Hence the minus. Press F to see what happens without it.
    draw_angle = -ship_angle if flip_sign else ship_angle
    image = pygame.transform.rotate(SHIP_IMAGE, draw_angle)
    rect = image.get_rect(center=ship_pos)     # it grew: re-centre it
    screen.blit(image, rect)

    screen.blit(big.render("SCORE %d" % score, True, (231, 236, 243)), (16, 14))
    info = [
        "angle      %6.1f deg" % (ship_angle % 360),
        "nose       (%.2f, %.2f)" % (nose.x, nose.y),
        "nose len   %.3f   <- always 1" % nose.length(),
        "rocks      %d" % len(rocks),
    ]
    for i, line in enumerate(info):
        screen.blit(font.render(line, True, (135, 147, 164)), (16, 48 + i * 20))

    if not flip_sign:
        screen.blit(font.render("F: drawing with +angle - the ship flies correctly "
                                "and points the wrong way",
                                True, (255, 107, 107)), (16, HEIGHT - 26))
    if not rocks:
        screen.blit(big.render("all clear - press R", True, (81, 207, 102)),
                    (WIDTH / 2 - 110, HEIGHT / 2))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
