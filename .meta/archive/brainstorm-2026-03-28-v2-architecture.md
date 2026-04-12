# V2 Architecture — Tool separation

**Date:** 2026-04-06
**Status:** BRAINSTORM — validated direction, needs detailed spec

---

## The 3 layers (clear separation)

```
Layer 3 — MASTER ORCHESTRATOR (night shift manager)
  │  Picks tools, manages queue, tracks dependencies
  │  NEVER codes. Accumulates plans + decisions for user review.
  │  Runs on test branch always.
  │
  ├── Layer 2 — SKILLS (equal peers, interchangeable)
  │     /debate        — adversarial 3-agent debate → debate record
  │     /brainstorm    — structured exploration → brainstorm.md
  │     /plan          — task decomposition → plan.md
  │     superpowers:*  — TDD, code review, debugging, etc.
  │     (future skills plug in at this layer)
  │
  └── Layer 1 — PRIMITIVES (Claude Code native)
        Agent tool, Edit, Write, Bash, Read, etc.
```

## Master orchestrator — "nightshift"

### What it does
- Reads a queue of subjects/tasks from `.meta/scratch/queue.md`
- For each subject, picks the right skill(s) in the right order
- Manages CHRONOLOGICAL ORDER with explicit dependency tracking
- Runs debates, brainstorms, plans — accumulates artifacts
- Does NOT implement (no code, no edits outside .meta/)
- Flags decisions: AUTO (reversible, low impact) vs HITL (structuring)
- When done, produces a MORNING BRIEF for the user

### What it produces (overnight)
```
.meta/
├── nightshift/
│   ├── morning-brief.md        # Summary of everything done overnight
│   ├── decisions-needed.md     # Queue of USER DECISION NEEDED items
│   ├── plans/                  # Implementation plans (ordered, with deps)
│   │   ├── 01-plan-xxx.md     # Explicit chronological numbering
│   │   ├── 02-plan-yyy.md     # Each plan notes its dependencies
│   │   └── 03-plan-zzz.md
│   └── debates/                # Debate records from overnight
│       ├── debate-xxx.md
│       └── debate-yyy.md
```

### What it does NOT do
- No code writing
- No file edits outside .meta/
- No commits
- No decisions on irreversible/structuring topics
- No implementation of any kind

### Morning brief format
```markdown
# Morning Brief — {date}

## Overnight progress
- {n} debates completed, {n} plans drafted
- {n} decisions made autonomously (reversible, low-impact)
- {n} decisions awaiting your input

## Decisions needed (ordered by priority)
1. [STRUCTURING] {topic} — see debate-xxx.md → impacts plans 02, 03
2. [STRATEGIC] {topic} — see debate-yyy.md → blocks plan 01
3. ...

## Plans ready for validation (in implementation order)
1. plan-01-xxx.md — depends on: nothing — ready to implement
2. plan-02-yyy.md — depends on: decision #1 above
3. plan-03-zzz.md — depends on: plan-01, plan-02

## Auto-decisions taken (for your review)
- {decision}: {choice} — reason: {why it was safe to auto-decide}
- ...
```

### Dependency management
- Each plan has a `depends_on:` field listing prerequisites
- When a debate changes a prior assumption, the orchestrator:
  1. Identifies all downstream plans affected
  2. Either adapts them or flags for re-planning
  3. Notes the cascade in the morning brief
- Implementation order = topological sort of dependency graph

### Dream mode integration
- Dream mode (auto-memory consolidation) runs AFTER nightshift
- Nightshift produces artifacts → Dream mode synthesizes learnings
- Dream mode updates SESSION-CONTEXT.md and memory files
- Result: user wakes up to both DECISIONS + CONTEXT fully updated

## Decision criteria: AUTO vs HITL

| Criteria | AUTO (orchestrator decides) | HITL (user decides) |
|----------|---------------------------|---------------------|
| Reversibility | Easy to undo | Hard/impossible to undo |
| Impact scope | Single component | Cross-cutting, architectural |
| Precedent | Similar decision already made | First time, sets precedent |
| Confidence | Debate reached consensus | Debate has irreducible tensions |
| Risk | Low — wrong choice costs hours | High — wrong choice costs days/weeks |

## Fork strategy (V2+, not V1)

When a decision is too hard to call:
- Orchestrator continues BOTH options as parallel plan branches
- Downstream plans are duplicated with suffix `-fork-A` / `-fork-B`
- Morning brief highlights the fork point and divergence
- User chooses after seeing downstream implications
- Unchosen fork is archived, not deleted (may be useful later)
