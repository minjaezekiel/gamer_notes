"""
spritesheet.py — the sheet, built in code, and the slicer.

WHAT THIS IS
    Shared by the four examples in this lesson so that each of them can be about
    one idea instead of about drawing a character. It is the only file in this
    level that other examples import, and it is here because a spritesheet is
    content rather than a lesson.

    Every number in draw_pose is a fraction of `size`, so one edit resizes the
    whole sheet and nothing distorts (lesson 2).

HOW TO USE IT
    from spritesheet import make_sheet, slice_sheet, FRAME_W, FRAME_H, ROWS
"""

import pygame

FRAME_W = 32
FRAME_H = 40
COLUMNS = 6
ROWS = {"idle": 0, "walk": 1, "jump": 2}

SKIN = (255, 217, 160)
SHIRT = (77, 171, 247)
LEGS = (43, 50, 64)
EYE = (20, 24, 32)


def draw_pose(surface, ox, oy, size_w, size_h, phase, mode):
    """One pose, drawn into a cell whose top-left is (ox, oy).

    `phase` runs 0..1 around the cycle. Everything is relative to the cell size.
    """
    mid = ox + size_w / 2
    swing = pygame.math.Vector2(1, 0).rotate(phase * 360).y     # a sine, via rotate
    bob = abs(pygame.math.Vector2(1, 0).rotate(phase * 360).x) * size_h * 0.03
    head_r = size_w * 0.17
    head_y = oy + size_h * 0.20 + (bob if mode == "walk" else 0)

    if mode == "jump":
        head_y = oy + size_h * 0.16

    pygame.draw.circle(surface, SKIN, (mid, head_y), head_r)
    pygame.draw.rect(surface, SHIRT,
                     (mid - size_w * 0.20, head_y + head_r * 0.7,
                      size_w * 0.40, size_h * 0.30))
    pygame.draw.rect(surface, EYE,
                     (mid + head_r * 0.2, head_y - head_r * 0.25,
                      size_w * 0.07, size_w * 0.07))

    arm_y = head_y + head_r * 0.9
    if mode == "jump":
        pygame.draw.rect(surface, SKIN, (mid - size_w * 0.34, arm_y - size_h * 0.06,
                                         size_w * 0.12, size_h * 0.18))
        pygame.draw.rect(surface, SKIN, (mid + size_w * 0.22, arm_y - size_h * 0.06,
                                         size_w * 0.12, size_h * 0.18))
    else:
        pygame.draw.rect(surface, SKIN,
                         (mid - size_w * 0.30 - swing * size_w * 0.10, arm_y,
                          size_w * 0.11, size_h * 0.17))
        pygame.draw.rect(surface, SKIN,
                         (mid + size_w * 0.19 + swing * size_w * 0.10, arm_y,
                          size_w * 0.11, size_h * 0.17))

    hip_y = head_y + head_r * 0.7 + size_h * 0.30
    if mode == "jump":
        pygame.draw.rect(surface, LEGS, (mid - size_w * 0.18, hip_y,
                                         size_w * 0.13, size_h * 0.24))
        pygame.draw.rect(surface, LEGS, (mid + size_w * 0.05, hip_y,
                                         size_w * 0.13, size_h * 0.17))
    elif mode == "idle":
        pygame.draw.rect(surface, LEGS, (mid - size_w * 0.18, hip_y,
                                         size_w * 0.13, size_h * 0.26))
        pygame.draw.rect(surface, LEGS, (mid + size_w * 0.05, hip_y,
                                         size_w * 0.13, size_h * 0.26))
    else:
        lead = swing * size_w * 0.14
        pygame.draw.rect(surface, LEGS, (mid - size_w * 0.18 + lead, hip_y,
                                         size_w * 0.13, size_h * 0.26))
        pygame.draw.rect(surface, LEGS, (mid + size_w * 0.05 - lead, hip_y,
                                         size_w * 0.13, size_h * 0.26))


def make_sheet(frame_w=FRAME_W, frame_h=FRAME_H, columns=COLUMNS):
    """One Surface, three rows of `columns` poses. No files involved."""
    sheet = pygame.Surface((frame_w * columns, frame_h * len(ROWS)), pygame.SRCALPHA)
    for i in range(columns):
        # idle: two poses that matter, repeated
        draw_pose(sheet, i * frame_w, ROWS["idle"] * frame_h,
                  frame_w, frame_h, (i % 2) / 2.0, "idle")
        # walk: a full cycle across all the columns
        draw_pose(sheet, i * frame_w, ROWS["walk"] * frame_h,
                  frame_w, frame_h, i / columns, "walk")
        # jump: one pose, repeated so every row is the same width
        draw_pose(sheet, i * frame_w, ROWS["jump"] * frame_h,
                  frame_w, frame_h, 0.0, "jump")
    return sheet


def slice_sheet(sheet, frame_w=FRAME_W, frame_h=FRAME_H):
    """One list of Surfaces per row. Done ONCE, at load time, never in the loop.

    subsurface SHARES the sheet's pixels - nothing is copied - so this is free.
    The sheet must stay alive and must not be drawn over afterwards.
    """
    rows = []
    for row in range(sheet.get_height() // frame_h):
        frames = []
        for col in range(sheet.get_width() // frame_w):
            rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
            frames.append(sheet.subsurface(rect))
        rows.append(frames)
    return rows


def flip_rows(rows):
    """Both directions, built ONCE. transform.flip makes a new Surface every
    call, so doing it per frame is the easiest way to make a pygame game slow."""
    return [[pygame.transform.flip(f, True, False) for f in row] for row in rows]
