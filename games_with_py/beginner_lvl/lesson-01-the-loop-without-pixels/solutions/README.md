# Lesson 1 — Solutions and marking notes

---

## Section A

**A1.** [3] INPUT (`input("> ")`), UPDATE (the `if`/`elif` or command dictionary that changes the
state), RENDER (`print(...)`). One mark each. Accept render-first ordering in the loop, since a text
game usually prints the room before asking — the important thing is that the three are separate.

**A2.** [2] State is everything the game remembers between turns: health, position, inventory,
score. One mark. The connection to saving: if the state is genuinely all in those variables, then
writing them to a file and reading them back is enough to restore the game exactly. Second mark.

**A3.** [3] A text game **stops and waits** at `input()`; nothing happens until the player types.
A graphical game cannot wait, because the world keeps moving — so it runs its loop around 60 times a
second whether or not anything is pressed. Two marks for the distinction, one for noting that
everything else about the structure is the same.

**A4.** [2] It stops health going below zero — "whichever is bigger, 0 or the result". The player
would otherwise see "health: −3", which looks like a bug and breaks any health bar drawn from it.

**A5.** [3] Any two: adding a room needs no new code; you can see the whole map in one place; `go()`
is written once and is correct for every room; exits can be listed automatically; the map could be
loaded from a file or built by a player; the movement code can be tested once.

---

## Section B

**B1.** [3] `20 − 5 = 15`, then `15 − 30 = −15`, then `max(0, −15)` is `0`. **Prints `0`.**
Two marks for the answer, one for correct working. A common wrong answer is `−15`, from forgetting
what `max` does.

**B2.** [4] **The loop never ends.** `cmd_quit` has no `global playing`, so the assignment
`playing = False` creates a **brand new local variable** called `playing` inside the function. That
local is set to `False` and then discarded when the function returns. The outer `playing` is never
touched, so `while playing` stays true forever.

**No error is raised.** Two marks for "it does not quit", two for the explanation. Insist on the
phrase "a new local variable" — "it doesn't work" is not an explanation.

**B3.** [3] Nothing is printed by `go` itself, and `current_room` becomes `"tunnel"`. The direction
`"north"` is in the cavern's exits, so the lookup succeeds and the room changes silently. (The next
loop iteration will print the tunnel.)

**B4.** [4] Two marks each:

- **Version A** gives `["GO", "NORTH"]`. The verb is `"GO"`, which does not match `"go"` in the
  command dictionary, so the game says it does not understand.
- **Version B** gives `["go", "north"]` and works.

Why it matters: a player who types `GO NORTH` and is told "unknown command" concludes the **game** is
broken, not that they typed it wrong. Being forgiving about input is not politeness; it is the
difference between a game people play and one they close.

---

## Section C

**C1.** [4] This is a deliberate trap and the question warns about it.

Because `player_health` is **assigned** somewhere in the function, Python decides at compile time
that it is a **local** variable for the whole function — including on the right-hand side. So the
line tries to read a local `player_health` that has not been given a value yet, and raises:

```
UnboundLocalError: cannot access local variable 'player_health'
where it is not associated with a value
```

So it does *not* silently do nothing; it raises an error that mentions a variable the student is
sure they defined. Two marks for the explanation.

Fix: `global player_health` as the first line of the function. Two marks.

(Worth noting for the class: B2's version *was* silent, because it only assigned and never read. The
difference between those two cases is confusing and worth a minute at the board.)

**C2.** [3] `"tunel"` is misspelled in the cavern's exits — one `n`. So `go("north")` sets
`current_room = "tunel"`, and the next `ROOMS[current_room]` lookup fails with `KeyError: 'tunel'`.

Teach the diagnostic: the error message names the missing key, which tells you exactly what to search
for. Note that the error appears *one step after* the real mistake, which is a very common pattern.

**C3.** [4] It increments `turns`, so a function named `show_status` is **changing the state**. Two
marks.

The rule it breaks: **render shows, update changes — never both.** Two marks.

The practical consequence is worth drawing out: if you later call `show_status()` twice (say, once
from `look` and once from the main loop), the turn counter silently runs at double speed, and the bug
appears nowhere near the function that caused it. This category of bug is exactly why the separation
exists.

---

## Section D — marking the build

Checkpoint 4 is a full pass.

**Checkpoint 2.** Check that `show_status()` really changes nothing. Students frequently decrement
something inside it.

**Checkpoint 3 — the heart of the lesson.** Look for one `go()` function driven by the data. If they
have written `if current_room == "cavern": ... elif current_room == "tunnel": ...` they have
completed the task and missed the point. Ask them how they would add a tenth room, and let the answer
make the argument.

**Checkpoint 6.** The test is whether a *second* locked door needs new code. If it does, the
requirement is special-cased rather than data-driven. The expected shape:

```python
needed = ROOMS[destination].get("needs_key")
if needed is not None and needed not in inventory:
    print("The way is locked. You need:", needed)
    return
```

**Encourage them to make it theirs.** A spaceship, a school at night, a haunted shop. Students invest
much more in a world they invented, and the code is identical.

---

## Section E — marking notes, not answers

**E1.** Looking for requirements expressed as data rather than as special cases. Good shapes:

```python
"crypt": {
    "description": "...",
    "exits": {...},
    "needs_light": True,          # checked generally when entering
    "monster_chance": 0.3,        # rolled on arrival
    "visited": False,             # changes the description next time
}
```

The thing to praise: a new flag that `go()` understands generally works for *every* room at once.
The thing to question: flags that only one room will ever use are often better as a special case —
ask them where the line is. There is no clean answer and that is worth saying.

**E2.** The honest answer is that it gets unpleasant somewhere between eight and fifteen globals.
Expected suggestions: gather them into one `player` dictionary, or a `game` dictionary holding
everything. Both are real answers, and both are what the intermediate level does properly with
classes. Do not push them towards classes today; the *feeling* that too many globals is bad is worth
more than the solution.

**E3 — the question that is really the course.** What breaks: `input()` blocks, so no time passes in
the game's eyes while the player thinks. The torch cannot burn down, because no code runs.

Expect answers like:

- Check the real clock each turn and work out how much time passed (`time.time()`). This works for a
  turn-based game and is a genuinely good answer.
- Count turns instead of seconds. Simpler, but then a player who thinks for ten minutes loses no
  torch, which may actually be what you want.
- Run the input reading in parallel somehow. Correct instinct, much harder than it sounds.
- Stop waiting: check whether a key has been pressed, and if not, carry on anyway.

That last one is exactly what lesson 3 does, and it is the whole reason graphical games are
structured differently. A student who gets there has worked out the design of every real-time game
from first principles. Tell them so.

---

## Teacher note: the `global` conversation

Plan to spend five to ten minutes on this. Two boxes on the board:

```
   OUTSIDE                 INSIDE cmd_quit()
   playing = True          playing = False   <- a DIFFERENT box
```

Then show that adding `global playing` deletes the second box and makes the function write to the
first one.

It is worth saying plainly that this design choice in Python is a common complaint, and that it
exists so that functions cannot accidentally modify outer variables — which is usually what you want.
Students find it much easier to accept once they know it is a deliberate trade-off rather than a
quirk they are failing to understand.
