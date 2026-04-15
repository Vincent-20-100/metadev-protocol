# ADR-010 — Skills & agents architecture (v1.6.0)

**Date:** 2026-04-15
**Status:** ACCEPTED
**Supersedes:** ADR-006 (Skills T1 — workflow automation) — the v1.0 skill inventory

---

## Context

Between v1.0 and v1.5 the skill and agent surface grew organically:
- 10 skills in `template/.claude/skills/` but only 3 copied into meta's own `.claude/skills/`
- 4 "agents" referenced in the trigger table (`code-reviewer`, `test-engineer`,
  `security-auditor`, `data-analyst`) but no files backing them
- `/radar` and `/audit-repo` doing overlapping jobs (emerging-tech discovery vs
  structural analysis of one repo) with two scripts and two card schemas
- No mechanical check that the trigger table rows matched the filesystem

The audit at PM.15 surfaced three defects:
1. **Ghost agents** — trigger table lied about what existed
2. **Fake dogfooding** — meta advertised skills it wasn't actually using
3. **Overlapping surface** — `/radar` and `/audit-repo` competed for the same
   slash-palette slot with no enforceable boundary

---

## Decision

**1. Mechanical contract.** `scripts/check_skills_contract.py` runs in
pre-commit and asserts: every `| skill |` or `| agent |` row in both trigger
tables maps to a real file on disk. Default mode checks template-only;
`--strict` also asserts full meta ↔ template parity.

**2. Dual-maintenance dogfooding.** Every skill and agent in
`template/.claude/` must have an identical copy in meta `.claude/`. Meta is
no longer a subset — it's a mirror with one exception (meta may have a
stricter superset during transitions, guarded by `TestMetaParity`).

**3. Four local agents promoted from ghost to real:**
- `code-reviewer` — post-implementation review, tiered CRITICAL/WARN/NIT
- `test-engineer` — generative test author, not a runner
- `security-auditor` — OWASP sweep scoped to the diff
- `data-analyst` — audits statistical claims, pipelines, metrics

They are **additive** to the `superpowers` plugin, not fallbacks.

**4. `/radar` + `/audit-repo` fused into `/tech-watch`:**
- One skill, two modes (sweep / deep)
- Shared card schema under `.meta/references/research/`
- `scripts/tech_watch/` unified package with `sweep/` and `deep.py` submodules
- Dual-shipped (meta + template)

**5. `/test` and `/save-progress` thinned** under the skill-vs-tool principle:
deterministic work extracted to `scripts/save_progress_preflight.py`, skill
body reduced to invocation + narrative framing.

---

## Consequences

- **v1.6.0 invariants:** 10 skills + 5 agents, dual-maintained, mechanically
  checked, no ghost rows
- **Downstream impact:** external projects on v1.5.0 will see large diffs on
  `copier update` — migration notes in CHANGELOG cover the renames
- **Future-proofing:** adding a new skill or agent now requires adding the
  file in both trees AND the trigger-table row (the contract check fails
  otherwise), which eliminates the drift class that caused this audit
- **Name hygiene:** the slash palette no longer has ambiguous neighbors

## Rejected alternatives

- **Keep `/radar` and `/audit-repo` separate** — rejected because the
  "orthogonal depth axis" claim was contradicted by the fused card format
  and the single `/tech-watch` namespace in the palette
- **Delete the 4 agents entirely** — rejected because they represent real
  post-implementation workflows that devils-advocate (a decision challenger)
  does not cover
- **Ship agents template-only, not in meta** — rejected because meta is
  where the template gets dogfooded; asymmetric meta means the template
  never gets real use by its own author
