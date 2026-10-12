# Roadmap

Format: [Wayfinder](wayfinder.md). Nodes are decisions; tickets are CLEAR, DIM or FOGGED; a ticket
is only specified in detail once its parent decision is settled.

**North star:** an operator running several agents reaches for Bliss Point at the moment of handoff,
the way they reach for a formatter before a commit.

---

## D0 — Does Bliss Point own any dispatch?

**SETTLED 2026-08-19** — No. It is a prompt compiler; routing, sockets and sessions stay in the
harness. Settled by the user, directly, against the original multiplexer framing.

Everything below inherits this. A ticket that needs a runtime is out of scope by construction, and
that is the single most useful thing this tree does.

---

## D1 — What surfaces does it ship on?

**SETTLED 2026-08-19** — All three, in this order: Python library, then a dsh plugin, then a
TypeScript renderer. Settled by a primary-source
[investigation](research/2026-08-19-harness-investigation.md) that cloned the repositories.

What settled it:

- **dsh's plugin seam is real and named.** `ctx.systemPrompt.section()`, plus the
  `system-prompt/assemble` and `agent/pre-step` waterfalls, on vendored Cordis with reversible
  teardown. A prompt-shaping plugin needs no patch to core.
- **Forking pi is rejected.** Its loop is 797 lines inside a ten-package monorepo. A survive/delete
  map put loop, tools, sessions, TUI and server in DELETE and left only `prompt-templates.ts` and a
  model-id list surviving — over 95% deleted on day one. We imitate pi's layering and consume it.
- **The counterargument is recorded:** forking wins *if* Bliss Point becomes an interactive
  end-to-end tool. That violates D0, so it loses here and only here. If D0 ever reopens, this
  decision reopens with it.

- **T1.1 — dsh plugin.** DIM. Hook `system-prompt/assemble`; declare `inject: ['systemPrompt']`.
- **T1.2 — TypeScript renderer over the same YAML/Markdown.** DIM. Still gated on D3, since
  template overrides would have to port too.
- **T1.3 — pi package.** DIM, and promoted: the audit found `dodo-reach/pi-clarify` (verified,
  169★) already doing "rewrite rough prompts before send" *as a pi package*, alongside 788 repos
  under the `pi-package` topic. The extension surface is where this ecosystem actually adopts
  things; a library people must remember to call is not.
- **T1.4 — Publish to PyPI.** DIM. Unblocked by nothing; wants a name check first.

---

## D2 — Are the dial values right?

**OPEN**, and openly so — the README says the numbers are calibrated opinion.

**Settled by:** an eval bench that perturbs one dial at a time and scores acceptance-criteria pass
rate against token cost. Until then no benchmark is claimed anywhere in the repo.

- **T2.1 — Outcome log.** CLEAR, done. Append-only JSONL, written from day one.
- **T2.2 — The 20-task A/B on pi.** CLEAR. Protocol pre-registered in
  [eval-protocol.md](eval-protocol.md): four information-matched arms (raw / flat / compiled /
  one-dial ablation), two model tiers, 480 runs, thresholds declared before any data exists.
  The tier interaction is the thesis; arm A is the mechanism falsifier. **Blocked on T2.7** —
  there is nothing to run until tasks exist.
- **T2.3 — The `flat` renderer for arm F.** DONE 2026-08-20, before the task corpus existed.
  `bliss flat` / `blisspoint.flat()`. Its control properties are enforced by tests: no recipient
  parameter, drops nothing, and provably a superset of every compiled brief across all profiles
  and phases.
- **T2.4 — Publish results including the ones that contradict the profiles.** FOGGED.
- **T2.5 — Mine the outcome log for shapes that correlate with rework.** FOGGED. Needs volume first,
  which means dogfooding is the prerequisite, not a nice-to-have.
- **T2.7 — The task corpus and its admissibility gate.** CLEAR, machinery DONE 2026-08-20 in a
  separate repo (`bliss-point-corpus`) so no agent under test can read its own grader. The gate
  enforces six rules and *fails* rather than warns; 17 fixture tests prove it rejects each one.
  **Tasks: 0 of 20.** They are sourced from closed issues on real repositories whose fixing PR
  added a test, verified against the GitHub API by `verify_candidate.py` before admission — a
  task authored here would encode the hypothesis it is meant to test.
- **T2.6 — Make stable-before-volatile section order an invariant.** DIM. See
  [token economy](token-economy.md); the renderer already does it by intuition, and a test should
  make it a rule so a brief's head stays a reusable cache prefix.

---

## D3 — Do templates override the renderer, or only feed it?

**OPEN.** Today the renderer builds every section in code and the profiles supply only data. The
alternative is per-`(target, phase)` Markdown that replaces the default rendering wholesale.

