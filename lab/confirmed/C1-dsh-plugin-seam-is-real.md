# C1 — DeepSeek Harness can host Bliss Point as a plugin

**Confirmed 2026-08-19** from primary source, by cloning the repository rather than reading press.

`ctx.systemPrompt.section()`, plus the `system-prompt/assemble` and `agent/pre-step` waterfalls, on
vendored Cordis with reversible teardown. A prompt-shaping plugin needs no patch to dsh core.

**Source:** deepseek-harness `packages/core/system-prompt/src/index.ts`, `docs/architecture.md`,
`LICENSE` (MIT). Settled roadmap D1.

**Not confirmed in the same pass:** a "120× cost reduction" figure reported as FACT by the same
investigation appears nowhere in the dsh tree. See findings/F1.
