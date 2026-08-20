> **Orchestrator verification, 2026-08-21.** Codex's adversarial pair review of the orchestrator's
> own F5 inference, requested with the counter-argument spelled out for it. Its verdict — *F5 does
> not survive as written* — was **accepted after independent verification** of every load-bearing
> claim: `dsh/packages/core/agent-loop/package.json` has 11 dependencies and none from pi or
> earendil-works; `dsh/packages/llm/llm-pi-ai/package.json` depends on `@earendil-works/pi-ai`
> `^0.82.1`; pi's own `packages/ai` is 0.84.2 and Prime's is a fork at 0.7.4; Prime's shipped tool
> surface is `ipython` only. All confirmed.
>
> F5 was rewritten and renamed as a result, and three overstatements were removed from the seam
> report. See [F5](../../lab/findings/F5-related-provider-code-is-not-a-confound.md).

# Pair review — F5 and the harness seam inference

**Review date:** 2026-08-21  
**Verdict:** **F5 does not survive as written.** A narrower finding survives: pi, Prime Agent, and
the optional dsh multi-provider adapter contain **related pi-family provider code**, so their auth
results should not be presented as three independent samples of the harness ecosystem. That does
not make them one harness, does not reduce the three pinned implementations to one causal fact, and
does not independently confound a comparison of harness-level behavior.

The Phase 0 decisions remain unchanged: **0 GO / 5 NO-GO hypotheses** is correct. It is a count of
pre-registered cells, not a claim that five independent harnesses failed.

## The three claims

### (a) “pi, Prime Agent and dsh all descend from or embed pi's provider layer”

**Literally defensible only after narrowing “provider layer”; materially misleading in F5's present
use.**

- pi is the upstream implementation inspected at `@earendil-works/pi-ai` 0.84.2.
- dsh's `@deepseek-ai/dsh-llm-pi-ai` adapter depends on
  `@earendil-works/pi-ai` `^0.82.1`. It reuses pi-ai's provider catalog, protocol implementations,
  model descriptors and streaming surface. That is a real embedded dependency, not a naming
  coincidence.
- Prime began as a hard fork of pi-mono and retains the package identifiers, architecture and
  extension model. But its own README immediately adds the omitted qualification: **“it is now
  developed and distributed independently.”** Its repository owns a different `pi-ai` snapshot,
  versioned 0.7.4 at the pin.

Those facts justify **“three related provider implementations”**. They do not justify “three
descendants of one codebase” at the harness level, “three forks,” “one provider layer” in the
singular, or the title “Three of the four harnesses are the same harness.” In particular, dsh is
not a pi fork. It calls pi-ai below a dsh-owned adapter.

The strongest counter-argument is also the correct one: nearly everything the bake-off intended
to vary sits above that adapter in dsh.

| Intended harness variable | dsh ownership at the pinned commit |
|---|---|
| prompt assembly | `@deepseek-ai/dsh-system-prompt`; scoped sections, variables and an assembly waterfall |
| tool mediation | dsh tool registry/restriction and a dsh tool-call scheduler |
| agent loop | `@deepseek-ai/dsh-agent-loop`; no pi-ai dependency in that package |
| context management | dsh inbox, event-sourced session surface, runtime-context and compaction seams |
| provider transport | dsh adapter over `@earendil-works/pi-ai` |

The dsh agent-loop package depends on dsh Agent, LLM, Session, System Prompt, Tools, Scope, Settings
and Cordis packages; it does not depend on pi's coding agent or agent core. The adapter translates
dsh history and tool schemas into pi-ai's context vocabulary, then translates the response stream
back. That is a provider/transport seam, not shared prompt assembly, tool mediation, loop or context
policy.

Prime has genuine harness ancestry from pi, but “same harness” is still too strong. The pinned
Prime tree adds an RLM runtime, persistent IPython kernel, recursive agents, goals, daemon/session
machinery, and an `ipython`-only shipped built-in tool surface. Its current `agent-loop.ts`,
`agent.ts`, system-prompt and compaction files differ materially from the pinned pi files. A
no-index source comparison shows, respectively, 427/260, 129/131, 133/84 and 193/402 inserted/deleted
lines. Those figures do not attribute which fork made each change, but they are enough to reject
identity at the pinned revisions.

**Call on (a):** keep the dependency/lineage fact; delete the harness-equivalence inference.

### (b) “the five NO-GOs are one fact observed three times”

**No. The observations are correlated, but the asserted single root cause is not supported.**

There are three distinct accounting levels:

1. **H5 and H9 are one dsh feasibility finding repeated across two role cells.** Both fail because
   the same dsh adapter cannot provide MiniMax OAuth. The repetition is intentional for the role ×
   harness grid, but it is not two independent auth discoveries.
