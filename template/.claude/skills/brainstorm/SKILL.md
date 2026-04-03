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
