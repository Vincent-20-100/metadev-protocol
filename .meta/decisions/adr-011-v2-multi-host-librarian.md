# ADR-011 — v2.0 multi-host + librarian + harness audit

**Date:** 2026-04-17
**Status:** ACCEPTED
**Supersedes:** —
**Complements:** ADR-010 (skills & agents architecture v1.6.0)

---

## Context

The PM.15 caveman audit (7 repos, avril 2026) surfaced three convergent gaps
in the v1.6 template:

1. **Single-host bias.** `CLAUDE.md` is the only agent entry point. Peers in
   the audit corpus (caveman, open-context-council, deepagents) ship
   agents-in-code patterns pointing at Codex (`AGENTS.md`), Gemini CLI
   (`GEMINI.md`), Cursor, Windsurf, Cline. The template cannot be dogfooded
   on any of these hosts today.

2. **Saturated conversational context.** `.meta/references/` grows as audit
   cards, research outputs, and synthesis documents accumulate. Every session
   that needs one of those facts loads the whole file into the main agent,
   even when 15 lines would answer the question. The Karpathy LLM-wiki
   pattern and the EgoVault Knowledge Compiler (3-tier compilation) both
   point at the same fix: a read-only curator that returns extracts.

3. **No deterministic harness benchmark.** Every post-audit discussion
   relied on prose summaries ("looks good," "missing a few things"). There
   was no single number that said the template's harness is well-formed —
   which means drift is invisible until a user complains.

The spec debate (`.meta/debates/debate-2026-04-16-deep-source-gate-hook.md`)
also resolved a fourth question: should a PreToolUse gate hook enforce the
"deep sources via librarian only" convention? Answer: no. Conventions in
CLAUDE.md + the librarian being strictly better than raw reads are enough;
a gate hook is bypassable and punishes edge cases we cannot enumerate.

---

## Decision

**1. Multi-host CI fan-out.**

- `sync-config.yaml` is the host registry. `claude` is `primary: true`
  (source of truth, never overwritten). `codex` and `gemini` are
  `import-stub` targets. Tier 2 hosts (cursor, windsurf, cline) sit
  commented under the active block so enabling one is a one-line edit.
- `scripts/sync_hosts.py` (stdlib + yaml) generates `AGENTS.md` and
  `GEMINI.md` as 4-line @import stubs pointing at `CLAUDE.md`. `--check`
  mode verifies no drift and is wired into pre-commit + GitHub Actions.
- Import stubs are **generated**, never hand-edited. The comment at the
  top of each stub says so.

**2. Librarian agent.**

- Sixth local agent, dual meta + template. Read-only. Cherry-picks
  extracts from `.meta/references/`, `docs/`, and `src/` with confidence
  scoring and `file:line` citations.
- CLAUDE.md gains a convention aiguisee: the conversational agent
  **must not** read `.meta/references/` directly; it delegates to the
  librarian. Gold sources (`CLAUDE.md`, `PILOT.md`, `.claude/rules/`,
  `.claude/skills/`) remain directly accessible.
- Trigger is **Propose**: the user decides before dispatch.

**3. Deterministic harness audit scorecard.**

- `evals/harness_audit.py` scores the repo on 6 categories (Skills,
  Agents, Hosts, Contract, Taxonomy, Safety), 10 points each, 60 total.
- `--self` audits the meta-repo, `--path` audits a generated project.
  `--json` emits machine-readable output for CI.
- Meta-repo invariant: 60/60. Anything less fails the run.

---

## Consequences

- **v2.0 invariants:** 6 agents (added librarian), multi-host stubs
  generated and checked, deterministic scoring gate (60/60).
- **Downstream impact:** external projects upgrading from v1.6 get new
  files (`AGENTS.md`, `GEMINI.md`, `evals/`, `scripts/sync_hosts.py`,
  `sync-config.yaml`, `.claude/agents/librarian.md`), a new pre-commit
  hook (sync-hosts), and one trigger-table row + one convention block
  appended to `CLAUDE.md`. No deletions, no renames.
- **Convention enforcement is behavioral, not mechanical.** The deep-sources
  convention lives in CLAUDE.md; the librarian is attractive because it
  returns curated extracts with citations and confidence, which is
  strictly better than a raw Grep+Read loop. Debate log cited in the
  supersedes chain.
- **Harness audit = canary.** Any future change that degrades skill or
  agent coverage, breaks a stub, or removes a safety script is caught by
  the score dropping below 60.

## Rejected alternatives

- **PreToolUse gate hook** blocking raw reads of `.meta/references/` —
  rejected in debate log (2026-04-16). Bypassable, punishes legitimate
  edge cases, and the librarian's superiority removes the need for
  enforcement.
- **Custom multi-agent harness** (à la deepagents) — rejected. Claude Code
  is already the harness; reimplementing middleware would duplicate what
  the platform provides and lock us out of upstream improvements.
- **Tier 2 hosts (cursor, windsurf, cline) in v2.0** — deferred. We
  cannot dogfood them without installing those IDEs ourselves. The
  commented-out block in `sync-config.yaml` is the onboarding path when
  a downstream user asks.
- **Librarian can modify files** — rejected. Read-only mandate is
  load-bearing: a curator that can write is a second implementation
  agent with unclear scope. Hard rule in the agent definition.
