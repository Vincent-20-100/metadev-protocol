# Spec — Skills & agents architecture overhaul

**Date:** 2026-04-14
**Precursors:**
- `.meta/drafts/skills-architecture-audit.md` (Phase 1 diagnostic)
- `.meta/debates/debate-2026-04-14-skills-architecture-three-forks.md` (debate record with decisions)
**Target release:** v1.6.0
**Confidence:** AMBER (fusion introduces a novel output schema; ghost-agent removal touches every generated project on `copier update`)

---

## 1. Objective

Resolve the three-fork structural debt that accumulated through v1.0.0 → v1.5.0:

- **Broken contracts** — CLAUDE.md trigger tables (meta + template) advertise 4 agents that do not exist.
- **Author-POV drift** — the meta-repo claims to dogfood the template via `projectSettings` loading, but the mechanism does not exist and meta has stale duplicates of template skills.
- **Ambiguous surface** — `/radar` and `/audit-repo` overlap at the slash palette with no enforceable boundary.

Ship a single v1.6.0 that makes the contract truthful, the dogfooding real, and the skill surface unambiguous. Replace social discipline with mechanical invariants wherever cheap.

---

## 2. Target architecture

### 2.1 Skill/agent layout — single rule

> **Every row in any CLAUDE.md trigger table must map to a concrete artifact: a local file under `.claude/skills/<name>/` or `.claude/agents/<name>.md`, OR a labeled optional-plugin marker.**

Enforced mechanically by `scripts/check_skills_contract.py` at pre-commit.
Social discipline is insufficient; the audit proved drift between v1.4.0 and v1.5.0 alone.

### 2.2 Meta vs template — symmetric dogfooding

> **Rule: anything shipped in `template/` must also exist in the meta-repo so it can be exercised in real sessions while the template is being developed. The meta-repo is the first beta tester of every template change.**

Concretely, the meta-repo mirrors the template's `.claude/` tree:

```
metadev-protocol/
├── .claude/                            # Meta's OWN session surface (dogfood)
│   ├── settings.json                   # Committed — not just settings.local.json
│   ├── skills/                         # Same set as template/.claude/skills/
│   ├── agents/                         # Same set as template/.claude/agents/
│   └── rules/                          # Same set as template/.claude/rules/
├── template/
│   └── .claude/                        # What gets generated into new projects
│       ├── settings.json.jinja
│       ├── skills/
│       ├── agents/
│       └── rules/
├── scripts/                            # Meta-owned scripts (audit_public_safety, check_meta_naming, check_skills_contract, tech_watch/…)
└── template/scripts/                   # Scripts copied into generated projects
```

**Sync strategy.** Meta and template stay in sync through discipline + test, not runtime loading:

- Every commit that modifies `template/.claude/skills/<name>/` must also modify `.claude/skills/<name>/` (except the `.jinja` frontmatter replacements). A pre-commit hook asserts this.
- The template version uses Jinja variables (`{{ project_name }}`); the meta version hard-codes `metadev-protocol`.
- The `check_skills_contract.py` script checks both trees for parity: every template skill must exist in meta, and vice versa for any non-meta-only skill.

This is not "magic loading" — it is explicit dual maintenance with mechanical verification. The maintenance cost is small because the template changes slowly and the contract test catches drift immediately.

### 2.3 Skill inventory (target state)

| Skill | Meta `.claude/skills/` | Template `template/.claude/skills/` | Notes |
|---|---|---|---|
| `brainstorm` | ✅ | ✅ | Pure LLM, dual-maintenance |
| `debate` | ✅ | ✅ | Pure LLM |
| `orchestrate` | ✅ | ✅ | Pure LLM |
| `plan` | ✅ | ✅ | Pure LLM |
| `spec` | ✅ | ✅ | Pure LLM |
| `vision` | ✅ | ✅ | Already dual — keep |
| `research` | ✅ (sync to v1.5.0 thin version) | ✅ | Meta was stale — fix in this release |
| `tech-watch` | ✅ | ✅ | **NEW fusion** of current `/radar` + `/audit-repo`, dual-shipped |
| `test` | ✅ | ✅ | Thinned in this release (was flagged `/test` backlog) |
| `save-progress` | ✅ | ✅ | Thinned in this release (was flagged backlog) |

