---
type: plan
date: 2026-04-13
slug: audit-repo-skill
status: active
---

# Plan — `/audit-repo` skill (PM.6)

**Goal:** A **versatile, repo-agnostic** Claude Code skill that structurally
analyzes any GitHub repository and produces a standardized audit report
in `.meta/references/interim/`. The point is reusability across every project
the user has, not metadev-specific tooling.

**Core principle:** the skill must be **language-agnostic, domain-agnostic,
and framework-agnostic**. It produces the SAME output structure regardless
of the audited repo type. Interpretation depth happens after the audit, not
inside it.

**Scope:** meta-repo only. Skill lives in `.claude/skills/audit-repo/` at
meta-repo root (same location as other dogfooded skills). NOT shipped in
the template.

**Confidence:** AMBER — skill-design questions are resolved, but first real
audit run may surface output-format tweaks. The plan commits to a conservative
v1 that can iterate without breaking downstream consumers.

---

## Decisions (locked)

| # | Decision | Chosen | Reason |
|---|---|---|---|
| D1 | Placement | meta-repo only, `.claude/skills/audit-repo/SKILL.md` | Personal tool, not a template feature |
| D2 | Reusability constraint | Skill must work on ANY repo type — not metadev-specific | User requirement: "réutilisable pour tout mes projets" |
| D3 | Output structure | Fixed template, always the same sections | Enables future PM.4 multi-agent synthesis to consume audits uniformly |
| D4 | Fetch method | Clone shallow (`git clone --depth=1 --filter=blob:none`) to `/tmp/audit-<slug>/` | Read/Grep/Glob work on filesystem directly, no API plumbing |
| D5 | Input | `repo_url` (required), optional `angle` free-text hint | Keeps invocation simple |
| D6 | Tiered recommendation levels | 5 tiers: USE AS-IS / EXTRACT PARTS / BORROW CONCEPTS / INSPIRATION / REJECT | User confirmed REJECT tier reduces synthesis noise |
| D7 | Output location | `.meta/references/interim/session-YYYY-MM-DD-audit-<repo-slug>.md` | Filename respects meta taxonomy; `interim/` = processed external research |
| D8 | Cleanup | Skill deletes `/tmp/audit-<slug>/` after writing the report | No orphan clones on disk |
| D9 | Depth of analysis | Scan structure + README + top-level config + up to 5 "key files" discovered dynamically | Time-boxed; avoid trying to fully understand the repo |
| D10 | Versatility mechanism | Skill instructions list CATEGORIES of things to look for with repo-type-dependent EXAMPLES, not hardcoded rules | Agent adapts examples to what it actually finds |
| D11 | Project-type inference | Skill includes a "repo fingerprint" step: language / framework / agentic / library / app / template / research — informs which examples from D10 apply | Auto-tagging without locking in behaviour |
| D12 | Failure modes | Private repo / 404 / non-git URL / clone failure → skill reports the error in the output file and exits | Audit artifact exists for every invocation |

---

## Versatility principle (D2 + D10 detailed)

The skill must NOT have hardcoded branches like "if agentic project, look at
skills/". Instead, the SKILL.md prompts the LLM to:

1. **Fingerprint the repo** (language, framework, purpose, size).
2. **Scan a fixed list of categories** — same categories for every repo.
3. **For each category, apply examples relevant to the fingerprint** —
   examples are *hints*, not rules. If the fingerprint is "agentic Python
   project", skills/ and tools/ are relevant examples. If it's a Rust CLI,
   the same category ("extension points") points to Cargo features, subcommands.
4. **Produce the same output schema** regardless.

**Illustrative examples (in SKILL.md, not hardcoded):**
- Category "Extension points" →
  - Agentic project: skills/, agents/, hooks/, MCP servers
  - Library: plugin API, trait/interface surface
  - CLI: subcommands, config file schema
  - Template: copier.yml parameters, `_exclude` entries
- Category "Safety & governance" →
  - Any project: pre-commit, CI workflows, security policies, SECRETS handling
- Category "Documentation quality" →
  - Any project: README, CONTRIBUTING, ADRs, inline docstrings, examples

The skill's value is the **standardized output structure + category checklist**,
not domain expertise.

---

## Output schema (D3 — locked)

Every audit report follows this exact structure:

