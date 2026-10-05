"""
01-load-a-level.py — a world from a text file.

WHAT THIS DEMONSTRATES
    Loading, validating and drawing a level, and the two conversions:
        col = int(x // TILE)     position -> column
        x   = col * TILE         column   -> position
    Move the mouse and watch both happen at once.

    Press B to load broken-level.txt, which has one short row. The loader reports
    which row and why, instead of crashing somewhere else later.

HOW TO RUN IT
    python3 01-load-a-level.py
      B  load the broken level        G  grid        R  reload the good one

WHAT TO CHANGE FIRST
    Open level.txt, change a '.' to a '#', save, and press R. Then delete one
    character from a row and press R again.
"""

import os
import pygame
from tilemap import Tilemap, load_level, LevelError, TILE, TILES

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 800, 560

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - load a level")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

MAP_X, MAP_Y = 20, 60
show_grid = True
error_text = ""
level = None


def try_load(name):
    global level, error_text
    try:
        level = Tilemap(load_level(name))
        error_text = ""
    except LevelError as err:
        error_text = str(err)
    except FileNotFoundError as err:
        error_text = "FileNotFoundError: %s" % err


try_load("level.txt")
frames = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_g:
                show_grid = not show_grid
            elif event.key == pygame.K_b:
                try_load("broken-level.txt")
            elif event.key == pygame.K_r:
                try_load("level.txt")

    screen.fill((18, 22, 30))

    if level is not None:
        surface = pygame.Surface((level.width, level.height), pygame.SRCALPHA)
        level.draw(surface, 0, 0, level.width, level.height)
        screen.blit(surface, (MAP_X, MAP_Y))

        if show_grid:
            for col in range(level.cols + 1):
                x = MAP_X + col * TILE
                pygame.draw.line(screen, (29, 36, 46), (x, MAP_Y),
                                 (x, MAP_Y + level.height))
            for row in range(level.rows + 1):
                y = MAP_Y + row * TILE
                pygame.draw.line(screen, (29, 36, 46), (MAP_X, y),
                                 (MAP_X + level.width, y))

        # ---- position -> square, for whatever is under the pointer ----
        wx = mouse[0] - MAP_X
        wy = mouse[1] - MAP_Y
        col = int(wx // TILE)
        row = int(wy // TILE)
        inside = 0 <= wx and 0 <= wy and col < level.cols and row < level.rows

        if inside:
            pygame.draw.rect(screen, (240, 140, 0),
                             (MAP_X + col * TILE, MAP_Y + row * TILE, TILE, TILE), 2)

        screen.blit(big.render("%d x %d tiles of %d px" % (level.cols, level.rows, TILE),
                               True, (231, 236, 243)), (MAP_X, 26))

        py = MAP_Y + level.height + 16
        if inside:
            ch = level.char_at(col, row)
            info = level.info(col, row)
            rows_out = [
                ("x, y", "%d, %d" % (wx, wy)),
                ("col = x // TILE", "%d" % col),
                ("row = y // TILE", "%d" % row),
                ("corner = col * TILE", "%d, %d" % (col * TILE, row * TILE)),
                ("x %% TILE (into it)", "%d, %d" % (wx % TILE, wy % TILE)),
                ("character", repr(ch)),
                ("solid", str(info["solid"])),
            ]
            for i, (label, value) in enumerate(rows_out):
                screen.blit(font.render(label, True, (110, 122, 140)),
                            (MAP_X, py + i * 19))
                screen.blit(font.render(value, True, (255, 212, 59)),
                            (MAP_X + 200, py + i * 19))
        else:
            screen.blit(font.render("move the mouse over the level",
                                    True, (100, 112, 130)), (MAP_X, py))

        screen.blit(font.render("tile types in the table: %d" % len(TILES),
                                True, (100, 112, 130)), (MAP_X + 380, py))
        screen.blit(font.render("adding one is ONE line in TILES",
                                True, (100, 112, 130)), (MAP_X + 380, py + 19))

    if error_text:
        pygame.draw.rect(screen, (60, 24, 24), (MAP_X, MAP_Y, WIDTH - 2 * MAP_X, 70))
        pygame.draw.rect(screen, (201, 42, 42), (MAP_X, MAP_Y, WIDTH - 2 * MAP_X, 70), 2)
        screen.blit(big.render("LEVEL PROBLEM", True, (255, 107, 107)), (MAP_X + 14, MAP_Y + 12))
        screen.blit(font.render(error_text[:90], True, (255, 200, 200)),
                    (MAP_X + 14, MAP_Y + 42))

    screen.blit(font.render("B  load broken-level.txt    R  reload level.txt    G  grid",
                            True, (100, 112, 130)), (MAP_X, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        # exercise the error path too, so the checker really covers it
        if frames == SELFTEST_FRAMES:
            try_load("broken-level.txt")
        running = False

pygame.quit()
