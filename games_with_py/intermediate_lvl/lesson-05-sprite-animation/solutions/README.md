# Lesson 5 — Solutions and marking notes

---

## Section A

**A1.** [3] Any two, with the third mark for a clear consequence: one file is one load rather than thirty
· the graphics card never has to switch image, which is slow compared with drawing · one thing to name
and not lose · the poses stay in step with each other because they are in one picture.

**A2.** [3] `subsurface` returns a **Surface** that shares the parent's pixels, with no copying — so it
can be assigned to `self.image`, which `blit` cannot do — two marks. One thing it will not let you do:
blit it onto its own parent; also, the parent must stay valid and must not be drawn over — one mark.

**A3.** [3] A slow frame may have taken long enough for two or more poses to be due — one mark. `if`
advances only one and silently drops the rest — one mark — so the animation runs slow exactly when the
machine is already struggling, which is the worst possible time — one mark.

**A4.** [2] Subtracting keeps the leftover time, so the next pose comes a little sooner and the average
rate is exact — one mark. Zeroing throws it away, so every pose is slightly too long and the animation
drifts slow — one mark.

**A5.** [3] `!=` fires once, on the frame the state *changed*; `==` fires on **every** frame they are in
that state — two marks. The symptom: the frame and timer are reset before the timer can ever reach
`FRAME_TIME`, so the animation stays on pose 0 for ever — one mark.

**A6.** [2] Because the position then refers to the character's feet — one mark — so a taller pose grows
upwards instead of pushing the feet through the floor, and "stand on the ground" is
`rect.bottom = floor_y` — one mark.

**A7.** [2] Because at zero speed the factor is zero, the frame time is `1/0`, and the animation never
advances — one mark — so the character freezes mid-stride, which reads as broken rather than still —
one mark.

---

## Section B

**B1.** [3] 6 columns, 3 rows — one mark. Row 2, column 4: `Rect(128, 64, 32, 32)` — two marks.

**B2.** [3] `60 / 8 = 7.5` game frames per pose, so it alternates between 7 and 8 — two marks. 24 poses
in three seconds — one mark.

**B3.** [4] Steps of 0.01667 reach 0.125 after 8 of them, at 0.1333 s, and zeroing throws the extra
0.0083 away — so each pose lasts **0.1333 s** instead of 0.125 — two marks. That is 6.7% slow, so after
60 seconds the animation is about **4 seconds** behind — two marks. Accept 3.5–4.5.

**B4.** [3] The index becomes 6, which is past the end of a six-item list — one mark —
`IndexError: list index out of range` — one mark — raised on the line that assigns `self.image`, not on
the line that incremented the frame — one mark.

**B5.** [3] Speed 0 → **0.4** (the clamp). 80 → 0.4 (0.4 is the clamp; `80/200 = 0.4` exactly, so either
reading gives 0.4). 200 → **1.0**. 600 → **2.0** (the clamp). Three marks, roughly one per two answers.

---

## Section C

**C1.** [3] The pose advances once per **game** frame rather than on its own clock — two marks — so the
animation speed is whatever the frame rate happens to be, and is faster on a faster machine — one mark.
Fix: a timer and `FRAME_TIME`.

**C2.** [3] The reset runs on every frame they are walking, so `timer` never reaches `FRAME_TIME` — two
marks. Fix: compare with the previous state, `if self.state != self.last_state:` — one mark.

**C3.** [3] 190 is not a multiple of 32 — the last column would need to run from 160 to 192 and the
Surface stops at 190 — two marks. "Only sometimes" because the error appears only when the slicing
reaches that final column — one mark. Fix: make the sheet 192 wide, or compute the column count with
integer division and accept five columns.

**C4.** [4] The rect is re-anchored at `topleft`, so a taller image extends **downwards**, pushing the
feet below the floor — two marks. On landing the collision code pushes them back out, which is the "pop"
— one mark. Fix: `self.image.get_rect(midbottom=self.rect.midbottom)` — one mark.

