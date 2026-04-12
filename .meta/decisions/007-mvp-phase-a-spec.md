# MVP Phase A — Specification

**Date:** 2026-04-02
**Status:** DRAFT — pending review
**Scope:** All template/ files + copier.yml for a fully functional Python project generator

---

## Principles

1. **CLAUDE.md is the law** — few rules, non-negotiable, the LLM obeys
2. **GUIDELINES.md is the mentor** — best practices, proposed not imposed, the LLM draws from them
3. **Automatisms over instructions** — the LLM does the right thing without the user asking
4. **Sharp and minimal** — every line earns its place, no filler
5. **Python-first MVP** — language-specific templates (React, Go) come later
6. **Universal dev practices** — rules apply regardless of project type

---

## File-by-file specification

### 1. CLAUDE.md.jinja

**Role:** Session contract. The LLM reads this first and follows it as law.
**Target:** ~50 lines, English, sharp.

**Structure:**

```
# CLAUDE.md — {{ project_name }}

## First action
Read .meta/PILOT.md then .meta/SESSION-CONTEXT.md. Do nothing before.

## Automatisms
[8 hard-wired behaviors — see below]

## Rules
[8 universal dev rules — see below]

## Skills
[Available skills shortlist]

## Commands
[uv sync, ruff, pytest]

## Guidelines
Read .meta/GUIDELINES.md — it contains recommended practices. Apply them
when relevant. They are suggestions, not rules.
```

**Automatisms (hard-wired in CLAUDE.md):**

| # | Trigger | Behavior |
|---|---------|----------|
| 1 | Session start | Read PILOT.md + SESSION-CONTEXT.md before any action |
| 2 | `first_session: true` in PILOT.md | Offer a conversational intro: what the project structure is, what skills are available, how a session works |
| 3 | User asks for a feature or fix | Propose a plan before coding. If scope is unclear, suggest /brainstorm first |
| 4 | Milestone completed | Update PILOT.md (status table, objectives) |
| 5 | End of session (last commit or user signals done) | Rewrite SESSION-CONTEXT.md (architecture snapshot, active decisions, traps, open questions) |
| 6 | Every commit | Conventional commits format (feat:, fix:, docs:, chore:, refactor:) |
| 7 | Architecture is defined or changes structurally | Create .meta/ARCHITECTURE.md if it doesn't exist. Keep it in sync. On divergence: ask user — if assumed, rewrite the file; if not, guide back to the architecture |
| 8 | Any coding action | Apply rules below and draw from GUIDELINES.md |

**Rules (non-negotiable):**

| # | Rule |
|---|------|
| 1 | Single responsibility — separate functions, one purpose each |
| 2 | Config over hardcode — prefer yaml/toml config files over scattered variables |
| 3 | Hardcode the minimum — anything that can change = config or parameter |
| 4 | Every `except` logs or re-raises — never silent |
| 5 | Conventional commits — always |
| 6 | Drafts in `.meta/scratch/` — never at root, never in `src/` |
| 7 | Docstrings: WHAT not HOW |
| 8 | No over-engineering — complexity must be justified by a real need (YAGNI) |

**Skills shortlist (displayed in CLAUDE.md):**

```
Available skills:
  /brainstorm  — structured exploration before coding
  /plan        — break work into tasks with verification steps
  /ship        — pre-commit checklist + context update
  /lint        — ruff check + format on the whole project
  /test        — run pytest
```

**Profile-specific sections:**
Keep the current conditional blocks for architecture tree (app has config/, quant has different rules, etc.) but translated to English and trimmed to essentials.

---

### 2. .meta/GUIDELINES.md.jinja

**Role:** Mentor file. Best practices proposed, not imposed. The LLM reads it at session start and applies advice when relevant.
**Target:** ~60-80 lines, English, advisory tone.

**Tone:** "Prefer X over Y because Z" — never "you MUST".

**Sections:**

```
# Guidelines — {{ project_name }}

> These are recommended practices, not rules. Apply when relevant.
> The LLM should draw from these naturally and suggest them when appropriate.

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
- Name tests as sentences: test_should_reject_negative_amounts

## Refactoring signals
- When you copy-paste: extract
- When a file exceeds ~200 lines: consider splitting
- When you add a parameter to avoid changing logic: reconsider the design
- Ask the user before large refactors — propose, don't impose

## Working with the LLM
- When the request is vague, ask a clarifying question before coding
- Propose 2-3 approaches for non-trivial decisions
- Explain trade-offs, let the user decide
- After completing work, suggest what to verify
```

