# F2 — Building the instrument found the defect the instrument was meant to detect

**2026-08-20.** Method note. The corpus admissibility gate caught a live bug in the library on
the day it was written, before a single task existed.

## What happened

Corpus rule 5 says a task is admissible only if it compiles **gap-free against every profile**.
To prove the gate enforced that, `tests/test_gate.py` feeds it a task with no acceptance
criteria anywhere — not on the Task, not on any subtask — and demands a rejection.

The gate let it through.

## Why

D4 shipped two blocking gaps: `objective_empty`, and `acceptance_missing` when
`acceptance_binding >= 0.6`. But `render()` only reaches the `acceptance_missing` branch when
`acceptance_binding < 0.6 or not task.subtasks`. At high binding *with* subtasks present, the
criteria are supposed to move **into** the subtasks, and that path emitted
`subtask_acceptance_missing` — which was **advisory**.

So a brief compiled for `antigravity` (`acceptance_binding` 1.0), `casper` (1.0), `melchior`
(1.0), `codex` (0.9) or `balthasar` (0.9) at `implement` could carry a subtask list, no
observable definition of done anywhere in the document, and dispatch without complaint. The
condition D4 declared blocking was unenforced in exactly the configuration where the dial is
highest.

Fixed by making the subtask branch blocking at the same 0.6 threshold as the other branch, which
is what symmetry required all along. 42 tests green. Regression test added by name.

## The transferable part

The bug is unremarkable. **Where it was found is not.**

Nothing in the library's own 41 tests hit it, because they were written by the same person, on
the same day, with the same mental model — one that had `acceptance_missing` filed as "handled".
The gate found it because the gate was written against a *different* specification: the eval
protocol's rule 5, which says "gap-free in every arm" and does not care which code path produces
the gap.

That is the argument for building instruments before the thing they measure, and for writing
adversarial fixtures for every rule rather than trusting that a gate gates. A rule with no
fixture is a claim, and this project has already paid for two claims that were not checked
([[F1-agent-reports-need-grepping]]).

The cost of *not* finding it: tasks admitted with no acceptance criteria for the tight-contract
profiles, and arm C losing to arm F on those tasks for a reason that has nothing to do with
shaping. That is precisely the confound arm F exists to eliminate, arriving through the door
nobody was watching.

Related: [[H1-shaping-beats-information]], [[R1-arm-M-as-falsifier]]
