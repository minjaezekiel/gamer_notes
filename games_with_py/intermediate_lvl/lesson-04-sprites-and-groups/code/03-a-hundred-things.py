"""
03-a-hundred-things.py — where your machine stops coping, measured.

WHAT THIS DEMONSTRATES
    pygame's Group is convenient. It is not magic. spritecollide is a plain loop,
    so bullets against enemies costs len(a) x len(b) rectangle tests.

    This page runs the same simulation two ways - a Group and a plain list - and
    times update, draw and collision SEPARATELY, reporting the average and the
    worst of the last two seconds. Then it tells you which of the three is actually
    costing you, which is almost never the one people guess.

HOW TO RUN IT
    python3 03-a-hundred-things.py
      UP / DOWN   change the sprite count (100 ... 5000)
      SPACE       switch between Group and a plain list
      C           turn collision on and off
      R           reset the measurements

WHAT TO CHANGE FIRST
    Nothing, at first. Raise the count until "worst" passes 16.7 ms and write that
    number down - it is your machine's answer, and it is not the same as anybody
    else's. Then press C and raise it again: without collision you will get several
    times further, which tells you where the cost really was.
"""

import os
import random
import time
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 780, 500
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

COUNTS = [100, 250, 500, 1000, 2000, 3500, 5000]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - a hundred things")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

DOT = pygame.Surface((6, 6), pygame.SRCALPHA)
pygame.draw.circle(DOT, (77, 171, 247), (3, 3), 3)
TARGET = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.circle(TARGET, (255, 107, 107), (5, 5), 5)


class Mover(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=(random.uniform(0, WIDTH),
                                           random.uniform(40, HEIGHT - 90)))
        self.pos = Vector2(self.rect.center)
        self.vel = Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(40, 160)

    def update(self, dt):
        self.pos += self.vel * dt
        if self.pos.x < 0 or self.pos.x > WIDTH:
            self.vel.x = -self.vel.x
        if self.pos.y < 40 or self.pos.y > HEIGHT - 90:
            self.vel.y = -self.vel.y
        self.rect.center = self.pos


count_index = 2
use_group = True
do_collision = True

movers_group = pygame.sprite.Group()
targets_group = pygame.sprite.Group()
movers_list = []
targets_list = []

samples = {"update": [], "draw": [], "collide": [], "frame": []}
worst = {"update": 0.0, "draw": 0.0, "collide": 0.0, "frame": 0.0}


def record(name, ms):
    s = samples[name]
    s.append(ms)
    if len(s) > 120:
        s.pop(0)
    if ms > worst[name]:
        worst[name] = ms


def reset_measurements():
    for k in samples:
        samples[k].clear()
        worst[k] = 0.0


