# Lesson 6 — Solutions and marking notes

---

## Section A

**A1.** [3] `.h` holds **declarations** — what exists, so other files know what they may call.
`.cpp` holds **definitions** — the actual code. Two marks.

One mark for a reason to split: you can find things; changing one file only recompiles that file;
several people can work at once; and the header documents what a part is *meant* to be used for.

**A2.** [2] It makes the compiler read that header only once per compilation. Without it, two files
both including it would declare everything twice and the compiler would report redefinition errors.

**A3.** [3] **Compiling** turns each `.cpp` into a `.o` separately, needing only the declarations.
**Linking** joins the `.o` files into one executable, matching every call to its definition. Two
marks.

One mark for the messages:
- compile: `error: use of undeclared identifier 'put'`
- link: `Undefined symbols ... "put(int, int, char)"`

**A4.** [2] Delta time still lets **one frame be enormous** — after a stall, a suspend, or a window
drag. Everything then takes one huge step and a fast object can jump straight through a wall
(**tunnelling**). A fixed timestep keeps every step the same size, so that cannot happen.

**A5.** [3] **Subtract** because it keeps the leftover time, so the game stays exactly in step with
the real world. Zeroing it throws time away and the game slowly runs behind. Two marks.

**Clamp** because without it a long stall tries to run hundreds of updates in one frame, which takes
even longer, which makes the next gap bigger — the **spiral of death**, from which the game never
recovers. One mark.

---

## Section B

**B1.** [4] `0.05 ÷ 0.0167 = 2.99`, so `update` runs **three times**... let us be exact:
after 3 steps the accumulator has had `3 × 0.01667 = 0.05` taken off, leaving about **0.0000**.
Accept "three times, with essentially nothing left" or "two times with 0.0167 left" if they
consistently use 0.0166.

Next frame at 0.005 s: the accumulator reaches only 0.005, which is less than `STEP`, so `update`
runs **zero times**. Two marks each.

The zero-times case is the interesting one and worth discussing: a frame where no physics happens at
all is normal and correct, and the time is not lost — it waits in the accumulator.

**B2.** [3] **Linking** fails. `game.cpp` compiles fine, because `screen.h` declares `put` and that is
all the compiler needs. The linker then cannot find any definition of `put`, because `screen.o` was
never built or never passed in.

Error: `Undefined symbols ... "put(int, int, char)"`.

**B3.** [3] The Makefile is missing the dependency lines that say each `.o` also depends on the
headers it includes (`screen.o: screen.cpp screen.h`). `make` only looks at `screen.cpp`, which has
not changed, so it does nothing.

What they experience: **their change appears to do nothing**, and they will conclude their code is
wrong when the build is. `make clean && make` forces it, which is why students learn that incantation
early.

**B4.** [4] Roughly one mark each, plus one for comparing them:

- **Version A (delta time):** `frame_time` is 10 seconds. Everything moves 10 seconds' worth in **one
  step** — bullets teleport past aliens without colliding, and the player may be instantly dead or
  instantly safe. Tunnelling at its worst.
- **Version B (fixed, no clamp):** the accumulator holds 10 seconds, so the `while` loop runs **600
  updates** in one frame. The game fast-forwards 10 seconds correctly, but the frame takes a long
  time — and if that pushes the next frame over, the problem compounds. The spiral of death.
- **Version C (clamped):** `frame_time` becomes 0.25, so **15 updates** run. The game loses 9.75
  seconds of simulated time but stays responsive and never tunnels. **This is what you want.**

The honest point: version C deliberately *loses time*. That is a trade, not a perfect fix — and for
a game with a real-time clock or a network connection, losing time has its own consequences.

---

## Section C

**C1.** [3] The indented line starts with **spaces instead of a tab**. Make requires a real tab
character at the start of every rule's commands.

Why the message is unhelpful: Make is simply reporting that the line is not any syntax it recognises
— it has no idea the author meant a rule. And the difference is **invisible** in most editors, which
is what makes this such a notorious trap. Tell students how to switch on "show whitespace".

**C2.** [4] `int WIDTH = 46;` in a header is a **definition**, not a declaration. Every `.cpp` that
includes the header gets its own definition of the same global name, and the linker finds several and
refuses. `#pragma once` does not help: it prevents the header being read twice *per file*, not once
*per project*. Two marks.

Why `const int` works: a `const` variable at namespace scope has **internal linkage** by default in
C++ — each file quietly gets its own private copy, so there is no clash. Two marks.

