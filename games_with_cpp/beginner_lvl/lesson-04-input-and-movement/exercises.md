# Lesson 4 — Input And Movement

## Cheat sheet

### Blocking vs non-blocking

```cpp
std::cin >> command;   // STOPS and waits
int key = read_key();  // returns 0 and carries on
```

A real-time game **never waits**.

### Raw mode (Unix)

```cpp
void start_raw_mode() {
    tcgetattr(STDIN_FILENO, &original);
    termios raw = original;
    raw.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);
    fcntl(STDIN_FILENO, F_SETFL,
      fcntl(STDIN_FILENO, F_GETFL, 0) | O_NONBLOCK);
}

void stop_raw_mode() {       // NOT OPTIONAL
    tcsetattr(STDIN_FILENO, TCSANOW, &original);
}
```

- `ICANON` — line buffering (waits for Enter)
- `ECHO` — printing what you type
- `O_NONBLOCK` — `read()` returns immediately

**If the terminal breaks: type `reset` and press Enter.** You will not see yourself typing.

### Why `#ifdef`

Reading a key without waiting is **not standard C++**. The language says nothing about terminals.

```cpp
#ifdef _WIN32
  #include <conio.h>      // _kbhit(), _getch()
#else
  #include <termios.h>
#endif
```

### Arrow keys are THREE characters

`27`, then `91`, then `65`/`66`/`67`/`68` (up/down/right/left).

### Check first, then move

```cpp
int nx = x + dx, ny = y + dy;
char target = maze_at(nx, ny);
if (target == '#') return;   // do not move
x = nx; y = ny;
```

**Validate, then act.** Not: move, check, move back.

### Direction pairs

```cpp
'w' -> (0, -1)   // up is MINUS: row 0 is the top
's' -> (0, +1)
'a' -> (-1, 0)
'd' -> (+1, 0)
```

---

## Section A — Recall

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A1.</span> What is the difference between blocking and non-blocking input? Which does a real-time game need?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A2.</span> Name the two terminal behaviours raw mode switches off, and say why a game does not want each.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">A3.</span> Why must you call <code>stop_raw_mode()</code>? What does the user see if you do not, and what is the cure?
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A4.</span> Why does this code need <code>#ifdef</code> when nothing else in the course has?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[2 marks]</span>
<span class="q-num">A5.</span> How many characters does pressing the up arrow send, and what are they?
<div class="lines"><i></i></div>
</div>

---

## Section B — Predict the output

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B1.</span> The player is at <code>(5, 3)</code> and presses <code>w</code>. What square does the game check, and why is it <em>minus</em> one?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B2.</span> What happens if <code>O_NONBLOCK</code> is left out of <code>start_raw_mode()</code>? Describe exactly what the player sees.
<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">B3.</span> The player presses the up arrow. What does this print, and why three lines?

```cpp
int key = read_raw_key();
if (key != 0) std::cout << key << "\n";
```

(Called once per frame, three frames in a row.)

<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">B4.</span> A player walks into a wall. Describe what happens with each version, and say which is better and why.

```cpp
// version A
char target = maze_at(x + dx, y + dy);
if (target == '#') return;
x += dx; y += dy;

// version B
x += dx; y += dy;
if (maze_at(x, y) == '#') { x -= dx; y -= dy; }
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

---

## Section C — Find and fix the bug

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C1.</span> The game freezes until a key is pressed, then does exactly one frame and freezes again. What is missing?
<div class="lines"><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[4 marks]</span>
<span class="q-num">C2.</span> The player walks straight through walls. The maze data is correct. What is wrong?

```cpp
void try_move(int dx, int dy) {
    char here = maze_at(player_x, player_y);
    if (here == '#') return;
    player_x += dx;
    player_y += dy;
}
```

<div class="lines"><i></i><i></i><i></i></div>
</div>

<div class="q"><span class="marks">[3 marks]</span>
<span class="q-num">C3.</span> The game works perfectly, but after quitting, the student's terminal no longer shows what they type. What did they forget, and what should they type to fix the terminal?
<div class="lines"><i></i><i></i></div>
</div>

---

## Section D — Build it

<ul class="checkpoints">
<li><strong>Checkpoint 1.</strong> Get <code>read_key()</code> working. Print the code of each key pressed, with a heartbeat message so you can see the loop running while you press nothing.</li>
<li><strong>Checkpoint 2.</strong> Add <code>start_raw_mode()</code> and <code>stop_raw_mode()</code>. <strong>Test that quitting leaves your terminal working.</strong></li>
<li><strong>Checkpoint 3.</strong> Draw a maze from an array of strings, with a player <code>@</code>. Move the player with WASD. Walking through walls is fine for now.</li>
<li><strong>Checkpoint 4.</strong> Add the wall check &mdash; <strong>check the destination, then move</strong>. Walk round the whole maze and check you cannot escape.</li>
<li><strong>Checkpoint 5.</strong> Add collectable keys that disappear when you walk onto them, and a counter.</li>
<li><strong>Checkpoint 6.</strong> Add a locked exit that only works once all the keys are collected, and something that animates (a flickering torch, a countdown) so the screen is alive while you stand still.</li>
</ul>

<div class="note">
<span class="note-label">When your terminal breaks</span>
<p>It will. Type <code>reset</code> and press Enter. You will not see yourself typing, and it will
work anyway. Write that on a sticky note now.</p>
<p>Also: <strong>run from a real terminal</strong>, not an IDE's built-in console. Many of them do
not pass individual keystrokes through, and your perfectly correct program will appear dead.</p>
</div>

---

## Section E — Design challenge

<div class="open">
<span class="note-label">No right answer</span>
</div>

**E1.** `read_key()` reads **one** key per frame. What happens if the player presses three keys very
quickly within one frame? Is it a problem? **How would you find out?**

<div class="lines wide"><i></i><i></i><i></i></div>

**E2.** The maze is written in the code. Design how you would load it from a **file** so levels could
be made without recompiling. What could go wrong with a file a player has edited, and what should
your program do about each case?

<div class="lines wide"><i></i><i></i><i></i><i></i></div>

**E3.** Your program changes a **system-wide** setting and has to put it back. What else might a game
change that it must restore? What happens if the program **crashes** before the restore runs?

<div class="lines wide"><i></i><i></i><i></i></div>

**E4.** Non-blocking input needed different code for Windows and Unix, because standard C++ says
nothing about terminals. **Why would the language leave out something so obviously useful?** What
would it cost to put it in?

<div class="lines wide"><i></i><i></i><i></i></div>

---

## Stretch goals

1. **Push blocks** you can shove into empty space. You now have Sokoban — and some real design
   decisions about what happens when a crate hits another crate.
2. Load the maze from a file.
3. A patrolling guard on its own timer. Notice that **none of your input code changes**.
4. A field of view, so you only see squares near you.
5. **Hold-to-move**, with a short delay before the repeat starts. Genuinely awkward in a terminal —
   find out why.