```markdown
---
type: session
date: YYYY-MM-DD
slug: audit-<repo-slug>
status: active
---

# Audit — <owner/repo>

**URL:** <url>
**Audited:** YYYY-MM-DD
**Angle hint:** <angle or "general">

## 1. Fingerprint

- **Primary language:** ...
- **Type:** agentic / library / CLI / template / app / research / other
- **Size:** N files, M LOC (approx)
- **Activity:** last commit, open issues, stars
- **License:** ...
- **One-line pitch:** ...

## 2. Structure map

<tree -L 2 output, curated — only meaningful entries>

## 3. Key findings per category

### 3.1 Extension points
- **What:** ...
- **Where:** `path/to/file:line`
- **Why it matters:** ...

### 3.2 Safety & governance
...

### 3.3 Documentation quality
...

### 3.4 Developer workflow (tooling, scripts, automation)
...

### 3.5 Distinctive patterns (anything outside the above categories)
...

## 4. Tiered recommendations

### USE AS-IS
- [item] — copy path `...` — rationale

### EXTRACT PARTS
- [item] — take `<specific chunk>` from `path/to/file` — rationale

### BORROW CONCEPTS
- [concept] — adapt idea to our context — rationale

### INSPIRATION
- [theme] — loose influence, no direct port — rationale

### REJECT
- [item] — why it does not fit — rationale

## 5. Open questions for follow-up

- ...

## 6. Metadata

- **Clone command used:** `git clone --depth=1 --filter=blob:none <url> /tmp/audit-<slug>`
- **Files read:** `<list>`
- **Audit duration:** approximate
```

**Locked sections:** 1, 2, 3.1–3.5, 4 (all 5 tiers, even if empty), 5, 6.

Even an empty tier must appear with "(none)" — the synthesis run (PM.4) depends
on consistent structure.

---

## Tasks

### Task 1 — SKILL.md draft

- [ ] Create `.claude/skills/audit-repo/SKILL.md` with:
  - Frontmatter (`name: audit-repo`, `description: ...`)
  - Usage examples (`/audit-repo <url>`, `/audit-repo <url> --angle <hint>`)
  - Hard rules (no modifications to audited repo, no secrets committed, always produce output file)
  - Phase-by-phase process (fetch → fingerprint → scan → tier → write → cleanup)
  - Output schema locked from §Output schema above
  - "Rationalizations" table (common excuses to skip steps) — dogfood the skill template style
  - Versatility reminder: categories are fixed, examples are fingerprint-dependent

**Files:**
- `.claude/skills/audit-repo/SKILL.md` (new)

### Task 2 — Category examples library

- [ ] In SKILL.md, include a collapsible "Examples per fingerprint" appendix
  with 5-6 repo types (agentic, library, CLI, template, app, research) × 5 categories
- [ ] Keep examples illustrative, not prescriptive — max 2-3 examples per cell
- [ ] Explicit note: "If the repo does not match any listed fingerprint, reason
  from first principles using the category names"

### Task 3 — Repo fingerprint heuristics

- [ ] In SKILL.md, document a short heuristic for fingerprinting:
  - Language: count file extensions
  - Type: presence of `pyproject.toml` / `Cargo.toml` / `package.json`; presence of `.claude/skills/` (agentic signal); presence of `copier.yml` / `cookiecutter.json` (template); presence of `notebooks/` (research)
  - One-line pitch: lift from README first paragraph
- [ ] No external classifier — the LLM interprets on the fly

### Task 4 — Failure handling

- [ ] If clone fails, write an audit file with Fingerprint = "UNREACHABLE",
  all other sections marked "(clone failed: <reason>)", and still commit the
  artifact under `.meta/references/interim/`
- [ ] Private repo → same path, reason = "authentication required"
- [ ] Non-git URL → reason = "not a git repository"

### Task 5 — Dogfood test run

- [ ] Execute the skill on one reference repo post-implementation
  (suggest: `GuillaumeDesforges/claude-ai-project-starter`) to validate output format
- [ ] If the output reveals schema gaps, iterate the SKILL.md once; do not break
  the locked section names

---

## Verification checklist

- [ ] Skill exists at `.claude/skills/audit-repo/SKILL.md`
- [ ] First smoke test produces a valid audit file under `.meta/references/interim/`
- [ ] Audit file filename passes `check_meta_naming.py` (uses `session-` prefix)
- [ ] All 5 tiers present in output (including empty ones as "(none)")
- [ ] Output schema sections match the locked template exactly
- [ ] `/tmp/audit-<slug>/` is cleaned up after the run
- [ ] SKILL.md references zero metadev-specific concepts in the category list
- [ ] CLAUDE.md trigger table updated to include `/audit-repo` with a trigger row

---

## Out of scope (deferred)

- **Auto-invocation** from tech-watch output (user runs manually on curated URLs)
- **Batch mode** (`/audit-repo <url1> <url2> ...`) — one at a time in v1
- **Diff audits** (compare two versions of the same repo over time) — future
- **Private repo support via token** — v2 if ever
- **Inline code block quoting** in the audit — link to `path:line`, don't copy code

---

## File summary (for full-auto execution)

**New files:**
- `.claude/skills/audit-repo/SKILL.md`

**Modified files:**
- `CLAUDE.md` (add `/audit-repo` row to the Skills & Agents trigger table)

**Commit:** `feat(skills): add /audit-repo skill for standardized repo analysis`
