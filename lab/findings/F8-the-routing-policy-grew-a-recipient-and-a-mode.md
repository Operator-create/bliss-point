# F8 — The source document grew a recipient and a mode, and the mode is not the shaper's problem

**2026-09-10.** The operator supplied two documents this project derives from. Both were compared
against the copies vendored in `docs/source/` on 2026-08-23.

- **`AGENT_PROMPTING_PROTOCOL.docx`** — substantively unchanged. A word-level diff returns only the
  vendoring header and line breaks inside the subtask template.
- **`MODEL ROUTING POLICY - GPT ASTRA EDITION.docx`** — changed twice, and the vendored copy
  predated both.

## Change one: a recipient this library did not have

Added between 2026-08-23 and 2026-09-09. A new tier sits between Antigravity/Hermes and Grok:
**GPT Astra**, "maximum-intelligence generalist / computer operator / 3D & game prototype specialist
/ nuclear security auditor", with an escalation gate, a nuclear-option rule for security audits, and
a mandatory return contract of six items.

This is ordinary derived work and it is done: [`profiles/astra.yaml`](../../profiles/astra.yaml),
labelled calibrated opinion like the rest, and with less behind it than the rest — no brief has been
dispatched to this recipient from this library yet.

It occupies a corner of the dial space nothing else did: `decomposition` 0.20 with `context_volume`
0.95. Every other low-decomposition profile is also low-volume, because until now "don't give it a
checklist" and "don't give it the corpus" travelled together. The consequences of that corner are
[F9](F9-one-profile-moved-the-whole-correlation-matrix.md).

**One rule now contradicts another, and it is recorded rather than resolved.** Astra's family is
`openai`, the same as `codex`, so `cross_family()` makes neither eligible to validate the other. The
routing policy positions Astra as the final adversarial reviewer of everything — including the
production code the policy sends to Codex. Both rules are defensible: same-family review really does
agree with itself too often, and the last auditor really should be the strongest reader available.
The project does not get to have both, and there is no measurement here that settles which to keep.

## Change two: a mode, which I read as a shape variable and which is not one

Edited 2026-09-10. The Hermes triad's brief now depends on a **mode set at the receiver**:

> Cheap models ... should also be able to execute small and medium bounded-scope work **when
> reasoning mode is elevated** (Hermes exposes `/reasoning max` on demand; Antigravity exposes
> `/boost`). When reasoning mode is below high, treat them primarily as fast verification, fast
> bounded investigation, or fast second opinions — not as cost-saving substitutes for difficult
> production engineering.

And, on how the triad should then be addressed:

> Receivers run with `/reasoning max` at the Hermes agent so reasoning mode is elevated for the work
> class. Below high, treat the triad primarily as verification and investigation; above, treat it as
> a capable executor.

I first read this as a direct challenge to the key this library is built on: `compile(task,
target="melchior")` resolves a profile by **name**, so if one recipient has two shapes, the name is
no longer sufficient. Filed as [H10](../refuted/R4-receiver-mode-is-not-a-shape-variable.md), an
eighth resolution input composing like phase and stakes.

**That reading did not survive review, and the document says so plainly.** Every line in
`docs/source/model-routing-policy.txt` that mentions reasoning mode assigns a *work class*, and the
verb is always `treat`:

> **line 22** — "They should also be able to execute small and medium bounded-scope work when
> reasoning mode is elevated (Hermes exposes /reasoning max on demand; Antigravity exposes /boost).
> When reasoning mode is below high, **treat** them primarily as fast verification, fast bounded
> investigation, or fast second opinions"

> **line 378** — "Below high, **treat** the triad primarily as verification and investigation;
> above, **treat** it as a capable executor."

The other six occurrences — lines 132, 160, 374, 536, 577 and 597 — are the same shape. Not one
prescribes any change to how a brief is phrased. The nearest thing to a shape instruction is line
597, *"Address the triad as you would any specialist: with individually testable subtasks and
/reasoning max at the receiver"*, and that prescription is **unconditional**: subtasks always, mode
as well. It is not "if elevated, then shape differently".

So the profile key is intact. `melchior` has one shape and two work classes, and what changes with
the mode is **which tasks may be routed to it**, which D0 gave to the harness on day one. The
correct target for an eighth input was never `resolve()`.

**What is real is a coupling defect, and it belongs to the dispatcher.** The harness can currently
send a frontier-class task to the triad without `/reasoning max` set, and nothing anywhere notices.
Who-to-send-to and what-mode-they-are-in are decided in the same act and are not checked against
each other. That is worth fixing, in the harness, and it is not a Bliss Point feature.

The tempting thing about the original reading is worth naming, because it is why I made it: it
would have been independent corroboration of this project's own thesis, arriving from a document
written without reference to the project. That is exactly the kind of conclusion to distrust on the
day you reach it.

## Also in the diff, and not acted on

A **small/medium gate**: the triad may execute a task only if it touches two or fewer modules, spans
at most one PR, and *every subtask is individually testable*. The first two clauses are routing, and
D0 gave routing to the harness. The third is a compile-time property of the Task in hand, and the
kind of thing the linter already checks for. Not built — a gate that guesses at "individually
testable" from a subtask's prose would be a model in the compile path, which the invariants forbid.

---

**Reviewed 2026-09-10 by balthasar at `/reasoning max`, verdict SURVIVES WITH CORRECTIONS.** The
Astra half stands; the mode half was rewritten above. Its document reading was checked line by line
against the vendored source before being accepted — all eight line numbers correct, both deciding
quotes exact — which is worth recording given that the last load-bearing quote from this reviewer
was fabricated with the right substance.

Related: [[F9-one-profile-moved-the-whole-correlation-matrix]],
[[R4-receiver-mode-is-not-a-shape-variable]], [[T1-shape-as-a-function-of-recipient]]
