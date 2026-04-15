# Skills & Agents Architecture — Audit 2026-04-14

**Status:** Phase 1 (read-only diagnostic). No changes made.
**Scope:** every skill, agent, rule, hook in meta and template, plus all docs that reference them.
**Why:** v1.5.0 shipped PM.11/PM.12 only on template side. Discovered the meta-repo has stale duplicates and the promised skill/agent landscape diverges from reality.

---

## 1. Exhaustive inventory

### 1.1 Skills

| Skill | Meta `.claude/skills/` | Template `template/.claude/skills/` | Status |
|---|---|---|---|
| brainstorm | ❌ | ✅ | Template-only (meta relies on same file?) |
| debate | ❌ | ✅ | Template-only |
| orchestrate | ❌ | ✅ | Template-only |
| plan | ❌ | ✅ | Template-only |
| radar | ❌ | ✅ | Template-only (script in `template/scripts/radar/`) |
| research | ✅ **STALE** (156 LOC, inline schema) | ✅ NEW (74 LOC, extracted schema) | **DIVERGENCE — meta is v1.4.0 era, template is v1.5.0** |
| save-progress | ❌ | ✅ | Template-only |
| spec | ❌ | ✅ | Template-only |
| test | ❌ | ✅ | Template-only |
| vision | ✅ | ✅ | Duplicate (identical — to verify at refactor) |
| audit-repo | ✅ (60 LOC, refactored v1.5.0) | ❌ | **Meta-only by design** — script at `scripts/audit_repo/` |

**Total:** 10 template skills + 1 meta-exclusive (`audit-repo`). **3 meta-local copies** (audit-repo intentional, research stale, vision redundant).

### 1.2 Agents

| Agent | Meta `.claude/agents/` | Template `template/.claude/agents/` | Promised in CLAUDE.md trigger table |
|---|---|---|---|
| devil's-advocate | ❌ | ✅ `devils-advocate.md` | Both meta + template ✓ |
| code-reviewer | ❌ | ❌ | Meta CLAUDE.md + template CLAUDE.md.jinja ❌ **GHOST** |
| security-auditor | ❌ | ❌ | Meta + template ❌ **GHOST** |
| test-engineer | ❌ | ❌ | Template only ❌ **GHOST** |
| data-analyst | ❌ | ❌ | Template only ❌ **GHOST** |

**Critical finding:** the trigger table in both meta and template CLAUDE.md promises 3–5 agents, but only 1 is shipped. Every generated project inherits this broken contract.

### 1.3 Rules

| Rule file | Meta `.claude/rules/` | Template `template/.claude/rules/` |
|---|---|---|
| code-style.md | ❌ | ✅ |
| testing.md | ❌ | ✅ |

**Meta has no `.claude/rules/` directory at all.** The CLAUDE.md claim "This repo uses the same skills and agents as generated projects" is untrue for rules.

### 1.4 Hooks

Scripts used as pre-commit hooks:
- `scripts/audit_public_safety.py` — secret + gitignore scan (both meta and template via `.pre-commit-config.yaml` copied verbatim)
- `scripts/check_meta_naming.py` — filename taxonomy check (both)
- `scripts/check_git_author.py` — blocks Claude/Anthropic authorship (both)
- `.pre-commit-config.yaml` hook `prevent-claude-coauthor-trailers` (meta only? — to verify at refactor)

### 1.5 Scripts (deterministic companions)

| Script | Meta `scripts/` | Template `template/scripts/` | Companion skill |
|---|---|---|---|
| `audit_repo/` | ✅ new v1.5.0 | ❌ | `.claude/skills/audit-repo/` (meta) |
| `radar/` | ❌ | ✅ | `template/.claude/skills/radar/` |
| `tech_watch.py` | ✅ | ❌ | None — legacy, superseded by `/radar`? **To verify** |
| `audit_public_safety.py` | ✅ | ✅ | None (hook-only) |
| `check_git_author.py`, `check_meta_naming.py` | ✅ both | ✅ both | None (hook-only) |

---

## 2. Divergences and incoherencies

