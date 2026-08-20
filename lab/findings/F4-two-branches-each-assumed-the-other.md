# F4 — Every brief compiled for codex was silently missing its acceptance criteria

**2026-08-20.** Found while dogfooding: compiling this project's own brief for `codex`, for the
harness bake-off, using the library the brief is about.

## The defect

`render()` decides acceptance criteria twice, in two branches that each assumed the other was
handling it.

```python
if d.decomposition >= 0.6:          # render the subtask list, criteria live inside it
    ...
if d.acceptance_binding < 0.6 or not task.subtasks:   # otherwise render them at the top
    ...
```

For `codex` — `decomposition` 0.35, `acceptance_binding` 0.9 — a Task carrying subtasks hits
**neither**:

- the top-level section is skipped, because binding is high *and* `task.subtasks` is non-empty, so
  the criteria are presumed to be inside the subtasks;
- the subtasks are never rendered, because `decomposition` is 0.35, and their criteria go with them.

The brief comes out with **no acceptance criteria anywhere and no gap raised.** The linter reported
`instructions_missing` — a different, minor thing — while the definition of done was on the floor.

The bug is the guard: `not task.subtasks` asks whether subtasks *exist*, when the only thing that
matters is whether they were *rendered*. Fixed by computing
`subtasks_rendered = d.decomposition >= 0.6 and bool(task.subtasks)` once and keying the acceptance
branch on that. 42 tests green, regression test across every profile.

## Why this one is worse than F2

It hit the profile carrying the most critical work. `codex` is the lane this project reserves for
"a critical, well-specified implementation", and 0.35/0.9 is not an odd corner — it is the shape
the profile was *designed* to have: **hand a principal engineer the contract, not a checklist.**
Exactly the configuration the profile exists for was the configuration that lost the contract.

It also breaks the library's central promise in the direction nobody watches. The README says the
dials *never invent content*. They also must never **silently delete** it: a field the Task carried,
that the recipient's own dials demanded, vanished with no gap. A gap would have been a bug report.
Silence was a lie of omission, and it shipped.

Three gap-related defects in one day — [F2](F2-the-gate-found-a-hole-in-the-gate.md),
[F3](F3-one-rule-for-five-ground-truths.md), and this — is not three unlucky bugs. It is one
structural weakness: **the gap linter is tested for what it reports, and not for what it fails to
notice.** Every test asserted "this input produces that gap". None asserted "no populated field ever
leaves the Task without either appearing in the brief or raising a gap". That invariant is the
actual contract, it is checkable across all profiles and phases with the `emitted()` helper arm F
already provides, and it should be the next thing written.

## The method note

All three were found by **building something that consumed the library from outside** — the corpus
gate, the sourcing brief, the bake-off brief — never by adding tests to the library. Self-written
tests share the author's blind spots by construction. Dogfooding is not a virtue signal here; it is
the only thing that has actually found defects.

Related: [[F2-the-gate-found-a-hole-in-the-gate]], [[F3-one-rule-for-five-ground-truths]]
