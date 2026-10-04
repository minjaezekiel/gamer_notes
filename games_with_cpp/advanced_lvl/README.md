# Games with C++ — Advanced Level

**C++ · 12 lessons · 4 weeks · 30 contact hours**

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
| 1 | Fixed timestep and interpolation | smooth rendering on top of discrete physics |
| 2 | Memory for game programmers | stack vs heap, smart pointers, no allocation in the loop |
| 3 | Data-oriented design | array-of-structs vs struct-of-arrays, cache lines, *measured* |
| 4 | A tiny ECS | entity ids, generations, systems |
| 5 | Broad-phase collision | a uniform grid / spatial hash |
| 6 | Swept collision | solving tunnelling properly |
| 7 | Pathfinding | A\* with a priority queue |
| 8 | Procedural generation | seeded RNG, reproducible worlds |
| 9 | Profiling and optimisation | measure first; `-O2`; where the time really goes |
| 10 | Shaders with raylib | GLSL basics and one real post-process effect |
| 11 | Build systems and shipping | Makefile → CMake, assets, other people's machines |
| 12 | **Capstone: a polished vertical slice** | architecture + performance + feel together |

---

## Before you start this level

You should have finished [`../intermediate_lvl/`](../intermediate_lvl/) (intermediate level), or be comfortable
with everything in it: the game loop, delta time, state, polled input, collision detection, state
machines, and describing levels as data rather than code.

**This level uses `raylib`.** Lesson 1 covers installing it.

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
python3 tools/new_lesson.py games_with_cpp/advanced_lvl 1 "Fixed timestep and interpolation"
```
