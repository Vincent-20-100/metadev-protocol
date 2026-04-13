---
type: plan
date: 2026-04-13
slug: vision-skill
status: active
---

# Plan — `/vision` skill (PM.1c)

**Goal:** Ship a `/vision` skill that fills (or updates) a dedicated `## Vision`
section in `PILOT.md` — forcing solo builders to write down the product framing
(problem / target user / V1 scope / north star) before jumping into code.

**Brainstorm source:** `archive/brainstorm-2026-04-13-vision-skill.md`

**Confidence:** GREEN — decisions locked, full-auto ready.

**Scope:** **shipped in template** + skills-pack mirror. Requires editing
`template/.meta/PILOT.md.jinja` to add the empty vision block.

---

## Decisions (locked from brainstorm)

| # | Decision | Chosen |
|---|---|---|
| D1 | Form | Hybrid — skill writes into PILOT.md section, no parallel file |
| D2 | Section location | `## Vision` placed **before** "Current state" in PILOT.md template |
| D3 | Sections inside vision | 4: Problem / Target user / V1 scope / North star metric |
| D4 | Invocation cadence | Auto-**proposed** at first-session detection + manual anytime |
| D5 | Re-invocation | Detects existing section, offers per-field update, never overwrites silently |
| D6 | Empty template | Ship 4 headings with `_TBD_` placeholders so the shape is visible day 1 |
| D7 | Questionnaire style | One question per section (4 questions total) for the initial fill; per-field follow-ups on re-invocation |
| D8 | Example values | Yes, skill shows one filled-in example from a hypothetical project to unstick users |
| D9 | Timestamp on update | Yes — `_Last updated: YYYY-MM-DD_` under the `## Vision` heading |

---

## PILOT.md section template (locked)

```markdown
## Vision

_Last updated: YYYY-MM-DD_

### Problem
_TBD — run `/vision` to fill this in._
<!-- 3-5 lines: what real-world friction does this project remove? -->

### Target user
_TBD — run `/vision` to fill this in._
<!-- 2-3 bullets: who hits this friction? what do they do today instead? -->

### V1 scope
_TBD — run `/vision` to fill this in._
<!-- MoSCoW short: Must / Should / Won't (for v1) -->

### North star metric
_TBD — run `/vision` to fill this in._
<!-- One measurable metric that tells you if the project is working. -->
```

This section lands in `template/.meta/PILOT.md.jinja` between the existing header
and the "Current state" section.

---

## Tasks

### Task 1 — Update `template/.meta/PILOT.md.jinja`

- [ ] Read the current jinja file to find the right insertion point (before "## Current state")
- [ ] Insert the Vision section template from above
- [ ] Preserve jinja variable substitutions in the rest of the file

### Task 2 — Write `template/.claude/skills/vision/SKILL.md`

- [ ] Frontmatter (`name: vision`, `description: fill or update the Vision section in PILOT.md`)
- [ ] Hard rules:
  - Only edit the `## Vision` section of `PILOT.md` — never touch other sections
  - Never overwrite existing content without asking per-field
  - Always update `_Last updated: YYYY-MM-DD_` on any change
  - Show an example only once at session start, not repeatedly
- [ ] Process for first fill (all `_TBD_`):
  1. Show the example block (hypothetical project)
  2. Ask Question 1 — Problem (one question, user answers)
  3. Ask Question 2 — Target user
  4. Ask Question 3 — V1 scope (guide toward MoSCoW)
  5. Ask Question 4 — North star metric (one measurable)
  6. Show the drafted section, ask confirm
  7. Use Edit to replace the Vision section in PILOT.md
- [ ] Process for update (existing non-TBD content):
  1. Show the current Vision section
  2. Ask which fields to update (multi-select)
  3. For each selected field: show current, ask new, confirm
  4. Update timestamp
- [ ] Rationalizations table:
  - "I know my project, skip the questions" → no, the point is the written artifact
  - "I'll fill it later" → brainstorm source says the gap is that people never fill it
  - "This is too early, I don't know V1 scope yet" → MoSCoW can start with Must only, iterate

### Task 3 — Hook into first-session detection (automatism #2)

- [ ] Read `template/CLAUDE.md.jinja` automatism #2 section
- [ ] Verify first_session detection exists (should — v0.0.3 added SessionStart hook)
- [ ] Update automatism #2 to explicitly propose `/vision` when Vision section is all `_TBD_`
- [ ] Proposal wording: "I see your Vision section is empty. Want to run `/vision` to frame the project before we dive in? (You can also skip and come back later.)"

### Task 4 — Mirror in skills-pack

- [ ] Copy `template/.claude/skills/vision/` → `skills-pack/skills/vision/`
- [ ] Note in skills-pack README that this skill assumes a `PILOT.md` with a `## Vision` section — users without metadev full template need to add the section manually

### Task 5 — Dogfood in meta-repo

- [ ] Copy skill into `.claude/skills/vision/` at meta-repo root
- [ ] Run `/vision` on the meta-repo itself — fill the Vision section in `.meta/PILOT.md` as a real test
- [ ] The meta-repo's own vision is: "Premium vibe-coding setup in one command" — use the README tagline as a starting point

### Task 6 — Meta-repo PILOT.md

- [ ] Add `## Vision` section to `.meta/PILOT.md` (not the jinja — the real file)
- [ ] Fill it with the meta-repo's actual vision

---

## Ripple effects (downstream updates — MANDATORY)

