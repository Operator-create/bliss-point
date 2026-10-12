# H3 — The seven dials are seven independent axes

**Status: OPEN, with one measurement already against it.** Test: `bliss correlate`, plus the arm A
ablation.

**Killed by:** two dials moving together across profiles written by *different people*, or an
ablation showing a dial's threshold flip changes nothing measurable.

**Current evidence (2026-08-19, n=7, single author — measures the author's habits):**
`specificity / verification_rigor` +0.978, `acceptance_binding / verification_rigor` +0.921. Both
are candidates for merging. Nothing merged yet; see refuted/R2 for what this evidence already
killed.

**Update 2026-09-10 — the evidence above is unstable outside the hull it was fitted to.** Adding
one profile (`astra`) moved the matrix by a mean of 0.176, dropping the audit's one surviving merge
candidate out of merge range (`acceptance_binding / verification_rigor` +0.921 → +0.796) along with
the tightest pair in the matrix, which nobody predicted (`specificity / verification_rigor`
+0.978 → +0.754). Adversarial review established that this is **not** generic small-sample noise: a
profile resampled from the existing seven matches that shift about 1% of the time, and 12 of 13
synthetic eighths leave `decomposition / context_volume` where n=7 put it. The cause is occupying a
corner of the dial space the first seven profiles left empty. Still OPEN, still nothing merged, and
the reason not to merge is now measured rather than argued.
[F9](../findings/F9-one-profile-moved-the-whole-correlation-matrix.md).

A second, independent line of evidence also arrived and points the other way:
[F7](../findings/F7-the-dials-are-continuous-the-renderer-is-not.md) shows that 18 of 24 sampled
(profile, dial) cells have a **constant rendered effect** across every phase and stakes level. A
dial whose effect never varies for a given profile is not an axis for that profile, whatever its
correlation with the others. Correlation of values and constancy of effects are different questions,
and this hypothesis has so far only been tested on the first.
