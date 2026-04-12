---
type: plan
date: 2026-04-13
slug: absorb-claude-starter-prose
status: active
---

# Plan — Absorb claude-ai-project-starter prose (PM.1a)

**Goal:** Merge the zero-risk, doc-only items from
`brainstorm-2026-04-12-claude-ai-project-starter.md` §4.1 into our prose
layer (PHILOSOPHY, GUIDELINES, CLAUDE.md) without importing any enforcement
or structural change. One commit, reviewable in under 5 minutes.

**Source:** `.meta/active/brainstorm-2026-04-12-claude-ai-project-starter.md` §4.1.

**Confidence:** GREEN — source brainstorm already triaged each item with
target file and rationale. Full-auto ready.

**Scope:** 11 items from §4.1, nothing from §4.2, §4.3, §4.4.

---

## Decisions (locked)

| # | Decision | Chosen | Reason |
|---|---|---|---|
| D1 | Which items | §4.1 batch only: A2, A3, A4, A6, A7, B1, B2, B4, B5, B6, B8 | Brainstorm explicitly marks this set as zero-risk |
| D2 | Which items deferred | §4.2 (C1 vision / C2 wiki / C3 /research) → new PENDING backlog entries | All three need dedicated brainstorm per source doc |
| D3 | Commit granularity | Single commit, message starts `docs(philosophy): absorb ...` | Source doc explicitly recommends this |
| D4 | Target files | PHILOSOPHY.md, template GUIDELINES.md.jinja, template CLAUDE.md.jinja, new adr template | Source §4.1 locks these |
| D5 | Prose style | Preserve author voice where quotes are strong; attribute openly in CREDITS | CREDITS.md already has a precedent |
| D6 | Template test | `copier copy . /tmp/test-absorb --defaults --trust --vcs-ref=HEAD` required | Rule #2 + #3: template changes must be tested |
| D7 | Em dashes | Keep them (brainstorm §4.4 D2 explicitly rejects the "no em dash" rule) | Our house style loves em dashes |

---

## Item-by-item mapping (from brainstorm §4.1)

### Block A — Philosophy & prose

| ID | Content | Target file | Placement |
|----|---------|-------------|-----------|
| A2 | Three pillars: Product excellence / Technical agility / AI intensity | `docs/PHILOSOPHY.md` | New section after "Core principles" or as a prelude |
| A3 | 5-step working rhythm (intent → draft → review → commit → improve) | `template/.meta/GUIDELINES.md.jinja` | New "Working rhythm" subsection under "Working with AI" |
| A4 | Anti-patterns trio: over-engineering / knowledge amnesia / perfectionism paralysis | `template/.meta/GUIDELINES.md.jinja` | Add to existing anti-patterns list |
| A6 | **"If you find yourself correcting AI on the same thing twice, add it to CLAUDE.md"** | `template/CLAUDE.md.jinja` | Top of the rules section as a sidebar quote |
| A7 | "Outdated documentation reduces AI effectiveness more than no documentation" | `template/.meta/GUIDELINES.md.jinja` | Documentation section |

### Block B — Engineering defaults

| ID | Content | Target file | Placement |
|----|---------|-------------|-----------|
| B1 | Trunk-based + local CI: "The real CI is the discipline of always keeping `main` green" | `template/.meta/GUIDELINES.md.jinja` | Git workflow section |
| B2 | Modular monolith as default; "AI reasons about a monolith far better than a mesh of services" | `template/.meta/GUIDELINES.md.jinja` | Architecture section |
| B4 | Dependencies are a liability — ask stdlib first | `template/.meta/GUIDELINES.md.jinja` | Already partially present; strengthen wording |
| B5 | Errors are knowledge — fix root cause, not symptom | `template/.meta/GUIDELINES.md.jinja` | Debugging section |
| B6 | Automate what repeats — third occurrence triggers automation | `template/.meta/GUIDELINES.md.jinja` | Automation section |
| B8 | 4-question tech stack decision framework → ADR template | `template/.meta/decisions/adr-template.md.jinja` | **NEW FILE** |

---

## Tasks

### Task 1 — Read target files

- [ ] Read `docs/PHILOSOPHY.md` to find the right anchor for A2 (three pillars)
- [ ] Read `template/.meta/GUIDELINES.md.jinja` to find anchors for A3, A4, A7, B1, B2, B4, B5, B6
- [ ] Read `template/CLAUDE.md.jinja` to find the rules section for A6
- [ ] Check if `template/.meta/decisions/` has an existing ADR template file; if yes, update rather than create

### Task 2 — Write the three pillars (A2) into PHILOSOPHY.md

- [ ] Add a "Three pillars" section. Preserve the three short quotes as-is, attribute to Guillaume Desforges / claude-ai-project-starter in a footnote
- [ ] Keep under 150 words total

### Task 3 — Write working rhythm (A3) into GUIDELINES.md.jinja

- [ ] Add "Working rhythm" subsection under "Working with AI":
  1. Define intent clearly (what, why, constraints)
  2. Let AI draft / research / implement
  3. Review critically (AI is confident but not always right)
  4. Commit, capture knowledge, move on
  5. Improve — learn from wins and failures
- [ ] One line per step, no fluff

### Task 4 — Add anti-patterns trio (A4) to GUIDELINES.md.jinja

