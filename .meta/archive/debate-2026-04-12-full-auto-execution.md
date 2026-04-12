---
type: debate
date: 2026-04-12
slug: full-auto-execution
status: active
---

# Debate Record — Full-auto plan execution mode

**Date:** 2026-04-12
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (The End-User)
**Status:** USER DECISION NEEDED

---

## Subject

Once the user has validated a plan, the LLM should execute it end-to-end without re-asking approval on each individual action — but without undermining the explicit-approval-before-implementation rule that protects against runaway autonomy. Which mechanism best preserves **trust + velocity + discoverability + reversibility**?

Three candidates were debated:
- **A — Prose convention** in `CLAUDE.md` ("approve plan = approve all actions inside it"), zero config
- **B — Config flag** `execution_mode: safe | full-auto` in `.claude/settings.json`, copier-tunable, à la `meta_visibility`
- **C — Unexplored third option** (discovered during debate)

## Angles

- **A (Le Puriste):** prose is self-documenting, lives at point of use, respects YAGNI, keeps judgment inside reasoning rather than reifying it into a toggle [insider]
- **B (Le Pragmatique):** config is auditable via git diff, propagates through copier, consistent with `meta_visibility` precedent, creates explicit recorded choice at project inception [insider]
- **C (The End-User):** both A and B frame the problem wrong — the real failure is situational awareness loss during execution, not permission location [lone wolf]

## Strong arguments (survived cross-critique)

- **Situational awareness is the actual failure mode** — raised by C, conceded by both A and B. The user approves a plan in state X; by step 7 the state has drifted to Y and the original approval no longer fits. Neither prose (read at session start, not re-invoked at step 7) nor a flag (read once at startup) addresses this.
- **Config flag is YAGNI without evidence of two distinct user profiles** — raised by A and C, conceded by B. Nobody has stated a concrete scenario where a user specifically wants `safe` mode. `meta_visibility` is a *structural* fact (public/private repo, infrastructure), not a *workflow governance* decision — the precedent is a consistency trap.
- **Execution receipts restore in-flight awareness** — raised by C, conceded by both insiders. The AI narrates each step as it runs ("Step 2/5 done: created src/vault/models.py"), each receipt includes a visible halt ("type STOP to pause"). Works for every user regardless of profile.
- **Prose edits lack a durable audit trail** — raised by B, conceded by A. Prose in CLAUDE.md gets rewritten silently; a settings.json change is a git-diffable decision event with timestamp, author, message.
- **Copier propagation is a genuine value** — raised by B, not rebutted by C. Prose conventions drift per-project; copier params propagate to every generated project from day 1 and `copier update` surfaces changes.

## Lone wolf insights

- **The debate between A and B is a debate about which file to put a rule in — not a debate about whether the execution experience is actually safe.** The wolf's most surgical critique. Both insiders were optimizing a permission-location question while the real harm surface (in-flight drift) sat untouched.
- **"People don't consult legal documents mid-action."** A CLAUDE.md rule read at session start is not present to the user at step 7 of a 15-step plan. Attention does not distribute uniformly across a session; long-context instruction following is known to degrade. Prose is a pre-flight mechanism, not an in-flight one.
- **`copier copy --defaults` is how most users bootstrap.** B's "explicit recorded choice at inception" assumes a careful adopter. Statistical users inherit defaults and never remember setting them — so the flag is often not a choice the user actually made.
- **Receipts solve awareness but under-specify control.** If the default is "keep going unless halted," then full-auto mode is effectively safe mode with narration. The wolf's own proposal required sharpening here.

## Contested arguments (no consensus)

- **Does auditability belong in config, in session logs, or in prose?**
  - **B says:** settings.json — structural, diff-reviewable, inherited by copier
  - **A says:** prose keeps accountability inside judgment; auditability is nice-to-have, not load-bearing
  - **C says:** append receipts to `.meta/active/session-YYYY-MM-DD.md` — gives receipts a git-diffable footprint without inventing new infrastructure, fits existing taxonomy
  - **Why it matters:** determines where the paper trail for "what was approved vs what was executed" actually lives, and whether new file machinery is needed.

