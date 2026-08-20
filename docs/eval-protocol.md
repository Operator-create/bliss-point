# Eval protocol — the 20-task A/B

**Status: pre-registered, not yet run.** This document is written *before* any data exists, and
the thresholds in it are binding. If the results are edited to fit a hypothesis after the fact, the
project is worth nothing, because the entire complaint against it is that the dials are unmeasured
taste.

## 1. The claim, stated so it can lose

> Shaping a brief to its recipient changes agent outcomes, beyond the effect of supplying the same
> information in a fixed format.

The second clause is the whole experiment. A compiled brief carries acceptance criteria,
constraints and a return contract; a one-line request does not. Comparing those two measures *"more
context helps"*, which is already known and is not the claim. Everything below exists to strip that
confound out.

**The claim dies if** the shape preference does not differ across recipients — if a small execution
model and a frontier reasoning model want the same brief. That is the interaction in §3, and it is
the primary falsifier.

A second, sharper falsifier attacks the mechanism rather than the matching: if flipping *one* dial
across the threshold where it actually changes the rendered document has no effect on how the agent
behaves, that dial is decoration. That is arm A in §2.

*(An earlier draft made "a brief compiled for the wrong profile does as well as the right one" the
fulcrum. It was struck — see Amendment 1.)*

## 2. Four arms, information-matched

Every arm below is built from the **same `Task` object**. The fields are identical; only the
rendering differs.

| arm | what it is | what it isolates |
|---|---|---|
| **R — Raw** | The request as a person actually types it. One or two lines. | The floor. What we do today. |
| **F — Flat** | Every `Task` field, one fixed generic template, no recipient named. `bliss flat` / `blisspoint.flat()`. | **The real control.** All the information, none of the shaping. |
| **C — Compiled** | `bliss compile(task, target=<the model actually running>)`. | The product. |
| **A — Ablated** | C with exactly **one** dial moved across the threshold where it changes the rendered document. Everything else identical. | **The mechanism falsifier.** If the flip changes nothing, that named dial is decoration. |

Primary comparison: **C vs F** (shaping vs information). Mechanism falsifier: **C vs A**. Matching
falsifier: the tier interaction in §3. Floor: **R**.

The ablated dial is the one that cell's prediction names, not a tour of all seven:

| cell | dial flipped | threshold | what changes in the brief |
|---|---|---|---|
| small models | `decomposition` | 0.6 | subtask list vs one Task section |
| frontier models | `autonomy` | 0.6 | "Decisions you own" vs prescribed |

Arm A is registered on **`scope_violations` and `steps`**, not on pass@1 — continuous metrics are
the ones with power at n=20 (§7). The resolved seven-vector for every run is logged, so the
ablation is auditable rather than described.

Arm F's renderer was **built before the task corpus**, deliberately, so it could not be tuned to
lose. Three properties make it a control rather than a strawman, and each is enforced by a test
rather than by intention:

1. **It cannot vary by recipient** — `flat(task)` takes no profile, phase or stakes argument. A test
   asserts the signature, so recipient-awareness cannot be added by accident.
2. **It drops nothing.** A test asserts that every populated `Task` field appears in the output, and
   a second asserts that **arm F's content is a superset of every compiled brief's**, across all
   profiles and all phases. The control can never hold *less* than the arm it controls for.
3. **It is not sabotaged.** No filler, no unstructured dump — it is what a careful person produces
   without this library: gather every field, label it, send it.

Property 2 is what the comparison rests on, and it cuts against us on purpose: arm C usually carries
*less text* than arm F, because shaping is partly selection. A paired test confirms the compiler
really does drop fields, so the contrast is not vacuous. **If C beats F while saying less, shaping
did the work. If it does not, field-gathering was the product** (§9).

## 3. The interaction is the real hypothesis

Bliss Point does not claim "structured briefs are better". It claims **different recipients need
different shapes**. That is an interaction effect, and it needs at least two model tiers to exist
at all:

- **Tier A — small/fast execution model.** Predicted: C ≫ F, driven by high `specificity`,
  `decomposition`, `acceptance_binding`. Predicted: M (goal-shaped) hurts *badly* — scope drift,
  invented requirements.
- **Tier B — frontier reasoning model.** Predicted: C > F by a smaller margin, driven by high
  `autonomy` and low `specificity`. Predicted: M (checklist-shaped) hurts by suppressing the
  model's own judgement — it follows a wrong checklist instead of noticing it is wrong.

**If both tiers want the same shape, the project's thesis is false** even if C beats F everywhere.
That outcome must be reported as prominently as a win. It would mean Bliss Point is a good linter
with a decorative IR — which is still a product, but a different one, and D7's positioning already
survives it.

