# Measurements

Scripts that re-derive the numbers quoted in `findings/`. Lab rule 5: a claim you cannot re-derive
is a rumour.

Each one runs against the installed library and the profiles directory in effect, prints its results
and asserts nothing about them. They are instruments, not tests — the tests live in `tests/` and
enforce invariants; these report the state of the world, including when the state of the world has
changed and a finding has gone stale.

| script | finding |
|---|---|
| `silent_subtraction.py` | [F6](../findings/F6-the-compiler-removed-a-quarter-of-what-it-was-given.md), [F7](../findings/F7-the-dials-are-continuous-the-renderer-is-not.md) |
| `f9_null_models.py` | [F9](../findings/F9-one-profile-moved-the-whole-correlation-matrix.md) — three null models for the "any eighth point moves it" objection |

`bliss correlate` re-derives [F9](../findings/F9-one-profile-moved-the-whole-correlation-matrix.md)
against the current profile set; the n=7 comparison needs the profiles as of `HEAD` on 2026-08-23.

**A number here is a property of the profiles installed when it was run.** Adding or editing a
profile changes them, which F9 is entirely about. Re-run before quoting.
