# Harness bake-off — does the harness change the agent, or does the model?

**Status: pre-registered, not yet run.** Written before Phase 0, and the thresholds bind. This is
the second experiment in this lab and it inherits the first one's rules: objective metrics outrank
judged ones, cross-family judging, no stopping on a good number, and negative results published as
prominently as positive ones.

## 1. The claims

Stated as the operator stated them, then stated so they can lose:

| | claim | measured on |
|---|---|---|
| **H5** | Melchior is *faster and a better coder* on **DeepSeek Harness** than on Hermes | hidden-test pass, steps, wall clock |
| **H6** | Balthasar is a *better researcher* on **Playwright CLI** than on Hermes | rubric, citation verifiability, tokens |
| **H7** | Casper *uses fewer tokens and is sharper* on **Prime agent** than on Hermes | input/output tokens, task success |
| **H8** | Melchior is better on **pi** | as H5 |
| **H9** | Balthasar is better on **DeepSeek Harness** | as H6 |

Each is a claim about a **harness**. That is what makes the design hard, and it is the entire
reason for section 2.

### 1.1 H8 and H9 turn three A/Bs into a grid, and that is the point

H5–H7 alone are three unrelated two-cell comparisons. Adding H8 and H9 means two roles are each
measured across three harnesses, and one harness (dsh) is measured across two roles — which buys an
**interaction** that isolated pairs cannot see:

| | Hermes | dsh | pi | Playwright | Prime |
|---|---|---|---|---|---|
| **Melchior** — coder | baseline | H5 | H8 | — | — |
| **Balthasar** — researcher | baseline | H9 | — | H6 | — |
| **Casper** — orchestrator | baseline | — | — | — | H7 |

- If dsh beats Hermes for **both** Melchior and Balthasar, it is a **general harness effect** — dsh
  is simply better plumbing, and the finding is "adopt dsh", role-independent.
- If dsh beats Hermes for Melchior but **not** Balthasar, it is a **role × harness interaction**:
  harnesses have shapes, and the right harness depends on what the agent is for.

That second outcome is this project's own thesis one level up. Bliss Point claims a *brief* must be
shaped to its recipient; a role × harness interaction would say the *runtime* must be too. It would
also be the first evidence for that thesis measured on something other than our own briefs, which
is worth more than another self-report.

The grid is what makes that separable. Neither outcome is assumed here, and the null — every
harness within noise of every other — remains the most likely single result at this sample size.

## 2. The control that decides whether any of this means anything

> **The model is held constant. Every harness runs MiniMax through the same MiniMax OAuth —
> the subscription login, not an API key.**