(Other correct fixes, worth accepting: `inline constexpr int WIDTH = 46;`, or `extern int WIDTH;` in
the header with the definition in exactly one `.cpp`.)

**C3.** [4] Two problems, and the `accumulator = 0.0` is the main one.

`if` instead of `while` means **at most one update per frame**, so if the accumulator ever holds
enough for two steps, the extra is never run. And `accumulator = 0.0` **throws away the leftover
time** instead of keeping it.

Together, the game consistently advances less simulated time than real time has passed, so it runs
slow — even though the frame rate is fine. Two marks for the `while`, two for the subtraction.

This is a good one to trace on the board, because the symptom ("runs at half speed") does not
obviously point at either line.

---

## Section D — marking the capstone

Mark on four things:

1. Does it build with `make` and run?
2. Is it **genuinely** split — headers declaring, sources defining, and `main.cpp` short?
3. Can they explain any function you point at?
4. **Did they change something to make it theirs?**

Checkpoint 4 is a full pass; 5 and 6 are distinction.

**Say point 4 before they start**, or they will aim for a copy of the example.

**The most common structural failure** is a "split" where `game.h` declares everything in the program
and `main.cpp` still does most of the work. Ask them how long `main.cpp` is — in the reference project
it is about 90 lines, almost all of it the timing loop.

**Checkpoint 2 — make them demonstrate the incremental rebuild.** Touch one `.cpp`, run `make`, and
watch only one compile line appear. It is the whole point of a Makefile and it takes ten seconds to
show.

**Giving them the reference project to extend is a legitimate route** if time is short. Reading and
modifying a multi-file project is closer to what they will actually do later than building one from
nothing, and it is a genuinely valuable skill in its own right.

---

## Section E — marking notes, not answers

**E1.** `screen.cpp` and `terminal.cpp` are **reusable unchanged** in any terminal game. `game.cpp` is
not — it is entirely about aliens. `main.cpp` is somewhere in between: the timing loop is general, but
the specific calls to `game_update` and `game_draw` are not.

What makes the difference: the reusable files **know nothing about this particular game**. `screen.cpp`
knows about a grid of characters; it has never heard of an alien. The moment a file mentions aliens,
it stops being reusable.

That observation is the whole of E4, and students who get here have essentially answered both.

**E2.** If the buffer were available everywhere, any file could write to it **without the bounds
check** — and the out-of-bounds bug from lesson 3 comes straight back, now from anywhere in the
program. You would also have no idea which files touch it, so changing how it works would mean
checking every file.

Keeping it `static` means there is exactly **one** way to draw, and that way is safe. The general
principle: **make the safe way the only way.**

**E3.** There is no single right answer and arguing about it is most of software architecture. A
reasonable platformer split:

| File | Holds |
|---|---|
| `screen` / `renderer` | drawing primitives |
| `input` | keyboard, gamepad |
| `level` | loading and storing the tilemap, tile collision |
| `player` | the player's state and movement |
| `entities` | enemies, items, projectiles |
| `game` | rules, score, win and lose |
| `main` | the loop and timing |

Things to probe: where does *collision between the player and the level* live — in `player` or in
`level`? (Either; it depends which one you would rather have know about the other.) What happens when
`entities` needs to know about `level`? Students discovering that **the dependencies between files
matter more than the files** have found the real content of the question.

**E4 — the engine question.** Look for the division:

**Reusable:** the screen buffer; input; the timing loop with its fixed timestep; collision helpers;
random numbers; a particle system; a state machine.

**Always specific:** what the entities are; what a collision *means*; the win and lose rules; the
level data; how it feels.

The best answers notice the boundary keeps moving — is "bullet" general or specific? — and that
over-generalising produces an engine harder to use than writing the game directly.

Tell them afterwards: **that is what a game engine is**, and `raylib`, which the intermediate level
starts with, is somebody else's answer to exactly this question. They will be able to look at it and
recognise the decisions.

---

## End of the C++ beginner track

Put lesson 1's `01-hello.cpp` on the projector next to today's project. Six lines, next to six files.

Then point out that the **shape never changed**: state, a loop, input, update, render. The same
structure they met on day one — in whichever track they started with.

Then be honest about what comes next. `raylib` at intermediate level gives them pixels, textures,
sound and proper held-key input. It does **not** give them a single new idea about how a game is
structured. They already have that, and that is why the next level will feel fast.