**Deletions:**
- `template/.claude/skills/radar/` → moved to `tech-watch/` (rename + absorb `audit-repo`)
- `.claude/skills/audit-repo/` → merged into `tech-watch/`
- `scripts/audit_repo/` (meta) → merged into `scripts/tech_watch/`
- `scripts/tech_watch.py` (meta legacy single-file) → deleted (v1.0.0 era, orphan)

### 2.4 Agent inventory (target state)

| Agent | Meta `.claude/agents/` | Template `template/.claude/agents/` | Notes |
|---|---|---|---|
| `devils-advocate.md` | ✅ | ✅ (already present) | Dual-maintenance begins here (currently meta has no `.claude/agents/` dir) |
| `code-reviewer.md` | ✅ | ✅ | **NEW** — post-implementation code review, auto-triggered on ≥3 files touched |
| `test-engineer.md` | ✅ | ✅ | **NEW** — generative test author (not a runner), propose trigger |
| `security-auditor.md` | ✅ | ✅ | **NEW** — OWASP sweep on touched code, propose trigger |
| `data-analyst.md` | ✅ | ✅ | **NEW** — statistical/pipeline audit, propose trigger. Shipped in meta too (beta-test parity per user Q6 rule) |

**Agent scopes** (crystallized 2026-04-14 during the planning session; each agent file follows the `devils-advocate.md` format with frontmatter + mandate + process + hard rules + output format + rationalizations table; model: sonnet for all four):

#### `code-reviewer`
- **Trigger:** ≥3 files touched in current plan, OR plan step just completed. **Auto.**
- **Mandate:** review post-implementation a logical change. Not a linter — a reader applying project rules, catching non-trivial logic bugs, verifying coherence with the in-flight spec/plan.
- **Process (5 steps):** identify scope (git diff HEAD~1 OR plan-listed files) → load `.claude/rules/` + CLAUDE.md rules → review by axis (correctness, style, tests, honesty) → tiered report (CRITICAL / WARN / NIT) with file:line + proposed fix + rationale → one invariant-question in closing.
- **Hard rules:** no cosmetic fixes while CRITICAL unresolved. Max 5 NIT per review. Steelman before contesting. Distinct from devils-advocate (challenges decisions, not code — never invoked together).

#### `test-engineer`
- **Trigger:** new module / new public API / missing coverage on touched code. **Propose.**
- **Mandate:** generative test author — given an implementation, propose and write the missing tests. Not a runner (`/test` does that), not a coverage checker (pytest-cov does that), an *author*.
- **Process (4 steps):** read target module + existing tests → behavioral mapping (list sentence-form test names for happy path + edges + errors + invariants) → write 2–5 concrete tests per `rules/testing.md` → `uv run pytest <new> -v` + report pass/fail.
- **Hard rules:** no assertion-less test. No `assert True`. No duplicates (read existing tests first). No mocks of internal services — only boundary mocks via fixtures.
- **Output:** pytest files created/modified in `tests/` + summary of what was added and why.

#### `security-auditor`
- **Trigger:** auth / secrets / input validation / crypto / network boundaries / file uploads / path traversal / command injection. **Propose.**
- **Mandate:** OWASP-style sweep scoped to a diff or module (NOT the whole repo — that's `audit_public_safety.py`'s job). Analyzes the *logic* of a specific change.
- **Process (4 steps):** attack surface mapping (user input, network, fs, subprocess) → OWASP-category sweep (only applicable categories) → tiered findings (EXPLOIT / HARDENING / INFO) → concrete fix per finding (minimal diff + rationale).
- **Hard rules:** reports only what touches the code under review (no global sweep). No hypothetical "what if" without a concrete vector. No false positives on stdlib safe usage.

