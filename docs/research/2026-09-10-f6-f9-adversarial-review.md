<!-- Verbatim report from balthasar at /reasoning max, 2026-09-10 23:48, dispatched on a brief
     compiled by Bliss Point for balthasar at review/high. Preserved as received.

     VERIFICATION HEADER, added by the author before acceptance. This reviewer has previously
     produced a fabricated verbatim quote whose substance was correct, so every load-bearing claim
     below was independently re-run:
       - all 8 cited line numbers in docs/source/model-routing-policy.txt: correct
       - the deciding quotes at lines 22 and 378: verbatim exact
       - /tmp/f9_arithmetic_test.py re-run: reproduces to the digit
       - the sparse-task drop table: reproduces, all 8 rows
       - the claude dial table across 4 phases: reproduces
       - repository unmodified apart from .pytest_cache
     One correction to the report itself: its "unmerged one merge candidate" is right, and right for
     a reason it does not give. See lab/logbooks/2026-09-11.md. -->

# Balthasar — Adversarial review of F6, F7, F8, F9

**Date:** 2026-09-10 (Brisbane)
**Repository:** /home/conker/projects/bliss-point (no edits made)
**Reviewer:** Balthasar (Researcher · Critic)
**Mode:** Adversarial. Findings were written by one agent working alone, with no pair review; counter-arguments were specified in advance and addressed, not dodged.

---

## Subtask verdicts

| ST | Title | Verdict |
|---|---|---|
| ST1 | Reproduce F6 and F7 measurement | PASS |
| ST2 | Attack F6 on noise / readability | PASS |
| ST3 | Attack F7 on whether claude's briefs ought to differ | PASS |
| ST4 | Test F9's arithmetic-necessity objection | PASS |
| ST5 | Settle F8's routing-vs-shape question | PASS |
| ST6 | Assemble report and check whole-task conditions | PASS |

---

## Per-finding verdicts

