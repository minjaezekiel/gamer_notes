"""
03-state-driven.py — the state picks the animation, not the keyboard.

WHAT THIS DEMONSTRATES
    * an ANIMATIONS table: the only place in the program that knows about rows
    * the game decides what the character is DOING; the table decides what is shown
    * resetting the frame when the state CHANGES - and press E to use `==` instead
      of `!=` and watch the animation stick on pose 0 for ever
    * flipping done ONCE at startup, with a switch (P) to do it per frame instead
      so you can watch the frame rate fall

HOW TO RUN IT
    python3 03-state-driven.py
      arrows / WASD  move        SPACE  jump
      E  the `==` bug        P  flip every frame        T  show the table

WHAT TO CHANGE FIRST
    Add a fourth entry to ANIMATIONS - "hurt", row 2, fps 6 - and one condition in
    the state block. Nothing else in the file has to change. That is what the table
    is for.
"""

import os
import pygame
from pygame.math import Vector2
from spritesheet import make_sheet, slice_sheet, flip_rows, FRAME_W, FRAME_H, ROWS

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 780, 470
GROUND_Y = 360

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("03 - state driven")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

sheet = make_sheet()
RIGHT = slice_sheet(sheet)          # built once
LEFT = flip_rows(RIGHT)             # flipped once

# ---------------------------------------------------------------------------
# THE TABLE. The only place that knows which row is which, or how fast.
# Adding an animation is one line here and one condition below.
# ---------------------------------------------------------------------------
ANIMATIONS = {
    "idle": {"row": ROWS["idle"], "fps": 2.0},
    "walk": {"row": ROWS["walk"], "fps": 8.0},
    "jump": {"row": ROWS["jump"], "fps": 1.0},
}


class Character:
    def __init__(self):
        self.pos = Vector2(WIDTH / 2, GROUND_Y)
        self.vel = Vector2(0, 0)
        self.on_ground = True
        self.facing = 1
        self.state = "idle"
        self.last_state = "idle"
        self.frame = 0
        self.timer = 0.0
        self.resets = 0
        self.image = RIGHT[ROWS["idle"]][0]
        self.rect = self.image.get_rect(midbottom=self.pos)

    def update(self, dt, use_equals_bug, flip_per_frame):
        keys = pygame.key.get_pressed()
        want = (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) - \
               (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0)
        if want:
            self.facing = want
        self.vel.x = want * 190

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = -470
            self.on_ground = False

        self.vel.y += 1300 * dt
        self.pos += self.vel * dt
        if self.pos.y >= GROUND_Y:
            self.pos.y = GROUND_Y
            self.vel.y = 0
            self.on_ground = True
        self.pos.x = max(30, min(WIDTH - 30, self.pos.x))

        # ---- 1. what is the character DOING? No pictures in this block. ----
        if not self.on_ground:
            self.state = "jump"
        elif abs(self.vel.x) > 10:
            self.state = "walk"
        else:
            self.state = "idle"

        # ---- 2. a CHANGE of state restarts the animation ----
        if use_equals_bug:
            # THE BUG: this fires on every frame the state IS walk, so the timer
            # is reset before it can ever reach frame_time.
            if self.state == "walk":
                self.frame = 0
                self.timer = 0.0
                self.resets += 1
        else:
            if self.state != self.last_state:
                self.frame = 0
                self.timer = 0.0
                self.resets += 1
        self.last_state = self.state

        # ---- 3. the frame timer ----
        anim = ANIMATIONS[self.state]
        frames_in_row = RIGHT[anim["row"]]
        frame_time = 1.0 / anim["fps"]
        self.timer += dt
        while self.timer >= frame_time:
            self.timer -= frame_time
            self.frame = (self.frame + 1) % len(frames_in_row)

        # ---- 4. pick the Surface ----
        if flip_per_frame:
            # the slow way: a new Surface every frame, for every character
            base = RIGHT[anim["row"]][self.frame]
            self.image = pygame.transform.flip(base, True, False) if self.facing < 0 else base
        else:
            source = RIGHT if self.facing > 0 else LEFT
            self.image = source[anim["row"]][self.frame]

        # keep the FEET where they were: a taller pose grows upwards
        self.rect = self.image.get_rect(midbottom=self.pos)


character = Character()
use_equals_bug = False
flip_per_frame = False
show_table = True
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
            elif event.key == pygame.K_e:
                use_equals_bug = not use_equals_bug
                character.resets = 0
            elif event.key == pygame.K_p:
                flip_per_frame = not flip_per_frame
            elif event.key == pygame.K_t:
                show_table = not show_table

    character.update(dt, use_equals_bug, flip_per_frame)

    screen.fill((20, 24, 32))
    pygame.draw.rect(screen, (33, 40, 52), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

    scaled = pygame.transform.scale(character.image, (FRAME_W * 3, FRAME_H * 3))
    screen.blit(scaled, scaled.get_rect(midbottom=character.pos))

    screen.blit(big.render("state: %s" % character.state, True, (255, 212, 59)), (28, 24))
    info = [
        "frame        %d" % character.frame,
        "facing       %s" % ("right" if character.facing > 0 else "left"),
        "on_ground    %s" % character.on_ground,
        "frame resets %d" % character.resets,
        "fps          %.0f" % clock.get_fps(),
    ]
    for i, line in enumerate(info):
        screen.blit(font.render(line, True, (135, 147, 164)), (28, 56 + i * 20))

    if show_table:
        screen.blit(font.render("ANIMATIONS", True, (231, 236, 243)), (WIDTH - 260, 24))
        for i, (name, spec) in enumerate(ANIMATIONS.items()):
            on = name == character.state
            screen.blit(font.render("%-6s row %d  %.0f fps" % (name, spec["row"], spec["fps"]),
                                    True, (255, 212, 59) if on else (110, 122, 140)),
                        (WIDTH - 260, 50 + i * 20))
        screen.blit(font.render("adding one is one line here", True, (74, 83, 98)),
                    (WIDTH - 260, 120))

    switches = [
        ("E  reset with == instead of !=", use_equals_bug),
        ("P  flip every frame", flip_per_frame),
    ]
    for i, (label, on) in enumerate(switches):
        screen.blit(font.render(("[x] " if on else "[ ] ") + label,
                                True, (255, 107, 107) if on else (100, 112, 130)),
                    (WIDTH - 310, HEIGHT - 58 + i * 20))

    if use_equals_bug:
        screen.blit(font.render("walk is stuck on pose 0: the reset fires every frame, "
                                "not on the change", True, (255, 107, 107)),
                    (28, HEIGHT - 26))
    elif flip_per_frame:
        screen.blit(font.render("a new flipped Surface every frame - watch the fps with "
                                "several characters", True, (255, 159, 67)),
                    (28, HEIGHT - 26))
    else:
        screen.blit(font.render("arrows move, space jumps - the state picks the row",
                                True, (74, 83, 98)), (28, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
