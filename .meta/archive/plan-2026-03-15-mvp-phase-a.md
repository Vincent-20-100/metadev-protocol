# MVP Phase A — Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform all template/ files into a fully functional, English-first Python project generator with 4 skills and sharp automatisms.

**Architecture:** Single copier template in `template/` with Jinja2 conditionals for 4 profiles. CLAUDE.md is the law (automatisms + rules), GUIDELINES.md is the mentor (advisory). Skills in `.claude/skills/`. All output in English.

**Tech Stack:** copier, Jinja2, uv, ruff, pre-commit, Python 3.13+

**Spec:** `.meta/scratch/mvp-phase-a-spec.md`

---

## Files involved

| File | Action | Purpose |
|------|--------|---------|
| `template/CLAUDE.md.jinja` | Rewrite | Session contract — automatisms + rules |
| `template/.meta/GUIDELINES.md.jinja` | Create | Mentor file — advisory practices |
| `template/.meta/PILOT.md.jinja` | Rewrite | Project dashboard with first_session flag |
| `template/.meta/SESSION-CONTEXT.md.jinja` | Rewrite | Living context with architecture snapshot |
| `template/pyproject.toml.jinja` | Modify | uv_build backend + ruff/pytest config |
| `template/src/{{ project_slug }}/__init__.py.jinja` | Create | Package entry point |
| `template/.pre-commit-config.yaml` | Modify | Add pre-commit-hooks repo |
| `copier.yml` | Modify | English questions + auto-setup tasks |
| `template/.claude/skills/brainstorm/SKILL.md` | Create | /brainstorm skill |
| `template/.claude/skills/plan/SKILL.md` | Create | /plan skill |
| `template/.claude/skills/ship/SKILL.md` | Create | /ship skill |
| `template/.claude/skills/lint/SKILL.md` | Create | /lint skill |
| `template/.claude/settings.json.jinja` | Modify | Add .meta/ permissions, remove compact hook |
| `template/.gitignore.jinja` | Modify | Translate comments to English |

---

## Task 1: Rewrite CLAUDE.md.jinja

The core file. Everything else references it.

**Files:**
- Rewrite: `template/CLAUDE.md.jinja`

- [ ] **Step 1: Replace the entire file with the new English version**

```jinja
# CLAUDE.md — {{ project_name }}

> Read automatically by Claude Code at every session.

## First action

Read `.meta/PILOT.md` then `.meta/SESSION-CONTEXT.md`. Do nothing before.

## Automatisms

These behaviors are mandatory. Apply them without being asked.

1. **Session start** — read PILOT.md + SESSION-CONTEXT.md before any action
2. **First session** — if `first_session: true` in PILOT.md, offer a conversational intro: project structure, available skills, how a session works. Then set the flag to `false`
3. **Before coding** — propose a plan before implementing. If scope is unclear, suggest `/brainstorm` first
4. **Milestone completed** — update PILOT.md (status table, objectives, next steps)
5. **End of session** — rewrite SESSION-CONTEXT.md: architecture snapshot, active decisions, traps, open questions
6. **Every commit** — conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
7. **Architecture changes** — if `.meta/ARCHITECTURE.md` doesn't exist and architecture is defined, create it. Keep it in sync with the code. On divergence, ask the user: if intentional, rewrite the file; if not, guide back to the defined architecture
8. **Always** — apply the rules below and draw from `.meta/GUIDELINES.md`

## Rules

Non-negotiable. These apply to every action.

1. **Single responsibility** — one function, one purpose
2. **Config over hardcode** — prefer yaml/toml config files over scattered variables
3. **Minimize hardcoding** — anything that can change = config or parameter
4. **No silent errors** — every `except` logs or re-raises
5. **Conventional commits** — always
6. **Drafts in `.meta/scratch/`** — never at root, never in `src/`
7. **Docstrings: WHAT not HOW** — describe purpose, not implementation
8. **YAGNI** — no over-engineering, complexity must be justified

## Architecture

```
{{ project_slug }}/
├── src/{{ project_slug }}/    # Validated source code
├── tests/                     # Mirror of src/ — one test per module
├── .meta/
│   ├── PILOT.md               # Project dashboard (READ FIRST)
│   ├── SESSION-CONTEXT.md     # Living context (rewritten each session)
│   ├── GUIDELINES.md          # Recommended practices (advisory)
│   ├── decisions/             # ADRs
│   ├── sessions/              # Session archives
│   └── scratch/               # Drafts (gitignored)
{% if project_type == "app" %}├── config/
│   ├── system.yaml            # App config (versioned)
│   ├── user.yaml.example      # User prefs (gitignored)
│   └── install.yaml.example   # Secrets and paths (gitignored)
{% endif %}├── CLAUDE.md
└── pyproject.toml
```

## Skills

```
/brainstorm  — structured exploration before coding (one question at a time)
/plan        — break work into tasks with verification steps
/ship        — pre-commit checklist + context update (does NOT commit)
/lint        — ruff check + format on the whole project
/test        — run pytest
```

## Commands

```bash
uv sync                     # Install dependencies
uv run ruff check .         # Linter
uv run ruff format .        # Formatter
uv run pytest               # Tests
```

## Guidelines

Read `.meta/GUIDELINES.md` — it contains recommended practices.
Apply them when relevant. They are suggestions, not rules.
```

