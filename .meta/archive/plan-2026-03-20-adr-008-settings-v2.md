# Implementation Plan — ADR-008 Settings v2 Improvements

**Date:** 2026-04-05
**Based on:** ADR-008 validated decisions
**Scope:** 8 tasks, estimated 1 session

---

## Context

The template currently has a basic settings.json with:
- Allow: uv, git (individual commands), Read, Edit(src/tests/.meta)
- Deny: rm -rf, sudo, .env, .git
- Hook: PostToolUse auto-ruff

ADR-008 adds: attribution config, security denys, first-session hook,
.claude/rules/, and plan enforcement in CLAUDE.md.

---

## Tasks

### Task 1 — Update settings.json.jinja

**File:** `template/.claude/settings.json.jinja`

**Changes:**
1. Add `"attribution": {"commit": ""}` — suppress Co-authored-by trailer
2. Add security deny rules:
   - `Read(~/.ssh/**)`
   - `Read(~/.aws/**)`
   - `Read(~/.pypirc)`
   - `Bash(dd *)`
3. Add ask rule: `Bash(git push --force *)`
4. Add SessionStart hook that checks `first_session: true` in PILOT.md and
   injects welcome context if present
5. Simplify git allows: use `Bash(git *)` instead of individual commands
   (git status, git diff, git log, git add, git commit listed separately
   is verbose — `Bash(git *)` covers all git commands. The deny/ask rules
   handle the dangerous ones)

**Verification:** JSON valid, copier generates correctly.

### Task 2 — Create .claude/rules/testing.md

**File:** `template/.claude/rules/testing.md`

**Content:** pytest conventions for this project:
- Test file naming: `test_<module>.py` mirroring `src/` structure
- Use fixtures from conftest.py
- Prefer `tmp_path` for file operations
- One test function per behavior, descriptive names
- Run tests before committing: `uv run pytest`

**Not profile-specific** — applies to all profiles.

### Task 3 — Create .claude/rules/code-style.md

**File:** `template/.claude/rules/code-style.md`

**Content:** Formatting and style rules that complement ruff:
- snake_case functions/variables, PascalCase classes, SCREAMING_SNAKE constants
- English for all code, comments, docstrings, commit messages
- Imports: stdlib → third-party → local (ruff handles this automatically)
- Docstrings: describe WHAT, not HOW (reinforces CLAUDE.md rule 7)
- Comments: explain WHY, not WHAT (surgical, not narrating)

### Task 4 — Strengthen automatism #4 in CLAUDE.md

**File:** `template/CLAUDE.md.jinja`

**Current:** `4. **Before coding** — propose a plan before implementing. If scope is unclear, suggest /brainstorm first`

**New:** `4. **Before any Edit or Write** — you must have proposed a plan and received user approval. If no plan exists, propose one. If scope is unclear, suggest /brainstorm first. Never implement without explicit user go-ahead`

Stronger language: "must have" + "never implement without" vs "propose".

### Task 5 — Document deferred options in GUIDELINES.md

**File:** `template/.meta/GUIDELINES.md.jinja`

**Add a section** "Advanced Claude Code configuration" documenting:
- `enabledPlugins` to force Superpowers for all contributors
- `autoDreamEnabled` for background memory consolidation
- `autoMemoryDirectory` to redirect memory to .meta/
- Status line configuration example
- Plan mode recommendation (`Shift+Tab` or `--permission-mode plan`)
- Subagent persistent memory (`memory: user` in agent frontmatter)

Each with a brief explanation and the JSON to add to settings.json.

### Task 6 — Add check-toml to pre-commit

**File:** `template/.pre-commit-config.yaml`

**Change:** Add `check-toml` hook (currently has check-yaml but not check-toml).
pyproject.toml is a critical file — invalid TOML breaks the project.

### Task 7 — Test full generation (all 4 profiles)

```bash
copier copy . /tmp/test-minimal --defaults --trust -d project_name="test-minimal"
copier copy . /tmp/test-app --defaults --trust -d project_name="test-app" -d project_type="app"
copier copy . /tmp/test-data --defaults --trust -d project_name="test-data" -d project_type="data"
copier copy . /tmp/test-quant --defaults --trust -d project_name="test-quant" -d project_type="quant"
```

For each: verify settings.json is valid JSON, rules/ files exist,
CLAUDE.md has updated automatism #4.

### Task 8 — Commit and push

Conventional commit:
```
feat: implement ADR-008 settings v2 improvements

- attribution: suppress co-author trailer natively
- security: deny credential reads + dd, ask force-push
- first-session hook: inject welcome context on first_session flag
- .claude/rules/: testing.md + code-style.md starter files
- automatism #4 strengthened (plan required before any edit)
- GUIDELINES.md: documented deferred advanced options
- pre-commit: added check-toml
```

---

## Out of scope (this plan)

- plansDirectory configuration (pending .meta/ reorganization brainstorm)
- Language parameters in copier.yml
- Public vs private gitignore strategy
- AGENTS.md generation
- Profile-specific skills