**Settled by:** the first real case where the code renderer cannot express a shape someone needs.
Not before — this is a decision that should be forced by evidence, not taken on elegance.

**Risk if we get it wrong:** overrides are the obvious path to 126 drifting templates, which is the
exact failure the additive dials were chosen to avoid.

- **T3.1 — Template override loader.** DIM.
- **T3.2 — Section-level overrides instead of whole-brief.** FOGGED. Probably the safer shape, if
  D3 lands on yes.

---

## D4 — Is the gap linter advisory or blocking?

**SETTLED 2026-08-19** — Both, split by code. Two conditions block; everything else advises.
Settled by an [independent audit](research/2026-08-19-grok-audit-and-pi-sentiment.md) making the
argument that a total hard gate makes a one-line handoff impossible, while a total advisory gate
turns the load-bearing feature into a warning nobody reads.

Blocking: `objective_empty` always, and `acceptance_missing` when `acceptance_binding >= 0.6`.
`bliss compile --gate` exits 1 on those; `--strict` still exits 1 on any gap.

- **T4.1 — Pre-dispatch hook that refuses a blocking brief.** DIM. Now well-defined enough to build.
- **T4.2 — The drop channel.** DONE 2026-09-10. `Brief.drops`, alongside `Brief.gaps`. A gap points
  forward (*the recipient needs something you did not supply*); a drop points backward (*you
  supplied something and the shape removed it*). Separate channels because the remedies are
  opposite — gather it, versus override the dial — and because reporting 448 correct selections as
  gaps would bury the two that are not. Drops are **advisory by construction**: they never block,
  since a correct selection is not an error. See
  [F6](../lab/findings/F6-the-compiler-removed-a-quarter-of-what-it-was-given.md).

---

## D5 — Does `stakes` earn its place?

**OPEN, and now with a measurement that narrows it.** It currently moves four dials in a fixed
pattern. That may mean it is a real axis, or that it is two dials wearing a trenchcoat.

**Settled by:** whether any profile ever needs a stakes table that is not a scalar multiple of the
default one. One counterexample settles it.

**Evidence 2026-09-10** ([F7](../lab/findings/F7-the-dials-are-continuous-the-renderer-is-not.md)):
across the eight shipped profiles, low / normal / high produce a **byte-identical brief at 31 of 48
(profile, phase) pairs**. Where it does change something, it changes it through
`acceptance_binding` and `verification_rigor`. Its `+0.15` to `escalation_explicitness` at high
stakes buys an escalation section for **no profile in any phase** — checked exhaustively, not
sampled.

That is not yet an answer to D5, because 17 of 48 pairs do differ. It is a sharper question:
`stakes` earns its place through two dials, and is inert on the one an operator would most expect it
to move. Whether that is a bad axis or a badly calibrated one is **D8**, below.

---

## D6 — Seven dials, or fewer?

**OPEN, now with a measurement.** `bliss correlate` computes pairwise Pearson correlation across
the installed profiles. Run against the seven shipped profiles:

| pair | r | |
|---|---|---|
| specificity / verification_rigor | **+0.978** | moves together |
| acceptance_binding / verification_rigor | **+0.921** | moves together |
| specificity / acceptance_binding | **+0.904** | moves together |
| autonomy / escalation_explicitness | −0.632 | independent enough |
| specificity / decomposition | +0.604 | independent enough |
| context_volume / anything | ≤ +0.773 | the most independent dial |

An external audit predicted two merges: `acceptance_binding + verification_rigor`, and
`autonomy + escalation_explicitness`. **The first is supported (+0.921). The second is not
(−0.632)** — those two move in *opposite* directions, which is what you would expect if
escalation is what you add when you take autonomy away, rather than a synonym for it. The audit
also expected `specificity` and `decomposition` to track each other; at +0.604 they are among the
weakest pairs, while the tightest pair in the whole matrix — `specificity / verification_rigor` at
+0.978 — is one nobody predicted.

**Why this does not settle it.** All seven profiles have one author. A correlation across them
measures that author's habits, not a property of language models. Merging dials on this evidence
would repeat the exact error the audit accuses the project of: acting on unmeasured taste while
calling it a finding.

**Settled by:** the same matrix computed over profiles written by other people, or by the D2 bench
showing that perturbing two "separate" dials produces indistinguishable outcomes. Until then the
hypothesis is recorded, not applied.

