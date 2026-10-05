"""
01-your-first-sprite.py — the contract, and the three ways to break it.

WHAT THIS DEMONSTRATES
    A Sprite needs exactly two attributes - self.image and self.rect - and
    super().__init__() in its constructor. Press 1, 2 or 3 to spawn a sprite with
    one of those three things missing, and read the EXACT error each one produces.

    Those three messages account for most of the time people lose in this lesson,
    and all three come from inside pygame rather than from your own file.

HOW TO RUN IT
    python3 01-your-first-sprite.py
      SPACE  spawn a correct sprite
      1  spawn one with no super().__init__()
      2  spawn one whose image is called `picture`
      3  spawn one whose rect is called `box`
      C  clear

WHAT TO CHANGE FIRST
    Press 1, 2 and 3 in turn and copy the three error messages into your notes.
    You will meet all three again in lesson 5.
"""

import os
import random
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 760, 440
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("01 - your first sprite")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 26)


def make_blob(size, colour):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(s, colour, (size // 2, size // 2), size // 2 - 1)
    pygame.draw.circle(s, (255, 255, 255), (size // 3, size // 3), max(2, size // 8))
    return s


class Blob(pygame.sprite.Sprite):
    """The correct version. Two attributes and one call."""

    def __init__(self, pos, velocity):
        super().__init__()                       # (1) the bookkeeping line
        self.image = make_blob(26, (77, 171, 247))   # (2) must be called `image`
        self.rect = self.image.get_rect(center=pos)  # (3) must be called `rect`
        self.pos = Vector2(pos)                  # floats: the real position
        self.velocity = velocity

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos              # ints, for drawing and colliding
        if not screen.get_rect().inflate(80, 80).collidepoint(self.rect.center):
            # kill() removes this sprite from EVERY group it is in. No searching,
            # no removing while iterating, no index bookkeeping.
            self.kill()


class NoSuper(Blob):
    def __init__(self, pos, velocity):
        # super().__init__() deliberately missing
        self.image = make_blob(26, (255, 107, 107))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.velocity = velocity


class WrongImageName(pygame.sprite.Sprite):
    def __init__(self, pos, velocity):
        super().__init__()
        self.picture = make_blob(26, (255, 212, 59))     # not `image`
        self.rect = self.picture.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.velocity = velocity

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos


class WrongRectName(pygame.sprite.Sprite):
    def __init__(self, pos, velocity):
        super().__init__()
        self.image = make_blob(26, (81, 207, 102))
        self.box = self.image.get_rect(center=pos)       # not `rect`
        self.pos = Vector2(pos)
        self.velocity = velocity

    def update(self, dt):
        self.pos += self.velocity * dt
        self.box.center = self.pos


all_sprites = pygame.sprite.Group()
last_error = ""
last_tried = ""
frames = 0


def random_velocity():
    return Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(90, 210)


def spawn(kind):
    """Each attempt is wrapped so the page can REPORT the error instead of dying.
    In your own game these are ordinary crashes - which is the point."""
    global last_error, last_tried
    last_tried = kind
    pos = (WIDTH / 2, HEIGHT / 2)
    try:
        if kind == "correct":
            all_sprites.add(Blob(pos, random_velocity()))
        elif kind == "no super":
            all_sprites.add(NoSuper(pos, random_velocity()))
        elif kind == "image misspelled":
            all_sprites.add(WrongImageName(pos, random_velocity()))
        elif kind == "rect misspelled":
            all_sprites.add(WrongRectName(pos, random_velocity()))
        last_error = ""
    except Exception as err:                     # noqa: BLE001 - reporting
        last_error = "%s: %s" % (type(err).__name__, err)


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                spawn("correct")
            elif event.key == pygame.K_1:
                spawn("no super")
            elif event.key == pygame.K_2:
                spawn("image misspelled")
            elif event.key == pygame.K_3:
                spawn("rect misspelled")
            elif event.key == pygame.K_c:
                all_sprites.empty()
                last_error = ""
                last_tried = ""

    # one line updates everything
    all_sprites.update(dt)

    screen.fill((20, 24, 32))

    # one line draws everything - and this is where a missing image or rect is
    # discovered, which is why the traceback points at pygame and not at you
    try:
        all_sprites.draw(screen)
    except Exception as err:                     # noqa: BLE001 - reporting
        last_error = "%s: %s   (raised by draw)" % (type(err).__name__, err)
        # drop the broken sprite so the demo keeps running
        for s in list(all_sprites):
            if not hasattr(s, "image") or not hasattr(s, "rect"):
                all_sprites.remove(s)

    screen.blit(big.render("sprites alive: %d" % len(all_sprites), True, (231, 236, 243)),
                (18, 16))
    keys_help = [
        "SPACE  a correct sprite",
        "1      no super().__init__()",
        "2      image called `picture`",
        "3      rect called `box`",
        "C      clear",
    ]
    for i, line in enumerate(keys_help):
        screen.blit(font.render(line, True, (135, 147, 164)), (18, 48 + i * 20))

    if last_tried:
        screen.blit(font.render("last tried: %s" % last_tried, True, (255, 212, 59)),
                    (18, HEIGHT - 62))
    if last_error:
        screen.blit(font.render(last_error[:86], True, (255, 107, 107)), (18, HEIGHT - 40))
        screen.blit(font.render("note where that error came from: inside pygame, not your file",
                                True, (135, 147, 164)), (18, HEIGHT - 20))
    elif last_tried:
        screen.blit(font.render("no error", True, (81, 207, 102)), (18, HEIGHT - 40))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        # exercise every path before leaving, so the checker really tests them
        if frames == SELFTEST_FRAMES:
            for kind in ("correct", "no super", "image misspelled", "rect misspelled"):
                spawn(kind)
        running = False

pygame.quit()
