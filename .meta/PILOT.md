# PILOT.md — metadev-protocol

**Date:** 2026-04-07
**Phase:** v0.2 — Skills ecosystem + agent personas

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

### ADR-009 — Universal architecture (DONE)
- Single Python template — project_type profiles removed ✅
- Universal structure: src/, tests/, scripts/, data/{raw,interim,processed}/, docs/ ✅
- Expansion paths in GUIDELINES: notebooks/, app/, api/, config/, models/, infra/ ✅
- CLAUDE.md structure guidance (encourage, not forbid) ✅
- ADR written: .meta/decisions/adr-009-universal-architecture.md ✅

### v0.2 — Skills ecosystem (IN PROGRESS)
- /debate skill v1: 3-agent adversarial debate, 6 presets ✅
- /debate skill v2: hybrid context (2 insiders + 1 lone wolf), anti-rationalization ✅
- /spec skill: MoSCoW requirements formalization ✅
- /orchestrate skill: session orchestrator with dependency tracking ✅
- AGENTS.md: 4 personas (code-reviewer, test-engineer, security-auditor, data-analyst) ✅
- Verification evidence + anti-rationalization tables on all skills ✅
- Skills-pack for standalone installation ✅
- Template versioning: v0.1.0, v0.1.1 tags, copier update documented ✅
- Skills reordered by workflow phase in CLAUDE.md ✅

### Plans ready (not yet implemented)
- **debate-v2-plan.md** — hybrid context + lone wolf final implementation
- **plan-rodin-agent.md** — devil's-advocate persona (5th agent, Rodin-inspired)

### Future (noted in memory, not in scope)
- Nightshift: overnight autonomous orchestrator (needs server infra)
- Adoption mode: inject method into existing repos without Copier
- /orchestrate iteration: test and refine in real usage
- Plugin distribution: publish skills as Claude Code plugin

### v2 Phase C — Roadmap

| Part | Scope | Status |
|------|-------|--------|
| 1 | Superpowers integration + /save-progress rename | DONE |
| 2 | Knowledge hierarchy (L1/L2/L3 context layers) | BRAINSTORM DONE |
| 3 | Infrastructure (CI, config levels, language params) | TO BRAINSTORM |
| 4 | Skills ecosystem (/debate, /spec, /orchestrate, AGENTS.md) | IN PROGRESS |
| 5 | Multi-agent support (devil's-advocate, nightshift) | PLANNED |
| — | ADR-008: Settings v2 improvements | DONE |
| — | ADR-009: Universal Python architecture | DONE |

### Key decisions

- Skills T2 delegated to Superpowers plugin (not custom)
- Superpowers outputs redirected to .meta/scratch/ via CLAUDE.md
- /brainstorm + /plan kept as lightweight fallbacks
- /ship renamed to /save-progress
- ADR-009: single Python template, no profiles, no underscore prefix
- /debate: hybrid context (2 insiders + 1 fresh lone wolf) — design validated, implementation pending
- Agent personas follow Osmani pattern (AGENTS.md)
- Semver tags are immutable — never rewrite, always bump
- ALWAYS write plans before coding — no exceptions

---

## References

```
.meta/references/
├── gstack-skill-pack.md         <- 23-agent sprint workflow (garrytan)
├── skill-design-sources.md      <- All skill/agent design inspirations
```

## Scratch files

```
.meta/scratch/
├── mvp-phase-a-spec.md          # MVP spec (archived as ADR-007)
├── mvp-phase-a-plan.md          # MVP implementation plan
├── v2-roadmap.md                # Full v2 roadmap with sequence
├── v2-part1-spec.md             # Superpowers integration spec
├── v2-part2-brainstorm.md       # Knowledge hierarchy brainstorm
├── v2-architecture-separation.md # Nightshift vs orchestrate separation
├── adr-008-implementation-plan.md # Settings v2 plan (DONE)
├── adr-009-brainstorm.md        # Universal architecture brainstorm (RESOLVED)
├── debate-skill-v1-spec.md      # Debate v1 spec (DONE)
├── debate-v2-plan.md            # Debate v2: hybrid context + lone wolf (READY)
├── plan-spec-skill.md           # /spec skill plan (DONE)
└── plan-rodin-agent.md          # Devil's advocate agent plan (READY)
```

---

## AI context

- Gold files are the synthesized source of truth
- Decisions are ADRs with rationale and confidence levels
- Any change to template/ must be tested with copier copy
- Stack: Python 3.13+, uv, ruff, copier, pre-commit
- ALL template output in English
- Superpowers plugin is the recommended complement (not a dependency)
- ALWAYS write a plan and get user validation before implementing
- Skill design sources: .meta/references/skill-design-sources.md
