# Lesson 1 — The Loop Without Pixels

## Cheat sheet

### A game is three things

1. **State** — the numbers it remembers
2. **A loop** — which changes them
3. **Output** — which shows them

Only the third needs graphics.

### The loop

```python
while playing:
    show_room()              # RENDER
    command = input("> ")    # INPUT
    do_command(command)      # UPDATE
```

A text game **waits** at input. A graphical game cannot. That is the only real difference.

### State

```python
player_health = 20
current_room = "cavern"
inventory = []
playing = True
```

Write these on paper, retype them tomorrow, and the game carries on. That is why saving is possible.

### The world as data

```python
ROOMS = {
    "cavern": {
        "description": "A dark cavern.",
        "exits": {"north": "tunnel"},
    },
}
```

```python
def go(direction):
    global current_room
    exits = ROOMS[current_room]["exits"]
    if direction in exits:
        current_room = exits[direction]
    else:
        print("You cannot go that way.")
```

One function, any number of rooms.

### `global` — the trap

```python
def cmd_quit(rest):
    global playing      # WITHOUT this...
    playing = False     # ...Python makes a NEW local
                        # variable, changes it, throws
                        # it away, and reports NO ERROR.
```

### Being forgiving about input

```python
words = input("> ").strip().lower().split()
if not words:
    continue
verb = words[0]
rest = words[1:]
```

### Clamping

```python
health = max(0, health - damage)   # never below 0
health = min(MAX, health + heal)   # never above MAX
```

### Words

**State** — what the game remembers.
**Dictionary** — `{"key": value}`.
**Data-driven** — behaviour from data, not code.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What are the three jobs in a game loop, in order? Give the Python that does each one in a text game.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does <em>state</em> mean, and what does it have to do with being able to save a game?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> What is the one real difference between a text game's loop and a graphical game's loop?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> What does <code>max(0, health - damage)</code> do, and why would a player care?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Give two advantages of storing rooms in a dictionary rather than in a chain of <code>if</code> statements.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

**Write your answer before running anything.**

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> What does this print?

```python
health = 20
health = health - 5
health = health - 30
print(max(0, health))
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What happens when you type <code>quit</code>? Be precise &mdash; there is no error message.

```python
playing = True

def cmd_quit():
    playing = False

while playing:
    if input("> ") == "quit":
        cmd_quit()
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> The player is in <code>"cavern"</code> and types <code>go north</code>. What is printed, and what is <code>current_room</code> afterwards?

```python
ROOMS = {
    "cavern": {"exits": {"north": "tunnel"}},
    "tunnel": {"exits": {"south": "cavern"}},
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> The player types <code>GO NORTH</code> (capitals). What happens with each version, and why does it matter which you use?

```python
# version A
words = input("> ").split()

# version B
words = input("> ").strip().lower().split()
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> The player's health never actually changes, and Python reports no error at all. Why not, and what is the fix?

```python
player_health = 20

def take_damage(amount):
    player_health = player_health - amount
```

Careful: this one <em>does</em> raise an error, and it is not the one you might expect. Explain
exactly what Python does here.

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> Moving to the tunnel crashes with <code>KeyError: 'tunnel'</code>. What is wrong?

```python
ROOMS = {
    "cavern": {"exits": {"north": "tunel"}},
    "tunnel": {"exits": {"south": "cavern"}},
}
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> This function is supposed to only display things, but it has a bug that will cause confusing problems later. Find it, and say which rule it breaks.

```python
def show_status():
    global turns
    turns = turns + 1
    print("health:", player_health)
    print("turn:", turns)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

Build your own text adventure. At least four rooms, and make it *yours* — a spaceship, a school at
night, a sunken ship.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> A <code>while</code> loop that prints something, reads a command, and quits on <code>quit</code>. Check that it really stops.</li>
<li><strong>Checkpoint 2.</strong> Add state: health and an inventory. Write <code>show_status()</code> that displays them and <strong>changes nothing</strong>.</li>
<li><strong>Checkpoint 3.</strong> Build a <code>ROOMS</code> dictionary with at least four rooms and working exits. Write <code>go(direction)</code> once, so it works for every room.</li>
<li><strong>Checkpoint 4.</strong> Put items in rooms. Add <code>take</code>, so an item moves from the room's list into the inventory. Print the room's items when you arrive.</li>
<li><strong>Checkpoint 5.</strong> Add a way to lose (health reaching 0) and a way to win (reaching a room, or carrying a particular item). Make sure both end the loop properly.</li>
<li><strong>Checkpoint 6.</strong> Add a locked door. Put the requirement in the room <em>data</em>, not as a special case inside <code>go()</code> &mdash; so a second locked door needs no new code.</li>
</ul>

<div class="note">
<span class="note-label">If something changes and then un-changes</span>
<p>You are missing a <code>global</code>. Python has quietly created a <em>new</em> local variable
inside your function, changed that, and thrown it away when the function ended. No error is raised.
This is the most confusing thing in Python for beginners, and everybody hits it once.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Your rooms are dictionaries. Design the data for something more interesting: a room that is
dark until you have a torch; a monster that only appears sometimes; a room that changes after you
visit it. Write what one of your room dictionaries would look like.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** You now have about five global variables. If you added magic, money, time of day and a quest
log, how many would there be? Is that a problem? What would you do instead?

<div class="lines"><i></i><i></i><i></i></div>

**E3. The one that matters.** Your game waits forever at `input()`. Suppose you wanted a torch that
burns out after two minutes of **real time**, whether or not the player types anything. What breaks?
Sketch what would have to change.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. `take` and `drop`. Decide where you store which items are where, and say why.
2. A locked door whose requirement lives in the data.
3. **Save and load** with `json.dump` and `json.load`. If your state really is all in those
   variables, this is about four lines. If it is not, you will find out immediately.
4. A monster that moves one room each turn — your first taste of something happening without the
   player doing it.
5. Ten rooms. Draw the map on paper first. Notice you changed no code.