**C5.** [3] `pygame.transform.flip` is called **every frame, for every character**, and each call makes a
new Surface — two marks. Fix: build both direction sets once at startup and choose between two lists —
one mark.

---

## Section D — marking the build

1. **The sheet is drawn magnified with a grid** (checkpoint 1). It makes every later bug a glance rather
   than a guess.
2. **The three-number readout exists** (checkpoint 3): pose, timer, game frames. Insist on it.
3. **They wrote the `==` version first** (checkpoint 4) and saw the animation stick on pose 0. Meeting it
   deliberately is worth far more than being warned.
4. **The feet stay put** when the jump pose is taller (checkpoint 6). Test it in front of them.
5. **Checkpoint 7 was done both ways.** Removing the lower clamp and standing still produces a frozen
   mid-stride pose that looks like a crash and is not.
6. **Checkpoint 8 is kept.** The side-by-side switch is the best demonstration in the lesson and costs
   two lines.

---

## Section E — marking notes

**E1.**

*Sharing is right* when the sheet is built once and never changed — which is the normal case. It is free,
and thousands of frames cost no extra memory.

*Sharing causes a hard bug* when the parent Surface is later drawn over: every subsurface silently
changes, and nothing in the animation code is wrong. The classic version is building the sheet, slicing
it, and then reusing the same Surface to build a second sheet. Credit also: a subsurface of the **display
surface**, which pygame flips and reuses every frame.

Full marks for naming one of each with the mechanism, not just the words.

**E2.**

- **In the class** — everything in one place, easy to follow, and a change means editing code.
- **A separate module** — still code, but the tuning is in one file a programmer can hand over.
- **A JSON file** — a non-programmer can edit it, it can ship separately, and you have taken on loading,
  validating and handling a corrupt file (lesson 11's whole subject).
- **Passed in** — the most flexible and the most plumbing; the same Sprite class can serve two games.

For a non-programmer changing frame rates: **JSON**, with the cost stated — somebody has to write the
loader and decide what happens when the file is wrong. Credit anyone who notes that the right answer
depends on how often it changes, and that the honest default is to start in the class and move it out
when somebody actually asks.

**E3.** The state machine needs two things it has not got:

1. **A one-shot mode.** Some animations loop; `attack` must stop at the last frame rather than wrapping.
   That is a flag in the table — `"loop": False` — and a different end condition in the timer.
2. **A memory of what to return to.** The attack must know what was happening before, or it has to
   re-derive the state from scratch when it ends (which is usually fine and simpler).

Attacking again halfway through is the interesting part, and there are three defensible answers:

- **restart it** — responsive, and it can be spammed so the animation never completes;
- **ignore it** — the animation always finishes, and the game feels unresponsive;
- **buffer it** — remember the press and start the next attack the instant this one ends.

The third is what good action games do, and it is exactly the jump-buffering idea from the web track's
capstone. Full marks for choosing one and naming its cost; strong credit for recognising the buffer.

**E4.** "Speed" should mean **how fast the character is moving relative to the ground they are standing
on**, not how fast they are moving through the world.

- Carried by a moving platform: their world speed is the platform's, and their feet are still. Use
  `velocity - platform.velocity`.
- Walking into a wall: their world speed is **zero** while they are still trying to walk. Here the
  animation should probably keep playing, so what you want is the *intended* speed, not the achieved one.
- Pushed by an explosion: they are moving fast and not walking at all — which argues the animation should
  be driven by **input or intent**, not by velocity.

The best answers conclude that there are two different quantities — *intent* and *achieved movement* —
and that different animations want different ones: walking wants intent, a slide or a skid wants the
achieved speed. Credit any answer that separates those two, however phrased. This is the same
intent-versus-input distinction from the beginner levels, arriving in a new place.

---

## If you only mark one thing

Checkpoint 4, with the `==` version written first and then fixed. It is the one bug in this lesson whose
symptom — an animation stuck on its first pose — gives no hint at all about its cause, and meeting it on
purpose is the only cheap way to learn it.
