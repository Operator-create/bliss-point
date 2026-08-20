# R3 — H6 is dead on arrival: Playwright CLI is not an agent harness

**Refuted 2026-08-20**, in Phase 0, before anything was installed.

## The claim

**H6:** Balthasar would be a better researcher running on Playwright CLI than on Hermes.

## Why it cannot be tested

`microsoft/playwright-cli` (Apache-2.0, ★12,683) is a **command-line interface to browser
automation**. Its own README states its requirements as *"Claude Code, GitHub Copilot, or any other
coding agent"* and its usage is to point such an agent at the CLI. It has no model provider, no
prompt assembly, and no autonomous LLM loop. There is no `minimax_oauth: no` to report, because
there is no model call at all.

It is a **tool that lives inside a research harness**, not a harness. Comparing "balthasar on
Playwright CLI" against "balthasar on Hermes" would compare Hermes-with-a-browser-tool against
Hermes-without-one — which is a real and interesting question, and **it is not the question H6
asked**. H6 asked about the harness.

## What was actually learned

The claim was a **category error**, and catching it cost one source-only probe rather than 12 runs
plus the setup around them. This is the design working exactly as intended: Phase 0 exists to kill
unfalsifiable claims before Phase 1 spends anything, and the brief explicitly instructed codex to
report a category error rather than substitute a stand-in tool to keep the cell alive.

## The question worth keeping

Whether *browser access* improves balthasar's research is testable, and the metric this lab already
chose for it is the right one: **verifiable-citation rate**, not eloquence. That is a tool-access
experiment inside one harness, not a harness comparison, and it is cheaper than H6 was going to be.
Filed as a candidate, not scheduled.

Related: [[H5-H9-harness-shapes-the-agent]], [[F5-three-harnesses-one-provider-layer]]
