# Bliss Point

**A handoff contract for multi-agent work: it refuses to dispatch a brief the recipient cannot
execute.**

Routing decides *who* gets the work. Bliss Point decides *what shape the work arrives in*, and then
checks that what you supplied is enough for that particular recipient to act on.

A frontier reasoning model handed a 14-step checklist will follow the checklist instead of noticing
the checklist is wrong. A fast execution model handed a goal abstraction will improvise scope you
never asked for. Same task, same words, opposite failure. The fix is not a better prompt; it is a
different *shape* of prompt per recipient — and the shape is a deterministic function of who is
receiving it, what phase the work is in, and what it costs to be wrong.

Bliss Point is a small, dependency-light **task-contract compiler**. The dials below are its
intermediate representation; the linter is the part you actually feel. It does not route, dispatch,
run a loop, or hold a socket. It takes what you know about a task and emits the brief. Your harness —
[DeepSeek Harness](https://github.com/deepseek-ai), [pi](https://github.com/earendil-works/pi),
Claude Code, a shell script — does the sending.

```python
import blisspoint as bp

brief = bp.compile(task, target="codex", phase="implement", stakes="high")
print(brief.text)              # the brief
for gap in brief.gaps:         # what you failed to supply that this agent will need
    print(gap.code, gap.details)
```

## The seven dials

There is no "small model prompt" and "big model prompt". It's a gradient, so the tiers are a point
in a seven-dimensional space, each axis 0.0 → 1.0:

| dial | 0.0 | 1.0 |
|---|---|---|
| `specificity` | state the goal, let the agent choose the steps | prescribe the steps |
| `decomposition` | one outcome | numbered, individually testable subtasks |
| `acceptance_binding` | criteria at the end of the whole task | criteria inside every subtask |
| `autonomy` | every decision is already made | the agent owns the design decisions |
| `context_volume` | minimum-sufficient handoff, start fresh | full evidence corpus, continue the thread |
| `verification_rigor` | self-report is enough | named command / screenshot / test evidence required |
| `escalation_explicitness` | no escalation path stated | enumerated escalation triggers |

The point resolves deterministically, with no model in the loop:

```
profile base dials  →  + phase deltas  →  + stakes deltas  →  + explicit overrides
```

```console
$ bliss dials antigravity --phase implement
antigravity · implement · normal stakes

  specificity              ########.. 0.85
  decomposition            #########. 0.90
  acceptance_binding       ########## 1.00
  autonomy                 ##........ 0.20
  context_volume           ######.... 0.60
  verification_rigor       ########## 0.95
  escalation_explicitness  ###....... 0.30
```

## The linter is the product

Dials do not invent content — they *demand* it. If the resolved point says this agent needs
per-subtask acceptance criteria and you supplied none, that is a gap, reported before you spend the
tokens:

```console
$ bliss compile balthasar --objective "Check if the plugin APIs are stable" --phase research --stakes high --strict
  - context_volume is high but no evidence supplied — either gather it or turn the dial down
  - decomposition is high but no subtasks supplied — this agent needs an engineering task list, not one outcome
  - no acceptance criteria — there is no observable definition of done
  - verification_rigor is high but no verification method — name the command, test or visual check
  - escalation_explicitness is high but no triggers named — say when to stop and hand back
```

That is a lazy one-line delegation getting caught at compile time instead of coming back four
minutes later as a confident, unfalsifiable answer.

Each gap carries a stable `code` (`subtasks_missing`, `evidence_bulky`, …) and structured
`details` such as `{"subtask_ids": ["ST3"]}`. Branch on the code; the message wording is for
humans and is not part of the API.

## Install

```bash
pip install -e .
bliss profiles
```

Python ≥3.10, one dependency (PyYAML). The profiles and templates are plain YAML and Markdown, so a
port to another language is a renderer, not a rewrite.

## Profiles

An agent profile is base dials plus the operational facts that shape a brief — model family (used
to keep validators cross-family), what it returns, and the traps it has actually walked into.

```yaml
name: balthasar
family: minimax
role: hermes researcher / critic / risk hypothesis generator
dials:
  decomposition: 0.80
  context_volume: 0.70
  autonomy: 0.40
  # ...
notes:
  - No working web access. Supply the corpus in a file; never ask it to recall external facts.
  - Reads the working tree, not the commit you name.
  - Treat its security warnings as hypotheses until corroborated.
```

Ships with `claude`, `codex`, `antigravity`, `grok`, and the Hermes triad (`casper`, `balthasar`,
`melchior`). Point `BLISSPOINT_PROFILES` at your own directory to replace them entirely — the
profiles are data, not code.

That directory is a complete configuration: your profiles plus `_phases.yaml` and `_stakes.yaml`.
It is validated on load and fails once, naming the file and the key. A misspelled `dial:` or an
unknown dial name is an error, never a profile that quietly runs at the 0.5 defaults.

## Cross-family validation

A model reviewing its own family's work agrees with it too often. `cross_family()` returns only the
profiles eligible to validate a given author:

```console
$ bliss validators balthasar
antigravity
claude
codex
grok
```

## Status

**v0.1 — usable, and honest about what it is not.**

Phase 1 is deterministic and curated: the profiles encode operational experience, not measurements.
Every compiled brief and its outcome is appended to a JSONL log (`bp.record(brief, "pass")`), which
is the raw material for Phase 2 — an eval bench that perturbs one dial at a time and scores
acceptance-criteria pass rate against token cost. Until that exists, the numbers in the profiles are
**calibrated opinion, clearly labelled as such**. No benchmark is claimed.

## Non-goals

- Routing, dispatch, session management, sandboxes, event buses — that is your harness's job.
- Being a framework. The whole library is a few hundred lines and reads in one sitting.
- Guessing. When a dial demands input you did not give, it reports a gap; it never fills one in.

## The lab

The numbers in `profiles/` are calibrated opinion, and this repository keeps a working record of
turning them into something better — or discarding them.

- **[`lab/hypothesis/`](lab/hypothesis/)** — the live claims, each one naming what would kill it.
- **[`lab/refuted/`](lab/refuted/)** — what died, and what killed it. **Start here.** A falsifier
  the product could not lose to, struck before any data was collected; a dial merge an audit
  recommended, killed by measurement at r = −0.632.
- **[`lab/confirmed/`](lab/confirmed/)** — what survived, marked provisional.
- **[`lab/findings/`](lab/findings/)** — including the one about a fabricated benchmark figure that
  arrived tagged `FACT` with a 100% confidence column.
- **[`lab/logbooks/`](lab/logbooks/)** — written as it happened, dead ends included.
- **[`docs/eval-protocol.md`](docs/eval-protocol.md)** — the 20-task A/B, pre-registered with
  binding thresholds, an honest power analysis, and a public amendment log.

If `lab/refuted/` is ever empty, nothing here is being tested.

## Prior art

- **[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)** — MIT, on vendored
  Cordis. Verified pluggable at the prompt seam: `ctx.systemPrompt.section()` and the
  `system-prompt/assemble` and `agent/pre-step` waterfalls. Bliss Point can ship as a plugin there
  without patching core. (Star counts quoted in press are unverified here.)
- **[pi](https://github.com/earendil-works/pi)** — MIT. Widely described as "an agent loop in ~300
  lines"; measured, `packages/agent/src/agent-loop.ts` is **797 lines** inside a ten-package
  monorepo. The layering is real in code even though the size claim is not: `pi-ai` (completions)
  / `pi-agent` (loop, tools, sessions) / `pi-tui` + `pi-coding-agent` (interface). Bliss Point
  imitates that separation and targets pi as a consumer; it does not fork it, because a fork
  inherits a runtime a compiler has no use for.
- **[pi-agent-harness](https://github.com/baryonlabs/pi-agent-harness)** — generates specialist
  agents and orchestration prompts from a domain sentence. Adjacent, and it generates a team;
  Bliss Point shapes each handoff to a team you already have.

None of them treat prompt shape as a function of the recipient. That gap is the whole project.

## License

MIT
