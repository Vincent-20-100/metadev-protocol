# ARCHITECTURE.md — metadev-protocol

> Validated structural decisions and the reasoning behind each choice.
> For decisions still being explored → see `.meta/decisions/`

## Core vision

**"Separate the product from the process."**

A clean project maintains two distinct spheres:
- **The product** (`src/`, `tests/`, `docs/`) — what gets delivered, reviewed, stable
- **The process** (`.meta/`) — session notes, draft ideas, AI context

Polluting `src/` with work-in-progress code or the root with session notes
is the primary vector for cognitive debt and project instability.

---

## ADR-001: `copier` as template engine

**Status:** Accepted
**Date:** 2026-04-01

**Context:** The repo needs to generate typed projects (minimal, app, data, quant) from
a common base. Several approaches were considered.

**Decision:** `copier` (Python), no orphan branches, no shell scripts.

**Reasoning:**
- **Orphan branches** require cherry-picking every improvement to each branch — one hook update = 4 manual operations. Fragile.
- A **shell script** is untyped, not versioned properly, shell-dependent.
- **`copier`** is declarative (`copier.yml`), supports Jinja2 for conditionals, and enables `copier update` to propagate template improvements to existing projects.

**Consequence:** A single template with `{% if project_type == "quant" %}` blocks.
Maximum maintainability — one source of truth.

---

## ADR-002: `.meta/` mandatory in every project

**Status:** Accepted
**Date:** 2026-04-01

**Context:** Vibe-coding sessions accumulate drafts, notes, intermediate versions
that pollute the repo.

**Decision:** Every generated project contains a `.meta/` at root.

**Contents:**
```
.meta/
├── PILOT.md        # Project state — versioned, updated each session
├── SESSION-CONTEXT.md  # Living context — rewritten each session
├── GUIDELINES.md   # Advisory best practices
├── sessions/       # Past session archives — versioned
├── decisions/      # Incubating ADRs — versioned
└── scratch/        # Temporary drafts — .gitignored
```

**Gitignore rule:**
```gitignore
.meta/scratch/*
!.meta/scratch/.gitkeep
```

**Anti-pattern to avoid:** Ignoring all of `.meta/` (loss of session memory)
or versioning `scratch/` (git log pollution).

---

## ADR-003: `CLAUDE.md` as session contract

**Status:** Accepted
**Date:** 2026-04-01

**Context:** Claude Code automatically reads `CLAUDE.md` at every session initialization.
This file is the primary entry point for contextualizing the AI.

**Decision:** `CLAUDE.md` at the root of every generated project, with two companion files.

**Design principles:**
1. **CLAUDE.md is the law** — few rules, non-negotiable, the LLM obeys
2. **GUIDELINES.md is the mentor** — best practices, proposed not imposed
3. **Automatisms over instructions** — hard-wired behaviors the LLM applies without being asked

**Mandatory sections:**
1. First action (read PILOT.md + SESSION-CONTEXT.md)
2. Automatisms (8 hard-wired behaviors)
3. Rules (8 universal dev rules, max)
4. Architecture (project tree)
5. Skills (available commands)
6. Commands (build, test, lint)
7. Guidelines pointer

---

## ADR-004: 4 project profiles in `copier.yml`

**Status:** Accepted
**Date:** 2026-04-01

**Context:** Guardrail, dependency, and structure needs diverge significantly
between a quick side-project and a serious quant project.

**Decision:** 4 profiles — `minimal`, `app`, `data`, `quant`.

| Profile | Use case | Guardrails | Dependencies |
|---------|----------|-----------|--------------|
| `minimal` | Side project, experimentation | ruff only | stdlib + pytest |
| `app` | API, backend, web | ruff + pyright + tests | fastapi, pydantic, httpx |
| `data` | ETL, pipelines | ruff + data validation | polars, duckdb |
| `quant` | Backtesting, modeling | ruff + shape checks | numpy, pandas, matplotlib |

**Rule:** The `minimal` profile never receives heavy dependencies.
If a side-project grows, migrate to the right profile — don't bloat minimal.

---

## ADR-005: `uv` exclusively

**Status:** Accepted
**Date:** 2026-04-01

**Decision:** `uv` as the sole package and environment manager.
No direct pip, no poetry, no conda.

**Reasoning:** Speed (Rust), native lockfile (`uv.lock`), replaces pip + venv + virtualenv
in a single command, conforms to `pyproject.toml` PEP 517/518 standard.
`uv_build` as build backend for generated projects (pure Python).

---

## ADR-006: Skills T1 — workflow automation

**Status:** Accepted
**Date:** 2026-04-02

**Decision:** 5 skills shipped with every generated project.

| Skill | Purpose | Output |
|-------|---------|--------|
| `/brainstorm` | Socratic exploration, one question at a time, 2-3 alternatives, YAGNI | `.meta/scratch/brainstorm.md` |
| `/plan` | Task decomposition with file mapping and verification steps | `.meta/scratch/plan.md` |
| `/ship` | Pre-commit checklist + PILOT.md update + SESSION-CONTEXT.md rewrite | Updated `.meta/` files |
| `/lint` | `ruff check --fix` + `ruff format` on the whole project | Terminal report |
| `/test` | `pytest` runner with optional arguments | Terminal report |

**Principle:** Skills are the right place for dev workflow. Not CLAUDE.md (too short, always loaded), not hooks (too rigid). Skills are loaded on demand, shared via git, composable.

---

## Explicitly out of scope

- **CI/CD** on this template repo: unjustified overhead for solo development
- **Automated template tests**: `copier copy . /tmp/test --defaults` locally is sufficient
- **Multi-language**: this template is Python-only, intentionally
- **Docker** in minimal profile: don't over-engineer small projects
- **Multi-LLM support**: Claude Code only for MVP (.cursorrules later)
