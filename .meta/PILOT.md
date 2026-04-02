# PILOT.md — metadev-protocol

**Date:** 2026-04-01
**Phase:** Strategic brainstorm done — ready for MVP implementation

---

## Project state

### Infrastructure (DONE)
- pyproject.toml, .pre-commit-config.yaml, copier.yml ✅
- Template generates successfully (minimal + app tested) ✅
- Pre-commit installed ✅

### Research (DONE)
- 15 raw references in .meta/references/ ✅
- 5 gold syntheses in .meta/gold/ ✅
- 6 ADRs in .meta/decisions/ ✅

### Strategic brainstorm (DONE)
- Target audience: B/C (devs discovering vibe coding) ✅
- Identity: "brand new workshop" (opinionated lightweight framework) ✅
- Language: English default, 3 levels (code/project/meta) ✅
- Superpowers: autonomous, inspired, credited ✅
- Versioning: one-shot for now ✅
- All decisions in ADR-006 ✅

### MVP scope (NEXT — 1 session)

| # | Action | Status |
|---|--------|--------|
| 1 | Rewrite all templates to English | ❌ |
| 2 | Add src/{{project_slug}}/__init__.py | ❌ |
| 3 | Switch build backend to uv_build | ❌ |
| 4 | Add ruff + pytest config in pyproject.toml.jinja | ❌ |
| 5 | Enrich pre-commit (trailing-whitespace, check-yaml, no-commit-to-branch) | ❌ |
| 6 | Add no-co-author-llm hook (pre-commit + settings.json) | ❌ |
| 7 | Create skill /brainstorm (prescriptive, Superpowers-inspired) | ❌ |
| 8 | Create skill /plan (writes to .meta/scratch/plan.md) | ❌ |
| 9 | Create skill /ship (checklist + PILOT update + SESSION-CONTEXT rewrite) | ❌ |
| 10 | Create skill /lint (ruff check + format) | ❌ |
| 11 | Update CLAUDE.md.jinja (English, first-session detection, skill shortlist) | ❌ |
| 12 | Test full generation (all profiles) | ❌ |

### Post-MVP (vision C)
- Skills T2: /spec, /tdd, /review, /debug, /consolidate
- Knowledge hierarchy: INDEX.md, /digest, /dream, /tidy
- GitHub Actions CI
- Config 3 levels (app profile)
- Language params in copier.yml
- Profile-specific skills

---

## Gold files (knowledge base)

```
.meta/gold/
├── skills-workflow-and-utilities.md    <- 13 skills classified T1/T2/T3
├── context-management.md              <- 3 axes, 5 compaction levels
├── claude-code-architecture.md        <- Leak + official docs
├── vibe-coding-practices.md           <- 5 principles, 7 anti-patterns
└── python-dev-and-templating.md       <- 8 decisions, sprint plan
```

## AI context

- Gold files are the synthesized source of truth
- References are raw sources (bronze)
- Decisions are ADRs with rationale and confidence levels
- Any change to template/ must be tested with copier copy
- Stack: Python 3.12+, uv, ruff, copier, pre-commit
- ALL template output must be in English
