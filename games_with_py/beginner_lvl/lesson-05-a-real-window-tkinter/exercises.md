# Lesson 5 — A Real Window: tkinter

## Cheat sheet

### y points DOWN now

| | turtle | **tkinter** |
|---|---|---|
| `(0,0)` | middle | **top-left** |
| y grows | up | **down** |

```python
y = y - 5     # moves UP
y = y + 5     # moves DOWN (gravity ADDS)
```

Turtle was the odd one out. This is the normal world.

### Setup

```python
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=W, height=H,
    bg="#15181d", highlightthickness=0)
canvas.pack()
```

`highlightthickness=0` removes a 2-pixel border that silently breaks collision maths.

### Rectangles are TWO CORNERS

```python
canvas.create_rectangle(left, top, right, bottom)
```

Not x, y, width, height. Write a helper:

```python
def set_box(item, x, y, w, h):
    canvas.coords(item, x, y, x + w, y + h)
```

### Create ONCE, then move

```python
ball = canvas.create_oval(0,0,0,0, fill="red")  # before the loop
canvas.coords(ball, x, y, x+20, y+20)           # in the loop
```

**Never `create_` inside the loop.** The canvas keeps every shape forever and the game grinds to a
halt.

| Retained (tkinter) | Immediate (turtle, web) |
|---|---|
| system remembers shapes | you redraw everything |
| move what moved | clear and redraw |

### Removing

```python
canvas.delete(fruit["item"])   # the canvas's record
fruits.pop(i)                  # AND yours
```

Two sets of books. Keep them in step.

### The loop

```python
window.after(16, game_loop)
```

Same as `ontimer` and `requestAnimationFrame`.

### Input

```python
def on_press(event):
    keys[event.keysym] = True
window.bind("<KeyPress>", on_press)
window.focus_force()
```

### Falling

```python
f["speed"] += GRAVITY * dt   # accel changes speed
f["y"]     += f["speed"]*dt  # speed changes position
```

### Difficulty with a floor

```python
delay = max(0.35, 1.2 - score * 0.004)
```

Design the limit at the same time as the slope.

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> In tkinter, where is <code>(0, 0)</code> and which way does y grow? Write the line that makes something move <em>up</em>.
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What four numbers does <code>create_rectangle</code> take?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Explain the difference between <em>retained mode</em> and <em>immediate mode</em>, and say which turtle and tkinter each are.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> <code>canvas.create_oval(...)</code> returns something. What is it?
<div class="lines"><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A5.</span> Why must you call <code>canvas.delete()</code> <em>as well as</em> removing the item from your own list?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> A fruit is at <code>y = 100</code> with speed 200, and <code>GRAVITY = 320</code>. After one frame of <code>dt = 0.016</code>, what is its speed and its y? Is it higher or lower on the screen?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> The game runs beautifully for about three seconds and then becomes jerky and then unusable. What is wrong, and roughly how many shapes exist after ten seconds at 60 fps?

```python
def draw():
    canvas.create_oval(x - 20, 170, x + 20, 210, fill="red")
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> What size and shape does this produce? The author wanted a basket 92 wide and 18 tall at <code>(100, 400)</code>.

```python
canvas.create_rectangle(100, 400, 92, 18)
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> <code>score</code> is 0, then 100, then 300. What is the spawn delay each time? What is the delay at a score of 10,000, and why?

```python
delay = max(0.35, 1.2 - score * 0.004)
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The fruit rises off the top of the screen instead of falling. One character is wrong. Which, and why?

```python
fruit["y"] -= fruit["speed"] * dt
```

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> Caught fruit disappears from the game &mdash; it stops counting for the score and stops colliding &mdash; but it stays visible on screen forever. What is missing?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> About half the fruit that reaches the bottom is never removed, and lives are lost at the wrong times. Name the bug. You have seen it twice before &mdash; where?

```python
for i in range(len(fruits)):
    if fruits[i]["y"] > HEIGHT:
        remove_fruit(i)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Get a tkinter window with a canvas, and draw a rectangle. Prove you understand the two-corners form by making it exactly 92&times;18 at a position you choose.</li>
<li><strong>Checkpoint 2.</strong> Write <code>set_box(item, x, y, w, h)</code>. Add the <code>game_loop</code> with <code>after(16, ...)</code> and the <code>dt</code> calculation with its clamp.</li>
<li><strong>Checkpoint 3.</strong> Add a basket you steer with the arrow keys, clamped inside the window. Create its canvas item <strong>once</strong>, outside the loop.</li>
<li><strong>Checkpoint 4.</strong> Make fruit spawn at the top at random x and fall. Keep them in a list of dictionaries, each holding its own canvas item id.</li>
<li><strong>Checkpoint 5.</strong> Catch the fruit with the AABB test. Add a score. Remove caught fruit from <strong>both</strong> your list and the canvas &mdash; looping backwards.</li>
<li><strong>Checkpoint 6.</strong> Add lives, a menu, a game-over screen, and a difficulty curve with a floor.</li>
</ul>

<div class="note">
<span class="note-label">If your game slows to a crawl</span>
<p>You are creating canvas items inside the loop. Add
<code>print(len(canvas.find_all()))</code> to <code>draw()</code> and watch the number climb into the
thousands. Create once, outside the loop; then only <code>coords()</code>.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Turtle made you redraw everything; tkinter remembers your shapes. For each of these, say which
you would rather have and why: **a Snake game**; **a particle effect with 500 sparks**; **a chess
board**; **a scrolling platform level**.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** You keep a Python list of fruit *and* the canvas keeps items. What goes wrong when the two
disagree? Design a way to make it **impossible** for them to disagree.

<div class="lines wide"><i></i><i></i><i></i></div>

**E3.** Your fruit speeds up as the score rises. At some point it will exceed human reaction time. How
would you find that point **without guessing**? What would you change *instead* of speed?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** `after(16, game_loop)` asks for 60 fps. What happens if the window is dragged, or another
program hogs the machine for half a second? What does the `dt` clamp protect you from — and what does
the clamp *cost* you?

<div class="lines wide"><i></i><i></i><i></i></div>

---

## Stretch goals

1. Bad fruit you must avoid. Now the game is about choosing, not just moving.
2. A combo counter — and decide what breaks a combo.
3. Mouse control with `<Motion>`. Which feels better?
4. A real pause that stops the spawn timer too.
5. Draw your measured frames per second. Then add 500 fruit and watch what happens.
