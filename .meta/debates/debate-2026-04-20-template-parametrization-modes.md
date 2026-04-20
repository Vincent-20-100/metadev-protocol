# Debate Record — Template parametrization modes (light/full/flag-only)

**Date:** 2026-04-20
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user / fresh user on day 1)
**Status:** USER DECISION NEEDED

---

## Subject

Should metadev-protocol ship a copier parametrization to reduce friction for "mini / throwaway" projects?

- **Option A — Full binaire**: `mode: light | full` copier question. `light` = no `.pre-commit-config.yaml` + no empty `data/` dirs. `full` = current state.
- **Option B — Single-mode + doc**: no copier question. Template stays monolithic. README documents "for throwaway, `rm .pre-commit-config.yaml && rm -rf data/`".
- **Option C — Flag-dossiers-only**: `empty_dirs: yes/no` flag only. Hooks always present (non-negotiable). "Light" = just fewer dirs.

## Angles

- **A (Puriste):** correctness, YAGNI discipline, doctrinal coherence [insider]
- **B (Pragmatique):** ship now, solo-dev realism, DX friction minimization [insider]
- **C (End-user):** fresh user on day 1 of metadev-protocol, zero accumulated context [lone wolf]

---

## Strong arguments (survived cross-critique)

- **A1 — Matrix testing cost is real** — raised by Puriste, conceded by Pragmatique in Phase 2. Every flag × 4 existing profiles = 8 CI variants per PR. Bisectability (R015 in `branching.md`) suffers.
- **A4 — Doctrinal coherence: templates teach by example** — raised by Puriste, conceded by all agents. The recursive nature of metadev-protocol means every design choice is a pedagogical signal. A `mode: light` flag that disables hooks teaches "discipline is negotiable" to downstream projects. Decisive argument.
- **B5 — Ruff precedent proves friction is not hypothetical** — raised by Pragmatique, conceded by Puriste in Phase 2. The 2-week debugging loop (PR-1 + PR-2.5) is hard evidence that "full" defaults create predictable friction. The pain cluster exists.
- **C1 — Information gap at `copier copy` time** — raised by End-user, conceded by Pragmatique in Phase 2. A new user has never felt "12 hooks" and cannot evaluate the light/full tradeoff before experiencing it.
- **C2 — "Throwaway" is retrospective, not upfront** — raised by End-user, conceded by both insiders in Phase 2. Nobody declares "this is a weekend experiment" on Day 1. Day 1 quick prototype → Day 7 production is the norm. Upgrading from a deliberately degraded state is a worse path than never degrading.
- **C3 — Every copier question is an abandonment event** — raised by End-user, uncontested. CLI onboarding research: friction at setup is the single largest churn predictor.
- **C5 — Hooks and empty dirs are asymmetric concerns** — raised by End-user, became the convergence point. Hooks = load-bearing safety (non-negotiable). Empty dirs = aesthetic/pedagogical (genuinely optional). Treating them as one "mode" conflates two problems.

## Lone wolf insights (survived cross-critique)

- **"Throwaway is retrospective, not upfront"** (C2) — the observation insiders missed because they thought in terms of user *intent* rather than user *trajectory*. This insight alone invalidates Option A's premise.
- **"Every copier question is an abandonment event"** (C3) — the outsider saw the onboarding funnel as a funnel, not as a series of deliberate choices. Insiders saw "cost-free parametrization"; the wolf saw "an extra gate".
- **"Light = broken template"** (C4) — the wolf refused to frame hook-less as a lighter version. Shipped as equivalent choices, they send a wrong pedagogical signal. Hardened in Phase 2 after Puriste's A4 landed.

The wolf drove the debate's convergence. Without C2, Pragmatique's B3 (upgrade path needs parametrization) would have held; C2 exposed B3 as solving a problem the flag creates.

## Contested arguments (no consensus)

- **B1 — Bimodal user distribution (30% throwaway)** — raised by Pragmatique, acknowledged by both others as empirically plausible but unverified. End-user conceded "I cannot disprove it from first principles." Puriste called the figure a speculation without external user requests. **Why it matters:** if 30% is correct, a flag for those users is justified (Option A becomes live again). If it's <5%, the testing cost wins (Option B or C). Empirical gap not resolvable in this debate.
- **B3 — Upgrade path needs the flag** — raised by Pragmatique, refuted by end-user in Phase 2. Agent C's counter: "`copier update` diffs against the previous tag regardless of whether you graduated from `light` or manually added hooks. The flag documents intent; it doesn't simplify the upgrade path technically." Pragmatique conceded in Phase 2 ("retrofitting justification"). Argument died.

