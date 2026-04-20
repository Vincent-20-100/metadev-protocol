# Debate Record — Hooks↔Rules doctrine (4 decisions)

**Date:** 2026-04-20
**Preset:** architecture
**Mode:** standard (one-pass per user instruction "tranche en une passe")
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user persona — DX-focused, minimal project context)
**Status:** USER DECISION NEEDED

---

## Subject

4 doctrine decisions blocking the PR-1+PR-2 execution for the hooks↔rules audit (see `.meta/drafts/audit-hooks-rules-2026-04-20.md`).

## Angles

- **A (Puriste):** correctness, parsing automation, long-term maintainability [insider]
- **B (Pragmatique):** ship now, minimize friction, low-maintenance [insider]
- **C (End-user / lone wolf):** simplicity, DX, readability for a fresh metadev user

---

## D1 — Enforcement metadata format

| Agent | Position |
|---|---|
| A Puriste | **YAML frontmatter** — mechanically parseable, auditable |
| B Pragmatique | **Filename convention** (`hardblock-*.md`) — zero parsing, brutally visible |
| C End-user | **Markdown header** (`> **Enforcement:** hard-block`) — first thing the eye sees |

### Strong arguments

- **Puriste A1** — "Filename convention is unverifiable at import time ; one person names `yagni.md` when it should be `advisory-yagni.md` and the system breaks silently." Valid against B.
- **End-user C1** — "Frontmatter is invisible until you know to look for it. A dev who opens the file in an editor sees prose, not metadata." Valid against A.
- **Pragmatique B2** — "A rule that looks enforceable but isn't creates false confidence." Valid point but not decisive.

### Contested

- Puriste invokes tooling needs ("find | grep" audit, CI validation). End-user's red line is explicit: "If the project ships a linting script that actually reads enforcement metadata at hook time, frontmatter earns its keep. Until then it's infrastructure for hypothetical tooling."
- **Crux** : does the repo *actually need* programmatic metadata extraction NOW, or is it YAGNI ?

### Orchestrator synthesis

