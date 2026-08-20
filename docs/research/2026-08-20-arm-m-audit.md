<!-- Independent audit of arm M by the project's grok consultant, 2026-08-20, briefed with a
     Bliss Point compiled brief (grok / review / high stakes).

     ORCHESTRATOR VERIFICATION: every dial value cited below was re-derived with `bliss dials`
     and is exact - claude/antigravity/codex at implement all match. The audit was adopted in
     full; see Amendment 1 in ../eval-protocol.md. -->

# Arm M audit — Bliss Point eval protocol

Scope: arm M only (`docs/eval-protocol.md` vs `src/blisspoint/brief.py` and shipped profiles). Not a redesign of C vs F.

---

## Conclusion

**Abandon arm M as the experiment's falsifier.** Do not run the cross-role compile. Do not leave `C ≈ M` as the line the claim "dies" on. Do not spend 120 of 480 runs on it.

Current M is not a hard test. It is a cartoon the product is built to beat, scored with a threshold that cannot fire at n=20. Elegance is the reason it is still in the table. That is not a scientific reason.

The matching claim already has a real killer that does not use M: **(C−F) differs across tiers / the 2×2, or the thesis is false** (`eval-protocol.md` §3, §7, §9). The mechanism claim needs a one-dial ablation on continuous metrics, not a fourth renderer costume.

Threat (2) is **not** a contradiction in terms. A gap-free mis-shaped brief can be built. What cannot be built is a *cross-role* M that is both gap-free and information-matched at render time. That is an identification failure, not a construction impossibility. It still kills M *as designed* (researcher brief → executor). It does not kill every wrong-shape comparison.

---

## 1. Threat ranking

Ranked by how badly each wrecks M **as a falsifier** — a test that can honestly make the product lose.

| Rank | Threat | Why it sits there |
|---|---|---|
| **1 — fix first** | **(1) straw man** | A falsifier that can only produce "C wins" is not a falsifier. Current M *is* the absurd case threat (1) names. |
| **2** | **(3) underpowered threshold** | The registered kill rule is arithmetically dead. A dead instrument cannot confirm C>M and cannot underwrite C≈M. |
| **3** | **(2) completeness confound** | Real identification problem for *cross-role* M. Repairable. **Not a contradiction in terms.** |

**Fix (1) first.** You already printed (3) as a known defect (`eval-protocol.md` §7). The unmarked trap is that *powering the current M* produces a significant straw-man win. That is how elegance turns into a headline.

### Why (1) is the worst

M is specified as "a goal-shaped researcher brief sent to an executor, and vice versa" (`eval-protocol.md` 32, 45–50). That is not a hypothetical. Resolved at `phase=implement`:

| | spec | decomp | accept | autonomy |
|---|---|---|---|---|
| `claude` | 0.35 | 0.30 | 0.40 | 0.80 |
| `antigravity` | 0.85 | 0.90 | 1.00 | 0.20 |

L1 on those four dials = **2.30**. `brief.py` then does exactly the cartoon: decomp 0.30 < 0.6 and spec 0.35 < 0.4 → one section titled "Design an approach for: {objective}" (`brief.py` 226–228). Antigravity's own notes say it needs "an engineering task list of modular subtasks, never an abstract problem." C will crush that. It proves "don't send an architecture brief to a 7B frontend engineer," which routing already knew. The dials are not under test.

Invert-every-dial (1−x) and random-point-in-dial-space are the same sin with extra geometry. Some random Ms will be near C; some will be clowns; the mixture is uninterpretable.

### Why (3) is second, not first

You pre-registered `C − M ≥ +15pp` on pass@1 while stating n=20 binary only resolves 25–30pp (`eval-protocol.md` 223–241). The row cannot fire. If you then treat a +12pp directional as "C beat M" you cheated; if you treat it as "C ≈ M, delete the dials" you called a power failure a scientific conclusion. Either way §9's kill condition is costume.

This is a one-row fix. It is not why M is conceptually rotten. **Do not fix (3) and keep (1).** That is how you get a powered demonstration of a straw man.

### Why (2) is not fatal as a contradiction

`brief.py` 4–6 and `architecture.md`: dials decide which sections exist and how they bind; they never invent content. A gap is an empty *field* a dial demanded.

