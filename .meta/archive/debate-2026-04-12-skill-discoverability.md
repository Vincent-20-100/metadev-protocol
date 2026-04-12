# Debate Record — Skill Discoverability Mechanism

**Date:** 2026-04-12
**Preset:** architecture
**Mode:** standard
**Context:** hybrid
**Wolf:** Agent C (UX Designer)
**Status:** DECIDED

---

## Subject

What mechanism guarantees the LLM proactively proposes and uses skills/agents in metadev-protocol generated projects? Options: (A) reinforce decision tree, (B) new automatism with trigger table, (C) enrich Skills section with inline triggers, (B+C) combine.

## Angles

- **A (Centraliste):** A dedicated automatism is the only reliable mechanism — the LLM respects Law, not Reference [insider]
- **B (Minimaliste):** Enriching Skills section suffices — every new automatism dilutes the existing ones [insider]
- **C (UX Designer):** The problem isn't where to put triggers but whether the LLM can detect the signals [lone wolf]

## Strong arguments (survived cross-critique)

- **"Vague idea is not a detectable signal"** — raised by C, uncontested by A or B. Fatal to any trigger table based on user intent labels. Reframes the entire problem.
- **"Automatisms are execution contracts, not documentation"** — raised by A, conceded by B and C. The Law/Reference distinction is mechanically real.
- **"YAGNI — no data on which triggers work"** — raised by B, uncontested. Starting light is prudent.

## Lone wolf insights

- **Inversion of the detection problem** — instead of detecting vagueness (impossible), detect absence of specificity (tractable). If the user doesn't name a file/function/action, a skill probably applies. This reframes triggers from "match a rare pattern" to "default behavior unless clearly unnecessary."
- **"Proposed ≠ used"** — every confirmation step loses users. The friction gap must be designed explicitly, not assumed away.

## Contested arguments (no consensus)

- **Token cost of automatism vs inline** — B says 40 vs 20 tokens matters at scale. A says they do different work (Law ≠ Reference), so comparison is invalid. Unresolved but moot if we start with inline + promotion path.

## Dismissed arguments

- **"Tables scale" (A)** — future argument, not present need. YAGNI.
- **"Token math at 1000 projects" (B)** — precise calculation on imprecise assumptions.
- **A's deviation to public-safety hard gates** — conflated pre-commit hooks with skill proposals, off-topic.

## Convergence points

- All 3: trigger conditions must be based on observable signals, not retrospective labels
- All 3: co-location of triggers with skill definitions reduces maintenance drift
- A+C: the Law/Reference distinction matters mechanically
- B+C: start minimal, promote based on evidence

## Irreducible tensions

- **Authority vs friction** — Law (automatism) guarantees execution but creates friction for experts. Reference (inline) respects autonomy but risks being ignored. The promotion path is a compromise, not a resolution.

## Decision

**DECIDED: Level 1 (enriched Skills table with inverted default) + Level 2 (devil's advocate Rule of 3 as automatism)**

Inverted default instruction: "If the user's message does not reference a specific file, function, or concrete action, at least one skill applies. Check the trigger table before responding."

Promotion path: if inline triggers prove insufficient after real usage, promote to dedicated automatism.
