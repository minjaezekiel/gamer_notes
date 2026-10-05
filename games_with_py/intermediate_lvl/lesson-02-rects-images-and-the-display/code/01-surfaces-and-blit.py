"""
01-surfaces-and-blit.py — sprites made of numbers.

WHAT THIS DEMONSTRATES
    * a Surface is a rectangle of pixels; you can make your own
    * pygame.SRCALPHA is what makes the unpainted parts transparent. Press A to
      turn it off and watch every sprite arrive in a black box.
    * blit copies one Surface onto another, in three forms:
          screen.blit(s, (x, y))          whole thing, at a position
          screen.blit(s, rect)            whole thing, at a Rect
          screen.blit(sheet, pos, src)    PART of it - lesson 5 lives here
    * every number in make_sprite is a FRACTION of size, so one edit resizes it

HOW TO RUN IT
    python3 01-surfaces-and-blit.py
      A  toggle SRCALPHA
      +/-  change the sprite size
      S  show the generated spritesheet and the source rectangle

WHAT TO CHANGE FIRST
    Press + a few times. Nothing distorts, because no number in make_sprite is a
    fixed pixel count. Then go and hard-code one of them and press + again.
"""

import os
import pygame

WIDTH, HEIGHT = 720, 440
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - surfaces and blit")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 21)
big = pygame.font.SysFont(None, 26)

SKIN = (255, 217, 160)
SHIRT = (77, 171, 247)
LEGS = (43, 50, 64)
COIN = (255, 212, 59)


def make_player(size, use_alpha=True):
    """Every number here is a fraction of `size`. That is the whole technique:
    one edit resizes the sprite and nothing distorts."""
    flags = pygame.SRCALPHA if use_alpha else 0
    surface = pygame.Surface((size, size), flags)
    # head
    pygame.draw.circle(surface, SKIN,
                       (size // 2, int(size * 0.22)), int(size * 0.16))
    # body
    pygame.draw.rect(surface, SHIRT,
                     (size * 0.28, size * 0.36, size * 0.44, size * 0.34))
    # legs
    pygame.draw.rect(surface, LEGS, (size * 0.30, size * 0.70, size * 0.14, size * 0.28))
    pygame.draw.rect(surface, LEGS, (size * 0.56, size * 0.70, size * 0.14, size * 0.28))
    # one eye, so the sprite has a direction
    pygame.draw.rect(surface, (20, 24, 32),
                     (size * 0.54, size * 0.18, size * 0.08, size * 0.08))
    return surface


def make_coin(size, use_alpha=True):
    flags = pygame.SRCALPHA if use_alpha else 0
    surface = pygame.Surface((size, size), flags)
    pygame.draw.circle(surface, COIN, (size // 2, size // 2), int(size * 0.44))
    pygame.draw.circle(surface, (255, 255, 255),
                       (int(size * 0.38), int(size * 0.36)), max(1, int(size * 0.1)))
    return surface


def make_sheet(cell, count, use_alpha=True):
    """A spritesheet is ONE Surface with the frames in a row. Lesson 5 slides a
    source rectangle along it; today we only look at it."""
    flags = pygame.SRCALPHA if use_alpha else 0
    sheet = pygame.Surface((cell * count, cell), flags)
    for i in range(count):
        frame = make_coin(cell, use_alpha)
        # make each frame a little narrower, so the "spin" is visible
        squash = 1.0 - abs(i - (count - 1) / 2) / count
        scaled = pygame.transform.scale(frame, (max(2, int(cell * squash)), cell))
        sheet.blit(scaled, (i * cell + (cell - scaled.get_width()) // 2, 0))
    return sheet


size = 64
use_alpha = True
show_sheet = True
sheet_frame = 0
sheet_timer = 0.0

player = make_player(size, use_alpha)
coin = make_coin(size // 2, use_alpha)
sheet = make_sheet(32, 6, use_alpha)

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
            elif event.key == pygame.K_a:
                use_alpha = not use_alpha
            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                size = min(160, size + 16)
            elif event.key == pygame.K_MINUS:
                size = max(16, size - 16)
            elif event.key == pygame.K_s:
                show_sheet = not show_sheet
            # The Surfaces are rebuilt only when something CHANGED, not every
            # frame. Rebuilding per frame is the commonest slow-game mistake.
            player = make_player(size, use_alpha)
            coin = make_coin(size // 2, use_alpha)
            sheet = make_sheet(32, 6, use_alpha)

    sheet_timer += dt
    if sheet_timer > 0.12:
        sheet_timer = 0.0
        sheet_frame = (sheet_frame + 1) % 6

    # ---- render ----------------------------------------------------------
    screen.fill((20, 24, 32))
    # a chequered patch, so transparency is obvious rather than theoretical
    for cx in range(0, 300, 20):
        for cy in range(90, 330, 20):
            if (cx // 20 + cy // 20) % 2 == 0:
                pygame.draw.rect(screen, (34, 40, 52), (cx + 20, cy, 20, 20))

    screen.blit(big.render("sprites made in code", True, (231, 236, 243)), (20, 20))

    # form 1: a position
    screen.blit(player, (40, 120))
    # form 2: a Rect (any Rect; only its topleft is used)
    coin_rect = coin.get_rect(topleft=(40 + size + 30, 130))
    screen.blit(coin, coin_rect)

    screen.blit(font.render("blit(s, (x, y))", True, (135, 147, 164)), (40, 120 + size + 14))
    screen.blit(font.render("blit(s, rect)", True, (135, 147, 164)),
                (40 + size + 30, 130 + coin.get_height() + 14))

    if show_sheet:
        # form 3: PART of a Surface - the third argument is a source rectangle
        sx = sheet_frame * 32
        source = pygame.Rect(sx, 0, 32, 32)
        screen.blit(big.render("one frame of a sheet", True, (255, 212, 59)), (400, 100))
        screen.blit(sheet, (400, 136))
        pygame.draw.rect(screen, (255, 107, 107), (400 + sx, 136, 32, 32), 2)
        screen.blit(sheet, (400, 200), source)
        screen.blit(font.render("blit(sheet, pos, source_rect)", True, (135, 147, 164)),
                    (400, 240))
        screen.blit(font.render("source = (%d, 0, 32, 32)" % sx, True, (255, 107, 107)),
                    (400, 262))

    status = [
        "size        %d   (+ / -)" % size,
        "SRCALPHA    %s   (A)" % ("on" if use_alpha else "OFF"),
        "sheet       %s   (S)" % ("shown" if show_sheet else "hidden"),
        "fps         %.1f" % clock.get_fps(),
    ]
    for i, line in enumerate(status):
        colour = (255, 107, 107) if (i == 1 and not use_alpha) else (135, 147, 164)
        screen.blit(font.render(line, True, colour), (20, HEIGHT - 96 + i * 21))

    if not use_alpha:
        screen.blit(font.render("no SRCALPHA: the untouched pixels are opaque black",
                                True, (255, 107, 107)), (300, HEIGHT - 34))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
