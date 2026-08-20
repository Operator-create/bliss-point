> **Orchestrator verification, 2026-08-20.** Archived from codex's Phase 0 probe. Every decisive
> claim below was re-checked against primary source by the orchestrator before acceptance:
>
> - All five repositories exist with the licences and owners stated (`gh api`): `earendil-works/pi`
>   (MIT, ★94,252), `deepseek-ai/deepseek-harness` (MIT, ★171,980),
>   `PrimeIntellect-ai/prime-agent` (MIT, ★17,465), `microsoft/playwright-cli` (Apache-2.0,
>   ★12,683), `NousResearch/hermes-agent` (MIT, ★233,372).
> - **pi**: `packages/ai/src/providers/minimax.ts` at the pinned commit reads
>   `auth: { apiKey: envApiKeyAuth("MiniMax API key", ["MINIMAX_API_KEY"]) }` with **no `oauth`
>   member**; `packages/ai/src/auth/oauth/` contains anthropic, github-copilot, kimi-coding,
>   openai-codex, openrouter, radius and xai — **no minimax**. Confirmed.
> - **dsh**: the quoted limitation is verbatim — *"A provider that authenticates through OAuth
>   alone is not offered"* — and gives the mechanism: pi-ai resolves OAuth from a *stored*
>   credential, and the adapter has no credential store and runs no login flow. Confirmed.
> - **Prime**: `packages/ai/src/utils/oauth/index.ts` exports exactly `anthropicOAuthProvider`,
>   `githubCopilotOAuthProvider` and `openaiCodexOAuthProvider`. **No MiniMax.** Confirmed.
>
> **A note the orchestrator added, then had to retract (2026-08-21).** The report states,
> separately and accurately, that Prime Agent *"began as a hard fork of pi-mono"* and that dsh's LLM
> package is *"pi-ai-backed"*. The orchestrator joined those into a claim that the three harnesses
> were effectively one and that the bake-off grid was therefore confounded. **Pair review by codex
> refuted that**, and the refutation was verified: dsh's `agent-loop` package has eleven
> dependencies and none is pi; dsh owns its prompt assembly, tool mediation and context management;
> the three trees pin different pi-ai versions (0.82.1 / 0.84.2 / 0.7.4). The surviving finding is a
> sampling caveat, not a confound — see
> [F5](../../lab/findings/F5-related-provider-code-is-not-a-confound.md). **Nothing in codex's own
> report was withdrawn.**

# Bliss Point harness bake-off — Phase 0 feasibility report

**Date:** 2026-08-20  
**Scope:** source-only feasibility probe; no package, harness, service, Python environment, browser, or Docker container was installed  
**Binding control:** `bliss-point/docs/harness-bakeoff.md`, sections 2 and 2.1, as supplied in the local pre-registered protocol: every tested cell must use **MiniMax-M3 through MiniMax subscription OAuth**. An API key is recorded only for a possible operator-approved redesign and does not satisfy the control.

## Executive result

**0 GO / 5 NO-GO. No contested Phase 1 cell is feasible under the pre-registered OAuth control.**

Hermes is the only examined harness with a native MiniMax OAuth implementation. DeepSeek Harness, pi, and Prime Agent can reach MiniMax through API-key paths but cannot authenticate to MiniMax the same way Hermes does. Microsoft Playwright CLI is not an agent harness; it is a browser-automation CLI intended to be driven by a separate coding agent.

| hypothesis | call | failed Phase 0 question(s) | decisive reason |
|---|---|---|---|
| H5 — Melchior on DeepSeek Harness | **NO-GO** | Q3 | `minimax_oauth: no`; the generic adapter explicitly does not offer OAuth-only providers |
| H6 — Balthasar on Playwright CLI | **NO-GO** | Q1, Q3, Q4 | category error: Playwright CLI supplies browser commands to another agent and has no model/auth/prompt loop |
| H7 — Casper on Prime Agent | **NO-GO** | Q3; Q4 also has a capability-parity defect | `minimax_oauth: no`; MiniMax is API-key-only, and the sole `ipython` tool is too broad for an internal capability-matched allowlist |
| H8 — Melchior on pi | **NO-GO** | Q3 | `minimax_oauth: no`; MiniMax is API-key-only |
| H9 — Balthasar on DeepSeek Harness | **NO-GO** | Q3 | same failed OAuth control as H5 |

