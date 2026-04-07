---
name: plan
description: Break work into concrete tasks with verification steps
---

> If you have the Superpowers plugin installed, prefer `superpowers:writing-plans`
> for more detailed implementation plans. This skill is a lightweight fallback.

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

## Verification

Before finishing, confirm:
- [ ] All files involved are listed (no surprise edits during implementation)
- [ ] Each task has a concrete "Verify" step (not just "check it works")
- [ ] Tasks are ordered by dependency (no task references a later task's output)
- [ ] Plan is written to `.meta/scratch/`
- [ ] User has validated the plan

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "I can figure it out as I go" | Plans catch dependency issues BEFORE you hit them mid-implementation. |
| "The tasks are too small to plan" | Small tasks still have ordering. Wrong order = rework. |
| "Let me just map the files mentally" | Write them down. Your context window is finite. The user needs to see them too. |
| "Verification steps are obvious" | If they're obvious, writing them takes 10 seconds. If they're not, you just prevented a silent failure. |

## Execution

When the user approves the plan, create a Task per item and execute in order.
Mark each task as completed as you go.
