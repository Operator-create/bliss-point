# C2 — pi's "~300 line agent loop" is not accurate

**Confirmed 2026-08-19** by measurement. This corrected a claim we had already published.

`packages/agent/src/agent-loop.ts` is **797 lines**, inside a ten-package monorepo. The *layering*
claim survives — `pi-ai` / `pi-agent` / `pi-tui` are real module boundaries — but the size claim
does not.

**Consequence:** README corrected. Forking pi rejected: a survive/delete map put loop, tools,
sessions, TUI and server in DELETE, leaving over 95% deleted on day one.

**Verified separately via the GitHub API:** pi is MIT, 93,622 stars, 11,586 forks — higher than the
46–65k quoted in secondary press.