## Dismissed arguments (refuted or irrelevant)

- **A2 — Empty dirs are pedagogical** — raised by Puriste, refuted by End-user in Phase 2. Pedagogical value is "front-loaded and non-repeating"; experienced users just delete them. Empty dirs are noise-not-teaching for project #2 onwards.
- **A3 — "Nobody asked for this" YAGNI veto** — raised by Puriste, partially refuted by Pragmatique in Phase 2 via ruff precedent. YAGNI as absolute veto lost ground; it survives as a weighting factor, not a stop-sign.
- **A5 — Upgrade path independent of flag** — raised by Puriste, CONFIRMED (not refuted). This argument moves to "strong uncontested" once Option A is off the table. No parametrization needed to enable upgrades.
- **B4 — YAGNI cuts both ways: "just delete files" is reverse-engineering** — raised by Pragmatique, partially conceded by Puriste. But softened when C5 reframed: if hooks are non-negotiable, there's no "files to delete" problem. B4 dissolves under Option C.

## Convergence points (all 3 agents agree in Phase 2)

- **Hooks are non-negotiable** — safety scaffolding that ships on every project. Disagreement on how to communicate this, but not on whether.
- **Empty dirs are the only genuinely optional element** — no load-bearing purpose beyond pedagogy. Asymmetric with hooks.
- **Option A is off the table** — `mode: light | full` creates more problems than it solves. Unanimous rejection in Phase 2.
- **Documentation alone is insufficient** — Option B's "just add a paragraph to README" lost the wolf ("lone wolf at 11pm doesn't read docs"). Unanimous agreement in Phase 2 that docs don't absorb friction.

## Irreducible tensions

- **Is `empty_dirs: no` actually zero-cost?** Agent A's caveat survives: "if the dirs have hidden purpose (linting picks them up, copier update logic depends on them, etc.), that assumption fails, and I'm back to Option B." This is an empirical question to resolve before committing.
- **B1 (30% throwaway) remains unverified.** If external user data shows the figure is real, the flag-only solution still underserves a cohort that wants less scaffolding than Option C provides. No resolution possible without empirical data.

---

## Recommendation

**Option C — `empty_dirs: yes/no` flag, hooks non-negotiable.** All 3 agents converged here in Phase 2.

**Confidence: HIGH**, contingent on one empirical check:

1. Verify that the empty dirs (`data/{raw,interim,processed}/`, possibly others) are not referenced by any hook, script, CI workflow, or rule. If any file grep for `data/raw` or similar returns load-bearing dependencies, the flag breaks the template invisibly → fallback to Option B.

**Design specifics:**
- `copier.yml` question: `empty_dirs: yes/no`, default `yes` (mirror current behavior, zero surprise for existing users).
- Jinja-conditional `{% if empty_dirs %}` wraps the dir creation in template config.
- Document the flag in a new line in `copier.yml` help text — NOT in README. Users see the choice at `copier copy` time; no need to seek it.
- Upgrade path: `copier update` natively works. If a user starts with `empty_dirs: no` and later wants them, they re-run with `empty_dirs: yes` and accept the added files.

**What this debate rejects:**
- Option A (mode flag) — dies on C2 (throwaway is retrospective) and A1 (matrix cost).
- Option B (monolithic + doc) — dies on C3 (docs don't absorb friction) and B5 (real pain exists).

## Decision

**USER DECISION NEEDED**

Key questions to confirm before implementing:

1. **Empirical check (blocker):** Do any hooks / scripts / CI workflows / rules reference `data/{raw,interim,processed}/` or similar dirs? If yes, the flag must handle those references, or Option B wins by default.
2. **Default value:** Default `empty_dirs: yes` (mirror current, no surprise) or `empty_dirs: no` (optimize for the "weekly experiment" pattern)? Recommendation: `yes` — zero change for current users, opt-in for experimenters.
3. **B1 (30% throwaway) — worth verifying before v2.1 launch?** If external users confirm <5%, even the empty_dirs flag might be YAGNI. If ≥20%, flag is clearly justified. Currently: no external data.
