"""Profile / phase / stakes resolution.

Resolution is deterministic and total:

    profile base dials  ->  + phase deltas  ->  + stakes deltas  ->  + caller overrides

No model is asked what shape it wants. That is the point.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .dials import Dials

_ENV = "BLISSPOINT_PROFILES"
_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "profiles"


def profiles_dir() -> Path:
    return Path(os.environ.get(_ENV, _DEFAULT_DIR))


@dataclass(frozen=True)
class Profile:
    name: str
    family: str            # model family -- validators must come from a different one
    role: str
    dials: Dials
    notes: tuple = ()
    fresh_conversation_default: bool = True
    return_contract: tuple = ()

    @property
    def id(self) -> str:
        return self.name


def _load_yaml(path: Path) -> dict:
    with path.open() as fh:
        return yaml.safe_load(fh) or {}


def load_profile(name: str) -> Profile:
    path = profiles_dir() / f"{name}.yaml"
    if not path.exists():
        known = ", ".join(sorted(list_profiles())) or "(none)"
        raise FileNotFoundError(f"no profile '{name}'. known: {known}")
    raw = _load_yaml(path)
    return Profile(
        name=raw.get("name", name),
        family=raw.get("family", "unknown"),
        role=raw.get("role", ""),
        dials=Dials(**(raw.get("dials") or {})),
        notes=tuple(raw.get("notes") or ()),
        fresh_conversation_default=bool(raw.get("fresh_conversation_default", True)),
        return_contract=tuple(raw.get("return_contract") or ()),
    )


def list_profiles() -> list:
    d = profiles_dir()
    return sorted(p.stem for p in d.glob("*.yaml") if not p.stem.startswith("_"))


def _modifier_table(kind: str) -> dict:
    path = profiles_dir() / f"_{kind}.yaml"
    return _load_yaml(path) if path.exists() else {}


def phases() -> list:
    return sorted(_modifier_table("phases"))


def resolve(target: str, phase: str = "implement", stakes: str = "normal",
            overrides: dict | None = None) -> tuple:
    """Return (Profile, Dials). Deterministic: same inputs, same point."""
    profile = load_profile(target)
    dials = profile.dials

    ptab = _modifier_table("phases")
    if phase not in ptab:
        raise KeyError(f"unknown phase '{phase}'. known: {sorted(ptab)}")
    dials = dials.shifted(ptab[phase] or {})

    stab = _modifier_table("stakes")
    if stakes not in stab:
        raise KeyError(f"unknown stakes '{stakes}'. known: {sorted(stab)}")
    dials = dials.shifted(stab[stakes] or {})

    if overrides:
        dials = dials.shifted(overrides)
    return profile, dials
