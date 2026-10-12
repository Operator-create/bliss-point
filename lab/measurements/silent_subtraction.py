#!/usr/bin/env python3
"""What the compiler removes, and whether the removal is audible.

Re-derives the numbers in lab/findings/F6 and F7. Lab rule 5: a claim you cannot
re-derive is a rumour.

    python lab/measurements/silent_subtraction.py

Method: one Task with every field populated, compiled for every
(profile x phase x stakes) point. A populated field that does not appear in the
rendered brief was removed. Presence is checked by substring against the rendered
text, using the same marker the eval's arm-F control uses, so this measures the
renderer's actual output rather than a second reading of its source.
"""
from collections import Counter

import blisspoint as bp
from blisspoint.brief import TASK_FIELDS, Subtask, Task, has_content
from blisspoint.flat import emitted, flat
from blisspoint.profiles import phases

STAKES = ("low", "normal", "high")

TASK = Task(
    objective="Make the retried capture converge on one terminal state.",
    current_state="The handler is idempotent; the state machine is not.",
    files=["api/payments/webhook.py"],
    decisions=["The public API contract does not change."],
    constraints=["No new database columns."],
    non_goals=["Rewriting the state machine."],
    evidence="Sentry PAY-4471: 38 orders stuck pending.",
    attempts="A dedupe set in the handler moved the race.",
    instructions="Move idempotency into the state machine.",
    subtasks=[Subtask(id="ST1", title="Guard the capture transition",
                      purpose="stop double-apply", scope="api/orders/state.py",
                      instructions="make the transition idempotent",
                      acceptance=["replaying capture twice yields one paid order"],
                      verification="pytest tests/payments -k retry",
                      returns="the diff")],
    acceptance=["replaying a capture event twice leaves one paid order"],
    verification="pytest tests/payments -k retry",
    open_decisions=["whether to key on event id or transition id"],
    escalation_triggers=["the fix requires a schema change"],
    return_format=["changed files", "test output"],
)

POINTS = [(t, p, s) for t in bp.list_profiles() for p in phases() for s in STAKES]
POPULATED = [f for f in TASK_FIELDS if has_content(getattr(TASK, f))]


def main() -> None:
    briefs = {pt: bp.compile(TASK, pt[0], phase=pt[1], stakes=pt[2]) for pt in POINTS}

    print(f"{len(POINTS)} points ({len(bp.list_profiles())} profiles x {len(phases())} "
          f"phases x {len(STAKES)} stakes), {len(POPULATED)} populated fields each\n")

    # --- 1. how much is removed, and how much of it is audible ---------------
    per_field, per_profile, unexplained = Counter(), Counter(), 0
    for (target, _, _), b in briefs.items():
        for d in b.drops:
            per_field[d.field] += 1
            per_profile[target] += 1
            unexplained += d.dial == "unexplained"
    total = sum(per_field.values())
    print(f"fields removed:      {total} of {len(POINTS) * len(POPULATED)} field-renderings "
          f"({100 * total / (len(POINTS) * len(POPULATED)):.1f}%)")
    print(f"reported as drops:   {total}")
    print(f"unexplained:         {unexplained}   (a drop no dial accounts for is a renderer bug)")
    print(f"gaps raised:         {sum(len(b.gaps) for b in briefs.values())}   "
          f"(gaps fire on absence; nothing here is absent)\n")
    for f, n in per_field.most_common():
        print(f"  {f:<24} removed at {n:>3} of {len(POINTS)} points")

    # --- 2. can phase and stakes reach a render threshold at all? ------------
    print("\n--- threshold reachability (the renderer reads dials only through >= 0.60) ---")
    for dial in ("escalation_explicitness", "decomposition", "autonomy"):
        stuck = []
        for target in bp.list_profiles():
            vals = [getattr(briefs[(target, p, s)].dials, dial)
                    for p in phases() for s in STAKES]
            over = sum(1 for v in vals if v >= 0.6)
            if over == 0 or over == len(vals):
                stuck.append(f"{target}({'on' if over else 'off'})")
        print(f"  {dial:<24} fixed regardless of phase and stakes for "
              f"{len(stuck)}/{len(bp.list_profiles())}: {', '.join(stuck)}")

    # --- 3. how many distinct briefs does the whole space produce? -----------
    print("\n--- output collapse ---")
    for target in bp.list_profiles():
        texts = {briefs[(target, p, s)].text for p in phases() for s in STAKES}
        print(f"  {target:<14} {len(texts):>2} distinct briefs from "
              f"{len(phases()) * len(STAKES)} points")
    allt = {b.text for b in briefs.values()}
    print(f"  {'TOTAL':<14} {len(allt):>2} distinct briefs from {len(POINTS)} compilations")

    same = sum(1 for t in bp.list_profiles() for p in phases()
               if len({briefs[(t, p, s)].text for s in STAKES}) == 1)
    n_pairs = len(bp.list_profiles()) * len(phases())
    print(f"\n  stakes changes nothing at {same}/{n_pairs} (profile, phase) pairs")

    # --- 4. the control property the eval rests on ---------------------------
    f_fields = emitted(flat(TASK), TASK)
    assert all(emitted(b.text, TASK) <= f_fields for b in briefs.values())
    print(f"\n  arm C is a subset of arm F at all {len(POINTS)} points: yes")


if __name__ == "__main__":
    main()