def rebuild():
    n = COUNTS[count_index]
    movers_group.empty()
    targets_group.empty()
    movers_list.clear()
    targets_list.clear()
    for _ in range(n):
        m = Mover(DOT)
        movers_group.add(m)
        movers_list.append(m)
    for _ in range(max(8, n // 20)):
        t = Mover(TARGET)
        targets_group.add(t)
        targets_list.append(t)
    reset_measurements()


rebuild()
frames = 0

running = True
while running:
    frame_start = time.perf_counter()
    dt = clock.tick(0) / 1000.0        # tick(0) = no cap: measure the real cost
    dt = min(dt, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                count_index = min(len(COUNTS) - 1, count_index + 1)
                rebuild()
            elif event.key == pygame.K_DOWN:
                count_index = max(0, count_index - 1)
                rebuild()
            elif event.key == pygame.K_SPACE:
                use_group = not use_group
                reset_measurements()
            elif event.key == pygame.K_c:
                do_collision = not do_collision
                reset_measurements()
            elif event.key == pygame.K_r:
                reset_measurements()

    # ---- UPDATE, timed ----------------------------------------------------
    t0 = time.perf_counter()
    if use_group:
        movers_group.update(dt)
        targets_group.update(dt)
    else:
        for m in movers_list:
            m.update(dt)
        for t in targets_list:
            t.update(dt)
    record("update", (time.perf_counter() - t0) * 1000)

    # ---- COLLISION, timed -------------------------------------------------
    hits = 0
    t0 = time.perf_counter()
    if do_collision:
        if use_group:
            # a plain loop inside: len(movers) x len(targets) rect tests
            found = pygame.sprite.groupcollide(movers_group, targets_group, False, False)
            hits = len(found)
        else:
            for m in movers_list:
                for t in targets_list:
                    if m.rect.colliderect(t.rect):
                        hits += 1
                        break
    record("collide", (time.perf_counter() - t0) * 1000)

    # ---- DRAW, timed ------------------------------------------------------
    screen.fill((16, 20, 27))
    t0 = time.perf_counter()
    if use_group:
        movers_group.draw(screen)
        targets_group.draw(screen)
    else:
        for m in movers_list:
            screen.blit(m.image, m.rect)
        for t in targets_list:
            screen.blit(t.image, t.rect)
    record("draw", (time.perf_counter() - t0) * 1000)

    # ---- the readout ------------------------------------------------------
    n = COUNTS[count_index]
    targets = len(targets_list)
    panel = pygame.Surface((420, 150), pygame.SRCALPHA)
    panel.fill((10, 13, 18, 235))
    screen.blit(panel, (14, HEIGHT - 164))
    pygame.draw.rect(screen, (43, 50, 64), (14, HEIGHT - 164, 420, 150), 1)

    def avg(name):
        s = samples[name]
        return sum(s) / len(s) if s else 0.0

    total_avg = avg("update") + avg("draw") + avg("collide")
    lines = [
        ("mode", "Group" if use_group else "plain list", (255, 212, 59)),
        ("sprites", "%d movers x %d targets" % (n, targets), (135, 147, 164)),
        ("rect tests/frame", "%s" % format(n * targets if do_collision else 0, ","),
         (255, 107, 107) if do_collision and n * targets > 100000 else (135, 147, 164)),
        ("update", "%6.2f ms   worst %6.2f" % (avg("update"), worst["update"]),
         (135, 147, 164)),
        ("draw", "%6.2f ms   worst %6.2f" % (avg("draw"), worst["draw"]),
         (135, 147, 164)),
        ("collide", "%6.2f ms   worst %6.2f" % (avg("collide"), worst["collide"]),
         (255, 107, 107) if avg("collide") > 8 else (135, 147, 164)),
        ("total", "%6.2f ms   (a frame has 16.7)" % total_avg,
         (255, 107, 107) if total_avg > 16.7 else (81, 207, 102)),
    ]
    for i, (label, value, colour) in enumerate(lines):
        screen.blit(font.render(label, True, (100, 112, 130)), (26, HEIGHT - 150 + i * 20))
        screen.blit(font.render(value, True, colour), (170, HEIGHT - 150 + i * 20))

    screen.blit(big.render("%.0f fps" % clock.get_fps(), True, (231, 236, 243)), (18, 14))
    help_lines = [
        "UP / DOWN  sprite count",
        "SPACE      Group or plain list",
        "C          collision %s" % ("on" if do_collision else "OFF"),
        "R          reset measurements",
    ]
    for i, line in enumerate(help_lines):
        screen.blit(font.render(line, True, (100, 112, 130)), (WIDTH - 250, 18 + i * 20))

    # which of the three is actually costing you?
    worst_part = max(("update", avg("update")), ("draw", avg("draw")),
                     ("collide", avg("collide")), key=lambda p: p[1])
    screen.blit(font.render("most expensive right now: %s" % worst_part[0],
                            True, (255, 212, 59)), (WIDTH - 250, 110))

    pygame.display.flip()

    record("frame", (time.perf_counter() - frame_start) * 1000)
    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
