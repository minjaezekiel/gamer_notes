"""
tilemap.py — loading a level from a file, and the table that says what each
character means.

WHAT THIS IS
    Shared content for this lesson's four examples (see COURSE_SPEC section 9).
    It holds the LEVEL and the loader; the ideas each example is about stay in the
    numbered files.

THE FOUR TRAPS, handled here
    * the trailing newline, which adds an empty row
    * rstrip() eating trailing SPACES as well as the newline
    * rows of different lengths
    * open() using the working directory rather than the script's folder
"""

from pathlib import Path

import pygame

TILE = 32
HERE = Path(__file__).parent

# ---------------------------------------------------------------------------
# THE TILE TABLE. A new tile type is one line here, and nothing else changes.
# ---------------------------------------------------------------------------
TILES = {
    ".": {"solid": False, "colour": None},
    "@": {"solid": False, "colour": None, "start": True},
    "#": {"solid": True,  "colour": (58, 69, 85)},
    "~": {"solid": False, "colour": (28, 79, 124), "slows": True},
    "^": {"solid": False, "colour": (90, 34, 34), "deadly": True},
    "o": {"solid": False, "colour": None, "coin": True},
}
UNKNOWN = {"solid": False, "colour": (90, 20, 100), "unknown": True}


class LevelError(Exception):
    """Raised at LOAD time, with a message naming the row - which is the whole
    reason the check is worth four lines."""


def load_level(filename="level.txt"):
    """Read a level file and return a list of equal-length strings."""
    path = HERE / filename              # not the working directory
    with open(path, encoding="utf-8") as handle:
        # rstrip("\n") only: plain rstrip() would also eat trailing spaces, and a
        # level that uses spaces for empty tiles would quietly lose its right edge.
        lines = [line.rstrip("\n") for line in handle]

    # nearly every editor writes a trailing newline, which makes an empty last row
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        raise LevelError("%s is empty" % path.name)

    width = len(lines[0])
    bad = [i for i, row in enumerate(lines) if len(row) != width]
    if bad:
        raise LevelError("%s: row(s) %s are not %d characters long"
                         % (path.name, bad, width))

    unknown = sorted({c for row in lines for c in row if c not in TILES})
    if unknown:
        # a warning rather than an error: an unknown tile is drawn as a purple
        # question mark, which is easier to find than a crash
        print("warning: unknown tile character(s): %s" % " ".join(unknown))

    return lines


class Tilemap:
    def __init__(self, lines):
        self.lines = lines
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.width = self.cols * TILE
        self.height = self.rows * TILE

    def char_at(self, col, row):
        # OUT OF BOUNDS IS SOLID, except above the map - so a high jump is allowed
        # but walking off the side is not.
        if col < 0 or col >= self.cols:
            return "#"
        if row < 0:
            return "."
        if row >= self.rows:
            return "#"
        return self.lines[row][col]

    def info(self, col, row):
        return TILES.get(self.char_at(col, row), UNKNOWN)

    def is_solid(self, col, row):
        return self.info(col, row)["solid"]

    def start_position(self):
        for row in range(self.rows):
            col = self.lines[row].find("@")
            if col >= 0:
                return pygame.Vector2(col * TILE + TILE / 2, row * TILE + TILE)
        return pygame.Vector2(TILE * 1.5, TILE * 2)

    def tiles_touching(self, rect):
        """Every tile this rect overlaps. At most four for a box smaller than a
        tile. The -1 stops an edge exactly on a boundary counting the next one."""
        c0 = rect.left // TILE
        c1 = (rect.right - 1) // TILE
        r0 = rect.top // TILE
        r1 = (rect.bottom - 1) // TILE
        for row in range(r0, r1 + 1):
            for col in range(c0, c1 + 1):
                yield col, row

    def solid_rects_touching(self, rect):
        out = []
        for col, row in self.tiles_touching(rect):
            if self.is_solid(col, row):
                out.append(pygame.Rect(col * TILE, row * TILE, TILE, TILE))
        return out

    def draw(self, surface, camera_x=0, camera_y=0, view_w=None, view_h=None,
             coins_taken=None):
        """Only the visible tiles. The four lines that stop a big level being slow."""
        view_w = view_w or surface.get_width()
        view_h = view_h or surface.get_height()
        first_col = max(0, int(camera_x // TILE))
        last_col = min(self.cols - 1, int((camera_x + view_w) // TILE) + 1)
        first_row = max(0, int(camera_y // TILE))
        last_row = min(self.rows - 1, int((camera_y + view_h) // TILE) + 1)

        drawn = 0
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                info = self.info(col, row)
                x = col * TILE - camera_x
                y = row * TILE - camera_y
                if info.get("colour"):
                    pygame.draw.rect(surface, info["colour"], (x, y, TILE, TILE))
                    if info["solid"] and not self.is_solid(col, row - 1):
                        pygame.draw.rect(surface, (77, 90, 110), (x, y, TILE, 4))
                    drawn += 1
                if info.get("deadly"):
                    for k in range(3):
                        pygame.draw.polygon(surface, (255, 107, 107),
                                            [(x + 2 + k * 10, y + TILE),
                                             (x + 7 + k * 10, y + TILE - 12),
                                             (x + 12 + k * 10, y + TILE)])
                if info.get("coin"):
                    if coins_taken is not None and (col, row) in coins_taken:
                        continue
                    pygame.draw.circle(surface, (255, 212, 59),
                                       (x + TILE // 2, y + TILE // 2), 7)
                    drawn += 1
                if info.get("unknown"):
                    pygame.draw.rect(surface, info["colour"], (x, y, TILE, TILE))
                    drawn += 1
        return drawn

    def pre_render(self):
        """The whole level onto one Surface, once. Size is
        cols * rows * TILE^2 * 4 bytes - do that multiplication before you try it
        on a big level."""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw(surface, 0, 0, self.width, self.height)
        return surface
