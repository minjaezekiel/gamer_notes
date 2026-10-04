# ============================================================================
# 01 - The same thing, as a dictionary and as a class
# Lesson 6, Games with Python, Beginner
#
# WHAT THIS SHOWS:  A class is a dictionary that also knows what it is and what
#                   it can do. Side by side, so you can see they hold the same
#                   data.
#
# RUN IT:           python3 01-dict-vs-class.py
# TRY THIS:         un-comment the two lines near the bottom marked TYPO and
#                   run it again. Notice WHEN each error appears, and how
#                   helpful each message is.
#
# No graphics in this file. It is about the idea, not the pixels.
# ============================================================================

# ============================================================================
# VERSION A - a dictionary
# ============================================================================
brick_dict = {
    "x": 40,
    "y": 60,
    "w": 68,
    "h": 24,
    "hits": 2,
    "alive": True,
}


# The behaviour lives SOMEWHERE ELSE, in functions you have to remember to
# pass the dictionary to.
def brick_colour(brick):
    return "orange" if brick["hits"] >= 2 else "blue"


def brick_box(brick):
    return (brick["x"], brick["y"], brick["w"], brick["h"])


def brick_hit(brick):
    brick["hits"] -= 1
    if brick["hits"] <= 0:
        brick["alive"] = False


# ============================================================================
# VERSION B - a class
# ============================================================================
class Brick:
    """A brick. Its data AND what it can do, in one place."""

    def __init__(self, x, y, w, h, hits):
        """Runs when you make a new Brick.

        'self' is the brick being made. It is not magic and not a keyword:
        when you later write brick.colour(), Python calls Brick.colour(brick)
        and that first argument is conventionally named self.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hits = hits
        self.alive = True

    def colour(self):
        return "orange" if self.hits >= 2 else "blue"

    def box(self):
        return (self.x, self.y, self.w, self.h)

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.alive = False


brick_obj = Brick(40, 60, 68, 24, hits=2)


# ============================================================================
# THEY HOLD THE SAME DATA
# ============================================================================
print("DICTIONARY                        CLASS")
print("-" * 64)
print(f"brick_dict['x']      = {brick_dict['x']:<10} brick_obj.x      = {brick_obj.x}")
print(f"brick_colour(d)      = {brick_colour(brick_dict):<10} brick_obj.colour() = {brick_obj.colour()}")
print(f"brick_box(d)         = {str(brick_box(brick_dict)):<22} brick_obj.box() = {brick_obj.box()}")

print()
print("Hit each one twice:")
brick_hit(brick_dict)
brick_obj.hit()
print(f"  after 1 hit:  dict alive={brick_dict['alive']}   class alive={brick_obj.alive}")
brick_hit(brick_dict)
brick_obj.hit()
print(f"  after 2 hits: dict alive={brick_dict['alive']}  class alive={brick_obj.alive}")

print()
print("Same data. Same behaviour. The difference is WHERE the behaviour lives,")
print("and what happens when you make a mistake.")

# ============================================================================
# WHAT HAPPENS WHEN YOU MAKE A TYPO
# ============================================================================
print()
print("Reading a key/attribute that does not exist:")

try:
    print(brick_dict["spede"])
except KeyError as error:
    print("  dictionary ->", type(error).__name__, error)

try:
    print(brick_obj.spede)
except AttributeError as error:
    print("  class      ->", type(error).__name__, error)

# ---- TYPO: un-comment these to see a difference that MATTERS ----
# A dictionary happily accepts a brand new key, so this typo is COMPLETELY
# SILENT - you set "spede" and then wonder why the speed never changes.
# brick_dict["spede"] = 99
# print("  dictionary accepted a misspelled key:", brick_dict)
#
# A class will accept this too, by default. Python is flexible that way.
# brick_obj.spede = 99
# print("  the class accepted it too:", brick_obj.spede)
#
# So a class does NOT protect you from every typo. What it DOES give you is:
#   - one obvious place to look to find out what a Brick has
#   - the behaviour next to the data it works on
#   - a name, so the code says "Brick" rather than "some dictionary"

print()
print("A class is NOT always better. For a one-off bag of values a dictionary")
print("is still the right answer. Use a class when a thing has both DATA and")
print("BEHAVIOUR, and there are many of them.")