**The caution above now has a number, 2026-09-10.** Adding an eighth profile (`astra`, derived from
the routing policy, nothing else changed) moved the matrix by a **mean of 0.176** across all 21
pairs and pushed three pairs across the |r| ≥ 0.9 line. The audit's one surviving merge candidate
fell out of merge range, `acceptance_binding / verification_rigor` +0.921 → **+0.796**, and so did
the tightest pair in the matrix, `specificity / verification_rigor` +0.978 → **+0.754**, which the
roadmap records as the pair nobody predicted. The largest single move was
`decomposition / context_volume`, +0.773 → **+0.183**, because `astra` is the first profile to
combine low decomposition with high context volume — a corner of the space that had been empty, and
whose emptiness was what the correlation was measuring.

Had the merge been taken on the n=7 evidence, one new profile would have unmade it. See
[F9](../lab/findings/F9-one-profile-moved-the-whole-correlation-matrix.md), where an adversarial
review established the part that matters: the shift is not generic small-sample instability. A
profile resampled from the habits already in the set matches it about 1% of the time, and 12 of 13
synthetic eighths leave `decomposition / context_volume` where the n=7 matrix put it. The cause is
**corner occupancy**, so the right statement of D6's caution is that the matrix is fitted to a hull
and does not generalise outside it. The numbers in the table above are the n=7 ones and are kept as
they were published; `bliss correlate` prints the current set.

---

## D8 — Should a phase or stakes delta be able to reach a render threshold?

**OPEN. Filed 2026-09-10** from
[F7](../lab/findings/F7-the-dials-are-continuous-the-renderer-is-not.md).

Resolution is continuous; the renderer reads the result only through eleven `>=` thresholds. The
deltas in `_phases.yaml` and `_stakes.yaml` were calibrated as if the output were continuous too, so
most of them land inside a step and change nothing. 144 (profile × phase × stakes) points produce
**26 distinct briefs**; `claude` produces one brief at all 18 of its points.

**There is already a counterexample on the record**, which is what makes this a decision rather than
a curiosity. On 2026-08-20 a high-stakes `codex` brief needed its escalation triggers — they were
safety stops — and no phase or stakes setting could produce them. It took a manual dial override,
with the reason written down.

Five options, none taken:

1. **Accept it.** Profile base values decide shape; phase and stakes are documentation with
   arithmetic attached. Cheapest and honest, if the README stops implying otherwise.
2. **Widen the deltas** so a phase or stakes change can cross a threshold. This is a dial-value
   change and therefore blocked behind **D2** — it is exactly the unmeasured retuning this project
   refuses to do on taste.
3. **Move the thresholds per profile.** More expressive, and it makes every profile a renderer
   config; D3's 126-drifting-templates risk in a new place.
4. **Render continuously** — graded prose rather than present/absent sections. Large, and it would
   make the arm C / arm F information-subset property much harder to establish.
5. **Make supplied stop conditions undroppable**, treating "an escalation trigger the operator wrote
   down must reach the recipient" as a safety invariant rather than a dial-quality question. Narrow,
   and the only option that addresses the recorded counterexample directly. It changes the semantics
   of one dial, so doing it before the D2 bench runs would contaminate the thing the bench measures.

**Settled by:** the operator, on option 5, since it is a safety call rather than a measurement; and
by the D2 bench on the rest. Until then, drops are at least **audible** (T4.2), which is what was
missing when the counterexample happened.

---

## D7 — Is "prompt compiler" the right positioning?

**SETTLED 2026-08-20** — No. Bliss Point is a **task-contract compiler**, and the headline is the
refusal, not the compilation: *it refuses to dispatch a brief the recipient cannot execute.* The
dials are the IR; the linter is the product. Settled by the author, adopting the audit's argument.

The reasoning that won: compilers imply IR, optimisation and backends; DSPy
already owns the term in this space; and the sharpest sentence available is not "we compile
prompts" but **"we refuse to dispatch a brief the recipient cannot execute."** Its proposal is
*handoff contract* or *task-contract compiler* — the linter is the product, the dials are the IR.

**Counterargument on the record, now overridden:** "prompt compiler" is a category people already
search for, which matters for a project with a reputation goal. Overridden because searchability
into a crowded category is worth less than one sentence nobody else is saying, and because DSPy
already owns the term for a different thing.

**What this changes:** the README headline and framing. Not the name, not the API, not the module
layout. If the eval in D2 shows the dials do nothing and only the linter carries the effect, this
positioning will already be the honest one.

---

## Invariants

Not decisions. These are the constraints every branch above inherits, taken from what makes pi worth
admiring:

- **Readable in one sitting.** If the library stops fitting in a person's head, the design failed,
  and no feature is worth that.
- **No model in the compile path.** Resolution stays deterministic, or the bench means nothing.
- **Never invent content.** A dial that demands input you did not supply reports a gap. Always.
- **Profiles are data.** Anyone can replace the whole set with `BLISSPOINT_PROFILES` and owe us
  nothing.
