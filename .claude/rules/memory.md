> **Enforcement:** advisory — relies on LLM discipline. No hook. Same pattern as `code-style.md` for LLM-behavior rules.

# Living docs maintenance

## Core principle

**False context causes more damage than missing context.**
Priority at every session end: remove stale or contradictory content before adding anything.

A fresh LLM reading a wrong SESSION-CONTEXT will confidently head in the wrong direction.
A fresh LLM reading an empty SESSION-CONTEXT will ask — which is recoverable.

## Definitions

**Session** = a milestone delivered (one commit or a logical group of commits).
Not a Claude Code conversation. Not a calendar day.

## SESSION-CONTEXT.md rules

**Never append — always rewrite.**
SESSION-CONTEXT.md is not a journal. Each session, rewrite it from scratch.
Delete obsolete reasoning. Do not comment it out.

**Target: ≤ 50 lines nominal.**
Above 50 lines is a signal to triage. Not a hard block — a prompt to ask:
"Is every line here still load-bearing?"

**Required sections with line budgets:**

| Section | Budget | Format |
|---|---|---|
| Architecture snapshot | ≤ 8 lines | Free prose, current modules + interfaces |
| Active decisions | ≤ 15 lines | `"We do X because Y. Rejected: Z."` |
| Traps to avoid | ≤ 10 lines | `"Don't do X — it causes Y (observed DATE)"` |
| Open questions | ≤ 8 lines | One question per line |
| Pending plans | ≤ 9 lines | `"- plan-<slug>.md — <one-line status>"` |

**Dense session escape valve.**
If a session generates more context than fits in 50 lines (e.g. debugging spike,
architecture exploration), create `.meta/active/session-YYYY-MM-DD-<slug>.md`
and reference it from SESSION-CONTEXT. SESSION-CONTEXT stays ≤ 50 lines.
Example reference: `See session-2026-04-21-auth-spike.md in active/ — 3 options open.`

**Mandatory full rewrite every 5 commits.**
Run `git log --oneline -5` at session start. If the oldest of the 5 commits predates
the last SESSION-CONTEXT rewrite date (visible in the file header), do a full rewrite
regardless of apparent freshness. Staleness accumulates silently.

## PILOT.md rules

**Update immediately on status change** — do not batch updates to end of session.
When a task moves from TODO to DONE, update PILOT.md now.

**Target: ≤ 120 lines.** Beyond this, compliance with the rules at the bottom of the
file drops measurably (source: ADR-003, Boris Cherny sizing).

**Clean before adding.** Before inserting a new row or section, scan for stale rows
to remove. The file must not grow unboundedly.

## Context window

**Compact at milestone boundaries.**
Run `/compact` before starting a new milestone (new feature, new spec, new plan).
Not on a timer. Not when "it feels slow". At the natural transition point.

## End-of-session checklist

1. Rewrite SESSION-CONTEXT.md (never append)
2. Update PILOT.md for any status changes
3. Check line counts — triage if over budget
4. Check 5-commit reset rule — full rewrite if due
5. Commit both files together

## Rejected alternatives

- **Hard block at 50 lines (hook):** rejected. A hook on line count enforces form, not
  quality. A 48-line file full of stale decisions is worse than a 55-line file of fresh
  ones. Advisory is sufficient when the rule is clear.
- **Adaptive bound 50/80:** rejected. The upper bound becomes the default. "Dense session"
  becomes a permanent excuse. Segmentation to `.meta/active/` is the correct escape valve.
- **Temporal compaction trigger:** rejected. Arbitrary — compacts when unnecessary, misses
  natural transition points. Milestone-based trigger is semantically correct.
