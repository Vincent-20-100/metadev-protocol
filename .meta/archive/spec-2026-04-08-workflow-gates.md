# Spec — Workflow Gates (mandatory approval before implementation)

**Date:** 2026-04-08
**Source:** Debate record `.meta/debates/debate-workflow-gates.md`
**Status:** VALIDATED (2026-04-08) — ready for implementation plan

---

## Problem

Claude jumps to implementation without explicit user approval. The current
Automatism #4 ("propose a plan and receive user approval") is too vague:
- No tiers — a typo and an architecture change get the same treatment
- No decision tree — Claude doesn't know when to suggest brainstorm vs spec vs plan vs debate
- No tracking of pending plans — risk of conflicts between sessions
- Debate is never positioned as optional (expensive in tokens)
- No rule against coding during a conversation without explicit "go"

## Goal

Replace Automatism #4 with a structured, tiered workflow that:
1. Guarantees explicit user approval before ANY implementation
2. Scales ceremony proportionally to scope/risk
3. Defines when each skill applies (brainstorm, spec, plan, debate)
4. Tracks pending plans to prevent conflicts
5. Handles plans-of-plans (/orchestrate) for autonomous multi-step work

---

## Requirements

### Must have (M)

**M1 — Explicit approval gate**
Claude NEVER implements (Edit/Write on code/config) without explicit user
approval. "Explicit" means Claude asks a direct question and waits for
an affirmative answer. Silence, "sounds good", or reading the plan is
NOT approval. Claude must ask "OK to proceed?" or equivalent and WAIT.

**M2 — Three tiers based on file scope**

| Tier | Signal | Process |
|------|--------|---------|
| Trivial | 1 file, localized change | State what you'll do → ask "OK?" → wait → execute |
| Standard | >1 file OR structural change in 1 file | Write brief plan → ask for approval → wait → execute |
| Complex | New pattern / architecture / large scope | Spec required → plan → ask for approval → /orchestrate if multi-step |

"Structural change in 1 file" = new module, API change, refactoring of
public interface, anything that changes the contract of the code.

**M3 — Pre-spec clarification**
If the idea behind a spec isn't clearly defined, Claude MUST suggest
/brainstorm (or /debate if trade-offs exist) before writing the spec.
Claude does not write a spec on a vague idea.

**M4 — Decision tree in CLAUDE.md**
Replace Automatism #4 with an explicit decision tree:

```
User request arrives
  │
  ├─ Idea is vague/undefined?
  │   └─ Suggest /brainstorm → clarify → re-enter tree
  │
  ├─ Hard decision with trade-offs?
  │   └─ Suggest /debate (or /brainstorm if user prefers — debate
  │      is always a suggestion, never an obligation)
  │
  ├─ Claude agrees with 3+ positions in a row without friction?
  │   └─ Invoke devil's-advocate agent (Rule of 3 — anti-consensus bias)
  │
  ├─ Structural decision and user wants a challenge?
  │   └─ Invoke devil's-advocate agent on demand
  │
  ├─ Requirements need formalization? (complex scope)
  │   └─ Write /spec → then continue to plan
  │
  ├─ 1 file, localized change (trivial)
  │   └─ "I'll do X in file Y. Go?" → wait for OK → execute
  │
  ├─ >1 file OR structural (standard)
  │   └─ Write plan → ask approval → execute
  │
  └─ Large scope / new pattern (complex)
      └─ Write spec → write plan → ask approval → execute
          (use /orchestrate if multi-step)
```

**M5 — Debate is always optional**
Claude may suggest /debate for hard trade-offs, but /brainstorm is
always a valid alternative. Debate costs significantly more tokens.
Claude must accept /brainstorm without resistance if the user prefers.

**M8 — Devil's advocate (Rodin agent)**
The devil's-advocate agent persona (inspired by Benjamin Code's Rodin)
is integrated into the workflow as a consensus-bias breaker:
- **Rule of 3**: if Claude validates 3 user positions in a row without
  genuine friction, actively seek what's missing, wrong, or oversimplified
- **On-demand**: user can invoke the devil's-advocate on any decision
- **In /debate**: can complement the lone wolf in Phase 2 or challenge
  the orchestrator's synthesis in Phase 3
- **Anti-complaisance**: never validate a position just because the user
  or another agent defends it. Steelman before critiquing.
- **Classification**: tag claims as ✓ Correct, ~ Contestable,
  ⚡ Oversimplified, ◐ Blind spot, ✗ Wrong

**M6 — Emergent decisions during execution**
If during implementation Claude discovers something that deviates from
the approved plan (unexpected dependency, conflict, design question that
wasn't covered), Claude STOPS and asks the user. If execution follows
the plan without surprises, no checkpoint needed.

**M7 — Pending plans tracking**
SESSION-CONTEXT.md must include a "Pending plans" section listing plans
that were written but not yet implemented. At session start (Automatism #1),
Claude checks for pending plans and flags conflicts with new requests.

### Should have (S)

**S1 — /orchestrate for compound work**
When a validated plan has multiple dependent steps, suggest /orchestrate.
The user approves the global plan once, then /orchestrate executes
sub-steps autonomously — checkpointing only on deviation.

**S2 — Plan location convention**
All plans go to `.meta/scratch/plan-<topic>.md`.
All specs go to `.meta/scratch/spec-<topic>.md`.
(Already documented in "Superpowers output paths" section.)

### Won't have (W)

**W1 — Mechanical line-count rules**
No "< 5 lines = trivial" rule. Line count says nothing about complexity.
File count + structural impact is the signal.

**W2 — Mandatory debate**
Debate is never mandatory. Always a suggestion.

**W3 — Harness-level hook enforcement**
No settings.json hook to block Edit/Write. The rule is in CLAUDE.md
(law level). Hooks are fragile and hard to maintain.

---

## Files to modify

| File | Change |
|------|--------|
| `template/CLAUDE.md.jinja` | Replace Automatism #4 with decision tree. Add pending plans to Automatism #1. Mention debate-is-optional in Skills section. Add devil's-advocate to agent personas list. |
| `template/.meta/GUIDELINES.md.jinja` | Update "Working with the user" section to reference the tiers. Remove any conflicting guidance. Add Rule of 3 guidance. |
| `template/.meta/SESSION-CONTEXT.md.jinja` | Add "Pending plans" section template. |
| `template/AGENTS.md.jinja` | Add devil's-advocate persona (anti-complaisance, steelmanning, classification, Rule of 3). |

## What does NOT change

- Other automatisms (1-3, 5-10) stay as-is
- Rules section stays as-is
- Skills list stays as-is (just add a note about debate being optional)
- Architecture section stays as-is

---

## Acceptance criteria

1. Generated project's CLAUDE.md contains the decision tree
2. Generated project's SESSION-CONTEXT.md has a "Pending plans" section
3. `copier copy --defaults` still works
4. A reader of CLAUDE.md can determine the correct tier for any request
   without ambiguity
5. The word "debate" appears with "optional" or "suggestion" nearby
6. AGENTS.md contains devil's-advocate persona with Rule of 3
7. Decision tree includes devil's-advocate trigger (3 validations without friction)
