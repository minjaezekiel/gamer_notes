"""
04-chase-and-flee.py — one recipe, four behaviours.

WHAT THIS DEMONSTRATES
    subtract, normalise, scale - and how little has to change to turn chasing into
    fleeing, orbiting, or a guard with a field of view.

        CHASE   d = (player - me).normalize()
        FLEE    d = (me - player).normalize()      the SAME LINE, swapped
        ORBIT   d turned 90 degrees: Vector2(-d.y, d.x)
        CONE    facing.dot(to_player) > 0.7

    Press G to remove the zero-length guard, then let a chaser reach you. The game
    stops with ValueError: Can't normalize Vector of length zero - which is the
    error this whole lesson exists to make familiar.

HOW TO RUN IT
    python3 04-chase-and-flee.py
      arrows or WASD   move, or drag with the mouse
      G  remove the zero-length guard
      1 2 3  how close a chaser is allowed to get

WHAT TO CHANGE FIRST
    Press G, then stand still and let the red chaser reach you exactly. Read the
    traceback: it names the line, which is what makes Python's behaviour kinder
    than JavaScript's silent NaN.
"""

import math
import os
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 780, 470
SELFTEST_FRAMES = int(os.environ.get("SELFTEST_FRAMES", "0"))

PLAYER_SPEED = 250
AGENT_SPEED = 135
CONE = 0.7                 # cos 45 degrees
GUARD_SIGHT = 240

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("04 - chase and flee")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
big = pygame.font.SysFont(None, 26)

player = Vector2(WIDTH / 2, HEIGHT / 2)
agents = [
    {"pos": Vector2(90, 90),  "kind": "chase", "colour": (255, 107, 107)},
    {"pos": Vector2(660, 110), "kind": "flee",  "colour": (81, 207, 102)},
    {"pos": Vector2(120, 380), "kind": "orbit", "colour": (255, 212, 59)},
]
guard = {"pos": Vector2(620, 370), "angle": 200.0, "sees": False}

use_guard = True
stop_distance = 24
crashed = ""
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
            elif event.key == pygame.K_g:
                use_guard = not use_guard
                crashed = ""
            elif event.key == pygame.K_1:
                stop_distance = 0
            elif event.key == pygame.K_2:
                stop_distance = 24
            elif event.key == pygame.K_3:
                stop_distance = 60
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            player = Vector2(event.pos)

    keys = pygame.key.get_pressed()
    move = Vector2(
        (1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0) -
        (1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0),
        (1 if keys[pygame.K_DOWN] or keys[pygame.K_s] else 0) -
        (1 if keys[pygame.K_UP] or keys[pygame.K_w] else 0),
    )
    # The same guard, on the player's own movement: with no key held this is the
    # zero vector, and normalising it would raise.
    if move.length_squared() > 0:
        player += move.normalize() * PLAYER_SPEED * dt
    player.x = max(14, min(WIDTH - 14, player.x))
    player.y = max(14, min(HEIGHT - 14, player.y))

    # ---- the three simple agents -----------------------------------------
    for a in agents:
        gap = player - a["pos"]              # 1. SUBTRACT: target minus me

        if use_guard and gap.length_squared() == 0:
            continue                         # nothing sensible to do: skip
        try:
            direction = gap.normalize()      # 2. NORMALISE
        except ValueError as err:
            crashed = "ValueError: %s" % err
            continue

        if a["kind"] == "flee":
            direction = -direction           # the same line, reversed
        elif a["kind"] == "orbit":
            sideways = Vector2(-direction.y, direction.x)   # turn 90 degrees
            direction = (sideways + direction * 0.22).normalize()

        # 3. SCALE, then add. Stopping short keeps the gap non-zero, which is the
        # other half of the fix.
        if a["kind"] != "chase" or gap.length() > stop_distance:
            a["pos"] += direction * AGENT_SPEED * dt        # mutates in place
        a["pos"].x = max(12, min(WIDTH - 12, a["pos"].x))
        a["pos"].y = max(12, min(HEIGHT - 12, a["pos"].y))

    # ---- the guard: a field of view from one dot product ------------------
    to_player = player - guard["pos"]
    facing = Vector2(1, 0).rotate(guard["angle"])
    in_range = to_player.length_squared() < GUARD_SIGHT * GUARD_SIGHT
    dot = facing.dot(to_player.normalize()) if to_player.length_squared() > 0 else 1.0
    guard["sees"] = in_range and dot > CONE
    if guard["sees"]:
        guard["pos"] += to_player.normalize() * AGENT_SPEED * 1.1 * dt
        guard["angle"] = Vector2(1, 0).angle_to(to_player)
    else:
        guard["angle"] += 40 * dt

    # ---- render -----------------------------------------------------------
    screen.fill((15, 20, 27))

    # the cone, drawn from the same numbers the test uses
    half = math.degrees(math.acos(CONE))
    points = [guard["pos"]]
    steps = 14
    for i in range(steps + 1):
        a_deg = guard["angle"] - half + (2 * half) * i / steps
        points.append(guard["pos"] + Vector2(1, 0).rotate(a_deg) * GUARD_SIGHT)
    cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(cone_surface,
                        (255, 107, 107, 40) if guard["sees"] else (77, 171, 247, 30),
                        points)
    screen.blit(cone_surface, (0, 0))

    for a in agents:
        pygame.draw.circle(screen, a["colour"], a["pos"], 11)
        gap = player - a["pos"]
        if gap.length_squared() > 0:
            d = gap.normalize()
            if a["kind"] == "flee":
                d = -d
            elif a["kind"] == "orbit":
                d = (Vector2(-d.y, d.x) + d * 0.22).normalize()
            pygame.draw.line(screen, a["colour"], a["pos"], a["pos"] + d * 36, 2)
        screen.blit(font.render(a["kind"], True, a["colour"]),
                    (a["pos"].x - 18, a["pos"].y - 30))

    pygame.draw.circle(screen, (255, 107, 107) if guard["sees"] else (77, 171, 247),
                       guard["pos"], 12)
    screen.blit(font.render("SEES YOU" if guard["sees"] else "watching", True,
                            (255, 107, 107) if guard["sees"] else (77, 171, 247)),
                (guard["pos"].x - 30, guard["pos"].y - 32))

    pygame.draw.circle(screen, (231, 236, 243), player, 13)

    screen.blit(big.render("one recipe, four behaviours", True, (231, 236, 243)), (16, 14))
    info = [
        "guard clause (G)   %s" % ("on" if use_guard else "OFF - will raise"),
        "chaser stops at    %d px   (1 2 3)" % stop_distance,
        "facing . toPlayer  %.2f   (needs > %.2f)" % (dot, CONE),
    ]
    for i, line in enumerate(info):
        colour = (255, 107, 107) if (i == 0 and not use_guard) else (135, 147, 164)
        screen.blit(font.render(line, True, colour), (16, 46 + i * 20))

    if crashed:
        screen.blit(font.render(crashed, True, (255, 107, 107)), (16, HEIGHT - 26))
    elif not use_guard and stop_distance == 0:
        screen.blit(font.render("stand still and let the red one reach you exactly",
                                True, (255, 212, 59)), (16, HEIGHT - 26))

    pygame.display.flip()

    frames += 1
    if SELFTEST_FRAMES and frames >= SELFTEST_FRAMES:
        running = False

pygame.quit()