### 2.1 **Critical — meta research skill is stale**
`meta/.claude/skills/research/SKILL.md` = v1.4.0 era (inline schema, 156 lines).
`template/.claude/skills/research/SKILL.md` = v1.5.0 (74 lines + `output-schema.md` sibling).
Root cause: the v1.5.0 refactor (commit `8fa4b4e`) only touched the template side, leaving meta untouched. Meta has no `output-schema.md` companion — if someone invokes `/research` in the meta repo, the skill file is stale and a referenced companion is missing.

### 2.2 **Critical — 4 ghost agents in trigger tables**
Both `CLAUDE.md` (meta) and `template/CLAUDE.md.jinja` (template) list `code-reviewer`, `security-auditor` (+ `test-engineer`, `data-analyst` in template) in the Skills & Agents trigger table. **None of these agent files exist.** Every generated project ships with a table advertising tools that cannot be invoked.

### 2.3 **Structural — "meta dogfoods template" is a lie**
`CLAUDE.md` (meta) line: *"This repo uses the same skills and agents as generated projects (loaded from `template/.claude/skills/` via `projectSettings`)."*

Reality:
- No `settings.json` in `.claude/` — only `settings.local.json` (gitignored)
- No `projectSettings` mechanism in place
- Meta has its own local `.claude/skills/` with 3 directories (1 intentional, 2 duplicated or stale)
- Meta has no `.claude/agents/`, no `.claude/rules/`

When you work in the meta repo, Claude Code only sees what's in `.claude/`. The "dogfooding via pointer" is fiction.

### 2.4 **ARCHITECTURE.md ADR-006 is 4 versions stale**
ADR-006 claims 5 skills shipped: `/brainstorm`, `/plan`, `/ship`, `/lint`, `/test`.
Reality: **10** skills, `/ship` doesn't exist (→ `/save-progress`), `/lint` was retired (replaced by pre-commit ruff hook).

### 2.5 **PILOT.md "8+ skills" is a minor undercount**
Vision section says *"Should: 8+ skills"*. Actual: 10 in template, 1 in meta. Cosmetic but misleading.

### 2.6 **CHANGELOG, README, GUIDELINES — to audit at Phase 2**
Not yet verified: README skill listing, CHANGELOG entries for each skill addition, GUIDELINES skill-vs-tool examples. Likely stale in the same way.

### 2.7 **Missing meta `.meta/GUIDELINES.md`**
Template generates `.meta/GUIDELINES.md` in every project. The meta repo itself has no `.meta/GUIDELINES.md` — it relies on `.meta/PILOT.md` + `.meta/ARCHITECTURE.md` + `.meta/DECISIONS.md` only. Consistency issue with the dogfooding claim.

---

## 3. Scope crossings (who does what)

### 3.1 Clear orthogonality (keep as-is)
- `/brainstorm` (internal ideation) vs `/research` (external facts) vs `/audit-repo` (external repo deep dive) vs `/radar` (passive tech-watch) — four distinct axes, well-separated.
- `/spec` (formalization) vs `/plan` (decomposition) vs `/orchestrate` (multi-step execution) — three stages of the same pipeline, clearly ordered.
- `/debate` (decision-making with alternatives) vs `/brainstorm` (exploration without forced decision) — both conversational but `/debate` demands a winner.
- `/vision` (Vision section of PILOT) — unique entry point, no overlap.

### 3.2 Fuzzy boundaries (to clarify in Phase 2 spec)
- **`/save-progress` vs automatism #6** ("End of session — rewrite SESSION-CONTEXT.md"). Is `/save-progress` the user-invoked version of the automatism, or something else? The trigger table says "end of session OR user says 'stop', 'pause'" — same trigger as the automatism.
- **`/test` as skill vs pre-commit `pytest`** — what does `/test` do that `uv run pytest` does not? If it's just running pytest + framing output for the user, it's a 100% deterministic skill that should be thinned (memo backlog already flags it).
- **`audit-repo` meta-only** — is there a reason a generated project cannot audit external repos? If `/radar` surfaces a candidate in a generated project, the user would want `/audit-repo` there too. Current separation feels arbitrary.
- **`tech_watch.py` vs `/radar`** — `scripts/tech_watch.py` (~230 LOC, predates `/radar`) fetches trending GitHub repos. Is it superseded by `/radar`, complementary, or dead code? Both live in `scripts/` but only `/radar` is skilled.

