# Web Games — Advanced Level

**HTML, CSS and JavaScript · 12 lessons · 4 weeks · 30 contact hours**

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
| 1 | The fixed timestep | why physics must not depend on frame rate; the accumulator |
| 2 | Entities as data | component thinking, arrays over object graphs, why ECS exists |
| 3 | Collision at scale | broad phase vs narrow phase, spatial hashing |
| 4 | Swept collision | tunnelling, continuous detection, separating axes |
| 5 | Pathfinding | BFS first, then A\*, on a tilemap |
| 6 | Procedural generation | randomness with rules, seeds, rooms and corridors |
| 7 | Performance and profiling | the devtools profiler, garbage, object pooling |
| 8 | What a shader actually is | WebGL in concept, measurable canvas effects in practice |
| 9 | Game architecture | events, decoupling, data-driven config |
| 10 | Juice II: feel engineering | input buffering, hitstop, camera dynamics |
| 11 | Shipping | accessibility, touch, resizing, deploying |
| 12 | **Capstone: a vertical slice** | one polished level, playtested and iterated on evidence |

---

## Before you start this level

You should have finished [`../intermediate_lvl/`](../intermediate_lvl/) (intermediate level), or be comfortable
with everything in it: the game loop, delta time, state, polled input, collision detection, state
machines, and describing levels as data rather than code.

**This level still uses no libraries** — Canvas 2D and plain JavaScript, as before.

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
python3 tools/new_lesson.py webgames/advanced_lvl 1 "The fixed timestep"
```
