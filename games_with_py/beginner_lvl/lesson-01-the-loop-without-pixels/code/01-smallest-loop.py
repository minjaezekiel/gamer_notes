# ============================================================================
# 01 - The smallest possible game loop
# Lesson 1, Games with Python, Beginner
#
# WHAT THIS SHOWS:  input -> update -> render, repeating until you stop it.
#                   Nine lines, and it is a real game loop.
#
# RUN IT:           python3 01-smallest-loop.py
# CHANGE ME FIRST:  swap the order of the three jobs. What changes?
# TRY THIS:         delete "playing = False" and try to quit.
# ============================================================================

playing = True          # STATE: is the game still running?
count = 0               # STATE: how many times have they pressed enter?

while playing:
    # ---- RENDER: show the player the state ----
    # It changes nothing. It only displays.
    print()
    print("You have pressed enter", count, "times.")
    print("Type 'quit' to stop.")

    # ---- INPUT: what does the player want? ----
    # Note that the program STOPS here and waits. A graphical game cannot do
    # this, because the world has to keep moving while the player thinks.
    # That is the one real difference, and it arrives in lesson 3.
    command = input("> ")

    # ---- UPDATE: change the state ----
    if command == "quit":
        playing = False
    else:
        count = count + 1
        # Read "=" as "becomes", not "equals". In maths, count = count + 1 is
        # nonsense. Here it means: work out count + 1, then store it in count.

print()
print("You pressed enter", count, "times. Goodbye.")
