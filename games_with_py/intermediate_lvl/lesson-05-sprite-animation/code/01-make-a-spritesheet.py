"""
01-make-a-spritesheet.py — a spritesheet with no image file.

WHAT THIS DEMONSTRATES
    A pygame Surface is a rectangle of pixels; you can draw on one and then treat
    it as a spritesheet. Three rows, six columns, built from numbers.

    Three reasons this is a technique and not a workaround:
      * a lesson cannot break because a file is missing
      * a sprite made of numbers is tuned by changing a number
      * drawing something ONCE onto a Surface, instead of every frame, is one of
        the best optimisations in 2D games

HOW TO RUN IT
    python3 01-make-a-spritesheet.py
      G  grid        N  cell numbers        + / -  zoom
      W / H  make the cells wider or taller and rebuild the sheet

WHAT TO CHANGE FIRST
    Press W a few times. Every pose stretches correctly, because no number in
    draw_pose is a fixed pixel count. Then go and hard-code one of them.
"""

import os
import pygame
from spritesheet import make_sheet, ROWS

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 780, 470

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - make a spritesheet")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

frame_w, frame_h = 32, 40
zoom = 4
show_grid = True
show_numbers = True
sheet = make_sheet(frame_w, frame_h)
frames = 0
row_names = {v: k for k, v in ROWS.items()}

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            rebuild = False
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_g:
                show_grid = not show_grid
            elif event.key == pygame.K_n:
                show_numbers = not show_numbers
            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                zoom = min(8, zoom + 1)
            elif event.key == pygame.K_MINUS:
                zoom = max(1, zoom - 1)
            elif event.key == pygame.K_w:
                frame_w = min(64, frame_w + 4)
                rebuild = True
            elif event.key == pygame.K_h:
                frame_h = min(72, frame_h + 4)
                rebuild = True
            if rebuild:
                sheet = make_sheet(frame_w, frame_h)

    screen.fill((20, 24, 32))

    ox, oy = 28, 86
    scaled = pygame.transform.scale(sheet,
                                    (sheet.get_width() * zoom, sheet.get_height() * zoom))
    screen.blit(scaled, (ox, oy))

    if show_grid:
        for col in range(sheet.get_width() // frame_w + 1):
            x = ox + col * frame_w * zoom
            pygame.draw.line(screen, (240, 140, 0), (x, oy), (x, oy + scaled.get_height()))
        for row in range(sheet.get_height() // frame_h + 1):
            y = oy + row * frame_h * zoom
            pygame.draw.line(screen, (240, 140, 0), (ox, y), (ox + scaled.get_width(), y))

    if show_numbers:
        for row in range(sheet.get_height() // frame_h):
            for col in range(sheet.get_width() // frame_w):
                label = font.render("%d,%d" % (col, row), True, (255, 212, 59))
                screen.blit(label, (ox + col * frame_w * zoom + 3,
                                    oy + row * frame_h * zoom + 3))

    screen.blit(big.render("the generated sheet, %dx" % zoom, True, (231, 236, 243)), (28, 28))
    screen.blit(font.render("%d x %d px   cells %d x %d   %d columns x %d rows"
                            % (sheet.get_width(), sheet.get_height(), frame_w, frame_h,
                               sheet.get_width() // frame_w, sheet.get_height() // frame_h),
                            True, (135, 147, 164)), (28, 54))

    px = ox + scaled.get_width() + 24
    if px < WIDTH - 180:
        screen.blit(font.render("ROWS", True, (231, 236, 243)), (px, oy))
        for row in sorted(row_names):
            screen.blit(font.render("row %d  %s" % (row, row_names[row]),
                                    True, (135, 147, 164)), (px, oy + 24 + row * 20))
        screen.blit(font.render("to take one cell:", True, (231, 236, 243)), (px, oy + 110))
        for i, line in enumerate(["rect = Rect(col*%d, row*%d," % (frame_w, frame_h),
                                  "            %d, %d)" % (frame_w, frame_h),
                                  "frame = sheet.subsurface(rect)"]):
            screen.blit(font.render(line, True, (255, 212, 59)), (px, oy + 134 + i * 20))

    screen.blit(font.render("G grid   N numbers   +/- zoom   W wider   H taller",
                            True, (100, 112, 130)), (28, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
