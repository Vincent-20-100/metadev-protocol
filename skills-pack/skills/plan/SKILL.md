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

## Execution

When the user approves the plan, create a Task per item and execute in order.
Mark each task as completed as you go.
