"""bliss — compile a task into a correctly shaped brief."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from . import __version__
from .compiler import compile as compile_task, cross_family
from .dials import DIAL_NAMES, DIAL_POLES, correlation
from .flat import flat
from .profiles import list_profiles, load_profile, phases, resolve


def _load_task(path: str) -> dict:
    raw = Path(path).read_text()
    return json.loads(raw) if path.endswith(".json") else yaml.safe_load(raw)


def _parse_overrides(pairs) -> dict:
    out = {}
    for p in pairs or []:
        name, _, val = p.partition("=")
        if name not in DIAL_NAMES:
            raise SystemExit(f"unknown dial '{name}'. known: {', '.join(DIAL_NAMES)}")
        out[name] = float(val)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="bliss", description=__doc__)
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compile", help="render a brief for one agent")
    c.add_argument("target")
    c.add_argument("--task", help="path to a task .yaml/.json")
    c.add_argument("--objective", help="inline objective, instead of --task")
    c.add_argument("--phase", default="implement")
    c.add_argument("--stakes", default="normal", choices=["low", "normal", "high"])
    c.add_argument("--set", dest="overrides", action="append", metavar="dial=value")
    c.add_argument("--strict", action="store_true", help="exit 1 if the brief has any gap")
    c.add_argument("--gate", action="store_true",
                   help="exit 1 only on blocking gaps (no objective, or no acceptance "
                        "criteria when the recipient's contract is tight)")

    d = sub.add_parser("dials", help="show the resolved point without rendering")
    d.add_argument("target")
    d.add_argument("--phase", default="implement")
    d.add_argument("--stakes", default="normal", choices=["low", "normal", "high"])

    sub.add_parser("profiles", help="list known agents")
    sub.add_parser("correlate", help="are the dials independent? (D6)")

    f = sub.add_parser("flat", help="render arm F: every field, no recipient (eval control)")
    f.add_argument("--task", required=True)
    sub.add_parser("phases", help="list known phases")

    v = sub.add_parser("validators", help="who may review this agent's work")
    v.add_argument("author")

    args = ap.parse_args(argv)

    if args.cmd == "profiles":
        for name in list_profiles():
            p = load_profile(name)
            print(f"{p.name:<12} {p.family:<10} {p.role}")
        return 0

    if args.cmd == "flat":
        print(flat(_load_task(args.task)), end="")
        return 0

    if args.cmd == "correlate":
        names = list_profiles()
        pts = [load_profile(n).dials for n in names]
        pairs = sorted(correlation(pts).items(), key=lambda kv: -abs(kv[1]))
        print(f"pairwise dial correlation across {len(names)} profiles: {', '.join(names)}\n")
        for (a, b), r in pairs:
            flag = "  <-- moves together" if abs(r) >= 0.9 else ""
            print(f"  {r:+.3f}  {a} / {b}{flag}")
        print("\nA pair at |r| >= 0.9 across profiles written by DIFFERENT people is one dial.")
        print("Across profiles written by one author it is one author's habit. See docs/roadmap.md D6.")
        return 0

    if args.cmd == "phases":
        print("\n".join(phases()))
        return 0

    if args.cmd == "validators":
        eligible = cross_family(args.author)
        print("\n".join(eligible) if eligible else "(none — add a profile from another family)")
        return 0

    if args.cmd == "dials":
        profile, dials = resolve(args.target, phase=args.phase, stakes=args.stakes)
        print(f"{profile.name} · {args.phase} · {args.stakes} stakes\n")
        print(dials.render_table())
        print()
        for n in DIAL_NAMES:
            lo, hi = DIAL_POLES[n]
            print(f"  {n}: 0.0 = {lo} | 1.0 = {hi}")
        return 0

    if not args.task and not args.objective:
        raise SystemExit("give --task <file> or --objective <text>")
    task = _load_task(args.task) if args.task else args.objective
    brief = compile_task(task, args.target, phase=args.phase, stakes=args.stakes,
                         overrides=_parse_overrides(args.overrides))
    print(brief.text)
    if brief.gaps:
        print("\n".join(["", "<!-- gaps ------------------------------------------"]
                        + [f"  - [{g.code}] {g}" for g in brief.gaps] + ["-->"]), file=sys.stderr)
        if args.strict or (args.gate and brief.blocking_gaps):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
