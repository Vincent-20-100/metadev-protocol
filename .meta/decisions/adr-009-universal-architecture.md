# ADR-009 — Universal Python project architecture

**Date:** 2026-04-06
**Status:** ACCEPTED

---

## Context

The template had 4 profiles (minimal, app, data, quant) mixing two orthogonal axes:
- **Language/stack** (Python + uv + ruff) — identical across all profiles
- **Project type** (app vs data vs quant) — different folder structures and dependencies

This created maintenance burden (4 profiles to test) and limited flexibility
(can't add data/ to a "minimal" project mid-way). The profiles also mapped
poorly to reality — most projects blend concerns.

The new direction: **one template per language** (starting with Python),
with a universal folder structure that works for any use case.

## Decision

### 1. Single universal template — no more project_type

The `project_type` question is removed from copier.yml. One Python template
serves all use cases. Future templates will be per-language (React, etc.),
not per-type.

### 2. No underscore prefix for dormant folders

Rejected the `_notebooks/`, `_docs/` convention. Reasons:
- `_` prefix means "private" in Python — wrong signal
- Tooling may treat `_` prefixed dirs specially
- Copier can simply generate what's needed — no "dormant" concept required

### 3. Universal folder structure

Always generated:
```
src/{slug}/              # Package source
tests/                   # Tests
scripts/                 # Utility scripts, automation
data/raw/                # Raw data — immutable
data/interim/            # Intermediate transformations
data/processed/          # Final outputs
docs/                    # Documentation
.meta/                   # Development cockpit
```

### 4. Data versioned by default

The three data subdirectories are tracked via .gitkeep so the structure
is visible from day one. When datasets grow large, users add patterns
to .gitignore and document data sources in data/README.md or PILOT.md.

### 5. Structure guidance, not prohibition

CLAUDE.md encourages following the predefined structure but does not
forbid creating new directories. The LLM should check GUIDELINES.md
before creating top-level directories.

### 6. Expansion paths in GUIDELINES.md

For use cases beyond the base structure, GUIDELINES documents standard
expansion paths: `notebooks/`, `app/`, `api/`, `config/`, `models/`,
`infra/`. The LLM picks from this menu rather than inventing names.

## Consequences

- **Simpler maintenance**: one template to develop, test, and document
- **Better LLM guidance**: pre-built structure prevents improvised layouts
- **Flexible growth**: expansion paths provide a vocabulary without upfront bloat
- **No migration needed**: new projects get the universal structure; existing
  projects generated with old profiles continue to work as-is
- **pyproject.toml ships with empty dependencies**: users add what they need
