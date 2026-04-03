# DECISIONS.md — Decision journal

> All structural decisions, including rejected alternatives.
> Format: date — decision — context — alternatives rejected
>
> ADRs being refined are in `.meta/decisions/` before landing here.

---

## 2026-04-01 — Project name: `metadev-protocol`

**Decision:** Repo name `metadev-protocol`, concept named "The Meta Protocol".

**Context:** Tension between `pilot-protocol`, `meta-protocol`, `metadev-protocol`.
"Meta" alone risked confusion with Meta (Facebook) in Google searches.
"Pilot" was too specific to the `.meta/PILOT.md` pattern.

**Rejected:** `pilot-protocol` (too narrow), `meta-protocol` (name collision risk).

---

## 2026-04-01 — `copier` over orphan branches

**Decision:** Template system via `copier` + `copier.yml`.

**Context:** First idea explored with Gemini = orphan Git branches
(`template/quant`, `template/app`). Abandoned during conversation.

**Why orphan branches were rejected:**
- Every improvement to a common hook = cherry-pick on N branches
- `git archive` for extraction is fragile and non-standard
- No mechanism to update already-generated projects

**Decisive advantage of `copier`:** `copier update` propagates template
evolution to existing projects — critical for long-term maintainability.

---

## 2026-04-01 — `pre-commit` over `lefthook`

**Decision:** `pre-commit` (Python ecosystem) for git hooks.

**Context:** Gemini suggested `lefthook` (Go binary). Both do the job.

**Rejected:** `lefthook` — adds a non-Python binary dependency in a Python-only stack.
`pre-commit` installs via uv, consistent with the rest of the stack.

---

## 2026-04-01 — `.meta/scratch/` gitignored, rest of `.meta/` versioned

**Decision:** Selective gitignore on `.meta/`.

**Context:** Tension between "keeping session memory" and "not polluting git history".

**Solution:** Separate ephemeral drafts (`scratch/`) from valuable artifacts
(`PILOT.md`, `sessions/`, `decisions/`). Versioned `PILOT.md` = recoverable context
after `git clone` or machine change.

---

## 2026-04-01 — 4 `copier.yml` profiles (not 3, not 10)

**Decision:** `minimal`, `app`, `data`, `quant`.

**Context:** Discussion on profile granularity. Risk of over-specifying
(one profile per framework) vs under-specifying (everything in minimal).

**Guideline adopted:** One profile = one category of relevant guardrails.
Internal technical differences within a profile (FastAPI vs Django) are managed
in the project's `CLAUDE.md`, not in the template.

---

## 2026-04-02 — CLAUDE.md as law, GUIDELINES.md as mentor

**Decision:** Split project instructions into two files with distinct authority levels.

**Context:** Tension between directive (LLM follows exactly) and advisory (LLM adapts).
Resolved by separation: CLAUDE.md is non-negotiable, GUIDELINES.md is advisory.

**Why not one file:** Too many rules in CLAUDE.md and the LLM ignores them.
Too few and important practices get lost. Two files with different authority
levels give the right balance.

---

## 2026-04-02 — 8 automatisms hard-wired in CLAUDE.md

**Decision:** The LLM applies these behaviors without being asked.

**Context:** The core value of the template is that the LLM manages context
automatically (reads PILOT.md, proposes plans, updates SESSION-CONTEXT.md).
Without hard-wired automatisms, the user must remind the LLM every session.

**Key automatisms:** session start context loading, first-session intro,
plan-before-code, milestone updates, end-of-session context rewrite,
conventional commits, architecture sync, rules + guidelines application.

---

## 2026-04-02 — Skills T1: brainstorm, plan, ship, lint, test

**Decision:** Ship 5 skills with every generated project.

**Context:** Based on Superpowers methodology (130K stars) and gold file research.
Skills are the right layer for workflow — loaded on demand, shared via git.

**Why these 5:** They cover the full session lifecycle (explore → plan → implement → verify → ship).
T2 skills (/spec, /tdd, /review, /debug) deferred to post-MVP.
