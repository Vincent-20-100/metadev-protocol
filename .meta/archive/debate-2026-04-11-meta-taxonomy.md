# Debate Record — `.meta/` taxonomy (state-outer vs type-outer vs hybrid-matrix)

**Date:** 2026-04-11
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user — cold-start DX perspective)
**Status:** USER DECISION NEEDED

---

## Subject

`.meta/` in this repo currently conflates drafts, validated artifacts, and archived
artifacts under `scratch/`. 14 files in `scratch/` mix real drafts with validated
specs/plans (launch-plan.md, plan-rodin-agent.md, plan-workflow-gates.md,
spec-workflow-gates.md); 22 files in `references/` are unsorted research.

We need a taxonomy that serves 4 drivers simultaneously:
- (a) gitignore visibility — one simple rule
- (b) discoverability — find "all plans" / "all specs" without hunting
- (c) lifecycle workflow — status change reflected by file movement
- (d) historical archival — chronological sort, retrieve past decisions
- (e) onboarding for external visitors (public template repo)

Filename convention already decided: dates in filename for chronological sort.

## Angles

- **A (Puriste):** correctness, clean semantic boundaries, enforceable invariants [insider]
- **B (Pragmatique):** ship fast, minimize friction on the common case [insider]
- **C (End-user):** cold-start DX, minimum mental load for cold visitors [lone wolf]

---

## Strong arguments (survived cross-critique)

- **State-outer enables invariant enforcement via filesystem structure** — raised by A,
  conceded by B. A file cannot exist simultaneously in `active/` and `archive/` if state
  is the outer partition. Human discipline fails; filesystem hierarchy doesn't.

- **State-outer gives trivial gitignore** — raised by A and C, uncontested. Two rules
  (`.meta/drafts/`, `.meta/trash/`) cover the entire visibility control concern. Any
  type-outer structure requires multi-line rules that are fragile to reorganization.

- **Nested `state/type/file` is over-engineering** — raised by C, conceded by A. The
  filename already encodes the type (`plan-`, `spec-`, `debate-`). A second `plans/`
  directory repeats the same information. Three levels for a markdown file is excessive
  for a small team.

- **"What's alive?" is the first question for cold visitors** — raised by C, uncontested.
  A public-repo visitor arriving at `.meta/` on GitHub wants to know current state
  before wanting to know content type. State-outer answers that question in one click.

- **File creation (high frequency) vs status transitions (low frequency)** — raised by B,
  partially conceded. B was right that creation is 5-10x more frequent than graduation,
  which initially argued against state-outer. BUT — conceded by B in Phase 2 — flat
  state-outer's creation cost is just "save to the right folder", not substantially
  different from type-outer's "save to the right type/state subfolder".

- **`git mv` makes lifecycle transitions reviewable** — raised by A, uncontested. Moving
  a file between state directories produces a commit that documents the graduation,
  better than a silent rename or metadata update.

## Lone wolf insights

- **C's "filename + tooling" is stronger than C's initial pitch.** The cold-start
  visitor argument exposed a real blindspot insiders missed: both A and B assumed
  the visitor starts with a type-question ("give me a plan") when the actual
  cold-start question is state-first ("what's alive here?"). This reversed A's
  position on nesting.

- **Enforcement via tooling, not structure, is consistent with the repo's method.** C's
  Phase 2 fix — a pre-commit hook or scaffolding skill for prefix validation — isn't
  a hack. It's exactly the kind of guardrail metadev-protocol builds for other things.
  Using tooling to enforce the invariant lets the structure stay flat without losing
  robustness.

## Contested arguments (no consensus)

- **Is the type-prefix discipline robust enough?** A argued tooling-enforced
  convention is always weaker than filesystem-enforced structure. C argued tooling
  can validate *content* (not just naming) which structure cannot. This is a real
  tension — but both agreed the flat structure is the right base; the disagreement
  is about the enforcement layer on top.
  - **For structural (A):** zero setup, impossible states are impossible
  - **For tooling (C):** extends to content validation, consistent with the method
  - **Mitigation:** start with convention + lightweight lint (CI check) — add a
    scaffolding skill later only if errors happen

## Dismissed arguments (refuted or irrelevant)

- **Type-outer (Option B as originally framed)** — B himself retracted it in Phase 2.
  The "type-first mental model" argument collapsed when C pointed out that filename
  prefixes already serve the type-filtering need with zero directory overhead.

