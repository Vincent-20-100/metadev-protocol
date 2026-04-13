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

- The LLM knows how to behave (`CLAUDE.md` encodes the automatisms and rules)
- Context survives between sessions (`PILOT.md` + `SESSION-CONTEXT.md`)
- The workflow is automated, not explained (skills and agents handle the process)
- The product and the process never mix (`src/` vs `.meta/`)
- Dangerous drift is caught before commit (hooks over prose)

It's not a toolbox where you pick what you need. It's an opinionated workshop where everything is pre-installed and ready. The LLM follows the workflow naturally — the user doesn't remind.

## Three pillars

Every project built with metadev-protocol stands on three commitments:

- **Product excellence** — *"Ship less, ship better. Every feature earns its place."*
- **Technical agility** — *"Small, reversible decisions over big upfront designs. Optimize for changeability, because the first architecture will be wrong."*
- **AI intensity** — *"The human role shifts from doing to directing, reviewing, and deciding."*

These are not aspirations — they are constraints on every session.
<!-- Source: Guillaume Desforges / claude-ai-project-starter, absorbed 2026-04-13 -->

## Core principles

### 1. Separate the product from the process

The most important principle. A clean project has two spheres:

| Sphere | Contains | Rule |
|--------|----------|------|
| **Product** (`src/`, `tests/`, `docs/`) | What gets delivered | Stable, reviewed, tested |
| **Process** (`.meta/`) | How it gets built | Ephemeral, draft, AI workspace |

They never mix. Code doesn't live in `.meta/drafts/`. Session notes don't live at root. This separation is the primary defense against cognitive debt.

### 2. Law and mentor

Instructions to the LLM split into two authority levels:

- **`CLAUDE.md` is the law.** 11 automatisms + 9 rules, non-negotiable. The LLM obeys without question. These cover what matters most: context management, plan-before-edit, commit format, honesty constraint, anti-consensus bias.
- **`GUIDELINES.md` is the mentor.** Best practices proposed, not imposed. The LLM draws from them naturally and suggests them when relevant. "Prefer X over Y because Z" — never "you MUST."

Why two files? Too many rules in one file and the LLM ignores them. Too few and important practices get lost. The split gives precision where it matters (law) and breadth where it helps (mentor).

### 3. Automatisms over instructions

The LLM should do the right thing without being asked. `CLAUDE.md` encodes **11 hard-wired behaviors**:

1. **Session start** — read `PILOT.md` + `SESSION-CONTEXT.md` before any action; flag pending-plan conflicts
2. **First session** — detect the flag and offer a conversational intro
3. **Superpowers plugin** — recommend `/install-plugin obra/superpowers` if not present
4. **Before any edit** — follow the TRIVIAL/STANDARD/COMPLEX decision tree; plan-validated = all actions validated
5. **Milestone completed** — update `PILOT.md`
6. **End of session** — rewrite `SESSION-CONTEXT.md`
7. **Every commit** — one complete logical unit, conventional format, bisectable
8. **Architecture changes** — create/maintain `.meta/ARCHITECTURE.md`
9. **Context recall** — check `.meta/archive/` before asking the user
10. **Rule of 3** — after 3 consecutive user agreements without friction, auto-invoke devil's-advocate (anti-consensus bias)
11. **Always** — apply rules and draw from `.meta/GUIDELINES.md`

The user doesn't say "read the context" or "update the status." The system does.

### 4. Hooks over instructions

Critical rules that the LLM might ignore (formatting, lint, secret leaks, author identity) are enforced by hooks, not written in `CLAUDE.md`. A `PostToolUse` hook runs ruff after every file edit. Pre-commit runs ruff, `check_git_author` (blocks Claude/Anthropic authorship), `check_meta_naming`, and `audit_public_safety` (secret scan) before every commit.

If it's important enough to never skip, make it a hook. If it's important but contextual, make it a rule. If it's advice, make it a guideline.

### 5. Skills and agents are the workflow layer

Skills (`.claude/skills/`) and agents (`AGENTS.md`) are the right place for dev workflow:
- **Not `CLAUDE.md`** — too short, always loaded, can't hold process details
- **Not hooks** — too rigid, can't handle interactive workflows
- **Skills and agents** — loaded on demand, shared via git, composable in pipelines

**10 built-in skills** ship with every project:

| Skill | When | What it does |
|-------|------|-------------|
| `/brainstorm` | Idea is vague | One question at a time, 2-3 alternatives, YAGNI |
| `/spec` | Scope needs formalization | MoSCoW requirements |
| `/debate` | Hard trade-off with 2+ defensible options | 3-agent adversarial debate (2 insiders + 1 lone wolf) |
| `/plan` | Scope is clear | Tasks with file mapping and verification checklist |
| `/orchestrate` | Multi-step objective spanning phases | Session orchestrator with dependency tracking |
| `/research` | Question needs external facts or recent state-of-the-art | WebSearch + WebFetch + MCP, 8-call soft budget, output to `.meta/references/raw/` |
| `/vision` | Vision section empty or product framing unclear | Guided dialogue → fills Problem / Target user / V1 scope / North star in PILOT.md |
| `/test` | After implementation | Run pytest with optional arguments |
| `/lint` | Before commit or after touching >1 file | `ruff check` + `format` on the whole project |
| `/save-progress` | End of session | Checklist + `PILOT.md` + rewrite `SESSION-CONTEXT.md` |