#### `data-analyst`
- **Trigger:** pipeline / ETL / metric computation / statistical claim / dataset quality question. **Propose.**
- **Mandate:** audit statistical claims, pipelines, metric computations. Catches sampling bias, leakage, reproducibility gaps, off-by-one on temporal windows, metric gaming.
- **Process (4 steps):** identify claim or pipeline scope (file/function/notebook) → verify assumptions (types, shapes, distributions, invariants) → classical traps hunt (train-test leakage, look-ahead, survivorship, p-hacking, multiple comparisons) → propose validation tests (freeze detected invariants + sanity checks on shape/nullity/range).
- **Hard rules:** never "looks correct" — always exhibit proof (distribution / shape / value). Reproducibility check mandatory: no seed = HARDENING finding. Skip if code doesn't manipulate data (out of scope).
- **Meta-repo applicability:** limited (template repo has no data pipelines) but shipped in meta for symmetric beta-test per user Q6 rule ("tout ce qui est dans template doit exister en meta pour beta-test").

**Superpowers plugin positioning** (framing confirmed 2026-04-14):

The local skills `brainstorm`, `plan`, `spec`, `debate`, `orchestrate`, `research`, `test`, `save-progress` are **fallbacks**. The `superpowers` plugin ships superior and more complete versions (`superpowers:brainstorming`, `superpowers:writing-plans`, `superpowers:executing-plans`, `superpowers:test-driven-development`, `superpowers:requesting-code-review`, `superpowers:systematic-debugging`, …). When `superpowers` is installed, it is the preferred provider; our local skills exist so the template works out-of-the-box without requiring any plugin install.

The four new local agents (`code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst`) are **additive**, not fallbacks — their scopes complement but do not duplicate the superpowers agents exactly, and a user with superpowers installed benefits from both sets.

CLAUDE.md and CLAUDE.md.jinja keep their existing "Recommended plugin" section pointing at superpowers (already present in v1.5.0). The section is strengthened to make the fallback relationship explicit for the core skills.

**No plugin-pointer row in the trigger table.** The debate's original "optional:plugin" row is abandoned because we ship the 4 agents locally. The contract script does NOT need an external allowlist — every row maps to a local file.

### 2.5 Rules inventory (target state)

`template/.claude/rules/` (already exists):
- `code-style.md`
- `testing.md`

Meta `.claude/rules/` (to create, symmetric):
- `code-style.md`
- `testing.md`

### 2.6 Hooks inventory (target state)

`scripts/` (meta) and `template/scripts/` (copied into generated projects):

| Hook script | Purpose | Meta | Template |
|---|---|---|---|
| `audit_public_safety.py` | Secrets + gitignore scan | ✅ | ✅ |
| `check_meta_naming.py` | `.meta/` filename taxonomy | ✅ | ✅ |
| `check_git_author.py` | Block Claude/Anthropic authorship | ✅ | ✅ |
| **`check_skills_contract.py`** | **NEW — every trigger-table row maps to an artifact** | ✅ | ✅ |

`.pre-commit-config.yaml` (meta) and `template/.pre-commit-config.yaml`:
Add a `check-skills-contract` hook pointing to the new script.

---

## 3. Unified `/tech-watch` contract

### 3.1 Scope

`/tech-watch` is a single skill that produces **structured technical review notes** about external software. It adapts its depth to the input:

- **Sweep mode** (no positional argument, or explicit `--sweep`) — periodic multi-source discovery. Fetches emerging repos/articles from 5 tier-0 sources, scores by project themes, writes one shallow card per survivor to `.meta/references/research/`. This is the current `/radar` behavior.
- **Deep mode** (positional argument = a GitHub URL, or explicit `--deep <url>`) — targeted analysis of a single repository. Clones, fingerprints, runs the 5-category scan, tiers recommendations, writes one deep card to `.meta/references/research/`. This is the current `/audit-repo` behavior.

Both modes produce cards that share the same front-matter schema and section skeleton. Deep cards have more sections filled; shallow cards have fewer. A human or subsequent LLM can mix-and-match cards in the same directory without schema collisions.

### 3.2 Invocation

```bash
# Sweep
uv run python -m scripts.tech_watch                  # sweep across all themes
uv run python -m scripts.tech_watch --sweep          # same, explicit
uv run python -m scripts.tech_watch --refresh-themes # re-extract themes from PILOT.md

# Deep
uv run python -m scripts.tech_watch https://github.com/astral-sh/ruff
uv run python -m scripts.tech_watch --deep https://github.com/astral-sh/ruff --angle <hint>
```