- [ ] Add to existing anti-patterns list or create one if missing:
  - Over-engineering — building for hypothetical scale
  - Knowledge amnesia — re-deciding the same thing next month
  - Perfectionism paralysis — polishing what should ship

### Task 5 — Add correction rule (A6) to CLAUDE.md.jinja

- [ ] Add a callout near the top of the rules section:
  > "If you find yourself correcting the AI on the same thing twice, add it to
  > CLAUDE.md — the rule belongs in the contract, not in your memory."
- [ ] Attribute in a comment, not inline

### Task 6 — Add doc-decay rule (A7) to GUIDELINES.md.jinja

- [ ] Add to Documentation section:
  > "Outdated documentation reduces AI effectiveness more than no documentation.
  > Update docs at the same commit that changes behaviour — never later."

### Task 7 — Strengthen engineering defaults (B1-B6) in GUIDELINES.md.jinja

- [ ] B1: Git workflow section — add trunk-based + local-CI framing
- [ ] B2: Architecture section — add modular monolith rationale
- [ ] B4: Dependencies section — tighten "ask stdlib first" wording
- [ ] B5: Debugging section — "Errors are knowledge. Fix the root cause, not the symptom."
- [ ] B6: Automation section — "Third occurrence triggers automation."

### Task 8 — ADR template (B8) — NEW FILE

- [ ] Create `template/.meta/decisions/adr-template.md.jinja` with the 4-question framework:
  ```markdown
  # ADR NNN — <title>

  **Date:** YYYY-MM-DD
  **Status:** proposed / accepted / superseded by ADR NNN

  ## 1. What problem are we solving?
  ## 2. What alternatives did we consider?
  ## 3. Why this choice?
  ## 4. What is the exit cost if we're wrong?
  ```
- [ ] Verify the file gets copied by `copier` (run template test)

### Task 9 — CREDITS update

- [ ] Add a line to `CREDITS.md` under the existing claude-ai-project-starter entry:
  "v1.2.0 — absorbed philosophy prose and engineering defaults (A2, A3, A4, A6, A7, B1, B2, B4, B5, B6, B8)"
- [ ] Preserve existing credit if already present

### Task 10 — Template generation test

- [ ] Run `copier copy . /tmp/test-absorb --defaults --trust --vcs-ref=HEAD`
- [ ] Verify `.meta/GUIDELINES.md`, `CLAUDE.md`, and `.meta/decisions/adr-template.md` in the generated project contain the new content
- [ ] `cd /tmp/test-absorb && uv run ruff check .` passes
- [ ] Delete `/tmp/test-absorb`

### Task 11 — Follow-up backlog entries

- [ ] Update `.meta/PILOT.md` Post-merge backlog:
  - `PM.1a` → DONE
  - Add **PM.1b** — C3 `/research` skill — PENDING (needs brainstorm: scope boundary vs `/brainstorm`)
  - Add **PM.1c** — C1 vision scaffolding — PENDING (needs brainstorm: skill vs PILOT section vs hybrid)
  - Add **PM.1d** — C2 wiki tier — PENDING (needs brainstorm: boundary with decisions/ and archive/)
- [ ] Move `brainstorm-2026-04-12-claude-ai-project-starter.md` to `archive/` — its §4.1 is absorbed, §4.2/4.3 become the backlog entries above

---

## Verification checklist

- [ ] All 11 items from §4.1 land in the right files
- [ ] No items from §4.2/§4.3/§4.4 sneak in
- [ ] `CLAUDE.md.jinja` contains the A6 callout
- [ ] `PHILOSOPHY.md` contains the A2 three pillars with attribution
- [ ] `GUIDELINES.md.jinja` contains A3, A4, A7, B1, B2, B4, B5, B6
- [ ] `adr-template.md.jinja` exists and contains the 4-question framework
- [ ] `CREDITS.md` acknowledges the absorption
- [ ] Template generation test passes
- [ ] `ruff check` on meta-repo passes
- [ ] Brainstorm file moved to archive/
- [ ] PILOT.md backlog updated with PM.1a DONE + PM.1b/c/d PENDING

---

## Out of scope (deferred)

- **C1 vision scaffolding** → PM.1c PENDING, needs brainstorm
- **C2 wiki tier** → PM.1d PENDING, needs brainstorm
- **C3 /research skill** → PM.1b PENDING, needs brainstorm (boundary with /brainstorm)
- **Block A1** (README hero rewrite) — deferred to a README v2 decision
- **Block A5, A8, A9** — post-v1.2 (brainstorm §4.3)
- **Block B3, B7, B9** — post-v1.2 (brainstorm §4.3)
- **Block C4, C5** — post-v1.2

---

## File summary (for full-auto execution)

**New files:**
- `template/.meta/decisions/adr-template.md.jinja`

**Modified files:**
- `docs/PHILOSOPHY.md` (A2)
- `template/.meta/GUIDELINES.md.jinja` (A3, A4, A7, B1, B2, B4, B5, B6)
- `template/CLAUDE.md.jinja` (A6)
- `CREDITS.md` (attribution line)
- `.meta/PILOT.md` (backlog update)

**File moves:**
- `.meta/active/brainstorm-2026-04-12-claude-ai-project-starter.md` → `.meta/archive/`

**Commit:** `docs(philosophy): absorb framing and engineering-defaults prose from claude-ai-project-starter`
