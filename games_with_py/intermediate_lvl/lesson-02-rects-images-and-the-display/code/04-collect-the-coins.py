"""
04-collect-the-coins.py — the whole lesson, assembled.

WHAT THIS DEMONSTRATES
    * sprites made in code, once, at startup
    * a float position with a Rect copied from it
    * walls as a list of Rects, resolved ONE AXIS AT A TIME (so you slide along
      them instead of stopping dead)
    * coins collected with colliderect, removed safely
    * text rendered only when the score CHANGES, not every frame
    * the sprite flipped once at startup rather than every frame
    * the frame rate on screen, because opinions about speed are worthless

HOW TO RUN IT
    python3 04-collect-the-coins.py
      arrows or WASD   move
      R                new coins
      B                resolve both axes at once (the sticky-corner bug)
      T                render the score text every frame (watch the fps)

WHAT TO CHANGE FIRST
    Press B and walk diagonally into a corner. You stop dead instead of sliding.
    Then press B again. That is the beginner-level lesson arriving in pygame.
"""

import os
import random
import pygame

WIDTH, HEIGHT = 760, 480
TILE = 40
SPEED = 260
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - collect the coins")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 21)
score_font = pygame.font.SysFont(None, 34)


def make_player(size):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 217, 160), (size // 2, int(size * 0.24)), int(size * 0.17))
    pygame.draw.rect(s, (77, 171, 247), (size * 0.26, size * 0.38, size * 0.48, size * 0.34))
    pygame.draw.rect(s, (43, 50, 64), (size * 0.28, size * 0.72, size * 0.15, size * 0.26))
    pygame.draw.rect(s, (43, 50, 64), (size * 0.57, size * 0.72, size * 0.15, size * 0.26))
    pygame.draw.rect(s, (20, 24, 32), (size * 0.56, size * 0.20, size * 0.08, size * 0.08))
    return s


def make_coin(size):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 212, 59), (size // 2, size // 2), int(size * 0.44))
    pygame.draw.circle(s, (255, 255, 255),
                       (int(size * 0.38), int(size * 0.36)), max(1, int(size * 0.09)))
    return s


# Built ONCE. The flip is done here too, not every frame.
PLAYER_RIGHT = make_player(34)
PLAYER_LEFT = pygame.transform.flip(PLAYER_RIGHT, True, False)
COIN_IMAGE = make_coin(22)

WALLS = [
    pygame.Rect(0, 0, WIDTH, TILE),
    pygame.Rect(0, HEIGHT - TILE, WIDTH, TILE),
    pygame.Rect(0, 0, TILE, HEIGHT),
    pygame.Rect(WIDTH - TILE, 0, TILE, HEIGHT),
    pygame.Rect(160, 120, TILE * 5, TILE),
    pygame.Rect(160, 120, TILE, TILE * 4),
    pygame.Rect(440, 200, TILE, TILE * 5),
    pygame.Rect(440, 200, TILE * 6, TILE),
    pygame.Rect(240, 320, TILE * 4, TILE),
]

# float position is the truth; the rect is a copy for drawing and colliding
player_x, player_y = 90.0, 90.0
player_rect = PLAYER_RIGHT.get_rect(topleft=(player_x, player_y))
facing = 1

coins = []
score = 0
both_axes_bug = False
render_every_frame = False
frames = 0

# the cached score Surface, and the value it was rendered for
score_surface = None
score_rendered_for = None
renders = 0


def new_coins():
    out = []
    attempts = 0
    while len(out) < 12 and attempts < 400:
        attempts += 1
        r = COIN_IMAGE.get_rect(topleft=(random.randint(TILE + 6, WIDTH - TILE - 30),
                                         random.randint(TILE + 6, HEIGHT - TILE - 30)))
        if any(r.colliderect(w) for w in WALLS):
            continue
        out.append(r)
    return out


coins = new_coins()


def blocked(rect):
    """The AABB test, already written. Returns the first wall hit, or None."""
    for wall in WALLS:
        if rect.colliderect(wall):
            return wall
    return None


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                coins = new_coins()
            elif event.key == pygame.K_b:
                both_axes_bug = not both_axes_bug
            elif event.key == pygame.K_t:
                render_every_frame = not render_every_frame

    keys = pygame.key.get_pressed()
    want_x = (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) - \
             (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0)
    want_y = (1 if keys[pygame.K_DOWN] or keys[pygame.K_s] else 0) - \
             (1 if keys[pygame.K_UP] or keys[pygame.K_w] else 0)
    if want_x:
        facing = want_x

    dx = want_x * SPEED * dt
    dy = want_y * SPEED * dt

    if both_axes_bug:
        # ---- THE BUG: move both, then undo both. No way to know which caused it.
        player_x += dx
        player_y += dy
        player_rect.topleft = (round(player_x), round(player_y))
        if blocked(player_rect):
            player_x -= dx
            player_y -= dy
            player_rect.topleft = (round(player_x), round(player_y))
    else:
        # ---- X first, then fix X. The correction knows which axis it is undoing.
        player_x += dx
        player_rect.x = round(player_x)
        wall = blocked(player_rect)
        if wall:
            if dx > 0:
                player_rect.right = wall.left
            elif dx < 0:
                player_rect.left = wall.right
            player_x = float(player_rect.x)

        # ---- then Y, from the corrected X.
        player_y += dy
        player_rect.y = round(player_y)
        wall = blocked(player_rect)
        if wall:
            if dy > 0:
                player_rect.bottom = wall.top
            elif dy < 0:
                player_rect.top = wall.bottom
            player_y = float(player_rect.y)

    # ---- coins. Rebuild the list rather than removing while iterating. ----
    remaining = []
    for coin_rect in coins:
        if player_rect.colliderect(coin_rect):
            score += 10
        else:
            remaining.append(coin_rect)
    coins = remaining

    # ---- the text, rendered only when the number CHANGES ------------------
    if render_every_frame or score_rendered_for != score:
        score_surface = score_font.render("SCORE %d" % score, True, (231, 236, 243))
        score_rendered_for = score
        renders += 1

    # ---- render -----------------------------------------------------------
    screen.fill((20, 24, 32))
    for wall in WALLS:
        pygame.draw.rect(screen, (58, 69, 85), wall)
    for coin_rect in coins:
        screen.blit(COIN_IMAGE, coin_rect)
    screen.blit(PLAYER_RIGHT if facing > 0 else PLAYER_LEFT, player_rect)

    screen.blit(score_surface, (TILE + 10, TILE + 8))
    info = [
        "coins left   %d" % len(coins),
        "fps          %.1f" % clock.get_fps(),
        "text renders %d  (T to render every frame)" % renders,
        "collision    %s  (B)" % ("BOTH AXES - bug" if both_axes_bug else "one axis at a time"),
    ]
    for i, line in enumerate(info):
        colour = (255, 107, 107) if (i == 3 and both_axes_bug) else (135, 147, 164)
        screen.blit(font.render(line, True, colour), (TILE + 10, HEIGHT - TILE - 96 + i * 21))

    if not coins:
        screen.blit(score_font.render("all collected - press R", True, (81, 207, 102)),
                    (WIDTH // 2 - 130, HEIGHT // 2))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
