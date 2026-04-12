---
type: brainstorm
date: 2026-04-13
slug: vision-skill
status: archived
---

# Brainstorm — `/vision` skill (PM.1c)

**Parent:** `archive/brainstorm-2026-04-12-claude-ai-project-starter.md` §4.2 C1
**Outcome:** plan-2026-04-13-vision-skill.md — full-auto ready
**Status:** decisions locked, plan produced, archived.

---

## 1. Problem

Today, `PILOT.md` starts with a "Current state" section but has **no scaffolding for the upstream layer** — the *why* of the project. Users jump straight into `/brainstorm` without having written down the problem, the target user, the V1 scope, or a north star metric.

Guillaume Desforges's `03-business-vision.md` has a mini product-brief template covering problem / user / principles ranking / V1 scope / north star / competitive / success metrics. **That's the gap for solo builders** — it forces the product framing before code exists.

---

## 2. Decisions

| # | Decision | Chosen | Rejected alternatives |
|---|---|---|---|
| D1 | **Form** | Hybrid: a `/vision` skill that fills a dedicated section in `PILOT.md` — no parallel file | New standalone file (adds maintenance surface); PILOT section only (no re-invocable skill); template-only copier prompt (freezes at creation, not iterable) |
| D2 | **PILOT section location** | New `## Vision` section, placed **before** "Current state" in the PILOT template | After Current state (vision should anchor the dashboard, not footnote it) |
| D3 | **Sections in the vision block** | 4 sections: Problem / Target user / V1 scope / North star metric | Guillaume has 7 — product principles ranking (too meta for v1), competitive landscape (belongs to `/research`), success metrics detail (overlap with north star) |
| D4 | **Invocation cadence** | Auto-**proposed** at first-session detection (via existing automatism #2) + manually anytime | Auto-executed (too intrusive); manual-only (the gap stays unfilled for users who don't know the skill exists) |
| D5 | **Re-invocation behaviour** | `/vision` detects the existing section and offers to update specific fields, not overwrite | Overwrite (destroys accumulated context); append-only (makes PILOT.md grow unboundedly) |
| D6 | **Empty template in PILOT.md.jinja** | Ship the 4 section headings empty with `_TBD_` placeholders so the user sees the shape from day 1 | Omit entirely (first-session detection might not fire) |

---

## 3. Interaction with other skills

- **`/research`** (PM.1b) can feed `/vision` — "understand the competitive landscape, then fill V1 scope"
- **`/brainstorm`** runs AFTER `/vision` — vision gives the frame, brainstorm explores options within it
- **`/spec`** and **`/plan`** run downstream — they reference the V1 scope and north star

Proposed natural chain:
```
/vision → /research → /brainstorm → /spec → /plan → /orchestrate
```

Not enforced — the user can skip any step — but this is the intended flow when building from scratch.

---

## 4. Open questions (punted to plan phase)

- **Section-by-section questionnaire** — the skill asks one question per section (4 questions total) or one question per bullet inside sections (10+ questions)? Plan decides based on token economy
- **Example values** — should the skill show a filled-in example from a hypothetical project to unstick users? Plan decides based on dogfooding feedback
- **Vision versioning** — when vision is updated, do we stamp a `_Last updated: YYYY-MM-DD_` line? Plan says yes, it's cheap and audit-friendly

---

## 5. Out of scope

- **Product principles ranking** (Guillaume §03) — deferred, too meta for solo v1 projects
- **Competitive landscape** — lives in `/research`, not `/vision`
- **Success metrics** beyond the single north star — YAGNI
- **Vision validation by external reviewers** — not a skill concern

---

## 6. Next step

Execute `plan-2026-04-13-vision-skill.md`.
