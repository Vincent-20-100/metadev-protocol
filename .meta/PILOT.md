# PILOT.md — metadev-protocol

**Date:** 2026-04-03
**Phase:** v2 Part 1 DONE, Part 2 brainstorm DONE — next: Part 3

---

## Project state

### MVP Phase A (DONE)
- All templates in English ✅
- CLAUDE.md (law) + GUIDELINES.md (mentor) ✅
- PILOT.md + SESSION-CONTEXT.md (context) ✅
- 5 skills (brainstorm, plan, ship, lint, test) ✅
- pyproject.toml (uv_build + ruff + pytest) ✅
- Pre-commit enriched ✅
- copier.yml English + auto-setup ✅
- All 4 profiles tested ✅
- docs/PHILOSOPHY.md + template GUIDE.md ✅
- All meta-repo files in English ✅
- Repo cleaned (removed src/, .env.example, .python-version, .claudeignore) ✅

### v2 Phase C — Roadmap

| Part | Scope | Status |
|------|-------|--------|
| 1 | Superpowers integration + /save-progress rename | DONE |
| 2 | Knowledge hierarchy (L1/L2/L3 context layers) | BRAINSTORM DONE |
| 3 | Infrastructure (CI, config levels, language params) | TO BRAINSTORM |
| 4 | Profile-specific skills | TO BRAINSTORM |
| 5 | Multi-agent support (AGENTS.md) | TO BRAINSTORM |

### Key decisions (v2)

- Skills T2 delegated to Superpowers plugin (not custom)
- Superpowers outputs redirected to .meta/scratch/ via CLAUDE.md
- /brainstorm + /plan kept as lightweight fallbacks
- /ship renamed to /save-progress
- /consolidate dropped (YAGNI)
- Auto-install Superpowers: check → propose → install if user agrees
- Knowledge hierarchy: L1/L2/L3 aligned with Claude Code native memory (MEMORY.md = L2)
- Mini-RAG deferred (too ambitious for v2, revisit if L1/L2/L3 insufficient)
- AGENTS.md support planned as Part 5
- Deep Agents, AGENTS.md spec added to recommended ecosystem

---

## Scratch files (current brainstorms)

```
.meta/scratch/
├── mvp-phase-a-spec.md          # MVP spec (archived as ADR-007)
├── mvp-phase-a-plan.md          # MVP implementation plan
├── v2-roadmap.md                # Full v2 roadmap with sequence
├── v2-part1-spec.md             # Superpowers integration spec
└── v2-part2-brainstorm.md       # Knowledge hierarchy brainstorm (IN PROGRESS)
```

---

## AI context

- Gold files are the synthesized source of truth
- Decisions are ADRs with rationale and confidence levels
- Any change to template/ must be tested with copier copy
- Stack: Python 3.13+, uv, ruff, copier, pre-commit
- ALL template output in English
- Superpowers plugin is the recommended complement (not a dependency)
- AGENTS.md standard tracked for future multi-agent support
