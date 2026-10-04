# Lesson 1 — The Loop Without Pixels

> **Games with Python · Beginner level · Lesson 1 of 6 · 2 hours 30 minutes**

## By the end of today you will have built

A playable text adventure with **real game state** — health, an inventory, rooms you can move
between, and a monster that can kill you.

```
--------------------------------------------------
  THE CAVERN
  Water drips somewhere in the dark.
--------------------------------------------------
  health: 18/20     carrying: torch, rusty key

  Exits: north, east

  > go north
```

No graphics. Not one pixel. And it will still be a game, built on exactly the same structure as
every game in this course — which is the whole point of starting here.

## Where this fits

- **Back:** nothing. This is lesson 1.
- **Forward:** [lesson 2](../lesson-02-drawing-with-turtle/notes.md) adds drawing.
- **Sideways:** students on the web track built a moving square today. Different output, **identical
  structure**. By lesson 6 you will see why that matters.

---

## The idea, in plain words

### Why start with no graphics?

Because graphics are not what a game is.

Almost every beginner tutorial starts by putting a sprite on a screen, and the student ends up
believing a game is a picture that moves. Then they get stuck the moment they want it to *do*
something, because they never learned what was underneath.

A game is three things:

1. **State** — the numbers it remembers.
2. **A loop** — which changes those numbers, over and over.
3. **Output** — which shows you the numbers.

Only the third one needs graphics. Today you build the first two, and prove they are a game on their
own.

### A game is a program that does not finish

Most programs you have written run top to bottom and stop. A game cannot: the world has to keep
existing while the player decides what to do.

```python
# This is a program.
print("Hello")
print("Goodbye")
# ...and it is over.

# This is a game.
while playing:
    show_room()           # RENDER:  show the player what is going on
    command = input("> ") # INPUT:   what does the player want?
    do_command(command)   # UPDATE:  change the numbers
# ...and it keeps going until something sets playing to False.
```

That `while` loop is **the game loop**, and it is the same three jobs you will use for the rest of
this course:

| Job | In a text game | In a graphical game |
|---|---|---|
| **INPUT** | `input("> ")` | which keys are held down? |
| **UPDATE** | work out what the command does | move things, check collisions |
| **RENDER** | `print()` the room | draw pixels on a screen |

> **The one real difference.** A text game *waits* at `input()`. A graphical game cannot wait — it
> runs its loop 60 times a second whether you press anything or not, because the world keeps moving.
> Lesson 3 is where that changes. Everything else stays the same.

### State: what the game remembers

```python
# The game's STATE: everything it needs to remember between turns.
player_health = 20
player_max_health = 20
current_room = "cavern"
inventory = []
playing = True
```

That is it. That is the whole game, as far as the computer is concerned. Everything printed on screen
is just a way of *showing* those five values to a human.

Here is a test worth doing: if you wrote those five values on a piece of paper, closed the program,
and typed them back in tomorrow, the game would carry on exactly where it left off. **That is what
state means** — and it is why saving a game is possible at all.

### Rooms are data, not code

The obvious way to write rooms is with `if`:

```python
# DO NOT DO THIS
if current_room == "cavern":
    print("You are in a dark cavern.")
    if command == "north":
        current_room = "tunnel"
    elif command == "east":
        current_room = "pool"
elif current_room == "tunnel":
    print("A narrow tunnel.")
    # ...and so on, forever
```

Three rooms is tolerable. Ten is a mess. Twenty is unmaintainable, and you cannot add a room without
risking the ones that already work.

Describe the world as **data** instead:

```python
# Each room is a dictionary. The whole world is a dictionary of them.
ROOMS = {
    "cavern": {
        "description": "A dark cavern. Water drips somewhere you cannot see.",
        "exits": {"north": "tunnel", "east": "pool"},
    },
    "tunnel": {
        "description": "A narrow tunnel. The air is colder here.",
        "exits": {"south": "cavern"},
    },
}
```

Now the code that moves the player works for **any** number of rooms:

```python
def go(direction):
    global current_room
    exits = ROOMS[current_room]["exits"]
    if direction in exits:
        current_room = exits[direction]      # one line, any map size
    else:
        print("You cannot go that way.")
```

Adding a twentieth room means adding data. It does not mean touching `go()` at all.

> This is the same idea the web track meets in its last lesson, with brick layouts. **Separate the
> thing that changes often from the thing that changes rarely.** You are meeting it in lesson 1,
> because in Python it is easier to show.

---

## The idea, in pictures

Open [the game loop explainer](../../../shared/visualizers/game-loop.html).

