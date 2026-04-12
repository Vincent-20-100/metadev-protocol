# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).
This project uses [semantic versioning](https://semver.org/).

---

## [Unreleased] (v1.0.0 candidate)

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
