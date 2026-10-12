# F7 — 144 compilations produce 26 briefs

**2026-09-10.** Same measurement as [F6](F6-the-compiler-removed-a-quarter-of-what-it-was-given.md),
different question:
[`lab/measurements/silent_subtraction.py`](../measurements/silent_subtraction.py).

The README sells a gradient — *"there is no small model prompt and big model prompt; it's a
gradient, so the tiers are a point in a seven-dimensional space"* — and `bliss dials` prints two
decimal places. Resolution really is continuous: base dials, plus phase deltas, plus stakes deltas,
plus overrides, all real-valued.

The renderer reads those values only through `>=` comparisons against eleven fixed thresholds. So
the output is a step function, and the question worth asking is not how precise the arithmetic is
but **how often the arithmetic reaches a step.**

| | |
|---|---|
| (profile × phase × stakes) points | 144 |
| distinct briefs produced | **26** |
| `claude`, across all 18 of its points | **1 distinct brief** |
| (profile, phase) pairs where low/normal/high stakes are byte-identical | **31 of 48** |

## The dial that never moves

`escalation_explicitness` is fixed, regardless of phase and stakes, for **7 of 8** profiles:

| | reachable range over all 18 points | renders? |
|---|---|---|
| `grok` | 0.00 – 0.25 | never |
| `claude` | 0.10 – 0.35 | never |
| `antigravity`, `codex` | 0.20 – 0.45 | never |
| `balthasar` | 0.70 – 0.95 | always |
| `melchior` | 0.75 – 1.00 | always |
| `casper` | 0.80 – 1.00 | always |
| `astra` | 0.55 – 0.95 | only at low stakes does it stop |

`_stakes.yaml` adds `+0.15` to this dial at high stakes. Checked exhaustively, that delta **buys an
escalation section for no profile in any phase.** The only stakes-driven crossing anywhere in the
matrix runs the other way: `astra` at *low* stakes loses one. And "high stakes" is exactly the
setting under which an operator would expect stop conditions to appear — which is how F6's safety
stops were lost.

`decomposition` is fixed the same way for 6 of 8 profiles, `autonomy` for 5 of 8.

## What this does and does not say

**A step function is not a flaw.** Prose has a section or it does not; nothing renders 0.55 of an
escalation section. Composing continuous deltas and quantising once at the end is a reasonable
design, and it is what makes `base + phase + stakes + override` associative and cliff-free to reason
about.

The narrower, real criticism is this: **for most (profile, dial) pairs the composition cannot reach
the quantisation boundary, so the deltas are dead weight and the two-decimal display promises a
precision the output does not have.** An operator reading `escalation_explicitness 0.45` on a
high-stakes brief reasonably concludes that some escalation language is present. None is.

**It does not damage the eval.** [`eval-protocol.md`](../../docs/eval-protocol.md) holds phase and
stakes fixed and defines arm A as a one-dial ablation deliberately *across the render threshold*.
That choice is vindicated here rather than undermined: threshold crossings are where the entire
observable effect lives, so they are the only ablation that could have shown anything.

**It sharpens D5 and D6.** `bliss correlate` measured correlation between dial *values*. This
measures dial *effects*, and effects are what an eval can see. A dial whose rendered effect is
constant across every phase and every stakes level, for a given profile, is not an axis for that
profile — it is a profile flag. Of the 24 (profile, dial) cells sampled here, **18 are constant.**

**One author, eight profiles, one task.** The collapse is a property of the shipped profile values,
not a theorem about the design. A profile set clustered near 0.6 would show the opposite. That
caveat is the same one D6 already carries, and it does not go away by being repeated — see
[F9](F9-one-profile-moved-the-whole-correlation-matrix.md) for what a single added profile does to
the other measurement made on this sample.

## What it costs to leave alone

Nothing, until someone tunes a dial, observes no change, concludes the dial does nothing, and merges
it — which is [R2](../refuted/R2-autonomy-escalation-are-one-dial.md) arriving by a new road. The
measurement above is the defence: it distinguishes *this dial has no effect* from *this dial's delta
could not reach its threshold from where this profile starts*.

Filed against [T1](../theory/T1-shape-as-a-function-of-recipient.md), which committed to shape being
"a point in a small number of **continuous** dimensions", and which is now amended. At the output it
is a point in a small number of **boolean** ones, and the continuity lives entirely in the
composition.

Related: [[F6-the-compiler-removed-a-quarter-of-what-it-was-given]],
[[F9-one-profile-moved-the-whole-correlation-matrix]], [[H3-seven-independent-dials]],
[[R2-autonomy-escalation-are-one-dial]]
