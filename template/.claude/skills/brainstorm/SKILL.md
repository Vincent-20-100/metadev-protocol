---
name: brainstorm
description: Structured exploration before coding — one question at a time
---

> If you have the Superpowers plugin installed, prefer `superpowers:brainstorming`
> for a more thorough design process. This skill is a lightweight fallback.

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

## Verification

Before finishing, confirm:
- [ ] At least 2 alternatives were considered for each major decision
- [ ] YAGNI was applied — no speculative features survived
- [ ] Open questions are listed (not swept under the rug)
- [ ] Brainstorm file is written to `.meta/scratch/`

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "I already know the best approach" | If you haven't considered alternatives, you don't know it's the best. You know it's the first. |
| "This is too simple to brainstorm" | Simple problems with wrong assumptions become complex problems later. |
| "The user seems to know what they want" | Explore anyway. Users often discover what they actually want during brainstorm. |
| "Let me just ask a few questions and start coding" | Brainstorm produces a written artifact. Questions in chat disappear from context. |

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