| Area | File | Update | Notes |
|---|---|---|---|
| **PILOT template** | `template/.meta/PILOT.md.jinja` | Insert Vision section before Current state | Task 1 |
| **Template CLAUDE.md** | `template/CLAUDE.md.jinja` | Automatism #2 updated + `/vision` row in Skills & Agents trigger table | Trigger: "Vision section empty OR user asks about product framing" — **Propose** |
| **Meta-repo CLAUDE.md** | `CLAUDE.md` | Same trigger table row | Dogfooding parity |
| **Template skills count** | `template/CLAUDE.md.jinja` | "9 skills" → "10 skills" (assuming /research already shipped) or "8 skills" → "9 skills" if shipped alone | Order-dependent; grep at implementation time |
| **Meta-repo skills count** | `CLAUDE.md` | Same | |
| **README.md** | `README.md` | Add `/vision` row in Toolkit skills table | One-liner: "Fill the Vision section in PILOT.md — problem / user / V1 scope / north star metric" |
| **README.md** | `README.md` | Update hero bullets if they mention skills count | Grep |
| **README.md** | `README.md` | Update Rails diagram PLAN stage to add `/vision` OR consider adding a new pre-PLAN stage "FRAME" | Design question — default: add to PLAN for simplicity |
| **PHILOSOPHY.md** | `docs/PHILOSOPHY.md` | Skills count; add `/vision` row; mention in automatism #2 description | Grep "8 built-in skills" or current count |
| **CHANGELOG.md** | `CHANGELOG.md` | `[v1.2.0]` Added: `**New skill: /vision**` | If v1.2.0 section already opened by /research, add to it |
| **skills-pack/README.md** | `skills-pack/README.md` | Add `/vision` row; note PILOT.md section dependency | |
| **Template generation test** | `tests/test_template_generation.py` | Add assertion that generated PILOT.md contains `## Vision` section | Ensures the jinja change sticks |
| **Pytest skill enumeration** | `tests/test_template_generation.py` | Add `vision` to expected skill list | |
| **Meta PILOT.md** | `.meta/PILOT.md` | PM.1c → DONE + real Vision section filled via dogfood | Task 6 |
| **ARCHITECTURE.md** (meta) | `.meta/ARCHITECTURE.md` | If skills list is documented, add `/vision` | Check first |
| **CREDITS.md** | `CREDITS.md` | Re-confirm Guillaume Desforges entry mentions `/vision` as absorbed from his §03 business vision scaffolding | |

**Grep checklist (run before committing):**
```bash
grep -rn "8 skills\|9 skills" --include="*.md" --include="*.jinja"
grep -rn "first_session\|first-session\|automatism #2" --include="*.md" --include="*.jinja"
grep -rn "## Current state" template/.meta/PILOT.md.jinja
```

---

## Verification checklist

- [ ] `template/.claude/skills/vision/SKILL.md` exists
- [ ] `template/.meta/PILOT.md.jinja` has the Vision section before Current state
- [ ] `skills-pack/skills/vision/SKILL.md` mirrors the template version
- [ ] Meta-repo can invoke `/vision` and updates `.meta/PILOT.md` Vision section
- [ ] Meta-repo Vision section is actually filled (dogfood test)
- [ ] Template generation test: generated project has `## Vision` with `_TBD_` placeholders
- [ ] Automatism #2 in both template and meta CLAUDE.md proposes `/vision` on first session when Vision is TBD
- [ ] Trigger table rows added in both CLAUDE.md files
- [ ] Skills count bumped everywhere (CLAUDE.md × 2, README, PHILOSOPHY)
- [ ] README Toolkit table has `/vision` row
- [ ] README Rails diagram updated (PLAN stage or new FRAME stage)
- [ ] PHILOSOPHY.md skill count and table updated
- [ ] CHANGELOG v1.2.0 Added entry
- [ ] skills-pack README updated
- [ ] `tests/test_template_generation.py` asserts Vision section present
- [ ] `copier copy . /tmp/test-vision --defaults --trust` passes
- [ ] `uv run ruff check .` passes
- [ ] PILOT.md: PM.1c → DONE

---

## Out of scope (deferred)

- **Product principles ranking** (Guillaume's §03 item) — too meta for solo v1
- **Competitive landscape** — belongs to `/research`, not `/vision`
- **Detailed success metrics** beyond north star — YAGNI
- **External validation workflow** — not a skill concern
- **Vision history / diff view** — `_Last updated_` timestamp is sufficient audit

---

## Commit plan

Two commits:

1. `feat(skills): add /vision skill and Vision section in PILOT template`
   - `template/.claude/skills/vision/SKILL.md`
   - `template/.meta/PILOT.md.jinja` (Vision section insertion)
   - `skills-pack/skills/vision/SKILL.md`
   - `.claude/skills/vision/SKILL.md` (meta dogfood)

2. `docs: propagate /vision skill across README, PHILOSOPHY, CHANGELOG, CLAUDE.md, tests`
   - README.md
   - docs/PHILOSOPHY.md
   - CHANGELOG.md
   - template/CLAUDE.md.jinja (trigger table + automatism #2)
   - CLAUDE.md (meta)
   - skills-pack/README.md
   - CREDITS.md
   - tests/test_template_generation.py
   - .meta/PILOT.md (PM.1c done + real Vision dogfood fill)

If shipped together with `/research`, the `docs:` commit can be unified — decide at implementation time based on whether they ship in the same batch.
