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