---

### 3. PILOT.md.jinja

**Role:** Project dashboard. Where the project stands, what's next.
**Target:** ~40 lines, English.

**Structure:**

```
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

**Notes:**
- `first_session: true` is the flag CLAUDE.md checks for intro behavior
- After first session, the LLM sets it to `false` and rewrites objectives
- Status table reflects that uv sync + pre-commit install ran automatically (copier _tasks)

---

### 4. SESSION-CONTEXT.md.jinja

**Role:** Living context. Rewritten (not appended) each session. The WHY behind current state.
**Target:** ~30 lines template, grows organically.

**Structure:**

```
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

---

### 5. pyproject.toml.jinja

**Changes from current:**

1. **Build backend:** hatchling → uv_build

```toml
[build-system]
requires = ["uv_build"]
build-backend = "uv_build"
```

2. **Add ruff config:**

```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]
# E=pycodestyle, F=pyflakes, W=warnings, I=isort, N=naming,
# UP=pyupgrade, B=bugbear, SIM=simplify

[tool.ruff.format]
quote-style = "double"
```

3. **Add pytest config:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

4. **Rest unchanged** — profile-specific deps stay as-is, just translated comments if any.

---

### 6. src/{{ project_slug }}/__init__.py

**New file.** Minimal:

```python
"""{{ project_name }}."""
```

This creates the proper `src/` layout so `uv run pytest` works with the pythonpath config.

---

### 7. .pre-commit-config.yaml (template)

**Current:** ruff check + ruff format only.

**Add:**

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

**Note:** no-commit-to-branch protects main — forces feature branches.

---

### 8. copier.yml

**Changes:**

1. **All questions translated to English:**

```yaml
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

2. **_tasks: auto-setup with uv check + prompt:**

```yaml
_tasks:
  - "git init"
  - >
    command -v uv >/dev/null 2>&1 && {
      uv sync && uv run pre-commit install &&
      echo '✅ Dependencies installed, pre-commit activated.';
    } || {
      echo '⚠️  uv not found.';
      echo 'Install it: curl -LsSf https://astral.sh/uv/install.sh | sh';
      echo 'Then run: uv sync && uv run pre-commit install';
    }
```

**Note on y/n prompt:** copier _tasks run non-interactively by default.
Shell `read -p` may not work reliably across platforms (especially Windows).
Fallback approach: check + auto-install if available, clear message if not.
If interactive prompt is needed, we use a post-copy script instead of inline _tasks.
**Decision: test at implementation time.** If `read` works in copier _tasks on
the target platforms, add the y/n. If not, use the check+message approach above.

3. **_message_after_copy translated:**

```yaml
_message_after_copy: |
  ✅ Project {{ project_name }} created with The Meta Protocol.

  Next steps:
    1. cd {{ project_slug }}
    2. Open .meta/PILOT.md and define your first session goal
    3. Launch Claude Code: claude

  Stack: Python {{ python_version }} | uv | ruff | profile: {{ project_type }}
```

---

### 9. Skills

All skills live in `template/.claude/skills/<name>/SKILL.md`.

#### /brainstorm

```markdown
---
name: brainstorm
description: Structured exploration before coding — one question at a time
---

You are in BRAINSTORM mode. Your job is to explore the idea, not implement it.

## Hard rules
- Ask ONE question at a time
- For each decision, propose 2-3 alternatives with trade-offs
- Apply YAGNI aggressively — cut scope creep
- DO NOT write any code, create any file, or make any edit
- When done, write the summary to .meta/scratch/brainstorm.md

## Process
1. Understand the goal — ask what, why, for whom
2. Explore constraints — what's non-negotiable, what's flexible
3. For each design decision, present options with your recommendation
4. Validate the full picture with the user
5. Write brainstorm.md with: decisions taken, alternatives rejected (with reasons), open questions

## Output format (.meta/scratch/brainstorm.md)

# Brainstorm — [topic]
**Date:** [date]

## Decisions
- Decision 1: [choice] — because [reason]. Rejected: [alternative] ([why])
- ...

## Open questions
- ...

## Next step
Run /plan to break this into tasks.
```

#### /plan

```markdown
---
name: plan
description: Break work into concrete tasks with verification steps
---

