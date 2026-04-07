---
name: save-progress
description: Pre-commit checklist and context update — does NOT commit
allowed-tools: Bash(uv *), Bash(git status *), Read, Edit(.meta/**)
---

You are in SAVE-PROGRESS mode. Verify everything is clean and update project context.

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

## Verification

Before reporting ready:
- [ ] All 5 checklist items passed (no skipped checks)
- [ ] PILOT.md status table reflects actual state (not aspirational)
- [ ] SESSION-CONTEXT.md captures traps and open questions (not just successes)
- [ ] No stray files at project root

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "Tests are passing, good enough" | Lint and format issues compound. Check everything. |
| "I'll update PILOT.md later" | You won't. Next session starts by reading PILOT.md — stale state = wrong decisions. |
| "SESSION-CONTEXT.md is fine from last time" | Context decays every session. Rewrite, don't append. |
| "There's only one small change, no need for the full checklist" | Small changes break things. The checklist takes 30 seconds. |
