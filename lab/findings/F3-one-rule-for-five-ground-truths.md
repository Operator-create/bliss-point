# F3 — The corpus came back 27 bug fixes and nothing else, and the brief was why

**2026-08-20.** Method note on briefing, which is awkward, because this project is a library
about briefing.

## What happened

Sourcing for the 20-task corpus went to `balthasar` as deep research. The brief carried five
numbered criteria, and criterion 8 read: *the fixing PR added or modified a test file. This is
essential: the added test becomes our hidden acceptance test.*

It came back with 31 verified candidates: **27 bug fixes, 3 features, 1 investigation, 0
refactors, 0 under-specified.** The quota needs 6 / 5 / 3 / 4 / 2.

The researcher did not fail. The brief made three of the five categories unsatisfiable:

| category | its actual ground truth | why criterion 8 is impossible |
|---|---|---|
| refactor | the **existing** suite stays green | a refactor that adds a test changed behaviour — the opposite of the task |
| investigation | a rubric, blind-judged | the issue closes with an explanation and **no code change**, so there is no PR |
| under-specified | inverted: stopping to ask is the pass | too vague to have produced a fix at all |

The protocol had this right in section 4 from the start. The brief flattened it into one rule that
happened to fit the category I had most clearly in mind.

## The same error was in the gate

`corpus_check.py` required `hidden_tests` from every category outside the judged set — refactor
included. So a correctly sourced refactor task would have been **rejected by my own gate** for
lacking an artifact the protocol never asked it for. Two independent expressions of one mistaken
belief, written the same afternoon, neither checking the other.

Fixed: the gate now refuses a refactor that *carries* a hidden test, requires
`pre_existing_suite_must_pass` in its place, and stops demanding a fixing PR from categories where
no upstream fix exists. Four tests cover it. 21 gate tests green.

## Why this belongs in the lab and not just in a commit

Bliss Point's entire thesis is that **a brief must be shaped to what is receiving it**. This was a
failure of a different kind, and a more embarrassing one: the brief was shaped to the *sender's*
mental model of the work rather than to the structure of the work itself. One rule, five kinds of
thing, and the rule was silently a specification of only one kind.

The dials do not catch this. There is no dial for *"the task decomposition you are handing over is
wrong"*. `decomposition` controls whether subtasks are rendered, not whether the subtasks are
coherent. What would have caught it is the gap linter's own principle applied one level up: the
brief asserted a uniform acceptance rule across a heterogeneous set, and nothing checked that the
assertion held for each member.

Two things follow, and the first is cheap enough to do now:

1. **A brief that ranges over categories should state the acceptance rule per category, or state
   explicitly that one rule covers all of them.** That is a linter rule, not a dial — which is more
   evidence for D7's positioning that the linter is the product.
2. The researcher's output was **the right answer to the question asked**. Judging the lane on
   category coverage would have been judging it for my defect. Round 1's 31 candidates all verified
   clean against the API; the shortfall was upstream of the work entirely.

Related: [[F1-agent-reports-need-grepping]], [[F2-the-gate-found-a-hole-in-the-gate]]
