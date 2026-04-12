# CLAUDE.md — metadev-protocol

> Read automatically by Claude Code at every session.

## This repo is recursive

`metadev-protocol` is a **template system** for bootstrapping AI-assisted Python projects.
It applies the method to build the method. What you work on here becomes the standard
for all future projects.

## First action

Read `.meta/PILOT.md` then `.meta/ARCHITECTURE.md`. Do nothing before.

## Two spheres, two rules

| Sphere | Content | Rule |
|--------|---------|------|
| `template/` | What gets copied into new projects | Stable, tested, intentional |
| `.meta/` | Development cockpit for THIS repo | Ephemeral, draft, OK |

## Architecture

```
metadev-protocol/
├── template/                    # Injected into new projects
│   ├── CLAUDE.md.jinja          # Session contract for generated projects
│   ├── pyproject.toml.jinja     # Dependencies per profile
│   ├── .gitignore.jinja
│   ├── .pre-commit-config.yaml  # Pre-commit config (copied as-is)
│   ├── .meta/
│   │   ├── PILOT.md.jinja       # Project dashboard
│   │   ├── SESSION-CONTEXT.md.jinja  # Living context
│   │   ├── GUIDELINES.md.jinja  # Advisory best practices
│   │   ├── active/.gitkeep
│   │   ├── archive/.gitkeep
│   │   ├── drafts/.gitkeep
│   │   ├── decisions/.gitkeep
│   │   └── references/{raw,interim,synthesis}/
│   ├── .claude/
│   │   ├── settings.json.jinja  # Permissions + hooks
│   │   └── skills/              # brainstorm, plan, ship, lint, test
│   ├── src/{{ project_slug }}/  # Package source
│   └── tests/                   # Test suite
├── .meta/                       # Development cockpit for THIS repo
│   ├── PILOT.md                 # Current state → READ FIRST
│   ├── ARCHITECTURE.md          # Validated architectural decisions
│   ├── DECISIONS.md             # ADR journal
│   ├── GUIDELINES.md            # Advisory practices
│   ├── active/                  # Validated artifacts, not yet archived
│   ├── archive/                 # Implemented / historical
│   ├── drafts/                  # WIP — gitignored
│   ├── decisions/               # Individual ADRs (adr-NNN-slug.md)
│   └── references/              # raw/ · interim/ · synthesis/
├── CLAUDE.md                    # This file
├── copier.yml                   # Template engine (init questions)
├── pyproject.toml               # Meta-repo dependencies
└── .pre-commit-config.yaml      # Meta-repo pre-commit config
```

## Rules

1. **No temp files at root** — WIP goes in `.meta/drafts/` (gitignored). Validated artifacts in `.meta/active/`, implemented in `.meta/archive/`. Filename format: `<type>-<YYYY-MM-DD>-<slug>.md` (types: spec, plan, brainstorm, debate, session) — enforced by `scripts/check_meta_naming.py`
2. **`template/` only receives validated work** — test with `copier copy . /tmp/test-proj --defaults` before committing
3. **Modify template = test template** — any change in `template/` triggers a local generation test
4. **Commit per logical unit** — one feature/fix/decision = one commit (not per file, not per timer). Must be reviewable in <5 minutes and bisectable (tests pass independently). Conventional format: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`. The plan determines granularity — decompose upfront, not in git
5. **All template output in English** — code, docs, skills, comments
6. **YAGNI** — no over-engineering, complexity must be justified
7. **Semver tags are immutable** — never rewrite or move a tag, always bump the version
8. **Tag every release** — after merging a set of features, create a semver tag with an annotated message summarizing changes. This is mandatory: `copier update` relies on tags to diff versions for external projects
9. **Tag message = changelog** — the annotated tag message must list what changed (added, changed, removed, fixed) so external projects can review before updating

## Versioning

Template versions use semver tags (`v0.1.0`, `v0.2.0`, etc.).
External projects depend on these tags for `copier update` diffs.

```bash
# After merging features, tag the release:
git tag -a v0.X.0 -m "$(cat <<'EOF'
v0.X.0 — Short title

Added:
- ...

Changed:
- ...

Fixed:
- ...
EOF
)"
git push origin v0.X.0
```

Every tag is permanent. If a tag is wrong, bump to the next version.

## Stack

- Python >= 3.13
- `uv` exclusively (no pip, no poetry, no conda)
- `ruff` for lint + format
- `copier` for template generation
- `pre-commit` for git hooks

## Commands

```bash
uv sync                                    # Install dependencies
uv run ruff check .                        # Linter
uv run ruff format .                       # Formatter
copier copy . /tmp/test-proj --defaults    # Test template locally
```

## What you do NOT do here

- No application code — this repo is configuration and templates only
- No notebooks — wrong signal in a standards repo
- No global package installs — everything goes through `uv run`
- No changes to `template/` without testing the generation output