### 3.3 Ghost agents (to decide in Phase 2 spec)
For each ghost agent (`code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst`):
- **Option A — ship them** (design real agent files, trigger tables become truthful)
- **Option B — delist them** (remove from trigger tables, fall back on user-invoked behavior or superpowers plugin)
- **Option C — lazy reference** (rewrite trigger table entries as *"if the `superpowers` plugin is installed, it provides code-reviewer; otherwise use the skill workflow"*)

`code-reviewer` in particular is referenced by the superpowers plugin — Option C is credible for it. The other 3 have no obvious upstream.

---

## 4. Doc staleness matrix (files requiring updates at Phase 3)

| File | Stale content | Severity |
|---|---|---|
| `.meta/ARCHITECTURE.md` | ADR-006 lists wrong skills | HIGH |
| `.meta/PILOT.md` | "8+ skills", no section on current skill/agent landscape | MEDIUM |
| `CLAUDE.md` (meta) | Trigger table has 2 ghost agents, false "dogfooding" claim | HIGH |
| `template/CLAUDE.md.jinja` | Trigger table has 4 ghost agents | HIGH |
| `template/.meta/GUIDELINES.md.jinja` | Skill-vs-tool section is good but doesn't cover the full inventory | LOW |
| `README.md` | Skill listing — **to verify** | MEDIUM |
| `CHANGELOG.md` | v1.5.0 entry — **to add** | HIGH |
| `.meta/decisions/` | No ADR documenting the current skill architecture (ADR-006 is stale) | MEDIUM |
| `.meta/GUIDELINES.md` | **Missing** — should be created to match template | LOW |
| `tests/test_template_generation.py` | `TestSkills.EXPECTED_SKILLS` — to verify matches template reality | MEDIUM |
| Trigger tables in skill SKILL.md files | Cross-references (`/brainstorm` ↔ `/spec` ↔ `/plan`) — to verify after any renaming | LOW |

---

## 5. Open questions for Phase 2 spec

1. **Dogfooding model** — do we (a) make meta truly load template skills via `projectSettings` (needs research on whether Claude Code supports this), (b) delete the meta `.claude/skills/` duplicates and document that meta-specific skills go in `.claude/skills/`, or (c) symlink at generation time? The current state is the worst of all worlds.

2. **Ghost agents** — ship them, delist them, or lazy-reference them (Option A/B/C above)?

3. **Meta-specific skills** — should `audit-repo` move into the template so generated projects can audit external repos too? Or is it truly meta-only (rationale: internal tool for curating inputs to metadev-protocol)?

4. **Legacy `tech_watch.py`** — retire it (it's superseded by `/radar`), keep it as a standalone utility, or fold into `/radar`?

5. **`/test` and `/save-progress`** — thin now (retroactive refactor) or defer to next-touch rule from memory?

6. **`.meta/GUIDELINES.md`** in meta-repo — create it, or document that meta does not need it (the rationale being that CLAUDE.md + ARCHITECTURE.md + DECISIONS.md cover the same ground for this specific repo)?

7. **ARCHITECTURE.md rewrite** — rewrite ADR-006 in place, or mark it "SUPERSEDED by ADR-NNN" and write a new one? Per `.meta/DECISIONS.md` convention — to verify.

8. **New skills from `emergent-patterns.md`** — the PM.14 synthesis produced 5 patterns. Pattern #4 in particular ("artefacts textuels adversariaux") suggests SKILL.md files should include a "rationalizations anticipées" section. Do we treat this as a skill-writing convention (document in GUIDELINES) or as a retrofit of every SKILL.md? Scope creep — probably defer to a follow-up run.

---

## 6. Recommended next step

Proceed to **Phase 2 — Architecture spec**. Spec should:
- Answer the 8 open questions above
- Produce a target architecture diagram (skills × agents × rules × hooks × scripts, meta vs template, with explicit ownership)
- Update ADR-006 (or write ADR-00X superseding it)
- Define the sync strategy between meta and template (the structural question)

Output: `.meta/drafts/spec-2026-04-14-skills-architecture.md`.

Then Phase 3 writes the execution plan with exhaustive file list.
