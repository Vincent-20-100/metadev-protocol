# ADR-006 — Strategic Brainstorm: Project Direction

**Date:** 2026-04-01
**Status:** VALIDATED — decisions taken during brainstorm session

---

## Decisions

### 1. Target audience: B/C

Devs who discover vibe coding, with or without background. Well-commented,
fluent UX, not a tutorial. The LLM answers questions, the system is self-explanatory.

### 2. Language: 3 distinct levels

| Level | What | Default | Configurable ? |
|-------|------|---------|----------------|
| **Code** | Variables, docstrings, technical comments | English always | No |
| **Project** | CLAUDE.md, skills, README, commits | English | Yes — `project_language` copier param |
| **Meta/dev** | PILOT.md, SESSION-CONTEXT.md, decisions/, conversations | English | Yes — `dev_language` copier param |

Current templates are in French — need rewrite to English for MVP.

### 3. Relationship with Superpowers: autonomous, inspired, credited

- Our skills live in `.claude/skills/` (project-level, shared via git)
- Superpowers is a user-level plugin (not shareable via repo)
- We create our own skills inspired by Superpowers methodology (MIT license)
- We cite Superpowers explicitly and will contact obra (Jesse Vincent)
- We recommend Superpowers as external complement for advanced workflows

### 4. Identity: "A brand new workshop" — opinionated lightweight framework

- Not a toolbox (user picks tools) — an workshop (everything pre-installed, ready to use)
- Prescriptive: the LLM follows the workflow naturally, user doesn't remind
- Not blocking: user can ignore skills, bypass hooks, work freely
- The system "forces" the LLM without "trapping" the user

### 5. Complexity: everything is there, conversational onboarding

- Full structure generated for everyone (no stripped-down version)
- CLAUDE.md instructs LLM to detect first session and offer intro
- PILOT.md has a "first_session: true" flag
- Comments explain everything — if it's clear, the LLM can answer questions
- Recommended external skills shortlist in session start

### 6. Versioning: one-shot for now

- `copier copy` once, project lives its life
- No `copier update` mechanism in MVP
- Upgrade path: copy a fresh template for new projects
- Revisit when project matures

### 7. Skill inter-dependencies

- `/brainstorm` writes `.meta/scratch/brainstorm.md`
- `/plan` reads brainstorm.md if it exists, writes `.meta/scratch/plan.md`
- `/ship` updates PILOT.md + rewrites SESSION-CONTEXT.md
- Dependencies are explicit in each skill's instructions
- No hard coupling — each skill works standalone too

### 8. External skills shortlist

- Recommended external plugins/skills displayed at session start
- Lives in CLAUDE.md or PILOT.md (TBD)
- Examples: Superpowers, browser control, specific MCP servers
- Updated per profile (app might recommend different tools than data)

### 9. Multi-LLM: Claude Code only for MVP

- CLAUDE.md is Claude Code specific
- .cursorrules / CONVENTIONS.md for other tools = post-MVP
- The skills format (SKILL.md) is Claude Code specific anyway

### 10. copier.yml questions update needed

Current: project_name, project_slug, project_type, author_name, python_version
To add (post-MVP): project_language, dev_language
Keep minimal for MVP — each question is friction at `copier copy`

---

## Open items for post-MVP (vision C)

- Knowledge hierarchy (INDEX.md, gold/references, /digest, /dream, /tidy)
- Timestamp-based truth resolution
- 3 maintenance mechanisms (human-in-the-loop, dream mode, lifecycle)
- Skills T2 (/spec, /tdd, /review, /debug, /consolidate)
- GitHub Actions CI
- Config 3 levels (app profile)
- Profile-specific skills (/api-test, /backtest, /pipeline-run)
- Multi-language templates (project_language param)
- Multi-LLM support (.cursorrules)