2. **pi's proximate cause** is its MiniMax provider declaration: `auth.apiKey` resolves
   `MINIMAX_API_KEY`; no MiniMax OAuth implementation is registered.
3. **Prime's proximate cause** is its repository-owned provider/auth snapshot: MiniMax maps to
   `MINIMAX_API_KEY`, while its built-in OAuth registry contains Anthropic, GitHub Copilot and
   OpenAI Codex. Common ancestry makes this omission plausibly correlated with pi's, but Phase 0 did
   not perform history/blame analysis proving that a single inherited change caused both products'
   present decisions.
4. **dsh has an additional, independent adapter-level cause.** Its adapter deliberately constructs
   its pi-ai `Models` collection with no credential store and runs no login flow. Its own limitation
   therefore rejects **every OAuth-only provider**, including providers pi-ai itself can support.
   The dsh README says credentials never enter the collection and the harness passes a resolved key
   as an override. This limitation would remain even if the embedded pi-ai catalog acquired a
   MiniMax OAuth module.

The pinned versions also matter: dsh consumes pi-ai 0.82.1, the pi checkout is 0.84.2, and Prime
owns its 0.7.4 fork. They are related code, not one installed library or one identical registry.

The careful conclusion is:

> The three auth NO-GOs are not independent ecosystem samples. H5/H9 duplicate one dsh result;
> pi and Prime have correlated provider lineage; and dsh adds its own key-only adapter boundary.
> Each of the three named alternatives nevertheless fails the cell feasibility requirement at its
> pinned revision.

“5 of 5 harnesses failed” should indeed never be written, but for more direct reasons than F5 gives:
there were five **hypotheses**, only four alternative products, Playwright CLI was not a harness,
and Hermes passed OAuth. “0 of 5 pre-registered cells was feasible” and “none of the three real
alternative agent harnesses supported the required MiniMax OAuth path” are accurate.

**Call on (b):** reject “one fact observed three times”; retain “correlated, non-independent
evidence,” with H5/H9 explicitly deduplicated for auth prevalence claims.

### (c) “the grid was confounded independently of auth”

**Wrong. Shared lineage is not, by itself, a confound.**

A confound is a second varying cause that tracks the treatment and prevents attribution. A common
provider implementation is a held-common component. If it really were identical across cells, it
would reduce provider-transport noise and make differences in prompt assembly, tool mediation,
loop and context policy easier to attribute to the harness. Related internals can also make a useful
controlled comparison: forks with different tool or loop policies can be cleaner contrasts than
wholly unrelated systems.

The actual limitations are narrower:

- The provider paths are not perfectly common: the pins use different pi-ai versions, dsh wraps
  pi-ai in its own credential/context/stream adapter, and Prime owns a divergent fork. A future run
  would need request capture to decide whether transport differences changed the effective input.
- A whole-harness A/B can attribute an outcome to the **runtime bundle**, not to one mechanism
  inside it. To claim “prompt assembly caused this,” the design would need subsystem instrumentation
  or ablation. That limitation exists even for unrelated harnesses.
- Family-heavy sampling limits **external validity**. Results from pi and Prime should not be
  generalized as three independent architectures or used to estimate ecosystem prevalence.

None of those makes the named grid invalid for its stated whole-harness questions. Most
importantly, H5/H9's role × harness contrast uses **the same dsh treatment across two roles by
design**. Calling that repetition a lineage confound is backwards: it is what permits the
interaction estimate. It also does not involve Prime, and dsh is not a pi harness. At most, one
successful dsh interaction would support a dsh-specific result; “harnesses have shapes” as a broad
law would require replication across more harnesses and roles.

**Call on (c):** delete the auth-independent-confound claim. Replace it with an external-validity
warning and a mechanism-attribution warning.

## Claims to cut or narrow in `F5-three-harnesses-one-provider-layer.md`

- **Line 1:** the title is false. Suggested title: **“F5 — Three candidates use related pi-family
  provider code.”**
- **Lines 18–21:** “three descendants of one codebase” is false for dsh. Say that Prime shares
  harness ancestry, while dsh embeds pi-ai only at its LLM seam.
- **Line 28:** “forks of a common core” is false for dsh.
- **Lines 34–43:** replace the single-root-cause account with the correlated-evidence statement
  above. Do not say “one provider layer.”
- **Lines 47–50:** delete “one genuinely uncorrelated contrast,” “any single pi-descendant,” and
  “replication ... at 3× the price.” The three harnesses expose meaningfully different treatments.
  H5/H9's dsh repetition is necessary for the planned interaction.
- **Line 52:** obsolete because Phase 1 is closed; even prospectively, cost should follow the
  hypotheses and precision target, not collapse to one cell merely because provider code is
  related.

