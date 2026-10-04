# ============================================================================
# 03 - THE TEXT ADVENTURE  (the finished lesson 1 result)
# Lesson 1, Games with Python, Beginner
#
# WHAT THIS SHOWS:  A complete game with no graphics at all. State, a loop,
#                   a world described as DATA, and commands in a dictionary.
#
# RUN IT:           python3 03-adventure.py
#
# CHANGE ME FIRST:  The ROOMS dictionary below. Add a room. You will not have
#                   to change a single line of the code that moves the player -
#                   that is what "data-driven" means.
#
# BREAK IT:         Remove the "global" from cmd_quit and try to quit. Python
#                   reports no error. The game simply refuses to stop, and
#                   nothing tells you why.
# ============================================================================

import random

MAX_HEALTH = 20

# ============================================================================
# THE WORLD - this is DATA, not code.
#
# Every room is a dictionary. The whole map is a dictionary of them. Adding a
# twentieth room means adding data here; the go() function never changes.
# ============================================================================
ROOMS = {
    "cavern": {
        "description": "A dark cavern. Water drips somewhere you cannot see.",
        "exits": {"north": "tunnel", "east": "pool"},
        "items": ["torch"],
    },
    "tunnel": {
        "description": "A narrow tunnel. The air is colder here.",
        "exits": {"south": "cavern", "north": "chamber"},
        "items": [],
    },
    "pool": {
        "description": "A still black pool. Something glints under the water.",
        "exits": {"west": "cavern"},
        "items": ["rusty key"],
    },
    "chamber": {
        "description": "A high chamber. Carvings cover every wall.",
        "exits": {"south": "tunnel", "east": "vault"},
        "items": [],
        "monster": "a cave troll",
    },
    "vault": {
        "description": "The vault. A chest sits in the centre, closed.",
        "exits": {"west": "chamber"},
        "items": ["gold hoard"],
        "needs_key": "rusty key",   # you cannot enter without this
    },
}

# ============================================================================
# STATE - everything the game remembers between turns.
# ============================================================================
current_room = "cavern"
player_health = MAX_HEALTH
inventory = []
playing = True
turns = 0


# ============================================================================
# RENDER - these functions SHOW the state. They never change it.
# ============================================================================
def show_room():
    room = ROOMS[current_room]
    print()
    print("-" * 52)
    print(" ", current_room.upper())
    print(" ", room["description"])
    print("-" * 52)
    print("  health:", player_health, "/", MAX_HEALTH, end="     ")
    if inventory:
        print("carrying:", ", ".join(inventory))
    else:
        print("carrying: nothing")

    if room["items"]:
        print("  You can see:", ", ".join(room["items"]))
    if "monster" in room:
        print("  DANGER:", room["monster"], "blocks your way!")

    # The exits are read from the DATA, so this is right automatically for any
    # room anyone ever adds.
    print("  Exits:", ", ".join(sorted(room["exits"])))
    print()


# ============================================================================
# UPDATE - these functions CHANGE the state.
# ============================================================================
def go(direction):
    global current_room, player_health
    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("You cannot go that way.")
        return

    destination = exits[direction]

    # A locked door. Notice this is NOT special-cased for the vault: the
    # requirement lives in the room data, so any room can be locked by adding
    # one line to ROOMS and changing nothing here.
    needed = ROOMS[destination].get("needs_key")
    if needed is not None and needed not in inventory:
        print("The way is locked. You need:", needed)
        return

    # A monster in the room you are LEAVING gets a free hit.
    if "monster" in ROOMS[current_room]:
        damage = random.randint(2, 5)
        player_health = max(0, player_health - damage)
        print(ROOMS[current_room]["monster"], "strikes you for", damage, "as you flee!")

    current_room = destination


def take(what):
    room = ROOMS[current_room]
    if what in room["items"]:
        room["items"].remove(what)      # it leaves the room...
        inventory.append(what)          # ...and joins your inventory
        print("You take the", what + ".")
    else:
        print("There is no", what, "here.")


def fight():
    global player_health
    room = ROOMS[current_room]
    if "monster" not in room:
        print("There is nothing here to fight.")
        return

    monster = room["monster"]
    if "torch" not in inventory:
        print("It is too dark to fight", monster, "without a light.")
        return

    damage = random.randint(1, 7)
    player_health = max(0, player_health - damage)
    print("You drive", monster, "back with the torch! It wounds you for", damage, ".")

    if random.random() < 0.45:
        del room["monster"]             # remove the key from the dictionary
        print(monster, "flees into the dark.")


# ============================================================================
# COMMANDS - a dictionary of functions.
#
# Once you have more than about four commands, a chain of elif starts to hurt.
# A dictionary is tidier, and - more usefully - it lets the game list its own
# commands, so "help" can never be out of date.
# ============================================================================
def cmd_look(rest):
    show_room()


def cmd_go(rest):
    if not rest:
        print("Go where?")
        return
    go(rest[0])


def cmd_take(rest):
    if not rest:
        print("Take what?")
        return
    take(" ".join(rest))        # join, so "take rusty key" works


def cmd_fight(rest):
    fight()


def cmd_quit(rest):
    global playing
    # WITHOUT this "global", Python creates a brand new local variable called
    # playing, sets it to False, and throws it away when the function ends.
    # No error. The game just will not quit.
    playing = False
    print("You leave the caves.")


def cmd_help(rest):
    print("Commands:", ", ".join(sorted(COMMANDS)))


COMMANDS = {
    "look": cmd_look,
    "go": cmd_go,
    "take": cmd_take,
    "fight": cmd_fight,
    "help": cmd_help,
    "quit": cmd_quit,
    # Shortcuts, so "north" works as well as "go north".
    "north": lambda rest: go("north"),
    "south": lambda rest: go("south"),
    "east": lambda rest: go("east"),
    "west": lambda rest: go("west"),
}


# ============================================================================
# THE GAME LOOP
# ============================================================================
print("THE CAVERNS")
print("Type 'help' for commands.")

while playing:
    # ---- RENDER ----
    show_room()

    # ---- INPUT ----
    raw = input("> ")
    # .strip() removes spaces at the ends, .lower() makes case not matter.
    # Being forgiving here is not politeness: a player who types "GO NORTH"
    # and is told "unknown command" concludes your game is broken.
    words = raw.strip().lower().split()

    if not words:
        continue                # they just pressed enter; ask again

    verb = words[0]
    rest = words[1:]

    # ---- UPDATE ----
    if verb in COMMANDS:
        COMMANDS[verb](rest)
    else:
        print("I do not know how to", repr(verb) + ".", "Try 'help'.")

    turns = turns + 1

    # ---- the game can end without the player choosing ----
    if player_health <= 0:
        print()
        print("You collapse in the dark. You survived", turns, "turns.")
        playing = False
    elif "gold hoard" in inventory:
        print()
        print("You have the hoard! You escape rich, in", turns, "turns.")
        playing = False

print()
print("Goodbye.")
