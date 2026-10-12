# F6 — The compiler removed 22% of what it was given, and reported none of it

**2026-09-10.** Measured, not argued:
[`lab/measurements/silent_subtraction.py`](../measurements/silent_subtraction.py). One Task with
every field populated, compiled at all 144 (profile × phase × stakes) points.

| | |
|---|---|
| populated field-renderings | 2160 |
| removed from the brief | **448 (20.7%)** |
| gaps raised across all 144 briefs | **0** |

Gaps fire on *absence*, and nothing here was absent. So the linter — the part of this project the
README calls "the product" — was structurally incapable of saying a word about a quarter of the
content it was handed.

Most of those removals are correct. Selection is what the dials are *for*: `codex` gets a contract
rather than a checklist, so its subtask list goes; `grok` is not authorised to decide, so the open
decisions go. The defect was never the removal. It was that the removal was inaudible.

## The case that made it worth fixing

Removed most often, across the 144 points:

```
open_decisions        91     subtasks          78     acceptance     66
escalation_triggers   78     instructions      66     verification   45
```

`escalation_triggers` is the one with teeth. On **2026-08-20** a brief compiled for `codex` lost
three escalation triggers that were safety stops — *do not bind pihole's port 53, do not fall back
to the 7.4 GiB laptop, do not copy an identity to the server* — because `escalation_explicitness`
resolved to 0.45 against a 0.60 render threshold. That was caught by reading the rendered text, by
luck, and fixed with a manual override. The logbook recorded it as an open design question.

It was not a one-off. `escalation_explicitness` cannot reach 0.60 for `antigravity`, `claude`,
`codex` or `grok` at **any** phase and **any** stakes level — see
[F7](F7-the-dials-are-continuous-the-renderer-is-not.md). Four of the eight shipped profiles will
silently discard a stop condition every time one is supplied, and raising stakes to high does not
help any of them.

## The fix, and why it is not a gap

A new `Drop` alongside `Gap`. A gap points forward — *the recipient needs something you did not
supply*. A drop points backward — *you supplied something and the shape removed it*. Opposite
directions, opposite remedies (gather it, versus override the dial), so they get separate channels.
Reporting 423 correct selections as gaps would have buried the two that were not.

Each drop names the dial, its resolved value, the threshold it failed, **which side** of the
threshold it is on (so a caller knows which way to turn it), and the rationale:

```
escalation_triggers was supplied but this shape drops it: escalation_explicitness
is 0.45, below the 0.60 threshold — no escalation path is stated at this setting
```

Detection is derived from the rendered text, not from a second copy of the render logic. F4 was two
branches each assuming the other had rendered the field; a checker that reads the output cannot make
that mistake.

## Two things found while building it

**The detector under-reported, and an independent count caught it.** The probe said 543 removals,
the detector said 417. The difference was `_subtask_marker` indexing `[0]` into both a list
(`acceptance`, giving the first criterion) and a string (`verification`, giving the first
*character*, which is present in every brief). Same class of bug as F4: one branch handling two
shapes. Worth recording that the fix was found by disagreement between two counts, not by reading
the code.

**The first version of the invariant passed the defect it was written for.** Reverting F4's fix,
the invariant stayed green: it reported the lost acceptance criteria as a legitimate drop with the
rationale *"criteria are bound inside each subtask instead"* — while the subtask list had never been
rendered. The rationale was **named** but never **checked**. Fixed by verifying that the stated
cause actually holds, and the F4 revert now fails
`test_every_drop_is_explained_by_a_dial`. An invariant that accepts a false explanation is an
invariant that accepts anything.

## The live defect it found on its first run

With `decomposition >= 0.6` and a Task carrying `instructions` but **no subtasks**, both branches
are skipped: there is no subtask list to render, and the instructions branch is gated on the dial
being *low*. The brief goes out with an objective, a return contract and **no statement of what to
do**:

```
# ANTIGRAVITY — visual engineer / frontend / synthesizer / computer operator
## Objective
Rebuild the settings screen.
## Acceptance criteria
- every panel renders at 360px
## Return
- changed files ...
```

`subtasks_missing` fires, but it is advisory, so `bliss compile --gate` passes this. It affects
`antigravity`, `casper`, `melchior` and `balthasar` — every profile whose `decomposition` is high by
design, which is four of seven, and is F4's exact twin one section down the renderer. Fixed: the
instructions render as a degraded `Task` section with the gap still raised. Degraded, flagged and
non-empty beats clean and silent.

## The noise objection, answered with a count

The obvious objection is that the fix reproduces the problem: 448 advisory notices are as easy to
ignore as silence was, and the failure mode has moved from invisible to unreadable. Put to an
adversarial reviewer, and answered with a measurement rather than an argument.

The 448 is a property of the **test fixture**, which populates every field at every point precisely
so the script can subtract. A realistic dispatch carries only the fields an operator actually filled
in. On one such task — an architecture decision, sparsely populated, compiled at `design` and normal
stakes — the operator sees:

| profile | drops | which |
|---|---|---|
| `grok` | 3 | current_state, verification, escalation_triggers |
| `antigravity`, `claude` | 2 | open_decisions / verification, escalation_triggers |
| `casper`, `codex`, `melchior` | 1 | open_decisions, or escalation_triggers |
| `astra`, `balthasar` | 0 | — |

**At most three notes per dispatch.** That is readable, and each one names the dial, the value, the
side of the threshold and the rationale, none of which silence provided. The objection is right that
a drop *can* still be ignored; that is an argument for ranking them one day, not for not emitting
them.

## What this does not show

One task, fully populated, one author. Presence is checked by substring against the rendered text,
so a marker that coincidentally appears elsewhere would hide a removal — false negatives are
possible, false positives are not. The 20.7% is a property of *these* eight profiles, and a
profile set with less extreme dials would remove less.

52 tests green.

**Reviewed 2026-09-10 by balthasar at `/reasoning max`, verdict SURVIVES AS WRITTEN.** Every figure
above was re-derived independently from the committed measurement script, and the realistic-load
table is its work, re-run here before being accepted.

Related: [[F4-two-branches-each-assumed-the-other]], [[F2-the-gate-found-a-hole-in-the-gate]],
[[F7-the-dials-are-continuous-the-renderer-is-not]]