Blocking gaps are only `objective_empty` and `acceptance_missing` when `acceptance_binding ≥ 0.6` (`brief.py` 100–108, 246–254). `subtasks_missing` is advisory.

**Gap-free M is constructible.** Arm F already requires every Task field (`eval-protocol.md` 31, 36–37). Populate the Task to the union of fields any profile in the cell would demand. Then `compile(task, wrong_profile).blocking_gaps == []` and `compile(task, right_profile).blocking_gaps == []`. Shape is which supplied content is *selected and bound*, not whether the Task was empty.

The apparent paradox ("the gaps ARE the dials") confuses the linter with the renderer.

What *is* fatal to M-as-designed: cross-role compile cannot be both gap-free **and** information-matched *in the rendered text*. Researcher dials omit the subtask list even when it sits on the Task (`brief.py` 207–228, the `else` branch). Executor dials include it. C then has more of the Task in the prompt. M loses because it is a poorer information subset, which F was invented to prevent. That is identification, not impossibility.

Where (2) becomes operationally fatal: if "no task authored while looking at the dials" (`eval-protocol.md` 103–104) is read as *sparse* Tasks. A real bug report has no `subtasks` and no `acceptance`. Compile that as antigravity/casper and you get blocking `acceptance_missing`. M then either cannot dispatch or loses for incompleteness. That is a Task-admissibility rule, not a proof that wrong-shape briefs cannot exist.

**Do not force M to be gap-free against the *running* model's profile.** That un-mis-shapes it. Force it gap-free against the *donor* profile, on a union-complete Task. Completeness is matched at the Task, the way F already requires.

---

## 2. Mis-shape rule to implement

**Name: `same-role adjacent donor`.** Not invert, not random, not cross-role tier swap.

If you keep any wrong-shape arm at all — and you should not, as a required falsifier — this is the only rule I would allow.

Reject the four listed options as primary:

| Rule | Why not |
|---|---|
| Swap the two tiers' profiles | This *is* current M. It is (1). |
| Invert every dial (1−x) | Maximum-distance straw man. Same sin, prettier geometry. |
| Random point in dial space | Uninterpretable mix of near-misses and clowns. Some Ms will be C. |
| Adjacent plausible profile (raw) | Right family; too vague to pre-register; `return_contract` would still swap the asked-for artifact. |

**Procedure, concrete enough to code:**

1. Freeze a role class on each eval profile, one line, before tasks exist:
   - `implement = {codex, antigravity, melchior}`
   - `research = {grok, claude, balthasar}`
   - `synthesize = {casper}`
2. For a cell whose C target is T: M's donor is the other profile in the **same role class** with largest L1 on the load-bearing dials for that cell. Never cross role class. If the 2×2 is running, prefer other-family, same size-class.
3. **The pair the product already admits is the test.** Codex notes: "A giant task list micromanaging every coding move wastes what it is good at." Antigravity notes: "Needs an engineering task list of modular subtasks, never an abstract problem." At `implement`:

   | | spec | decomp | accept | autonomy |
   |---|---|---|---|---|
   | `codex` | 0.90 | **0.35** | 0.90 | 0.35 |
   | `antigravity` | 0.85 | **0.90** | 1.00 | 0.20 |

   L1 on those four = **0.85**. Decomposition 0.35 vs 0.90 **crosses the 0.6 render threshold** in `brief.py` 207–228. That is a plausible mis-shape: what a competent person who read "always give agents a task list" would actually send Codex. It is not a researcher goal-abstraction.

4. Swap **only** the load-bearing dials that cell's prediction names (`eval-protocol.md` 45–50):
   - Tier A (small/fast): copy donor's `specificity`, `decomposition`, `acceptance_binding`.
   - Tier B (frontier): copy donor's `autonomy`, `specificity`.
   - Leave the other five dials at C's resolved values.
5. **Keep T's `return_contract`, phase, and stakes.** Wrong artifact schema ("architecture and interfaces" on a bugfix) is not a shape test.
6. Render with `compile(..., overrides=...)` (`compiler.py` 9–17). Log the actual 7-vector in the run file.
7. **Admissibility:** Task enters the corpus only if C and M both have `blocking_gaps == []`. Advisory gaps are a covariate. Fill missing fields once, frozen, identical across arms — the F contract applied honestly.