**What to look for:** press **Step 1 frame** three times and watch the three boxes light up in turn.
Your text adventure does exactly this, with one difference: it pauses at INPUT and waits for you,
instead of checking the keyboard and carrying straight on. Everything else is the same.

The explainer is a web page, and your game is Python. That is deliberate. **The loop is an idea, not
a feature of a language.**

---

## The idea, in code

### Step 1: the smallest possible game loop

```python
playing = True
count = 0

while playing:
    # RENDER: show the state
    print("You have pressed enter", count, "times.")

    # INPUT: what does the player want?
    command = input("> ")

    # UPDATE: change the state
    if command == "quit":
        playing = False
    else:
        count = count + 1

print("Goodbye.")
```

Nine lines, and it is a real game loop. Run it. Notice that nothing happens until you type something
— and notice that the three jobs are in the same order you will use all course.

### Step 2: state the player cares about

```python
player_health = 20
inventory = []

def show_status():
    """Print the player's state. RENDER only - changes nothing."""
    print()
    print("  health:", player_health, "/ 20")
    if inventory:
        # ", ".join(...) glues a list into one string with commas between.
        print("  carrying:", ", ".join(inventory))
    else:
        print("  carrying: nothing")
```

That docstring — the text in triple quotes — is not decoration. Writing "RENDER only, changes
nothing" is a promise to your future self, and if you later find yourself changing `player_health`
inside a function like this, you have broken the rule from lesson 1 of every track: **update changes
numbers, render shows them. Never both.**

### Step 3: splitting the command

```python
command = input("> ").strip().lower()
# .strip() removes spaces at the ends, so "  go north  " works
# .lower() makes it lower case, so "GO NORTH" works too
#
# Being forgiving about input is not politeness. A player who types GO NORTH
# and is told "unknown command" concludes your game is broken, not that they
# typed it wrong.

words = command.split()        # "go north" becomes ["go", "north"]

if not words:
    continue                   # they just pressed enter; ask again

verb = words[0]                # "go"
rest = words[1:]               # ["north"]  (a list, possibly empty)
```

### Step 4: a dictionary of commands

Once you have more than about four commands, a chain of `elif` starts to hurt. A dictionary of
functions is tidier and, more importantly, lets the game list its own commands:

```python
def cmd_look(rest):
    show_room()

def cmd_go(rest):
    if not rest:
        print("Go where?")
        return
    go(rest[0])

def cmd_quit(rest):
    global playing
    playing = False

COMMANDS = {
    "look": cmd_look,
    "go": cmd_go,
    "north": lambda rest: go("north"),   # a shortcut: typing "north" alone
    "quit": cmd_quit,
    "help": lambda rest: print("Commands:", ", ".join(sorted(COMMANDS))),
}

# And the whole command handling becomes four lines:
if verb in COMMANDS:
    COMMANDS[verb](rest)
else:
    print("I do not know how to", verb)
```

Look at `help`. It lists the commands by reading `COMMANDS` itself, so it can never be out of date.
That is what data-driven design buys you: the game can answer questions about itself.

---

## The maths you just used

Essentially none — and it is worth saying why.

The only arithmetic today is `player_health = player_health - damage`. As in every language, `=` here
does **not** mean "equals". It means *"work out the right-hand side, then store the answer on the
left"*. In maths, `x = x - 5` is nonsense. In programming it is Tuesday. Read `=` as **"becomes"**.

One genuinely useful habit, though: **clamp** values that have limits.

```python
player_health = player_health - damage
if player_health < 0:
    player_health = 0            # never show "health: -3"

# Python has a neater way to say the same thing:
player_health = max(0, player_health - damage)
```

`max(0, x)` means "whichever is bigger, 0 or x" — so the answer can never go below zero. You will use
this constantly: health bars, scores, timers, ammunition.

---

## Break it on purpose

Use `code/03-adventure.py`. Predict first, then run.

| Change this | Predict what happens | What actually happened |
|---|---|---|
| Delete `playing = False` from `cmd_quit` | | |
| Remove `.lower()` from the input line, then type `GO NORTH` | | |
| Add a room to `ROOMS` whose exit points at a room that does not exist | | |
| Remove the `global` from inside `cmd_quit` | | |
| Change `inventory = []` to `inventory = {}` | | |
| Set starting health to `0` | | |

The fourth one is the most instructive. Python will not report an error — the function will quietly
create its own local `playing`, change that, and throw it away. The game simply refuses to quit, and
nothing tells you why.

---

## Think like an engineer

1. Your rooms are a dictionary. **Design the data** for something more interesting: a room that is
   dark until you have a torch, a door that needs a key, a monster that is only in some rooms. What
   does your room dictionary look like now? What did it cost in readability?
