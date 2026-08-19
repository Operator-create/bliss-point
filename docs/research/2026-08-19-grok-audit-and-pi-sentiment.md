<!-- Independent audit + sentiment read by grok, 2026-08-19, briefed with a Bliss Point
     compiled brief (grok / review). Grok did not read the code; this is an audit of the idea.

     ORCHESTRATOR VERIFICATION, 2026-08-19, via the GitHub API:
       - dodo-reach/pi-clarify: CONFIRMED, 169 stars, "rewrite rough prompts into precise
         technical prompts before send". Grok's figure was exact.
       - topic:pi-package: 788 repos, not 802. Same order; the pattern claim stands.
       - earendil-works/pi: 93,622 stars, 11,586 forks, MIT. Grok declined to re-count and
         quoted 46k-65k from press; the real number is higher than either.
     Grok's dial-merge recommendation was tested rather than adopted. See docs/roadmap.md D6
     and `bliss correlate`: one of its two proposed merges is supported, the other is not. -->

# Grok review — Project Bliss Point (idea) and pi sentiment

Sampling window for both questions: 2026-01 through 2026-08-19, with Q2 weighted to the last ~30 days of X/GitHub. Bias stated per question. Observation and inference are labelled. Code was not reviewed; Q1 uses the project's own stated idea (seven dials, gap linter, no runtime) from its project memory and peer briefs, not a source-line audit.

---

## QUESTION 1 — Audit: why Bliss Point fails, and what to add instead of dials

### Conclusion

The dominant failure is not "too many dials" as a catalogue of risks. It is this: **the seven-dial model is an unevaluated taste space that cannot falsify itself, so nobody who already has a working harness will let it sit on the dispatch path.**

The compiler owns no runtime and ships calibrated opinion (the README says so; eval is Phase 2). The claim that matters is that *recipient-shaped briefs change agent outcomes*. Until compile → dispatch → pass/fail exists, the seven axes are a 7-dimensional colour picker. Power users will keep writing AGENTS.md and pi skills. The gap linter is the only piece that could earn a seat at dispatch, and even that is currently a list of English sentences rather than a contract a harness can act on.

The seven-dial assumption deserves the attack. Two pairs are one dial in disguise:

- **acceptance_binding and verification_rigor** both encode "how tightly is done-ness specified." Binding without rigor is theatre; rigor without binding has nothing to check. One dial (contract tightness) with two render effects is enough.
- **autonomy and escalation_explicitness** both encode "how far the agent goes before a human." Escalation is the failure mode of autonomy, not an orthogonal axis.

**specificity** and **decomposition** are correlated in practice (a more specific brief is usually more decomposed) but they are not the same axis; keep both until an eval says otherwise. **context_volume** is a budget, not a shape; it belongs as a constraint on the renderer, not a peer of "what kind of task this is."

That leaves a cleaner 4+1: specificity, decomposition, contract tightness (merge of acceptance + verification), autonomy/escalation (merged), plus context_volume as a budget. Seven is authorial completeness, not independent degrees of freedom.

**Gap linter: hard gate on a few blocking codes, advisory on the rest.** A total hard gate makes the tool unusable for the actual job (a one-line handoff). A total advisory gate makes the load-bearing feature into ESLint-warn, which people ignore. Block on missing objective and on missing acceptance when contract tightness is high. Everything else warns.

**Positioning: "prompt compiler" oversells the dials and undersells the linter.** Compilers have IR, optimisation, and backends. This is a **handoff contract**: typed brief + lint. DSPy already owns "prompt compiler" in the engineering camp. The interesting sentence is not "we compile prompts"; it is "we refuse to dispatch a brief the recipient cannot execute." Call it a **task-contract compiler** or **handoff linter**. Do not add more dials to look more like a compiler.

**Most valuable addition that is not more dials:** a **closed eval loop on two real consumers** (pi and dsh, even 20 tasks): same task, static prompt vs compiled brief, scored by the agent's own acceptance. Second, a **pi package** that injects the brief at handoff — pi-clarify already rewrites prompts in this ecosystem; a compiler that is not a plugin will not be used.

### Strongest supporting evidence (observation)

