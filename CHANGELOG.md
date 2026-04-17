# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).
This project uses [semantic versioning](https://semver.org/).

---

## [v2.0.0] — 2026-04-17 — Multi-host + Librarian + Harness audit

Major release. ADR-011 complements ADR-010.

### Added
- **Librarian agent** (6th local agent, dual meta + template) — read-only curator for `.meta/references/`, `docs/`, `src/`. Returns extracts with `file:line` citations and confidence scoring.
- **Multi-host CI fan-out:**
  - `sync-config.yaml` — host registry (`claude` primary, `codex` + `gemini` import-stubs, tier 2/3 commented)
  - `scripts/sync_hosts.py` — stdlib + yaml, idempotent, `--check` mode for CI
  - `AGENTS.md` + `GEMINI.md` — 4-line auto-generated @import stubs pointing at `CLAUDE.md` (never hand-edited)
  - `.github/workflows/sync-hosts.yml` — CI job failing on stub drift
  - `sync-hosts` pre-commit hook
- **`evals/harness_audit.py`** — deterministic 6-category scorecard (Skills, Agents, Hosts, Contract, Taxonomy, Safety; 60 pts max). Modes: `--self` (meta) and `--path` (generated project). Emits text or `--json`.
- **Convention aiguisee in CLAUDE.md** — deep sources (`.meta/references/`) must be accessed via the librarian, not by the conversational agent directly. Gold sources remain directly accessible.
- **ADR-011** — `.meta/decisions/adr-011-v2-multi-host-librarian.md`.
- **Tests:** `TestMultiHost` (generated-project stubs), `TestHarnessAuditSelf` (meta scores 60/60), `tests/test_sync_hosts.py`.

### Changed
- **Trigger tables (meta + template)** — librarian row added.
- **`TestAgents.EXPECTED_AGENTS`** — 5 → 6.
- **Pre-commit** — new `sync-hosts --check` hook fires on changes to `.claude/skills/`, `.claude/agents/`, `CLAUDE.md`, or `sync-config.yaml`.

### Migration v1.6.0 → v2.0.0
- New files: `AGENTS.md`, `GEMINI.md`, `evals/`, `scripts/sync_hosts.py`, `sync-config.yaml`, `.claude/agents/librarian.md`, `.github/workflows/sync-hosts.yml`.
- `CLAUDE.md` gains a librarian trigger row and a deep-sources convention block.
- `.pre-commit-config.yaml` gains the `sync-hosts` hook.
- No files deleted, no renames. `copier update` is additive.

---

## [v1.6.0] — 2026-04-15 — Skills architecture overhaul

Structural release. ADR-010 supersedes ADR-006.

### Added
- **`scripts/check_skills_contract.py`** — pre-commit hook asserting every trigger-table row maps to a real artifact. Default mode checks template-only; `--strict` also enforces meta ↔ template full parity.
- **Meta `.claude/settings.json`** — committed session settings for the meta-repo. Dogfooding is now explicit, not aspirational.
- **Meta `.meta/GUIDELINES.md`, `.claude/agents/`, `.claude/rules/`** — meta now mirrors the template's full `.claude/` tree.
- **4 new local agents shipped in both meta and template:**
  - `code-reviewer` — post-implementation review, tiered CRITICAL/WARN/NIT, distinct from devils-advocate
  - `test-engineer` — generative test author, not a runner
  - `security-auditor` — OWASP sweep scoped to touched code
  - `data-analyst` — audits statistical claims, pipelines, metrics
- **`/tech-watch` unified skill** — fuses `/radar` (sweep) and `/audit-repo` (deep) into a single skill with a shared card schema at `.meta/references/research/`.
- **`scripts/tech_watch/` package** (dual meta + template) — `sweep/` submodule (ex-radar) and `deep.py` module (ex-audit_repo), dispatched from `__main__.py` based on whether a URL is passed.
- **`scripts/save_progress_preflight.py`** — deterministic 5-check block for `/save-progress`, replacing inline skill work.
- **Tests:** `TestMetaParity` (skills, agents, rules, settings, guidelines), `TestAgents`, `TestTechWatchYAGNI`.
- **ADR-010** — `.meta/decisions/adr-010-skills-architecture.md`.

### Changed
- **Trigger tables (meta + template) rewritten:**
  - 4 ghost agents that previously advertised unshipped functionality are now real and invocable
  - `/radar` and `/audit-repo` rows collapsed into a single `/tech-watch` row
- **Superpowers framing** — the "Recommended plugin" section now states explicitly that the 8 local workflow skills are fallbacks (work out-of-the-box) and that superpowers ships superior versions; the 4 local agents are additive, not fallbacks.
- **`/test` and `/save-progress`** thinned under the skill-vs-tool filter.
- **ADR-006 superseded** by ADR-010 (v1.6.0 skills inventory: 10 skills + 5 agents, dual-maintained).

### Removed
- `/radar` skill (absorbed into `/tech-watch` sweep mode) and `template/scripts/radar/` package.
- `/audit-repo` skill (absorbed into `/tech-watch` deep mode) and `scripts/audit_repo/` (meta).
- `scripts/tech_watch.py` — legacy v1.0 orphan, superseded by the new package at the same directory name.

### Migration notes (v1.5.0 → v1.6.0 via `copier update`)
- `/radar` invocations become `/tech-watch` (no args = sweep, same behavior).
- `/audit-repo <url>` becomes `/tech-watch <url>` (deep mode).
- Card output path is unchanged: `.meta/references/research/`.
- `[project.optional-dependencies] radar` renamed to `tech-watch` in `pyproject.toml`.
- 4 new agents appear under `.claude/agents/` — nothing to migrate.

---

## [v1.2.0] — 2026-04-13 — Research skill, vision skill, audit-repo skill, tech watch, prose absorption

### Added
- **New skill: `/research`** — external research with WebSearch + WebFetch + MCP. 7-step process with 8-call soft budget. Structured output to `.meta/references/raw/`. Strict orthogonality with `/brainstorm`. Shipped in template + skills-pack.
- **New skill: `/vision`** — guided 4-question dialogue filling the Vision section in PILOT.md (Problem / Target user / V1 scope / North star). Auto-proposed at first session when section is TBD. Re-invocation mode supports per-field update. Shipped in template + skills-pack.
- **New skill: `/audit-repo`** — standardized structural analysis of any GitHub repository (meta-repo only). Shallow clone → fingerprint → 5 fixed categories → tiered recommendations (USE AS-IS / EXTRACT PARTS / BORROW CONCEPTS / INSPIRATION / REJECT). Output to `.meta/references/interim/`. Enables PM.4 multi-agent synthesis.
- **Tech watch script** (`scripts/tech_watch.py`) — stdlib-only GitHub Search API script querying 6 AI-coding topics with SHA256 dedup cache. Output to `.meta/references/raw/`. Requires `GITHUB_TOKEN` in `.env`.
- **Vision section in PILOT.md template** — 4 subsections with `_TBD_` placeholders, auto-detected by first-session automatism.
- **Three pillars** in `docs/PHILOSOPHY.md` — product excellence / technical agility / AI intensity.
- **Engineering defaults** in `template/.meta/GUIDELINES.md.jinja` — working rhythm (5 steps), trunk-based development, modular monolith default, stdlib-first dependencies rule.
- **ADR template** (`template/.meta/decisions/adr-template.md.jinja`) — 4-question framework: what problem / alternatives / why this choice / exit cost.
- **Correction-loop callout** in `template/CLAUDE.md.jinja` — "If you find yourself correcting the AI on the same thing twice, add it to CLAUDE.md."
- `.env.example` documenting `GITHUB_TOKEN` setup.

### Changed
- Skills count bumped 8 → 10 across README, PHILOSOPHY.md, and skills-pack README.
- `template/CLAUDE.md.jinja` automatism #2 extended to propose `/vision` when Vision section is all TBD.
- `/research` and `/vision` rows added to trigger tables in both `template/CLAUDE.md.jinja` and meta-repo `CLAUDE.md`.
- `CREDITS.md` — added `claude-ai-project-starter` (Guillaume Desforges) with absorbed item inventory.

---

## [v1.1.0] — 2026-04-12 — Skill discoverability + README rework

### Added
- **Skill discoverability mechanism** — inverted-default trigger table in `CLAUDE.md` (8 skills + 5 agents) with Auto/Propose actions and observable-signal triggers. Propagated to both template and meta-repo. Solves the "LLM under-proposes features" problem by requiring a trigger scan before every response
- **Automatism #11 — Rule of 3 (anti-consensus bias)** — auto-invokes devil's-advocate agent after 3 consecutive user agreements without friction
- **README — "The loop you know vs. the loop you want"** — Before/After Mermaid diagram as emotional hook before mechanism
- **README — "The rails your prompt rides"** — Mermaid pipeline (REMEMBER → PLAN → GUARD → SHIP) showing enforced workflow with session continuity loopback
- **Banner SVG** — embedded base64 Press Start 2P font for true pixel-art rendering on GitHub (bypasses `@import` block), 3D triple shadow, CRT scanlines + vignette

### Changed
- **README** — new tagline ("Premium vibe-coding set-up in one command. Automatisms, skills, agents, secrets scanning, session memory — so the AI follows the structure, not your prompts."), full visual rework, rule count bumped 10 → 11
- **CLAUDE.md (meta-repo)** — new Skills & Agents section with trigger table (dogfoods the same mechanism the template ships)
- **`.gitignore`** — excludes `.claude/settings.local.json` (local-only, never commit)

---

## [v1.0.1] — 2026-04-09 — Governance polish (4-repo audit)

### Added
- **Honesty constraint (Rule #9)** — never write "verified/confirmed/tested/reproduced" without cited evidence
- **Tiered confidence gates** — GREEN/AMBER/RED levels in plan skill
- **Synthesis type** — new `.meta/` artifact type with slug lineage convention
- **Working with AI section** — anti-patterns, ADR template, practical defaults in GUIDELINES
- **Brand guide** — visual identity reference
- **Demo script + VHS tape** — reproducible terminal demo
- **Banner SVG** — initial version

### Changed
- CREDITS.md — added Feynman + Earnings Call Analyst

---

## [v1.0.0] — 2026-04-08 — First public release

### Added
- **Execution modes** — `safe` (default) and `full-auto` permission presets via `execution_mode` copier parameter
- **Public safety audit** — stdlib script (`scripts/audit_public_safety.py`) with 3 checks (sensitive files, gitignore coverage, 40+ secret patterns), pre-commit hook, 2 GitHub Actions workflows
- **`.meta/` taxonomy** — `active/`, `archive/`, `drafts/`, `decisions/`, `references/` with filename convention enforced by `check_meta_naming.py`
- **`meta_visibility` parameter** — `public` (default, commits `.meta/`) or `private` (gitignores `.meta/`)
- **Workflow gates** — tiered decision tree (automatism #4), devil's-advocate persona, pending plans check at session start
- **Pre-commit hooks** — `check_git_author` (blocks Claude/Anthropic authorship), `audit-public-safety-quick` (secret scan)
- **GitHub Actions** — `public-safety.yml` (push/PR gate), `public-alert.yml` (reactive on repo publicization)
- **Publication files** — CREDITS.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CONTRIBUTORS.md
- **Commit strategy** — commit-per-logical-unit rule in CLAUDE.md and GUIDELINES

### Changed
- **CLAUDE.md** — plan-validated rule (automatism #4) strengthened
- **README** — execution modes documentation, "Before going public" section
- **`.gitignore`** — enriched to cover all canonical paths (venv, IDE, coverage, node_modules, etc.)

### Fixed
- Public safety audit scans `.meta/` for real secrets (removed blanket exclusion)

---

## [v0.2.0] — 2026-04-07 — Skills ecosystem + agent personas

### Added
- `/debate` v2 — hybrid context (2 insiders + 1 lone wolf), anti-rationalization, 6 domain presets
- `/spec` — MoSCoW requirements formalization
- `/orchestrate` — session orchestrator with dependency tracking
- `AGENTS.md` — code-reviewer, test-engineer, security-auditor, data-analyst personas
- All skills: verification checklists + anti-rationalization tables
- Semver tag immutability rule

---

## [v0.1.1] — 2026-04-07 — Add /orchestrate skill

### Added
- `/orchestrate` — session orchestrator with dependency tracking
- `copier update` documentation in GUIDE.md

---

## [v0.1.0] — 2026-04-07 — Universal architecture + debate skill

### Added
- ADR-009: single universal Python template (replaces 4 profiles)
- Universal structure: `src/`, `tests/`, `scripts/`, `data/{raw,interim,processed}/`, `docs/`
- `/debate` skill — 3-agent adversarial debate with 6 domain presets
- Skills-pack for standalone installation

### Changed
- Template versioning via `copier update`

### Removed
- Profile system (minimal, app, data, quant) — replaced by universal architecture

---

## [v0.0.3] — 2026-04-07 — Settings v2

### Added
- Native attribution suppression (`attribution.commit: ""`)
- Security deny rules (credentials, dd) + ask force-push
- SessionStart hook (first_session detection)
- `.claude/rules/` (testing.md + code-style.md)
- Pre-commit `check-toml`

### Changed
- Automatism #4 strengthened (plan enforcement)
- GUIDELINES.md advanced options documented

---

## [v0.0.2] — 2026-04-07 — Superpowers integration

### Added
- Superpowers plugin auto-detection and install recommendation
- `/save-progress` skill (renamed from `/ship`)
- Knowledge hierarchy brainstorm (L1/L2/L3 context layers)
- Superpowers output paths redirected to `.meta/scratch/`

---

## [v0.0.1] — 2026-04-07 — MVP Phase A

### Added
- All templates in English
- 5 skills: brainstorm, plan, ship, lint, test
- CLAUDE.md + GUIDELINES.md + PILOT.md + SESSION-CONTEXT.md
- `pyproject.toml` with `uv_build` + ruff + pytest
- Pre-commit hooks
- `copier.yml` with 4 profiles (minimal, app, data, quant)
- GUIDE.md for user onboarding
