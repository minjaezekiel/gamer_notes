# CURRICULUM_MAP — all 90 lessons

The full shape of the course. Phase 1 authors the 18 beginner lessons; the other 72 are specified
here so that later sessions can resume without re-deriving the design, and so a teacher can see
where the course is heading from day one.

**Legend:** ✅ authored · 🟡 in progress · ⬜ specified, not yet authored

Cadence throughout: **3 lessons per week, 2 h 30 m each.**
Beginner = 2 weeks (6 lessons) · Intermediate = 4 weeks (12) · Advanced = 4 weeks (12).

---

## The spine, across all three tracks

Read this table sideways. The same concept appears in the same week in every track — that symmetry is
the design. A student who takes two tracks sees the same idea wearing different clothes, which is
what makes the idea stick.

| Beginner week/lesson | Web | Python | C++ |
|---|---|---|---|
| W1 L1 | the loop + first pixel | the loop without pixels | the compiler + first program |
| W1 L2 | coordinates, velocity, delta time | drawing with turtle | a game is data (structs) |
| W1 L3 | input as state | making it move | drawing with letters (buffer) |
| W2 L4 | collision | Snake | input and movement |
| W2 L5 | rules, score, feel | a real window (tkinter) | many things at once |
| W2 L6 | **capstone: Breakout** | **capstone: Brick Breaker** | **capstone: ASCII arcade** |

---

## `webgames/` — HTML, CSS, JavaScript (Canvas 2D, no frameworks, ever)

### `beginner_lvl/` — 6 lessons, 15 h

| # | Title | Core concept | Students build | State |
|---|---|---|---|---|
| 1 | What is a game, really? | rules, state, feedback loops; the loop; the canvas | first drawn + cleared frame | ✅ |
| 2 | Moving pictures | coordinates (Y points down), velocity, `requestAnimationFrame`, delta time | a bouncing ball that moves the same on any machine | ✅ |
| 3 | Player in control | events vs polled key *state*; input → intent | a paddle you steer | ✅ |
| 4 | When things touch | AABB overlap, circle distance, reflection | Pong, part 1 | ✅ |
| 5 | Rules, score and feel | state machine, scoring, sound, juice | Pong, finished | ✅ |
| 6 | **Capstone: Breakout** | levels as data, decomposition, debugging, publishing | complete Breakout | ✅ |

### `intermediate_lvl/` — 12 lessons, 30 h

| # | Title | Core concept | State |
|---|---|---|---|
| 1 | One file becomes many | ES modules, a `Game` object, dependency direction | ⬜ |
| 2 | Vectors for real | a `Vec2`, magnitude, direction, normalising | ⬜ |
| 3 | Acceleration, friction and drag | a ship that feels good to fly | ⬜ |
| 4 | Sprites and spritesheets | `drawImage`, source rects, animation frames | ⬜ |
| 5 | Tilemaps | levels as 2-D arrays, drawing a world, tile collision | ⬜ |
| 6 | The camera | scrolling, following the player, world vs screen space | ⬜ |
| 7 | Scenes, properly | menu / play / pause / transitions as a real state machine | ⬜ |
| 8 | Sound design with Web Audio | SFX, music, why audio timing is unforgiving | ⬜ |
| 9 | Particles and juice engineering | emitters, tweens, easing, screen shake | ⬜ |
| 10 | Enemies that seem to think | patrol, chase, flee; state-driven AI | ⬜ |
| 11 | Saving and loading | `localStorage`, JSON, high scores, settings | ⬜ |
| 12 | **Capstone: a platformer** | gravity, jumping, coyote time, a complete small game | ⬜ |

### `advanced_lvl/` — 12 lessons, 30 h

| # | Title | Core concept | State |
|---|---|---|---|
| 1 | The fixed timestep | why physics must not depend on frame rate; the accumulator | ⬜ |
| 2 | Entities as data | component thinking, arrays over object graphs, why ECS exists | ⬜ |
| 3 | Collision at scale | broad phase vs narrow phase, spatial hashing | ⬜ |
| 4 | Swept collision | tunnelling, continuous detection, separating axes | ⬜ |
| 5 | Pathfinding | BFS first, then A\*, on a tilemap | ⬜ |
| 6 | Procedural generation | randomness with rules, seeds, rooms and corridors | ⬜ |
| 7 | Performance and profiling | the devtools profiler, garbage, object pooling | ⬜ |
| 8 | What a shader actually is | WebGL in concept, measurable canvas effects in practice | ⬜ |
| 9 | Game architecture | events, decoupling, data-driven config | ⬜ |
| 10 | Juice II: feel engineering | input buffering, hitstop, camera dynamics | ⬜ |
| 11 | Shipping | accessibility, touch, resizing, deploying | ⬜ |
| 12 | **Capstone: a vertical slice** | one polished level, playtested and iterated on evidence | ⬜ |