pi is the harness for every cell; it is multi-provider, so the harness is held constant while the
model varies. That is exactly why the eval runs on pi rather than on our own dispatcher.

### 3.1 Tier and family are different variables, and the first draft confused them

Calling the two conditions "Tier A" and "Tier B" quietly assumed capability was the only thing
changing. If the small model and the large model come from different vendors, then any interaction
found could be a **vendor idiosyncrasy** — one company's post-training preferring checklists —
wearing the costume of a capability law. The whole thesis would rest on a confound.

The minimum design that separates them is a **2 x 2: {small, large} x {family 1, family 2}**, four
cells, same four arms in each.

| | family 1 | family 2 |
|---|---|---|
| **small** | cell A | cell B |
| **large** | cell C | cell D |

- If the shape preference tracks the **row**, it is a capability effect and the thesis holds.
- If it tracks the **column**, it is a vendor effect and Bliss Point's profiles are really
  vendor-specific lore, which is still useful but is a much smaller claim honestly stated.
- If it tracks **neither**, there is no interaction and §9 applies.

A third family in at least the small row is worth the cost if the budget survives it, because two
columns cannot distinguish "vendor effect" from "these two vendors happen to differ".

## 4. Tasks

**20 tasks**, fixed before the first run, in a dedicated repo:

| category | n | ground truth |
|---|---|---|
| Bug fix with a failing test | 6 | hidden test file, not shown to the agent |
| Small feature with a spec | 5 | hidden test file |
| Refactor preserving behaviour | 3 | existing suite must stay green + a scope check |
| Investigation / audit (no code change) | 4 | rubric, blind-judged |
| Deliberately under-specified | 2 | **correct behaviour is to stop and ask**; see §6.5 |

Rules that make a task admissible:

1. **Hidden acceptance.** The checking test is never in the brief. An agent that reads the test
   and satisfies it literally has not done the task.
2. **Declared scope.** Every task names the paths it may touch, so scope drift is measurable as a
   diff, not as a judgement call.
3. **Solvable by the weaker tier.** If Tier A cannot do a task under any arm, that task measures
   difficulty, not shape. Pilot each task once on Tier A under arm C; drop tasks that fail flat.
4. **No task authored while looking at the dials.** Tasks come from real bug reports and real
   feature requests, otherwise they encode the hypothesis.
5. **Union-complete, and gap-free in every arm.** The `Task` carries the union of every field any
   arm in that cell would demand, filled once and frozen. A task enters the corpus only if **every
   arm compiles with `blocking_gaps == []`**. Otherwise an arm loses for being incomplete rather
   than for being shaped differently, which is exactly the confound arm F exists to remove.
   Advisory gaps are recorded as a covariate.

## 5. Metrics

### 5.1 Outcome — the thing that matters

- **`pass`** — hidden tests green, binary, per run.
- **`pass@1`** across trials.
- Refactor tasks additionally require the pre-existing suite green.

### 5.2 Cost

- **`input_tokens`**, **`output_tokens`**, reported *separately*. Input dominates in agentic loops
  and is the cache-sensitive one; a single total hides the effect.
- **`cached_input_tokens`** where the provider reports it. A compiled brief has a stable prefix by
  construction (see [token economy](token-economy.md)), so this is where that design decision
  either pays off or does not.
- **`cost_usd`**, computed from the provider's published price *at run time* and recorded in the
  result file. Prices move; a hardcoded number would silently rot.

### 5.3 Speed

- **`steps`** — agent turns to completion. **This is the primary speed metric.** It is
  provider-load independent and reproducible.
- **`wall_clock_s`** — reported, but secondary and never used for a claim on its own. It is
  contaminated by provider load, so runs are randomised across time of day and the arm order is
  counterbalanced within each task.

### 5.4 Quality, beyond pass/fail

- **`scope_violations`** — files or hunks touched outside the task's declared paths. Objective,
  computed from the diff. This is where a mis-shaped brief is expected to show up first.
- **`self_corrections`** — reverted edits and retried tool calls within a run.
- **`unrequested_additions`** — new files, new dependencies, new abstractions nobody asked for.
- **`judge_score`** — for the investigation tasks only, a 1–5 rubric on evidence quality, fact vs
  inference separation, and whether absent evidence was reported as absent.

### 5.5 Judging

The judge sees the task and the final artifact. It **never sees which arm produced it**, and the
files are shuffled and renamed before judging. Per the repo's own rule, the judge is selected with
`cross_family()` — it must not share a model family with the agent that produced the work.