- Project memory (2026-08-19): bliss point is a point in seven named dials, additive `profile → phase → stakes → overrides`, **no model in the loop**; gap linter "rejects at compile time"; eval bench is **Phase 2**; templates are "calibrated opinion."
- Explicit non-goal: not a multiplexer, owns no dispatch.
- Prior-art check in the same memory: dsh, pi, baryonlabs/pi-agent-harness. None claimed as eval-backed for recipient-shaped prompts.
- Adjacent live product: dodo-reach/pi-clarify (GitHub topic pi-package, 169 stars as of this window) already does "rewrite rough prompts before send" **inside pi**, which is where extension happens.

### Counterargument

A small, deterministic, runtime-free library can be the right first artefact: DSPy was also "opinion then eval." Seven axes may be a useful IR even if some are correlated, the way CSS has overlapping properties. A hard lint gate without eval still prevents the exact failure the author cares about (lazy one-liners producing confident wrong work). "Prompt compiler" is a known category (LLMCompiler, DSPy, promptfoo) and may help GitHub reputation more than "linter."

### Confidence and what would change it

Medium-high on the failure mode (adoption without a score). Medium on which two dials to merge — I have the names and definitions from the idea writeup, not a factorial experiment. Would change: a 20-task A/B on pi showing the seven-point brief beats a static template by a margin larger than noise; or a correlation matrix of dial settings in real logs showing all seven move independently.

### Recommended next action

Do not add dials. Freeze four shape dials + one budget. Give gaps stable codes. Make two codes blocking. Ship a 20-task eval on pi (and dsh if the plugin seam is real) before any positioning push. If a plugin is written, write it for pi's package system, not as a fork of pi.

---

## QUESTION 2 — Sentiment and how people extend pi

### Method (required)

- **Time window:** 2026-01-01 to 2026-08-19; "current" sentiment from ~2026-07-20 to 2026-08-19.
- **Source mix:** X keyword + semantic search (badlogicgames, pidotdev, pi.dev, pi-coding-agent, earendil-works/pi); GitHub topic `pi-package` (802 public repos listed); r/LocalLLaMA threads on Earendil move and OpenClaw; HN on Mario's "I've sold out" post; mariozechner.at and pi.dev news; Pragmatic Engineer interview (Apr 2026).
- **Sampling bias:** English X/GitHub; people who publish extensions and dunk on Claude Code; Mario's own account is over-weighted; silent daily users and non-English communities are **unobserved**. Star counts in secondary press (46k–65k) were **not re-counted from the GitHub API in this pass**. I did not clone pi. I did not measure Discord/HN beyond the linked thread.

If a claim below is only from Mario or from SEO blogs, it is labelled as such.

### Conclusion

Current builder sentiment is **positive and practical, not messianic.** Pi is treated as the default *minimal, provider-stable, self-extensible* harness: four tools, you bring the rest as packages. That is durable. The Apr 2026 Earendil/"sold out" scare was real and has not produced a LibreOffice-style fork that I could see. People are not waiting for more core features; they are **piling Claude-Code-shaped capability back on as extensions** (workflows, sandbox, tasks, MCP, permissions, prompt rewrite). That is the live pattern. Hype is star-count and "destroys OpenClaw" YouTube; durable signal is the pi-package topic and week-of-audit X posts installing real packages.

### Strongest supporting evidence (observation)

**Sentiment, durable**
- Identity: "minimal harness, adapt Pi to your workflow" (pi.dev; Mario 2025-11-30 post). X 2026-08-19: Ryan Lanciaux — does not change tools when models change; considering a multi-agent comms plugin. Same thread: "Everything above the harness is disposable by design."
- Shaw (2026-08-06, 52k views): "It's a good agent harness… pi back on top after months of Hermes dominance." That is scene-insider hype-adjacent; treat as mood, not measurement.
- Pragmatic Engineer (2026-04-29): Pi exists because Claude Code became unpredictable; add as few features as possible. Companies already hiring people whose job is a custom Pi setup (X reply 2026-08-12).
- r/LocalLLaMA (2026-04, Earendil move): mix of "Mario is OSS, MIT, it'll be fine" and "the only decent harness will now be enshittified." **Unobserved:** whether those doubters left.

