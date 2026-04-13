---
type: plan
date: 2026-04-13
slug: research-skill
status: active
---

# Plan — `/research` skill (PM.1b)

**Goal:** Ship a `/research` skill that gathers structured external research
(web + docs + MCP) and writes the findings to `.meta/references/raw/`. Clean
orthogonality with `/brainstorm` (internal ideation) and `/audit-repo`
(GitHub-specific deep dives).

**Brainstorm source:** `archive/brainstorm-2026-04-13-research-skill.md`
**Reference source:** `Panniantong/Agent-Reach` — audit for web-research loop
patterns, source consolidation, relevance ranking, output format choices.

**Confidence:** GREEN — decisions locked in brainstorm, full-auto ready.

**Scope:** **shipped in template** (generated projects need it) + skills-pack mirror.

---

## Decisions (locked from brainstorm)

| # | Decision | Chosen |
|---|---|---|
| D1 | Scope | External research only — web + docs + MCP |
| D2 | Output location | `.meta/references/raw/session-YYYY-MM-DD-research-<slug>.md` |
| D3 | Tools | WebSearch + WebFetch + MCP servers (context7 etc.) when present |
| D4 | Relationship | Strict orthogonality with `/brainstorm` |
| D5 | Output schema | Standardized: question / sources / findings / open questions / next step |
| D6 | Invocation | Manual in v1 |
| D7 | Time-box | Soft budget of 8 WebFetch calls per run (the skill recommends, does not enforce) |
| D8 | Citation format | Per-section bullets with URL + snippet + date-accessed |
| D9 | Source diversity | Skill prompts for min 3 distinct sources; warns if fewer at the end |

---

## Output schema (locked)

```markdown
---
type: session
date: YYYY-MM-DD
slug: research-<slug>
status: active
---

# Research — <question in one line>

**Question:** <full question>
**Date:** YYYY-MM-DD
**Sources consulted:** N (web: A, docs: B, MCP: C)

## 1. Context
<2-4 lines on why this research was needed>

## 2. Sources
- **[1]** <title> — <url> — accessed YYYY-MM-DD
- **[2]** ...

## 3. Findings (by theme)

### 3.1 <theme>
- <finding> [1]
- <finding> [2,3]

### 3.2 <theme>
...

## 4. Consensus vs divergence
- **Consensus across sources:** ...
- **Divergences / contradictions:** ...

## 5. Open questions for follow-up
- ...

## 6. Suggested next step
- `/brainstorm` if decision needed, or `/spec` if scope clear
```

---

## Tasks

### Task 1 — Audit Agent-Reach for patterns

- [ ] If PM.6 `/audit-repo` is already shipped → run `/audit-repo https://github.com/Panniantong/Agent-Reach --angle web-research-patterns`
- [ ] If PM.6 is NOT yet shipped → manual scan via WebFetch: README, any `research/` or `search/` directory, any prompt files. Note patterns worth absorbing in a new note under `.meta/references/interim/`
- [ ] Decisions to validate from the audit:
  - Does Agent-Reach use a query-expansion loop (initial query → follow-ups) or one-shot? Adopt if it fits.
  - Does it enforce source diversity? Our D9 says yes — confirm approach.
  - Does it do inline citation or end-of-doc bibliography? Our D8 says per-section bullets — confirm.

### Task 2 — Write `template/.claude/skills/research/SKILL.md`

- [ ] Frontmatter (`name: research`, `description: external research with WebSearch + WebFetch + MCP`)
- [ ] Hard rules:
  - No code editing
  - Always write output file to `.meta/references/raw/`
  - Always cite sources with URL + date
  - Warn if fewer than 3 distinct sources
  - Soft budget: recommend stopping at 8 WebFetch calls, let user override
- [ ] Process:
  1. Clarify the question (one reformulation pass)
  2. Initial WebSearch with 2-3 query variants
  3. Fetch top 3-5 promising URLs with WebFetch
  4. Check MCP servers if available (context7 for library docs)
  5. Identify themes across findings
  6. Spot consensus and divergence
  7. Write the output file following the schema
  8. Propose next step (`/brainstorm`, `/spec`, or nothing)
- [ ] Rationalizations table (common excuses to skip steps): "I know the answer" → you're reasoning from training data, which may be stale; "one source is enough" → enforce minimum 3; etc.
- [ ] Output schema embedded from §Output schema above

### Task 3 — Mirror in skills-pack

- [ ] Copy `template/.claude/skills/research/` → `skills-pack/skills/research/`
- [ ] Verify the skill is standalone (no dependency on `.meta/` taxonomy beyond the output path — which becomes optional in skills-pack context)

### Task 4 — Dogfood in meta-repo

- [ ] Copy the skill into `.claude/skills/` at meta-repo root (same as other dogfooded skills) so it's immediately usable in THIS repo
- [ ] Run a real research session (suggest: "what are emerging patterns in AI-coding project templates post-2025-Q4?") to validate the output schema
- [ ] If the schema reveals gaps, iterate SKILL.md once

### Task 5 — CREDITS.md update

- [ ] Add Panniantong/Agent-Reach under "Reference sources" with one-line rationale
- [ ] Re-confirm Guillaume Desforges entry mentions `/research` as absorbed

