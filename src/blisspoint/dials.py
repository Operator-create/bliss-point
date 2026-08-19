"""The seven dials.

A "bliss point" is not a bucket, it is a point in a seven-dimensional space.
Every dial runs 0.0 -> 1.0 and each one changes the *shape* of the brief that
comes out the other end, never the content.

The dials are deliberately few. If you cannot explain a new dial's effect on
the rendered brief in one line, it is not a dial, it is a preference.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, fields

#: name -> (meaning at 0.0, meaning at 1.0)
DIAL_POLES = {
    "specificity": ("state the goal, let the agent choose the steps",
                    "prescribe the steps"),
    "decomposition": ("one outcome",
                      "numbered, individually testable subtasks"),
    "acceptance_binding": ("acceptance criteria at the end of the whole task",
                           "acceptance criteria inside every subtask"),
    "autonomy": ("every decision is already made",
                 "the agent owns the design decisions"),
    "context_volume": ("minimum-sufficient handoff, start fresh",
                       "full evidence corpus, continue the thread"),
    "verification_rigor": ("self-report is enough",
                           "named command / screenshot / test evidence required"),
    "escalation_explicitness": ("no escalation path stated",
                                "enumerated escalation triggers"),
}

DIAL_NAMES = tuple(DIAL_POLES)


def clamp(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else round(float(x), 3)


@dataclass(frozen=True)
class Dials:
    specificity: float = 0.5
    decomposition: float = 0.5
    acceptance_binding: float = 0.5
    autonomy: float = 0.5
    context_volume: float = 0.5
    verification_rigor: float = 0.5
    escalation_explicitness: float = 0.5

    def __post_init__(self) -> None:
        for f in fields(self):
            object.__setattr__(self, f.name, clamp(getattr(self, f.name)))

    def shifted(self, deltas: dict) -> "Dials":
        """Apply additive deltas. Unknown keys raise -- typos in a profile are bugs."""
        unknown = set(deltas) - set(DIAL_NAMES)
        if unknown:
            raise KeyError(f"unknown dial(s): {sorted(unknown)}")
        return Dials(**{n: getattr(self, n) + deltas.get(n, 0.0) for n in DIAL_NAMES})

    def as_dict(self) -> dict:
        return asdict(self)

    def render_table(self) -> str:
        rows = []
        for n in DIAL_NAMES:
            v = getattr(self, n)
            bar = "#" * int(round(v * 10)) + "." * (10 - int(round(v * 10)))
            rows.append(f"  {n:<24} {bar} {v:.2f}")
        return "\n".join(rows)


def correlation(points: list) -> dict:
    """Pearson correlation between every pair of dials across a set of Dials.

    D6 asks whether seven dials are seven independent axes. Two dials that move
    together across every profile are one dial wearing two names. This is the
    measurement that settles it -- note that it measures the *profiles supplied*,
    so run it over profiles written by other people before believing it.
    """
    n = len(points)
    if n < 3:
        raise ValueError("need at least 3 profiles to say anything about correlation")

    cols = {name: [getattr(p, name) for p in points] for name in DIAL_NAMES}
    means = {k: sum(v) / n for k, v in cols.items()}

    def corr(a: str, b: str) -> float:
        da = [x - means[a] for x in cols[a]]
        db = [x - means[b] for x in cols[b]]
        num = sum(x * y for x, y in zip(da, db))
        den = (sum(x * x for x in da) ** 0.5) * (sum(y * y for y in db) ** 0.5)
        return 0.0 if den == 0 else round(num / den, 3)

    out = {}
    names = list(DIAL_NAMES)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            out[(a, b)] = corr(a, b)
    return out