### 5.6 Linter validity — free, and it tests D4

Every compiled brief records its gaps. Cross-tabulate **blocking gaps present** against **task
failed**. If briefs with blocking gaps fail no more often than briefs without, the gate in D4 is
superstition and should be removed. This costs nothing extra and is the only metric here that can
falsify a decision already shipped.

## 5.7 Objectivity and family bias

Models are not neutral referees of other models. A judge tends to score work from its own family
higher — same post-training, same idioms, same notion of a good answer — so a single-family
evaluation can manufacture a result out of nothing but taste. Everything here exists to keep that
from happening, and to *measure* it where it cannot be removed.

**1. Objective metrics outrank judged ones, and cover most of the eval.** Hidden tests, scope diff,
token counts and step counts are computed mechanically and no model has an opinion about them. They
decide 16 of the 20 tasks outright. The rubric judgement applies only to the 4 investigation tasks.
The strongest defence against judge bias is to shrink the surface where judgement matters at all.

**2. Judging is a cross-family panel, never one judge.** At least two judges, from two different
families, neither sharing a family with the agent that produced the work — selected with the
library's own `cross_family()`. Disagreement is reported, not averaged away: inter-rater agreement
(Krippendorff's alpha) is published with the results. **Alpha below 0.6 means the rubric is broken
and the judged tasks are reported as inconclusive**, not quietly resolved by picking a judge.

**3. Self-preference is measured, not assumed.** Each judge family also scores a blind sample of
work produced by its *own* family. The difference between the score it gives its own family and the
score it gives others is the self-preference bias, in rubric points, for that judge. It is published
as a number. If the measured bias exceeds the effect we are claiming, **the judged portion of the
result is void** — the instrument is less precise than the thing it is measuring.

**4. Blinding is on the artifact, and its limits are stated.** Judges see the task and the final
artifact only: no arm label, no model name, files shuffled and renamed. This does not fully work.
Models have stylistic fingerprints, and a judge may recognise its own family's prose without being
told. That residual leak is a stated limitation, which is why control 1 matters more than this one.

**5. The analysis is replicated across families.** The analysis script is written before the data
exists. Once results are in, an agent from a different family than the script's author re-runs the
numbers from the raw run files and must reproduce them. A disagreement is a finding about the
analysis, and blocks publication until resolved.

**6. Comfortable results get the adversarial pass.** Before publishing any result favourable to
Bliss Point, one agent from a family with no stake in the design is briefed to argue that the result
is an artefact, given the raw data. Its objection is published alongside the result whether or not
we agree with it. Results *unfavourable* to Bliss Point do not need this step — the asymmetry is
deliberate, because only one direction is motivated.

**7. No stopping on a good number.** The run count is fixed in advance (§8). Stopping early because
the effect looks strong is how a null result becomes a paper.

## 6. Controls

1. **Same harness build, pinned.** Record the pi commit; a harness upgrade mid-run invalidates it.
2. **Temperature fixed and recorded.** Seeded where the provider supports it.
3. **3 trials** per (task, arm, model). Agentic runs are high-variance; one trial is an anecdote.
4. **Randomised order, counterbalanced arms** within each task.
5. **Fresh session per run.** No conversational carryover — that is the confound the routing policy
   already warns about.
6. **Blind judging** (§5.5).
7. **The under-specified tasks (§4) are scored inverted:** an agent that confidently produces code
   has failed; one that stops and asks has passed. Without these, every metric rewards
   overconfidence, and a brief that encourages an agent to charge ahead would look like a win.

## 7. Pre-registered thresholds

Declared now, so they cannot be moved later.

| comparison | metric | counts as a result |
|---|---|---|
| C vs F | pass@1 | ≥ +20 percentage points, paired |
| C vs F | input tokens at equal pass rate | ≥ −20% |
| C vs F | steps at equal pass rate | ≥ −15% |
| C vs A | scope_violations | paired bootstrap median difference, 95% CI excluding 0 |
| C vs A | steps | paired bootstrap median difference, 95% CI excluding 0 |
| C vs A | pass@1 | directional only, never a headline |
| Tier A vs Tier B | (C − F) | different in *sign or magnitude*, or the thesis is false |

**The defect that produced Amendment 1.** The first draft required "C − M ≥ +15pp" while also
stating that 20 paired tasks resolve only 25–30 points. The falsifier could not fire at the planned
sample size. The audit's ranking was that this was the *second* problem, not the first — powering a
straw man just produces a well-powered straw man — so the row was not repaired, it was removed
along with the arm.

**Statistics.** Paired per task. Binary outcomes: McNemar on discordant pairs, plus a paired
bootstrap CI. Continuous outcomes (tokens, steps): paired bootstrap, reported as median difference
with a 95% interval. No p-value is reported without the effect size next to it.

**Honest power.** With 20 paired tasks, a binary outcome can only detect a *large* difference —
roughly 25–30 percentage points at 80% power. It cannot resolve a 10-point effect, and this
protocol will not claim one. The continuous metrics (tokens, steps) are far better powered at the
same n, detecting roughly a 0.65 standard-deviation paired effect. **Expect the cost and step
metrics to carry the finding and the pass-rate metric to be directional only.** If a pass-rate
result lands between 10 and 25 points, the correct write-up is "underpowered, inconclusive,
n needs to be 60+", not a headline.

## 8. Budget

20 tasks × 4 arms × 2 tiers × 3 trials = **480 runs**. At a conservative 60k total tokens per
agentic run, that is roughly **29M tokens**.

Run Tier A first, in full. It is the cheap tier and it carries the strongest predicted effect, so
if C does not beat F there, stop and reconsider before spending on Tier B. Price the run from the
provider's current published rates at execution time and record the figures in the results file.

## 9. What would make us abandon the dials

Written down now, while it is still cheap to be honest:

- **C ≈ A** — flipping the dial this cell claims is causal changes nothing measurable. That dial is
  decoration and gets deleted by name, which is a sharper outcome than a vague "the dials are
  wrong".
- **Both tiers prefer the same shape** — the interaction does not exist; there is one good brief
  format, not a per-recipient one.
- **F ≈ C and both ≫ R** — a fixed rich template is enough; Bliss Point becomes one template and a
  linter, which is a smaller and more honest project.

Any of these gets published in the repo with the same prominence as a win. A negative result that
is reported is worth more to a stranger reading this repo than a positive one that is not
reproducible.

## 10. Build order

1. The `flat` renderer for arm F — before task selection, so it cannot be tuned.
2. The task corpus and its hidden tests, in a separate repo.
3. The runner: fresh pi session per run, captures tokens, steps, wall clock, diff, transcript.
4. The scorers: hidden tests, scope diff, blind judge.
5. Pilot on 3 tasks × 4 arms × Tier A. Fix the instrumentation, **not the hypothesis**.
6. Full Tier A. Decide whether Tier B is worth it.


---

## 11. Amendment log

Amendments are numbered, dated and public. Nothing in this document is edited silently; a
pre-registration that quietly repairs itself is not a pre-registration.

### Amendment 1 — 2026-08-20 — arm M struck, arm A added

**What changed.** The mis-shaped arm (compile against a deliberately wrong profile) is removed from
the design. The fourth slot becomes a one-dial ablation. The claim no longer dies on C ≈ M; the
matching falsifier is the tier interaction in §3, and the mechanism falsifier is arm A.

**Why.** An [independent audit](research/2026-08-20-arm-m-audit.md) ranked three known threats and
found the first fatal: as specified, arm M was a straw man the product could not lose to. The
shipped profiles make the cross-role jump extreme — `claude` and `antigravity` at `implement`
differ by an L1 of 2.30 across the four load-bearing dials, which drops the renderer into a single
"Design an approach for: {objective}" section against a profile whose own notes say it needs a task
list and never an abstract problem. Beating that demonstrates "do not send an architecture brief to
a frontend engineer", which routing already knew. The dials would not have been under test.

The audit also corrected a belief of ours: a gap-free mis-shaped brief is **not** a contradiction in
terms. Gaps are empty *fields* a dial demanded, so a union-complete Task compiles gap-free against
any profile. What cannot be done is make a cross-role brief simultaneously gap-free and
information-matched *in the rendered text*, because researcher dials omit the subtask list even when
it sits on the Task — so M would carry less of the Task than C and lose as a poorer information
subset, which is precisely the confound arm F exists to eliminate. An identification failure, not an
impossibility.

**What we kept from the old arm.** If a wrong-shape illustration is ever wanted, the audit specified
a defensible one — *same-role adjacent donor*, swapping only the load-bearing dials while holding
`return_contract`, phase and stakes. The informative pair already exists in the repo: `codex`
(`decomposition` 0.35) against `antigravity` (0.90) at `implement`, which crosses the 0.6 render
threshold and is what a competent person who believed "always send a task list" would actually do.
That is a pilot figure, not 120 eval runs.

**Cost.** None. The 120 runs arm M would have consumed are spent on arm A, which can kill a dial by
name.