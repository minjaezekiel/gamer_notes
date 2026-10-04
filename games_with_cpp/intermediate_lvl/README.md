# Games with C++ — Intermediate Level

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
> Start here instead: [`../beginner_lvl/`](../beginner_lvl/)

---

## What this level will cover

| # | Lesson | Core idea |
|---|---|---|
| 1 | Setting up raylib | installing, compiling, linking, your first window |
| 2 | The raylib loop | shapes, colours, input, the frame |
| 3 | References, pointers and ownership | who owns this thing, and who frees it |
| 4 | Structs become classes | constructors, methods, a `Ball` that manages itself |
| 5 | Maths with raymath | vectors, angles, lerp |
| 6 | Many entities | `std::vector`, iterating, removing safely |
| 7 | Textures and sprite animation | loading, source rects, frame timing |
| 8 | Tilemaps from a file | parsing, drawing, colliding |
| 9 | `Camera2D` | scrolling and world vs screen coordinates |
| 10 | Sound and resource lifetime | RAII, load once, unload exactly once |
| 11 | Scenes and `enum class` | a state machine the compiler helps you get right |
| 12 | **Capstone: a raylib arcade game** | a complete, polished small game |

---

## Before you start this level

You should have finished [`../beginner_lvl/`](../beginner_lvl/) (beginner level), or be comfortable
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

[`../advanced_lvl/`](../advanced_lvl/) — 12 more lessons: fixed timestep, entities as data, collision at scale, pathfinding, procedural generation, profiling, and shipping.

## Contributing

If you are authoring these, [`docs/AUTHORING_GUIDE.md`](../../docs/AUTHORING_GUIDE.md) has the
mechanics and [`docs/COURSE_SPEC.md`](../../docs/COURSE_SPEC.md) has the contract. Start with:

```bash
python3 tools/new_lesson.py games_with_cpp/intermediate_lvl 1 "Setting up raylib"
```
