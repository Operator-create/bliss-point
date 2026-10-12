# R4 — H10 is dead: reasoning mode assigns a work class, it does not change the brief

**Filed 2026-09-10 at 23:40. Refuted 2026-09-10 at 23:48**, by the fourth of the four killers it
named for itself, before any code was written for it.

## The claim

**H10:** the routing policy's receiver reasoning mode (`/reasoning max` on the Hermes triad,
`/boost` on Antigravity) is an eighth resolution input, composing additively with phase and stakes:

```
profile base  →  + phase  →  + stakes  →  + mode  →  + overrides
```

with one delta vector serving all three triad profiles, because the thing being modelled is a
property of elevated reasoning rather than of `casper`, `balthasar` and `melchior` separately.

## What killed it

Its own killer number four, quoted from the hypothesis as filed:

> **The doctrine is about routing, not shape.** If elevating the mode changes only *which tasks may
> be sent* and not *how they should be phrased*, then it belongs entirely to the harness under D0,
> and Bliss Point should record that and do nothing. This is the cheapest of the four to check and
> should be checked first.

It was checked first, by `balthasar` at `/reasoning max` — which is the joke worth recording, since
the hypothesis was about that flag and the flag was set on the agent that killed it. Every one of
the eight lines in `docs/source/model-routing-policy.txt` mentioning reasoning mode assigns a work
class. The verb is `treat` in every case:

| line | what it does |
|---|---|
| 22 | *"When reasoning mode is below high, **treat** them primarily as fast verification…"* |
| 378 | *"Below high, **treat** the triad primarily as verification and investigation; above, **treat** it as a capable executor."* |
| 132, 160, 374, 536, 577, 597 | the same shape: which class of work may go to which recipient |

Not one prescribes a change to how a brief is phrased. The nearest candidate is line 597 —
*"Address the triad as you would any specialist: with individually testable subtasks and
/reasoning max at the receiver"* — and its shape prescription is **unconditional**. Subtasks always;
mode as well. It never reads "if elevated, then shape differently".

Every line number and both deciding quotes were re-verified against the vendored source before the
refutation was accepted.

## What was actually learned

**The profile key is intact.** `melchior` has one shape and two work classes. What the mode changes
is what may be routed to it, and D0 gave routing to the harness on 2026-08-19.

**There is still a defect, and it is not this one.** Who-to-send-to and what-mode-the-receiver-is-in
are decided in the same act and checked against each other nowhere. A frontier-class task can go to
the triad with the mode unset and nothing notices. That is a harness coupling bug. It is worth
fixing and it is not a Bliss Point feature.

**The cost of being wrong here would have been high**, which is why the hypothesis said so at filing
time: an eighth resolution input touches `resolve()`, every profiles directory's contract, the CLI
and the eval's arm definitions, and cannot be removed quietly once profiles depend on it. Eight
minutes of reading killed it. The rule that made that possible is the one this folder exists for —
name the killer at filing time, and check the cheapest one first.

## The error worth keeping

The original reading was attractive because it would have been **independent corroboration of this
project's thesis**, arriving in a document written without reference to the project. A constraint
the library could not express, discovered in the wild, is the most flattering possible shape for a
finding. That is precisely when to check it hardest — the same lesson as
[F5](../findings/F5-related-provider-code-is-not-a-confound.md), where a convenient conclusion was
reached on the day an experiment died and turned out to be inverted.

Related: [[F8-the-routing-policy-grew-a-recipient-and-a-mode]],
[[F5-related-provider-code-is-not-a-confound]], [[T1-shape-as-a-function-of-recipient]]
