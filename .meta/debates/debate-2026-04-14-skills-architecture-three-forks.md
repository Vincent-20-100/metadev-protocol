# Debate Record — Skills architecture (3 linked forks)

**Date:** 2026-04-14
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user DX)
**Status:** RESOLVED 2026-04-14 — user chose a fourth way on Tension 1 (fusion), confirmed B+C on Tension 2

---

## Subject

Three linked architectural forks on the skills/agents system of metadev-protocol:

- **F1 — Ghost agents.** CLAUDE.md trigger table (meta + template) advertises 5 agents; only 1 is shipped. Ship 4 missing, delist, or lazy-reference through the `superpowers` plugin?
- **F2 — `/radar` vs `/audit-repo`.** Real orthogonality (discovery vs deep-dive) or naming collision? Should `/audit-repo` move from meta-only into the template?
- **F3 — Script colocation.** Today: `scripts/<name>/` + `.claude/skills/<name>/SKILL.md` split across two trees. Proposal: `.claude/skills/<name>/` hosts SKILL.md + Python files as one unit.

## Angles

- **A (Puriste):** correctness, patterns, convention [insider]
- **B (Pragmatique):** ship fast, iterate, YAGNI [insider]
- **C (End-user DX):** simplicity, discoverability, zero-surprise [lone wolf]

---

## Strong arguments (survived cross-critique)

1. **The trigger table IS the public API of the skills system** (A, adopted by B and C). CLAUDE.md is loaded at every session; advertising unimplemented tools violates the repo's own honesty constraint. A lying API corrupts every downstream decision. `copier copy . /tmp/test` currently produces a CLAUDE.md whose claims are false.

2. **Option (c) lazy-reference is the worst of all options** (C, hardened by A, B retracted initial hedge). It moves the lie into a dependency chain that cannot be tested at template-generation time. The user now has to trust *two* repos instead of one, and failure modes branch ("plugin missing", "plugin version mismatch", "plugin abandoned").

3. **A ~20-line `scripts/check_skills_contract.py` at pre-commit converts the honesty rule from discipline into invariant** (A4, universally adopted). Asserts that every trigger-table row maps to an actual file under `.claude/skills/` or `.claude/agents/`. This is the cheapest durable fix — it prevents the next ghost from shipping at all. It also aligns with the repo's own skill-vs-tool principle (max deterministic, min LLM).

4. **Cold-start rule as guiding principle** (C4, adopted by A and B): *"Nothing ships in `template/` that a first-time user cannot invoke, find, or verify without asking the author."* Dissolves the three forks into one rule. Becomes the invariant that the contract script enforces.

5. **Naming collision at the slash palette is real regardless of architectural orthogonality** (C, conceded by A and B). Insider "discovery vs deep-dive" is invisible when the user is typing `/` in the palette. `/radar` and `/audit-repo` reading as overlapping is a pure DX bug at the point of use. Rename required.

6. **Colocation is theoretically right but its migration cost is real today** (A conceded to B). `copier update` breakage on every downstream project is a concrete tax. A pre-commit contract check delivers the "no ghosts" invariant without forcing the layout change.

---

## Lone wolf insights (survived cross-critique)

- **"200-with-garbage is worse than 404"** (C1). A missing slash command produces a visible error; a ghost agent hallucinated by the LLM produces confident garbage that destroys trust more violently than an error ever could. This sharpened the F1 framing from "delist" to "delete now, re-add only in the same commit that implements the agent".

- **"Asymmetric availability is a betrayal pattern"** (C2). `/audit-repo` existing in meta but not in template teaches users "the author kept the good stuff for themselves". A recursive template ("what you build here becomes the standard") demands symmetry. This is the strongest argument for shipping `/audit-repo` in template.

- **"Directory structure IS the architecture diagram"** (C3). A's colocation argument was structural; C restated it as the cheapest form of documentation — `ls .claude/skills/radar/` answering "everything `/radar` is" costs zero maintenance.

- **"Author-POV drift is the root disease"** (C4). All three forks are symptoms: F1 = author imagined full system and wrote docs for that; F2 = author built a tool they need and forgot to ship it; F3 = author picked Python convention from a pre-skill world. The cure is a single rule that forces author-test on every template artifact.

---

## Convergence points (ship these — no user decision needed)

### Convergence 1 — Delete ghost agents now
**All 3 agents agree.** Delete `code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst` rows from the trigger table in CLAUDE.md (meta) and `template/CLAUDE.md.jinja`. Keep `devil's-advocate`. Re-add any of the 4 only in the same commit that ships the corresponding agent file.

### Convergence 2 — Ship `scripts/check_skills_contract.py` at pre-commit
**All 3 agents agree.** ~20 lines of Python. Reads CLAUDE.md (both meta and template/CLAUDE.md.jinja), extracts the trigger table, asserts every skill/agent row maps to an existing directory. Fails pre-commit on drift. Hooked into `.pre-commit-config.yaml`.