Without it there is no experiment. Hermes runs MiniMax-M3; if DeepSeek Harness were run on a
DeepSeek model, "Melchior codes better on dsh" would measure *DeepSeek's model* and attribute it to
dsh's harness. Every one of the three claims has this failure mode, and it is the same confound
that killed arm M in the [eval protocol](eval-protocol.md#11-amendment-log): comparing a thing to a
differently-shaped thing and reporting the difference as if one variable moved.

The operator's instruction to wire every harness to MiniMax OAuth *is* this control. It is recorded
here as load-bearing rather than as a setup convenience.

### 2.1 OAuth specifically, not an API key

The auth path is part of the control, not a setup detail, for three reasons:

1. **H7 is a cost claim.** It says Casper *uses fewer tokens* on Prime. If one harness authenticated
   by subscription and another by metered API, the two cells would be billed, throttled and
   possibly served differently, and the token and cost columns would not be comparable. The claim
   would be untestable on its own primary metric.
2. **A subscription and an API key are not guaranteed to be the same serving path.** Rate limits,
   context handling and routing can differ. Holding the auth path constant removes a variable that
   would otherwise sit silently underneath every cell.
3. **Cost.** Metered API billing across 66 runs is real money for an experiment that is
   underpowered by design.

**Mixed auth paths are forbidden.** If it turns out that no harness but Hermes can do MiniMax
OAuth, the correct move is *not* to run some cells on OAuth and others on a key. Either the grid
shrinks to the harnesses that can, or the **whole grid** — Hermes baselines included — moves to one
identical API path together. That second option is a decision for the operator, because it costs
money; it is not a call to make silently mid-run.

**If a harness cannot be pointed at MiniMax by OAuth, its cell is reported as "not tested"** — never
run anyway and quietly caveated in a footnote. This is the most likely way for cells to die: most
agent harnesses support an OpenAI-compatible endpoint plus a key, and third-party *OAuth* support is
comparatively rare. Phase 0 exists to find out before anything is installed.

### 2.1 The second confound: the agent is not the harness

"Melchior" is a Hermes *profile* — a system prompt, a skill set, a tool allowlist. On DeepSeek
Harness there is no Melchior. So H5 does not really say "Melchior on dsh"; it says "the Melchior
role, **reconstructed** on dsh". Reconstruction fidelity is a free variable, and a sloppy port
loses for being a sloppy port.

Controls:

1. The **system prompt is transferred byte-identical**. Any edit forced by the target harness is
   recorded in the run manifest as a diff, and a cell needing more than trivial edits is flagged.
2. The **tool allowlist is matched by capability**, not by name: same ability to read, write, run
   shell, search. Extra tools the target harness offers are *disabled*.
3. **No profile identity is copied to the server.** Fresh throwaway profiles built from the prompt
   text, per the standing routing policy — opserver is a worker, not a home for any agent.

### 2.2 The skills axis

The operator's design, and it is the right one: every cell runs **twice** — once with **no skills**,
once with the **same skills**. That separates "this harness is better" from "this harness's skill
system is better", which are different products.

Skills selected for the second condition must be **pure-prompt** — no harness-specific tool calls —
or they cannot port, and the comparison silently becomes a test of skill portability.

## 3. Design

**8 cells** (5 contested + 3 Hermes baselines), each run under **2 skill conditions** × **3
tasks**. Trials: 2 on the coding cells, where agentic variance is worst; 1 elsewhere. That is 66
runs — 36 Melchior, 18 Balthasar, 12 Casper.

Every role's Hermes cell is its **shared baseline**: Melchior's Hermes runs serve H5 and H8 both,
so adding the third harness costs one new cell, not two.

**Honest power, stated up front.** This is a pilot at n=3 tasks. It is *underpowered by
construction* and cannot confirm a claim. It can do three useful things, and only these:

- **kill a claim** that shows no effect or an effect pointing the wrong way,
- **surface a capability difference** that is qualitative and does not need statistics
  (a harness that cannot run the task at all),
- **cost the real experiment** if a claim survives.

Any surviving claim goes to a powered run. Nothing here gets written up as "X is better than Y".

## 4. Tasks, reused rather than invented

The coding cell runs on **verified candidates from the corpus** — real closed issues, hidden tests
lifted from the real fixing PR, declared scope, admissibility checked by
`corpus_check.py`. That machinery already exists and was built for exactly this discipline, so the
bake-off inherits ground truth instead of authoring it.

| role | tasks | ground truth |
|---|---|---|
| Melchior — coding (H5, H8) | 3 bugfix candidates | hidden test, plus scope diff |
| Balthasar — research (H6, H9) | 3 investigation-shaped questions with checkable citations | every claim must resolve to a real URL or file:line; fabrications counted |
| Casper — orchestration (H7) | 3 fixed multi-step briefs | task completed, tokens counted |

The **same three tasks** are used across every harness for a given role. A harness that got easier
tasks would win for that reason alone.

H6's primary metric is **verifiable-citation rate**, not eloquence. This lab has already paid twice
for confident prose with a fabricated number in it (F1), and a research harness that browses is
exactly the kind of thing that could improve *or worsen* that rate.

## 5. Metrics

Same instrument as the main eval, so results are comparable:

- **steps** — primary speed metric, provider-load independent
- **input_tokens / output_tokens**, separately; `cost_usd` priced at run time
- **wall_clock_s** — secondary, never a claim on its own
- **pass** — hidden tests, binary (coding cell)
- **verifiable_citation_rate** — resolved claims / total claims (research cell)
- **scope_violations** — diff outside declared paths
- **judge_score** — 1–5 rubric, blind, cross-family

## 6. Judging

Blind: judges see the task and the artifact, never the harness label, files shuffled and renamed.
Judge selection uses the library's own `cross_family()`. Every agent under test runs MiniMax, so
**codex (GPT-5.6) is cross-family by construction** and is the designated quality reviewer — and it
reviews *paired with the orchestrator*, per the operator's instruction, with disagreements recorded
rather than averaged.

## 7. Thresholds, declared now

| claim | metric | counts as directional support | counts as killed |
|---|---|---|---|
| H5 | steps to green | dsh ≥ 25% fewer at equal pass | dsh worse or within ±10% |
| H5 | pass on hidden tests | dsh ≥ +2 of 6 runs | dsh ≤ Hermes |
| H6 | verifiable_citation_rate | Playwright ≥ +20 points | equal or worse |
| H7 | total tokens at equal success | Prime ≥ 25% fewer | within ±10% or worse |

A claim that lands inside the dead band is reported as **"no detectable difference at this sample
size"** — not as a win for the incumbent.

## 8. What this is for

Bliss Point's question is not "which harness is best". It is **whether any of these harnesses has a
seam worth adopting**. C1 already confirmed dsh's plugin seam can host a prompt compiler without
patching core. The bake-off's real deliverable is a **seam report**: for each harness, what it does
structurally that Hermes does not, and whether that structure is portable into this project.

A claim can be killed and its harness still contribute the most valuable finding.

## 9. Phases, each gated

0. **Feasibility probe. No installs.** Establish what each of these five things *is*, whether it
   exists as an agent harness, whether it installs on Ubuntu 26.04, and — decisively — whether it
   accepts MiniMax OAuth. **Stop and report.** A claim whose harness cannot hold the model constant
   is unfalsifiable as stated, and that is a finding, not a blocker to route around.
1. Install, on opserver only, with a **removal manifest written as installation proceeds**.
2. Port the three roles: byte-identical prompts, capability-matched tools, diffs recorded.
3. Run the no-skills condition. Then the same-skills condition.
4. Score. Objective metrics mechanically; blind rubric by cross-family judges.
5. Pair review of answer quality: orchestrator + codex, disagreements published.
6. **Uninstall everything**, verified against the manifest and a before/after snapshot.

## 10. Constraints on the host

opserver is a worker, not a home. From the standing routing policy, all still in force:

- **No agent identity is copied there.** No `~/.hermes` rsync, no profile home.
- **Never bind :80 or :53** — pihole is the LAN's DNS and taking it down takes the house's
  internet down. Confirmed occupied at recon. Anything needing a port starts at **8081**.
- Unattended SSH is `BatchMode=yes ConnectTimeout=10`, and the box is not assumed to be up.
- Everything installed in this experiment is **temporary by contract** (phase 6).

Host at recon, 2026-08-20: 30 GiB RAM / 28 free, 8 cores, 80 GiB disk free, Docker 29.7.2,
Node 22.22.1, Python 3.14.4. Missing and needed: `uv`, `pipx`, `gh`.


---

## 12. Phase 0 result — 2026-08-20

**0 GO / 5 NO-GO. No contested cell is feasible under the OAuth control.**
[Full report](research/2026-08-20-bakeoff-phase0.md), orchestrator-verified against primary source.

| hypothesis | call | reason |
|---|---|---|
| H5 — melchior on dsh | NO-GO | `minimax_oauth: no` — the adapter offers no OAuth-only provider |
| H6 — balthasar on Playwright CLI | **DEAD** | not an agent harness at all — [R3](../lab/refuted/R3-playwright-cli-as-a-research-harness.md) |
| H7 — casper on Prime | NO-GO | `minimax_oauth: no`; plus a capability-parity defect, below |
| H8 — melchior on pi | NO-GO | `minimax_oauth: no` — MiniMax is registered API-key-only |
| H9 — balthasar on dsh | NO-GO | same adapter as H5 |

### 12.1 The five NO-GOs are one fact observed three times

pi, Prime Agent and DeepSeek Harness **all descend from or embed pi's provider layer** — Prime is a
hard fork of pi-mono, dsh's LLM seam is `@deepseek-ai/dsh-llm-pi-ai`. They inherit the same provider
model, in which MiniMax is API-key-only and the OAuth registry ships Anthropic, GitHub Copilot and
OpenAI Codex. See [F5](../lab/findings/F5-three-harnesses-one-provider-layer.md).

So the honest statement is **not** "five harnesses failed". It is: *one provider layer, shared by
three harnesses, does not implement MiniMax OAuth* — plus a category error, plus Hermes being the
only harness in the set that implements it natively.

This also degrades the grid independently of auth. The interaction H8 and H9 were added to detect is
much weaker evidence for a role × harness law when the harnesses are forks of each other. **The one
uncorrelated contrast is Hermes vs any single pi-descendant**, and any Phase 1 should be priced
against one contested cell rather than five.

### 12.2 A second, independent defect in H7

Prime Agent's only built-in model tool is `ipython`, which the model uses to read files, run
commands, edit code and inspect data. Allowlisting it grants filesystem, process and network
capability through one interpreter, so §2.1's **capability-matched tool allowlist** cannot be
satisfied with Prime's own allowlist. H7 would need external sandboxing to be comparable at all —
a defect that survives any decision about auth.

### 12.3 What Phase 0 delivered anyway

Per §8, the real deliverable was the **seam report**, and it arrived whether or not a run ever
happens:

- **dsh** — an agent-scoped prompt section with `complete: true` becomes the exact assembled prompt,
  and `includeRuntimeContext: false` suppresses dynamic additions. With
  [C1](../lab/confirmed/C1-dsh-plugin-seam-is-real.md), this is the strongest hosting seam found for
  a prompt compiler. Note its tool `restrict()` is **visibility composition, not an authority
  boundary** — relevant to anyone assuming a tool allowlist is a sandbox.
- **pi** — `--system-prompt` replaces the default outright, and `--no-context-files`,
  `--no-skills`, `--no-extensions`, `--no-prompt-templates` suppress discovered additions. That is
  precisely the control surface the main eval's arms need, and it is why pi remains the right
  harness for the 20-task A/B.
- **Prime** — the `ipython`-only tool design is a genuinely different bet, and the reason it cannot
  meet this protocol's capability control.

### 12.4 Status

**Phase 1 is not authorised.** The three live options — stop and bank the seam report, move the
whole grid to one metered API path, or write a MiniMax OAuth adapter — differ in cost and in what
they would measure, and the choice is the operator's. Nothing is installed; nothing needs
uninstalling. Phase 6 is a no-op unless Phase 1 proceeds.
