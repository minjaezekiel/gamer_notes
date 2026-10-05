"""
02-rects.py — every Rect attribute, live.

WHAT THIS DEMONSTRATES
    A Rect is the AABB from the beginner level with thirty helpers attached. Drag
    the blue box with the mouse and watch all nine named positions update. Assigning
    to any of them MOVES THE BOX, which is how you place things in pygame.

    The red box is fixed. `colliderect` lights up when they overlap - that is the
    four-condition test you wrote by hand, already written.

HOW TO RUN IT
    python3 02-rects.py
      drag the blue box with the mouse
      1  blue.center    = the red box's center
      2  blue.bottom    = the red box's top     ("stand on it")
      3  blue.midleft   = the red box's midright
      C  clamp the blue box inside the window
      arrow keys nudge it one pixel

WHAT TO CHANGE FIRST
    Press 2. One line put the blue box exactly on top of the red one, with no
    arithmetic. That is `rect.bottom = floor_y`, which is the whole of standing on
    a floor.
"""

import os
import pygame

WIDTH, HEIGHT = 760, 460
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - rects")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 25)

screen_rect = screen.get_rect()
blue = pygame.Rect(120, 150, 110, 80)
red = pygame.Rect(430, 230, 150, 110)

dragging = False
drag_offset = (0, 0)
last_action = "drag the blue box"
frames = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # collidepoint: is this point inside me?
            if blue.collidepoint(event.pos):
                dragging = True
                drag_offset = (blue.x - event.pos[0], blue.y - event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Each of these is ONE assignment, and each MOVES the whole box.
            elif event.key == pygame.K_1:
                blue.center = red.center
                last_action = "blue.center = red.center"
            elif event.key == pygame.K_2:
                blue.bottom = red.top
                blue.centerx = red.centerx
                last_action = "blue.bottom = red.top   ('stand on it')"
            elif event.key == pygame.K_3:
                blue.midleft = red.midright
                last_action = "blue.midleft = red.midright"
            elif event.key == pygame.K_c:
                blue.clamp_ip(screen_rect)
                last_action = "blue.clamp_ip(screen_rect)"
            elif event.key == pygame.K_LEFT:
                blue.x -= 1
            elif event.key == pygame.K_RIGHT:
                blue.x += 1
            elif event.key == pygame.K_UP:
                blue.y -= 1
            elif event.key == pygame.K_DOWN:
                blue.y += 1

    if dragging:
        blue.x = mouse[0] + drag_offset[0]
        blue.y = mouse[1] + drag_offset[1]

    touching = blue.colliderect(red)

    # ---- render -----------------------------------------------------------
    screen.fill((20, 24, 32))

    pygame.draw.rect(screen, (201, 42, 42) if touching else (120, 60, 60), red)
    pygame.draw.rect(screen, (77, 171, 247), blue)

    # the nine named positions, drawn where they are
    points = [
        ("topleft", blue.topleft), ("midtop", blue.midtop), ("topright", blue.topright),
        ("midleft", blue.midleft), ("center", blue.center), ("midright", blue.midright),
        ("bottomleft", blue.bottomleft), ("midbottom", blue.midbottom),
        ("bottomright", blue.bottomright),
    ]
    for name, pos in points:
        pygame.draw.circle(screen, (255, 212, 59), pos, 4)

    screen.blit(big.render("a Rect knows where its own parts are", True, (231, 236, 243)),
                (20, 20))

    px = 20
    py = 300
    rows = [
        ("left, top", "%d, %d" % (blue.left, blue.top)),
        ("right, bottom", "%d, %d" % (blue.right, blue.bottom)),
        ("width, height", "%d, %d" % (blue.width, blue.height)),
        ("center", "%s" % (blue.center,)),
        ("midbottom", "%s" % (blue.midbottom,)),
        ("topright", "%s" % (blue.topright,)),
    ]
    for i, (name, value) in enumerate(rows):
        screen.blit(font.render(name, True, (135, 147, 164)), (px, py + i * 21))
        screen.blit(font.render(value, True, (255, 212, 59)), (px + 130, py + i * 21))

    px2 = 330
    screen.blit(font.render("blue.colliderect(red)", True, (135, 147, 164)), (px2, py))
    screen.blit(font.render(str(touching), True,
                            (255, 107, 107) if touching else (81, 207, 102)),
                (px2 + 200, py))
    screen.blit(font.render("blue.collidepoint(mouse)", True, (135, 147, 164)), (px2, py + 21))
    screen.blit(font.render(str(blue.collidepoint(mouse)), True, (255, 212, 59)),
                (px2 + 200, py + 21))

    screen.blit(font.render("1  center = red.center", True, (135, 147, 164)), (px2, py + 56))
    screen.blit(font.render("2  bottom = red.top", True, (135, 147, 164)), (px2, py + 77))
    screen.blit(font.render("3  midleft = red.midright", True, (135, 147, 164)), (px2, py + 98))
    screen.blit(font.render("C  clamp_ip(screen)", True, (135, 147, 164)), (px2, py + 119))

    screen.blit(font.render("last: " + last_action, True, (81, 207, 102)), (20, HEIGHT - 28))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
