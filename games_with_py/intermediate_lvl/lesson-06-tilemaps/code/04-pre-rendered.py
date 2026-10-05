"""
04-pre-rendered.py — draw the level once, not three hundred times a frame.

WHAT THIS DEMONSTRATES
    Two ways of drawing a tilemap, timed on your machine:

      PER TILE     a draw call for every visible tile, every frame
      PRE-RENDERED the whole level blitted onto one Surface ONCE, at load time,
                   and then one blit per frame

    The millisecond figures are measured, not claimed. Press T to switch and watch
    them. Then press L to tile the level four times in each direction and see both
    numbers move - and read the memory estimate, which is why this does not scale
    for ever.

HOW TO RUN IT
    python3 04-pre-rendered.py
      T  switch method        L  make the level bigger        R  reset timings

WHAT TO CHANGE FIRST
    Press L twice and look at the "one Surface would be" figure. Then work out what
    it would be for a 500 x 500 tile level before you try it.
"""

import os
import time
import pygame
from tilemap import Tilemap, load_level, TILE

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 820, 560

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - pre-rendered")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

base_lines = load_level("level.txt")
repeat = 1
pre_rendered = None
level = None
use_pre_rendered = False
camera_x = camera_y = 0.0

samples = {"draw": []}
worst = {"draw": 0.0}


def build(times):
    """Tile the level `times` x `times` to make a bigger one, then pre-render it."""
    global level, pre_rendered
    wide = ["".join(row for _ in range(times)) for row in base_lines]
    tall = []
    for _ in range(times):
        tall.extend(wide)
    level = Tilemap(tall)
    # Pre-rendering: ONE Surface, drawn once, at load time.
    pre_rendered = level.pre_render()
    samples["draw"].clear()
    worst["draw"] = 0.0


build(repeat)
tiles_drawn = 0
frames = 0

running = True
while running:
    dt = clock.tick(0) / 1000.0        # no cap: we are measuring
    dt = min(dt, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_t:
                use_pre_rendered = not use_pre_rendered
                samples["draw"].clear()
                worst["draw"] = 0.0
            elif event.key == pygame.K_l:
                repeat = 1 if repeat >= 4 else repeat + 1
                build(repeat)
            elif event.key == pygame.K_r:
                samples["draw"].clear()
                worst["draw"] = 0.0

    keys = pygame.key.get_pressed()
    speed = 600
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera_x += speed * dt
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera_x -= speed * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        camera_y += speed * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        camera_y -= speed * dt
    camera_x = max(0, min(max(0, level.width - WIDTH), camera_x))
    camera_y = max(0, min(max(0, level.height - HEIGHT + 120), camera_y))

    screen.fill((18, 22, 30))

    t0 = time.perf_counter()
    if use_pre_rendered:
        # ONE blit. The level was drawn once, at load time.
        screen.blit(pre_rendered, (-round(camera_x), -round(camera_y)))
        tiles_drawn = 1
    else:
        tiles_drawn = level.draw(screen, round(camera_x), round(camera_y),
                                 WIDTH, HEIGHT - 120)
    elapsed = (time.perf_counter() - t0) * 1000
    samples["draw"].append(elapsed)
    if len(samples["draw"]) > 120:
        samples["draw"].pop(0)
    worst["draw"] = max(worst["draw"], elapsed)

    average = sum(samples["draw"]) / len(samples["draw"]) if samples["draw"] else 0.0
    surface_bytes = level.width * level.height * 4

    pygame.draw.rect(screen, (10, 13, 18), (0, HEIGHT - 120, WIDTH, 120))
    pygame.draw.rect(screen, (43, 50, 64), (0, HEIGHT - 120, WIDTH, 120), 1)

    screen.blit(big.render("PRE-RENDERED (one blit)" if use_pre_rendered
                           else "PER TILE (one call per visible tile)",
                           True, (81, 207, 102) if use_pre_rendered else (255, 212, 59)),
                (18, HEIGHT - 106))

    rows = [
        ("level", "%d x %d tiles  (%d total)"
         % (level.cols, level.rows, level.cols * level.rows)),
        ("draw calls this frame", "%d" % tiles_drawn),
        ("draw time", "%.3f ms   worst %.3f ms" % (average, worst["draw"])),
        ("one Surface would be", "%s bytes  (%.2f MB)"
         % (format(surface_bytes, ","), surface_bytes / 1_048_576)),
        ("fps", "%.0f" % clock.get_fps()),
    ]
    for i, (label, value) in enumerate(rows):
        screen.blit(font.render(label, True, (110, 122, 140)), (18, HEIGHT - 78 + i * 18))
        screen.blit(font.render(value, True, (231, 236, 243)), (210, HEIGHT - 78 + i * 18))

    screen.blit(font.render("T  switch    L  bigger level (x%d)    arrows scroll" % repeat,
                            True, (100, 112, 130)), (520, HEIGHT - 78))
    screen.blit(font.render("a 500 x 500 level at 32 px would need about 1 GB",
                            True, (100, 112, 130)), (520, HEIGHT - 60))
    screen.blit(font.render("which is why chunking exists", True, (100, 112, 130)),
                (520, HEIGHT - 42))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
