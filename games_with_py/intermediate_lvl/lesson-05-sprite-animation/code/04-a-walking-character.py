"""
04-a-walking-character.py — the lesson assembled.

WHAT THIS DEMONSTRATES
    Everything from this lesson in one Sprite, in a Group, on a small platform
    level: sliced frames, the two clocks, a state table, flipping done once,
    anchored at the feet, and the walk's frame rate matched to the real speed.

    Press C to remove the LOWER clamp from the speed-matched frame rate and then
    stand still: the character freezes mid-stride, which looks like a crash and is
    not.

HOW TO RUN IT
    python3 04-a-walking-character.py
      arrows / WASD  move        SPACE  jump
      C  remove the low clamp        M  match the animation to speed, on/off
      D  draw the sheet with the current cell boxed

WHAT TO CHANGE FIRST
    Press M off and walk slowly, then quickly. The feet slide. Press M on and do it
    again. That is the whole of stretch goal 1 from the web track, and it is four
    lines.
"""

import os
import pygame
from pygame.math import Vector2
from spritesheet import make_sheet, slice_sheet, flip_rows, FRAME_W, FRAME_H, ROWS

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 800, 480
WALK_SPEED = 200
SCALE = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - a walking character")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 26)

sheet = make_sheet()
RIGHT = slice_sheet(sheet)
LEFT = flip_rows(RIGHT)

ANIMATIONS = {
    "idle": {"row": ROWS["idle"], "fps": 2.0, "speed_matched": False},
    "walk": {"row": ROWS["walk"], "fps": 8.0, "speed_matched": True},
    "jump": {"row": ROWS["jump"], "fps": 1.0, "speed_matched": False},
}

PLATFORMS = [
    pygame.Rect(0, 430, WIDTH, 50),
    pygame.Rect(140, 350, 180, 18),
    pygame.Rect(430, 300, 160, 18),
    pygame.Rect(630, 380, 140, 18),
]


class Walker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(90, 430)
        self.vel = Vector2(0, 0)
        self.on_ground = True
        self.facing = 1
        self.state = "idle"
        self.last_state = "idle"
        self.frame = 0
        self.timer = 0.0
        self.poses_shown = 0
        self.image = self._surface()
        self.rect = self.image.get_rect(midbottom=self.pos)

    def _surface(self):
        row = ANIMATIONS[self.state]["row"]
        source = RIGHT if self.facing > 0 else LEFT
        base = source[row][self.frame % len(source[row])]
        return pygame.transform.scale(base, (FRAME_W * SCALE, FRAME_H * SCALE))

    def update(self, dt, speed_matched=True, low_clamp=True):
        keys = pygame.key.get_pressed()
        want = (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) - \
               (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0)
        if want:
            self.facing = want
        self.vel.x = want * WALK_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = -520
            self.on_ground = False
        self.vel.y = min(900, self.vel.y + 1400 * dt)

        # move and land, one axis at a time (lesson 2's collision, simplified)
        self.pos.x += self.vel.x * dt
        self.pos.x = max(20, min(WIDTH - 20, self.pos.x))

        previous_bottom = self.pos.y
        self.pos.y += self.vel.y * dt
        self.on_ground = False
        for p in PLATFORMS:
            if (self.vel.y >= 0 and previous_bottom <= p.top + 2
                    and self.pos.y >= p.top
                    and p.left - 14 < self.pos.x < p.right + 14):
                self.pos.y = p.top
                self.vel.y = 0
                self.on_ground = True

        # ---- state ----
        if not self.on_ground:
            self.state = "jump"
        elif abs(self.vel.x) > 10:
            self.state = "walk"
        else:
            self.state = "idle"
        if self.state != self.last_state:
            self.frame = 0
            self.timer = 0.0
            self.last_state = self.state

        # ---- the frame rate, matched to the real speed ----
        anim = ANIMATIONS[self.state]
        fps = anim["fps"]
        if speed_matched and anim["speed_matched"]:
            factor = abs(self.vel.x) / WALK_SPEED
            # The LOWER clamp is not tidiness: without it a stationary character
            # has a frame time of infinity and freezes mid-stride.
            lo = 0.4 if low_clamp else 0.0
            fps = anim["fps"] * max(lo, min(2.0, factor))

        if fps > 0:
            frame_time = 1.0 / fps
            self.timer += dt
            row_len = len(RIGHT[anim["row"]])
            while self.timer >= frame_time:
                self.timer -= frame_time
                self.frame = (self.frame + 1) % row_len
                self.poses_shown += 1

        self.image = self._surface()
        # anchored at the FEET, so a taller pose grows upwards
        self.rect = self.image.get_rect(midbottom=self.pos)
        self.current_fps = fps


walker = Walker()
everything = pygame.sprite.Group(walker)
speed_matched = True
low_clamp = True
show_sheet = True
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
            elif event.key == pygame.K_c:
                low_clamp = not low_clamp
            elif event.key == pygame.K_m:
                speed_matched = not speed_matched
            elif event.key == pygame.K_d:
                show_sheet = not show_sheet

    everything.update(dt, speed_matched, low_clamp)

    screen.fill((18, 22, 30))
    for p in PLATFORMS:
        pygame.draw.rect(screen, (58, 69, 85), p)
        pygame.draw.rect(screen, (77, 90, 110), (p.x, p.y, p.width, 4))
    everything.draw(screen)

    screen.blit(big.render("state: %s" % walker.state, True, (255, 212, 59)), (22, 20))
    info = [
        "speed        %5.0f px/s" % abs(walker.vel.x),
        "anim rate    %5.1f poses/s" % walker.current_fps,
        "pose         %d" % walker.frame,
        "poses shown  %d" % walker.poses_shown,
        "fps          %5.0f" % clock.get_fps(),
    ]
    for i, line in enumerate(info):
        screen.blit(font.render(line, True, (135, 147, 164)), (22, 52 + i * 20))

    switches = [
        ("M  match animation to speed", speed_matched, False),
        ("C  low clamp", low_clamp, True),
    ]
    for i, (label, on, good_when_on) in enumerate(switches):
        colour = ((81, 207, 102) if on == good_when_on or on else (255, 107, 107)) \
            if good_when_on else ((81, 207, 102) if on else (100, 112, 130))
        screen.blit(font.render(("[x] " if on else "[ ] ") + label, True, colour),
                    (22, HEIGHT - 72 + i * 20))

    if not low_clamp and abs(walker.vel.x) < 1 and walker.state == "walk":
        screen.blit(font.render("no low clamp: frame rate is 0, so the walk is frozen mid-step",
                                True, (255, 107, 107)), (260, HEIGHT - 72))
    elif not speed_matched:
        screen.blit(font.render("fixed 8 poses/s: walk slowly and watch the feet slide",
                                True, (255, 159, 67)), (260, HEIGHT - 72))

    if show_sheet:
        z = 1
        sx, sy = WIDTH - sheet.get_width() * z - 20, 20
        screen.blit(sheet, (sx, sy))
        row = ANIMATIONS[walker.state]["row"]
        pygame.draw.rect(screen, (255, 107, 107),
                         (sx + walker.frame * FRAME_W * z, sy + row * FRAME_H * z,
                          FRAME_W * z, FRAME_H * z), 2)
        screen.blit(font.render("D", True, (74, 83, 98)), (sx - 14, sy))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
