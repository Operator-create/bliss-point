# T1 — Prompt shape as a deterministic function of the recipient

**Status: unmeasured. This is the thing the lab exists to test.**

The model: a brief's effectiveness depends on the *shape* it arrives in, shape is a point in a small
number of continuous dimensions, and the right point is a deterministic function of
(recipient, phase, stakes) rather than something a model should be asked to choose.

Two consequences the theory commits to, both falsifiable:

1. **The point is computable without inference** — no model in the compile path, or the whole
   apparatus is just another LLM call and the determinism claim is empty.
2. **The right point differs by recipient** — otherwise there is one good brief format, and the
   correct product is a template plus a linter (hypothesis/H2).

The dials are the current guess at those dimensions, not the theory itself. If `bliss correlate`
and the arm A ablation collapse seven dials to three, the theory survives with a smaller IR. If
shape turns out not to matter once information is held constant, the theory is dead and
hypothesis/H1 is what kills it.

---

## Revision, 2026-09-10 — "continuous" was the wrong word for the output

The model above says shape is "a point in a small number of **continuous** dimensions". Measured,
that is true of the resolution and false of the rendering.
[F7](../findings/F7-the-dials-are-continuous-the-renderer-is-not.md): the renderer reads the dials
only through eleven `>=` comparisons, and the 144 (profile × phase × stakes) points the shipped
profiles can reach produce **26 distinct briefs**. For `claude`, all 18 points produce one.

The theory is amended rather than damaged, and the amendment is worth stating precisely because it
changes what an experiment can see:

> Shape is a point in a small number of **quantised** dimensions. Continuity lives in the
> composition — base plus phase plus stakes plus overrides — and is discarded at the last step. The
> observable object is the set of sections a brief contains, and it is a boolean vector.

Two consequences the amended theory commits to:

1. **An eval can only see threshold crossings.** Perturbing a dial within a step is guaranteed to
   change nothing, so a null result from such a perturbation is evidence about the renderer, not
   about the dial. The arm A ablation was already specified across the render threshold, which was
   the right call for a reason not stated at the time.
2. **A delta that cannot reach a threshold is not a small effect, it is no effect.** High stakes
   adds +0.15 to `escalation_explicitness` and buys an escalation section for none of the eight
   shipped profiles, in any phase. The
   first consequence of the amendment is that this is a **design defect to decide about**
   ([D8](../../docs/roadmap.md)), not a measurement to interpret.

What survives untouched is the part the lab exists to test: that the right point is a deterministic
function of the recipient, and that the function needs no model. Quantised or not, nothing in F7
bears on whether the point is *correct*.

A second amendment was proposed and is **not** being made. H10 held that the function's domain is
larger than `(recipient, phase, stakes)` — that a mode set at the receiver belongs in it too. It was
refuted the same evening by its own cheapest killer
([R4](../refuted/R4-receiver-mode-is-not-a-shape-variable.md)): the routing policy's reasoning mode
assigns a **work class**, never a shape. The domain of the shape function is unchanged, and the
theory is untouched by the episode except for one thing worth keeping in it —

> A constraint the library cannot express, discovered in a document written without reference to the
> library, is the most flattering possible evidence for this theory. It is therefore the evidence to
> check hardest, and the one time it appeared, it was a misreading.
