# ADR-004 — Decision matrix: all patterns classified

**Date:** 2026-04-01
**Status:** DRAFT — pending validation by Vincent

---

## Classification grid

### Axis 1 — Priority (quality/importance)

| Tier | Meaning | Criterion |
|------|---------|-----------|
| **T1 ESSENTIAL** | If this is missing, the template has no value | Without it, the generated project is worse than a `mkdir` |
| **T2 RECOMMENDED** | High added value, community consensus | Adopted by >50% of good repos, measurable impact |
| **T3 NICE-TO-HAVE** | Useful but not critical, can come later | Improves experience without being a blocker |
| **T4 AVOID** | Over-engineering, too specific, or counterproductive | Adds complexity with no clear benefit for a bootstrap |

### Axis 2 — Scope (vanilla vs custom)

| Scope | Meaning |
|-------|---------|
| **VANILLA** | In all profiles (minimal/app/data/quant) |
| **PROFILE** | Conditional on project type |
| **USER** | The user adds it themselves if needed |

---

## The matrix

### T1 ESSENTIAL

| Pattern | Scope | Source | Implemented? |
|---------|-------|--------|--------------|
| CLAUDE.md with AI instructions (<120 lines) | VANILLA | SOTA, ADR-003 | YES |
| pyproject.toml with deps by profile | VANILLA | EgoVault, SOTA | YES |
| Clean .gitignore | VANILLA | Standard | YES |
| uv as dependency manager | VANILLA | SOTA, consensus | YES |
| ruff for lint + format | VANILLA | SOTA, consensus | YES |
| pre-commit hooks (ruff) | VANILLA | SOTA, ADR-001 | YES |
| Conventional commits documented | VANILLA | EgoVault, SOTA | YES |
| .meta/ cockpit (PILOT.md) | VANILLA | EgoVault, ADR-003 | YES |
| tests/ with conftest.py | VANILLA | EgoVault, SOTA | YES |
| .claude/settings.json (permissions) | VANILLA | ADR-002 | YES |
| git init post-copy | VANILLA | SOTA | YES |

### T2 RECOMMENDED

