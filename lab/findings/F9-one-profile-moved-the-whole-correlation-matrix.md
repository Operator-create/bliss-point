# F9 — A profile in an empty corner moved the D6 matrix by 0.18; a profile like the others cannot

**2026-09-10.** `bliss correlate` before and after
[`profiles/astra.yaml`](../../profiles/astra.yaml) was added. Nothing else changed.

| pair | n=7 | n=8 | shift |
|---|---|---|---|
| `specificity / verification_rigor` | **+0.978** | +0.754 | −0.224 |
| `acceptance_binding / verification_rigor` | **+0.921** | +0.796 | −0.125 |
| `autonomy / verification_rigor` | −0.898 | −0.637 | +0.261 |
| `decomposition / context_volume` | +0.773 | +0.183 | **−0.590** |

Mean absolute shift across all 21 pairs: **0.176**. Three pairs crossed the |r| ≥ 0.9 line that
`bliss correlate` prints as *"moves together"*: the audit's one surviving merge candidate
(`acceptance_binding / verification_rigor`), the tightest pair in the matrix and one nobody
predicted (`specificity / verification_rigor`), and `specificity / autonomy`, which crossed *into*
the band from −0.888 to −0.915.

## Why it matters

An external audit read the n=7 matrix and recommended two merges:
`acceptance_binding + verification_rigor`, and `autonomy + escalation_explicitness`. The second was
killed by measurement at r = −0.632 ([R2](../refuted/R2-autonomy-escalation-are-one-dial.md)). The
first was **supported at +0.921** and left standing, unmerged, only because
[D6](../../docs/roadmap.md) refused to act on a matrix with one author behind it.

That refusal now has a number. One profile — an eighth, from the same source — drops that pair to
+0.796. Had the merge been taken on the n=7 evidence, a single new profile would have unmade it.
The same profile drops `specificity / verification_rigor`, the tightest pair in the matrix, from
+0.978 to +0.754. That pair was never an audit merge candidate; the roadmap records it as the one
nobody predicted, which is why it is quoted here as a second, independent instance rather than as a
second recommendation overturned.

## Why the shift is this large, tested rather than asserted

The obvious objection is that **any** eighth point moves a seven-point Pearson correlation, so 0.176
is arithmetic wearing the costume of a discovery. That objection was put to an adversarial reviewer
and tested twice, independently, with different synthetic eighth profiles. Both runs say the same
thing: the magnitude is ordinary, and the mechanism is not.

| eighth profile drawn as | median mean-shift | moves it at least as much as `astra` |
|---|---|---|
| uniform random over the dial space | 0.133 | 20% |
| resampled dial-by-dial from the existing seven | 0.091 | **1%** |
| hand-written agent archetypes (junior implementer, SRE, doc writer, …) | 0.091 | **0 of 8** |
| reviewer's 13 candidates: 8 midpoints of existing pairs, 5 corner-occupiers | 0.023 | 2 of 13, **both corner-occupiers** |

So `astra`'s 0.176 is unremarkable against an arbitrary point and extreme against a plausible one.
A profile drawn from the habits already in the set beats it about 1% of the time. The two synthetic
eighths that do match it are the two the reviewer built to occupy empty corners.

The per-pair result is sharper still. Of the reviewer's 13 candidates, **12 leave
`decomposition / context_volume` between +0.728 and +0.827**, where the n=7 matrix put it. The one
that collapses it to +0.183 is `corner_low_decomp_high_volume`, which is `astra`'s corner by
construction.

`astra` is the first profile with **low `decomposition` and high `context_volume`** at once — 0.20
against 0.95, where `claude` sits at 0.30/0.50, `codex` at 0.35/0.35 and `grok` at 0.10/0.20. "Do
not hand it a checklist" and "do not hand it the corpus" had happened to travel together across all
seven profiles. They travel together no longer.

So the honest reading is not "correlations are noisy", and it is also not "one profile moved it by
0.176". It is: **the n=7 matrix was fitted to a hull with an empty corner, it does not generalise
outside that hull, and the first profile to occupy the corner removed the correlation.** That is the
precise condition under which a correlation from a small hand-authored sample should not be
believed, and D6 had guessed it correctly without being able to show it.

## What it does not license

It does not show the dials are independent. It shows this *measurement* of independence is unstable
at n=8, in a direction that happens to favour keeping seven dials — which is the direction this
project would prefer, and therefore the one to be most suspicious of. `astra`'s values are ones a
Bliss Point author chose, on the same day, having read F6 and F7. The D6 settlement condition is
unchanged and still unmet: **the matrix computed over profiles written by other people**, or an
ablation showing that perturbing two "separate" dials produces indistinguishable outcomes.

Re-derive: `bliss correlate`, and `git show HEAD~1:profiles` for the n=7 set. The null-model runs
are `lab/measurements/f9_null_models.py`.

---

**Reviewed 2026-09-10 by balthasar at `/reasoning max`, verdict SURVIVES WITH CORRECTIONS**, and
the corrections are applied above. Two were its own and one was mine to begin with:

- **The headline named the number, not the cause.** Corrected: the title, the mechanism section and
  the null-model table now say corner occupancy, because without it the finding generalises into a
  claim about statistical instability that neither test supports.
- **"Both of the audit's merge candidates" was wrong.** `specificity / verification_rigor` was never
  an audit merge candidate — the roadmap records it as the pair nobody predicted. One audit
  candidate fell out of range, alongside one unpredicted pair. Corrected here, in `roadmap.md` D6
  and in `H3`.
- Its 13-candidate test and my three null models were built independently and agree. Every number
  in its report was re-run before any of this was accepted.

Related: [[F8-the-routing-policy-grew-a-recipient-and-a-mode]], [[H3-seven-independent-dials]],
[[R2-autonomy-escalation-are-one-dial]]
