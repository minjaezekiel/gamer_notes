#!/usr/bin/env python3
"""Check that every key and the exit can actually be reached from the start.

TEACHER-FACING. Run it with:   python3 test_maze_reachable.py

WHY THIS EXISTS
A maze with an unreachable key is a broken lesson, and you cannot tell by
looking - especially after you have edited it. This does a flood fill from the
player's starting square and reports anything it cannot get to.

If you change the MAZE in ../code/03-maze-walker.cpp, paste the new one in
below and run this before teaching from it.
"""
from collections import deque
import sys

# Keep this in step with MAZE in ../code/03-maze-walker.cpp
MAZE = [
    "##############################",
    "#@...#........#..........#...#",
    "#.##.#.######.#.########.#.#.#",
    "#.#..........*....#....*.#.#.#",
    "#.#.####.#####.##.#.####.#.#.#",
    "#...#......#......#....#...#E#",
    "#.#########.######.###.#####.#",
    "#..........#.....*.....#.....#",
    "##############################",
]

HEIGHT = len(MAZE)
WIDTH = len(MAZE[0])

# Every row must be the same length, or the C++ code reads past the end of a
# string - which is an out-of-bounds read, exactly the bug lesson 3 warned about.
ragged = [i for i, row in enumerate(MAZE) if len(row) != WIDTH]
if ragged:
    sys.exit(f"FAIL: rows {ragged} are not {WIDTH} characters wide")

start = next((x, y) for y in range(HEIGHT) for x in range(WIDTH)
             if MAZE[y][x] == '@')
keys = [(x, y) for y in range(HEIGHT) for x in range(WIDTH) if MAZE[y][x] == '*']
exits = [(x, y) for y in range(HEIGHT) for x in range(WIDTH) if MAZE[y][x] == 'E']

# Flood fill: walk everywhere that is not a wall, starting from the player.
seen = {start}
queue = deque([start])
while queue:
    x, y = queue.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if (0 <= nx < WIDTH and 0 <= ny < HEIGHT
                and (nx, ny) not in seen and MAZE[ny][nx] != '#'):
            seen.add((nx, ny))
            queue.append((nx, ny))

print(f"  grid {WIDTH} x {HEIGHT}, start at {start}, {len(seen)} squares reachable")

unreachable = []
for kind, places in (("key", keys), ("exit", exits)):
    for place in places:
        ok = place in seen
        print(f"  {'ok  ' if ok else 'FAIL'} {kind} at {place}")
        if not ok:
            unreachable.append((kind, place))

if not keys:
    print("  note: this maze has no keys, so the exit is unlocked from the start")
if not exits:
    sys.exit("FAIL: there is no exit")

print()
if unreachable:
    sys.exit(f"MAZE IS BROKEN: {len(unreachable)} unreachable target(s)")
print("MAZE IS PLAYABLE")
