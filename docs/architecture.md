# Architecture

## What this is

A pure function with a linter attached.

```
Task (what you know)  ─┐
profile               ─┤
phase                 ─┼──►  resolve()  ──►  Dials  ──►  render()  ──►  Brief(text, gaps, drops)
stakes                ─┤
overrides             ─┘
```

No model runs. No network call. No state. Same inputs, same brief, byte for byte — which is what
makes the future eval bench meaningful: you can perturb exactly one dial and attribute the
difference.

## Module map

| module | lines | job |
|---|---|---|
| `dials.py` | 100 | the seven axes, clamping, additive shifts |
| `profiles.py` | 158 | load profiles + phase/stakes tables, resolve the point |
| `brief.py` | 461 | `Task` in, brief text, gaps and drops out. The only place shape rules live |
| `flat.py` | 110 | arm F: every field, no recipient. The eval's control |
| `compiler.py` | 41 | `compile()` and `cross_family()` |
| `outcomes.py` | 42 | append-only JSONL log |
| `cli.py` | 128 | `bliss compile / dials / profiles / phases / correlate / flat / validators` |

`brief.py` roughly doubled on 2026-09-10 when drop detection landed, and it is now more than half
the library. The "readable in one sitting" invariant is not broken yet, but that file is the one to
watch: it holds the render rules *and* the check that the render rules lost nothing, and those are
two jobs.

## Why the dials are additive, not a lookup table

A lookup table of (agent × phase × stakes) briefs is 8 × 6 × 3 = 144 templates that drift apart the
moment anyone edits one. Additive deltas mean a phase's meaning is written once — `design` raises
autonomy and lowers specificity *for every agent* — and adding an eighth agent costs one YAML file,
not eighteen.

It also makes the model legible. `bliss dials codex --phase design` shows you the point, and you
can argue with the number.

## Where content comes from

The dials decide which sections exist and how they are bound. They never write content. Everything
in the rendered brief traces to a field you supplied on the `Task`, a `return_contract` from the
profile, or a fixed instruction line. When the resolved point demands a section you left empty, it
is reported as a gap and the section is omitted.

This is deliberate. A prompt compiler that invents acceptance criteria is a prompt compiler that
launders your uncertainty into an agent's confidence.

The mirror rule, added 2026-09-10: it must not silently *remove* content either. A populated field
that the resolved point discards is reported as a drop, naming the dial and the threshold. Every
compiled brief satisfies **emitted ∪ dropped ∪ gapped ⊇ populated**, asserted across all profiles,
phases and stakes levels in `TestNothingVanishes`. Selection is legitimate; silence is not.

## Provenance

`docs/source/` holds the two operational documents the profiles were derived from — a model routing
policy (who gets the work) and an agent prompting protocol (how the work is packaged). They are
preserved verbatim. The profiles are the machine-readable form; when they disagree, the profiles
win, because the profiles are what actually runs.

## Not in scope

Routing, dispatch, sockets, sessions, sandboxes, retries, memory. Bliss Point is a library your
harness calls, in one line, at the moment it is about to send something to an agent.