The audit itself (this debate's parent) proposes a generable hook↔rule matrix as future tooling. That's not hypothetical — it's the next chantier after PR-4. So puriste's "parsing automation" has a concrete user (future audit regen). **But** frontmatter YAML + markdown header are NOT mutually exclusive: we can have BOTH (frontmatter for parsing, a first-line blockquote for humans).

**Recommendation: hybrid A+C**. Every rule file starts with YAML frontmatter (`enforcement: hard-block`) PLUS a one-line blockquote `> **Enforcement:** hard-block — see below` in the body. Cost: 3 lines of boilerplate per file. Benefit: both machine audit AND human DX.

Rejected : filename convention (B) — breaks when rules evolve in status, and "hardblock-yagni.md" is semantically misleading when YAGNI gets retrograded to advisory.

---

## D2 — Conventional commit hook

| Agent | Position |
|---|---|
| A Puriste | **`conventional-pre-commit`** (Python) — stack unity |
| B Pragmatique | **Custom `scripts/check_commit_message.py`** — zero dep |
| C End-user | **`conventional-pre-commit`** (Python) — clone + `uv sync` = works |

### Convergence : A + C → `conventional-pre-commit`

### Strong arguments (both agents)

- **Stack unity** — metadev-protocol is Python-pure (uv, ruff, copier). Adding Node for one hook is a toolchain split that contradicts the "zero setup overhead" pitch (C1).
- **Precedent** — scripts like `check_meta_naming.py`, `check_git_author.py` already set the "pure Python custom check" pattern, and they work. `conventional-pre-commit` follows the same pattern without reinventing.
- **DX wall for new user** — "runs `pre-commit install`, tries to commit, gets cryptic npm error" (C1).

### Against custom script (B)

- Maintenance burden on us for a standard problem already solved.
- No upstream for bug reports.
- Regex ambiguity on edge cases (trailers, multi-line messages, merges) already handled by the library.

### Orchestrator synthesis

Clear winner: **`conventional-pre-commit`**. Pragmatique's "custom script" argument underestimates the hidden cost of maintaining a parser for a spec that evolves (Conventional Commits v1.0.0 has edge cases custom regexes miss).

---

## D3 — PR batching

| Agent | Position |
|---|---|
| A Puriste | **Strict sequential** 1→2→3→4 |
| B Pragmatique | **PR-1+PR-2 merged**, then 3 and 4 |
| C End-user | **Strict sequential** |

### Convergence : A + C → Strict sequential

### Strong arguments

- **Puriste A1** — "If PR-2 lands and you discover a flaw in the hook enforcement format (D1), you can revert PR-1 alone without unwinding three other features." Decisive.
- **End-user C2** — Repo's own rule (R015: "1 commit = 1 logical unit, bisectable") applies to PRs. Violating it undermines the discipline the template models.
- **Pragmatique B1** weakness — "Serial batching kills the ship window" assumes multi-person review queue. This is solo dev: the bottleneck is the author, not the reviewer.

### Irreducible tension

Pragmatique's valid concern: **PR-1 (strictness ruff) without PR-2 (rules doc) leaves the LLM blind to the new strictness config** — gap between fix and doc-of-the-fix, exactly the same problem the audit diagnosed.

### Orchestrator synthesis

**Recommendation: strict sequential BUT with a twist** — PR-1 must include a minimal doc-snippet in its commit message or PR description pointing to the upcoming PR-2 (the real rule file). This way bisectability is preserved AND the LLM doesn't regress between merges (because PR-2 follows within hours, not days).

If PR-1 and PR-2 can't be produced within the same session, PR-1 includes a stub `template/.claude/rules/linting.md` with just the minimal config doc — then PR-2 expands it with all G1-G5 rules.

---

## D4 — Multi-host rule conditionality

| Agent | Position |
|---|---|
| A Puriste | **Always generated + prose marker** |
| B Pragmatique | **Always generated + prose marker** |
| C End-user | **Always generated + prose marker** |

### Triple convergence

### Strong arguments (consensus)

- **Invisibility of conditional (Jinja) is a silent failure mode** (A1, B1, C1) — "A user who generates a single-host project has no idea rule G3 exists. Six months later they add a second machine and have no rule, no hook, no documentation."
- **Rules files cost kilobytes** — "The cost of an extra rule document is near-zero. The cost of hidden rules is infinite" (A1).
- **grep-ability** — a rule behind `{% if %}` is invisible to static inspection (A).

### Rejected

- Jinja conditional (option A in the initial question set) loses.
- Paragraph in `branching.md` (option C) also loses — "discovery by accident" (C2).

### Orchestrator synthesis

**Unanimous: always generate the rule, marked "applicable only in multi-host mode" in prose and frontmatter.** Zero debate left.

---

## Lone wolf insights (end-user angle that survived)

- **"Frontmatter is invisible until you know to look for it"** — resolved via hybrid (frontmatter + blockquote in body).
- **"runs pre-commit install, gets cryptic npm error"** — decisive for D2.
- **"discovery by accident"** — decisive for D4.

The wolf brought the crucial DX reality check that insiders underweighted.

---

## Convergence points (all agents agree)

- Stack unity (Python-only) matters for this project.
- Silent failure modes (Jinja conditionals, missing frontmatter) are worse than visible redundancy.
- Bisectability is non-negotiable.

## Irreducible tensions

- **D3 (sequential vs batching)** : real risk of LLM-blindness between PR-1 merge and PR-2 merge. Mitigated by the "PR-1 ships with a stub doc" twist, not fully eliminated.

---

## Final recommendation

| Decision | Winning option | Confidence |
|---|---|---|
| **D1** | **Hybrid** : YAML frontmatter + first-line blockquote header in body | Medium-high |
| **D2** | **`conventional-pre-commit`** (Python) | High |
| **D3** | **Strict sequential**, with PR-1 shipping a minimal doc stub | High |
| **D4** | **Always generate + prose marker** ("applies only if multi-host") | Very high |

## Decision

**USER DECISION NEEDED**

To decide, consider:
- D1 : accept the 3-line-per-rule frontmatter+blockquote cost ? Yes/no.
- D3 : are PR-1 and PR-2 produced in the same session (so the "LLM blind gap" is <1h) ? If no, PR-1 must ship the stub doc.
- Any other decision to revisit ?