- [ ] **Step 2: Verify the file renders correctly with Jinja2 syntax**

Check: no raw `{{` outside of Jinja variable blocks, conditionals close properly, profile-specific blocks (app/quant/data) are correct.

- [ ] **Step 3: Commit**

```bash
git add template/CLAUDE.md.jinja
git commit -m "feat: rewrite CLAUDE.md.jinja — English, automatisms, rules, skills"
```

---

## Task 2: Create GUIDELINES.md.jinja

The mentor file — advisory, not directive.

**Files:**
- Create: `template/.meta/GUIDELINES.md.jinja`

- [ ] **Step 1: Create the file**

```jinja
# Guidelines — {{ project_name }}

> These are recommended practices, not rules. Apply when relevant.
> Draw from these naturally and suggest them when appropriate.

## Code structure

- Prefer small, focused functions over long ones
- Group related logic in modules, not mega-files
- Keep entry points thin — route to logic, don't contain it
- When a function grows beyond ~30 lines, consider splitting

## Configuration

- Centralize config in files (yaml/toml), not scattered constants
- Separate concerns: system config vs user preferences vs secrets
- Use environment variables for deployment-specific values only

## Naming and clarity

- Names should reveal intent — avoid abbreviations
- A good name removes the need for a comment
- Consistent vocabulary: pick one term per concept, stick to it

## Error handling

- Handle errors at the right level — not too early, not too late
- Prefer explicit error types over generic exceptions
- Log context: what was attempted, what failed, what was the input

## Testing

- Test behavior, not implementation
- One assertion per test when possible
- Name tests as sentences: `test_should_reject_negative_amounts`

## Refactoring signals

- When you copy-paste: extract
- When a file exceeds ~200 lines: consider splitting
- When you add a parameter to avoid changing logic: reconsider the design
- Ask the user before large refactors — propose, don't impose

## Working with the user

- When the request is vague, ask a clarifying question before coding
- Propose 2-3 approaches for non-trivial decisions
- Explain trade-offs, let the user decide
- After completing work, suggest what to verify
```

- [ ] **Step 2: Commit**

```bash
git add template/.meta/GUIDELINES.md.jinja
git commit -m "feat: add GUIDELINES.md.jinja — advisory best practices"
```

---

## Task 3: Rewrite PILOT.md.jinja

**Files:**
- Rewrite: `template/.meta/PILOT.md.jinja`

- [ ] **Step 1: Replace the entire file**

```jinja
# PILOT.md — {{ project_name }}

**Date:** YYYY-MM-DD
**Phase:** Initialization
**first_session:** true

---

## Current objectives

Define your first session objective here.

---

## Project state

| Component | Status | Notes |
|-----------|--------|-------|
| Repo created | ✅ | Via metadev-protocol |
| Dependencies installed | ✅ | `uv sync` ran at generation |
| Pre-commit installed | ✅ | `pre-commit install` ran at generation |
| First module in `src/` | ❌ | |

---

## Next steps

1. Define the project goal
2. Sketch the initial architecture in `.meta/decisions/`
3. Start the first module

---

## Session notes

- Project generated with metadev-protocol (profile: {{ project_type }})
- Stack: Python {{ python_version }} | uv | ruff
```

- [ ] **Step 2: Commit**

```bash
git add template/.meta/PILOT.md.jinja
git commit -m "feat: rewrite PILOT.md.jinja — English, first_session flag"
```

---

## Task 4: Rewrite SESSION-CONTEXT.md.jinja

**Files:**
- Rewrite: `template/.meta/SESSION-CONTEXT.md.jinja`

- [ ] **Step 1: Replace the entire file**

