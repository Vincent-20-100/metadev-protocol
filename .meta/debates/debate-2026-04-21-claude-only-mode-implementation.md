# Debate Record — Claude-only mode: implementation strategy

**Date:** 2026-04-21
**Preset:** architecture
**Mode:** standard (no deep loop — 2/3 converged)
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user DX persona)
**Status:** USER DECISION NEEDED

---

## Subject

`metadev-protocol` v2.0.0 shipped multi-LLM support (AGENTS.md / GEMINI.md / sync-config.yaml / scripts/sync_hosts.py / hook H008 / CI workflow) **unconditionally**. Every generated project inherits it. Vincent (solo dev, Claude Code exclusively) declared a Claude-only mode **non-negotiable**. Debate scope: *how* to implement it, not whether. Four options on the table:

- **A** — 2 bools per host (`enable_codex`, `enable_gemini`), default `false`.
- **B** — 1 bool `enable_multi_host`, default `false`.
- **C** — Inversion: Claude-only is the real template, multi-host is an add-on (sub-template / overlay / post-gen script).
- **D** — Keep v2.0.0, add `disable_multi_host` negative flag default `false` (retrocompat perfect).

## Angles

- **A (Puriste):** doctrinal coherence, YAGNI strict, reversibility of template decisions [insider]
- **B (Pragmatique):** minimize migration friction for egovault / T7 / Cert; ship today [insider]
- **C (End-user DX):** solo dev generating a new project — absent > disabled, no onboarding tax [lone wolf]

## Phase 1 preferences
- A → **Option C**
- B → **Option B**
- C (wolf) → **Option C**

## Phase 2 updates
- A → Option C holds; concedes B's tag-immutability is real. Requires explicit v3.0.0 governance if multi-host ever becomes mandatory.
- B → Option B + documented cleanup path; concedes onboarding friction is real; rejects Option C on "two sources of truth / testing matrix explodes".
- C (wolf) → Option C holds, BUT concedes B's #3 on the *delivery mechanism*: if Option C requires a two-step onboarding (copier copy + post-gen script), B wins on pragmatic grounds. Option C must be a **single copier invocation** to survive.

---

## Strong arguments (survived cross-critique)

