# R1 — "Compiling against the wrong profile is a valid falsifier"

**Refuted 2026-08-20**, before any data was collected, by an independent audit
(../../docs/research/2026-08-20-arm-m-audit.md). Struck as Amendment 1.

The design compiled a brief against a deliberately wrong profile and treated C ≈ M as the line the
whole claim died on.

**What killed it:** it was a straw man the product could not lose to. `claude` and `antigravity` at
`implement` differ by an L1 of 2.30 across the four load-bearing dials, which drops the renderer
into a single "Design an approach for: {objective}" section aimed at a profile whose own notes say
it needs a task list and never an abstract problem. Beating that demonstrates "do not send an
architecture brief to a frontend engineer" — which the routing policy already knew. The dials were
never under test.

**Second defect, ours:** the registered threshold was "C − M ≥ +15pp" while the power analysis in
the same document said n=20 resolves only 25–30pp. The falsifier could not fire. It was not
repaired, because powering a straw man only yields a well-powered straw man.

**What replaced it:** arm A, a one-dial ablation across the render threshold, scored on
`scope_violations` and `steps`.
