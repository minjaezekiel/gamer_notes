"""
02-slicing-and-timing.py — two clocks, and the three ways to get the timer wrong.

WHAT THIS DEMONSTRATES
    * slicing the sheet ONCE into lists of Surfaces with subsurface
    * the frame timer, with the game clock and the sprite clock shown side by side
    * three switches, each turning on one real mistake:
          B  advance one pose per GAME frame
          Z  timer = 0 instead of timer -= FRAME_TIME   (watch the drift counter)
          I  `if` instead of `while`, then drop the frame cap with F

HOW TO RUN IT
    python3 02-slicing-and-timing.py
      [ ]  slower / faster animation
      F    drop the frame cap to 12 fps
      B Z I  the three bugs

WHAT TO CHANGE FIRST
    Press Z and leave it running for a minute while you do something else. The
    animation looks perfectly fine, and the drift counter climbs the whole time.
"""

import os
import pygame
from spritesheet import make_sheet, slice_sheet, FRAME_W, FRAME_H, ROWS

SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))
WIDTH, HEIGHT = 780, 470

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("02 - slicing and timing")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 19)
big = pygame.font.SysFont(None, 25)

# Built and sliced ONCE, at load time. Never in the loop.
sheet = make_sheet()
rows = slice_sheet(sheet)
walk = rows[ROWS["walk"]]

anim_fps = 8.0
frame_index = 0
timer = 0.0
poses_shown = 0
game_frames = 0

bug_per_frame = False
bug_zero_timer = False
bug_if_not_while = False
low_fps = False

# how far behind the zeroing version falls, measured against the ideal
ideal_poses = 0.0
frames = 0

running = True
while running:
    cap = 12 if low_fps else 60
    dt = clock.tick(cap) / 1000.0
    game_frames += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_b:
                bug_per_frame = not bug_per_frame
            elif event.key == pygame.K_z:
                bug_zero_timer = not bug_zero_timer
                poses_shown = 0
                ideal_poses = 0.0
            elif event.key == pygame.K_i:
                bug_if_not_while = not bug_if_not_while
            elif event.key == pygame.K_f:
                low_fps = not low_fps
            elif event.key == pygame.K_RIGHTBRACKET:
                anim_fps = min(30.0, anim_fps * 1.5)
            elif event.key == pygame.K_LEFTBRACKET:
                anim_fps = max(1.0, anim_fps / 1.5)

    frame_time = 1.0 / anim_fps
    ideal_poses += dt * anim_fps

    # ---- the animation clock ---------------------------------------------
    if bug_per_frame:
        # THE BUG: one pose per game frame. The animation now runs at whatever
        # the frame rate is - a number nobody chose.
        frame_index = (frame_index + 1) % len(walk)
        poses_shown += 1
    else:
        timer += dt
        if bug_if_not_while:
            # `if` advances at most ONE pose, so a slow frame silently drops the
            # rest and the animation runs slow exactly when the machine struggles.
            if timer >= frame_time:
                timer = 0.0 if bug_zero_timer else timer - frame_time
                frame_index = (frame_index + 1) % len(walk)
                poses_shown += 1
        else:
            while timer >= frame_time:
                # SUBTRACT keeps the leftover. Zeroing throws it away and drifts.
                timer = 0.0 if bug_zero_timer else timer - frame_time
                frame_index = (frame_index + 1) % len(walk)
                poses_shown += 1

    image = walk[frame_index]

    # ---- render -----------------------------------------------------------
    screen.fill((20, 24, 32))

    big_image = pygame.transform.scale(image, (FRAME_W * 4, FRAME_H * 4))
    screen.blit(big_image, (60, 120))

    # the sheet, with the current cell boxed - the best debugging aid here
    sheet_zoom = 2
    sx, sy = 300, 120
    screen.blit(pygame.transform.scale(sheet, (sheet.get_width() * sheet_zoom,
                                               sheet.get_height() * sheet_zoom)), (sx, sy))
    pygame.draw.rect(screen, (255, 107, 107),
                     (sx + frame_index * FRAME_W * sheet_zoom,
                      sy + ROWS["walk"] * FRAME_H * sheet_zoom,
                      FRAME_W * sheet_zoom, FRAME_H * sheet_zoom), 2)

    screen.blit(big.render("two clocks", True, (231, 236, 243)), (28, 26))

    left = [
        ("GAME CLOCK", "", (77, 171, 247)),
        ("  frames", "%d" % game_frames, (135, 147, 164)),
        ("  cap", "%d fps  (F)" % cap, (135, 147, 164)),
        ("SPRITE CLOCK", "", (255, 159, 67)),
        ("  pose", "%d of %d" % (frame_index, len(walk)), (135, 147, 164)),
        ("  poses shown", "%d" % poses_shown, (135, 147, 164)),
        ("  rate", "%.1f /s  ([ ])" % anim_fps, (135, 147, 164)),
        ("  ratio", "%.1f game frames per pose"
         % (game_frames / poses_shown if poses_shown else 0), (135, 147, 164)),
    ]
    for i, (label, value, colour) in enumerate(left):
        screen.blit(font.render(label, True, colour), (28, 330 + i * 18))
        if value:
            screen.blit(font.render(value, True, colour), (170, 330 + i * 18))

    # the timer bar
    bar_x, bar_y, bar_w = 300, 330, 200
    pygame.draw.rect(screen, (27, 33, 48), (bar_x, bar_y, bar_w, 12))
    fill = 1.0 if bug_per_frame else min(1.0, timer / frame_time)
    pygame.draw.rect(screen, (255, 159, 67), (bar_x, bar_y, int(bar_w * fill), 12))
    pygame.draw.rect(screen, (43, 50, 64), (bar_x, bar_y, bar_w, 12), 1)
    screen.blit(font.render("timer %.4f / %.4f s" % (timer, frame_time),
                            True, (135, 147, 164)), (bar_x, bar_y + 18))

    drift = ideal_poses - poses_shown
    switches = [
        ("B  one pose per game frame", bug_per_frame),
        ("Z  timer = 0 instead of -=", bug_zero_timer),
        ("I  if instead of while", bug_if_not_while),
    ]
    for i, (label, on) in enumerate(switches):
        screen.blit(font.render(("[x] " if on else "[ ] ") + label,
                                True, (255, 107, 107) if on else (100, 112, 130)),
                    (bar_x, 382 + i * 20))

    if bug_zero_timer or bug_if_not_while:
        screen.blit(font.render("poses behind where it should be: %.1f" % drift,
                                True, (255, 107, 107) if drift > 2 else (255, 212, 59)),
                    (bar_x + 230, 382))
        screen.blit(font.render("(leave it running - this is the point)",
                                True, (100, 112, 130)), (bar_x + 230, 402))
    elif bug_per_frame:
        screen.blit(font.render("running at %d poses a second, which nobody chose" % cap,
                                True, (255, 107, 107)), (bar_x + 230, 382))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
