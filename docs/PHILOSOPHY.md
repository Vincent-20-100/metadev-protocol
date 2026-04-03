# The Meta Protocol — Philosophy & Design

> This document explains **why** metadev-protocol exists and the principles behind every design choice.
> It is the reference for contributors and anyone curious about the project.
> Keep it in sync with reality — when the vision evolves, this doc evolves.

---

## The problem

AI-assisted coding (vibe coding) is powerful but chaotic. Without structure:

- The LLM loses context between sessions and reinvents the wheel
- Drafts, notes, and half-finished code pollute the repository
- The developer spends more time re-explaining intent than building
- Quality erodes because the LLM takes shortcuts no one catches
- Every project starts from scratch — no accumulated best practices

The cost is not the individual session. It's the compound debt across dozens of sessions and projects.

## The solution

**metadev-protocol** is a pre-configured workshop for AI-assisted Python projects. One `copier copy` command generates a project where:

- The LLM knows how to behave (CLAUDE.md encodes the rules)
- Context survives between sessions (PILOT.md + SESSION-CONTEXT.md)
- The workflow is automated, not explained (skills handle the process)
- The product and the process never mix (src/ vs .meta/)

It's not a toolbox where you pick what you need. It's an opinionated workshop where everything is pre-installed and ready. The LLM follows the workflow naturally — the user doesn't remind.

## Core principles

### 1. Separate the product from the process

The most important principle. A clean project has two spheres:

| Sphere | Contains | Rule |
|--------|----------|------|
| **Product** (`src/`, `tests/`, `docs/`) | What gets delivered | Stable, reviewed, tested |
| **Process** (`.meta/`) | How it gets built | Ephemeral, draft, AI workspace |

They never mix. Code doesn't live in `.meta/scratch/`. Session notes don't live at root. This separation is the primary defense against cognitive debt.

### 2. Law and mentor

Instructions to the LLM split into two authority levels:

- **CLAUDE.md is the law.** Few rules (8 max), non-negotiable. The LLM obeys without question. These cover what matters most: context management, commit format, code hygiene.
- **GUIDELINES.md is the mentor.** Best practices proposed, not imposed. The LLM draws from them naturally and suggests them when relevant. "Prefer X over Y because Z" — never "you MUST."

Why two files? Too many rules in one file and the LLM ignores them. Too few and important practices get lost. The split gives precision where it matters (law) and breadth where it helps (mentor).

### 3. Automatisms over instructions

The LLM should do the right thing without being asked. CLAUDE.md encodes 8 hard-wired behaviors:

1. **Session start** — read PILOT.md + SESSION-CONTEXT.md before anything
2. **First session** — detect the flag and offer an intro
3. **Before coding** — propose a plan first
4. **Milestone done** — update PILOT.md
5. **End of session** — rewrite SESSION-CONTEXT.md
6. **Every commit** — conventional format
7. **Architecture changes** — create/maintain ARCHITECTURE.md
8. **Always** — apply rules and draw from guidelines

The user doesn't say "read the context" or "update the status." The system does.

### 4. Hooks over instructions

Critical rules that the LLM might ignore (formatting, lint) are enforced by hooks, not written in CLAUDE.md. A PostToolUse hook runs ruff after every file edit. Pre-commit runs ruff + trailing-whitespace + check-yaml before every commit.

If it's important enough to never skip, make it a hook. If it's important but contextual, make it a rule. If it's advice, make it a guideline.

### 5. Skills are the workflow layer

Skills (`.claude/skills/`) are the right place for dev workflow:
- **Not CLAUDE.md** — too short, always loaded, can't hold process details
- **Not hooks** — too rigid, can't handle interactive workflows
- **Skills** — loaded on demand, shared via git, composable in pipelines

Five skills ship with every project:

| Skill | When | What it does |
|-------|------|-------------|
| `/brainstorm` | Idea is vague | Socratic exploration: one question at a time, 2-3 alternatives, YAGNI |
| `/plan` | Scope is clear | Break work into 2-5 min tasks with file mapping and verification |
| `/ship` | Work is done | Checklist (tests + lint + files), update PILOT.md, rewrite SESSION-CONTEXT.md |
| `/lint` | Anytime | ruff check + format on the whole project |
| `/test` | Anytime | Run pytest with optional arguments |

Skills form a pipeline: brainstorm → plan → implement → test → ship. Each can work standalone too.

### 6. Context survives sessions

Three files maintain project memory:

- **PILOT.md** — the dashboard. Where the project stands, what's next, what's done. Updated after milestones.
- **SESSION-CONTEXT.md** — the living context. Architecture snapshot, active decisions, traps, open questions. Rewritten (not appended) each session.
- **ARCHITECTURE.md** — created when architecture is defined. The LLM maintains it and checks for divergence.

Together, these files mean a new session starts with full context — even after compaction, machine change, or weeks of inactivity.

### 7. Progressive disclosure

Not everything loads at once:

| Layer | When loaded | Size |
|-------|-----------|------|
| CLAUDE.md | Every session, automatically | ~50 lines |
| PILOT.md + SESSION-CONTEXT.md | Session start (automatism #1) | ~30-40 lines each |
| GUIDELINES.md | Session start (automatism #8) | ~60 lines |
| Skills | On demand (/brainstorm, /plan, etc.) | ~30 lines each |
| .meta/decisions/ | When needed | Variable |

This hierarchy respects the LLM's context window. The essential is always present. The detailed is available on demand.

## Design decisions

Every structural choice has a rationale documented in `.meta/decisions/`:

| ADR | Decision | Key reasoning |
|-----|---------|--------------|
| 001 | Patterns from EgoVault + state of the art | Curated from 15 references, 5 gold syntheses |
| 002 | `.claude/` directory in template | Permissions, hooks, skills — shared via git |
| 003 | CLAUDE.md sizing + 2-file cockpit | <60 lines law + living context |
| 004 | Tiered pattern matrix (T1-T4) | Prioritize what to implement first |
| 005 | Knowledge hierarchy brainstorm | INDEX.md, /digest, /dream — deferred to v2 |
| 006 | Strategic brainstorm | Audience B/C, "brand new workshop", English default |
| 007 | MVP Phase A specification | Full spec for every template file |

## Target audience

Developers discovering vibe coding — with or without programming background. The system is:

- **Well-commented** — if it's clear, the LLM can answer questions
- **Self-explanatory** — first-session detection offers an intro
- **Not a tutorial** — it's a workshop, not a classroom

## What this is NOT

- **Not a framework** — no runtime dependency, no library to import
- **Not a toolbox** — you don't pick tools, the workshop is pre-configured
- **Not multi-language** — Python only (for now)
- **Not multi-LLM** — Claude Code only (for now)
- **Not a CI/CD system** — local development focus

## Versioning

Currently one-shot: `copier copy` once, the project lives its life. No `copier update` mechanism in MVP. Upgrade path: generate a fresh project for new work, adapt older projects manually.

## Roadmap

**Phase A (MVP) — Done:**
- 4 profiles (minimal, app, data, quant)
- CLAUDE.md (law) + GUIDELINES.md (mentor)
- PILOT.md + SESSION-CONTEXT.md (context)
- 5 skills (brainstorm, plan, ship, lint, test)
- Auto-setup (uv sync + pre-commit install)

**Phase C (v2) — Planned:**
- Skills T2: /spec, /tdd, /review, /debug, /consolidate
- Knowledge hierarchy: INDEX.md, /digest, /dream, /tidy
- GitHub Actions CI
- Profile-specific skills
- Multi-language templates
