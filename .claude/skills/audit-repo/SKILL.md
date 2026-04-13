---
name: audit-repo
description: Standardized structural analysis of any GitHub repository — fingerprint, categories, tiered recommendations
---

# /audit-repo

Usage: `/audit-repo <url>` or `/audit-repo <url> --angle <hint>`

Produces a structured audit report in `.meta/references/interim/`. Works on **any** repo type
— language-agnostic, domain-agnostic, framework-agnostic.

---

## Hard rules

- **No modifications** to the audited repo under any circumstances
- **No secrets** in the output file — redact any credential or token found
- **Always produce the output file**, even on failure (failure reason goes in Fingerprint section)
- **Always clean up** `/tmp/audit-<slug>/` after writing the report
- **Locked section names** — the output schema is fixed; do not rename or skip sections
- Every tier must appear in the report — empty tiers get `(none)`, never omitted

---

## Process

### Phase 1 — Fetch

```bash
git clone --depth=1 --filter=blob:none <url> /tmp/audit-<slug>/
```

- `<slug>` = repo name lowercased, dashes only (e.g., `agent-reach`)
- If clone fails: write failure report, skip to Phase 5

### Phase 2 — Fingerprint

Determine repo characteristics before scanning:

1. **Language** — count file extensions; identify dominant language
2. **Type** — use presence signals:
   - `.claude/skills/` → agentic project
   - `copier.yml` / `cookiecutter.json` → template
   - `notebooks/` or `*.ipynb` → research
   - `pyproject.toml` / `Cargo.toml` / `package.json` → library or app
   - `Dockerfile` / `docker-compose.yml` → app
3. **Size** — approx file count, LOC
4. **Activity** — last commit date, stars, open issues (from README or git log)
5. **License** — from LICENSE file or README
6. **One-line pitch** — first paragraph of README

### Phase 3 — Scan (5 fixed categories)

For each category, apply examples relevant to the fingerprint detected in Phase 2.
Examples are **hints**, not rules — reason from first principles if the repo type is unusual.

#### 3.1 Extension points

| Fingerprint | Relevant examples |
|---|---|
| Agentic project | `skills/`, `agents/`, hooks, MCP server configs |
| Library | Plugin API, trait/interface surface, extension hooks |
| CLI | Subcommands, config file schema, environment variables |
| Template | `copier.yml` parameters, `_exclude` entries, jinja conditionals |
| App | Middleware, route registrations, event handlers |
| Research | Data pipeline stages, experiment config, notebook entry points |

#### 3.2 Safety & governance

Applies to **every** repo type:
- Pre-commit hooks, CI workflows (`.github/workflows/`)
- Secret scanning, `.gitignore` discipline
- `SECURITY.md`, branch protection signals
- Auth patterns, input validation, SQL injection surfaces

#### 3.3 Documentation quality

Applies to **every** repo type:
- README completeness (purpose, quickstart, examples)
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
- ADRs or decision logs
- Inline docstrings and type annotations
- Examples directory or runbook

#### 3.4 Developer workflow

Applies to **every** repo type:
- `Makefile` / `justfile` / scripts
- Test suite coverage and runner
- Lint and format tooling
- Dependency management (`uv`, `poetry`, `pip`, `cargo`, `npm`)
- Dev environment setup (`.env.example`, devcontainer, Nix)

#### 3.5 Distinctive patterns

Anything not captured above:
- Unusual architecture decisions worth noting
- Patterns that solve a recurring problem elegantly
- Anti-patterns that should be avoided

### Phase 4 — Tier recommendations

Assign each notable finding to one of 5 tiers:

| Tier | Meaning |
|---|---|
| **USE AS-IS** | Copy the file or pattern directly — no adaptation needed |
| **EXTRACT PARTS** | Take a specific chunk from a specific file |
| **BORROW CONCEPTS** | Adapt the idea to our context — no direct copy |
| **INSPIRATION** | Loose influence, no direct port |
| **REJECT** | Does not fit — explain why to reduce future noise |

All 5 tiers must appear in the output. Empty tier → `(none)`.

### Phase 5 — Write output file

Write to `.meta/references/interim/session-YYYY-MM-DD-audit-<slug>.md` following the
locked schema below.

### Phase 6 — Cleanup

```bash
rm -rf /tmp/audit-<slug>/
```

Confirm deletion before finishing.

---

## Output schema (locked)

```markdown
---
type: session
date: YYYY-MM-DD
slug: audit-<slug>
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

### 3.4 Developer workflow
...

### 3.5 Distinctive patterns
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

---

## Failure handling

If clone fails for any reason, write this minimal report:

```markdown
## 1. Fingerprint

- **Primary language:** UNREACHABLE
- **Type:** unknown
- **Clone result:** (clone failed: <reason>)

## 2–5. (clone failed: <reason>)

## 6. Metadata

- **Clone command used:** `git clone --depth=1 --filter=blob:none <url> /tmp/audit-<slug>`
- **Files read:** none
- **Audit duration:** <N>s
```

Common failure reasons:
- Private repo → "authentication required"
- 404 → "repository not found"
- Non-git URL → "not a git repository"

---

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|---|---|
| "I already know this repo well" | The audit produces a written artifact. Unrecorded knowledge evaporates. |
| "The angle hint covers everything" | Angle hints narrow focus, they don't replace structural scanning. |
| "The repo is simple, I can skip Phase 3" | Fixed categories surface findings you wouldn't look for without prompting. |
| "I'll skip empty tiers" | PM.4 synthesis depends on consistent structure. Missing tiers break the consumer. |
| "I'll clean up the clone later" | `/tmp/` clones accumulate disk space silently. Clean up now. |
