# Lesson 6 — Solutions and marking notes

---

## Section A

**A1.** [3] Any three: it is tiny · the data looks like the level, so it can be read and edited by eye ·
lookups are instant, because you compute which square to look at rather than testing every wall ·
editing is editing text, with no tools to build. One mark each.

Push for the lookup one if nobody offers it: with rectangles you ask everybody, with a grid you work out
your seat number.

**A2.** [3] Any three, one mark each: the trailing newline adds an empty row · `rstrip()` eats trailing
spaces as well as the newline · rows of different lengths give an `IndexError` or a silent hole · `open`
uses the working directory, not the script's folder.

**A3.** [3] `//` is floor division and rounds towards negative infinity — one mark. They differ for
**negative** positions: `-5 // 32` is `-1`, `int(-5 / 32)` is `0` — one mark. A player at x = −5 is in
column −1, and reporting column 0 lets them stand inside the left-hand wall — one mark.

**A4.** [2] Any two problems, one mark each: no `IndexError` when the player leaves the map · no separate
off-the-edge code · the border of `#` becomes optional · the player cannot escape the world.

**A5.** [3] Because a combined move that ends in a wall gives **no information about which direction
caused it** — two marks — so there is nothing sensible to undo, and any guess is wrong in some case —
one mark. Credit the bonus observation that two steps also give wall-sliding for free.

**A6.** [2] It is what the **downward** collision test reports: if moving down put you inside a solid
tile, you have landed — one mark. From a key press, the game would believe the player's input rather than
the world, and the two disagree the moment they walk off a ledge — one mark.

**A7.** [2] It stops a box whose right edge lands exactly on a tile boundary from being counted as
touching the next column — one mark. Without it the player sticks in gaps exactly their own width,
because the game thinks they overlap a wall they are only adjacent to — one mark.

---

## Section B

**B1.** [3] `95 // 32 = 2`, `64 // 32 = 2`. Two marks. Top-left corner `(64, 64)` — one mark. Note that
64 is exactly on a boundary, which is the case the `- 1` exists for.

**B2.** [3] `-5 // 32` is **−1**; `int(-5 / 32)` is **0**. Two marks. −1 is correct, and getting 0 means
the game thinks a player just off the left edge is in column 0 — inside the wall — one mark.

**B3.** [4] `c0 = 60 // 32 = 1`; `c1 = (60 + 26 - 1) // 32 = 85 // 32 = 2`;
`r0 = 30 // 32 = 0`; `r1 = (30 + 26 - 1) // 32 = 55 // 32 = 1`. So columns 1–2 and rows 0–1: **four**
tiles. One mark per line.

**B4.** [3] `readlines()` gives the rows **plus** a final element for the text after the last newline —
with a trailing newline that is an empty string, so there is **one extra row** and it is `""`. Two marks.
That row is shorter than the others, so either the length check fires or the bottom of the level silently
has no floor — one mark.

**B5.** [3] `400 × 32 = 12,800` pixels each way, so `12,800 × 12,800 = 163,840,000` pixels at 4 bytes =
**655,360,000 bytes**, about **0.65 GB**. Two marks for the working, one for the conclusion that this is
why chunking exists.

---

## Section C

**C1.** [3] `open` resolves relative to the **working directory**, which is wherever the game was
launched from, not where the script lives. Two marks. Fix:
`open(Path(__file__).parent / "level.txt")` — one mark.

**C2.** [4] Both axes are moved before anything is tested, so the undo removes **both** — two marks. The
consequences: the player stops dead at a corner instead of sliding, and in some arrangements the partial
undo lets them creep upward — one mark. Fix: move X, test and fix X, then move Y, test and fix Y — one
mark.

**C3.** [3] The trailing newline produced an empty last row, which the drawing code treats as a row of
nothing — two marks. Fix: drop trailing blank lines after loading, or use
`read().rstrip("\n").split("\n")` — one mark.

