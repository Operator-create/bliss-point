# Harness seams — where a prompt compiler can attach

**The deliverable Phase 0 actually produced.** The [bake-off](harness-bakeoff.md) set out to
measure whether three agents perform better on other harnesses. It never ran: every contested cell
failed the model-constancy control, and the grid turned out to be confounded independently of that
([F5](../lab/findings/F5-three-harnesses-one-provider-layer.md)). §8 of that protocol said the real
deliverable was a seam report regardless of whether a claim survived. This is it.

The question here is narrow and practical: **for each harness, what does it do structurally that
Hermes does not, and can Bliss Point attach to it without patching core?**

Everything below is from pinned commits, verified against primary source. Nothing was installed.

## The lineage, first, because it reframes everything else

| harness | relationship | evidence |
|---|---|---|
| pi | the origin | `earendil-works/pi` |
| Prime Agent | hard fork of pi-mono | *"retains inherited `@earendil-works/pi-*` source package identifiers"* |
| DeepSeek Harness | embeds pi's LLM layer | package named `@deepseek-ai/dsh-llm-pi-ai`, *"pi-ai-backed"* |
| Hermes | independent | the only one of the four with native MiniMax OAuth |

Three of the four are one family. Read the seams below as **two designs**, not four.

## DeepSeek Harness — the strongest hosting seam

MIT. Already confirmed in [C1](../lab/confirmed/C1-dsh-plugin-seam-is-real.md) by cloning rather
than reading press: `ctx.systemPrompt.section()`, the `system-prompt/assemble` and `agent/pre-step`
waterfalls, vendored Cordis, reversible teardown. **A prompt-shaping plugin needs no patch to core.**

Phase 0 adds the detail that matters for a compiler:

- An agent-scoped prompt section with **`complete: true`** becomes the exact complete prompt after
  assembly, and **`includeRuntimeContext: false`** suppresses dynamic additions. That is a
  byte-identical prompt channel — the thing Bliss Point needs to hand over a compiled brief without
  the harness editing it underneath.
- Tools are limited by composing only the required rows, or by `ctx.tools.restrict(filter)`.

**One warning worth carrying out of this exercise.** dsh's own tools README states that
`restrict()` is **visibility composition, not an authority boundary**. A restricted tool list is not
a sandbox: it changes what the model is offered, not what the process can do. Anyone — including
this project — who has reasoned "the allowlist is the containment" should read that sentence twice.

## pi — the control surface the eval needs

MIT. Not a hosting seam; a **control surface**, and an unusually complete one:

- `--system-prompt <text>` replaces the default prompt outright
- `--no-context-files`, `--no-skills`, `--no-extensions`, `--no-prompt-templates` suppress every
  automatically discovered addition
- `--tools <list>` is an allowlist; `--no-tools` / `--no-builtin-tools` are stricter floors

That combination is exactly what the [20-task A/B](eval-protocol.md) requires: four arms must differ
*only* in the text of the brief, which is impossible on a harness that silently appends skills or
context files. **This reconfirms pi as the right harness for the main eval**, independently of the
bake-off's collapse, and for a better reason than "it is multi-provider".

Caveat recorded: CLI semantics are a claim, not a proof. Phase 1 of the eval should capture one
outgoing request and diff it against the compiled brief to establish byte identity rather than
assume it.

## Prime Agent — a different bet, and why it fails this protocol

MIT, hard fork of pi. Its distinguishing choice is that **the model's only built-in tool is
`ipython`** — used to read files, run commands, edit code and inspect data through one interpreter.

That is a genuinely interesting design and it is why H7 could not have been run cleanly even with
the auth question solved: allowlisting `ipython` grants filesystem, process and network capability
in a single grant, so a **capability-matched** tool allowlist — the bake-off's control against
comparing a well-equipped agent with a hobbled one — cannot be expressed with Prime's own allowlist.
Containment would have to come from outside the harness.

Also relevant to anyone pointing a harness at MiniMax: at the pinned commit Prime's direct `minimax`
catalog exposes M2.7 variants, and **MiniMax-M3 is reachable only as `minimax/minimax-m3` through
`prime-inference`** with a `PRIME_API_KEY`. A model name matching is not the same as the same
serving path.

## Playwright CLI — not a harness

Apache-2.0. Browser automation driven *by* an agent; its README requires *"Claude Code, GitHub
Copilot, or any other coding agent"*. No model provider, no prompt assembly, no loop.
[R3](../lab/refuted/R3-playwright-cli-as-a-research-harness.md) records the refutation. It may be a
useful **tool inside** a research agent, which is a separate and cheaper experiment.

## What Bliss Point should take from this

1. **dsh is the adoption target if one is wanted.** It is the only harness examined that offers a
   documented, reversible seam for injecting a complete system prompt without forking it.
2. **pi stays the eval harness.** Its suppression flags are what make information-matched arms
   possible at all.
3. **A tool allowlist is not an authority boundary.** Stated by dsh about its own design, and true
   of the others; worth propagating into this project's own language about `return_contract` and
   tool scoping, which has been loose about the distinction.
4. **Check lineage before claiming a contrast.** Three "different harnesses" sharing one provider
   layer is the same error as arm M and as tier-vs-family, and it is cheap to check first.
