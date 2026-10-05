"""
04-a-square-you-steer.py — the whole lesson in one file.

WHAT THIS DEMONSTRATES
    * polled input for movement (get_pressed), so holding a key glides
    * a KEYDOWN event for a one-off action, so it happens once per press
    * delta time on every movement
    * clamping to the window, using WIDTH - SIZE rather than WIDTH
    * intent, not keys: `wants_left` is computed once, and the movement code never
      mentions a key name - so adding WASD was one line
    * a clean quit, and the four-line self-test hook

HOW TO RUN IT
    python3 04-a-square-you-steer.py
      arrows or WASD   move
      SPACE            jump back to the centre (once per press)
      T                drop the frame cap to 10 fps
      Escape           quit

WHAT TO CHANGE FIRST
    Press T and check the square still crosses the window in the same time. If it
    does, your delta time is right. That ten-second test is the only objective
    proof available, and it is the one thing from this lesson that every later
    lesson depends on.
"""

import os
import pygame

WIDTH, HEIGHT = 640, 420
SIZE = 36
SPEED = 300                      # pixels per SECOND
BACKGROUND = (20, 24, 32)
SQUARE = (77, 171, 247)
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - a square you steer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 21)

x = WIDTH / 2 - SIZE / 2
y = HEIGHT / 2 - SIZE / 2
frame_cap = 60
recentres = 0
frames = 0
trail = []

running = True
while running:
    dt = clock.tick(frame_cap) / 1000.0

    # ---- 1. INPUT ---------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # A one-off action belongs in an EVENT. With get_pressed() this
                # would fire on every frame the key was held.
                x = WIDTH / 2 - SIZE / 2
                y = HEIGHT / 2 - SIZE / 2
                recentres += 1
                trail.clear()
            elif event.key == pygame.K_t:
                frame_cap = 10 if frame_cap == 60 else 60

    keys = pygame.key.get_pressed()

    # Turn keyboard facts into game intentions, in ONE place. The movement code
    # below never mentions a key, so adding WASD cost one line each.
    wants_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    wants_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    wants_up = keys[pygame.K_UP] or keys[pygame.K_w]
    wants_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

    # ---- 2. UPDATE --------------------------------------------------------
    if wants_left:
        x -= SPEED * dt
    if wants_right:
        x += SPEED * dt
    if wants_up:
        y -= SPEED * dt
    if wants_down:
        y += SPEED * dt

    # Clamp. Note WIDTH - SIZE: x is the LEFT edge, so clamping to WIDTH would let
    # the square sit entirely outside the window.
    x = max(0, min(WIDTH - SIZE, x))
    y = max(0, min(HEIGHT - SIZE, y))

    if wants_left or wants_right or wants_up or wants_down:
        trail.append((x, y))
        if len(trail) > 50:
            trail.pop(0)

    # ---- 3. RENDER --------------------------------------------------------
    screen.fill(BACKGROUND)

    for i, (tx, ty) in enumerate(trail):
        shade = 30 + int(60 * i / max(1, len(trail)))
        pygame.draw.rect(screen, (shade, shade + 10, shade + 24),
                         (tx + 12, ty + 12, 12, 12))

    pygame.draw.rect(screen, SQUARE, (x, y, SIZE, SIZE))

    readout = [
        "x, y        %4.0f, %4.0f" % (x, y),
        "dt          %.4f s" % dt,
        "frame cap   %d   (T)" % frame_cap,
        "fps         %.1f" % clock.get_fps(),
        "recentres   %d   (SPACE, once per press)" % recentres,
    ]
    for i, line in enumerate(readout):
        screen.blit(font.render(line, True, (135, 147, 164)), (14, 14 + i * 20))

    if frame_cap != 60:
        screen.blit(font.render("10 fps: the square should still cross the window "
                                "in the same time", True, (255, 212, 59)),
                    (14, HEIGHT - 26))

    pygame.display.flip()

    # ---- the self-test exit ----------------------------------------------
    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
