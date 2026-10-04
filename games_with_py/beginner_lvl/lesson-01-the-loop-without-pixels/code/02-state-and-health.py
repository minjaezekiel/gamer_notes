# ============================================================================
# 02 - State the player actually cares about
# Lesson 1, Games with Python, Beginner
#
# WHAT THIS SHOWS:  Keeping the game's numbers in variables, and keeping the
#                   code that CHANGES them separate from the code that SHOWS
#                   them.
#
# RUN IT:           python3 02-state-and-health.py
# CHANGE ME FIRST:  MAX_HEALTH on line 20. Try 5, then fight a few times.
# TRY THIS:         remove the max(0, ...) and let your health go negative.
#                   Would a player think that was a bug? (Yes.)
# ============================================================================

import random

# ---- CONSTANTS -------------------------------------------------------------
# CAPITALS by convention means "this never changes while the game runs", so a
# reader knows not to go looking for where it gets modified.
MAX_HEALTH = 20

# ---- STATE -----------------------------------------------------------------
# Everything the game remembers. Write these five values on paper, restart the
# program tomorrow and type them back in, and the game carries on exactly where
# it left off. THAT is what state means - and it is why saving a game is
# possible at all.
player_health = MAX_HEALTH
inventory = []
gold = 0
playing = True


def show_status():
    """RENDER only. Shows the state; changes nothing.

    That promise matters. If you ever find yourself changing player_health
    inside a function like this, you have mixed up update and render - which
    is where a whole category of confusing bugs comes from.
    """
    print()
    print("-" * 46)
    print("  health:", player_health, "/", MAX_HEALTH)
    print("  gold:  ", gold)
    if inventory:
        # ", ".join(list) glues a list into one string with commas between.
        print("  carrying:", ", ".join(inventory))
    else:
        print("  carrying: nothing")
    print("-" * 46)


def fight():
    """UPDATE only. Changes the state; prints only what just happened."""
    global player_health, gold
    # "global" tells Python: change the variable OUTSIDE this function, not a
    # new local one. Forget it and Python silently makes a local variable,
    # changes that, throws it away, and reports no error at all.

    damage = random.randint(1, 6)
    reward = random.randint(2, 9)

    # max(0, x) means "whichever is bigger, 0 or x" - so health can never go
    # below zero and the player never sees "health: -3". This is CLAMPING, and
    # you will use it for health bars, scores, timers and ammunition.
    player_health = max(0, player_health - damage)
    gold = gold + reward

    print("You fight a goblin. It hits you for", damage, "damage.")
    print("You find", reward, "gold on its body.")


def rest():
    """UPDATE only."""
    global player_health
    # min(MAX_HEALTH, x) clamps the other way: never heal above the maximum.
    healed = min(MAX_HEALTH, player_health + 8)
    print("You rest. Health:", player_health, "->", healed)
    player_health = healed


# ---- THE GAME LOOP ---------------------------------------------------------
print("Type: fight, rest, take, quit")

while playing:
    show_status()                       # RENDER
    command = input("> ").strip().lower()   # INPUT

    # UPDATE
    if command == "fight":
        fight()
    elif command == "rest":
        rest()
    elif command == "take":
        inventory.append("a shiny pebble")
        print("You pick up a shiny pebble.")
    elif command == "quit":
        playing = False
    else:
        print("I do not understand", repr(command))

    # The game can end without the player choosing to stop.
    if player_health <= 0:
        print()
        print("You have died with", gold, "gold.")
        playing = False

print("Goodbye.")