The skill invokes the script and frames the output for the user.

### 3.3 Unified card schema

All cards live at `.meta/references/research/<slug>.md`:

```markdown
---
type: research-card
date: YYYY-MM-DD
slug: <kebab-slug>
mode: sweep | deep
source: <source_key>          # for sweep: feed/api id; for deep: "manual-url"
url: <canonical url>
themes: [theme1, theme2]      # for sweep; for deep: derived from angle or fingerprint
confidence: low | medium | high
---

# <Repo or article title>

## Fingerprint
<common fields: primary language, type, license, stars, last commit, pitch>
<deep-only additional fields: file count, detected frameworks, notable dependencies>

## Pitch
<1-3 sentences>

## Structure map                (deep only — curated tree -L 2)
## Key findings                 (deep only — 5 fixed categories)
### Extension points
### Safety & governance
### Documentation quality
### Developer workflow
### Distinctive patterns

## Tiered recommendations       (deep only)
### USE AS-IS
### EXTRACT PARTS
### BORROW CONCEPTS
### INSPIRATION
### REJECT

## Sweep context                (sweep only — why this surfaced)
- Matched themes: ...
- Score: ...
- Source: ...

## Open questions
- ...

## Metadata
- Mode: sweep | deep
- Fetched at: <timestamp>
- Script version: <semver>
```

A sweep card fills lines 1–10 of the schema (front-matter, Fingerprint, Pitch, Sweep context, Metadata). A deep card fills everything except Sweep context. A downstream consumer can detect the card type by the `mode:` front-matter field.

### 3.4 Python package layout

`scripts/tech_watch/` (meta) and `template/scripts/tech_watch/` (template):

```
tech_watch/
├── __init__.py
├── __main__.py          # CLI entry: dispatches sweep vs deep based on argv
├── core.py              # shared card writing, schema validation
├── sweep/
│   ├── __init__.py
│   ├── sources/         # feed adapters (GitHub trending, HN, arXiv, Papers with Code, HuggingFace)
│   ├── themes.py        # ThemesConfig + extraction from PILOT.md
│   ├── dedup.py         # canonical URL dedup
│   ├── score.py         # theme pertinence scoring
│   └── fetch.py         # orchestrates sweep run
├── deep/
│   ├── __init__.py
│   ├── clone.py         # shallow clone + cleanup
│   ├── fingerprint.py   # language, type, stars, last commit, license, pitch
│   ├── tree.py          # tree -L 2 builder
│   └── scan.py          # 5-category scan (USE/EXTRACT/BORROW/INSPIRATION/REJECT)
├── index.py             # regenerates .meta/references/research/INDEX.md
└── report.py            # card-writing (used by both modes)
```

Absorbs:
- `template/scripts/radar/*` → `tech_watch/sweep/*` + shared core
- `scripts/audit_repo/__main__.py` (meta) → `tech_watch/deep/*`

Dead:
- `scripts/tech_watch.py` (meta, legacy single-file v1.0.0) → deleted

### 3.5 Thin SKILL.md

`.claude/skills/tech-watch/SKILL.md` (≤ 100 lines):

```markdown
---
name: tech-watch
description: Structured technical review — sweep across sources or deep-dive on a URL, unified card schema in .meta/references/research/
---

# /tech-watch

Usage:
  /tech-watch                  → sweep mode (periodic multi-source discovery)
  /tech-watch <github-url>     → deep mode (targeted analysis of one repo)
  /tech-watch --refresh-themes → re-extract themes from PILOT.md

## Hard rules

- Never fetch content manually — always delegate to the script.
- Every card goes to `.meta/references/research/<slug>.md` using the shared schema.
- Sweep and deep modes share front-matter fields; a downstream consumer must not care about mode except via the `mode:` key.
- On first sweep run, bootstrap `.meta/research-themes.yaml` from PILOT.md (conversational — show and confirm).

## Three steps

1. Classify the input (no args → sweep; positional URL → deep).
2. Run the script (`uv run python -m scripts.tech_watch ...`).
3. Frame the output: count cards, surface the top-ranked or deepest findings, propose next step (`/brainstorm` if a decision emerges, `/audit-repo`-style follow-up if a sweep card deserves deep-diving, or nothing).
```

