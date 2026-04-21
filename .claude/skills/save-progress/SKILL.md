---
name: save-progress
description: Pre-commit checklist + context update — runs deterministic checks, updates PILOT.md and SESSION-CONTEXT.md. Does NOT commit.
allowed-tools: Bash(uv *), Bash(git status *), Bash(python *), Read, Edit(.meta/**)
---

You are in SAVE-PROGRESS mode. Run the deterministic preflight, then update project context.

## Hard rules

- DO NOT create a commit — that is a separate action.
- If preflight fails, STOP and report — do not update `.meta/` files.

## Step 1 — preflight (deterministic, one command)

```bash
uv run python scripts/save_progress_preflight.py
```

The script runs: `pytest`, `ruff check`, `ruff format --check`, `git status`,
and a check for stray drafts at the project root or code in `.meta/scratch/`.
It prints a JSON summary and exits non-zero on any failure.

## Step 2 — narrative update (LLM, only if step 1 is green)

1. **Update `.meta/PILOT.md`** — status table reflects actual state, not
   aspirational. Mark completed items. Add new next steps.
2. **Rewrite `.meta/SESSION-CONTEXT.md`** — architecture snapshot, active
   decisions (why), traps to avoid (what broke or could break), open
   questions. Rewrite, don't append.
3. **Report:** "Ready to commit. Run `git add` and `git commit`."

## Verification

- [ ] Preflight JSON shows `"ok": true` for all 5 checks
- [ ] PILOT.md reflects actual state
- [ ] SESSION-CONTEXT.md captures traps and open questions, not just wins

## Quick-pause mode (--skip-tests)

For mid-session checkpoints where tests are genuinely WIP, you may skip the
pytest run:

```bash
uv run python scripts/save_progress_preflight.py --skip-tests
```

**When to use:** only when tests are intentionally red (e.g., mid-refactor,
scaffold not yet wired). Not for "tests are slow" or "I can't fix this now."

**Required:** when using `--skip-tests`, add a `Skip-Tests: true` trailer to
the commit message so the bypass is machine-readable in git history:

```
fix: partial scaffold for new module

Skip-Tests: true
```

Also note in SESSION-CONTEXT.md under "Traps to avoid" that tests are red
and why, so the next session does not ship without fixing them.

## Rationalizations you must not accept

| Excuse | Why it's wrong |
|--------|---------------|
| "Tests are passing, that's enough." | Lint and format issues compound — preflight catches them. |
| "I'll update PILOT.md later." | You won't. Next session reads PILOT.md first; stale = wrong. |
| "SESSION-CONTEXT.md is fine from last time." | Context decays every session. Rewrite, don't append. |
| "Small change, skip the preflight." | Small changes break things. The script takes 30 seconds. |
| "Tests are slow, I'll use --skip-tests." | --skip-tests is for intentionally red tests, not slow ones. |
