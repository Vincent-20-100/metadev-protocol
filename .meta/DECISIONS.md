# DECISIONS.md — Decision journal

> All structural decisions, including rejected alternatives.
> Format: date — decision — context — alternatives rejected
>
> ADRs being refined are in `.meta/decisions/` before landing here.

---

## 2026-04-01 — Project name: `metadev-protocol`

**Decision:** Repo name `metadev-protocol`, concept named "The Meta Protocol".

**Context:** Tension between `pilot-protocol`, `meta-protocol`, `metadev-protocol`.
"Meta" alone risked confusion with Meta (Facebook) in Google searches.
"Pilot" was too specific to the `.meta/PILOT.md` pattern.

**Rejected:** `pilot-protocol` (too narrow), `meta-protocol` (name collision risk).

---

## 2026-04-01 — `copier` over orphan branches

**Decision:** Template system via `copier` + `copier.yml`.

**Context:** First idea explored with Gemini = orphan Git branches
(`template/quant`, `template/app`). Abandoned during conversation.

**Why orphan branches were rejected:**
- Every improvement to a common hook = cherry-pick on N branches
- `git archive` for extraction is fragile and non-standard
- No mechanism to update already-generated projects

**Decisive advantage of `copier`:** `copier update` propagates template
evolution to existing projects — critical for long-term maintainability.

---

## 2026-04-01 — `pre-commit` over `lefthook`

**Decision:** `pre-commit` (Python ecosystem) for git hooks.

**Context:** Gemini suggested `lefthook` (Go binary). Both do the job.

**Rejected:** `lefthook` — adds a non-Python binary dependency in a Python-only stack.
`pre-commit` installs via uv, consistent with the rest of the stack.

---

## 2026-04-01 — `.meta/scratch/` gitignored, rest of `.meta/` versioned

**Decision:** Selective gitignore on `.meta/`.

**Context:** Tension between "keeping session memory" and "not polluting git history".

**Solution:** Separate ephemeral drafts (`scratch/`) from valuable artifacts
(`PILOT.md`, `sessions/`, `decisions/`). Versioned `PILOT.md` = recoverable context
after `git clone` or machine change.

---

## 2026-04-01 — 4 `copier.yml` profiles (not 3, not 10)

**Decision:** `minimal`, `app`, `data`, `quant`.

**Context:** Discussion on profile granularity. Risk of over-specifying
(one profile per framework) vs under-specifying (everything in minimal).

**Guideline adopted:** One profile = one category of relevant guardrails.
Internal technical differences within a profile (FastAPI vs Django) are managed
in the project's `CLAUDE.md`, not in the template.

---

## 2026-04-02 — CLAUDE.md as law, GUIDELINES.md as mentor

**Decision:** Split project instructions into two files with distinct authority levels.

**Context:** Tension between directive (LLM follows exactly) and advisory (LLM adapts).
Resolved by separation: CLAUDE.md is non-negotiable, GUIDELINES.md is advisory.

**Why not one file:** Too many rules in CLAUDE.md and the LLM ignores them.
Too few and important practices get lost. Two files with different authority
levels give the right balance.

---

## 2026-04-02 — 8 automatisms hard-wired in CLAUDE.md

**Decision:** The LLM applies these behaviors without being asked.

**Context:** The core value of the template is that the LLM manages context
automatically (reads PILOT.md, proposes plans, updates SESSION-CONTEXT.md).
Without hard-wired automatisms, the user must remind the LLM every session.

**Key automatisms:** session start context loading, first-session intro,
plan-before-code, milestone updates, end-of-session context rewrite,
conventional commits, architecture sync, rules + guidelines application.

---

## 2026-04-02 — Skills T1: brainstorm, plan, ship, lint, test

**Decision:** Ship 5 skills with every generated project.

**Context:** Based on Superpowers methodology (130K stars) and gold file research.
Skills are the right layer for workflow — loaded on demand, shared via git.

**Why these 5:** They cover the full session lifecycle (explore → plan → implement → verify → ship).
T2 skills (/spec, /tdd, /review, /debug) deferred to post-MVP.

---

## 2026-04-06 — ADR-008: Settings v2 improvements

**Decision:** Implement 7 improvements to settings.json and template configuration.

**Context:** After auditing Claude Code docs and ecosystem (trailofbits security config,
official feature docs), identified gaps in settings.json and template guidance.

