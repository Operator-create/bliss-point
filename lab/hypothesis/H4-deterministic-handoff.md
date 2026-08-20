# H4 — A deterministic handoff template matches a model-written one

**Status: OPEN.** No experiment designed yet. Filed 2026-08-20.

## The claim

The handoff between agents can be produced **mechanically**, from state the harness already holds,
with no model call — and lose nothing that changes what the *receiving* agent does.

## Why this belongs in Bliss Point rather than beside it

Bliss Point already compiles the **outbound** direction: a Task becomes a brief shaped for its
recipient. A handoff is the **return** direction, and the machinery for it is already half-built —
every profile carries a `return_contract` declaring what that agent must send back:

```yaml
# profiles/melchior.yaml
return_contract:
  - commands run and their output
  - what was reproduced
  - the fix, or why it was not applied
  - residual risk
```

A deterministic handoff renderer is the **inverse of the existing compiler**, reading the same
profile data. That makes this a natural extension of the thesis, not a new subsystem: if shape is a
deterministic function of the recipient outbound, it should be a deterministic function of the
*next* recipient inbound.

## Four questions, which are not the same question

1. **Is a deterministic template good enough?** (quality)
2. **Can the harness fill it automatically without significant RAM?** (feasibility)
3. **Is the agent writing the file more efficient than the harness generating it?** (cost)
4. **Is a templated handoff faster than an untemplated one at similar quality?** (latency)

## The tradeoff this actually tests

A template can only **select** state that is already structured. It cannot **compress prose** or
**judge relevance**. A model can turn forty messages into five lines and decide which two mattered;
a `str.format` call cannot.

So the honest prediction is a **split**, and predicting where the split falls is the interesting
part:

- **Structured state should template cleanly** — files changed, commands run, tests passed,
  acceptance status per subtask, blockers, next action. The harness already knows all of it.
- **Unstructured reasoning should not** — *why* an approach was abandoned, which of three
  contradictory findings to believe, what the agent suspects but cannot prove.

If that split is real, the answer is neither template nor model: it is a template with a small
number of model-written fields, and the finding is *which* fields those are.

## Arms

Same discipline as the eval protocol: the arms must differ in one thing.

| arm | handoff produced by | inference cost |
|---|---|---|
| **N — none** | whatever the agent writes unprompted | 0 extra calls, unbounded variance |
| **T — template** | the harness, from structured state, zero model calls | **0 tokens** |
| **W — written** | the agent, prompted with its `return_contract` | 1 extra call |
| **H — hybrid** | template, with named fields written by the agent | 1 short call |

## Metrics

**The primary metric is the receiver's outcome, not the handoff's beauty.** A handoff is only good
if the next agent does better work with it. Judging handoffs directly measures taste.

- **Receiver task success** — the downstream agent's hidden-test pass rate.
- **Total cost** — tokens for the handoff *plus* the receiver's run. Arm T's handoff is free; if the
  receiver then burns tokens re-deriving what was dropped, T is not cheaper.
- **Latency** — wall clock and, for T, whether it is genuinely sub-second.
- **Information survival** — against the fixed list the routing policy already specifies for
  synthesis: objective, evidence, disagreements, decisions, failures, constraints, unresolved
  questions, relevant files, next action. Scored as present/absent per item, which is countable
  rather than judged.
- **Harness RSS** — see below.

## The RAM question is really about local models

On an API model, generating a handoff costs no local RAM at all — the question is meaningless. It
becomes real only when the summariser runs **locally**, which is exactly the constraint that has
been crashing herdr on a 7.4 GiB laptop. So the honest form of question 2 is:

> Does the handoff step force a local model into memory that would otherwise not be resident?

Arm T answers no by construction — string formatting has no model. Arms W and H answer no *if* the
writing agent is one already running, and yes if a separate summariser has to be loaded. That makes
arm T's real advantage **not** token cost but the fact that it cannot OOM anything.

Testable now that `operatorserver` exists (30 GiB, Docker): run the same handoff chain under a
constrained cgroup at 7 GiB and at 24 GiB, and see which arms survive the small one.

## Killed by

- **T's receiver does measurably worse than W's.** Determinism loses information that matters, and
  handoffs need a model.
- **T's handoff needs a model call to be usable anyway** — if the receiver's first act is to ask for
  clarification, the template did not remove a call, it moved one.
- **N ≈ W ≈ T.** Handoff format does not matter at all, and this is a non-problem. Worth knowing
  cheaply before building anything.

## Prior evidence, such as it is

[findings/F1](../findings/F1-agent-reports-need-grepping.md) records a real handoff failure: a reply
arrived at the right path, in the right format, with citations — and answered a different project's
question, because the destination was named per-agent rather than per-task. That is an argument that
handoff **routing** should be mechanical. It says nothing yet about whether handoff **content**
should be.