These are “not tested” cells under protocol section 2.1. Substituting an API key would be a protocol change and a metered-cost decision for the Operator, not a Phase 0 workaround.

## Evidence method and pinned sources

Four public repositories were cloned with `git clone --depth 1` into `~/harness-bakeoff` on opserver. Nothing was built or installed. Hermes was inspected only in its canonical laptop source checkout; no Hermes file, identity, profile, or credential was copied to opserver.

| subject | repository and pinned commit |
|---|---|
| DeepSeek Harness | [`deepseek-ai/deepseek-harness@141eb6f`](https://github.com/deepseek-ai/deepseek-harness/tree/141eb6fef83422698aef7a981029e843e8161534) |
| pi | [`earendil-works/pi@cffe4d7`](https://github.com/earendil-works/pi/tree/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f); the former `badlogic/pi-mono` URL currently redirects here |
| Playwright CLI | [`microsoft/playwright-cli@2f85a94`](https://github.com/microsoft/playwright-cli/tree/2f85a94b7b885dbf4a5d34462f253a8746a690c9) |
| Prime Agent | [`PrimeIntellect-ai/prime-agent@f8f0222`](https://github.com/PrimeIntellect-ai/prime-agent/tree/f8f02221eecad192c65324ebba50037505cfdac6) |
| Hermes baseline | [`NousResearch/hermes-agent@a61183b`](https://github.com/NousResearch/hermes-agent/tree/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f), inspected at `/home/conker/.hermes/hermes-agent` on the laptop |

The worker reports Node `v22.22.1`, npm `9.2.0`, Python `3.14.4`, Git `2.53.0`, and Docker `29.7.2`. `uv`, `pipx`, and `gh` were absent from `PATH` at the final probe.

## DeepSeek Harness

### 1. Is it an autonomous agent harness?

**Yes.** The repository calls `dsh` an open-source agent harness in [`README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/README.md). Its one-shot bundle creates a fresh Agent, submits a task, waits for quiescence, and exits; the exact headless command is `dsh --profile headless "task"` in [`packages/bundle/headless/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/bundle/headless/README.md) and [`packages/bundle/headless/src/startup.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/bundle/headless/src/startup.ts). It opens no listening port in headless mode.

### 2. Licence and Ubuntu 26.04 install feasibility

**MIT.** See [`LICENSE`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/LICENSE) and the root [`package.json`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/package.json).

The published path is `npx @deepseek-ai/dsh web`; source development uses `pnpm install`, `pnpm run build`, and `pnpm dsh web`, all documented in [`README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/README.md). The root engine is `node: "^22.19.0 || >=24.0.0"` in [`package.json`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/package.json), so opserver's Node 22.22.1 is compatible. Python 3.14 is not on the normal published runtime path. If a Web UI were ever used, the lab must override the default `3080` to `8081+` and pass `--no-open`; the present headless runner needs no port. **No listed install command was run.**

### 3. MiniMax authentication

`minimax_oauth: no`  
`minimax_api_key: yes`  
`evidence:` The bundled generic adapter uses `providers.<route>.apiKeyEnv`, `api`, `baseURL`, and `models` in [`packages/llm/llm-pi-ai/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/llm/llm-pi-ai/README.md) and [`packages/llm/llm-pi-ai/src/config.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/llm/llm-pi-ai/src/config.ts). It can therefore declare a MiniMax Anthropic-compatible API-key route using `apiKeyEnv: MINIMAX_API_KEY`, `api: anthropic-messages`, and `baseURL: https://api.minimax.io/anthropic`. Decisively, the same adapter's documented limitation says: **“A provider that authenticates through OAuth alone is not offered”** because it has no OAuth credential store or login flow. The base bundle mounts this adapter dormant until an `llm-pi-ai:` settings section supplies profiles; see [`packages/bundle/base/cordis.patch.yml`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/bundle/base/cordis.patch.yml).

The native DeepSeek adapter's `baseURL` and `apiKeyEnv` are not a solution: they select the `deepseek-official` chat-completions adapter and still provide no MiniMax OAuth flow; see [`packages/llm/llm-deepseek/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/llm/llm-deepseek/README.md).

### 4. Verbatim prompt and restricted tools

**Yes at the harness composition layer.** An agent-scoped prompt section with `complete: true` becomes the exact complete prompt after assembly, and `includeRuntimeContext: false` suppresses dynamic additions; see [`packages/core/system-prompt/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/core/system-prompt/README.md). The shipped minimal preset demonstrates both fields and mounts only persistent shell plus `str_replace_editor` in [`apps/cli/config/agent-presets/minimal/agent.cordis.yml`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/apps/cli/config/agent-presets/minimal/agent.cordis.yml).

Tools can be limited by composing only the required tool rows or by agent-scoped `ctx.tools.restrict(filter)` in [`packages/core/tools/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/packages/core/tools/README.md). That README expressly says the restriction is visibility composition, not an authority boundary, so Phase 2 would also need the host sandbox/approval policy to enforce the same filesystem/process/network authority.

**Hypotheses:** H5 **NO-GO**, H9 **NO-GO** — Q3 fails for both.

## pi

### 1. Is it an autonomous agent harness?

**Yes.** Pi describes itself as a terminal coding harness and supports interactive, print, JSON, RPC, and SDK modes in [`packages/coding-agent/README.md`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/coding-agent/README.md). `pi -p "task"` runs a non-interactive task through the coding-agent loop and exits; the CLI mode and tool behavior are documented in the same file.

### 2. Licence and Ubuntu 26.04 install feasibility

**MIT.** See [`LICENSE`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/LICENSE) and [`packages/coding-agent/package.json`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/coding-agent/package.json).

The published install is `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`, with `curl -fsSL https://pi.dev/install.sh | sh` as an alternative, in [`packages/coding-agent/README.md`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/coding-agent/README.md). The package engine is `node: ">=22.19.0"` in [`packages/coding-agent/package.json`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/coding-agent/package.json), so Node 22.22.1 is compatible and Python 3.14 is irrelevant to the standard runtime. **Neither install command was run.**

### 3. MiniMax authentication

`minimax_oauth: no`  
`minimax_api_key: yes`  
`evidence:` The MiniMax provider is hard-wired to `auth: { apiKey: envApiKeyAuth(... ["MINIMAX_API_KEY"]) }` and `baseUrl: "https://api.minimax.io/anthropic"` in [`packages/ai/src/providers/minimax.ts`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/ai/src/providers/minimax.ts). There is no `oauth` member on that provider. The OAuth section in [`packages/ai/README.md`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/ai/README.md) lists subscription/OAuth implementations but does not list MiniMax; the source OAuth implementations under [`packages/ai/src/auth/oauth/`](https://github.com/earendil-works/pi/tree/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/ai/src/auth/oauth) likewise contain no MiniMax module. The model generator recognizes `MiniMax-M3` as a direct MiniMax model in [`packages/ai/scripts/generate-models.ts`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/ai/scripts/generate-models.ts), but only behind the API-key provider. Model identity does not turn the key path into OAuth.

### 4. Verbatim prompt and restricted tools

**Yes, with augmentation explicitly disabled.** `--system-prompt <text>` replaces the default prompt, while `--no-context-files`, `--no-skills`, `--no-extensions`, and `--no-prompt-templates` suppress automatically discovered additions; these flags are in [`packages/coding-agent/README.md`](https://github.com/earendil-works/pi/blob/cffe4d776c8fad2b36b4fe6062ebb72c428e0f0f/packages/coding-agent/README.md). The same file defines `--tools <list>` as an allowlist across built-in, extension, and custom tools, with `--no-tools` and `--no-builtin-tools` as stricter starting points. Phase 2 would still need a captured outgoing request to prove byte identity rather than assume it from CLI semantics.

**Hypothesis:** H8 **NO-GO** — Q3 fails.

## Microsoft Playwright CLI

### 1. Is it an autonomous agent harness?

**No. Category error.** It is a command-line interface to Playwright browser automation. Its own requirements say it needs “Claude Code, GitHub Copilot, or any other coding agent,” and its usage says to point an agent at the CLI; see [`README.md`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/README.md). It maintains browser sessions and performs browser actions, but contains no model provider, prompt assembly, or autonomous LLM loop. It may be a tool *inside* a research harness; it is not the harness being compared.

### 2. Licence and Ubuntu 26.04 install feasibility

**Apache-2.0.** See [`LICENSE`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/LICENSE) and [`package.json`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/package.json).

The documented install is `npm install -g @playwright/cli@latest`; skills are separately added with `playwright-cli install --skills`, in [`README.md`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/README.md). Its engine is `node: ">=18"` in [`package.json`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/package.json), so Node 22.22.1 is compatible. This answers installability of the browser CLI only, not feasibility of H6. **No install command was run.**

### 3. MiniMax authentication

`minimax_oauth: no`  
`minimax_api_key: no`  
`evidence:` [`package.json`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/package.json) declares Playwright dependencies and the `playwright-cli` binary; [`README.md`](https://github.com/microsoft/playwright-cli/blob/2f85a94b7b885dbf4a5d34462f253a8746a690c9/README.md) defines browser commands and requires an external coding agent. There is no model-provider config key, model flag, API-key path, OAuth auth module, or login command because this program does not call an LLM.

### 4. Verbatim prompt and restricted tools

**No as a harness.** It has neither a system-prompt input nor a model-facing tool allowlist. Its CLI commands can be exposed selectively by whichever external coding agent drives it, but that would measure the external harness rather than Playwright CLI.

**Hypothesis:** H6 **NO-GO** — Q1, Q3, and Q4 fail. The hypothesis is dead on arrival as written.

## Prime Agent

### 1. Is it an autonomous agent harness?

**Yes.** Prime Agent describes itself as an RLM-native terminal coding and research harness in [`packages/coding-agent/README.md`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/coding-agent/README.md). It is an independent hard fork of pi and supports bounded unattended execution with `--autonomous` plus turn/token/time/gate limits, documented in the same README and [`packages/coding-agent/docs/usage.md`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/coding-agent/docs/usage.md). The earlier concern that “Prime agent” might only be a compute-provider CLI is not true of this repository.

### 2. Licence and Ubuntu 26.04 install feasibility

**MIT.** See [`LICENSE`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/LICENSE) and [`packages/coding-agent/package.json`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/coding-agent/package.json).

The supported install is `curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh`, documented in [`packages/coding-agent/README.md`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/coding-agent/README.md). The public release is a versioned tarball installed by that script, not the inherited npm package. The package requires Node `>=22.8.0` in [`packages/coding-agent/package.json`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/coding-agent/package.json), so Node 22.22.1 is compatible. [`install.sh`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/install.sh) offers to install `uv`, Python 3.11, `ipykernel`, and the Prime runtime; therefore the system Python 3.14 does not prevent the supported bootstrap, but the bootstrap is an installation and was not run in Phase 0.

### 3. MiniMax authentication

`minimax_oauth: no`  
`minimax_api_key: yes`  
`evidence:` MiniMax maps to `MINIMAX_API_KEY` in [`packages/ai/src/env-api-keys.ts`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/ai/src/env-api-keys.ts) and the provider table in [`packages/ai/README.md`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/ai/README.md). The built-in OAuth registry contains Anthropic, GitHub Copilot, and OpenAI Codex—no MiniMax—in [`packages/ai/src/utils/oauth/index.ts`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/ai/src/utils/oauth/index.ts).

There is an additional model-path mismatch at this commit. The direct `minimax` catalog exposes MiniMax-M2.7 variants, not MiniMax-M3, in [`packages/ai/src/models.generated.ts`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/ai/src/models.generated.ts). MiniMax-M3 is exposed as `minimax/minimax-m3` through `provider: "prime-inference"`, `baseUrl: "https://api.pinference.ai/api/v1"`, authenticated by `PRIME_API_KEY`, in that same generated catalog and [`packages/ai/README.md`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/ai/README.md). OpenRouter and Vercel routes also advertise M3, under their own key paths. None is MiniMax subscription OAuth, and none satisfies section 2.1.

### 4. Verbatim prompt and restricted tools

**Prompt: yes, with additions disabled. Tool-name allowlist: yes. Capability-matched restriction: no, not internally.** `--system-prompt <text>`, `--no-context-files`, `--no-skills`, `--no-extensions`, and `--no-prompt-templates` are documented in [`packages/coding-agent/README.md`](https://github.com/PrimeIntellect-ai/prime-agent/blob/f8f02221eecad192c65324ebba50037505cfdac6/packages/coding-agent/README.md). The same file defines `--tools <list>` and `--no-tools`.

However, Prime Agent's only built-in model tool is `ipython`; the README says the model uses it to read files, run commands, edit code, and inspect data. Allowlisting `ipython` therefore grants several protocol capabilities through one interpreter, and `--tools ipython` cannot separately disable process, filesystem, or network powers. External OS/container sandboxing could impose capability boundaries, but that is not Prime's tool allowlist. This is a second design issue for H7 even if the auth control were later changed.

**Hypothesis:** H7 **NO-GO** — Q3 fails; Q4 also cannot meet the protocol's capability-matched restriction using the built-in allowlist alone.

## Hermes incumbent baseline

### 1. Is it an autonomous agent harness?

**Yes.** Hermes documents coding, research, delegation, tools, sessions, and autonomous/scheduled work in [`README.md`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/README.md). Its CLI parser exposes one-shot `-z/--oneshot`, model/provider overrides, and toolset selection in [`hermes_cli/_parser.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/_parser.py).

### 2. Licence and Ubuntu 26.04 install feasibility

**MIT.** See [`LICENSE`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/LICENSE) and [`pyproject.toml`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/pyproject.toml).

The Linux install is `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` in [`README.md`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/README.md). The project requires Python `>=3.11,<3.14` in [`pyproject.toml`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/pyproject.toml), so opserver's system Python 3.14 cannot be used directly; the supported installer provisions its managed Python/uv environment. Technical installability is not authorization: the standing worker rule explicitly bans installing or recreating Hermes on opserver. The canonical laptop checkout remains the only baseline. No Hermes command or profile was copied to the server.

### 3. MiniMax authentication

`minimax_oauth: yes`  
`minimax_api_key: yes`  
`evidence:` [`hermes_cli/auth.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/auth.py) registers `minimax-oauth` with `auth_type="oauth_minimax"`, MiniMax OAuth portal/inference endpoints, client ID, scope, device-code exchange, token refresh, and runtime credential resolution. The same registry separately defines `minimax` as `auth_type="api_key"` with `api_key_env_vars=("MINIMAX_API_KEY",)` and `MINIMAX_BASE_URL`. [`hermes_cli/status.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/status.py) and [`hermes_cli/web_server.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/web_server.py) give the exact login command `hermes auth add minimax-oauth`. The provider/model selection path uses `provider: minimax-oauth`, and the OAuth catalog contains MiniMax-M3 in [`hermes_cli/models.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/models.py).

### 4. Verbatim prompt and restricted tools

**Role text: supported but normalized/appended. Whole model-facing system prompt replacement: not supported by the inspected CLI path. Toolset restriction: yes.** `agent.system_prompt` becomes `ephemeral_system_prompt` in [`hermes_cli/cli_agent_setup_mixin.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/cli_agent_setup_mixin.py). At request time Hermes joins its cached internal prompt, two newlines, and the ephemeral prompt, then strips the result in [`agent/conversation_loop.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/agent/conversation_loop.py). `--ignore-rules` and `--safe-mode` suppress user/project customizations but do not replace the stable Hermes internal prompt; see [`hermes_cli/_parser.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/hermes_cli/_parser.py) and [`agent/system_prompt.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/agent/system_prompt.py).

The CLI `--toolsets <comma-separated>` option is an allowlist, and `agent.disabled_toolsets` is a hard suppression list. Agent construction passes both to `get_tool_definitions()` in [`agent/agent_init.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/agent/agent_init.py); recursive toolset resolution is in [`toolsets.py`](https://github.com/NousResearch/hermes-agent/blob/a61183b56fdb45b9d2a0f2f6b8482e665ccf702f/toolsets.py).

## NEEDS THE OPERATOR

Under the current 0/5 result, there is no valid external Phase 1 cell and therefore no external OAuth command for the Operator to run. DeepSeek Harness, pi, Prime Agent, and Playwright CLI have no MiniMax OAuth login command in the inspected sources.

Only if a fresh Hermes MiniMax subscription login is required on the **canonical laptop** (never opserver), the human step is:

```bash
hermes auth add minimax-oauth
```

That flow presents the MiniMax authorization URL/device code and requires the Operator to complete subscription login in a browser. A run can then select the source-backed provider/model with `--provider minimax-oauth --model MiniMax-M3`. Do not run a second login merely for this report if the canonical Hermes credential is already valid.

If the Operator elects the API-key fallback, section 2.1 requires moving **every** cell, including Hermes baselines, to one identical key/endpoint/model path. No key acquisition, environment export, or metered call has been performed or pre-authorized here.

## Adversarial protocol review

1. **The current grid is empty, not merely smaller.** All four alternatives fail MiniMax OAuth; H5-H9 are all “not tested.” The only scientifically valid next action under the registered protocol is to stop. An API-key grid is a new operator decision and should be recorded as a protocol amendment before installation.
2. **H6 is a category error.** Playwright CLI can be held constant as a browser tool *within* two actual harnesses, but it cannot occupy a harness cell. A repaired research hypothesis would name the real host harness and vary only its browser seam; that would be a different experiment.
3. **“System prompt byte-identical” is underspecified.** DSH can enforce a complete prompt; pi/Prime replace their base prompts but require all augmentation sources disabled; Hermes appends the role text to a non-removable internal prompt and normalizes surrounding whitespace. The protocol must distinguish a byte-identical **role payload** from a byte-identical **entire model-facing system message**. If it means the latter, the incumbent baseline itself currently fails. Any future Phase 2 should capture the outgoing system-message bytes, hash them, and gate the run before task execution.
4. **The worker policy creates a host confound.** Phase 1 says install on opserver only, while standing policy forbids Hermes on opserver. Running Hermes baselines on the 7.4 GiB laptop and alternatives on the 30 GiB worker changes execution host, tool latency, filesystem, and network path. Even if wall clock remains secondary, task success and step behavior can move. Before an API-key redesign, specify one common execution topology that respects the Hermes ban; do not silently compare local Hermes with server-local alternatives.
5. **Prime's allowlist does not match capabilities.** Its single `ipython` tool bundles file, process, editing, and potentially network powers. `--tools ipython` is a name allowlist, not a capability allowlist. A future H7 needs an external sandbox policy with the same capabilities as the Hermes cell, or it remains tool-confounded.
6. **Editorial defect:** the updated protocol currently has two headings numbered `2.1` (“OAuth specifically” and “The second confound”). Renumber the latter to keep citations unambiguous; this does not affect the decision rule.

## Host integrity and no-install evidence

### Docker before

```text
portainer
pihole
```

### Docker after

```text
portainer
pihole
```

The lists match exactly.

### Protected listeners before

```text
LISTEN 0      200                        0.0.0.0:80         0.0.0.0:*
LISTEN 0      32                         0.0.0.0:53         0.0.0.0:*
LISTEN 0      200                           [::]:80            [::]:*
LISTEN 0      32                            [::]:53            [::]:*
```

### Protected listeners after

```text
LISTEN 0      200                        0.0.0.0:80         0.0.0.0:*
LISTEN 0      32                         0.0.0.0:53         0.0.0.0:*
LISTEN 0      200                           [::]:80            [::]:*
LISTEN 0      32                            [::]:53            [::]:*
```

Ports 80 and 53 remained bound throughout. No server was started; no other port was bound by this work.

### Commands and verification performed

- Read the Phase 0 brief and the binding protocol, including the corrected OAuth-specific section 2.1.
- Connected only with `ssh -o BatchMode=yes -o ConnectTimeout=10 opserver ...`.
- Created only `~/harness-bakeoff` on opserver.
- Ran four source-only shallow clones:
  - `git clone --depth 1 https://github.com/deepseek-ai/deepseek-harness.git ~/harness-bakeoff/deepseek-harness`
  - `git clone --depth 1 https://github.com/earendil-works/pi.git ~/harness-bakeoff/pi`
  - `git clone --depth 1 https://github.com/microsoft/playwright-cli.git ~/harness-bakeoff/playwright-cli`
  - `git clone --depth 1 https://github.com/PrimeIntellect-ai/prime-agent.git ~/harness-bakeoff/prime-agent`
- Used only `git rev-parse`, `find`, `rg`, `sed`, `wc`, `command -v`, `uname`, version queries, `docker ps`, and `ss` for inspection.
- No build, test, package-manager install, login, provider call, model call, browser launch, service start, or Docker mutation was run. Tests were intentionally not run because Phase 0 installs no dependencies and tests were not needed for source-level feasibility.

### Failures inside scope

- The first SSH connection was blocked by the local execution sandbox (`socket: Operation not permitted`). It was retried after the required network approval, using the mandated BatchMode/timeout options, and succeeded. This was not an opserver outage.
- One read-only `rg` inspection had a shell-quoting error and was rerun with corrected quoting; one guessed generated-data path did not exist and the real model catalog/source was then located. Neither failure changed state.
- No harness/runtime failure occurred because no harness was installed or executed.

## Phase 0 gate

**STOP. Do not enter Phase 1 under the current protocol.**

GO: **0**  
NO-GO: **5**