```jinja
# SESSION-CONTEXT.md — {{ project_name }}

> This file is **rewritten** (not appended) each session.
> It captures the living context — the WHY behind current decisions.
> Obsolete reasoning is removed.

---

## Architecture snapshot

<!-- Brief description of current modules and how they communicate -->
<!-- Created after first architectural decisions, empty at start -->

No architecture defined yet.

## Active decisions

<!-- Why current architectural choices were made -->
<!-- Format: "We do X because Y. Rejected alternative: Z." -->

No active decisions — fresh project.

## Traps to avoid

<!-- What has broken or could break -->
<!-- Format: "Don't do X — it causes Y (observed DATE)" -->

None identified.

## Open questions

<!-- What doesn't have an answer yet -->

None yet.
```

- [ ] **Step 2: Commit**

```bash
git add template/.meta/SESSION-CONTEXT.md.jinja
git commit -m "feat: rewrite SESSION-CONTEXT.md.jinja — English, architecture snapshot"
```

---

## Task 5: Update pyproject.toml.jinja

**Files:**
- Modify: `template/pyproject.toml.jinja`

- [ ] **Step 1: Switch build backend from hatchling to uv_build**

Replace:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

With:
```toml
[build-system]
requires = ["uv_build>=0.11.2,<0.12"]
build-backend = "uv_build"
```

- [ ] **Step 2: Add ruff configuration**

Append after the `[build-system]` block:

```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]

[tool.ruff.format]
quote-style = "double"
```

- [ ] **Step 3: Add pytest configuration**

Append after the ruff config:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- [ ] **Step 4: Commit**

```bash
git add template/pyproject.toml.jinja
git commit -m "feat: update pyproject.toml — uv_build backend, ruff + pytest config"
```

---

## Task 6: Create src package __init__.py

**Files:**
- Create: `template/src/{{ project_slug }}/__init__.py.jinja`

- [ ] **Step 1: Create the directory and file**

The file content:
```python
"""{{ project_name }}."""
```

Note: copier needs the directory to exist. The `{{ project_slug }}` in the path will be rendered by copier at generation time.

- [ ] **Step 2: Commit**

```bash
git add "template/src/{{ project_slug }}/__init__.py.jinja"
git commit -m "feat: add src/package/__init__.py template"
```

---

## Task 7: Enrich pre-commit-config.yaml

**Files:**
- Modify: `template/.pre-commit-config.yaml`

- [ ] **Step 1: Add pre-commit-hooks repo before the ruff repo**

Replace the entire file with:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: no-commit-to-branch
        args: [--branch, main]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

- [ ] **Step 2: Commit**

```bash
git add template/.pre-commit-config.yaml
git commit -m "feat: enrich pre-commit — trailing-whitespace, check-yaml, no-commit-to-branch"
```

---

## Task 8: Update copier.yml

**Files:**
- Modify: `copier.yml`

- [ ] **Step 1: Translate all questions to English, update defaults**

Replace the full questions section:

```yaml
# copier.yml — The Meta Protocol
# Project generator
# Usage: copier copy gh:Vincent-20-100/metadev-protocol my-new-project

# ─────────────────────────────────────────
# Init questions
# ─────────────────────────────────────────

project_name:
  type: str
  help: "Project name (e.g., egovault, price-tracker)"

project_slug:
  type: str
  help: "Python package slug (snake_case, no hyphens)"
  default: "{{ project_name | lower | replace('-', '_') | replace(' ', '_') }}"

project_type:
  type: str
  help: "Project type — determines guardrails and dependencies"
  choices:
    "Side project / Quick experiment": minimal
    "Web App / API / Backend": app
    "Data Engineering / ETL / Pipelines": data
    "Quantitative Analysis / Backtesting": quant
  default: minimal

author_name:
  type: str
  help: "Your first name (for pyproject.toml)"
  default: "Vincent"

python_version:
  type: str
  help: "Minimum Python version"
  default: "3.13"
```

- [ ] **Step 2: Update _tasks with uv check + auto-setup**

Replace the `_tasks` section:

```yaml
_tasks:
  - "git init"
  - >
    command -v uv >/dev/null 2>&1 && {
      uv sync && uv run pre-commit install &&
      echo '✅ Dependencies installed, pre-commit activated.';
    } || {
      echo '';
      echo '⚠️  uv not found.';
      echo 'Install it: curl -LsSf https://astral.sh/uv/install.sh | sh';
      echo 'Then run: uv sync && uv run pre-commit install';
    }
```

- [ ] **Step 3: Translate _message_after_copy**

```yaml
_message_after_copy: |
  ✅ Project {{ project_name }} created with The Meta Protocol.

  Next steps:
    1. cd {{ project_slug }}
    2. Open .meta/PILOT.md and define your first session goal
    3. Launch Claude Code: claude

  Stack: Python {{ python_version }} | uv | ruff | profile: {{ project_type }}
```

