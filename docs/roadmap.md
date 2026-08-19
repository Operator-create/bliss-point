# Roadmap

Format: [Wayfinder](wayfinder.md). Nodes are decisions; tickets are CLEAR, DIM or FOGGED; a ticket
is only specified in detail once its parent decision is settled.

**North star:** an operator running several agents reaches for Bliss Point at the moment of handoff,
the way they reach for a formatter before a commit.

---

## D0 — Does Bliss Point own any dispatch?

**SETTLED 2026-08-19** — No. It is a prompt compiler; routing, sockets and sessions stay in the
harness. Settled by the user, directly, against the original multiplexer framing.

Everything below inherits this. A ticket that needs a runtime is out of scope by construction, and
that is the single most useful thing this tree does.

---

## D1 — What surfaces does it ship on?

**OPEN.** Options: pure Python library / + TypeScript renderer / + dsh plugin / all three.

**Settled by:** the antigravity research report — specifically whether dsh's plugin interface can
express prompt shaping (ST1), and whether pi is worth forking, consuming or imitating (ST3).
Dispatched 2026-08-19.

**Provisional lean:** imitate pi's discipline, consume it as an integration target, do not fork —
a fork inherits the agent loop, which is exactly the part Bliss Point does not have.

- **T1.1 — dsh plugin spike.** FOGGED. Blocked on ST1 confirming real extension points.
- **T1.2 — TypeScript renderer over the same YAML/Markdown.** FOGGED. Blocked on D1 and on D4,
  since a template-override system would have to port too.
- **T1.3 — pi integration example.** FOGGED. Cheap if D1 lands on "consume".
- **T1.4 — Publish to PyPI.** DIM. Independent of D1; wants a second opinion on the name first.

---

## D2 — Are the dial values right?

**OPEN**, and openly so — the README says the numbers are calibrated opinion.

**Settled by:** an eval bench that perturbs one dial at a time and scores acceptance-criteria pass
rate against token cost. Until then no benchmark is claimed anywhere in the repo.

- **T2.1 — Outcome log.** CLEAR, done. Append-only JSONL, written from day one.
- **T2.2 — Bench harness.** DIM. One task, N dial perturbations, per-model scoring.
- **T2.3 — Perturbation protocol.** DIM. Which dial, which direction, how many trials to beat noise.
- **T2.4 — Publish results including the ones that contradict the profiles.** FOGGED.
- **T2.5 — Mine the outcome log for shapes that correlate with rework.** FOGGED. Needs volume first,
  which means dogfooding is the prerequisite, not a nice-to-have.

---

## D3 — Do templates override the renderer, or only feed it?

**OPEN.** Today the renderer builds every section in code and the profiles supply only data. The
alternative is per-`(target, phase)` Markdown that replaces the default rendering wholesale.

**Settled by:** the first real case where the code renderer cannot express a shape someone needs.
Not before — this is a decision that should be forced by evidence, not taken on elegance.

**Risk if we get it wrong:** overrides are the obvious path to 126 drifting templates, which is the
exact failure the additive dials were chosen to avoid.

- **T3.1 — Template override loader.** DIM.
- **T3.2 — Section-level overrides instead of whole-brief.** FOGGED. Probably the safer shape, if
  D3 lands on yes.

---

## D4 — Is the gap linter advisory or blocking?

**OPEN.** `--strict` exits 1 today, but nothing forces its use.

**Settled by:** dogfooding. If briefs ship with gaps and the work still lands, it is advice; if
gapped briefs correlate with rework in the outcome log, it becomes a gate.

- **T4.1 — Pre-dispatch hook that refuses a gapped brief.** FOGGED.

---

## D5 — Does `stakes` earn its place?

**OPEN.** It currently moves four dials in a fixed pattern. That may mean it is a real axis, or that
it is two dials wearing a trenchcoat.

**Settled by:** whether any profile ever needs a stakes table that is not a scalar multiple of the
default one. One counterexample settles it.

---

## D6 — Seven dials, or fewer?

**OPEN.** The honest test: if two dials move together across every real profile, they are one dial.

**Settled by:** correlation across profiles once there are enough of them — including profiles
written by other people, which is the part that cannot be faked in-house.

---

## Invariants

Not decisions. These are the constraints every branch above inherits, taken from what makes pi worth
admiring:

- **Readable in one sitting.** If the library stops fitting in a person's head, the design failed,
  and no feature is worth that.
- **No model in the compile path.** Resolution stays deterministic, or the bench means nothing.
- **Never invent content.** A dial that demands input you did not supply reports a gap. Always.
- **Profiles are data.** Anyone can replace the whole set with `BLISSPOINT_PROFILES` and owe us
  nothing.
