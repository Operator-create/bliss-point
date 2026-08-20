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

**The claim dies if** a brief compiled for the *wrong* recipient performs as well as one compiled
for the right one. That is not a hypothetical framing — it is arm M, and it is the reason to run
this at all.

## 2. Four arms, information-matched

Every arm below is built from the **same `Task` object**. The fields are identical; only the
rendering differs.

| arm | what it is | what it isolates |
|---|---|---|
| **R — Raw** | The request as a person actually types it. One or two lines. | The floor. What we do today. |
| **F — Flat** | Every `Task` field, rendered into one fixed generic template. No per-recipient variation. | **The real control.** Same information, no shaping. |
| **C — Compiled** | `bliss compile(task, target=<the model actually running>)`. | The product. |
| **M — Mis-shaped** | Compiled against a deliberately wrong profile — a goal-shaped researcher brief sent to an executor, and vice versa. | **The falsifier.** If C ≈ M, the dials are decoration and only field-gathering mattered. |

Primary comparison: **C vs F**. Falsifier: **C vs M**. Floor: **R**.

Arm F requires a `flat` renderer that emits every section unconditionally — roughly thirty lines,
and it must be written *before* the tasks are chosen, so it cannot be tuned to lose.

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

pi is the harness for both tiers; it is multi-provider, so the harness is held constant while the
model varies. That is exactly why the eval runs on pi rather than on our own dispatcher.

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
| C vs M | pass@1 | C − M ≥ +15pp, **required**, or the dials are decoration |
| C vs M | scope_violations | M > C, in the predicted direction per tier |
| Tier A vs Tier B | (C − F) | different in *sign or magnitude*, or the thesis is false |

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

- **C ≈ M** — shape does not matter, only field-gathering does. Keep the linter, delete the dials,
  and D7's positioning is already correct.
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