- [ ] **Step 4: Commit**

```bash
git add copier.yml
git commit -m "feat: translate copier.yml to English, add uv auto-setup"
```

---

## Task 9: Create /brainstorm skill

**Files:**
- Create: `template/.claude/skills/brainstorm/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```markdown
---
name: brainstorm
description: Structured exploration before coding — one question at a time
---

You are in BRAINSTORM mode. Your job is to explore the idea, not implement it.

## Hard rules

- Ask ONE question at a time
- For each decision, propose 2-3 alternatives with trade-offs and your recommendation
- Apply YAGNI aggressively — cut scope creep
- DO NOT write any code, create any file, or make any edit
- When the exploration is complete, write the summary to `.meta/scratch/brainstorm.md`

## Process

1. Understand the goal — ask what, why, for whom
2. Explore constraints — what's non-negotiable, what's flexible
3. For each design decision, present options with your recommendation
4. Validate the full picture with the user
5. Write brainstorm.md with: decisions taken, alternatives rejected (with reasons), open questions

## Output format

Write to `.meta/scratch/brainstorm.md`:

```
# Brainstorm — [topic]

**Date:** [date]

## Decisions

- **[Decision 1]:** [choice] — because [reason]. Rejected: [alternative] ([why])
- ...

## Open questions

- ...

## Next step

Run /plan to break this into tasks.
```
```

- [ ] **Step 2: Commit**

```bash
git add template/.claude/skills/brainstorm/SKILL.md
git commit -m "feat: add /brainstorm skill — socratic exploration"
```

---

## Task 10: Create /plan skill

**Files:**
- Create: `template/.claude/skills/plan/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```markdown
---
name: plan
description: Break work into concrete tasks with verification steps
---

You are in PLANNING mode. Your job is to decompose work into actionable tasks.

## Hard rules

- If `.meta/scratch/brainstorm.md` exists, read it first
- Map ALL files that will be created or modified BEFORE defining tasks
- Each task must have: file(s), what to do, how to verify
- Chunks should be 2-5 minutes of work
- Write the plan to `.meta/scratch/plan.md`
- DO NOT start implementing — plan only

## Process

1. Read brainstorm.md if it exists
2. Read the current codebase structure
3. List all files that will be touched
4. Break into ordered tasks with dependencies
5. Write plan.md
6. Ask user to validate before proceeding

## Output format

Write to `.meta/scratch/plan.md`:

```
# Plan — [topic]

**Date:** [date]
**Based on:** brainstorm.md (if applicable)

## Files involved

- `path/to/file.py` — create / modify (reason)
- ...

## Tasks

### 1. [Task title]
- **Files:** path/to/file.py
- **Do:** [concrete description]
- **Verify:** [how to check it works]

### 2. [Task title]
...
```

## Execution

When the user approves the plan, create a Task per item and execute in order.
Mark each task as completed as you go.
```

- [ ] **Step 2: Commit**

```bash
git add template/.claude/skills/plan/SKILL.md
git commit -m "feat: add /plan skill — task decomposition with verification"
```

---

## Task 11: Create /ship skill

