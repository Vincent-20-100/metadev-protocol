# PILOT.md — metadev-protocol

**Date:** 2026-04-06
**Phase:** ADR-008 DONE — ADR-009 brainstorm started (universal architecture)

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
- Repo cleaned ✅

### ADR-008 — Settings v2 (DONE)
- attribution.commit: "" (suppress co-author) ✅
- Security deny rules (credentials, dd) + ask force-push ✅
- SessionStart hook (first_session detection) ✅
- .claude/rules/ (testing.md + code-style.md) ✅
- Automatism #4 strengthened (plan enforcement) ✅
- GUIDELINES.md advanced options documented ✅
- Pre-commit check-toml added ✅
- All 4 profiles tested ✅

### ADR-009 — Universal architecture (BRAINSTORM STARTED)
- Research done: folder structures, data tiers, .meta separation ✅
- gstack skill pack analyzed (reference added) ✅
- Key decisions drafted:
  - Data tiers: raw / interim / processed (not bronze/silver/gold)
  - Underscore prefix for dormant folders (_notebooks/, _docs/, _config/)
  - Clear .meta vs project separation rules
  - Single profile per language (drop minimal/app/data/quant)
- **NEXT:** Full brainstorm session to finalize and implement

### v2 Phase C — Roadmap

| Part | Scope | Status |
|------|-------|--------|
| 1 | Superpowers integration + /save-progress rename | DONE |
| 2 | Knowledge hierarchy (L1/L2/L3 context layers) | BRAINSTORM DONE |
| 3 | Infrastructure (CI, config levels, language params) | TO BRAINSTORM |
| 4 | Profile-specific skills | TO BRAINSTORM |
| 5 | Multi-agent support (AGENTS.md) | TO BRAINSTORM |
| — | ADR-008: Settings v2 improvements | DONE |
| — | ADR-009: Universal Python architecture | BRAINSTORM STARTED |

### Key decisions

- Skills T2 delegated to Superpowers plugin (not custom)
- Superpowers outputs redirected to .meta/scratch/ via CLAUDE.md
- /brainstorm + /plan kept as lightweight fallbacks
- /ship renamed to /save-progress
- Auto-install Superpowers: check → propose → install if user agrees
- Knowledge hierarchy: L1/L2/L3 aligned with Claude Code native memory
- ADR-008: native attribution suppression, security denys, rules/, plan enforcement
- ADR-009 direction: single Python template with universal folders + underscore dormant pattern

---

## References

```
.meta/references/
├── gstack-skill-pack.md         <- 23-agent sprint workflow (garrytan)
├── (+ existing references)
```

## Scratch files

```
.meta/scratch/
├── mvp-phase-a-spec.md          # MVP spec (archived as ADR-007)
├── mvp-phase-a-plan.md          # MVP implementation plan
├── v2-roadmap.md                # Full v2 roadmap with sequence
├── v2-part1-spec.md             # Superpowers integration spec
├── v2-part2-brainstorm.md       # Knowledge hierarchy brainstorm
├── adr-008-implementation-plan.md # Settings v2 plan (DONE)
└── adr-009-brainstorm.md        # Universal architecture brainstorm (NEW)
```

---

## AI context

- Gold files are the synthesized source of truth
- Decisions are ADRs with rationale and confidence levels
- Any change to template/ must be tested with copier copy
- Stack: Python 3.13+, uv, ruff, copier, pre-commit
- ALL template output in English
- Superpowers plugin is the recommended complement (not a dependency)
- ADR-009 will reshape the template: single profile, universal folders, underscore dormant pattern
