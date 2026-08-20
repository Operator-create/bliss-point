# Harness seams — where a prompt compiler can attach

**The deliverable Phase 0 actually produced.** The [bake-off](harness-bakeoff.md) set out to
measure whether three agents perform better on other harnesses. It never ran: every contested cell
failed the model-constancy control. §8 of that protocol said the real
deliverable was a seam report regardless of whether a claim survived. This is it.

The question here is narrow and practical: **for each harness, what does it do structurally that
Hermes does not, and can Bliss Point attach to it without patching core?**

Everything below is from pinned commits, verified against primary source. Nothing was installed.

## Lineage, recorded on two separate axes

Provider lineage and harness lineage are different things, and conflating them produced a wrong
inference that pair review corrected
([F5](../lab/findings/F5-related-provider-code-is-not-a-confound.md)).

| harness | harness lineage | provider code |
|---|---|---|
| pi | upstream implementation | own `pi-ai` 0.84.2 |
| Prime Agent | hard fork of pi-mono, *"now developed and distributed independently"* | own `pi-ai` snapshot at 0.7.4 |
| DeepSeek Harness | **independent harness** — own agent loop, prompt assembly, tool mediation, context management | optional generic adapter depends on `pi-ai` `^0.82.1` |
| Hermes | separate implementation | the only inspected harness with native MiniMax OAuth |

**These are at least three materially distinct harness designs.** dsh is not a pi fork: its
`agent-loop` package has eleven dependencies and none is pi. Related provider code makes their
*auth-support* results correlated; it does not make the harnesses alike.

## DeepSeek Harness — the most explicit prompt-injection seam inspected

MIT. Already confirmed in [C1](../lab/confirmed/C1-dsh-plugin-seam-is-real.md) by cloning rather
than reading press: `ctx.systemPrompt.section()`, the `system-prompt/assemble` and `agent/pre-step`
waterfalls, vendored Cordis, reversible teardown. **A prompt-shaping plugin needs no patch to core.**

Phase 0 adds the detail that matters for a compiler:

- An agent-scoped prompt section with **`complete: true`** is restored as the sole prompt section
  after the assembly waterfall, and **`includeRuntimeContext: false`** suppresses dsh's separately
  injected context snapshots.

  **This is not yet a byte-identical wire channel, and it should not be described as one.**
  `renderPrompt()` still interprets `{{variable}}` groups and drops empty sections before the
  adapter places the string into pi-ai's `systemPrompt` slot, and pi-ai then does provider-specific
  serialisation. Phase 0 captured no outgoing request. Wire-level byte identity is an **execution
  gate**, to be demonstrated by capturing a real request — not inferred from source.
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
comparing a well-equipped agent with a hobbled one — cannot be expressed by Prime's *shipped*
built-in allowlist, which cannot subdivide `ipython`'s capabilities. Capability parity would need an
external sandbox or separately verified custom tools with `ipython` disabled; Phase 0 evaluated
neither route.

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

1. **dsh is the leading candidate for a future prompt-seam prototype** — the only harness inspected
   offering a documented, reversible complete-prompt injection API without a core patch. Not an
   "adoption target": this was a source-only probe that installed nothing, ran nothing, captured no
   wire traffic, and did not satisfy the auth path. Those are separate gates.
2. **pi has the most directly exposed CLI control surface** of the candidates, which is what
   information-matched arms need. Confirming it as the eval harness is conditional on a
   pinned-version smoke test and a captured outgoing system message — the caveat above governs the
   recommendation rather than trailing it.
3. **A tool allowlist is not an authority boundary.** Stated by dsh about its own design, and true
   of the others; worth propagating into this project's own language about `return_contract` and
   tool scoping, which has been loose about the distinction.
4. **Record provider lineage and harness lineage separately.** Related provider code makes
   auth-support results correlated and limits ecosystem generalisation. It does **not** make the
   harnesses identical, and it does not invalidate a whole-harness contrast — a component held
   common across cells reduces noise rather than confounding it. Getting this backwards is
   [F5](../lab/findings/F5-related-provider-code-is-not-a-confound.md).
