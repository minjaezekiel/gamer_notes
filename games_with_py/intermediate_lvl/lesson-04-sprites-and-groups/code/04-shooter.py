"""
04-shooter.py — hundreds of things, six lines of main loop.

WHAT THIS DEMONSTRATES
    The whole lesson, assembled. Look at the loop near the bottom: six lines do the
    work of about eighty, and every one of them is a group doing its job.

        all_sprites.update(dt)
        all_sprites.draw(screen)
        pygame.sprite.groupcollide(bullets, enemies, True, True)
        pygame.sprite.spritecollide(player, pickups, True)
        pygame.sprite.spritecollideany(player, enemies)
        sprite.kill()

    Every sprite is in `all_sprites` (the "draw me" question) AND in one more group
    (the "check me" question). Adding a new kind of interaction later is one group
    and one add().

HOW TO RUN IT
    python3 04-shooter.py
      arrows / WASD  move        SPACE  fire        R  restart

WHAT TO CHANGE FIRST
    In the Bullet class, remove `self.kill()` from the off-screen test. Watch the
    sprite count climb for ever and the frame rate fall. That one line is why the
    count stays flat.
"""

import os
import random
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 780, 520
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 30)

SCREEN_RECT = screen.get_rect()

# ---------------------------------------------------------------------------
# Sprites, drawn in code once at startup (lesson 2).
# ---------------------------------------------------------------------------
def make_ship(size=30):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(s, (77, 171, 247),
                        [(size / 2, 2), (size - 3, size - 4), (size / 2, size * 0.72),
                         (3, size - 4)])
    return s


def make_enemy(size=26):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(s, (192, 106, 154),
                        [(size / 2, size - 2), (size - 3, 4), (size / 2, size * 0.3), (3, 4)])
    return s


def make_bullet():
    s = pygame.Surface((4, 12), pygame.SRCALPHA)
    s.fill((255, 212, 59))
    return s


def make_pickup():
    s = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.circle(s, (81, 207, 102), (8, 8), 7)
    pygame.draw.circle(s, (255, 255, 255), (6, 6), 2)
    return s


def make_spark(colour):
    s = pygame.Surface((4, 4), pygame.SRCALPHA)
    s.fill(colour)
    return s


SHIP_IMAGE = make_ship()
ENEMY_IMAGE = make_enemy()
BULLET_IMAGE = make_bullet()
PICKUP_IMAGE = make_pickup()

# ---------------------------------------------------------------------------
# The groups. Each one is a QUESTION.
# ---------------------------------------------------------------------------
all_sprites = pygame.sprite.Group()     # "draw me"
enemies = pygame.sprite.Group()         # "a bullet should check me"
bullets = pygame.sprite.Group()         # "an enemy should check me"
pickups = pygame.sprite.Group()         # "the player picks me up"
effects = pygame.sprite.Group()         # "I am decoration"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SHIP_IMAGE
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - 70))
        self.pos = Vector2(self.rect.center)
        self.cooldown = 0.0
        self.lives = 3
        self.invulnerable = 0.0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        move = Vector2(
            (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) -
            (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0),
            (1 if keys[pygame.K_DOWN] or keys[pygame.K_s] else 0) -
            (1 if keys[pygame.K_UP] or keys[pygame.K_w] else 0))
        if move.length_squared() > 0:
            self.pos += move.normalize() * 300 * dt
        self.pos.x = max(16, min(WIDTH - 16, self.pos.x))
        self.pos.y = max(40, min(HEIGHT - 20, self.pos.y))
        self.rect.center = self.pos

        self.cooldown -= dt
        if self.invulnerable > 0:
            self.invulnerable -= dt
        if keys[pygame.K_SPACE] and self.cooldown <= 0:
            self.cooldown = 0.14
            spawn(Bullet(self.pos), bullets)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)

    def update(self, dt):
        self.pos.y -= 620 * dt
        self.rect.center = self.pos
        if self.rect.bottom < 0:
            self.kill()          # leaves all_sprites AND bullets, in one call


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, speed):
        super().__init__()
        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect(center=(x, -20))
        self.pos = Vector2(self.rect.center)
        self.speed = speed
        self.drift = random.uniform(-40, 40)

    def update(self, dt):
        self.pos.y += self.speed * dt
        self.pos.x += self.drift * dt
        if self.pos.x < 14 or self.pos.x > WIDTH - 14:
            self.drift = -self.drift
        self.rect.center = self.pos
        if self.rect.top > HEIGHT:
            self.kill()


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = PICKUP_IMAGE
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)

    def update(self, dt):
        self.pos.y += 90 * dt
        self.rect.center = self.pos
        if self.rect.top > HEIGHT:
            self.kill()


