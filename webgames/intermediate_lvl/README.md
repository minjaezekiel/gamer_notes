# Web Games — Intermediate Level

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
> Start here instead: [`../beginner_lvl/`](../beginner_lvl/)

---

## What this level will cover

| # | Lesson | Core idea |
|---|---|---|
| 1 | One file becomes many | ES modules, a `Game` object, which way dependencies point |
| 2 | Vectors for real | a `Vec2` class, magnitude, direction, normalising |
| 3 | Acceleration, friction and drag | a ship that feels good to fly |
| 4 | Sprites and spritesheets | `drawImage`, source rects, animation frames |
| 5 | Tilemaps | levels as 2-D arrays, drawing a world, tile collision |
| 6 | The camera | scrolling, following the player, world vs screen space |
| 7 | Scenes, properly | menu / play / pause / transitions as a real state machine |
| 8 | Sound design with Web Audio | SFX, music, why audio timing is unforgiving |
| 9 | Particles and juice engineering | emitters, tweens, easing, screen shake |
| 10 | Enemies that seem to think | patrol, chase, flee; state-driven AI |
| 11 | Saving and loading | `localStorage`, JSON, high scores, settings |
| 12 | **Capstone: a platformer** | gravity, jumping, coyote time, a complete small game |

---

## Before you start this level

You should have finished [`../beginner_lvl/`](../beginner_lvl/) (beginner level), or be comfortable
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

[`../advanced_lvl/`](../advanced_lvl/) — 12 more lessons: fixed timestep, entities as data, collision at scale, pathfinding, procedural generation, profiling, and shipping.

## Contributing

If you are authoring these, [`docs/AUTHORING_GUIDE.md`](../../docs/AUTHORING_GUIDE.md) has the
mechanics and [`docs/COURSE_SPEC.md`](../../docs/COURSE_SPEC.md) has the contract. Start with:

```bash
python3 tools/new_lesson.py webgames/intermediate_lvl 1 "One file becomes many"
```
