"""
02-tile-collision.py — two steps, never one.

WHAT THIS DEMONSTRATES
    * move X, fix X; then move Y, fix Y - and why one combined move cannot work
    * only the tiles the player's rect touches are ever tested (at most four,
      outlined in orange)
    * on_ground comes from the DOWNWARD test
    * what the missing -1 does, on a key: walk into the single-tile gap and stick

HOW TO RUN IT
    python3 02-tile-collision.py
      arrows / WASD  move        SPACE  jump
      B  one combined move (the bug)
      E  remove the -1 from the tile range
      D  debug drawing

WHAT TO CHANGE FIRST
    Press B and walk diagonally into a corner. The player climbs. Press B again and
    do it once more: now they slide, and you wrote no sliding code.
"""

import os
import pygame
from pygame.math import Vector2
from tilemap import Tilemap, load_level, TILE

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 800, 540
SPEED = 210
GRAVITY = 1500
JUMP = 520

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - tile collision")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

level = Tilemap(load_level("level.txt"))

one_step_bug = False
no_epsilon = False
show_debug = True
tested = []
fixed_x = fixed_y = False


class Player:
    def __init__(self):
        self.pos = Vector2(level.start_position())
        self.vel = Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, 22, 28)
        self.rect.midbottom = self.pos
        self.on_ground = False

    def tiles_touching(self):
        """The same as Tilemap.tiles_touching, but with the -1 on a switch so the
        class can watch the bug happen."""
        eps = 0 if no_epsilon else 1
        c0 = self.rect.left // TILE
        c1 = (self.rect.right - eps) // TILE
        r0 = self.rect.top // TILE
        r1 = (self.rect.bottom - eps) // TILE
        for row in range(r0, r1 + 1):
            for col in range(c0, c1 + 1):
                yield col, row

    def solid_hits(self):
        out = []
        for col, row in self.tiles_touching():
            tested.append((col, row))
            if level.is_solid(col, row):
                out.append(pygame.Rect(col * TILE, row * TILE, TILE, TILE))
        return out

    def update(self, dt):
        global fixed_x, fixed_y
        tested.clear()
        fixed_x = fixed_y = False

        keys = pygame.key.get_pressed()
        want = (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) - \
               (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0)
        self.vel.x = want * SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = -JUMP
            self.on_ground = False
        self.vel.y = min(900, self.vel.y + GRAVITY * dt)

        dx = self.vel.x * dt
        dy = self.vel.y * dt

        if one_step_bug:
            # ---- THE BUG: one move, one test. When the box ends up in a wall
            # there is no way to know WHICH direction put it there, so undoing
            # both is a guess - and at a corner it undoes the innocent one.
            self.pos.x += dx
            self.pos.y += dy
            self.rect.midbottom = (round(self.pos.x), round(self.pos.y))
            if self.solid_hits():
                self.pos.x -= dx
                self.pos.y -= dy
                self.rect.midbottom = (round(self.pos.x), round(self.pos.y))
                self.on_ground = True          # also a guess
                self.vel.y = 0
                fixed_x = fixed_y = True
            else:
                self.on_ground = False
            return

        # ---- step 1: X only. The fix KNOWS it is undoing horizontal movement.
        self.pos.x += dx
        self.rect.centerx = round(self.pos.x)
        for wall in self.solid_hits():
            if dx > 0:
                self.rect.right = wall.left
            elif dx < 0:
                self.rect.left = wall.right
            self.pos.x = self.rect.centerx
            self.vel.x = 0
            fixed_x = True

        # ---- step 2: Y only, from the corrected X.
        self.pos.y += dy
        self.rect.bottom = round(self.pos.y)
        self.on_ground = False
        for wall in self.solid_hits():
            if dy > 0:
                self.rect.bottom = wall.top
                self.on_ground = True          # THIS is where landing comes from
            elif dy < 0:
                self.rect.top = wall.bottom
            self.pos.y = self.rect.bottom
            self.vel.y = 0
            fixed_y = True

        if self.pos.y > level.height + 100:
            self.pos = Vector2(level.start_position())
            self.vel = Vector2(0, 0)


player = Player()
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
            elif event.key == pygame.K_b:
                one_step_bug = not one_step_bug
            elif event.key == pygame.K_e:
                no_epsilon = not no_epsilon
            elif event.key == pygame.K_d:
                show_debug = not show_debug

    player.update(dt)

    screen.fill((18, 22, 30))
    level.draw(screen, 0, 0, WIDTH, HEIGHT)

    if show_debug:
        for col, row in set(tested):
            pygame.draw.rect(screen, (240, 140, 0),
                             (col * TILE + 1, row * TILE + 1, TILE - 2, TILE - 2), 1)

    pygame.draw.rect(screen, (81, 207, 102) if player.on_ground else (77, 171, 247),
                     player.rect)

    panel_y = HEIGHT - 116
    pygame.draw.rect(screen, (10, 13, 18), (14, panel_y, 330, 104))
    pygame.draw.rect(screen, (43, 50, 64), (14, panel_y, 330, 104), 1)
    screen.blit(big.render("ONE STEP (broken)" if one_step_bug else "TWO STEPS (correct)",
                           True, (255, 107, 107) if one_step_bug else (81, 207, 102)),
                (26, panel_y + 18))
    info = [
        "tiles tested   %d of %d" % (len(set(tested)), level.cols * level.rows),
        "x fixed  %-5s   y fixed  %s" % (fixed_x, fixed_y),
        "on_ground      %s" % player.on_ground,
        "epsilon (E)    %s" % ("OFF - stick in gaps" if no_epsilon else "on"),
    ]
    for i, line in enumerate(info):
        colour = (255, 107, 107) if (i == 3 and no_epsilon) else (135, 147, 164)
        screen.blit(font.render(line, True, colour), (26, panel_y + 40 + i * 18))

    if one_step_bug:
        screen.blit(font.render("walk diagonally into a corner: the player climbs, and "
                                "nothing in that code looks wrong",
                                True, (255, 107, 107)), (360, HEIGHT - 26))
    elif no_epsilon:
        screen.blit(font.render("walk into a one-tile gap: you will stick in a space you fit",
                                True, (255, 107, 107)), (360, HEIGHT - 26))
    else:
        screen.blit(font.render("B  one-step bug    E  remove the -1    D  debug",
                                True, (100, 112, 130)), (360, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