class Spark(pygame.sprite.Sprite):
    """Decoration. In all_sprites and effects, in nothing that is tested."""

    def __init__(self, pos, colour):
        super().__init__()
        self.image = make_spark(colour)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(60, 240)
        self.life = random.uniform(0.25, 0.6)

    def update(self, dt):
        self.vel.y += 500 * dt
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.life -= dt
        if self.life <= 0:
            self.kill()


def spawn(sprite, *groups):
    all_sprites.add(sprite)
    for g in groups:
        g.add(sprite)
    return sprite


def burst(pos, colour, n=14):
    for _ in range(n):
        spawn(Spark(pos, colour), effects)


def reset():
    for g in (all_sprites, enemies, bullets, pickups, effects):
        g.empty()
    p = Player()
    all_sprites.add(p)
    return p


player = reset()
score = 0
spawn_timer = 0.0
wave = 1
game_over = False
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
            elif event.key == pygame.K_r:
                player = reset()
                score = 0
                wave = 1
                spawn_timer = 0.0
                game_over = False

    if not game_over:
        spawn_timer -= dt
        if spawn_timer <= 0:
            spawn_timer = max(0.25, 1.1 - wave * 0.05)
            spawn(Enemy(random.uniform(30, WIDTH - 30), 70 + wave * 8), enemies)
            if random.random() < 0.12:
                spawn(Pickup((random.uniform(30, WIDTH - 30), -20)), pickups)

        # ---- SIX LINES ----------------------------------------------------
        all_sprites.update(dt)

        for bullet, hit in pygame.sprite.groupcollide(bullets, enemies, True, True).items():
            for enemy in hit:
                burst(enemy.rect.center, (192, 106, 154))
                score += 25

        for pickup in pygame.sprite.spritecollide(player, pickups, True):
            burst(pickup.rect.center, (81, 207, 102), 10)
            score += 50
            player.lives = min(5, player.lives + 1)

        if player.invulnerable <= 0 and pygame.sprite.spritecollideany(player, enemies):
            for enemy in pygame.sprite.spritecollide(player, enemies, True):
                burst(enemy.rect.center, (255, 107, 107), 22)
            player.lives -= 1
            player.invulnerable = 1.4
            if player.lives <= 0:
                game_over = True
        # -------------------------------------------------------------------

        wave = 1 + score // 400

    screen.fill((12, 16, 23))
    all_sprites.draw(screen)

    screen.blit(big.render("SCORE %d" % score, True, (231, 236, 243)), (16, 12))
    for i in range(player.lives):
        screen.blit(pygame.transform.scale(SHIP_IMAGE, (16, 16)), (WIDTH - 40 - i * 22, 16))

    info = [
        "all_sprites %d" % len(all_sprites),
        "enemies %d  bullets %d  effects %d" % (len(enemies), len(bullets), len(effects)),
        "wave %d     %.0f fps" % (wave, clock.get_fps()),
    ]
    for i, line in enumerate(info):
        screen.blit(font.render(line, True, (110, 122, 140)), (16, HEIGHT - 66 + i * 20))

    if game_over:
        screen.blit(big.render("GAME OVER  -  press R", True, (255, 107, 107)),
                    (WIDTH / 2 - 150, HEIGHT / 2))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
