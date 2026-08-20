# F5 — Three of the four harnesses are the same harness

**2026-08-20.** The most consequential result of Phase 0, and it is not the one the probe was
looking for.

## What the evidence says

| harness | relationship to pi | source |
|---|---|---|
| **pi** | is pi | `earendil-works/pi` |
| **Prime Agent** | *"began as a hard fork of pi-mono ... retains inherited `@earendil-works/pi-*` source package identifiers"* | its own README |
| **DeepSeek Harness** | its LLM seam is `@deepseek-ai/dsh-llm-pi-ai`, *"pi-ai-backed"* | its own package.json |

Verified directly from the pinned commits, not from the probe's summary.

## Why it matters more than the auth result

The bake-off grid set out to compare melchior on **Hermes vs dsh vs pi**, and balthasar on
**Hermes vs dsh**. Three of those four harnesses share pi's provider layer. So the grid was largely
preparing to compare **three descendants of one codebase** and attribute the differences to
"harness".

That is [§5.7's family-bias problem](../../docs/eval-protocol.md) transposed onto runtimes. This lab
has now hit the same structural error three times in three different costumes:

- **arm M** — comparing against a differently-shaped thing and calling the difference one variable ([R1](../refuted/R1-arm-M-as-falsifier.md))
- **tier vs family** — capability and vendor moving together (§3.1)
- **this** — "different harnesses" that are forks of a common core

The pattern is always the same: *the contrast was assumed rather than established*. Establishing it
is cheap and nobody does it, because the labels are different and different labels feel like
different things.

## It also explains the uniform NO-GO

The five NO-GO results are **not five independent facts**. dsh, pi and Prime all inherit pi's
provider model, where MiniMax is registered API-key-only and the OAuth registry ships Anthropic,
GitHub Copilot and OpenAI Codex. It is **one fact observed three times**, plus one category error
([R3](../refuted/R3-playwright-cli-as-a-research-harness.md)), plus Hermes being the only harness in
the set with a native MiniMax OAuth implementation.

Reporting it as "5 of 5 harnesses failed" would overstate the evidence considerably. The honest
statement is: **one provider layer, shared by three harnesses, does not implement MiniMax OAuth.**

## What survives

The grid's one genuinely uncorrelated contrast is **Hermes vs any single pi-descendant**. Running
all three pi-descendants was buying replication of a shared codebase at 3× the price, and the
interaction H8/H9 were added to detect — dsh helping melchior but not balthasar — is much weaker
evidence for a "role × harness" law when the harnesses are forks of each other.

Both remaining paths to Phase 1 should be priced against **one** contested cell, not five.

Related: [[R1-arm-M-as-falsifier]], [[R3-playwright-cli-as-a-research-harness]], [[H5-H9-harness-shapes-the-agent]]
