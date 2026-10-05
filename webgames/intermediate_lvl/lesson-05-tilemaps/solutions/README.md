# Lesson 5 — Solutions and marking notes

---

## Section A

**A1.** [3] Any three: it is tiny (160 characters for a whole level) · the data looks like the level, so
you can read and edit it by eye · lookups are instant, because you work out which square to look at
rather than testing every wall · editing is editing text, with no tools to write. One mark each.

The strongest answer is the lookup one. Push for it if nobody offers it: with rectangles you ask every
wall "am I in you?"; with a grid you work out your seat number and look at that seat.

**A2.** [2] `round` goes to the *nearest* boundary, so a point 97% of the way across a tile is reported
as being in the next one, putting every collision up to half a tile out — one mark. Chopping the decimals
(`| 0`, `parseInt`, `Math.trunc`) is right for positive numbers and wrong for negative ones: a player at
`x = -5` is in column −1, not 0, so they can stand inside the left-hand wall — one mark.

**A3.** [2] Any two problems removed: no `undefined` error when the player leaves the array · no separate
"am I off the screen?" code · the border of `#` in the level becomes optional · the player can never
escape the world. One mark each.

**A4.** [3] Because a single combined move that ends inside a wall gives you **no information about which
direction caused it** — two marks. Resolving one axis at a time means each correction already knows the
direction it is undoing, so there is nothing to guess — one mark.

Bonus observation worth praising: it also gives wall-sliding for free, because X can be cancelled while
Y is allowed to continue.

**A5.** [2] It is what the **downward** collision test reports: if moving down put you inside a solid
tile, you have landed — one mark. Setting it from a key press means the game believes the player's input
rather than the world, and the two disagree the moment they walk off a ledge — one mark.

**A6.** [2] It stops a box whose edge lands exactly on a tile boundary from being counted as touching the
next tile along — one mark. Without it, the player sticks in gaps exactly their own width, because the
game thinks they are overlapping a wall they are only adjacent to — one mark.

**A7.** [2] Adding a tile type becomes one line of data rather than another branch in several places —
one mark — and the drawing and collision code never grow at all, because they ask the table rather than
knowing the answers — one mark.

---

## Section B

**B1.** [3] `col = floor(95/32) = 2`, `row = floor(64/32) = 2`. Two marks. Top-left corner is
`(64, 64)` — one mark. Note that 64 is exactly on a boundary, which is the case the `- 0.001` exists for.

**B2.** [4] `c0 = floor(60/32) = 1`, `c1 = floor((60+26-0.001)/32) = floor(85.999/32) = 2`.
`r0 = floor(30/32) = 0`, `r1 = floor((30+26-0.001)/32) = floor(55.999/32) = 1`.
So columns 1–2 and rows 0–1: **four squares**. One mark per line, up to four.

**B3.** [3] With the `- 0.001`: `c0 = 2`, `c1 = floor(89.999/32) = 2`, so **one column**. Two marks.
Without it: `c1 = floor(90/32) = 2` — the same here. Give the third mark for noticing that the real
difference appears when the box's *right* edge is exactly on a boundary: a box at x = 38 with width 26
has its right edge at 64 exactly, giving `c1 = 1` with the fudge and `c1 = 2` without, which is the
sticking bug. Credit anyone who constructs that case themselves.

**B4.** [4] Movement is `500 × 0.1 = 50`, so the untouched new y is 150. Row 5 starts at `y = 160`. The
player's bottom edge is at `150 + 26 = 176`, which is inside row 5, so the test fires. Two marks. The
correction is `y = 5 × 32 − 26 = 134`, and `vy = 0`, with `onGround = true`. Two marks.

**B5.** [3] Naive: `300 × 300 = 90,000` tiles per frame. Culled: about `26 × 17 = 442`. Two marks for the
numbers, one for the ratio — roughly **200 times** less work.

---

## Section C

**C1.** [3] `Math.round` instead of `Math.floor`. Two marks. The row flips to the next one when the player
is halfway through a tile, so everything is out by `TILE / 2 = 16` pixels — one mark.

**C2.** [4] Both axes are moved before anything is tested, so the undo has to remove **both**. Two marks.
The consequences: the player stops dead at a corner instead of sliding, and in some arrangements the
partial undo lets them creep upwards. Fix, two marks: move X, test and fix X, then move Y, test and fix
Y — two separate steps with two separate tests.

**C3.** [3] There is no out-of-bounds check, so `LEVEL[row]` is `undefined` for a negative row, and
`undefined.charAt` throws. Two marks. Fix: return `"#"` for anything off the map — one mark.