---

## 4. Contract check script — `scripts/check_skills_contract.py`

### 4.1 What it asserts

For each of `CLAUDE.md` (meta) and `template/CLAUDE.md.jinja`:

1. Parse the Skills & Agents trigger table (pipe-separated markdown table rows after the first `## Skills & Agents` heading).
2. For each row, read the first column (skill/agent name) and the second column (Type: `skill` or `agent`).
3. If Type is `skill`: assert `.claude/skills/<name>/SKILL.md` exists in the same tree (meta → `./.claude/skills/`, template → `./template/.claude/skills/`).
4. If Type is `agent`: assert `.claude/agents/<name>.md` exists in the same tree.
5. For each skill directory found in the tree, assert at least one row references it (no dead skill directories).
6. For each agent file found, assert at least one row references it.
7. For meta vs template parity: assert every skill in `template/.claude/skills/` has a counterpart in `.claude/skills/` (meta), AND every agent in `template/.claude/agents/` has a counterpart in `.claude/agents/` (meta). No exceptions — user Q6 rule enforces full symmetry (data-analyst included in meta even though metadev has no data pipelines).

No plugin-pointer handling needed — the 4 agents ship locally.

### 4.2 What it does NOT assert

- SKILL.md content quality (style, length, completeness) — that's humans and other hooks.
- That the script the skill invokes exists or runs — the wrapper points at `scripts/X`; if X is missing, the pytest `TestSkills` suite catches it.
- Semantic correctness of the trigger (the rule says "when X happens, propose Y"); only structural presence.

### 4.3 Integration

- `.pre-commit-config.yaml` (meta) adds a new local hook `check-skills-contract` running the script.
- `template/.pre-commit-config.yaml` same, copied verbatim.
- `tests/test_template_generation.py` adds `TestSkillsContract::test_generated_project_passes_contract_check` invoking the script on a freshly generated project.

---

## 5. What moves, what stays, what gets deleted

### 5.1 Renames and merges

| From | To | Action |
|---|---|---|
| `template/scripts/radar/` | `template/scripts/tech_watch/sweep/` + shared core | Move + restructure |
| `template/.claude/skills/radar/` | `template/.claude/skills/tech-watch/` | Rename + rewrite SKILL.md |
| `scripts/audit_repo/` (meta) | `scripts/tech_watch/deep/` (meta) | Move + restructure |
| `.claude/skills/audit-repo/` | merged into `.claude/skills/tech-watch/` | Delete — content absorbed into tech-watch SKILL.md |
| `.meta/research-themes.yaml` (schema) | same path, new format if needed for deep mode defaults | Schema extension |
| `.meta/references/research/` INDEX.md | same file, regenerated by `tech_watch.index` with mixed cards | Regenerate |

### 5.2 Creations