**What this costs in interpretability.** You can no longer say "we sent `claude.yaml` to the executor." You say "we got the two or three dials we claim are causal wrong, and left the rest right." That is a *narrower* claim, and that is the point. If C still cannot beat that M, those dials are decoration. If it can, you have isolated them. Current M cannot isolate anything.

It also costs the pretty story that M is "the compiler, pointed at the wrong profile." M becomes a constructed point. Publish the vector. Anyone who wants the pretty story is asking to win cheaply.

**Pass/fail:** do not judge any wrong-shape arm on pass@1 as a required row. n=20 binary is the regime you already called directional. If a wrong-shape comparison survives at all, register it on **`scope_violations` and `steps`** (already collected; ~0.65 SD paired at n=20, `eval-protocol.md` 236–238). Predicted direction stays: Tier A, under-specified → more scope drift; Tier B, over-prescribed → more steps / following a bad checklist.

---

## 3. Strongest falsifier that is *not* arm M, at n=20

**One-dial threshold crossing. Call it arm A. Put it in M's slot. Do not run both.**

Same Task, same profile, same five or six dials as C. Flip **one** advertised dial across the actual render threshold in `brief.py` (not a tasteful nudge — a section appears or vanishes):

| dial | threshold | what the brief does |
|---|---|---|
| `decomposition` | 0.6 | subtasks section vs one Task section |
| `specificity` | 0.4 | "Design an approach" vs "Do the following" |
| `autonomy` | 0.6 | "Decisions you own" vs prescribed |
| `acceptance_binding` | 0.6 | criteria inside every subtask vs at the end |
| `verification_rigor` | 0.6 | named command required vs omitted |
| `context_volume` | 0.6 / 0.35 | evidence corpus in or out |

Pair n=20. Metric: `scope_violations` and `steps`. Paired bootstrap median difference; CI must exclude 0 to count. Pass@1 directional only.

**The cell's load-bearing dial, not a tour of seven.** Tier A: `decomposition` across 0.6. Tier B: `autonomy` across 0.6. 20 × 1 extra arm × 2 tiers × 3 trials = **120 runs** — exactly the budget M was going to eat, spent on a test that can kill a named dial.

Why this is harsher on the product than M:

- No completeness confound: one threshold moves; the Task is union-complete.
- No straw man: the brief is still "for" that recipient.
- Attributable: if flipping `decomposition` across 0.6 does nothing to scope or steps, that dial is a named decoration (`dials.py` 16–31, `brief.py` 207–238).
- Power: continuous, n=20, the regime you already trust.
- It attacks the *mechanism*, not a cartoon mismatch.

**Promote the interaction you already registered.** "Tier A vs Tier B (C−F) different in sign or magnitude, or the thesis is false" (`eval-protocol.md` 221) is the matching claim's primary falsifier and does not use M. Rewrite §1 so the claim no longer "dies" on C≈M. §3 already kills the thesis without M.

A second, externally valid alternative if you will spend human time: **M_human** — a competent engineer writes the brief they would actually send, never seeing the dials. C vs that, on steps and scope, n=20. If the compiler cannot beat a competent person without your tool, matching is not a product. This is the "plausible mis-shape" you already suspected was the informative M. It is not arm M; it is an independent control. Do it on the 3-task pilot, not as a fourth full arm, unless ablation is cut.

---

## Attack on keeping M because it is elegant

Elegance is that every arm is `render(same Task, different dials)`. That sentence is doing too much work.

- **C vs F already isolates "shaping vs information."** F is the control the claim needs (`eval-protocol.md` 11–16, 34). Same fields, no matching.
- **The interaction already isolates "matching."** If both tiers want the same shape, the project is a linter with a decorative IR (§3, §9). That test does not require a fourth arm.
- Current M is a third way to say "matching," constructed so matching looks important. That is the opposite of a falsifier.
- Four arms × 2 tiers × 3 trials is 480 runs before family columns. You are paying 25% of the budget for the worst-identified contrast.
- §1's line *"the claim dies if C ≈ M"* overweights M so that a hollow C≫M win can be sold as the thesis. A product that needs that line is not trying to fail.
- The compiler-pointed-at-the-wrong-profile story is marketing. The scientific sentence is "we isolated the dials we claim are causal." Those are different experiments. You do not get both at n=20.

