# Lesson 3 — Making It Move

## Cheat sheet

### The loop that never waits

```python
def game_loop():
    update()
    draw()
    screen.update()
    screen.ontimer(game_loop, 16)   # call me again

game_loop()
screen.mainloop()
```

16 ms ≈ 1/60 second ≈ 60 fps.

**This is the web track's `requestAnimationFrame`.** Same idea, different word.

### Keys: record, never move

```python
keys = {}

def press(name):
    def handler():
        keys[name] = True
    return handler

def release(name):
    def handler():
        keys[name] = False
    return handler

for name in ["Up", "Down", "Left", "Right"]:
    screen.onkeypress(press(name), name)
    screen.onkeyrelease(release(name), name)

screen.listen()      # OR NOTHING WORKS
```

Then in `update()`:

```python
if keys.get("Right"):
    player_x += SPEED
```

`keys.get(name)` — `keys[name]` raises `KeyError` for an untouched key.

### Why `press(name)` returns a function

A `lambda` inside the loop shares **one** `name`, so every key ends up setting the last one. That is
the **closure trap**, and it produces a bug with no error message.

### The three silent failures

| Missing | Symptom |
|---|---|
| `screen.listen()` | no key does anything |
| `drawer.clear()` | everything smears |
| `onkeyrelease` | the player never stops |

### Clamping

```python
x = max(-330, min(330, x))
```

Inside out: never more than 330, never less than −330.

### Delta time (the proper way)

```python
now = time.time()
dt = now - last_time
last_time = now
if dt > 0.1:
    dt = 1 / 60        # clamp
player_x += SPEED * dt # SPEED is px per SECOND
```

Without it, a faster computer plays a faster game.

### Words

**Polling** — asking every frame. **Key repeat** — the OS re-sending a held key.
**Closure** — a function remembering where it was made.

---

## Section A — Recall

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A1.</span> What is the single most important difference between the lesson 1 loop and the lesson 3 loop?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A2.</span> What does <code>screen.ontimer(game_loop, 16)</code> do, and which JavaScript function does the same job?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A3.</span> Why does moving the player inside the key handler make it stutter?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A4.</span> Name the three things that, if missing, cause a silent failure in this lesson &mdash; and give the symptom of each.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> Why <code>keys.get("Right")</code> rather than <code>keys["Right"]</code>?
<div class="lines"><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B1.</span> All four arrow keys make the player move in the <em>same</em> direction. Why, and what is this mistake called?

```python
for name in ["Up", "Down", "Left", "Right"]:
    screen.onkeypress(lambda: keys.update({name: True}), name)
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B2.</span> <code>SPEED</code> is 5 pixels per frame and <code>ontimer</code> asks for 16 ms. How many pixels per second is that? What happens to the real speed if the computer only manages 30 frames per second?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B3.</span> The player holds Up and Right together, with <code>SPEED = 5</code>. How far do they actually travel each frame? Show the working, and say by what percentage that is faster than moving straight.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B4.</span> What does the player see?

```python
def game_loop():
    update()
    draw()
    screen.update()
    # no ontimer line
```

<div class="lines"><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The window opens, the player is drawn, and no key does anything at all. There is no error. What is missing?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C2.</span> The player leaves a solid snake-like trail of circles behind it. What is missing, and from which function?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C3.</span> This crashes with <code>KeyError: 'Right'</code> the moment the game starts &mdash; before any key has been pressed. Explain why, and give two different fixes.

```python
def update():
    global player_x
    if keys["Right"]:
        player_x += SPEED
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Get a <code>game_loop()</code> running with <code>ontimer</code>. Prove it is running by drawing a number that counts up every frame.</li>
<li><strong>Checkpoint 2.</strong> Add the <code>keys</code> dictionary with <code>onkeypress</code> and <code>onkeyrelease</code>. Draw the list of held keys on screen. Do not move anything yet.</li>
<li><strong>Checkpoint 3.</strong> Draw a player circle and make the arrow keys move it &mdash; <strong>inside <code>update()</code></strong>. Hold a key: it should glide with no pause.</li>
<li><strong>Checkpoint 4.</strong> Clamp the player inside the window. Test by holding a key for several seconds.</li>
<li><strong>Checkpoint 5.</strong> Add WASD as a second control scheme using the <em>intent</em> pattern, so <code>update()</code> never mentions a key name directly.</li>
<li><strong>Checkpoint 6.</strong> Add a second circle that moves a little towards the player every frame. You have just written an enemy.</li>
</ul>

<div class="note">
<span class="note-label">Three things to check before asking for help</span>
<p>1. Is <code>screen.listen()</code> there? 2. Is <code>drawer.clear()</code> the first line of
<code>draw()</code>? 3. Is <code>screen.mainloop()</code> at the very end? These three cause almost
every "it does nothing" problem in this lesson, and none of them produces an error message.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** Holding Up and Right makes the player about **41% faster** than holding one key. Describe
**three different** ways to fix it, and say which you would choose and why.

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E2.** Your player stops dead the instant you release a key. Think about a spaceship, a car and a
mouse cursor. Which should stop instantly, which should not, and what makes the difference?

<div class="lines"><i></i><i></i><i></i></div>

**E3.** You asked for a frame every 16 ms. What happens if `update()` and `draw()` together take
20 ms? Does the game run at 60 fps, 50 fps, or something else? What would you *measure* to find out?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** Your loop now runs whether or not the player does anything. **List five things that could
happen in it that have nothing to do with the player** — and notice that none of them were possible
in lesson 1.

<div class="lines"><i></i><i></i><i></i></div>

---

## Stretch goals

1. Fix the diagonal-speed bug. Say which approach you chose.
2. Momentum: a speed that builds and decays rather than snapping on and off.
3. Convert to proper delta time using `code/04-delta-time.py`, and draw the measured fps on screen.
4. A chaser that follows you. Then make it *avoidable* — much harder than it sounds.
5. Wrap around the edges instead of clamping. Which suits which kind of game?
