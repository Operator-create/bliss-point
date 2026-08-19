# Roadmap

Low resolution on purpose. Tickets stay fogged until they are in scope; zooming in early is how
plans rot.

## Phase 1 — curated (now)

- [x] Seven dials, additive resolution, deterministic renderer
- [x] Seven profiles derived from operational experience
- [x] Gap linter — the resolved point demands inputs, and says so before you spend tokens
- [x] Cross-family validator selection
- [x] Outcome log (written from day one; nothing reads it yet)
- [ ] Template overrides — per (target, phase) Markdown that replaces the default renderer
- [ ] Adapters: emit a brief straight into an existing multiplexer

## Phase 2 — measured (fogged)

The claim "these dial values are right" is currently unmeasured. Phase 2 makes it falsifiable.

- [ ] Eval bench: one task, N dial perturbations, per-model scoring
- [ ] Metrics: acceptance-criteria pass rate, retries, escalations, tokens, wall clock
- [ ] Mine the outcome log for shapes that correlate with rework
- [ ] Publish the numbers, including the ones that contradict the profiles

## Phase 3 — beyond (heavily fogged)

- [ ] Port the renderer to TypeScript so `dsh` and `pi` can consume the same Markdown templates
- [ ] Prefix/KV-cache-aware section ordering — stable prefix first, volatile context last
- [ ] Deterministic context selection (AST-derived graph) instead of raw file dumps

## Open questions

- Does `stakes` earn its place, or is it two dials wearing a trenchcoat?
- Are seven dials too many? The honest test is whether any two move together in every real profile.
- Is the gap linter better as a hard failure than a warning, in CI?
