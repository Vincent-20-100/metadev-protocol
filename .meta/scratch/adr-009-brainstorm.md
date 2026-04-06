# ADR-009 Brainstorm — Universal Python project architecture

**Date:** 2026-04-06
**Status:** RESOLVED — all decisions finalized and implemented (2026-04-06)
**Trigger:** Rethinking profile system (minimal/app/data/quant → single universal template)

---

## Problem

Current template has 4 profiles that mix two orthogonal axes:
- **Stack/language** (Python + uv + ruff) — same for all
- **Finalité** (app vs data vs quant) — different folder structures

This creates maintenance burden (4 profiles) and limits flexibility
(can't add data/ to a "minimal" project mid-way).

## Proposed direction

**One template per language** with a universal folder structure.
Optional folders use underscore prefix (`_notebooks/`) — visible but
clearly dormant. LLM renames them when first used.

## Key decisions (drafted)

### Data tiers: `raw / interim / processed`
- `raw/` = brut, immutable, backup
- `interim/` = normalisé, nettoyé, pré-traité
- `processed/` = output final, prêt à consommer
- Rejected: bronze/silver/gold (too Databricks-specific), raw/processed (2 tiers insufficient)
- Source: cookiecutter-data-science convention, most widely understood

### Dormant folders: underscore prefix
- `_notebooks/`, `_docs/`, `_config/` → rename to activate
- Visible in IDE/terminal (unlike dot-prefix)
- Clear signal: "not active yet"
- Git-friendly: no special .gitignore needed

### Always active vs dormant

| Always active | Dormant (underscore) |
|---------------|---------------------|
| src/{pkg}/ | _notebooks/ |
| tests/ | _docs/ |
| scripts/ | _config/ |
| data/raw,interim,processed/ | |
| .meta/ | |
| .claude/ | |

### .meta vs project separation
- Ships to users → project (`src/`, `scripts/`, `config/`)
- Helps build → `.meta/` (`scratch/`, `scripts/`, `decisions/`)
- Temp generation scripts → `.meta/scratch/` (NEVER `scripts/`)
- Exploratory one-off notebooks → `.meta/scratch/`
- Reusable notebooks → `_notebooks/` (when activated)

### CLAUDE.md instructions for LLM
- Never create parallel folders (no output/, stuff/, temp/)
- Raw data is immutable
- When activating a _folder, announce it to the user
- Temporary scripts → .meta/scratch/

## Open questions (to resolve in brainstorm)

1. **scripts/ always active or dormant?** — Leaning active (even minimal projects need a setup script)
2. **data/ always active?** — Leaning active (low cost, high guidance value)
3. **notebooks at root vs .meta?** — Current: `_notebooks/` at root (more natural when activated)
4. **Drop copier profiles entirely?** — Or keep as "presets" that activate the _ folders?
5. **Hook auto-reveal?** — PostToolUse hook that detects writes to _folder/ and renames. Timing issue: Write fails before hook runs. Needs investigation.
6. **Migration path** — How do existing projects generated with old profiles transition?

## Research sources

- Python project structure consensus (PyPA, cookiecutter-data-science, Real Python)
- Data tier naming (Databricks Medallion, dbt, cookiecutter-data-science)
- .meta separation patterns (ADR standards, py-pkgs)
- gstack skill pack (.meta/references/gstack-skill-pack.md)
