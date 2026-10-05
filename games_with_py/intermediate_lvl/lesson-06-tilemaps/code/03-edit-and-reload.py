"""
03-edit-and-reload.py — redesign the world by typing.

WHAT THIS DEMONSTRATES
    The level is DATA. Open level.txt in another window, change it, save, and press
    R. The world changes and the game keeps running.

    It also watches the file's modification time, so A turns on auto-reload and you
    need not press anything at all.

    Water slows you down, spikes send you back to the start, and coins score -
    none of which required a change to the drawing code, because all three are
    properties in the TILES table.

HOW TO RUN IT
    python3 03-edit-and-reload.py
      arrows / WASD  move        SPACE  jump
      R  reload now        A  auto-reload on save

WHAT TO CHANGE FIRST
    Add a sixth tile type to TILES in tilemap.py - say "=" with
    {"solid": True, "colour": (90, 120, 60)} - then type some "=" into level.txt
    and press R. Neither the draw loop nor the collision code needed touching.
"""

import os
import pygame
from pygame.math import Vector2
from tilemap import Tilemap, load_level, LevelError, TILE, HERE

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 800, 540
SPEED = 210
GRAVITY = 1500
JUMP = 520

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - edit and reload")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 26)

LEVEL_PATH = HERE / "level.txt"

level = Tilemap(load_level("level.txt"))
error_text = ""
auto_reload = False
last_mtime = LEVEL_PATH.stat().st_mtime
reloads = 0

coins_taken = set()        # "taken" lives OUTSIDE the level, so reloading is free
score = 0
deaths = 0


class Player:
    def __init__(self):
        self.reset()
        self.rect = pygame.Rect(0, 0, 22, 28)
        self.rect.midbottom = self.pos

    def reset(self):
        self.pos = Vector2(level.start_position())
        self.vel = Vector2(0, 0)
        self.on_ground = False

    def update(self, dt):
        global score, deaths
        keys = pygame.key.get_pressed()

        # water slows you: a PROPERTY from the table, not a special case in here
        in_water = any(level.info(c, r).get("slows")
                       for c, r in level.tiles_touching(self.rect))
        speed = SPEED * (0.45 if in_water else 1.0)
        gravity = GRAVITY * (0.35 if in_water else 1.0)

        want = (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) - \
               (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0)
        self.vel.x = want * speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = -JUMP
            self.on_ground = False
        self.vel.y = min(220 if in_water else 900, self.vel.y + gravity * dt)

        dx = self.vel.x * dt
        self.pos.x += dx
        self.rect.centerx = round(self.pos.x)
        for wall in level.solid_rects_touching(self.rect):
            if dx > 0:
                self.rect.right = wall.left
            elif dx < 0:
                self.rect.left = wall.right
            self.pos.x = self.rect.centerx
            self.vel.x = 0

        dy = self.vel.y * dt
        self.pos.y += dy
        self.rect.bottom = round(self.pos.y)
        self.on_ground = False
        for wall in level.solid_rects_touching(self.rect):
            if dy > 0:
                self.rect.bottom = wall.top
                self.on_ground = True
            elif dy < 0:
                self.rect.top = wall.bottom
            self.pos.y = self.rect.bottom
            self.vel.y = 0

        # deadly and collectable, both from the table
        for col, row in level.tiles_touching(self.rect):
            info = level.info(col, row)
            if info.get("deadly"):
                deaths += 1
                self.reset()
                return
            if info.get("coin") and (col, row) not in coins_taken:
                coins_taken.add((col, row))
                score += 10

        if self.pos.y > level.height + 100:
            deaths += 1
            self.reset()


player = Player()


def reload_level(reason):
    global level, error_text, reloads, last_mtime, coins_taken
    try:
        level = Tilemap(load_level("level.txt"))
        # The level is read-only, so "which coins are taken" lives outside it and
        # a reload costs nothing to recover from.
        coins_taken = set()
        player.reset()
        error_text = ""
        reloads += 1
    except (LevelError, FileNotFoundError) as err:
        error_text = "%s: %s" % (type(err).__name__, err)
    last_mtime = LEVEL_PATH.stat().st_mtime if LEVEL_PATH.exists() else 0


frames = 0
check_timer = 0.0

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
                reload_level("you pressed R")
            elif event.key == pygame.K_a:
                auto_reload = not auto_reload

    # watching the file's modification time: twice a second is plenty
    check_timer += dt
    if auto_reload and check_timer > 0.5:
        check_timer = 0.0
        if LEVEL_PATH.exists() and LEVEL_PATH.stat().st_mtime != last_mtime:
            reload_level("the file changed")

    player.update(dt)

    screen.fill((18, 22, 30))
    level.draw(screen, 0, 0, WIDTH, HEIGHT, coins_taken=coins_taken)
    pygame.draw.rect(screen, (77, 171, 247), player.rect)

    screen.blit(big.render("SCORE %d" % score, True, (231, 236, 243)), (16, 12))
    info = [
        "level     %d x %d" % (level.cols, level.rows),
        "reloads   %d   (R)" % reloads,
        "auto (A)  %s" % ("on" if auto_reload else "off"),
        "deaths    %d" % deaths,
    ]
    for i, line in enumerate(info):
        screen.blit(font.render(line, True, (110, 122, 140)), (16, 44 + i * 19))

    if error_text:
        pygame.draw.rect(screen, (60, 24, 24), (14, HEIGHT - 58, WIDTH - 28, 44))
        pygame.draw.rect(screen, (201, 42, 42), (14, HEIGHT - 58, WIDTH - 28, 44), 2)
        screen.blit(font.render(error_text[:100], True, (255, 200, 200)),
                    (26, HEIGHT - 44))
    else:
        screen.blit(font.render("edit level.txt in another window, then press R",
                                True, (100, 112, 130)), (16, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        if frames == SELFTEST_FRAMES:
            reload_level("the self test")
        running = False

pygame.quit()