**Changes adopted:**
- `attribution.commit: ""` — suppress Co-authored-by trailer natively (replaces planned pre-commit hook)
- Security deny rules: credentials reads (~/.ssh, ~/.aws, ~/.pypirc), dd blocked. Force push → ask
- SessionStart hook: detect `first_session: true` flag in PILOT.md
- `.claude/rules/` starter files: testing.md + code-style.md (lazy-loaded, reduces CLAUDE.md size)
- Automatism #4 strengthened: "must have proposed a plan and received user approval"
- GUIDELINES.md: documented deferred options (Superpowers, autoDream, memory, plan mode)
- Pre-commit: added check-toml

**Deferred:** enabledPlugins, autoDream, autoMemory, plansDirectory, language setting, AGENTS.md.

---

## 2026-04-06 — ADR-009 direction: universal architecture (brainstorm)

**Decision (draft):** Replace 4 profiles (minimal/app/data/quant) with a single universal
Python template. Optional folders use underscore prefix (`_notebooks/`, `_docs/`, `_config/`).

**Context:** Current profiles mix stack (Python) and purpose (app/data/quant) — two orthogonal axes.
One template per language with universal folders is more flexible and maintainable.

**Key directions:**
- Data tiers: `raw / interim / processed` (not bronze/silver/gold — too Databricks-specific)
- Dormant folders with `_` prefix — visible but clearly inactive, renamed when first used
- Clear .meta vs project separation: ships → project, helps build → .meta
- Temporary generation scripts → always .meta/scratch, never scripts/

**Status:** Brainstorm started, full session needed to finalize. See `.meta/scratch/adr-009-brainstorm.md`.

---

## 2026-04-15 — ADR-010: Skills & agents architecture v1.6.0

**Decision:** Ship 10 skills and 5 agents, dual-maintained meta ↔ template, enforced mechanically by `scripts/check_skills_contract.py` in pre-commit. Fuse `/radar` + `/audit-repo` into `/tech-watch` (sweep + deep modes, shared card schema). Promote 4 ghost agents (`code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst`) to real files, additive to the `superpowers` plugin. Thin `/test` and `/save-progress` under the skill-vs-tool principle.

**Context:** Pre-ship audit (PM.15) found three defects: ghost agent rows referencing non-existent files, fake dogfooding (meta `.claude/` was a subset of template), and ambiguous surface (`/radar` vs `/audit-repo` competing in the slash palette).

**Supersedes:** ADR-006 (v1.0 skill inventory).

**Rejected:** keeping `/radar` and `/audit-repo` separate (rejected — "orthogonal depth axis" claim contradicted by fused card format); deleting the 4 agents (rejected — they cover real workflows devils-advocate does not); shipping agents template-only (rejected — asymmetric meta means the template never gets real use by its own author).

**Full text:** `.meta/decisions/adr-010-skills-architecture.md`

---

## 2026-04-17 — ADR-011: v2.0 multi-host + librarian + harness audit

**Decision:** Ship v2.0 with (1) multi-host CI fan-out — `sync-config.yaml` + `scripts/sync_hosts.py` generate `AGENTS.md` and `GEMINI.md` as auto-regenerated @import stubs pointing at `CLAUDE.md`; (2) a 6th local agent `librarian` (read-only, cherry-picks extracts from `.meta/references/`, `docs/`, `src/` with `file:line` citations and confidence); (3) `evals/harness_audit.py` — a deterministic 6-category scorecard (Skills, Agents, Hosts, Contract, Taxonomy, Safety; 60 pts max) with `--self` and `--path` modes. Meta-repo invariant: 60/60.

**Context:** PM.15 caveman audit surfaced single-host bias (CLAUDE.md was the only agent entry point while peers ship AGENTS.md / GEMINI.md / Cursor / Windsurf / Cline patterns), saturated conversational context (`.meta/references/` files loaded whole when extracts would suffice — same signal as the Karpathy LLM-wiki and EgoVault Knowledge Compiler patterns), and no deterministic harness benchmark (drift invisible until user complaint).

**Complements:** ADR-010.

**Rejected:** PreToolUse gate hook enforcing the deep-sources convention (rejected in `.meta/debates/debate-2026-04-16-deep-source-gate-hook.md` — bypassable, punishes edge cases, and librarian superiority removes the need); custom multi-agent harness à la deepagents (rejected — Claude Code is already the harness, reimplementing middleware locks us out of upstream improvements); tier 2 hosts (cursor/windsurf/cline) in v2.0 (deferred — cannot dogfood without installing those IDEs, commented-out block in `sync-config.yaml` is the onboarding path); librarian with write access (rejected — read-only mandate is load-bearing, otherwise it becomes a second implementation agent).

**Full text:** `.meta/decisions/adr-011-v2-multi-host-librarian.md`
