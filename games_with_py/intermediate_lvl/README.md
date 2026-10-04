# Games with Python — Intermediate Level

**Python · 12 lessons · 4 weeks · 30 contact hours**

> ## ⬜ Not yet authored
>
> This level is **fully specified but not yet written**. The lessons below are the plan, taken from
> [`docs/CURRICULUM_MAP.md`](../../docs/CURRICULUM_MAP.md), and they are being authored in order.
>
> **What exists today:** all three `beginner_lvl` tracks are complete — 18 lessons with notes,
> runnable code, exercises, worked solutions and printable handouts. See
> [`docs/PROGRESS.md`](../../docs/PROGRESS.md) for exactly what is built.
>
> Start here instead: [`../beginner_lvl/`](../beginner_lvl/)

---

## What this level will cover

| # | Lesson | Core idea |
|---|---|---|
| 1 | Hello `pygame-ce` | installing it, surfaces, the explicit loop, the event queue |
| 2 | Rects, images and the display | blitting, transforms, loading assets |
| 3 | `Vector2` | movement at any angle, not just along the axes |
| 4 | Sprites and Groups | pygame's sprite system; update/draw for many things at once |
| 5 | Sprite animation | spritesheets, frame timing, animation driven by state |
| 6 | Tilemaps | loading a level from a text file; tile collision |
| 7 | Cameras and scrolling worlds | offsetting the world instead of moving the player |
| 8 | Sound and music | the mixer, channels, latency |
| 9 | Platform physics | gravity, platforms, axis-separated resolution |
| 10 | Enemies, waves and simple AI | spawning patterns, difficulty curves |
| 11 | Menus, scenes and save files | JSON persistence, settings |
| 12 | **Capstone: an arcade shooter** | waves, power-ups, score, a complete game |

---

## Before you start this level

You should have finished [`../beginner_lvl/`](../beginner_lvl/) (beginner level), or be comfortable
with everything in it: the game loop, delta time, state, polled input, collision detection, state
machines, and describing levels as data rather than code.

**This level uses `pygame-ce`.** Lesson 1 covers installing it.

## A note on what changes and what does not

Nothing in this level replaces the structure you already have. The loop is the same loop; the state
machine is the same state machine. What this level adds is **more inside** that structure — better
tools, more objects, and the techniques that stop a bigger game becoming unmanageable.

If a lesson here ever seems to introduce a brand new way of organising a game, read it again. It
almost certainly is not.

## Where next

[`../advanced_lvl/`](../advanced_lvl/) — 12 more lessons: fixed timestep, entities as data, collision at scale, pathfinding, procedural generation, profiling, and shipping.

## Contributing

If you are authoring these, [`docs/AUTHORING_GUIDE.md`](../../docs/AUTHORING_GUIDE.md) has the
mechanics and [`docs/COURSE_SPEC.md`](../../docs/COURSE_SPEC.md) has the contract. Start with:

```bash
python3 tools/new_lesson.py games_with_py/intermediate_lvl 1 "Hello `pygame-ce`"
```