**C4.** [3] `rect.right` is the pixel **just past** the box, so a box ending exactly on a boundary is
counted as touching the next column — two marks. Fix: `(rect.right - 1) // TILE` — one mark.

**C5.** [4] The third row is 16 characters long instead of 20 — two marks. Indexing past the end of a
Python string raises `IndexError` — so either the game crashes, or (if `tile_at` catches it or uses
slicing) those positions silently are not solid — one mark. The load-time length check turns this from a
mystery into a message — one mark.

Worth noting out loud: in the JavaScript track the same bug returns an empty string rather than raising,
which is *worse*. Python at least tends to shout.

---

## Section D — marking the build

1. **The row-length check exists and was tested** (checkpoint 1). Ask to see their error message.
2. **Touched tiles are outlined** (checkpoint 3). It makes the "at most four" claim something they have
   seen, and it makes checkpoint 4 a five-minute job.
3. **Diagonal walking slides** (checkpoint 4). The test: walk into a wall at 45°. Stopping dead means the
   one-step version.
4. **`on_ground` is drawn as a word** (checkpoint 5), and set only by the downward test.
5. **Checkpoints 6 and 7 did not require touching the drawing code.** If adding spikes meant editing the
   draw loop, the table is not doing its job — a good moment to ask why.
6. **Checkpoint 8 produced two numbers**, not an impression.

---

## Section E — marking notes

**E1.** The table works for *properties* and breaks for *behaviour*. Signs: properties only some tiles
have, so the table grows ragged; a property that is really a verb (`opens`, `moves`); and anything that
must remember state over time — because every tile of a type shares **one** table entry, and a door needs
its own open/closed.

The usual answer is that such things stop being tiles and become **entities** that happen to sit on the
grid — which is why no commercial game implements a moving platform as a tile. Full marks for reaching
that in any words.

**E2.**

- **List of strings** — readable, hand-editable, one character per tile (so 256 types), and awkward to
  change one tile at runtime because strings are immutable.
- **List of lists** — easy to change one tile, any values, and the source no longer *looks* like the
  level.
- **Flat `bytearray`** — compact and fast, needs `row * width + col`, and is unreadable as text.
- **A real format (`.tmx`)** — layers, object placement, and a proper editor; and now you have a
  dependency and a parser to write or install.

For 10,000 wide: a **flat array**, and the better answers notice you would not hold the whole level in
memory at once — you would load it in chunks. Credit anyone who questions the premise.

**E3.** The collision code currently knows only *whether* a tile is solid. A one-way platform also needs
**the direction of travel** and **where the player was before the move**:

```python
if info.get("one_way"):
    top = row * TILE
    was_above = previous_bottom <= top + 1
    if not (moving_down and was_above):
        continue      # not solid this frame
```

Two marks for "it needs the direction", full marks for also realising it needs the *previous* position —
otherwise a player jumping up through the platform snaps onto its top at the apex, when their velocity
turns downward while they are still inside it. Students who try it with direction alone will find that
bug themselves, which is the best outcome.

**E4.** All three are used in real games.

- **Edit the level in memory** — the map stays the single source of truth, drawing and collision need no
  changes, and you have destroyed the original, so restarting needs a saved copy. Most students pick this
  and forget the restart; the question asks on purpose.
- **A separate set of taken positions** — `{(col, row), ...}`. The level is untouched and restarting is
  free; every draw and every pickup test consults a second structure.
- **Two layers** — terrain and items. More code up front, and it scales: items can be added, removed and
  reset without touching terrain, which is what nearly every commercial tile game does.

Full marks need a stated cost and a sensible answer about restarting. The best answers notice that
"reload the level from the file" makes option 1 fine, and that the real question is whether the loaded
level is treated as **read-only** — which is a genuinely professional instinct.

---

## If you only mark one thing

Walk the player diagonally into a corner. If they slide, the two-step resolution is right and lessons 7,
9 and 12 will work. If they climb or stick, nothing built on this lesson will behave, so it is worth
fixing before they go any further.
