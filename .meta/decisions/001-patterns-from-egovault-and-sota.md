# ADR-001 — Patterns to integrate into the template (EgoVault + State of the Art)

**Date:** 2026-04-01
**Status:** VALIDATED — approved by Vincent, implemented in ADR-002 and ADR-003
**Sources:** audit-egovault.md, state-of-the-art-vibe-coding.md, claude-code-leak-analysis.md

---

## Context

Cross-referencing the EgoVault audit (real project, 374 tests, mature architecture) with
state-of-the-art research (CLAUDE.md sizing, hooks vs instructions, progressive disclosure).
The goal is to decide which patterns to integrate into the metadev-protocol template.

---

## Decisions

### ADOPT — Direct integration into the template

#### 1. Two-file cockpit: PILOT.md (state) + SESSION-CONTEXT.md (why)

- **Source:** EgoVault (PROJECT-STATUS + SESSION-CONTEXT)
- **Adaptation:** Rename to PILOT.md (already done) + add SESSION-CONTEXT.md.jinja
- **Key rule:** SESSION-CONTEXT.md is REWRITTEN each session, not appended to
- **Impact:** `template/.meta/` — add SESSION-CONTEXT.md.jinja

#### 2. Universal anti-LLM rules in CLAUDE.md

- **Source:** EgoVault G1-G13, filtered to universals
- **Rules to include in all profiles:**
  - G2 — Docstrings: WHAT not HOW
  - G5 — No over-engineering
  - G6 — Every except must log or re-raise
  - G13 — Comments: concise, surgical
- **Profile-specific rules (app only):**
  - G4 — tools never import infrastructure
  - G11 — Routing layers are thin (<15 lines)
- **Impact:** `template/CLAUDE.md.jinja` — add rules section

#### 3. CLAUDE.md < 200 lines (sizing constraint)

- **Source:** State of the art (Boris Cherny, ~100 lines / 2500 tokens)
- **Finding:** EgoVault has 350 lines = too long. Compliance drops beyond 200.
- **Decision:** The template generates a CLAUDE.md of 80-120 lines max
- **Trade-off:** Detailed rules (Wrong/Right examples) go in `.claude/` skills,
  not in CLAUDE.md
- **Impact:** `template/CLAUDE.md.jinja` — keep lean, offload detail

#### 4. Hooks > CLAUDE.md for enforcement

- **Source:** State of the art (hooks = 100% compliance vs CLAUDE.md = ~70-80%)
- **Finding:** EgoVault has NO hooks — everything is carried by CLAUDE.md = fragile
- **Decision:** The template generates `.pre-commit-config.yaml` with ruff (already done)
  + potentially Claude Code hooks in `.claude/settings.json`
- **Impact:** Already partially done. Explore Claude Code hooks.

#### 5. Three-level config (system / user / install)

- **Source:** EgoVault config/
- **Adaptation:** For the `app` profile, generate `config/` with .example files
- **Impact:** `template/` — conditional on project_type == "app"

#### 6. Permanent / provisional document hierarchy

- **Source:** EgoVault CLAUDE.md §3
- **Decision:** Integrate into the generated CLAUDE.md: "CLAUDE.md > docs/ > docstrings"
  + distinguish `.meta/` (provisional) from `docs/` (permanent)
- **Impact:** `template/CLAUDE.md.jinja`

#### 7. Mirror structure tests + conftest.py with DI mock

- **Source:** EgoVault tests/conftest.py
- **Decision:** Generate minimal `tests/conftest.py` with base fixtures
- **Impact:** `template/tests/conftest.py.jinja`

### ADAPT — To be modulated by profile

#### 8. Development workflow

- **Source:** EgoVault (7 phases) + State of the art (Research > Plan > Execute > Review > Ship)
- **Decision:** The template includes a simplified workflow in PILOT.md:
  Research > Plan > Implement > Test > Ship (5 phases, not 7)
- **EgoVault added BRAINSTORM + AUDIT** = relevant for mature projects, not bootstrap
- **Impact:** `template/.meta/PILOT.md.jinja`

#### 9. Multiple surfaces (API + CLI + MCP)

- **Source:** EgoVault
- **Decision:** Not in the base template. Document as a pattern in CLAUDE.md
  for the `app` profile: "If you need multiple surfaces, follow the ports & adapters pattern"
- **Impact:** `template/CLAUDE.md.jinja` (conditional app section)

### REJECT — Too specific or over-engineered for a bootstrap

#### 10. @loggable decorator with callback injection

- Too specific to EgoVault. The pattern is elegant but not generalizable to a bootstrap.

#### 11. Config-driven taxonomy

- Specific to projects with user classification. Not a template pattern.

#### 12. Complete 7-phase workflow

- Over-engineered for a bootstrap. Simplified to 5 phases (see #8).

#### 13. docs/superpowers/ lifecycle (specs/plans/audits/archive)

- Too heavy. The template generates `.meta/decisions/` for ADRs, that is sufficient.

---

## Implementation Plan

| Priority | Action | Impacted file |
|----------|--------|----------------|
| P0 | Reduce CLAUDE.md.jinja to <120 lines | template/CLAUDE.md.jinja |
| P0 | Add anti-LLM rules (G2, G5, G6, G13) | template/CLAUDE.md.jinja |
| P1 | Create SESSION-CONTEXT.md.jinja | template/.meta/ |
| P1 | Enrich PILOT.md.jinja (5-phase workflow) | template/.meta/PILOT.md.jinja |
| P1 | Add `_tasks` post-copy in copier.yml | copier.yml |
| P2 | Generate minimal tests/conftest.py | template/tests/ |
| P2 | 3-level config for app profile | template/config/ (conditional) |
| P3 | Explore Claude Code hooks (.claude/settings.json) | template/.claude/ |