---

## Ripple effects (downstream updates — MANDATORY)

| Area | File | Update | Notes |
|---|---|---|---|
| **Template CLAUDE.md** | `template/CLAUDE.md.jinja` | Add `/research` row to Skills & Agents trigger table | Trigger: "question needs external facts / recent state-of-the-art / competitive info" — **Propose** |
| **Meta-repo CLAUDE.md** | `CLAUDE.md` | Same row in the meta-repo trigger table | Dogfooding parity |
| **Template skills count** | `template/CLAUDE.md.jinja` | Any hardcoded "8 skills" → "9 skills" | Grep for "8 skills" |
| **Meta-repo skills count** | `CLAUDE.md` | Same | Grep for "8 skills" |
| **README.md** | `README.md` | Add `/research` row in "Skills" table of the Toolkit section | One-liner: "External research — WebSearch + WebFetch + MCP, 8-call soft budget, standardized output to `raw/`" |
| **README.md** | `README.md` | Update hero bullets if they mention skills count | Grep "8 skills" |
| **README.md** | `README.md` | Update Rails diagram if REMEMBER/PLAN/GUARD/SHIP labels list skills | PLAN stage currently lists `/brainstorm /spec /plan /debate /orchestrate` — add `/research` |
| **PHILOSOPHY.md** | `docs/PHILOSOPHY.md` | Skills count 8 → 9; add `/research` row to the skills table; mention in progressive disclosure layer | Also check "8 built-in skills" literal |
| **CHANGELOG.md** | `CHANGELOG.md` | New `[v1.2.0]` section if not already open, add under `Added:` | `**New skill: /research**` with one-line description |
| **skills-pack/README.md** | `skills-pack/README.md` | Add `/research` row in the Available skills table | Standalone description |
| **Template generation test** | — | Run `copier copy . /tmp/test-research --defaults --trust --vcs-ref=HEAD` | Verify `.claude/skills/research/SKILL.md` lands in generated project |
| **Pytest template test** | `tests/test_template_generation.py` | If the test enumerates shipped skills, add `research` to the expected list | Grep for skill names in tests/ |
| **PILOT.md** | `.meta/PILOT.md` | PM.1b → DONE | With commit ref |
| **ARCHITECTURE.md** (meta) | `.meta/ARCHITECTURE.md` | If skills list is documented, add `/research` | Check file first |
| **CREDITS.md** | `CREDITS.md` | Add Panniantong/Agent-Reach reference line | §Reference sources |

**Grep checklist (run before committing):**
```bash
grep -rn "8 skills" --include="*.md" --include="*.jinja"
grep -rn "brainstorm.*spec.*debate.*plan.*orchestrate" --include="*.md" --include="*.jinja"
grep -rn "/brainstorm.*/plan.*/orchestrate" --include="*.md" --include="*.jinja"
```

Every match is a potential update site.

---

## Verification checklist

- [ ] `template/.claude/skills/research/SKILL.md` exists and is syntactically valid
- [ ] `skills-pack/skills/research/SKILL.md` is a working mirror
- [ ] Meta-repo can invoke `/research` (skill is dogfooded)
- [ ] Real research session produces a valid output file matching the schema
- [ ] `CLAUDE.md.jinja` trigger table lists `/research`
- [ ] Meta-repo `CLAUDE.md` trigger table lists `/research`
- [ ] All "8 skills" literals bumped to "9 skills"
- [ ] README toolkit table has the `/research` row
- [ ] Rails diagram in README updated (PLAN stage)
- [ ] PHILOSOPHY.md skills table and count updated
- [ ] CHANGELOG has v1.2.0 Added entry
- [ ] skills-pack README updated
- [ ] Template generation test passes (`copier copy ... --defaults --trust`)
- [ ] `tests/test_template_generation.py` passes
- [ ] `uv run ruff check .` passes
- [ ] PILOT.md backlog: PM.1b → DONE
- [ ] CREDITS.md updated (Agent-Reach + Guillaume)
- [ ] Brainstorm archive file exists (already done in this commit batch)

---

## Out of scope (deferred)

- **Auto-digest raw → interim promotion** — future `/digest` skill
- **Multi-language search** — v2
- **Academic paper search (arxiv API)** — v2
- **Credential-gated sources** — permanently out of scope
- **Auto-invocation via trigger table** — dogfood first, then decide

---

## Commit plan

Two commits (one logical unit each):

1. `feat(skills): add /research skill to template and skills-pack`
   - `template/.claude/skills/research/SKILL.md`
   - `skills-pack/skills/research/SKILL.md`
   - `.claude/skills/research/SKILL.md` (meta-repo dogfood)

2. `docs: propagate /research skill across README, PHILOSOPHY, CHANGELOG, CLAUDE.md`
   - README.md
   - docs/PHILOSOPHY.md
   - CHANGELOG.md
   - template/CLAUDE.md.jinja
   - CLAUDE.md (meta)
   - skills-pack/README.md
   - CREDITS.md
   - .meta/PILOT.md
   - tests/test_template_generation.py (if affected)

If the template generation test catches a regression, fix in a third commit rather than amending.