The finding can survive only after changing its type: it is a **sampling/generalization caveat**,
not a refutation of the bake-off design.

## Overstatements in `harness-seams.md`

### Lineage and framing

- **Lines 4–6:** remove “the grid turned out to be confounded independently.” It did not.
- **Lines 18–23:** the table should say:
  - pi: inspected upstream harness and pi-ai 0.84.2;
  - Prime: independently developed hard fork of pi-mono, retaining harness ancestry;
  - dsh: independent harness whose optional generic LLM adapter depends on pi-ai 0.82.1;
  - Hermes: separate implementation and the only inspected harness with native MiniMax OAuth.
- Delete “three of four are one family” and “two designs, not four.” There are at least three
  materially distinct harness designs among Hermes, dsh, pi and Prime. Provider lineage is a
  separate axis.

### dsh “strongest hosting seam”

The source supports a narrower and still valuable claim:

- `ctx.systemPrompt.section()`, scoped registration, the assembly waterfall and reversible Cordis
  teardown provide a **documented source-level prompt-injection API without a core patch**.
- A `complete: true` section is restored as the sole prompt section after the waterfall.
- runtime-context suppression removes dsh's separately injected context snapshots.

It does **not** yet support “byte-identical prompt channel” without qualification. `renderPrompt()`
still interprets strict `{{variable}}` groups, drops empty sections and renders the section before
the adapter places the string into pi-ai's `systemPrompt` slot. pi-ai then performs
provider-specific wire serialization. No outgoing request was captured in Phase 0. The precise
claim should be:

> dsh exposes the most explicit **source-level complete-prompt injection seam among the inspected
> candidates**. It can suppress other dsh prompt sections and runtime contexts without a core
> patch. Wire-level byte identity remains an execution gate and must be demonstrated by capturing
> the outgoing request.

“Strongest” is acceptable only with that scope and criterion. “dsh is the adoption target” is too
strong after a source-only probe that did not install, run, test the wire, or satisfy the required
auth path. Say **“dsh is the leading candidate for a future prompt-seam prototype if its auth and
egress gates are separately solved.”**

### pi

The flags and suppression controls were verified in source/documentation, but “reconfirms pi as the
right harness” outruns Phase 0. Keep **“pi has the most directly exposed CLI control surface among
the inspected candidates.”** Make selection conditional on a pinned-version smoke test and captured
outgoing system message. The existing caveat at lines 58–60 is correct and should govern the
recommendation rather than follow an unconditional one.

### Prime

The shipped built-in tool finding is supported: `ToolName` is only `"ipython"`, and that interpreter
bundles filesystem, process and likely network capability. Narrow lines 67–71 to **“Prime's shipped
built-in allowlist cannot subdivide ipython's capabilities.”** “Containment would have to come from
outside the harness” is too absolute: a custom extension might provide narrower tools while
`ipython` is disabled, but Phase 0 did not evaluate or prove that route. The supported statement is
that capability parity needs an external sandbox or separately verified custom tools; it is not
available from the shipped `--tools ipython` configuration alone.

The MiniMax-M3/Prime Inference serving-path warning is supported.

### Playwright CLI and the final takeaways

The Playwright category correction is supported as written.

Keep the allowlist-versus-authority warning. Replace the lineage takeaway with:

> Record provider and harness lineage separately. Related provider code makes auth-support results
> correlated and limits ecosystem generalization; it does not make the harnesses identical or
> automatically invalidate a whole-harness contrast.

## Evidence used

Pinned source-only checkouts, with no package installation or execution:

- DeepSeek Harness `141eb6fef83422698aef7a981029e843e8161534`
- pi `cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f`
- Prime Agent `f8f02221eecad192c65324ebba50037505cfdac6`

Load-bearing paths:

- `dsh/packages/llm/llm-pi-ai/package.json`: pi-ai dependency and adapter identity
- `dsh/packages/llm/llm-pi-ai/README.md`: provider reuse, dsh credential boundary, no credential
  store/login, request adaptation
- `dsh/packages/core/agent-loop/package.json` and `src/`: dsh-owned loop and dependencies
- `dsh/packages/core/system-prompt/src/index.ts`: complete-section enforcement and rendering
- `pi/packages/ai/src/providers/minimax.ts`: API-key-only MiniMax declaration
- `prime/packages/coding-agent/README.md`: hard-fork lineage, independent development, RLM/IPython
- `prime/packages/ai/src/utils/oauth/index.ts`: repository-owned built-in OAuth registry
- `prime/packages/coding-agent/src/core/tools/index.ts`: shipped `ipython`-only built-in surface

No finding in the Phase 0 seam report needs to be withdrawn. The correction is to the later causal
and experimental-design inference layered on top of those findings.
