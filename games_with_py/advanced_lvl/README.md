# Games with Python — Advanced Level

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
> Start here instead: [`../intermediate_lvl/`](../intermediate_lvl/)

---

## What this level will cover

| # | Lesson | Core idea |
|---|---|---|
| 1 | Fixed timestep in Python | decoupling update from draw |
| 2 | Structuring a bigger game | packages, a scene manager, which way dependencies point |
| 3 | Data-driven design | enemies and levels as JSON, not as code |
| 4 | Dataclasses and type hints as design tools | making illegal states hard to write |
| 5 | Performance in Python | `cProfile`, what is actually slow, spatial partitioning |
| 6 | Pathfinding | BFS and A\* with `heapq` |
| 7 | Procedural generation | seeded dungeons, value noise |
| 8 | Particles and blend modes | surface tricks, additive blending |
| 9 | AI beyond `if` | state machines, steering behaviours, a first behaviour tree |
| 10 | Testing a game | `pytest` on game logic; separating logic from rendering so it *can* be tested |
| 11 | Packaging and shipping | PyInstaller, bundling assets, cross-platform traps |
| 12 | **Capstone: a roguelike slice** | generation + AI + persistence together |

---

## Before you start this level

You should have finished [`../intermediate_lvl/`](../intermediate_lvl/) (intermediate level), or be comfortable
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

This is the last level of the course. By the end of it you will have built a polished vertical slice and will know enough to pick up a full engine — Godot, Unity or Unreal — and recognise most of what it is doing.

## Contributing

If you are authoring these, [`docs/AUTHORING_GUIDE.md`](../../docs/AUTHORING_GUIDE.md) has the
mechanics and [`docs/COURSE_SPEC.md`](../../docs/COURSE_SPEC.md) has the contract. Start with:

```bash
python3 tools/new_lesson.py games_with_py/advanced_lvl 1 "Fixed timestep in Python"
```
