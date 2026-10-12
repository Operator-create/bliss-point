"""The objection to F9, tested rather than argued.

F9 claims astra's 0.176 mean shift is meaningful because astra occupies a
previously empty corner. The objection: ANY eighth point moves an n=7 Pearson
matrix, so 0.176 may be the ordinary magnitude and the mechanism story decoration.

Control: eighth profiles drawn without reference to astra, then the same
statistic. Two families of draw, because they answer different questions.
"""
import random, statistics, sys
sys.path.insert(0, "src")
from blisspoint import Dials, correlation, list_profiles, load_profile
from blisspoint.dials import DIAL_NAMES

BASE = [load_profile(n).dials for n in list_profiles() if n != "astra"]
ASTRA = load_profile("astra").dials
REF = correlation(BASE)


def shift(eighth):
    new = correlation(BASE + [eighth])
    return statistics.fmean(abs(new[k] - REF[k]) for k in REF)


def summarise(label, shifts):
    shifts = sorted(shifts)
    print(f"{label:<34} n={len(shifts):<4} min {shifts[0]:.3f}  "
          f"median {statistics.median(shifts):.3f}  max {shifts[-1]:.3f}")
    return shifts


print(f"astra's actual mean absolute shift: {shift(ASTRA):.3f}\n")
random.seed(20260910)

# (a) uniform random dials -- the weakest possible null: an arbitrary new point.
a = summarise("uniform random eighth", [
    shift(Dials(**{d: round(random.random(), 2) for d in DIAL_NAMES})) for _ in range(400)])

# (b) resampled from the existing seven, dial by dial -- a plausible new profile
#     that stays inside the region the author already occupies. This is the null
#     F9 actually needs: does a profile from the SAME habits move it as much?
b = summarise("resampled-from-existing eighth", [
    shift(Dials(**{d: getattr(random.choice(BASE), d) for d in DIAL_NAMES}))
    for _ in range(400)])

# (c) the eight hand-plausible profiles the brief asked balthasar for, written
#     here without looking at astra's numbers: recognisable agent archetypes.
HAND = {
    "junior implementer":  dict(specificity=.9, decomposition=.9, acceptance_binding=.9,
                                autonomy=.1, context_volume=.5, verification_rigor=.9,
                                escalation_explicitness=.9),
    "senior architect":    dict(specificity=.15, decomposition=.2, acceptance_binding=.3,
                                autonomy=.95, context_volume=.6, verification_rigor=.3,
                                escalation_explicitness=.15),
    "doc writer":          dict(specificity=.5, decomposition=.4, acceptance_binding=.5,
                                autonomy=.5, context_volume=.8, verification_rigor=.2,
                                escalation_explicitness=.2),
    "security auditor":    dict(specificity=.3, decomposition=.3, acceptance_binding=.6,
                                autonomy=.7, context_volume=.9, verification_rigor=.9,
                                escalation_explicitness=.7),
    "data labeller":       dict(specificity=.95, decomposition=.95, acceptance_binding=.95,
                                autonomy=.05, context_volume=.2, verification_rigor=.6,
                                escalation_explicitness=.4),
    "sre on call":         dict(specificity=.6, decomposition=.5, acceptance_binding=.8,
                                autonomy=.4, context_volume=.85, verification_rigor=.95,
                                escalation_explicitness=.95),
    "product researcher":  dict(specificity=.3, decomposition=.2, acceptance_binding=.4,
                                autonomy=.7, context_volume=.75, verification_rigor=.4,
                                escalation_explicitness=.3),
    "refactor bot":        dict(specificity=.8, decomposition=.7, acceptance_binding=.85,
                                autonomy=.2, context_volume=.3, verification_rigor=.9,
                                escalation_explicitness=.5),
}
print()
hand = []
for name, d in HAND.items():
    s = shift(Dials(**d))
    hand.append(s)
    print(f"  {name:<22} {s:.3f}")
print()
summarise("hand-written archetypes", hand)

for label, dist in (("uniform", a), ("resampled", b), ("archetypes", sorted(hand))):
    pct = 100 * sum(1 for x in dist if x >= shift(ASTRA)) / len(dist)
    print(f"share of {label:<12} eighth profiles that move it AT LEAST as much as astra: {pct:.0f}%")

# The mechanism claim, checked separately from the magnitude claim.
print("\n--- the specific pair F9 rests on ---")
pair = ("decomposition", "context_volume")
print(f"  n=7 r = {REF[pair]:+.3f}")
print(f"  with astra   r = {correlation(BASE + [ASTRA])[pair]:+.3f}")
lows = [p for p in list_profiles() if p != "astra"
        and load_profile(p).dials.decomposition < 0.6]
print("  pre-existing profiles with decomposition < 0.60, and their context_volume:")
for p in lows:
    d = load_profile(p).dials
    print(f"    {p:<12} decomposition {d.decomposition:.2f}  context_volume {d.context_volume:.2f}")
print(f"    astra        decomposition {ASTRA.decomposition:.2f}  context_volume {ASTRA.context_volume:.2f}")
