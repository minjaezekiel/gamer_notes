# Lesson 6 — Capstone: Brick Breaker

## Cheat sheet

### A class

```python
class Brick:
    def __init__(self, x, y, w, h, hits):
        self.x = x
        self.y = y
        self.hits = hits
        self.alive = True

    def colour(self):
        return "orange" if self.hits >= 2 else "blue"

    def box(self):
        return (self.x, self.y, self.w, self.h)

brick = Brick(40, 60, 68, 24, hits=2)
print(brick.x)        # 40
print(brick.colour()) # orange
```

**`self` is not magic.** `brick.colour()` calls `Brick.colour(brick)` — `self` is that first
argument.

Use a class when a thing has **data and behaviour** and there are **many of them**. A one-off bag of
values is still better as a dictionary.

### Levels as data

```python
LEVELS = [[
    [1, 1, 1, 1],
    [1, 0, 0, 1],
]]
```

```python
for row in range(len(layout)):
    for column in range(len(layout[row])):
        kind = layout[row][column]   # ROW FIRST
        if kind == 0: continue
        x = MARGIN + column * (BRICK_W + GAP)
        y = TOP    + row    * (BRICK_H + GAP)
```

### Which side was hit?

```python
ox = min(b.right, k.right) - max(b.left, k.left)
oy = min(b.bottom, k.bottom) - max(b.top, k.top)

if oy < ox: speed_y = -speed_y
else:       speed_x = -speed_x
```

The **smaller** overlap is the side it came in through.

### One brick per frame

```python
break        # after handling a hit
```

Otherwise a ball between two bricks flips twice and carries straight on.

### Saving

```python
SAVE = Path(__file__).parent / "highscore.json"

def load():
    try:
        return json.loads(SAVE.read_text())["high_score"]
    except Exception:
        return 0

def save(v):
    try:
        SAVE.write_text(json.dumps({"high_score": v}))
    except Exception:
        pass
```

The `try` blocks are **part of the feature**. A game that crashes because it cannot save is worse
than one that quietly does not.

### Steering

```python
offset = (ball.x - centre) / (paddle.w / 2)   # -1 .. +1
```

Divide by the maximum to get a fraction. Health bars, fades, sliders — all the same move.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What is <code>self</code>? Explain what happens when you write <code>brick.colour()</code>.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> When is a class a better choice than a dictionary? Name one thing in a game that should stay a dictionary.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> In <code>layout[row][column]</code>, why is the row index first?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> How do you work out which <em>side</em> of a brick the ball hit? Why does always flipping the vertical speed go wrong?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Give three different reasons the save file might fail to load, and say what the game should do in each case.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> How many bricks does this build, and what shape?

```python
[[1, 0, 1, 0],
 [0, 2, 0, 2],
 [1, 1, 1, 1]]
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What error does this give, and what does the message tell you about <code>self</code>?

```python
class Brick:
    def colour():
        return "blue"

b = Brick()
print(b.colour())
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> The ball is travelling right and slightly up, and clips the <strong>left edge</strong> of a brick. Which overlap is smaller, and which speed should flip? Describe what the player sees if the code always flips <code>speed_y</code>.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> Someone edits <code>highscore.json</code> to say <code>hello</code>. What happens when the game starts, and why?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C1.</span> Every <code>Brick</code> reports the same position, whichever one you ask. What is wrong?

```python
class Brick:
    x = 0
    y = 0

    def __init__(self, x, y):
        x = x
        y = y
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> Bricks disappear two or three at a time, and the ball often carries straight on afterwards instead of bouncing. What is missing?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> A destroyed brick stops being drawn but the ball still bounces off it. Which of the two records was cleaned up, and which was not? Write the fix.
<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

This is the capstone. You have 85 minutes. Most of it you have written before.

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> A tkinter window with a paddle you steer and a ball that bounces off the left, right and top walls. Falling off the bottom loses a life. (Lessons 3&ndash;5.)</li>
<li><strong>Checkpoint 2.</strong> Write a <code>Brick</code> class with <code>__init__</code>, <code>box()</code> and <code>hit()</code>. Make one and draw it.</li>
<li><strong>Checkpoint 3.</strong> Write <code>LEVELS</code> as nested lists and <code>build_level()</code> to turn one into <code>Brick</code> objects. Change digits and reload to prove it works.</li>
<li><strong>Checkpoint 4.</strong> Make the ball destroy bricks, bouncing off the correct <em>side</em>. Add the <code>break</code>. Add a score.</li>
<li><strong>Checkpoint 5.</strong> Add lives, at least three levels, a game-over screen and a restart. Make tough bricks change colour after the first hit.</li>
<li><strong>Checkpoint 6.</strong> Save the high score to a file so it survives closing the game. Test it by deliberately corrupting the file.</li>
</ul>

<div class="note">
<span class="note-label">How this is marked</span>
<p>Not on features. On four things: does it run; are the levels separate from the game logic; can you
explain any method I point at; and <strong>did you change something to make it yours?</strong></p>
<p>A rougher game with an original idea in it beats a perfect copy of the example.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Your save file is plain text that a player could open and edit. Is that a problem? When would
it be? What would you do about someone setting their high score to 999999 — and is **"nothing"** an
acceptable answer?

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** Your layouts are 8 columns wide. What would have to change for a 20-wide level? If the answer
is "nothing", your code is good. If it is "several numbers", list them and say why they are there.

<div class="lines"><i></i><i></i><i></i></div>

**E3.** Design a level format that can also say "this brick is red", "this brick drops a power-up",
"this brick cannot be broken". What does it look like? What did you give up?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4. The big one.** You have built four games in this track: a text adventure, a steerable player,
Snake, and Brick Breaker. **What is the same in all four?** Design the leftover part — the thing that
would be useful in a fifth game. What must always stay specific to one game?

<div class="lines wide"><i></i><i></i><i></i><i></i><i></i></div>

---

## Stretch goals

1. Power-ups dropped by bricks.
2. **A level editor** — click a grid, print the array, paste it back. About 30 lines.
3. Save the whole game, not just the score, so you can quit and resume.
4. Tough bricks that look tough.
5. **Make it yours.** Gravity. Moving bricks. Two players. This is the real one.
