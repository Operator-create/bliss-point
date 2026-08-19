# Token economy

Techniques found **implemented in source**, not proposed in blog posts. Extracted from an
[investigation](research/2026-08-19-harness-investigation.md) of DeepSeek Harness (`dsh`) and pi,
then re-verified path by path.

Evidence tags are used strictly: **FACT** means the file exists and says what is claimed.
**INFERENCE** means the mechanism is real but the stated *benefit* is deduced, not documented.

| # | Technique | Where it lives | What it buys | Tag |
|---|---|---|---|---|
| 1 | Append-only event log | `dsh` `packages/core/session`, `docs/architecture.md:45` | History is an immutable `SessionEvent` fold; past turns are never mutated, so the provider's prompt prefix stays byte-identical across steps and keeps hitting cache | log is **FACT**, cache benefit is **INFERENCE** |
| 2 | Tail-end compaction | `dsh` `packages/compaction/compaction/src/` (see `tool-pairing.ts`, "surface tail"); pi `packages/agent/src/harness/compaction/` | Summarisation is appended at the request tail instead of rewriting the system prompt, so compaction does not evict the warm prefix it is trying to save | **FACT** |
| 3 | Programmatic tool execution | `dsh` `packages/code-runtime/code-runtime-worker-thread/` | The model writes a script that loops and filters in a worker thread, returning one curated payload instead of dozens of intermediate tool-call turns | **FACT** |
| 4 | Output truncation and spilling | `dsh` `packages/spill/`; pi `packages/agent/src/harness/utils/truncate.ts` | Bulky tool output is truncated into context and persisted to disk, so one `find /` does not end the session | **FACT** |
| 5 | Subagent context isolation | `dsh` `packages/subagent/`; `pi-agent-harness` `extensions/subagent/` | Sub-tasks get an ephemeral context and hand back only a structured artifact | **FACT** |

## One claim we removed

The source investigation reported a "120× cost reduction ($0.0035/M vs $0.435–$1.32/M)" for
technique 1. Searching the `dsh` tree for every one of those figures returns **no match**. It is not
in the repository, so it is not repeated here as anything but a caution: a number with no file
behind it did not survive, no matter how confidently it was tagged FACT.

## What this means for a prompt compiler

Bliss Point never runs a loop, so techniques 2–5 are not ours to implement. Technique 1 is, and it
lands on one specific design decision: **section order**.

A brief's stable sections (role header, accepted decisions, constraints, return contract) are
identical across every call for a given profile. The volatile sections (evidence, current state,
subtasks) change per task. Emitting stable-then-volatile means the invariant head of the brief is
a reusable cache prefix; emitting them interleaved means every brief is a cache miss from its first
differing byte.

The renderer already orders sections this way, but by intuition rather than by rule. **T2.6** makes
it an invariant with a test that fails if a volatile section is emitted above a stable one.