| Pattern | Scope | Source | Implemented? |
|---------|-------|--------|--------------|
| SESSION-CONTEXT.md (rewrite, don't append) | VANILLA | EgoVault, ADR-003 | YES |
| 5-phase workflow in PILOT.md | VANILLA | EgoVault+SOTA, ADR-003 | YES |
| Document hierarchy (CLAUDE.md > decisions > docstrings) | VANILLA | EgoVault, ADR-003 | YES |
| Universal anti-LLM rules (G2, G5, G6, G13) | VANILLA | EgoVault, ADR-003 | YES |
| Auto-ruff PostToolUse hook | VANILLA | ADR-002, SOTA | YES |
| Context re-injection hook after compaction | VANILLA | ADR-002, ref hooks | YES |
| Skill /test (pytest) | VANILLA | ADR-002 | YES |
| Deny permissions (rm -rf, sudo, .env, .git) | VANILLA | ADR-002 | YES |
| Skill /lint (ruff check + format) | VANILLA | Direct logic | **NO** |
| Skill /ship (pre-commit checklist) | VANILLA | SOTA workflow | **NO** |
| src/{{project_slug}}/__init__.py | VANILLA | Standard Python | **NO** |
| PEP 735 dependency groups (dev/test) | VANILLA | SOTA | YES (partial) |
| Profile-specific app rules (thin routing, DI) | PROFILE:app | EgoVault G4/G11 | YES |
| Profile-specific quant rules (vectorization, math docs) | PROFILE:quant | EgoVault adapted | YES |
| Profile-specific data rules (idempotent, raw immutable) | PROFILE:data | EgoVault adapted | YES |
| 3-level config (system/user/install) | PROFILE:app | EgoVault, ADR-001 | **NO** |
| Deps fastapi+uvicorn | PROFILE:app | Standard | YES |
| Deps polars+duckdb | PROFILE:data | Standard | YES |
| Deps numpy+pandas+matplotlib | PROFILE:quant | Standard | YES |

### T3 NICE-TO-HAVE

| Pattern | Scope | Source | Implemented? |
|---------|-------|--------|--------------|
| Skill /review (code review in subagent fork) | VANILLA | Ref hooks/skills | **NO** |
| Compaction instruction in CLAUDE.md | VANILLA | SOTA | **NO** |
| 120-char line length ruff config | VANILLA | SOTA consensus | **NO** |
| Dynamic versioning (git tags) | VANILLA | SOTA | **NO** |
| Skill /api-test (test endpoints) | PROFILE:app | Direct logic | **NO** |
| Skill /pipeline-run | PROFILE:data | Direct logic | **NO** |
| Skill /backtest | PROFILE:quant | Direct logic | **NO** |
| Empty/template .mcp.json | USER | Ref MCP | **NO** |
| Subagent investigation pattern | USER | SOTA, leak | **NO** |
| Red Zone / Green Zone documentation | USER | SOTA | **NO** |
| 9-layer AI app as checklist | PROFILE:app | LinkedIn posts | **NO** |
| Recursive arguing (code + review agents) | USER | SOTA | **NO** |
| agnix linter for CLAUDE.md/skills | USER | top-repos | **NO** |
| Research-first development guide | VANILLA | SOTA | **NO** |

### T4 AVOID (for a bootstrap)

| Pattern | Why we reject it | Source |
|---------|-----------------|--------|
| 7-phase workflow (BRAINSTORM→AUDIT) | Over-engineered for a new project | EgoVault |
| docs/superpowers/ lifecycle (specs/plans/audits/archive) | Too heavy, relevant for mature projects | EgoVault |
| @loggable decorator with callback injection | Too specific to EgoVault's architecture | EgoVault |
| Config-driven taxonomy (YAML enums) | Specific to projects with user classification | EgoVault |
| Claude Code sandbox enabled by default | Too restrictive, breaks the dev flow | Ref hooks |
| Pre-configured MCP servers | Too specific to each user/environment | Ref MCP |
| PreToolUse hook to block rm (redundant with deny) | The deny in permissions already does the job | Ref hooks |
| KAIROS/autoDream/ULTRAPLAN patterns | Unreleased features, not usable | Leak |
| Anti-distillation fake tools | Anthropic-specific, not a dev pattern | Leak |
| pyright/mypy enabled by default | Adds friction without benefit for a bootstrap | SOTA |
| Generated CI/CD pipeline | Too specific (GitHub Actions vs GitLab vs...) | Standard |

---

## Next actions (by priority)

### Sprint 1 — Complete missing T2s

| Action | Effort |
|--------|--------|
| Create skill /lint | Small |
| Create skill /ship | Small |
| Create src/{{project_slug}}/__init__.py in template | Small |
| Create 3-level config/ for app profile | Medium |

### Sprint 2 — High-value T3s

| Action | Effort |
|--------|--------|
| Compaction instruction in CLAUDE.md | Small |
| Ruff 120 chars config in pyproject.toml.jinja | Small |
| Skill /review (subagent fork) | Medium |
| Profile-specific skills (api-test, pipeline-run, backtest) | Medium |

### Sprint 3 — Documentation and polish

| Action | Effort |
|--------|--------|
| Guide "how to add your own skills" | Small |
| MCP configuration guide | Small |
| Research-first development tips in CLAUDE.md | Small |

---

## Confidence levels

| Tier | Confidence | Justification |
|------|------------|---------------|
| T1 | VERY HIGH | Industry standards, broad consensus |
| T2 | HIGH | Tested on EgoVault and/or documented by the community |
| T3 | MEDIUM | Good idea but not yet tested in our context |
| T4 | HIGH (on the rejection) | Proven over-engineering or too specific |