- **Nested state/type hierarchy (Option A as originally framed)** — A himself retracted
  the nesting in Phase 2. The invariant-enforcement value comes from having state as
  the outer partition; the inner type subfolder adds no invariants the prefix doesn't.

- **"Automation breaks with flat + prefix" (B's counter to C)** — dismissed.
  `find .meta -name 'plan-*'` is one command and works cross-state. B conceded this.

## Convergence points

- **Flat state-outer with type encoded in filename prefix** (3/3)
- **Top-level directories:** `active/`, `archive/`, `drafts/`, `trash/` (3/3)
- **Filename format:** `<type>-<YYYY-MM-DD>-<slug>.md` (3/3)
- **Gitignore:** `.meta/drafts/` + `.meta/trash/` — nothing else (3/3)
- **`git mv` for lifecycle transitions** (3/3)
- **Tooling should enforce prefix convention** (3/3 — A conceded in Phase 2)

## Irreducible tensions

- **Where do `sessions/` go?** Session archives are dated and don't graduate — they're
  born in `archive/` essentially. Do they get a prefix (`session-YYYY-MM-DD.md`) in
  `archive/`, or do they stay as a carved-out subfolder (`archive/sessions/`)? Not
  resolved in the debate.

- **What about `references/` (22 files of raw research)?** Not covered by the taxonomy
  debate. These are neither state nor lifecycle — they're external inputs. Separate
  decision needed (user already flagged: sort bronze/silver/gold).

- **What about `debates/` (current location)?** Debates are born as historical records —
  they never have an "active" state. Do they get `debate-YYYY-MM-DD-slug.md` in
  `archive/`, or stay in a dedicated `debates/` folder? The debate didn't converge.

## Recommendation

**Confidence: high on the core structure. Medium on edge cases.**

### Recommended structure

```
.meta/
├── active/                              # validated, not yet implemented / still referenced
│   ├── plan-2026-04-11-workflow-gates.md
│   ├── spec-2026-04-11-workflow-gates.md
│   └── ...
├── archive/                             # implemented / historical
│   ├── plan-2026-03-15-mvp-phase-a.md
│   ├── debate-2026-04-08-meta-visibility.md
│   ├── session-2026-04-09-l-etudiant.md
│   └── ...
├── drafts/                              # WIP, gitignored
│   └── .gitkeep
├── trash/                               # explicit "to delete" staging, gitignored
│   └── .gitkeep
├── decisions/                           # ADRs — stay as-is (already well organized)
├── PILOT.md
├── SESSION-CONTEXT.md
├── ARCHITECTURE.md
├── DECISIONS.md
└── GUIDELINES.md
```

### Gitignore rules (one block)

```
.meta/drafts/
!.meta/drafts/.gitkeep
.meta/trash/
!.meta/trash/.gitkeep
```

### Filename convention

- Format: `<type>-<YYYY-MM-DD>-<kebab-slug>.md`
- Types: `plan`, `spec`, `brainstorm`, `debate`, `session`, `reference` (optional)
- Date = creation date for active artifacts; for archived, the date is preserved
  (not rewritten at archive time)

### Enforcement

Start lightweight:
1. Document the convention in GUIDELINES.md
2. Add a pre-commit hook that rejects files in `active/` or `archive/` without the
   `<type>-<YYYY-MM-DD>-*` pattern — **cheap to write, catches 100% of prefix errors**
3. Defer scaffolding skill (`/new plan <topic>`) until manual creation becomes painful

### Migration of existing files

- `scratch/` → user-driven triage into `active/` (validated, still referenced),
  `archive/` (implemented), `drafts/` (WIP), `trash/` (delete)
- `references/` → separate bronze/silver/gold triage (not in this debate's scope)
- `debates/debate-meta-visibility.md`, `debate-workflow-gates.md`, etc. → rename
  with date prefix and move to `archive/` or keep `debates/` as an exception

## Decision

**USER DECISION NEEDED**

Key questions to resolve:
1. **Accept the core structure?** (flat state-outer + prefix convention + lightweight hook)
2. **Resolve the 3 irreducible tensions:**
   - Sessions: prefix in `archive/` or dedicated subfolder?
   - References: separate system (bronze/silver/gold)?
   - Debates: rename + move to `archive/`, or keep `debates/` as an exception?
3. **Enforcement layer:** pre-commit hook now, scaffolding skill later?
4. **Migration strategy:** manual triage file-by-file, or bulk rules + spot-check?