- **Rule D4 was misapplied in v2.0.0 (A).** D4 says the *rule file* `multi-host.md` ships unconditionally (to stay visible on upgrade), NOT that the entire feature ships unconditionally. B and C did not contest this category distinction. Clean win for A.
- **Absent file > disabled file at onboarding (C).** A generated project with zero multi-host artifacts raises zero questions. Even a `disable_multi_host: false` entry in copier.yml forces the user to ask "what is this?" B conceded this is real DX friction.
- **v2.0.0 tag is immutable + cuts both ways (all 3).** No option can alter what v2.0.0 projects already inherited. The question is forward: v2.x.0+ default.
- **"3 projects blocked today" is a deployment urgency argument, not a design argument (C contesting B).** Designing the template's permanent default state based on 3 legacy projects is an inversion — the default should serve the 100th user, migration is handled separately.
- **Speculative extensibility is YAGNI-forbidden (A, C).** Betting the default on a hypothetical 3rd host (Option A's per-host granularity) is premature.

## Lone wolf insights (survived cross-critique + relevance check)

- **The template lies about what it is.** Claude-first pitch + Codex/Gemini stubs = semantic incoherence. Insiders missed this because they built the stubs intentionally; to a new user, they look like commitments. **Relevant — it's the core friction.**
- **Bool prompts at `copier copy` transfer architectural complexity to the user at worst moment.** At init, the user knows project name + Python version. They don't know what "multi-host agent coordination" means and shouldn't need to. **Relevant — implies Option C's delivery must NOT show a prompt for a feature the user hasn't asked about.**
- **Framework creator bias.** Shipping "all-inclusive" reflects the creator's mental model, not the user's. **Relevant — applies directly to Vincent's original v2.0.0 decision; admitting this is part of fixing it.**

## Contested arguments (no consensus)

- **Two sources of truth on upgrade (B vs A+C).**
  - *For B:* copier can't track "was the add-on ever applied?" → hybrid state on `copier update` → testing matrix explodes.
  - *Against (C):* only true IF delivery is two-step. If Option C is a single copier flag that includes an overlay directory, there's ONE source of truth (the copier run) with a clean branch (overlay applied or not).
  - *Why it matters:* this is the entire technical feasibility of Option C. If the overlay/sub-template pattern works cleanly in copier, C wins. If it doesn't, B wins by default.

- **Mid-project adoption friction (B vs C).**
  - *For B:* user who wants multi-host at month 6 just flips the bool, reruns template, done.
  - *Against (C):* copier overlays triggered by a flag work the same way — flip flag, rerun, overlay applied.
  - *Why it matters:* depends on copier ergonomics for overlays vs conditional exclusion. Empirical question, answerable in ~30 min by reading copier docs.

## Dismissed arguments

- **Option D (negative flag).** Refuted by B: creates silent state-vs-contract mismatch on `copier update` (files linger, flag says "no"). Neither A nor C defended D. **Out.**
- **Option A (per-host bools).** Refuted by B: premature assumption that future hosts follow the stub pattern. Refuted by C: "extensibility" for unknown hosts is YAGNI theater. Only A (Puriste) had mild sympathy, but A explicitly chose C over A. **Out.**

## Convergence points

- Option D is out (silent regression, no defender).
- Option A is out (premature, no defender).
- The real debate is B vs C, and specifically: **can Option C be implemented as a single copier invocation (overlay pattern) rather than a two-step (post-gen script)?**
- If YES → C wins on all angles (doctrine + DX + pragmatism).
- If NO → B wins on pragmatism, and C conceded this explicitly in Phase 2.

## Irreducible tensions

- **Template as values-statement (A, C) vs template as toolkit (B).** Unresolved — it's a philosophy call. Puriste/DX view: the default state encodes what the template *endorses*; dormant optional machinery is a statement. Pragmatique view: a toolkit with disabled-by-default features is ergonomic, not endorsing.
- **Onboarding friction (C) vs mid-project adoption friction (B).** Unresolved as pure principle. Practically resolved IF overlay pattern works: neither suffers.

## Recommendation

**Option C, pending one feasibility check.**

2 of 3 agents converged on C from genuinely different angles (doctrinal purity + end-user DX). B's sole remaining objection is the "two sources of truth" concern — and B's own analysis depends on Option C being a *two-step* delivery. If Option C can be delivered as **a single `copier copy` invocation that conditionally includes an overlay directory**, B's objection dissolves.

The devil's advocate's empirical question ("in the last 6 months did you open AGENTS.md/GEMINI.md in egovault/T7/Cert?") also directly informs the migration risk: if the answer is zero, Option C's "removal on update" becomes a service, not a regression.

**Confidence: high** on Option C as direction. **Medium** on feasibility — depends on a 30-min copier docs check.

## Decision

**USER DECISION NEEDED.** Two questions to tip the balance:

1. **Empirical (from devil's advocate):** In the last 6 months, have you opened or edited AGENTS.md / GEMINI.md / sync-config.yaml in egovault, T7, or Certification Masterclass — other than to regenerate them?
   - If NO → migration risk on `copier update` is 0. Option C can ship with default `false` and no special migration handling.
   - If YES → Option B is safer (stable bool contract), OR Option C with explicit migration note in v2.2.0 tag message.

2. **Technical (30-min doc check before committing to C):** Does copier support an overlay / conditional sub-template pattern that can be triggered by a single flag at `copier copy` time, without requiring a post-generation script?
   - If YES → Option C (recommended).
   - If NO → Option B (C's feasibility fails, B's toolkit view wins by default).

### Rule D4 side-note

A's Phase 1 argument — that v2.0.0 misapplied D4 (shipping the *feature* unconditionally when D4 only mandates the *rule file* be unconditional) — was uncontested. Regardless of which option wins (B or C), this distinction should be recorded in ADR-012: **the rule `multi-host.md` ships in every project; the multi-host feature files do not**.

---

**Action after decision:**
- If Option C: update `.meta/scratch/plan.md` to reflect overlay delivery (not 2 bools), create ADR-012 capturing the D4 clarification.
- If Option B: keep plan simpler (1 bool), still create ADR-012 on D4 clarification.
