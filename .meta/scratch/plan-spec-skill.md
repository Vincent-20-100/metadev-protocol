# Plan — /spec fallback skill

**Date:** 2026-04-07
**Status:** PLAN — ready to implement
**Effort:** Small

---

## Rationale

Gap in our flow: `/brainstorm` explores, `/plan` decomposes, but nothing
formalizes the WHAT (spec) between the two. Superpowers has this via
`superpowers:brainstorming` but we need a lightweight fallback like we
have for brainstorm and plan.

## Flow position

`/brainstorm` → `/spec` → `/debate` (if controversial) → `/plan` → implement

## Skill design

- Reads `.meta/scratch/brainstorm.md` if it exists (output of /brainstorm)
- Produces a structured spec in `.meta/scratch/spec-{topic}.md`
- Lightweight: no multi-agent, no phases — just structured output
- Points to `superpowers:brainstorming` for the full version

## Spec output format

```markdown
# Spec — {topic}

**Date:** {date}
**Status:** DRAFT

## Objective
What we're building and why (2-3 sentences max).

## Requirements
- [MUST] {requirement}
- [SHOULD] {requirement}
- [COULD] {requirement}

## Non-goals
- {explicitly out of scope}

## Proposed approach
{high-level how, not implementation details}

## Open questions
- {unresolved}

## Next step
Run /plan to decompose into tasks, or /debate if approach is controversial.
```

## Files to create
- `template/.claude/skills/spec/SKILL.md`
- `skills-pack/skills/spec/SKILL.md` (copy)

## Files to edit
- `template/CLAUDE.md.jinja` — add /spec to skills list
- `template/.meta/GUIDE.md.jinja` — add /spec description + update flow chain