- `scripts/tech_watch/` package in the meta-repo (currently missing — dogfooding gap)
- `template/scripts/tech_watch/` package in the template (absorbs `radar/` + `audit_repo/` code)
- `scripts/check_skills_contract.py` (meta)
- `template/scripts/check_skills_contract.py` (template, identical content)
- `.claude/agents/devils-advocate.md` (meta — currently missing, copied from template)
- `.claude/rules/code-style.md` (meta — currently missing, copied from template)
- `.claude/rules/testing.md` (meta — currently missing, copied from template)
- `.claude/settings.json` (meta — currently only `settings.local.json` exists; create a committed version for the dogfood contract)
- `.meta/GUIDELINES.md` (meta — currently missing; copy from template's rendered output)
- `.meta/decisions/adr-NNN-skills-architecture.md` (new ADR superseding ADR-006)

### 5.3 Deletions

- `scripts/tech_watch.py` (meta, legacy single-file v1.0.0 orphan)
- `.claude/skills/research/SKILL.md` (meta, stale v1.4.0 era version) → replaced by sync with template
- All 4 ghost agent rows from trigger tables (code-reviewer, test-engineer, security-auditor, data-analyst)
- Any lingering references to `/radar` in docs, tests, memory, PILOT — rename to `/tech-watch`

### 5.4 Updates (doc cascade)

| File | Update |
|---|---|
| `CLAUDE.md` (meta) | Rewrite Skills & Agents section: delete ghost rows, add plugin pointer row, rename `/radar` → `/tech-watch`, delete `audit-repo` row, add note about contract check |
| `template/CLAUDE.md.jinja` | Same |
| `.meta/ARCHITECTURE.md` | Supersede ADR-006; add new ADR-NNN with current 10-skill inventory and the dual-maintenance dogfooding rule |
| `.meta/PILOT.md` | Update Vision ("8+ skills" → "10+ skills"); add v1.6.0 changelog line; update roadmap state |
| `.meta/DECISIONS.md` | Add ADR-NNN entry |
| `README.md` | Rewrite skill listing; update `/radar` refs to `/tech-watch` |
| `CHANGELOG.md` | Add v1.6.0 section |
| `template/.meta/GUIDELINES.md.jinja` | Verify skill-vs-tool section still accurate; update skill inventory |
| `tests/test_template_generation.py` | Update `TestSkills.EXPECTED_SKILLS` list; add `test_tech_watch_has_sweep_and_deep_modes`; add `TestSkillsContract` |
| Individual SKILL.md files that cross-reference `/radar` or `/audit-repo` | Rename references to `/tech-watch` |

---

## 6. Non-goals for this release

Explicitly NOT in scope for v1.6.0, per the debate and the user's scoping:

- **Colocation refactor** (scripts moving under `.claude/skills/<name>/`) — deferred to v2.0.0. The contract check delivers the "no ghosts" invariant that colocation would have provided structurally.
- **Emergent-patterns retrofit** (Pattern #4 from `emergent-patterns.md` — rationalizations sections in every SKILL.md). Noted as Q8 in the audit, to be handled in a separate chantier later with its own debate + spec.
- **Shipping real `code-reviewer`, `security-auditor`, etc. agent files** — delete from the contract, re-add only when each is actually implemented, one commit per agent.
- **Meta-only tools that might need to exist** — currently nothing is planned. If any surface during implementation, they get added to the contract script's meta-only whitelist, not hand-waved.

---

## 7. Open questions (to answer during `/plan`)

1. **Card slug format for sweep cards** — currently radar uses `<source>-<date>-<slug>`. Does the fusion preserve this or normalize? → Keep current radar convention for sweep; deep cards use `deep-<repo-slug>-<date>`.
2. **`research-themes.yaml` schema extension** — does deep mode need default angles per theme? → Probably no; deep mode takes `--angle` explicitly. Themes only govern sweep scoring.
3. **Meta `.claude/settings.json` content** — should it be `full-auto` or `safe`? The repo is dogfooded by Vincent alone; `full-auto` makes sense. → Confirm with Vincent in the plan review.
4. **Dual-maintenance pre-commit hook** — is it enforced in v1.6.0 or deferred? Strict parity is the rule, but the hook is non-trivial to write correctly (Jinja diffing). → Ship a simpler version first: assert filename parity, not content parity. Content parity becomes v1.7.0.

---

## 8. Confidence & risks

**Confidence: AMBER.**

**GREEN on:**
- Ghost agent deletion (pure markdown edits, 100% mechanical)
- Contract check script (~50–80 lines of Python, easy to test)
- Dual-maintenance file creation (copies from template to meta)
- Dogfooding symmetry principle (user explicitly validated)

**AMBER on:**
- Tech-watch fusion — the unified card schema is novel. Sweep and deep currently produce different output shapes. Merging them cleanly requires the schema to be correct on first try; an incorrect schema means rewriting every card on the second release.
- `copier update` downstream impact — every external project on v1.5.0 will see major file moves (radar → tech_watch, audit-repo → tech-watch). The update diff will be large and potentially confusing.
- Meta dogfooding rollout — the meta-repo has gone ~9 releases without real symmetric dogfooding. Turning it on suddenly may surface latent bugs in skills that have never been exercised in the meta context.

**RED on:**
- None in this spec. The plan step will flag any RED risks that surface during file-level enumeration.

---

## 9. Next step

Proceed to `/plan`: exhaustive file list, task decomposition, commit sequence, verify steps per task. Plan output: `.meta/drafts/plan-skills-architecture.md`.
