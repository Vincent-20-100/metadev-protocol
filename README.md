# metadev-protocol

A pre-configured workshop for AI-assisted Python projects. One command, you're ready to build.

## What it does

```bash
copier copy gh:Vincent-20-100/metadev-protocol my-project --trust
```

Answer 5 questions (name, type, author, Python version) and get:

- **CLAUDE.md** — session contract with hard-wired automatisms (context management, architecture sync, conventional commits)
- **GUIDELINES.md** — advisory best practices the LLM draws from naturally
- **`.meta/`** — session cockpit (PILOT.md dashboard + SESSION-CONTEXT.md living context)
- **`.claude/`** — auto-ruff hooks, permissions, 5 skills (/brainstorm, /plan, /ship, /lint, /test)
- **pyproject.toml** — profile-specific dependencies, ready for `uv sync`
- **pre-commit** — ruff + trailing-whitespace + check-yaml + no-commit-to-branch
- **src/ + tests/** — proper package layout with placeholder test

## Profiles

| Profile | Dependencies | Guardrails |
|---------|-------------|------------|
| **minimal** | pytest, ruff, pre-commit | Universal rules only |
| **app** | + fastapi, uvicorn, pyright | Thin routing, dependency injection |
| **data** | + polars, duckdb | Idempotent pipelines, immutable raw data |
| **quant** | + numpy, pandas, matplotlib | Vectorization, document math assumptions |

## Quick start

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Generate a project
copier copy gh:Vincent-20-100/metadev-protocol my-project --trust

# Launch Claude Code
cd my-project
claude
```

Dependencies install automatically at generation. If `uv` is not in PATH, the generator tells you how to install it.

## What gets generated

```
my-project/
├── CLAUDE.md                       # Session contract (automatisms + rules)
├── pyproject.toml                  # Deps per profile, ruff + pytest config
├── .pre-commit-config.yaml         # ruff + pre-commit-hooks
├── .gitignore
├── src/my_project/__init__.py      # Package entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Shared fixtures
│   └── test_placeholder.py        # Starter test
├── .claude/
│   ├── settings.json               # Permissions + auto-ruff hook
│   └── skills/                     # brainstorm, plan, ship, lint, test
└── .meta/
    ├── PILOT.md                    # Project dashboard (read first)
    ├── SESSION-CONTEXT.md          # Living context (rewritten each session)
    ├── GUIDELINES.md               # Recommended practices (advisory)
    ├── decisions/                   # ADRs
    ├── sessions/                    # Session archives
    └── scratch/                     # Drafts (gitignored)
```

## Philosophy

**The LLM follows the workflow without being told.** CLAUDE.md encodes automatisms (read context first, plan before coding, update context at end of session). The user doesn't remind — the system does.

**Separate product from process.** Code (`src/`, `tests/`) is the deliverable. The cockpit (`.meta/`) is the AI workspace. They never mix.

**Hooks over instructions.** Critical rules (formatting, lint) are automatic hooks, not lines in CLAUDE.md the AI can ignore.

**Law and mentor.** CLAUDE.md is the law (few rules, non-negotiable). GUIDELINES.md is the mentor (best practices, proposed not imposed).

## Stack

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) — dependency management and venv
- [ruff](https://github.com/astral-sh/ruff) — lint + format
- [copier](https://github.com/copier-org/copier) — template generation
- [pre-commit](https://pre-commit.com/) — git hooks
- [Claude Code](https://claude.ai/code) — AI assistant

## Architectural decisions

ADRs are in `.meta/decisions/`:
- **ADR-001** — Patterns selected from EgoVault + state of the art
- **ADR-002** — `.claude/` directory config (permissions, hooks, skills)
- **ADR-003** — CLAUDE.md sizing, anti-LLM rules, 2-file cockpit
- **ADR-004** — Tiered pattern matrix (T1-T4 x vanilla/profile/user)
- **ADR-005** — Knowledge hierarchy brainstorm
- **ADR-006** — Strategic brainstorm: project direction and identity
- **ADR-007** — MVP Phase A specification

## Development

```bash
uv sync                                            # Install deps
uv run ruff check .                                # Lint
uv run ruff format .                               # Format
copier copy . /tmp/test --defaults --trust          # Test template
```