**5 agent personas** defined in `AGENTS.md`, invoked on demand:

| Agent | When |
|-------|------|
| `code-reviewer` | ≥3 files touched, or plan step completed |
| `test-engineer` | New module, new public API, missing coverage |
| `security-auditor` | Auth, secrets, input validation, crypto, network boundaries |
| `data-analyst` | Pipeline, ETL, metric computation, statistical claim |
| `devil's-advocate` | Auto-triggered by Rule of 3 (automatism #10) |

**Discoverability.** `CLAUDE.md` embeds an inverted-default trigger table (observable signals → Auto/Propose action) scanned before every response, so the LLM proactively surfaces relevant skills and agents instead of waiting to be asked.

**Superpowers plugin.** More thorough versions of brainstorming, planning, debugging, code review, and TDD are delegated to the [Superpowers plugin](https://github.com/obra/superpowers) (`/install-plugin obra/superpowers`). Built-in skills remain as fallbacks when the plugin is not installed.

### 6. Context survives sessions

Three files maintain project memory:

- **`PILOT.md`** — the dashboard. Where the project stands, what's next, what's done. Updated after milestones.
- **`SESSION-CONTEXT.md`** — the living context. Architecture snapshot, active decisions, traps, open questions. Rewritten (not appended) each session.
- **`.meta/ARCHITECTURE.md`** — created when architecture is defined. The LLM maintains it and checks for divergence.

`.meta/archive/` preserves historical plans, specs, debates, and session records by date — so a new session can read past decisions before asking the user (automatism #9).

Together, these mean a new session starts with full context — even after compaction, machine change, or weeks of inactivity.

### 7. Progressive disclosure

Not everything loads at once:

| Layer | When loaded | Size |
|-------|-----------|------|
| `CLAUDE.md` | Every session, automatically | ~170 lines |
| `PILOT.md` + `SESSION-CONTEXT.md` | Session start (automatism #1) | Variable |
| `GUIDELINES.md` | On demand (automatism #11) | ~200 lines |
| Skills | On demand (`/brainstorm`, `/plan`, etc.) | 30–500 lines each |
| Agents | On demand (`Task` tool) | ~50 lines each |
| `.meta/archive/` | When needed (automatism #9) | Variable |

This hierarchy respects the LLM's context window. The essential is always present. The detailed is available on demand.

## Design decisions

Every structural choice has a rationale documented in `.meta/decisions/`:

| ADR | Decision | Key reasoning |
|-----|---------|--------------|
| 001 | Patterns from EgoVault + state of the art | Curated from 15 references, 5 gold syntheses |
| 002 | `.claude/` directory in template | Permissions, hooks, skills — shared via git |
| 003 | `CLAUDE.md` sizing + 2-file cockpit | Law + living context |
| 004 | Tiered pattern matrix (T1–T4) | Prioritize what to implement first |
| 005 | Knowledge hierarchy brainstorm | `INDEX.md`, `/digest`, `/dream` — deferred |
| 006 | Strategic brainstorm | Audience B/C, "brand new workshop", English default |
| 007 | MVP Phase A specification | Full spec for every template file |
| 008 | Settings v2 | Permissions tiering, attribution suppression, hooks |
| 009 | Universal architecture | Single universal template replaces 4 profiles |

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

Template versions use semver tags (`v1.0.0`, `v1.1.0`, …). External projects depend on these tags for `copier update` diffs — template improvements are propagated to existing projects by re-running `copier update`, which surfaces a reviewable diff and resolves conflicts interactively. Tags are immutable by rule: never rewrite or move a tag, always bump the version.

## Roadmap

**v1.0.0 — First public release (2026-04-08).** Execution modes (safe/full-auto), public safety audit (script + pre-commit + 2 GitHub Actions), `.meta/` taxonomy with filename enforcement, `meta_visibility` copier parameter, workflow gates with tiered decision tree, publication files (CREDITS, CONTRIBUTING, CODE_OF_CONDUCT, CONTRIBUTORS).

**v1.0.1 — Governance polish (2026-04-09).** Honesty constraint (Rule #9), tiered confidence gates, synthesis artifact type with slug lineage, brand guide, demo script, banner.

**v1.1.0 — Skill discoverability + README rework (2026-04-12).** Inverted-default trigger table for the 8 skills and 5 agents, automatism #11 (Rule of 3 anti-consensus), pixel-art banner with embedded font, Before/After + Rails diagrams.

**Phase 4 — Public launch (in progress).** Beta outreach to curated contacts, draft posts (LinkedIn, X, Reddit, HN), demo GIF, public launch sequence.

**Post-merge backlog.** `/audit-repo` skill for cross-pollination, tech watch script, multi-agent synthesis run across reference sources, provenance sidecar convention. See `.meta/PILOT.md` for live status.
