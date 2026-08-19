"""Profile / phase / stakes resolution.

Resolution is deterministic and total:

    profile base dials  ->  + phase deltas  ->  + stakes deltas  ->  + caller overrides

No model is asked what shape it wants. That is the point.

A profiles directory is a complete, self-contained configuration: the profiles plus
`_phases.yaml` and `_stakes.yaml`. It is validated on load and fails once, early, naming
the file and the offending key — a typo must never resolve quietly to the 0.5 defaults.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from numbers import Real
from pathlib import Path

import yaml

from .dials import DIAL_NAMES, Dials

_ENV = "BLISSPOINT_PROFILES"
_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "profiles"

_PROFILE_KEYS = {"name", "family", "role", "dials", "notes",
                 "fresh_conversation_default", "return_contract"}


class ProfileError(ValueError):
    """A profiles directory is malformed. The message names the file and the key."""


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
        raw = yaml.safe_load(fh)
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise ProfileError(f"{path}: top level must be a mapping, got {type(raw).__name__}")
    return raw


def _check_dials(raw, path: Path, where: str) -> dict:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ProfileError(f"{path}: {where} must be a mapping of dial names to numbers")
    unknown = set(raw) - set(DIAL_NAMES)
    if unknown:
        raise ProfileError(f"{path}: {where} has unknown dial(s) {sorted(unknown)}. "
                           f"known: {', '.join(DIAL_NAMES)}")
    for name, value in raw.items():
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ProfileError(f"{path}: {where}.{name} must be a number, got {value!r}")
    return dict(raw)


def load_profile(name: str) -> Profile:
    path = profiles_dir() / f"{name}.yaml"
    if not path.exists():
        known = ", ".join(list_profiles()) or "(none)"
        raise FileNotFoundError(f"no profile '{name}' in {profiles_dir()}. known: {known}")
    raw = _load_yaml(path)

    unknown = set(raw) - _PROFILE_KEYS
    if unknown:
        raise ProfileError(f"{path}: unknown key(s) {sorted(unknown)}. "
                           f"allowed: {', '.join(sorted(_PROFILE_KEYS))}")

    declared = raw.get("name", name)
    if declared != name:
        raise ProfileError(f"{path}: name is '{declared}' but the filename says '{name}'. "
                           "They must match, or omit name entirely.")

    for field_name in ("family", "role"):
        value = raw.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ProfileError(f"{path}: {field_name} is required and must be a non-empty "
                               "string. family decides cross-family validator eligibility, "
                               "so it must never be guessed.")

    fresh = raw.get("fresh_conversation_default", True)
    if not isinstance(fresh, bool):
        raise ProfileError(f"{path}: fresh_conversation_default must be true or false, "
                           f"got {fresh!r}")

    return Profile(
        name=name,
        family=raw["family"],
        role=raw["role"],
        dials=Dials(**_check_dials(raw.get("dials"), path, "dials")),
        notes=tuple(raw.get("notes") or ()),
        fresh_conversation_default=fresh,
        return_contract=tuple(raw.get("return_contract") or ()),
    )


def list_profiles() -> list:
    return sorted(p.stem for p in profiles_dir().glob("*.yaml") if not p.stem.startswith("_"))


def _modifier_table(kind: str) -> dict:
    path = profiles_dir() / f"_{kind}.yaml"
    if not path.exists():
        raise ProfileError(
            f"missing {path}. A profiles directory must be self-contained: the profiles "
            f"plus _phases.yaml and _stakes.yaml. Copy the defaults and edit them.")
    table = _load_yaml(path)
    for key, deltas in table.items():
        _check_dials(deltas, path, key)
    return table


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
