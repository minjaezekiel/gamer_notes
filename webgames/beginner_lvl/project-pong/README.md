# Project: Pong, stage by stage

Pong is not built in one lesson. It grows across four of them, and each stage adds exactly one idea.

The staged files are **the lesson code examples themselves** — there are no duplicate copies here,
so nothing can drift out of sync with the lessons. This page tells you which file is which stage, and
how to see precisely what changed between them.

| Stage | What it adds | The file |
|---|---|---|
| **1. The ball** | velocity, delta time, bouncing off walls | [`lesson-02/code/03-bouncing-ball.html`](../lesson-02-moving-pictures/code/03-bouncing-ball.html) |
| **2. The paddle** | polled input, clamping to the screen | [`lesson-03/code/03-paddle.html`](../lesson-03-player-in-control/code/03-paddle.html) |
| **3. Collision** | AABB, two paddles, ball steering, an opponent | [`lesson-04/code/04-pong-part-1.html`](../lesson-04-when-things-touch/code/04-pong-part-1.html) |
| **4. A real game** | states, score, sound, shake, particles | [`lesson-05/code/04-pong-complete.html`](../lesson-05-rules-score-and-feel/code/04-pong-complete.html) |

## Seeing exactly what each stage added

From this folder:

```bash
# stage 1 -> stage 2: what did adding a player cost?
diff ../lesson-02-moving-pictures/code/03-bouncing-ball.html \
     ../lesson-03-player-in-control/code/03-paddle.html

# stage 3 -> stage 4: what turns a toy into a game?
diff ../lesson-04-when-things-touch/code/04-pong-part-1.html \
     ../lesson-05-rules-score-and-feel/code/04-pong-complete.html
```

If `diff` is unfamiliar, open the two files side by side in your editor instead. Most editors have a
"compare with" option.

### Why this is worth doing

Reading a finished 400-line game teaches you much less than seeing four 100-line additions. The
question to keep asking is not *"what does this code do?"* but **"what problem made this line
necessary?"**

A good exercise: before running a diff, write down what you *think* changed. Then check. The gap
between your prediction and the real diff is the most useful thing on this page.

## Suggested teaching use

- **Stage 1 → 2.** Ask the class what has to be added for a player to exist. Most will say "read the
  keyboard" and miss the clamping entirely.
- **Stage 2 → 3.** The collision test is four lines. The *response* — fixing the position, steering
  the ball, stopping the re-catch — is much more. Worth pointing out: detecting is the easy half.
- **Stage 3 → 4.** This is the big one. Almost none of the added code changes who wins. Ask the class
  to count how many of the new lines affect the *rules* versus the *feel*.

## Build it yourself

The point is not to read these. Each lesson's `exercises.md` section D walks you through building
your own version, and yours will be better than these because you will understand every line of it.
