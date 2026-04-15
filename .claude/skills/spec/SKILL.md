---
name: spec
description: "Formalize requirements into a structured spec. Usage: /spec <topic>"
---

# /spec — Specification writer

> If you have the Superpowers plugin installed, prefer `superpowers:brainstorming`
> for a more thorough spec process. This skill is a lightweight fallback.

You are in SPEC mode. Your job is to formalize WHAT we're building, not HOW.

## Hard rules

- Read `.meta/scratch/brainstorm.md` first if it exists — build on prior exploration
- Ask clarifying questions ONE AT A TIME if requirements are ambiguous
- Use MoSCoW priority (MUST / SHOULD / COULD) for every requirement
- DO NOT write any code, create any file, or make any edit except the spec
- Apply YAGNI — cut anything that isn't essential to the stated objective
- When done, write the spec to `.meta/scratch/spec-{topic}.md`

## Process

1. Read brainstorm.md if available — extract decisions already taken
2. State the objective in 2-3 sentences — confirm with the user
3. List requirements with MoSCoW priority — propose, user validates
4. Define non-goals explicitly — what we are NOT building
5. Propose a high-level approach (not implementation details)
6. List open questions
7. Write the spec file

## Output format

Write to `.meta/scratch/spec-{topic}.md`:

```markdown
# Spec — {topic}

**Date:** {date}
**Status:** DRAFT

## Objective
{What we're building and why — 2-3 sentences max.}

## Requirements
- [MUST] {requirement}
- [MUST] {requirement}
- [SHOULD] {requirement}
- [COULD] {requirement}

## Non-goals
- {explicitly out of scope}
- {explicitly out of scope}

## Proposed approach
{high-level how — architecture direction, not implementation details}

## Open questions
- {unresolved}

## Next step
Run /plan to decompose into tasks, or /debate if approach is controversial.
```

## Verification

Before finishing, confirm:
- [ ] Every requirement has a MoSCoW priority
- [ ] Non-goals are explicit (at least 2)
- [ ] No implementation details leaked into the spec
- [ ] User has validated the objective and requirements
- [ ] Spec file is written to `.meta/scratch/`

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "The brainstorm already covers this" | Brainstorm explores. Spec commits. They're different artifacts. |
| "Requirements are obvious" | If they're obvious, writing them takes 2 minutes. If they're not, you just saved hours. |
| "Let me just start coding" | Code without spec = rework. Every time. |
| "Non-goals aren't necessary" | Unbounded scope is the #1 project killer. Name what you're NOT doing. |