### Convergence 3 — Rename `/radar` to kill the palette collision
**B + C converge on `/tech-watch`.** A proposed `/scan`. Both eliminate the `/radar` vs `/audit-repo` ambiguity at the palette level. `/tech-watch` is more descriptive of the function (passive, scheduled monitoring of tech sources) than `/scan` (which overloads a generic verb). **Recommendation: `/tech-watch`** — 2/3 votes, stronger name hygiene.

### Convergence 4 — Keep split layout for v1.5.0 / v1.6.0
**All 3 agents agree** after cross-critique. A softened from "colocate now" to "colocate progressively, one skill per release". B and C confirmed split stays. The contract check from Convergence 2 delivers the "no ghosts" invariant that colocation would have enforced structurally — colocation becomes optional cleanup, not a load-bearing fix.

---

## Contested points (user decision needed)

### Tension 1 — Ship `/audit-repo` in template or keep meta-only?

| Agent | Position | Core reason |
|---|---|---|
| A (Puriste, updated) | **Ship** in template for v1.5.0 even flawed | Recursive template demands symmetry; boundary is proven by function pair (breadth/depth) and invocation pair (auto/manual) |
| B (Pragmatique) | **Meta-only** until first user request | No generated-project user has asked; "obvious utility" without a single report is YAGNI violation; shipping it to satisfy symmetry puts something in `template/` that users *can* invoke but cannot *usefully* invoke (no repo-to-audit context) |
| C (DX wolf, updated) | **Defer** the ship decision; still rename `/radar` now | Agrees with A that asymmetric availability is a betrayal pattern, but agrees with B that shipping a tool without a job for generated-project users is worse; waits for first signal OR refactor landing |

**Why it matters:** this is the user's single most load-bearing value judgment. Cold-start rule (A+C) favors shipping; YAGNI (B+C) favors deferring. The two agree on the diagnosis (author-POV drift) but disagree on the cure.

**Key question to tip the balance:** *"Do you expect users of generated projects to audit external repos as part of their normal workflow, or is auditing an activity that happens upstream (at template curation time) only?"*

- If the answer is "yes, users will audit repos" → ship now (A wins).
- If the answer is "no, auditing is a meta-activity" → keep meta-only (B wins).
- If the answer is "I don't know" → defer with rename (C wins).

### Tension 2 — Superpowers pointer in the trigger table, or only in GUIDELINES?

| Agent | Position |
|---|---|
| A (Puriste) | Trigger table = 100% invocable, no exceptions. Mention superpowers only in GUIDELINES or a separate "Recommended plugin" section |
| B (Pragmatique) | One-line pointer in the trigger table is acceptable if clearly marked as optional upstream |
| C (DX wolf) | One-line pointer is strictly better than deleting (preserves discoverability) as long as the line does not lie about availability |

**Why it matters:** this is a minor tension but it sets the precedent for how the trigger table handles external dependencies. If we allow one conditional entry, we'll allow others. A's rule is cleaner; B+C's is more discoverable.

**Key question:** *"Is it OK for CLAUDE.md to mention capabilities users can opt into, or must CLAUDE.md describe only what exists out-of-the-box after `copier copy`?"*

---

## Dismissed arguments (refuted by cross-critique)

- **B's original "one-line superpowers mention as optional upstream"** — retracted by B after A showed the conditional-contract problem.
- **A's original "merge with `--mode=audit|watch` flag"** — retracted by A, contested by C as invisible at the palette level (table-scannability beats flag parsimony for beginners).
- **A's original "colocate now"** — conceded the `copier update` breakage cost; deferred to progressive migration.
- **C's original "ship `/audit-repo` in generated projects for symmetry"** — partially contested by B showing cold-start users have no audit-target in their empty generated project. C softened to "defer pending signal or refactor".
- **B's original "defer all three forks until user signal arrives"** — contested by A+C because ghost agents actively corrupt the signal (users will report "Claude is broken" instead of "your CLAUDE.md lies"). F1 cannot wait.

---

## Irreducible tension

**Cold-start rule vs YAGNI, specifically on F2b (ship audit-repo).**

Both are legitimate values. Cold-start rule says "every template artifact must pass the first-user test"; YAGNI says "never build what no user has asked for". They agree on F1 (delete ghosts) because the cold-start test and YAGNI both condemn ghosts. They disagree on F2b because shipping `/audit-repo` satisfies cold-start but violates YAGNI (no demand signal).

No amount of cross-critique resolves this — it's a value judgment about which rule is load-bearing for THIS project at THIS stage. The user must pick.

---

## Recommendation (orchestrator synthesis)

**Confidence: high on convergence points, medium on Tension 1, low on Tension 2.**

### Execute the 4 convergence points immediately, in one commit:

1. Delete 4 ghost agents from both trigger tables
2. Ship `scripts/check_skills_contract.py` + pre-commit hook
3. Rename `/radar` → `/tech-watch` in SKILL.md, scripts, trigger tables, docs, tests
4. Keep split layout; add a `scope:` front-matter field to each SKILL.md (`scope: automated-discovery` vs `scope: manual-deep-dive` vs `scope: internal-workflow` etc.) that the contract script checks for collision

This is 1 commit, ~2 hours of work, covers the F1 + F3 + F2a decisions, and ships the mechanical enforcement that prevents recurrence.

### For Tension 1, orchestrator leans toward C (defer) for these reasons:

- It is the option most consistent with the cold-start rule **and** YAGNI (ship nothing that could backfire either way).
- The memory backlog already flags `/audit-repo` for "refactor complet" — moving a thing you're about to rewrite is genuinely wasted motion (B2's strongest point).
- The rename alone resolves the palette collision that the cold-start rule was complaining about (C conceded this).
- Shipping can happen with the refactor, not before — that's ONE commit instead of two (ship-then-rewrite).

But this is the user's call and the framing matters: if you have internal conviction that generated-project users will audit external repos, A's case is strong. If you don't, C's case is strongest.

### For Tension 2, orchestrator leans toward B+C (one-line pointer):

- A's "100% invocable" rule is purist but loses real discoverability value for `superpowers`, which is a first-class ecosystem the repo already depends on.
- The cost of one labeled line ("*If the `superpowers` plugin is installed, it provides code-reviewer, security-auditor, and test-engineer.*") is minimal and the clarity gain is concrete.
- The contract script from Convergence 2 can be extended to recognize "optional:plugin" markers so the invariant still holds.

---

## Decision

**USER DECISION NEEDED on:**

1. **Tension 1 — ship `/audit-repo` in template?** Answer A/B/C:
   - (A) Ship now, even flawed, for symmetry
   - (B) Keep meta-only permanently until a real user request
   - (C) Defer with rename now, ship when the refactor lands or a user asks

2. **Tension 2 — pointer to `superpowers` in the trigger table or only in GUIDELINES?** Answer A/B:
   - (A) Only in GUIDELINES (trigger table = 100% invocable)
   - (B) One labeled line in trigger table (discoverability gain)

**Orchestrator leans:** Tension 1 → **C (defer)**. Tension 2 → **B (one labeled line)**.

---

## User decision (2026-04-14)

### Tension 1 — Fourth way: **fusion** (not present in the debate)

The user rejected options A/B/C and proposed a fourth option none of the three
agents surfaced: **merge `/audit-repo` into `/tech-watch`** as a unified skill
that adapts to any depth of technical review and emits a structured note with
the same schema in both modes.

**Unified contract:**
- `/tech-watch` (no args / `--sweep`) → passive multi-source discovery (current `/radar` behavior), produces shallow cards
- `/tech-watch <url>` → active deep-dive on a specific GitHub URL (current `/audit-repo` behavior), produces a deep card
- Both modes write to the same directory (`.meta/references/research/`) with the same card schema at different depths
- The skill ships in **both meta and template** — the asymmetric-availability question dissolves because there is nothing to ship asymmetrically

**Why this beats A/B/C:**
- Kills the palette collision structurally (one skill name)
- Kills the asymmetric-availability betrayal (one codebase, both projects)
- Kills the orthogonality debate (fusion IS the proof of non-orthogonality — the depth axis is a continuous parameter, not two discrete tools)
- Kills the "move-then-rewrite" waste (the refactor and the ship happen in one motion)
- Single artifact to dogfood in the meta-repo

**New constraints this introduces:**
- The unified output schema must be defined up-front so both modes write compatible cards
- The Python package (`scripts/tech_watch/`) must absorb the current `scripts/audit_repo/` logic cleanly
- The rename `/radar` → `/tech-watch` becomes a rename + merge, not just a rename

### Tension 2 — User chose B (one labeled line in the trigger table)

Rationale: *"on avait choisi de recopier certains skills en fallback pour faire
tourner la template sans superpowers, mais superpowers est largement recommandé
et ses skills supplémentaires sont un gros atout sans pour autant mériter d'en
faire des fallbacks pour eux aussi."*

Concretely: the trigger table includes a labeled row pointing at `superpowers`
as the upstream provider of `code-reviewer`, `security-auditor`, `test-engineer`,
`data-analyst`, without shipping fallbacks for any of them. The line is clearly
marked as an optional-plugin reference; the contract check script recognizes
an `optional:plugin=<name>` marker so the invariant "every row maps to a real
artifact" still holds (the row maps to "installed plugin" rather than "local file").

### Next step

Proceed to `/spec` on the target architecture (including the fusion contract),
then `/plan` with exhaustive file list and commit decomposition.