If you keep a wrong-shape comparison at all, it is a *supporting illustration* from the 3-task pilot, scored continuously, built as a near-miss. It is not the fulcrum, and it is not worth 120 eval runs.

**Drop M from the four-arm design. Replace the fourth slot with one-dial ablation.** That is the direct statement.

---

## Strongest supporting evidence

- Your own M definition is the cross-role cartoon (`eval-protocol.md` 32, 45–50).
- Shipped profiles make that jump extreme: `claude` vs `antigravity` at implement, L1 = 2.30 on the four load-bearing dials; renderer emits "Design an approach for: {objective}" (`brief.py` 226–228).
- The informative adjacent pair is already in the repo: `codex` decomp 0.35 vs `antigravity` decomp 0.90 at implement — and both profiles' notes describe that exact disagreement.
- Your own power note: n=20 binary ≈ 25–30pp; 15pp cannot fire (`eval-protocol.md` 223–241). You already marked the row defective.
- Gaps are empty-field demands, not a proof that wrong shape requires missing content (`brief.py` 4–6, 146–275; blocking only at 100–108, 254). Union-complete Tasks are the F contract, not extra work.
- §9 already includes "both tiers prefer the same shape" and "F ≈ C," neither of which is M.

## The counterargument

M as cross-role compile is the interaction illustrated inside one cell: the small model should suffer a goal-brief, the frontier model a checklist. Ablation shows a dial moved; it does not show a recipient-shaped document. A reader will understand "we handed the executor the researcher brief" in a way they will not understand a 7-vector. If you union-complete the Task and score scope/steps, even a large mismatch might be a valid *directional* demo.

That argument buys a blog diagram. It does not buy a pre-registered falsifier. The interaction of (C−F) across the 2×2 *is* that demo, with F as the honest control. Spending 120 runs to reprint the interaction as a cartoon is how elegance eats the budget.

A weaker counterargument: keep M as specified, move the metric to scope/steps, and accept the straw man as "upper bound on matching." An upper bound that the product is guaranteed to clear is not a bound. It is a floor under the win.

## Confidence and what would change it

**0.80** on "do not run M as specified, and do not keep it as the claim's fulcrum."
**0.70** on "replace the fourth arm with one-dial ablation; if a wrong-shape arm survives, it is `same-role adjacent donor` on continuous metrics only."
**0.85** that (2) is not a contradiction in terms.

Would change it:

- A 3-task pilot showing C vs current-M is *not* a blowout on scope/steps (then current M is not a straw man in practice — I would still not register +15pp pass@1).
- Evidence that union-complete Tasks still cannot render M without blocking gaps even after filling every `Task` field (then (2) *is* fatal and you drop wrong-profile compilation entirely, leaving only ablation).
- A decision to raise n to ~60 for a binary M contrast, which would make +15pp real — still would not fix the straw man.
- If the 2×2 family×size design is cut for budget, the interaction test weakens and a *near-miss* wrong-shape arm becomes more load-bearing. That is a reason to *improve* M, not to keep the clown version — and still not a reason to make it the fulcrum.

## Recommended next action

1. **Strike arm M from the four-arm design.** Rewrite §1 so the claim no longer dies on C≈M. Promote "(C−F) differs across tiers / 2×2" to the matching claim's primary falsifier.
2. **Put one-dial ablation (arm A) in M's slot.** Tier A: `decomposition` across 0.6. Tier B: `autonomy` across 0.6. Register on `scope_violations` and `steps`; pass@1 directional.
3. **Strike the C vs M pass@1 required row.** If any wrong-shape illustration remains, it is `same-role adjacent donor` as specified in §2, scored on scope/steps, return_contract held at C, 7-vector logged — and it is a pilot figure, not 120 eval runs.
4. **Task admissibility:** union-complete fields; zero blocking gaps on every arm in the cell, including F and A.
5. Do this as a **visible protocol amendment**, not a quiet repair — matching the spirit of lines 227–229. A pre-registration that silently keeps M because it is pretty is not a pre-registration.

If budget only has room for one extra arm besides C/F/R: **keep ablation, drop M.** That is the choice that is most likely to make the product fail if the dials deserve to fail.