**C4.** [4] Two faults. (a) `onGround` is set for **any** collision, including a sideways one, so pressing
into a wall makes the game believe the player is standing on something — two marks. (b) `vy = 0` is also
applied to a horizontal collision, which cancels falling whenever they touch a wall — two marks.

Each axis's correction must only touch its own velocity, and only the *downward* Y correction may set
`onGround`.

Worth saying to the class: this bug is also how wall-jumping works. The difference between a bug and a
feature is whether you meant it and can control it.

**C5.** [3] The third row is 16 characters long instead of 20. Two marks. `LEVEL[row].charAt(col)` returns
an **empty string** for columns past the end — not `undefined`, so nothing throws — and an empty string
is not `"#"`, so those positions are not solid. One mark. This is why checkpoint 1 asks for a
same-length check at startup.

---

## Section D — marking the build

1. **The row-length check exists** (checkpoint 1). It takes four lines and prevents C5, which is otherwise
   a half-hour mystery.
2. **The touched tiles are outlined** (checkpoint 3). This is the single most useful debugging aid in the
   lesson, and it makes the "at most four" claim something they have seen rather than been told.
3. **Diagonal walking slides** (checkpoint 4). The test: walk into a wall at 45°. If they stop dead, they
   have written the one-step version.
4. **`onGround` is drawn on screen** (checkpoint 5) and is only ever set by the downward test. Watch for
   C4 in their own code; about half the class will write it.
5. **Checkpoints 6 and 7 did not require touching the drawing code.** If adding spikes meant editing the
   draw loop, the table is not doing its job — a good moment to ask why.

Checkpoint 7 is the one students enjoy most and it is more than a toy: once the level is data in a text
box, they start designing levels, and designing levels is where they discover what their own collision
code does wrong.

---

## Section E — marking notes

**E1.** The table works beautifully for *properties* and starts to fail for *behaviour*. Signs it is
breaking: properties that only some tiles have, so the table grows ragged; a property that is really a
verb (`opens`, `moves`, `spawns`); and anything that needs to remember state over time, because every
tile of a type shares one table entry and a door needs its own open/closed.

The usual answer is that such things stop being tiles and become **entities** that happen to sit on the
grid. Full credit for reaching that, in any words. Good follow-up: moving platforms are not tiles in any
commercial game, for exactly this reason.

**E2.**

- **Array of strings** — readable, editable by hand, one character per tile so only 256 types, and awkward
  to change a single tile at runtime (strings are immutable, so you rebuild the row).
- **Array of arrays** — easy to change one tile, any values you like, and the level no longer *looks* like
  the level in the source.
- **Flat array** — fastest and most compact, needs `row * WIDTH + col` arithmetic, and is impossible to
  read as text.
- **One string with newlines** — compact for loading from a file, and needs splitting before use.

For 10,000 tiles across the answer is a **flat typed array** (`Uint8Array`), and the better answers also
notice that at that size you would not store the whole level at once — you would load it in chunks. Credit
anyone who questions the premise.

**E3.** The collision code currently knows only *whether* a tile is solid. For a one-way platform it must
also know **the direction of travel** and **where the player was before the move**:

```js
if (TILES[t].oneWay) {
  // only solid if we are moving DOWN and our feet were above its top edge
  const topEdge = hit.row * TILE;
  if (player.vy > 0 && previousBottom <= topEdge) { /* land */ }
  else { /* pass through */ }
}
```

Two marks for "it needs to know the direction of movement", and full marks for also realising it needs the
*previous* position, or the player will snap to the top of a platform they are halfway through. Students
who try it with direction alone will find that bug themselves, which is the best outcome.

**E4.** All three are used in real games.

- **Change the level array** — the map stays the single source of truth, drawing and collision need no
  changes, and you have destroyed the original, so restarting the level needs a saved copy. (Most
  students pick this and forget the restart problem; the question asks about it on purpose.)
- **A separate list of taken coins** — the level is untouched and restarting is free, but every draw and
  every pickup test has to consult a second structure, and a `Set` of `"col,row"` strings is the usual
  shape.
- **Two layers** — a terrain layer and an items layer. More code up front and it scales: items can be
  added, removed and reset without touching terrain, which is what nearly every commercial tile game
  does.

Full marks need a stated cost and a sensible answer on restarting. The best answers notice that "load the
level from the original data" makes option 1 fine, and that the real question is whether the level data is
treated as read-only — which is a genuinely professional instinct.

---

## If you only mark one thing

Walk the player diagonally into a corner. If they slide, the two-step resolution is right and the rest of
the level will work. If they climb or stick, nothing built on top of this lesson will behave, so it is
worth fixing before they go any further.