**Files:**
- Create: `template/.claude/skills/ship/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```markdown
---
name: ship
description: Pre-commit checklist and context update — does NOT commit
allowed-tools: Bash(uv *), Bash(git status *), Read, Edit(.meta/**)
---

You are in SHIP mode. Verify everything is clean and update project context.

## Hard rules

- DO NOT create a commit — that is a separate action
- Run ALL checks before updating .meta/ files
- If any check fails, STOP and report — do not update .meta/

## Checklist

Run these in order:

1. `uv run pytest` — all tests must pass
2. `uv run ruff check .` — no lint errors
3. `uv run ruff format --check .` — no format issues
4. `git status` — check for untracked files that should be staged
5. Verify no drafts at root or code in `.meta/scratch/`

## If all checks pass

1. **Update PILOT.md:**
   - Update the status table
   - Update current objectives
   - Mark completed items
   - Add any new next steps

2. **Rewrite SESSION-CONTEXT.md:**
   - Architecture snapshot (current modules and how they connect)
   - Active decisions (why current choices were made)
   - Traps to avoid (what broke or could break)
   - Open questions (what still needs answers)

3. **Report:** "Ready to commit. Run `git add` and `git commit` or ask me to commit."
```

- [ ] **Step 2: Commit**

```bash
git add template/.claude/skills/ship/SKILL.md
git commit -m "feat: add /ship skill — checklist + context update"
```

---

## Task 12: Create /lint skill

**Files:**
- Create: `template/.claude/skills/lint/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```markdown
---
name: lint
description: Run ruff check + format on the whole project
allowed-tools: Bash(uv *)
---

Run the full linting suite:

```bash
uv run ruff check . --fix
uv run ruff format .
```

Report:
- Number of issues found and fixed
- Any remaining issues that need manual attention
- Files modified by the formatter
```

- [ ] **Step 2: Commit**

```bash
git add template/.claude/skills/lint/SKILL.md
git commit -m "feat: add /lint skill — ruff check + format"
```

---

## Task 13: Update settings.json.jinja

**Files:**
- Modify: `template/.claude/settings.json.jinja`

- [ ] **Step 1: Add .meta/ edit permissions and remove SessionStart compact hook**

Replace the entire file with:

```json
{
  "permissions": {
    "allow": [
      "Bash(uv *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Read",
      "Edit(src/**)",
      "Edit(tests/**)",
      "Edit(.meta/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Edit(.env)",
      "Edit(.git/**)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | xargs -I {} sh -c 'case \"{}\" in *.py) uv run ruff format \"{}\" 2>/dev/null && uv run ruff check \"{}\" --fix 2>/dev/null;; esac; exit 0'"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add template/.claude/settings.json.jinja
git commit -m "feat: update settings.json — add .meta/ permissions, remove compact hook"
```

---

## Task 14: Translate .gitignore.jinja comments

**Files:**
- Modify: `template/.gitignore.jinja`

- [ ] **Step 1: Translate French comments to English**

Replace:
```gitignore
# Environnement
```
With:
```gitignore
# Environment
```

Replace:
```gitignore
# Metadev
```
With:
```gitignore
# Meta protocol
```

- [ ] **Step 2: Commit**

```bash
git add template/.gitignore.jinja
git commit -m "docs: translate .gitignore comments to English"
```

---

## Task 15: Test full generation — all profiles

**Files:**
- No files modified — validation only

- [ ] **Step 1: Test minimal profile**

```bash
copier copy . /tmp/test-minimal --data project_name="test-minimal" --data project_type=minimal --defaults
cd /tmp/test-minimal
```

Verify:
- All files present (CLAUDE.md, GUIDELINES.md, PILOT.md, SESSION-CONTEXT.md, pyproject.toml, .pre-commit-config.yaml)
- Skills in `.claude/skills/` (brainstorm, plan, ship, lint, test)
- `src/test_minimal/__init__.py` exists
- CLAUDE.md is English with automatisms + rules
- PILOT.md has `first_session: true`
- pyproject.toml has `uv_build` backend + ruff/pytest config
- `uv sync` succeeds
- `uv run pytest` succeeds (0 tests collected, no errors)
- `uv run ruff check .` clean

- [ ] **Step 2: Test app profile**

```bash
copier copy . /tmp/test-app --data project_name="test-app" --data project_type=app --defaults
cd /tmp/test-app
```

Verify: same as minimal + config/ directory in architecture tree + app-specific deps (fastapi, uvicorn, pyright)

- [ ] **Step 3: Test data profile**

```bash
copier copy . /tmp/test-data --data project_name="test-data" --data project_type=data --defaults
cd /tmp/test-data
```

Verify: same as minimal + data-specific deps (polars, duckdb)

- [ ] **Step 4: Test quant profile**

```bash
copier copy . /tmp/test-quant --data project_name="test-quant" --data project_type=quant --defaults
cd /tmp/test-quant
```

Verify: same as minimal + quant-specific deps (numpy, pandas, matplotlib)

- [ ] **Step 5: Fix any issues found during testing**

If any profile fails, fix the template and re-test.

- [ ] **Step 6: Final commit if fixes were needed**

```bash
git add -A
git commit -m "fix: template adjustments from generation testing"
```

---

## Task 16: Update PILOT.md and commit spec

Update the meta-repo's own PILOT.md to reflect MVP completion.

- [ ] **Step 1: Update .meta/PILOT.md — mark all MVP items as done**

Set all 12 MVP scope items to ✅ and update the phase.

- [ ] **Step 2: Move spec from scratch to decisions**

```bash
cp .meta/scratch/mvp-phase-a-spec.md .meta/decisions/007-mvp-phase-a-spec.md
```

- [ ] **Step 3: Commit**

```bash
git add .meta/PILOT.md .meta/decisions/007-mvp-phase-a-spec.md
git commit -m "docs: mark MVP Phase A complete, archive spec as ADR-007"
```