---

## `games_with_py/` — Python

Beginner is **standard library only** (`turtle`, `tkinter`) so nothing needs installing and no school
IT lock-down can block it. `pygame-ce` arrives at intermediate, once the loop is already understood.

### `beginner_lvl/` — 6 lessons, 15 h

| # | Title | Core concept | Students build | State |
|---|---|---|---|---|
| 1 | The loop without pixels | state in variables; a game loop with no graphics at all | a text adventure with real state | ✅ |
| 2 | Drawing with turtle | coordinates, pen control, functions as reusable drawing | a game board and sprite art | ✅ |
| 3 | Making it move | `ontimer`, `tracer(0)`/`update()`, key bindings | a player you steer | ✅ |
| 4 | Snake | lists as the body, growth, self-collision, random food | Snake, complete | ✅ |
| 5 | A real window: tkinter | `Canvas`, `after()` as the frame timer, item ids | Catch the Falling Fruit | ✅ |
| 6 | **Capstone: Brick Breaker** | classes for entities, levels as nested lists, high scores to a file | complete Brick Breaker | ✅ |

### `intermediate_lvl/` — 12 lessons, 30 h (`pygame-ce`)

| # | Title | Core concept | State |
|---|---|---|---|
| 1 | Hello `pygame-ce` | installing it, surfaces, the explicit loop, the event queue | ⬜ |
| 2 | Rects, images and the display | blitting, transforms, loading assets | ⬜ |
| 3 | `Vector2` | movement at any angle, not just along the axes | ⬜ |
| 4 | Sprites and Groups | pygame's sprite system; update/draw for many things at once | ⬜ |
| 5 | Sprite animation | spritesheets, frame timing, animation driven by state | ⬜ |
| 6 | Tilemaps | loading a level from a text file; tile collision | ⬜ |
| 7 | Cameras and scrolling worlds | offsetting the world instead of moving the player | ⬜ |
| 8 | Sound and music | the mixer, channels, latency | ⬜ |
| 9 | Platform physics | gravity, platforms, axis-separated resolution | ⬜ |
| 10 | Enemies, waves and simple AI | spawning patterns, difficulty curves | ⬜ |
| 11 | Menus, scenes and save files | JSON persistence, settings | ⬜ |
| 12 | **Capstone: an arcade shooter** | waves, power-ups, score, a complete game | ⬜ |

### `advanced_lvl/` — 12 lessons, 30 h

| # | Title | Core concept | State |
|---|---|---|---|
| 1 | Fixed timestep in Python | decoupling update from draw | ⬜ |
| 2 | Structuring a bigger game | packages, a scene manager, which way dependencies point | ⬜ |
| 3 | Data-driven design | enemies and levels as JSON, not as code | ⬜ |
| 4 | Dataclasses and type hints as design tools | making illegal states hard to write | ⬜ |
| 5 | Performance in Python | `cProfile`, what is actually slow, spatial partitioning | ⬜ |
| 6 | Pathfinding | BFS and A\* with `heapq` | ⬜ |
| 7 | Procedural generation | seeded dungeons, value noise | ⬜ |
| 8 | Particles and blend modes | surface tricks, additive blending | ⬜ |
| 9 | AI beyond `if` | state machines, steering behaviours, a first behaviour tree | ⬜ |
| 10 | Testing a game | `pytest` on game logic; separating logic from rendering so it *can* be tested | ⬜ |
| 11 | Packaging and shipping | PyInstaller, bundling assets, cross-platform traps | ⬜ |
| 12 | **Capstone: a roguelike slice** | generation + AI + persistence together | ⬜ |

---

## `games_with_cpp/` — C++

