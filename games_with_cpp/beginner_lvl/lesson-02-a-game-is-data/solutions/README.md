# Lesson 2 — Solutions and marking notes

---

## Section A

**A1.** [3] A `struct` bundles related variables into one named type. One mark.
Two for any two of: related data cannot drift apart; functions take one argument instead of five;
adding another fighter is one line; the code says what the thing *is*; a typo in a field name becomes
a compile error.

**A2.** [3] `&` makes it a **reference** — the function works on the caller's actual variable, not a
copy, so changes stick. Two marks.

Without it the function gets a **copy**; it changes the copy, the copy is destroyed when the function
returns, and the original is untouched. One mark — and insist they mention that **there is no error
and no warning**.

**A3.** [2] When you only need to **read** something and it is **big enough that copying costs**.
`const` makes the compiler enforce the read-only part.

**A4.** [3] `(45 * 16) / 200 = 720 / 200 = **3**`. Two marks for the expression (multiply first), one
for the answer. A student who writes `(45 / 200) * 16` and answers 0 has found the bug the hard way —
give the method mark and point at B2.

**A5.** [2] **Cache.** Half the size means more of it fits in the processor's small fast memory, so
the program spends less time waiting for data. The game can run roughly twice as fast for that reason
alone, even on a machine with gigabytes free.

---

## Section B

**B1.** [4] Prints **100**. `heal` takes a `Fighter` **by value**, so it gets a copy. It adds 50 to
the copy's health, and the copy is discarded when the function returns. The original `troll` is never
touched.

Two marks for the value, two for the explanation. "It passes a copy" alone gets three; the fourth
mark is for noting there is no error.

**B2.** [4] `a = (80 * 16) / 100 = 1280 / 100 = **12**`.
`b = (80 / 100) * 16`. `80 / 100` is whole-number division, giving **0**, so `b = 0 * 16 = **0**`.

Version `b` is always 0 for anything below full health, because the fraction is thrown away before
the multiplication. Two marks for the values, two for the explanation.

**B3.** [3] `2147483647`, then `-2147483648`. The `int` wrapped round from its maximum to its
minimum. Two marks for the values, one for naming it as overflow.

(Worth mentioning to stronger students: signed overflow is technically *undefined behaviour* in C++,
so the compiler is permitted to do anything at all — in practice it usually wraps, but you should
never rely on it.)

**B4.** [4] **It does not compile.** The error is roughly
`cannot assign to variable 'f' with const-qualified type 'const Fighter &'`.

**Yes, the compiler is right.** `const` is a promise that this function will not modify what it was
given, and the assignment breaks that promise. The compiler catching it is the entire point of
`const` — the caller passed their real fighter in, trusting it would only be read.

Two marks for "does not compile", two for defending the compiler. Students who say the compiler is
being awkward have missed the idea; ask them what the caller was relying on.

---

## Section C

**C1.** [4] Both parameters are passed **by value**, so `do_attack` modifies copies. The defender's
real health is never touched, so the battle never ends.

Fix: `void do_attack(Fighter& attacker, Fighter& defender)`.

Two marks for the diagnosis, one for the fix, and **one for noting that nothing warns you** — the
code is completely legal C++ and compiles cleanly even with `-Wall`.

This is the defining bug of the lesson. Students who have written it themselves in checkpoint 4 will
answer instantly, which is exactly why checkpoint 4 asks them to.

**C2.** [3] The semicolon after the closing brace: `};` not `}`. A struct declaration is a statement
and needs one.

The error points at whatever comes next, because the compiler is still waiting for the declaration to
end and reads the following function as part of it. Warn students in advance — the message is one of
the worst in C++ for a beginner.

**C3.** [4] The fields other than `name` are **uninitialised**. `Fighter goblin;` sets aside the
memory but does not fill it in, so `health`, `max_health`, `attack` and `defence` contain whatever
junk was in that memory — different on each run.

Then `(health * WIDTH) / max_health` divides by a junk `max_health`, which can be enormous, negative,
or even zero (which crashes).

Two marks for "uninitialised", one for "it is junk, not zero", one for a fix: use `make_fighter`, or
`Fighter goblin = {};` to zero everything, or assign every field.

---

## Section D — marking the build

Checkpoint 4 is a full pass — and it is the lesson.

**Make them actually do checkpoint 4 in the wrong order.** Writing `do_attack` without the `&`,
running it, and watching a clean compile produce a battle where nobody can be hurt is worth more than
any explanation. Do it on the projector too if the class is quiet about it.

**Checkpoint 2.** The point of `make_fighter` is that `max_health` cannot disagree with `health`.
Students who set both by hand have working code and have missed the reason.

**Checkpoint 3.** Test at zero health. If they divide without clamping, a dead fighter can produce a
negative bar length, and the loop either prints nothing or runs oddly.

**Checkpoint 6.** The expected answer is one or two lines. If adding a third fighter took them twenty
lines, their functions are not taking `Fighter&` parameters, and that is worth showing them.

---

## Section E — marking notes, not answers

**E1.** The honest tension: a single `Item` struct with every possible field
(`heal_amount`, `attack_bonus`, `unlocks_door`, `charges`, …) means every potion carries an unused
`unlocks_door` and every key carries an unused `heal_amount`. It works, and it gets ugly fast.

Expected approaches, all legitimate at this level:

| Approach | Cost |
|---|---|
| One struct with all fields | wasted space, and nothing says which fields matter for which item |
| A `kind` field plus shared fields | needs a `switch` everywhere, but is simple and common |
| A struct per item type | cannot put them in one inventory without more machinery |
| A `name` plus a list of effects | general and flexible; much more code |

The second is what most small games actually do and is a fine answer. Students who notice that the
"all fields" version wastes memory *and* readability have got the point. The real resolution is
inheritance or variants, which is well beyond today — do not go there.

**E2.** The answer is that a `std::string` stores a **pointer** to the actual characters, which live
elsewhere in memory. The struct holds the fixed-size string *object* (typically 24 or 32 bytes),
not the text. So `sizeof` never changes no matter how long the name is.

This is a genuinely good question to have worked out, and it is the first appearance of an idea that
matters a lot later: **some data is stored where you can see it, and some is stored somewhere else
with a pointer to it.** That is the stack-versus-heap distinction, and it is lesson 2 of the advanced
level. Do not teach it properly today — just let the observation sit.

(Short strings are often stored *inside* the object by an optimisation called SSO, which is why the
number is as large as it is. Only mention this if a student goes looking.)

**E3.** Mark on reasoning. Things worth drawing out:

- C++'s way lets you **choose**: copy when safety matters, reference when speed matters, `const&`
  when you want both. Python decides for you and the decision is invisible.
- The cost is that you can get it wrong silently, which is exactly what C1 is about.
- Python is not actually "always references" — it is more subtle, and a student who has been bitten
  by mutating a list passed into a function has met the same issue from the other side.

The best answers notice that C++ makes you state something you were relying on anyway, and that
stating it is both the burden and the benefit.

---

## Teacher note: the photocopy demonstration

Do this physically, it takes thirty seconds, and it works better than any diagram.

Write a number large on a sheet of paper. **Photocopy it**, hand the copy to a student, and ask them
to change the number. Show the class the original: unchanged.

Then hand over the **original** and ask again. Now it has changed.

Write `&` on the board and say: *"this one character is the difference between handing someone a
photocopy and handing them the original."*
