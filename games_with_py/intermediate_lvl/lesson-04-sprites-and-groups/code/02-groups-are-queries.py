"""
02-groups-are-queries.py — a group is a question you can ask quickly.

WHAT THIS DEMONSTRATES
    One sprite can be in many groups, and each group is a QUESTION:

        all_sprites   "draw me"
        solid         "the player cannot pass me"
        hazards       "I hurt the player"
        collectables  "pick me up"

    Every sprite's membership is drawn next to it. Click a sprite to toggle it in
    and out of the `solid` group and watch the player's behaviour change with no
    change to any sprite's code.

    Press S for the self-collision trap: testing a sprite against a group that
    CONTAINS it always returns the sprite itself.

HOW TO RUN IT
    python3 02-groups-are-queries.py
      arrows / WASD  move the player
      click a block  add or remove it from `solid`
      S  run the self-collision test and show the count
      K  kill() a random block - watch it leave every group at once

WHAT TO CHANGE FIRST
    Click a wall to make it non-solid and walk through it. Nothing about that
    sprite changed except which question it answers.
"""

import os
import random
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 780, 480
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - groups are queries")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)
big = pygame.font.SysFont(None, 25)

all_sprites = pygame.sprite.Group()
solid = pygame.sprite.Group()
hazards = pygame.sprite.Group()
collectables = pygame.sprite.Group()

GROUPS = [("all", all_sprites), ("solid", solid),
          ("hazard", hazards), ("pickup", collectables)]


def make_block(size, colour):
    s = pygame.Surface(size, pygame.SRCALPHA)
    s.fill(colour)
    pygame.draw.rect(s, (255, 255, 255, 40), s.get_rect(), 2)
    return s


class Block(pygame.sprite.Sprite):
    def __init__(self, rect, colour):
        super().__init__()
        self.image = make_block(rect.size, colour)
        self.rect = rect

    def update(self, dt):
        pass


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 212, 59), (9, 9), 8)
        self.rect = self.image.get_rect(center=pos)
        self.spin = 0.0

    def update(self, dt):
        self.spin += dt


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = make_block((26, 30), (77, 171, 247))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        move = Vector2(
            (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) -
            (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0),
            (1 if keys[pygame.K_DOWN] or keys[pygame.K_s] else 0) -
            (1 if keys[pygame.K_UP] or keys[pygame.K_w] else 0))
        if move.length_squared() == 0:
            return
        step = move.normalize() * 230 * dt

        # X then Y, each tested against the `solid` GROUP - which is the question
        # "what can I not pass through?"
        self.pos.x += step.x
        self.rect.centerx = round(self.pos.x)
        for block in pygame.sprite.spritecollide(self, solid, False):
            if step.x > 0:
                self.rect.right = block.rect.left
            elif step.x < 0:
                self.rect.left = block.rect.right
            self.pos.x = self.rect.centerx

        self.pos.y += step.y
        self.rect.centery = round(self.pos.y)
        for block in pygame.sprite.spritecollide(self, solid, False):
            if step.y > 0:
                self.rect.bottom = block.rect.top
            elif step.y < 0:
                self.rect.top = block.rect.bottom
            self.pos.y = self.rect.centery


player = Player((80, 80))
all_sprites.add(player)

blocks = []
for rect, kind in [
    (pygame.Rect(200, 120, 120, 30), "wall"),
    (pygame.Rect(420, 90, 30, 180), "wall"),
    (pygame.Rect(260, 300, 180, 30), "wall"),
    (pygame.Rect(560, 200, 110, 30), "spikes"),
    (pygame.Rect(170, 380, 150, 26), "spikes"),
]:
    colour = (58, 69, 85) if kind == "wall" else (124, 45, 45)
    b = Block(rect, colour)
    all_sprites.add(b)
    if kind == "wall":
        solid.add(b)
    else:
        hazards.add(b)
    blocks.append(b)

for pos in [(140, 220), (350, 200), (520, 350), (660, 110), (300, 430)]:
    c = Coin(pos)
    all_sprites.add(c)
    collectables.add(c)

score = 0
hurt_flash = 0.0
self_test_result = ""
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
            elif event.key == pygame.K_s:
                # THE SELF-COLLISION TRAP. `block` is IN `solid`, so it finds
                # itself: a rectangle always overlaps itself.
                if blocks:
                    b = blocks[0]
                    found = pygame.sprite.spritecollide(b, solid, False)
                    filtered = [s for s in found if s is not b]
                    self_test_result = ("spritecollide(block, solid) found %d; "
                                        "after filtering itself out: %d"
                                        % (len(found), len(filtered)))
            elif event.key == pygame.K_k:
                if blocks:
                    victim = random.choice(blocks)
                    blocks.remove(victim)
                    victim.kill()        # leaves all_sprites AND solid/hazards
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in blocks:
                if b.rect.collidepoint(event.pos):
                    if b in solid:
                        solid.remove(b)
                    else:
                        solid.add(b)

    all_sprites.update(dt)

    # each of these lines asks one group its own question
    for coin in pygame.sprite.spritecollide(player, collectables, True):
        score += 10
    if pygame.sprite.spritecollideany(player, hazards):
        hurt_flash = 0.4
    if hurt_flash > 0:
        hurt_flash -= dt

    screen.fill((20, 24, 32))
    all_sprites.draw(screen)

    # membership, drawn next to each sprite
    for s in all_sprites:
        names = [name for name, g in GROUPS if s in g]
        label = font.render(",".join(names), True, (120, 132, 150))
        screen.blit(label, (s.rect.x, s.rect.bottom + 2))

    screen.blit(big.render("SCORE %d" % score, True, (231, 236, 243)), (18, 14))
    info = [
        "all_sprites   %d" % len(all_sprites),
        "solid         %d" % len(solid),
        "hazards       %d" % len(hazards),
        "collectables  %d" % len(collectables),
        "",
        "click a block to add/remove it from `solid`",
        "S  the self-collision trap    K  kill() one",
    ]
    for i, line in enumerate(info):
        screen.blit(font.render(line, True, (135, 147, 164)), (WIDTH - 310, 20 + i * 20))

    if self_test_result:
        screen.blit(font.render(self_test_result, True, (255, 212, 59)), (18, HEIGHT - 44))
    screen.blit(font.render("one sprite, several groups - a group is a question, not a box",
                            True, (74, 83, 98)), (18, HEIGHT - 22))

    if hurt_flash > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 107, 107, int(80 * min(1, hurt_flash / 0.4))))
        screen.blit(overlay, (0, 0))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
