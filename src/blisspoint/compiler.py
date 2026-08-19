"""The one function most callers need."""

from __future__ import annotations

from .brief import Brief, Task, render, wants_fresh_conversation
from .profiles import resolve


def compile(task, target: str, phase: str = "implement", stakes: str = "normal",
            overrides: dict | None = None) -> Brief:
    """Shape `task` for `target`.

    task     -- Task, or a dict accepted by Task.from_dict, or a bare objective string
    target   -- profile name (see `bliss profiles`)
    phase    -- research | design | implement | review | verify | synthesize
    stakes   -- low | normal | high
    overrides-- additive dial deltas, e.g. {"autonomy": -0.2}; use sparingly and say why
    """
    if isinstance(task, str):
        task = Task(objective=task)
    elif isinstance(task, dict):
        task = Task.from_dict(task)

    profile, dials = resolve(target, phase=phase, stakes=stakes, overrides=overrides)
    text, gaps = render(task, dials, profile)
    return Brief(
        text=text, dials=dials, target=profile.name, phase=phase, stakes=stakes,
        gaps=gaps, fresh_conversation=wants_fresh_conversation(profile, dials),
    )


def cross_family(author: str, candidates: list | None = None) -> list:
    """Validators must not share a model family with the author.

    Returns the candidate profiles eligible to review `author`'s work.
    """
    from .profiles import list_profiles, load_profile
    a = load_profile(author)
    pool = candidates if candidates is not None else list_profiles()
    return [p for p in pool if p != author and load_profile(p).family != a.family]
