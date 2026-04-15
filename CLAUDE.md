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
│   │   └── skills/              # brainstorm, spec, debate, plan, orchestrate, research, vision, test, lint, save-progress
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

1. **No temp files at root** — WIP goes in `.meta/drafts/` (gitignored). Validated artifacts in `.meta/active/`, implemented in `.meta/archive/`. Filename format: `<type>-<YYYY-MM-DD>-<slug>.md` (types: spec, plan, brainstorm, debate, session, synthesis) — enforced by `scripts/check_meta_naming.py`
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

## Skills & Agents

This repo uses the same skills and agents as generated projects (loaded from
`template/.claude/skills/` via `projectSettings`). Dogfood them here.

**Default rule (inverted detection):** if the user's message does not name a specific
file, function, or concrete action, at least one tool below applies. Scan the trigger
table before responding. Over-proposing costs one "no thanks" — under-proposing defeats
the whole point of dogfooding the template.

| Tool | Type | Trigger (observable signal) | Action |
|---|---|---|---|
| `/brainstorm` | skill | goal, idea, concept, problem, or feature described without naming files/functions | **Propose** |
| `/spec` | skill | scope unclear OR request for a "feature" / "system" / "workflow" across multiple pieces | **Auto** |
| `/plan` | skill | change would touch >1 file OR a structural change in `template/` | **Auto** |
| `/debate` | skill | hard trade-off with 2+ defensible options, especially for template conventions | **Propose** |
| `/orchestrate` | skill | multi-step objective spanning spec + plan + implementation across phases | **Propose** |
| `/research` | skill | question needs external facts, recent state-of-the-art, or competitive info | **Propose** |
| `/vision` | skill | Vision section is empty OR user asks about product framing / target user / scope | **Propose** |
| `/audit-repo` | skill | user shares a GitHub repo URL to analyze OR tech-watch output surfaced a new candidate | **Propose** |
| `/test` | skill | template code or scripts modified and no test run has happened yet | **Auto** (after impl) |
| `/save-progress` | skill | end of session OR user says "stop", "pause", "on arrête" | **Propose** |
| `devil's-advocate` | agent | 3 consecutive user agreements without friction (Rule of 3) | **Auto** |
| `code-reviewer` | agent | ≥3 files touched in current plan, or a plan step just completed | **Auto** |
| `test-engineer` | agent | new module, new public API, or missing coverage on touched code | **Propose** |
| `security-auditor` | agent | auth, secrets, input validation, crypto, network boundaries, file uploads | **Propose** |
| `data-analyst` | agent | pipeline, ETL, metric computation, statistical claim, or dataset quality question | **Propose** |

**Auto** = invoke without asking (announce it in one line). **Propose** = ask first,
explaining why this tool applies. Never stay silent when a trigger matches.

**Rule of 3 (anti-consensus bias):** count consecutive user agreements without
friction. At 3 in a row, invoke the devil's-advocate agent before continuing. The
signal is countable (agreements, not topics) and the user will never self-request a
challenge — that's why it must fire automatically.

**Superpowers fallback relationship:** the local skills (`brainstorm`, `plan`, `spec`, `debate`, `orchestrate`, `research`, `test`, `save-progress`) are fallbacks — they work out-of-the-box. The `superpowers` plugin ships superior versions of the same workflows (`superpowers:brainstorming`, `superpowers:writing-plans`, `superpowers:executing-plans`, etc.); when installed, prefer its versions. The 4 local agents (`code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst`) are additive, not fallbacks — they stay local even with superpowers installed.

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
python scripts/tech_watch.py              # Fetch trending AI-coding repos (needs GITHUB_TOKEN in .env)
```

## What you do NOT do here

- No application code — this repo is configuration and templates only
- No notebooks — wrong signal in a standards repo
- No global package installs — everything goes through `uv run`
- No changes to `template/` without testing the generation output