You are in PLANNING mode. Your job is to decompose work into actionable tasks.

## Hard rules
- If .meta/scratch/brainstorm.md exists, read it first
- Map ALL files that will be created or modified BEFORE defining tasks
- Each task must have: file(s), what to do, how to verify
- Chunks should be 2-5 minutes of work
- Write the plan to .meta/scratch/plan.md
- DO NOT start implementing

## Process
1. Read brainstorm.md if it exists
2. Read the current codebase structure (ls, relevant files)
3. List all files that will be touched
4. Break into ordered tasks with dependencies
5. Write plan.md
6. Ask user to validate before proceeding

## Output format (.meta/scratch/plan.md)

# Plan — [topic]
**Date:** [date]
**Based on:** brainstorm.md (if applicable)

## Files involved
- path/to/file.py — create / modify (reason)
- ...

## Tasks
### 1. [Task title]
- **Files:** path/to/file.py
- **Do:** [concrete description]
- **Verify:** [how to check it works]

### 2. [Task title]
...

## Execution
When ready, the LLM creates a Task per item and executes in order.
```

#### /ship

```markdown
---
name: ship
description: Pre-commit checklist and context update — does NOT commit
---

You are in SHIP mode. Verify everything is clean and update project context.

## Hard rules
- DO NOT create a commit — that's the user's or LLM's separate action
- Run ALL checks before updating .meta/ files
- If any check fails, stop and report — do not update .meta/

## Checklist
1. Run `uv run pytest` — all tests must pass
2. Run `uv run ruff check .` — no lint errors
3. Run `uv run ruff format --check .` — no format issues
4. Check for untracked files that should be staged (`git status`)
5. Check for files in wrong locations (drafts at root, code in scratch/)

## If all checks pass
1. Update PILOT.md:
   - Update status table
   - Update current objectives
   - Mark completed items
   - Add any new next steps

2. Rewrite SESSION-CONTEXT.md:
   - Architecture snapshot (current modules and how they connect)
   - Active decisions (why current choices were made)
   - Traps to avoid (what broke or could break)
   - Open questions (what still needs answers)

3. Report: "Ready to commit. Run `git add` and `git commit` or ask me to commit."
```

#### /lint

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

#### /test (already exists, unchanged)

---

### 10. .claude/settings.json.jinja

**Changes from current:**

- Add permissions for .meta/ editing (PILOT.md, SESSION-CONTEXT.md, ARCHITECTURE.md)
- Add skill paths

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

**Removed:** SessionStart compact hook (the CLAUDE.md automatism handles reading PILOT.md natively — no need for a hook to cat it).

---

### 11. .gitignore.jinja

**No spec changes needed.** Verify at implementation that it covers:
- `.meta/scratch/*` (with `!.meta/scratch/.gitkeep`)
- `__pycache__/`, `.venv/`, `*.pyc`
- `.env`

---

## Generation test plan

After implementation, test with:

```bash
# Test each profile
for profile in minimal app data quant; do
  copier copy . /tmp/test-$profile --data project_type=$profile --defaults
  cd /tmp/test-$profile
  # Verify: all files present, English content, uv sync works, pytest runs, ruff clean
  cd -
done
```

**Checks per profile:**
- [ ] All template files generated correctly
- [ ] CLAUDE.md is English, contains automatisms + rules
- [ ] GUIDELINES.md is English, advisory tone
- [ ] PILOT.md has first_session: true
- [ ] SESSION-CONTEXT.md has architecture snapshot section
- [ ] pyproject.toml has ruff + pytest config, uv_build backend
- [ ] src/package/__init__.py exists
- [ ] pre-commit hooks include trailing-whitespace, check-yaml, etc.
- [ ] Skills are in .claude/skills/ (brainstorm, plan, ship, lint, test)
- [ ] `uv sync` succeeds
- [ ] `uv run pytest` succeeds (0 tests, no errors)
- [ ] `uv run ruff check .` clean
- [ ] Profile-specific deps installed correctly

---

## Out of scope (post-MVP)

- Skills T2: /spec, /tdd, /review, /debug, /consolidate
- Knowledge hierarchy: INDEX.md, /digest, /dream, /tidy
- GitHub Actions CI
- project_language / dev_language copier params
- Multi-LLM support (.cursorrules)
- Profile-specific skills (/api-test, /backtest, /pipeline-run)
- Non-Python templates