**Sentiment, complaints (observed, not inferred from README)**
- Earendil move + npm scope `@earendil-works` (pi.dev news 2026-05-07; Mario X 2026-05-07). HN on "I've sold out": Austrian irony, still anxiety.
- Mario X 2026-05-21: foundation dropped sponsorship and GH org access — "end of an era."
- GitHub issue 3151 (2026-04-14): no first-class local-model lifecycle.
- X 2026-08-17 @ctxnn1: built pi-permission-gate because destructive commands must not auto-run.
- X 2026-07-23: pi-codemcp vs pi-mcp-adapter — default MCP path considered inefficient enough to rewrite.
- LocalLLaMA: a Rust rewrite of pi described as cutting off the ecosystem (comment, not verified as a serious fork).

**How people extend it (named artefacts)**
GitHub topic `pi-package` listed **802** public repos (page observed 2026-08-19). High-star examples, not a complete census:

| Artefact | What it adds |
|---|---|
| baryonlabs/pi-agent-harness | One sentence → specialist team, 6 patterns, subagent tool |
| QuintinShaw/pi-dynamic-workflows (~428★) | Claude-style dynamic workflows, worktrees, routing |
| fitchmultz/pi-cursor-sdk, pi-agent-browser-native | Cursor loop / agent-browser as native tools |
| carderne/pi-sandbox | OS sandbox + permission prompts |
| tintinweb/pi-tasks, pi-gitnexus, pi-schedule-prompt | Tasks widget, code graph, cron/heartbeat |
| dodo-reach/pi-clarify | Rewrite rough prompts before send (Bliss Point neighbour) |
| gotgenes/pi-anthropic-auth, patlux/pi-commandcode-provider, iaziz786/pi-cmd-login | Auth and model-provider adapters |
| edgehero/pi-dispatch | Pi as a service: cron, GH/GL triggers, spend cap |
| monotykamary/pi-fabric | Programmable tool/agent runtime |
| k0valik/pi-blackhole | Compaction + observational memory |
| waybarrios/opencode-power-pack | Skills pack targeting Codex/OpenCode/Pi |
| OpenClaw | Downstream product on pi-agent-core (Armin 2026-01-31; PE 2026-04-29) |

This week's X (not just READMEs): pi-smart-notify; pi-video (memgrafter); omp-best-of on Oh My Pi; pi-permission-gate; pi-meta-oauth; @juicesharp/rpiv-todo; luongnv89 `/herdr-agent-comm` for pi+herdr; Doug Lance encoding other-harness workflows as pi plugins.

**Pattern (inference, labelled):** core stays small; the community rebuilds the maximal agent as packages. "No MCP" is a core slogan; the community adds MCP anyway, then optimises it.

**Hype vs durable**
- Durable: four-tool loop, package/extension API, multi-provider, OpenClaw as a real downstream, weekly new packages.
- Hype: star inflation, YouTube "DESTROYS OpenClaw," "coding harnesses are solved," treating 802 topic repos as equal quality (many will be toys).
- Unobserved: MAU, revenue, what fraction of stars are OpenClaw tourists, Discord, whether Earendil has changed licence or telemetry. I did not open those.

### Counterargument

Pi could already be past the "minimal" story: a >90k-line monorepo (reported by a contemporaneous architecture pass, not re-measured here) plus 800 packages is not small for a new user. If Earendil productises, the extension culture could fragment (Oh My Pi, Rust rewrites). Sentiment on X is the loud minority.

### Confidence and what would change it

Medium-high on "positive among builders + extension-first." Would change: GitHub API star/fork time series; a licence or telemetry change from Earendil; a census of actually-installed packages vs repo count.

### Recommended next action for Bliss Point (this question only)

If the compiler wants users, ship as a **pi package** that runs at prompt-send/handoff, next to pi-clarify, not as a Python library people must remember to call. Do not fork pi. Watch Earendil for licence/telemetry; that is the only sentiment landmine still live.

---

## Decisions owned (short)

- **Seven dials:** no. Merge acceptance_binding + verification_rigor; merge autonomy + escalation_explicitness; demote context_volume to a budget. Four shape dials.
- **Gap linter:** mixed — hard gate on missing objective and missing acceptance-when-tight; advisory otherwise.
- **Positioning:** "prompt compiler" is the wrong hill. Handoff contract / task-contract compiler. The linter is the product; the dials are the IR.
