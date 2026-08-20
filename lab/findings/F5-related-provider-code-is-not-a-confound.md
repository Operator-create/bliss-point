# F5 — I mislabelled a sampling limit as a confound

**Filed 2026-08-20. Rewritten 2026-08-21 after pair review by codex, which was right.**

The original version of this finding claimed three things. Two were wrong, and the wrong ones were
mine — inferences layered on top of codex's Phase 0 data, not anything the probe reported.

## What was claimed, and what survives

| claim | verdict |
|---|---|
| (a) pi, Prime Agent and dsh "all descend from or embed pi's provider layer" — *"three of the four harnesses are the same harness"* | **too strong** |
| (b) the five NO-GOs are "one fact observed three times" | **wrong** |
| (c) the grid was "confounded independently of auth" | **wrong, and a category error** |

### (a) Related provider code — not one harness

The dependency is real: dsh's `@deepseek-ai/dsh-llm-pi-ai` depends on `@earendil-works/pi-ai`
`^0.82.1`, and Prime began as a hard fork of pi-mono. But its README continues, and I omitted the
continuation: *"it is now developed and distributed independently."*

The decisive check is where the shared code sits. Verified at the pinned commits:

- **`dsh/packages/core/agent-loop/package.json` has 11 dependencies and none is pi or
  earendil-works** — all are `@deepseek-ai/dsh-*`. The agent loop is entirely dsh's.
- dsh owns prompt assembly (`dsh-system-prompt`), tool mediation, context management. pi-ai sits
  **below** a dsh-owned adapter, as provider transport.
- The three trees pin **different pi-ai versions**: dsh 0.82.1, pi 0.84.2, Prime its own fork at
  0.7.4. Related code, not one installed library.

**Nearly everything the bake-off intended to vary sits above the shared layer.** "Three forks of one
codebase" was false for dsh, which is not a pi fork at all.

### (b) Correlated, not identical

Three distinct proximate causes, not one:

- **pi** — its MiniMax provider declares `auth.apiKey` only; no MiniMax OAuth module is registered.
- **Prime** — its repository-owned auth snapshot maps MiniMax to `MINIMAX_API_KEY`, and its built-in
  OAuth registry ships Anthropic, GitHub Copilot and OpenAI Codex. Plausibly correlated with pi's
  omission by ancestry, but Phase 0 ran no blame analysis proving one inherited change caused both.
- **dsh** — an **additional, independent** cause: its adapter builds its `Models` collection with no
  credential store and runs no login flow, so it rejects *every* OAuth-only provider. **That
  boundary would persist even if pi-ai gained a MiniMax OAuth module.**

H5 and H9 genuinely are one dsh result across two role cells — but that repetition is *by design*,
because it is what makes the role × harness interaction estimable.

### (c) The error worth keeping

**A confound must vary with the treatment.** A component held *common* across cells is the opposite:
it reduces transport noise and makes differences in prompt assembly, tool mediation and loop policy
*easier* to attribute to the harness. Forks with divergent tool and loop policies can be a cleaner
contrast than unrelated systems, not a dirtier one.

What I actually had was an **external-validity limit**: results from pi and Prime cannot be
generalised as three independent architectures or used to estimate how common MiniMax OAuth support
is across the ecosystem. That is a real caveat about *what the result would generalise to*. It is
not a defect in the comparison's internal validity, and it does not invalidate the grid.

I called a sampling limit a confound. This project has spent weeks policing exactly that distinction
— arm M, tier-vs-family — and I got it backwards the moment the error was mine and the conclusion
was convenient, because "the experiment was confounded anyway" is a comfortable thing to believe on
the day an experiment dies for unrelated reasons.

## What the finding is now

> pi, Prime Agent and dsh contain **related pi-family provider code**, so their MiniMax OAuth
> results are **correlated evidence, not three independent samples**. Deduplicate H5/H9 before any
> prevalence claim. This limits generalisation about the ecosystem; it does not make the harnesses
> the same, does not reduce three implementations to one cause, and does not confound a
> whole-harness comparison.

And the transferable rule: **record provider lineage and harness lineage separately.** They are
different axes, and a shared dependency at one is not shared behaviour at the other.

## What did not change

Phase 0's result stands: **0 GO / 5 NO-GO**, correctly a count of pre-registered *cells* rather than
a claim that five independent harnesses failed. No Phase 0 seam finding was withdrawn. The decision
to stop was not made on the strength of (c) and does not depend on it.

Related: [[R1-arm-M-as-falsifier]], [[R3-playwright-cli-as-a-research-harness]], [[F1-agent-reports-need-grepping]]
