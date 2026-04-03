# ADR-003 — Rewrite CLAUDE.md.jinja and add SESSION-CONTEXT.md

**Date:** 2026-04-01
**Status:** IMPLEMENTED
**Sources:**
- `.meta/references/state-of-the-art-vibe-coding.md` (finding #1: <200 lines)
- `.meta/references/audit-egovault.md` (patterns #2, #3, #7)
- ADR-001 decisions #1, #2, #3, #6

---

## Problem

The initial template CLAUDE.md (v1) was functional but:
- No anti-LLM rules (recurring AI errors were not addressed)
- No session workflow (the AI did not know where to start)
- No document hierarchy (what takes precedence over what?)
- No SESSION-CONTEXT.md (the cockpit had only one file)

## Decisions

### 1. CLAUDE.md < 120 lines

**Why:**
- Boris Cherny (creator of Claude Code) keeps his CLAUDE.md at ~100 lines / 2500 tokens
- Beyond ~200 lines, compliance drops significantly
- The old EgoVault CLAUDE.md was 350 lines = rules at the end of the file
  were often ignored

**Result:** 57 lines (minimal profile), 63 lines (app profile).
The detail (Wrong/Right examples of EgoVault G1-G13 rules) is in the
skills and docs, NOT in CLAUDE.md.

**Confidence level: HIGH** — Sizing is documented by the tool's creator.
The logic is simple: the shorter it is, the more it gets read.

### 2. Anti-LLM rules (G2, G5, G6, G13)

**What:** 4 universal rules extracted from EgoVault's 13, plus 2 profile-specific ones.

**Universal rules:**
- **R4 — Docstrings WHAT not HOW** (source: EgoVault G2) — LLMs tend
  to describe the implementation rather than the contract
- **R5 — No over-engineering** (source: EgoVault G5) — LLM trap #1:
  premature abstractions, factories of factories, useless patterns
- **R6 — Every except must log or re-raise** (source: EgoVault G6) — LLMs write
  silent `except: pass` by default
- **R7 — Surgical comments** (source: EgoVault G13) — LLMs drown code
  in obvious comments ("# Initialize the variable")

**Profile-specific rules:**
- **app:** R8 thin routing (<15 lines) + R9 dependency injection
- **quant:** R8 zero Python loops (vectorization) + R9 document math assumptions
- **data:** R8 idempotent pipelines + R9 raw data immutable

**Why these 4 and not all 13:**
- Budget of 120 lines = cannot include everything
- G1 (library names), G4 (inter-layer imports), G7-G12 are too
  specific to EgoVault's hexagonal architecture
- The 4 chosen apply to ALL Python projects, regardless of profile

**Where the idea comes from:** EgoVault audit section 4, confirmed by the state of the art
which says "verification commands > style guidelines" but LLM anti-patterns
are an exception — they MUST be in CLAUDE.md.

**Confidence level: HIGH** — Tested on 374 tests in EgoVault. The 4 rules
are the most universal. The risk = adding too many, not having too few.

### 3. Two-file cockpit (PILOT.md + SESSION-CONTEXT.md)

**What:**
- `PILOT.md` = factual state (what) — status table, next steps
- `SESSION-CONTEXT.md` = decision context (why) — active decisions,
  pitfalls, open questions

**Why 2 files instead of 1:**
- Source: EgoVault uses PROJECT-STATUS.md + SESSION-CONTEXT.md successfully
- PILOT.md accumulates (rows are added to the table)
- SESSION-CONTEXT.md is REWRITTEN each session (not appended to)
- The rewrite forces keeping only the relevant context = no bloat
- A single file always ends up becoming an unreadable log

**The key rule: "rewrite, don't append"**
- SESSION-CONTEXT.md is NOT a journal
- Each session, active decisions are rewritten from scratch
- Obsolete reasoning is deleted, not commented out
- This keeps the file under 50 lines = always readable

**How to use it:**
1. Start of session: Claude reads PILOT.md (state) + SESSION-CONTEXT.md (context)
2. During the session: decisions are made with the context in mind
3. End of session: update PILOT.md (new status) and REWRITE
   SESSION-CONTEXT.md (new context for the next session)

**Confidence level: HIGH** — Tested and validated on EgoVault (2+ months of use).
The "rewrite" pattern is counterintuitive but that is what makes it effective.

### 4. Five-phase workflow

**What:** Research > Plan > Implement > Test > Ship

**Why 5 and not 7 (EgoVault had 7):**
- EgoVault: BRAINSTORM > SPEC > PLAN > IMPLEMENT > TEST > AUDIT > SHIP
- BRAINSTORM and SPEC merged into "Research" — a bootstrap does not need
  formal specs
- AUDIT removed — too heavy for a new project, relevant for mature projects
- State of the art confirms: "Research > Plan > Execute > Review > Ship" is
  the universal workflow

**Where the idea comes from:**
- EgoVault (simplified)
- State of the art finding #7 (convergence from all sources)

**Confidence level: MEDIUM** — The workflow is consensual but has not been
tested as-is on a project from scratch. EgoVault used the 7-phase version.
The simplification is a reasonable bet.

### 5. Document hierarchy

**What:** CLAUDE.md > `.meta/decisions/` > docstrings > inline comments

**Why:**
- Source: EgoVault CLAUDE.md §3 ("permanent wins on conflict")
- When Claude finds a contradiction between CLAUDE.md and a comment
  in the code, it needs to know what to follow
- `.meta/` is provisional (AI workspace), `docs/` is permanent

**Confidence level: HIGH** — This is a common-sense convention. The risk
is negligible.

---

## Impacted files

| File | Action |
|------|--------|
| `template/CLAUDE.md.jinja` | REWRITTEN — v2 with rules, workflow, hierarchy |
| `template/.meta/PILOT.md.jinja` | UPDATED — 5-phase workflow added |
| `template/.meta/SESSION-CONTEXT.md.jinja` | CREATED — decision cockpit |