- **Does a config flag make sense as a future option, or is it a category error?**
  - **B (updated):** justified only if a concrete full-auto user profile emerges after receipts ship
  - **A:** category error — permission rules are runtime decisions, not structural facts; settings.json is for structural facts (like `meta_visibility`)
  - **Why it matters:** determines whether the roadmap leaves a door open for `execution_mode` or closes it on principle.

## Dismissed arguments (refuted or irrelevant)

- **"Consistency with `meta_visibility` precedent" (B argument 4)** — refuted by A and C as a false analogy. `meta_visibility` is structural infrastructure (repo accessibility); execution mode is workflow governance. "We have flags, therefore add a flag" inverts the reasoning.
- **"Flag creates deniability" (A argument 4)** — partially refuted by B: any written policy creates deniability by that logic; the counter is git history, which is ironclad for flags but weaker for prose. A retained the argument but B neutralized it against flags specifically.
- **"Receipts fully replace permission architecture" (C Phase 1)** — conceded away by C in Phase 2. Receipts are orthogonal, not substitute. They solve in-flight awareness; they do not answer "does plan approval grant blanket execution authority."

## Convergence points

All three agents converged on the following:

1. **Execution receipts with inline halt points are load-bearing.** Neither prose nor config addresses the in-flight drift problem. Receipts do.
2. **A settings.json `execution_mode` flag is YAGNI at this stage.** No concrete user has requested it. The `meta_visibility` precedent does not carry.
3. **Prose + receipts is sufficient for v1.0.0.** The existing workflow-gate rule in CLAUDE.md, combined with narrated step-by-step execution, covers both pre-flight intent and in-flight awareness.
4. **Receipts should have a durable footprint.** Ephemeral output is vulnerable to the deniability critique; session-log persistence closes the gap.

## Irreducible tensions

- **Portfolio-scale inheritance vs. single-project simplicity.** B's copier-propagation argument is not actually refuted — it points to a real capability gap (execution posture does not inherit across generated projects if it lives only in prose + receipts). The group conceded this gap exists but judged it premature to solve. If metadev-protocol sees real adoption and users start reporting "I want to set full-auto as my default across all my projects," the flag argument reactivates.

- **Accountability-through-judgment vs. accountability-through-structure.** A wants approval to feel like active responsibility; B wants it to leave a structural artifact. These are different theories of what accountability *is*. Receipts-in-session-log partially bridges them, but the philosophical tension remains.

## Recommendation

**Ship prose + execution receipts for v1.0.0. Defer the config flag.**

Concretely:
1. **Keep the existing workflow-gate prose in CLAUDE.md** — the rule "approve plan = approve the actions inside it" remains the semantic anchor. No new flag.
2. **Add an execution-receipt primitive** to the plan-execution skill (or document it as a convention in `/ship` / plan-execution flow): the LLM narrates each step as it completes, format "Step N/M done: <what changed>", and every receipt includes a visible halt affordance.
3. **Persist receipts to the session log** (`.meta/active/session-YYYY-MM-DD.md` or equivalent) so there is a git-diffable paper trail of what was executed vs. what was approved. This closes A's deniability critique and gives B an auditability artifact without adding a settings key.
4. **Do NOT ship an `execution_mode` flag.** Revisit only if a concrete user profile emerges post-launch requesting safe-mode-by-default across a portfolio of generated projects.

**Confidence: high.** Convergence was genuine — both insiders updated their theses toward the wolf's framing, and the wolf absorbed real gaps from the insiders (deniability, propagation) into a sharper proposal rather than holding the line.

## Decision

**USER DECISION NEEDED**

To decide, consider:

- **Is the execution-receipt primitive cheap to implement before v1.0.0 merge?** If it requires significant plan-skill rework, it may need to be deferred to v1.0.1 polish — in which case the prose rule stands alone for launch, with receipts as the first post-merge enhancement.
- **Where should receipts persist?** Session log is the recommendation, but the project currently has no enforced `session-*.md` file in `.meta/active/` — this may need a small taxonomy addition.
- **Do you want the config-flag door left open in the roadmap, or closed on principle?** Leaving it open means the recommendation reads "deferred"; closing it means "rejected on category grounds."