2. Right now the game has about five global variables. If you added magic, money, time of day and a
   quest log, how many would there be? Is that a problem? What would you do instead?
3. **The honest question.** Your game waits forever at `input()`. Suppose you wanted a torch that
   burns out after two minutes *of real time*, whether or not the player types anything. What
   breaks? Sketch what would have to change.
4. The fourth question is really the whole course. Write down what you would need in order for things
   to happen *while the player is thinking*. You will build exactly that in lesson 3.

---

## Vocabulary

| Word | What it means |
|---|---|
| **State** | Everything the game remembers between turns. |
| **Game loop** | The repeating input → update → render cycle. |
| **Dictionary** | A Python lookup table: `{"key": value}`. |
| **List** | An ordered collection: `["torch", "key"]`. |
| **`global`** | Says "change the variable outside this function, not a new local one". |
| **Clamping** | Forcing a value inside sensible limits. |
| **Data-driven** | Behaviour described by data, not by code. |

---

## Recap

- A game is **state**, a **loop** that changes it, and **output** that shows it. Only output needs
  graphics.
- The three jobs are **input, update, render**, in that order, in every language.
- Keep update and render separate: one changes numbers, the other shows them.
- Describe your world as **data** (dictionaries) and the code that works on it stays short.
- A text game **waits** at input. A graphical game cannot. That is the only real difference, and it
  arrives in lesson 3.

---

## Stretch goals

1. **Items.** Put items in rooms. Add `take` and `drop`. Where do you store which items are where —
   in the room, or in a separate dictionary? Both work; say why you chose yours.
2. **A locked door.** One exit needs the rusty key. Do not special-case it in `go()` — put the
   requirement in the room *data*, and make `go()` check for it generally.
3. **Save and load.** Write the state to a file with `json.dump`, and read it back. This is the test
   from the notes made real: if your state is complete, saving works.
4. **A monster.** It moves one room each turn. Now something happens without the player doing it,
   which is your first taste of lesson 3.
5. **Make the map ten rooms** and draw it on paper first. Notice that you did not change any code.

---

## Teacher notes

**Timing**

| Minutes | Block |
|---|---|
| 0–10 | **Hook.** Play a classic text adventure on the projector for five minutes, taking suggestions from the class. Then ask: "what does the computer actually remember?" |
| 10–25 | **Concept.** State, loop, output. The game-loop visualizer. Point out explicitly that it is a web page and they are writing Python, and that this is the point. |
| 25–40 | **Live-code** the nine-line counter loop. Everyone types it. Then add health. |
| 40–50 | Break. |
| 50–120 | **Build.** Exercises section D: the adventure. |
| 120–140 | Break-it-on-purpose. The missing-`global` one deserves five minutes on the board. |
| 140–150 | Recap. Lesson 2 draws things. |

**Setup check before the first lesson**

```bash
python3 --version                            # 3.10 or newer
python3 -c "import tkinter; print('ok')"     # needed from lesson 5
```

On some Linux installs `tkinter` is a separate package (`sudo apt install python3-tk`). That is the
only setup surprise in the whole beginner Python track, and it is better found now than in lesson 5.

**What usually goes wrong**

1. **The missing `global`.** A function assigns to `playing` or `current_room`, Python creates a new
   local variable, and the change silently vanishes. **No error is raised.** This is the single most
   confusing Python behaviour for beginners and it is worth real board time. Draw two boxes: "the
   variable outside" and "the new one this function just made".
2. **Mixing up `=` and `==`.** In an `if`, Python at least gives a syntax error, which is kinder than
   some languages.
3. **Indentation.** Mixing tabs and spaces. Tell them to set their editor to spaces once, on day one.
4. **`KeyError`.** They typed a room name that is not in `ROOMS`, usually a typo or a mismatched exit.
   Teach them to read the error: the last line names the missing key.
5. **Everything in one enormous `while` loop.** Common and tolerable today; it is the pressure that
   makes functions feel worth having.

**If you are running short on time** — give them `ROOMS` already written, with three rooms, and have
them build only the loop and the commands. Cut the `COMMANDS` dictionary and use `elif`; mention that
there is a tidier way and show it next lesson.

**For the student who finishes at minute 90** — stretch goal 3 (save and load with `json`) is the
best one, because it makes the lesson's central claim concrete: if your state is genuinely all in
those variables, saving is about four lines, and if it is not, they will find out immediately and
usefully.

**The thing to land:** ask at the end how much of today's lesson was about Python. The answer is
almost none of it — `while`, `if`, dictionaries and functions. All the actual content was about
*structure*: what a game remembers, and the order in which it does things. That is why it will
transfer when the pixels arrive next lesson, and why students taking a second track find it much
faster.