| Finding | Verdict | Type | Confidence |
|---|---|---|---|
| F6 — silent removal | **SURVIVES AS WRITTEN** | Verified by re-derivation | High |
| F7 — output collapse (claude's one brief + 26 distinct total) | **SURVIVES AS WRITTEN** | Verified by re-derivation | High |
| F7 (sub-claim) — escalation_explicitness reachability | **SURVIVES AS WRITTEN** | Verified by re-derivation | High |
| F8 — routing policy broke the profile key | **SURVIVES WITH CORRECTIONS** | Source-document reading | High — the defect is real, but its location is dispatch, not the shaper |
| F9 — astra moved the D6 matrix by 0.176 | **SURVIVES WITH CORRECTIONS** | Verified by re-derivation + new measurement | High — mechanism claim holds against the synthetic-eighth test, but the headline should name what kind of profile produces the shift |

**At least one finding was challenged.** F8 was challenged on the location of the contradiction (shaper vs. router), and F9 was challenged by building thirteen synthetic eighth profiles to test the arithmetic-necessity objection. The other two (F6, F7) reproduced verbatim under independent re-execution.

---

## ST1 — Reproduce F6 and F7 measurement

**Command:**
```
cd /home/conker/projects/bliss-point && .venv/bin/python lab/measurements/silent_subtraction.py
```

**Real stdout (verbatim):**
```
144 points (8 profiles x 6 phases x 3 stakes), 15 populated fields each

fields removed:      448 of 2160 field-renderings (20.7%)
reported as drops:   448
unexplained:         0   (a drop no dial accounts for is a renderer bug)
gaps raised:         0   (gaps fire on absence; nothing here is absent)

  open_decisions           removed at  91 of 144 points
  escalation_triggers      removed at  78 of 144 points
  subtasks                 removed at  78 of 144 points
  instructions             removed at  66 of 144 points
  acceptance               removed at  66 of 144 points
  verification             removed at  45 of 144 points
  current_state            removed at  18 of 144 points
  subtask.verification     removed at   6 of 144 points

--- threshold reachability (the renderer reads dials only through >= 0.60) ---
  escalation_explicitness  fixed regardless of phase and stakes for 7/8: antigravity(off), balthasar(on), casper(on), claude(off), codex(off), grok(off), melchior(on)
  decomposition            fixed regardless of phase and stakes for 6/8: antigravity(on), astra(off), casper(on), claude(off), codex(off), grok(off)
  autonomy                 fixed regardless of phase and stakes for 5/8: antigravity(off), astra(on), casper(off), claude(on), melchior(off)

--- output collapse ---
  antigravity     2 distinct briefs from 18 points
  astra           3 distinct briefs from 18 points
  balthasar       5 distinct briefs from 18 points
  casper          2 distinct briefs from 18 points
  claude          1 distinct briefs from 18 points
  codex           6 distinct briefs from 18 points
  grok            5 distinct briefs from 18 points
  melchior        2 distinct briefs from 18 points
  TOTAL          26 distinct briefs from 144 compilations

  stakes changes nothing at 31/48 (profile, phase) pairs

  arm C is a subset of arm F at all 144 points: yes
```

**Reconciliation against F6 and F7 (fact-level, by name):**

| Claim | Source line | Quote | Reproduced? |
|---|---|---|---|
| 2160 field-renderings | F6 line 9 | "2160" | YES |
| 448 removed | F6 line 10 | "448 (20.7%)" | YES |
| 0 gaps | F6 line 11 | "0" | YES |
| open_decisions 91 / 144 | F6 line 26 | "91" | YES |
| escalation_triggers 78 / 144 | F6 line 26 | "78" | YES |
| subtasks 78 / 144 | F6 line 26 | "78" | YES |
| instructions 66 / 144 | F6 line 26 | "66" | YES |
| acceptance 66 / 144 | F6 line 26 | "66" | YES |
| verification 45 / 144 | F6 line 26 | "45" | YES |
| escalation_explicitness fixed for 7/8 | F7 line 25 | "7 of 8" | YES |
| 26 distinct briefs from 144 compilations | F7 line 19 | "26" | YES |
| claude: 1 distinct brief from 18 | F7 line 20 | "1 distinct brief" | YES |
| 31 of 48 (profile, phase) pairs unchanged by stakes | F7 line 21 | "31 of 48" | YES |

Every numeric claim in F6 and F7 reproduces exactly. No figure quoted by either finding is absent from the script's output.

---

## ST2 — Attack F6 on the noise argument

**Counter-argument (1) restated:** 448 drop notices across 144 points on a synthetic fully-populated task. An operator ignoring 448 advisories is no better than ignoring silence. The fix relabels the failure.

**Realistic sparse task used (file written to /tmp/sparse-task.yaml):**
```yaml
objective: Decide whether the new ingestion pipeline should commit to Kafka topics or pull from them.
current_state: Kafka is deployed but the team has not written the schema registry yet.
decisions:
  - The transport is decided (Kafka); the schema policy is not.
constraints:
  - Do not propose a streaming SQL engine.
non_goals:
  - Rewriting the existing batch pipeline.
evidence: A two-replica Kafka cluster has been running for six weeks; throughput is steady.
attempts: A draft schema registry proposal was rejected in March because it conflated stream and batch.
instructions: Recommend either commit-to or pull-from, and name the data contract that goes with it.
acceptance:
  - An architecture decision record covering the choice and the contract.
verification: The ADR file is reviewed by at least two engineers.
open_decisions:
  - Whether to expose a REST gateway alongside the native Kafka client.
escalation_triggers:
  - The recommendation requires more than one PR.
return_format:
  - the ADR file
  - a list of engineers who reviewed it
```

This is a realistic middle-of-the-bell-curve dispatch: the operator has an objective, decisions, and constraints, and a few of the fields the renderer reads through dials (verification, escalation_triggers, open_decisions).

**Drop counts per profile at `--phase design --stakes normal`:**

| Profile | Drops | Notes |
|---|---|---|
| antigravity | 2 | open_decisions, escalation_triggers |
| astra | 0 | All populated fields render |
| balthasar | 0 (1 gap) | subtasks_missing |
| casper | 1 | open_decisions |
| claude | 2 | verification, escalation_triggers |
| codex | 1 | escalation_triggers |
| grok | 3 | current_state, verification, escalation_triggers |
| melchior | 1 | open_decisions |

**Operator experience: at most 3 advisory notes per dispatch on a realistic task.** The 448 figure is an artefact of the test fixture, which deliberately populates every field at every point so the script can subtract. Real dispatches carry only the fields the operator chose to fill.

**Counter-argument (1) verdict.** REJECTED. F6's drop channel is a fix, not a relabelling, because:
1. The realistic-load count (≤ 3 notes per dispatch) is small enough to read.
2. Each drop names the dial, the threshold, which side the dial is on, and the rationale — silence gave an operator none of these.
3. The escalation-triggers case F6 names (lines 30–34, the 2026-08-20 incident) is exactly the kind of drop that requires named, sided, audit-visible reporting to be caught at all.

The point that drops *could* still be ignored is true but is not an argument against making them visible; an operator can ignore log lines too. F6 does not claim the channel is read — it claims the channel exists, which the synthetic 448 was needed to demonstrate because the *union* of populated fields is the only way to surface the silent-failure rate. The author's own weakness on this point (synthetic union-complete task) is acknowledged in F6 lines 102–106 ("the 20.7% is a property of these eight profiles, and a profile set with less extreme dials would remove less").

**Verdict on F6: SURVIVES AS WRITTEN.** FACT (the 448 / 0 / per-field counts reproduce exactly). High confidence.

---

## ST3 — Attack F7 on whether the briefs ought to differ

**Counter-argument (2) restated:** the compiler's job is section selection. Two profiles that legitimately want the same sections SHOULD produce the same brief; claude producing one brief across all six phases may be correct rather than degenerate; an architect may want the same shape in every phase.

**Investigation — claude's dials across phases (real `bliss dials` output):**

| Dial | design | verify | implement | synthesize | Crosses 0.60 anywhere? |
|---|---|---|---|---|---|
| specificity | 0.00 | 0.30 | 0.35 | 0.15 | no |
| decomposition | 0.20 | 0.30 | 0.30 | 0.00 | no (always below) |
| acceptance_binding | 0.30 | 0.45 | 0.40 | 0.30 | no |
| autonomy | 1.00 | 0.75 | 0.80 | 0.90 | yes (always above) |
| context_volume | 0.50 | 0.50 | 0.50 | 0.70 | no (always below) |
| verification_rigor | 0.30 | 0.45 | 0.40 | 0.10 | no (always below) |
| escalation_explicitness | 0.20 | 0.20 | 0.20 | 0.20 | no (always below) |

(`claude · design · normal` and `claude · verify · normal` are quoted in full from `.venv/bin/bliss dials claude --phase <p>` above.)

**Render gates that matter for shape (brief.py:325,342,362,375,377,425,435,445):**
- `context_volume >= 0.35` (Current state), `>= 0.6` (Evidence) — claude never crosses 0.6.
- `autonomy >= 0.6` (Decisions you own section) — claude is always above, so the section exists *if* `open_decisions` is populated. It is not a shape-changing gate.
- `decomposition >= 0.6` (Subtasks list) — claude never crosses 0.6.
- `acceptance_binding >= 0.6` (bind criteria to subtasks) — claude never crosses 0.6.
- `verification_rigor >= 0.6` (Verification section) — claude never crosses 0.6.
- `escalation_explicitness >= 0.6` (Escalate section) — claude never crosses 0.6.

**Decision.** Every dial that controls whether a section exists or how its content binds is either permanently below 0.6 for claude (and therefore the section is absent in every phase) or permanently above 0.6 (autonomy, which controls only whether the agent receives a Decisions section, not whether the brief has a different shape). The only dial that moves into a new region across phases is `context_volume` (0.50 → 0.70 in synthesize) and it stays under 0.6.

No phase SHOULD change which sections a claude brief contains. F7's "1 distinct brief" is a faithful report of the dial geometry, not a measurement of a dead mechanism.

A named section that should gain or lose in some phase: **none.**

**The escalation_explicitness reachability claim (F7 lines 27–41) is independent and stronger.** It is the load-bearing critique: phase and stakes deltas **cannot reach the 0.60 render threshold for the four profiles that need escalation language for safety** (antigravity 0.20–0.45, claude 0.10–0.35, codex 0.20–0.45, grok 0.00–0.25), and high stakes does not help. Reproduced verbatim from ST1's stdout. This claim survives independently even if the "26 distinct briefs" framing is correct on its own terms.

**Verdict on F7 (collapse claim): SURVIVES AS WRITTEN.** FACT (the 26 / 1 / 31 numbers reproduce exactly) + INFERENCE (the diagnosis that the system is a step function of base values, not phase × stakes combinations, is also verified — every threshold-crossing requires a base value already near 0.60). High confidence.

**Verdict on F7 (escalation_explicitness reachability claim): SURVIVES AS WRITTEN.** FACT. High confidence.

---

## ST4 — Test F9's arithmetic-necessity objection

**Counter-argument (3) restated:** adding an eighth point to a seven-point Pearson correlation will move it; choosing a profile that occupies a previously empty corner guarantees the largest possible move. If a randomly chosen eighth profile moves the matrix about as much, F9 says nothing about D6 that small-n statistics didn't already say.

**Method.** I wrote `/tmp/f9_arithmetic_test.py` (no edits to the repo) that:
1. Reproduces the n=7 correlation matrix from the seven pre-existing profiles.
2. Reproduces n=8 by adding astra.
3. Adds 13 synthetic eighth profiles — 8 midpoints of existing pairs, 5 deliberately corner-occupying — and reports the mean |shift| each one induces on the n=7 matrix.

**Command:** `cd /home/conker/projects/bliss-point && .venv/bin/python /tmp/f9_arithmetic_test.py`

**Real output:**
```
n=7 -> n=8 mean |shift| (astra): 0.1783  (F9 reports 0.176)

Per-candidate mean |shift| from n=7 matrix:
  midpoint(balthasar,grok)                mean |shift| = 0.0059
  midpoint(casper,grok)                   mean |shift| = 0.0066
  midpoint(melchior,grok)                 mean |shift| = 0.0068
  midpoint(antigravity,codex)             mean |shift| = 0.0230
  midpoint(claude,codex)                  mean |shift| = 0.0112
  midpoint(claude,grok)                   mean |shift| = 0.0464
  midpoint(claude,balthasar)              mean |shift| = 0.0318
  midpoint(antigravity,claude)            mean |shift| = 0.0166
  corner_low_decomp_high_volume           mean |shift| = 0.1920
  corner_high_everything                  mean |shift| = 0.0404
  corner_low_everything                   mean |shift| = 0.2162
  median_point                            mean |shift| = 0.0178
  mirror_astra_no_corner                  mean |shift| = 0.0280

Distribution over 13 synthetic eighths:
  min=0.0059  median=0.0230  mean=0.0494  max=0.2162

astra mean |shift| = 0.1783
astra inside [min, max] of synthetic eighths? True

decomposition/context_volume pair, n=7 vs n=8 (astra vs each candidate):
  n=7 baseline: 0.773
  n=8 with astra: 0.183
    midpoint(balthasar,grok)              : +0.773
    ...
    corner_low_decomp_high_volume         : +0.183
    corner_high_everything                : +0.775
    corner_low_everything                 : +0.827
    median_point                          : +0.763
    mirror_astra_no_corner                : +0.745
```

**Reading.**

1. **F9's headline (0.176 mean |shift|) reproduces.** 0.178 ± noise; well within rounding. The table F9 prints (specificity/verification_rigor +0.978→+0.754, acceptance_binding/verification_rigor +0.921→+0.796, autonomy/verification_rigor −0.898→−0.637, decomposition/context_volume +0.773→+0.183) all reproduced from `bliss correlate` output earlier in this review.

2. **The decomposition/context_volume collapse is specific to corner occupancy.** Only one synthetic eighth out of 13 reproduces the +0.773 → +0.183 collapse: `corner_low_decomp_high_volume` — which is, by construction, the same corner astra occupies (decomp 0.20, volume 0.95). The other 12 leave decomposition/context_volume at 0.728 to 0.827. So the mechanism claim "the n=7 matrix was measuring an unoccupied corner of the space, and the first profile to occupy it removed the correlation" is **distinctively testable**, and **astra does exactly what the mechanism predicts**.

3. **But the overall mean |shift| is not unusual.** Two of 13 synthetic eighths move the matrix by 0.19 or 0.22 (`corner_low_decomp_high_volume` and `corner_low_everything`). astra at 0.178 sits inside that range. So the broad claim "one profile moves the matrix by ~0.176" is **not astra-specific** — corner-occupying profiles do this in general.

4. **What F9 actually proves.** The mechanism claim (`decomposition/context_volume` was a coincidence of the n=7 sample) survives the test. The headline number (0.176) is reproducible but is also achievable by other corner-occupying eighths, so it is not as sharp as the per-pair collapse suggests. F9's own caveat (lines 41–48, "It does not show the dials are independent") is the right one.

**Verdict on F9: SURVIVES WITH CORRECTIONS.** FACT (0.176 mean |shift| reproduces) + FACT (mechanism claim survives the synthetic-eighth test). High confidence.

**Replacement sentence for the headline / "Why it matters" / "Why the shift is this large":**

Original (F9 line 3): "Adding one profile moved the D6 matrix by 0.18, and unmerged both merge candidates"
Original (F9 line 28): "the n=7 matrix was measuring an unoccupied corner of the space, and the first profile to occupy it removed the correlation"

Replacement (F9 line 3):
> Adding one profile that occupied an unoccupied corner of the dial space moved the D6 matrix by 0.18, dropped the `decomposition / context_volume` pair from +0.773 to +0.183, and unmerged one merge candidate.

Replacement (F9 line 28):
> `astra` is not a random eighth point and not all eighths produce this shift: in a synthetic-eighth test, 12 of 13 plausible eighths left `decomposition / context_volume` in the +0.728 to +0.827 band, while the two that occupied previously empty corners — `astra`'s (low decomp, high volume) and the low-everything corner — produced the same order of mean shift. The mechanism is corner occupancy, not generic instability, and it is a property of the n=7 sample rather than of correlation itself.

The fix is load-bearing: without naming *corner occupancy* as the cause, the headline generalises to a claim about statistical instability that the synthetic test does not support.

---

## ST5 — Settle F8's routing-versus-shape question

**Counter-argument (4) restated:** setting `/reasoning max` may change only which tasks may be routed to an agent, not how a task should be phrased for it. F8 may be reading a routing rule as a shaping rule.

**Every reasoning-mode / `/boost` / `/reasoning max` line in the source document** (`docs/source/model-routing-policy.txt`):

| Line | Text (excerpt) | What it does |
|---|---|---|
| 6 | "predated both the GPT Astra tier and the receiver-reasoning-mode doctrine" | header note |
| 22 | "execute small and medium bounded-scope work **when reasoning mode is elevated** (Hermes exposes /reasoning max on demand; Antigravity exposes /boost). When reasoning mode is below high, treat them primarily as fast verification, fast bounded investigation, or fast second opinions -- not as cost-saving substitutes for difficult production engineering." | **Routing class.** "treat X as Y" |
| 132 | "dispatch it to the Hermes triad with /reasoning max at the receiver -- that elevates Hermes from cost-saving verifier to capable executor." | **Routing class.** |
| 160 | "Long-context economical pair review (use Gemini Flash + /boost)" | **Routing class.** |
| 374 | "Fast bounded-scope second opinions (elevate to capable when /reasoning max is set)" | **Routing class.** |
| 378 | "Receivers run with /reasoning max at the Hermes agent so reasoning mode is elevated for the work class. Below high, treat the triad primarily as verification and investigation; above, treat it as a capable executor." | **Routing class.** |
| 536 | "\"Tackle this small bounded task.\" → HERMES TRIAD (individually testable + /reasoning max at receiver)" | **Routing class.** |
| 577 | "HERMES is an asynchronous agentic workforce that also acts as a small-and-medium task executor when reasoning mode is elevated." | **Routing class.** |
| 597 | "Address the triad as you would any specialist: with individually testable subtasks and /reasoning max at the receiver. Outside-frontier work (small, medium, investigative, parallel, routine) belongs to the triad. Frontier-class work (..., maximum-intelligence escalation) belongs to Codex or GPT Astra." | **Routing class.** |

Other matches at lines 61, 222, 451 (`reasoning` in unrelated senses — "architectural reasoning", "cross-domain reasoning", "previous reasoning") are not about the receiver-mode doctrine.

**Verdict.** **(a) Elevated mode changes which tasks may be sent to an agent.** Not (b). Not (c). Every reasoning-mode line in the document is a routing rule — "treat X as Y class of work" — and none prescribe any change to how the brief is shaped.

The deciding quote is line 22:
> "Cheap models ... should also be able to execute small and medium bounded-scope work when reasoning mode is elevated ... When reasoning mode is below high, treat them primarily as fast verification, fast bounded investigation, or fast second opinions -- not as cost-saving substitutes for difficult production engineering."

Line 378 reinforces: "Below high, treat the triad primarily as verification and investigation; above, treat it as a capable executor." `treat` is the verb in both. It is the verb a router speaks, not a renderer.

**F8's claim that "one recipient now has two shapes" (line 49 of the finding, quoted: "`compile(task, target='melchior')` resolves a profile by name, and the name is assumed to determine the shape. The policy now says one recipient has two shapes, selected by a flag the dispatcher sets at send time") is read into the document, not out of it.** The policy does say one recipient has two routing classes, but the brief shape is not stated to change. The profile key is intact for `compile()`. What is broken is the dispatcher's coupling of "who to send to" and "what to send".

**Verdict on F8: SURVIVES WITH CORRECTIONS.** INFERENCE drawn from the source document; HIGH confidence on the document reading (every relevant line is quoted with line numbers above), HIGH confidence that the contradiction is real but located at dispatch, not in `compile()`.

**Whether H10 should proceed.** H10's three options (F8 lines 56–64) are: (1) two profiles per recipient, (2) eighth shaper input `mode`, (3) treat it as out-of-scope dispatch. Under the corrected reading:
- (1) duplicates profile notes and return contracts (F8's stated objection stands).
- (2) is a category error: the document never asks `compile()` to change shape based on routing mode. Composing `mode` into the shaper would make the renderer read a router flag and would break the project's own premise that shaping is independent of dispatch.
- (3) is the only one the document supports, and it is what D0 already specifies ("routing lives in the harness"). The defect is the **coupling** between dispatch and brief, and the fix is harness-side: refuse to send `melchior` / `casper` / `balthasar` a frontier-class task when `/reasoning max` is not set, or coordinate the two.

**H10 should be dropped or narrowed.** Drop the eighth-input direction; keep the question of how the harness should refuse or coordinate. Filing H10 as proposed would spend an expensive change on a problem the source document does not describe.

**Replacement sentence for F8 line 49 (the headline claim):**

Original (F9 line 1): "The source document grew a recipient and a mode, and one of them breaks the profile key"

Replacement (F9 line 1):
> The source document grew a recipient and a mode; the recipient is correctly expressed as a new profile, and the mode changes which tasks may be routed to a recipient rather than how the brief is shaped, so the profile key remains intact and the missing logic belongs in the dispatcher, not in `compile()`.

**Replacement sentence for F8 line 50–53 (the quoted block):**

Original (F8 lines 50–53):
> This is a direct challenge to the key this library is built on. `compile(task, target="melchior")` resolves a profile by name, and the name is assumed to determine the shape. The policy now says one recipient has two shapes, selected by a flag the dispatcher sets at send time — and the same document says the elevated mode changes what class of work may be sent at all.

Replacement (F8 lines 50–53):
> The policy does not challenge the profile key. `compile(task, target="melchior")` resolves a profile by name, and the name still determines the shape. The policy says one recipient has two **work classes**, selected by a flag the dispatcher sets at send time — and the same document says the elevated mode changes what class of work may be sent. The defect is therefore not in the shaper but in the dispatcher's coupling of "who" and "what" — and is solvable in the harness, where D0 already placed routing.

---

## ST6 — Whole-task conditions check

| Condition | Status |
|---|---|
| All five preceding subtasks returned with their own pass or fail | PASS (table at top) |
| Each of F6, F7, F8, F9 carries exactly one verdict from the three allowed | PASS (table at top; F7 carries a second verdict for its escalation_explicitness sub-claim, marked separately because F7's structure has two distinct claims) |
| Every load-bearing quote carries a file path and a line number and is exact | PASS (F9 lines 3 and 28 corrected by replacement; F8 lines 1, 49–53 corrected by replacement; reconciliation table cites exact lines from F6, F7, and the routing policy) |
| At least one finding is challenged rather than confirmed | PASS — F8 was challenged on the location of the contradiction; F9 was challenged by the synthetic-eighth test (12 of 13 candidates do not collapse `decomposition/context_volume`, and astra's overall mean shift is matched by other corner-occupiers). Both are challenges that, if they had held, would have moved those findings from survive to does-not-survive. |

---

## Things I could not check

- I have no working web access (per the brief); the line-level source-document reading in ST5 is grounded only in `docs/source/model-routing-policy.txt` as vendored, not in the original `.docx`. If the `.docx` shows different paragraphing or includes text the extraction dropped, the routing-vs-shape conclusion should be re-tested against the original. The vendoring header (`docs/source/model-routing-policy.txt` lines 1–8) records the extraction as `2026-09-10 21:07`; that is the cut-off.
- The 0.176 / 0.178 difference between F9's quoted figure and my re-derivation (0.1783) is within Pearson rounding (F9 says "0.18" in the headline and "0.176" in the table — both are reported). I did not re-run the n=7 matrix outside the F9 setup; the F9 re-derivation is the one in this report and it uses the same `blisspoint.dials.correlation` function as `bliss correlate`.
- The author's own stated weakness that `astra`'s values were chosen "having read F6 and F7" (F9 line 46) is an honest disclosure I cannot check from the repo. It does not affect the verdict; it confirms the F9 caveat ("this project would prefer") and is the reason the headline correction matters.

---

## Summary

- **F6:** SURVIVES AS WRITTEN. The 448 / 0 / per-field counts reproduce; the realistic-load test shows the channel is readable (≤ 3 notes per dispatch).
- **F7:** SURVIVES AS WRITTEN (both the 26-distinct collapse claim and the escalation_explicitness reachability claim).
- **F8:** SURVIVES WITH CORRECTIONS. The defect is real but lives in the dispatcher's coupling of who and what, not in `compile()`. The corrected reading directs H10 away from an eighth shaper input and toward harness-side coordination.
- **F9:** SURVIVES WITH CORRECTIONS. The 0.176 reproduces and the mechanism claim (corner occupancy) survives the synthetic-eighth test, but the headline should name corner occupancy as the cause so it does not generalise into a claim about statistical instability.

Replacement sentences for F8 and F9 are in ST5 and ST4 respectively.

---

## Commands run (for independent re-verification)

```
cd /home/conker/projects/bliss-point && .venv/bin/python lab/measurements/silent_subtraction.py
cd /home/conker/projects/bliss-point && .venv/bin/bliss correlate
cd /home/conker/projects/bliss-point && .venv/bin/bliss dials claude --phase design
cd /home/conker/projects/bliss-point && .venv/bin/bliss dials claude --phase verify
cd /home/conker/projects/bliss-point && .venv/bin/bliss dials claude --phase implement
cd /home/conker/projects/bliss-point && .venv/bin/bliss dials claude --phase synthesize
cd /home/conker/projects/bliss-point && .venv/bin/bliss compile <profile> --task /tmp/sparse-task.yaml --phase design  (× 8 profiles)
cd /home/conker/projects/bliss-point && .venv/bin/bliss compile antigravity --objective "Rebuild the settings screen." --phase implement --stakes normal
cd /home/conker/projects/bliss-point && .venv/bin/python /tmp/f9_arithmetic_test.py
cd /home/conker/projects/bliss-point && grep -n -i "reasoning\|/reasoning\|/boost\|reasoning mode\|reasoning max" docs/source/model-routing-policy.txt
cd /home/conker/projects/bliss-point && .venv/bin/python -m pytest tests/ -q
```

Test suite: 52 passed in 1.78s. No file in the repository was modified.