Beginner is **terminal and ASCII, compiler only**. A beginner fighting a linker is a beginner who
quits, so lesson 1 compiles with one command and no flags. `raylib` arrives at intermediate.

### `beginner_lvl/` — 6 lessons, 15 h

| # | Title | Core concept | Students build | State |
|---|---|---|---|---|
| 1 | Closer to the metal | what a compiler does; edit → compile → run; why games use C++ | a dice / coin-flip game | ✅ |
| 2 | A game is data | types, the cost of memory, `struct` for game state | a text RPG battle with stats | ✅ |
| 3 | Drawing with letters | a 2-D array as a screen buffer; render and clear; `<chrono>` timing | an animated dungeon map | ✅ |
| 4 | Input and movement | reading keys, bounds checks, tile collision | an ASCII maze walker | ✅ |
| 5 | Many things at once | `std::vector` of entities, the update loop, collision | ASCII Pong | ✅ |
| 6 | **Capstone: ASCII arcade** | `.h`/`.cpp` split, a Makefile, fixed timestep, debugging | a complete arcade game | ✅ |

### `intermediate_lvl/` — 12 lessons, 30 h (`raylib`)

| # | Title | Core concept | State |
|---|---|---|---|
| 1 | Setting up raylib | installing, compiling, linking, your first window | ⬜ |
| 2 | The raylib loop | shapes, colours, input, the frame | ⬜ |
| 3 | References, pointers and ownership | who owns this thing, and who frees it | ⬜ |
| 4 | Structs become classes | constructors, methods, a `Ball` that manages itself | ⬜ |
| 5 | Maths with raymath | vectors, angles, lerp | ⬜ |
| 6 | Many entities | `std::vector`, iterating, removing safely | ⬜ |
| 7 | Textures and sprite animation | loading, source rects, frame timing | ⬜ |
| 8 | Tilemaps from a file | parsing, drawing, colliding | ⬜ |
| 9 | `Camera2D` | scrolling and world vs screen coordinates | ⬜ |
| 10 | Sound and resource lifetime | RAII, load once, unload exactly once | ⬜ |
| 11 | Scenes and `enum class` | a state machine that the compiler helps you get right | ⬜ |
| 12 | **Capstone: a raylib arcade game** | a complete, polished small game | ⬜ |

### `advanced_lvl/` — 12 lessons, 30 h

| # | Title | Core concept | State |
|---|---|---|---|
| 1 | Fixed timestep and interpolation | smooth rendering on top of discrete physics | ⬜ |
| 2 | Memory for game programmers | stack vs heap, smart pointers, no allocation in the loop | ⬜ |
| 3 | Data-oriented design | array-of-structs vs struct-of-arrays, cache lines, *measured* | ⬜ |
| 4 | A tiny ECS | entity ids, generations, systems | ⬜ |
| 5 | Broad-phase collision | a uniform grid / spatial hash | ⬜ |
| 6 | Swept collision | solving tunnelling properly | ⬜ |
| 7 | Pathfinding | A\* with a priority queue | ⬜ |
| 8 | Procedural generation | seeded RNG, reproducible worlds | ⬜ |
| 9 | Profiling and optimisation | measure first; `-O2`; where the time really goes | ⬜ |
| 10 | Shaders with raylib | GLSL basics and one real post-process effect | ⬜ |
| 11 | Build systems and shipping | Makefile → CMake, assets, other people's machines | ⬜ |
| 12 | **Capstone: a polished vertical slice** | architecture + performance + feel together | ⬜ |

---

## Cross-track callbacks (deliberate, keep these)

These are the moments where we explicitly point at another track. They are what turns three courses
into one course.

| In | Point back to | The observation |
|---|---|---|
| `py` B-L3 | `web` B-L2 | `turtle.ontimer` and `requestAnimationFrame` are the same idea with different names. |
| `cpp` B-L3 | `web` B-L1 | Clearing an ASCII buffer *is* `ctx.clearRect`. Rendering is "erase, then draw". |
| `cpp` B-L5 | `py` B-L4 | A `std::vector<Segment>` and a Python list of segments are the same design. |
| all B-L6 | each other | Three capstones, three languages, one architecture: data, update, draw. |
| all I-L1 | all B-L6 | The capstone's one big file is why we are about to learn to split it up. |
| all A-L1 | all B-L2 | Delta time was the beginner fix; the fixed timestep is the real one. |
