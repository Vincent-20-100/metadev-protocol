---
type: spec
date: 2026-04-11
slug: meta-taxonomy
status: active
---

# Spec — `.meta/` taxonomy (flat state-outer + prefixed filenames)

**Source:** `.meta/debates/debate-meta-taxonomy.md` (2026-04-11)
**Replaces:** `.meta/scratch/plan-meta-visibility.md` (draft superseded — had wrong assumptions about scratch/)
**Status:** active — pending plan
**Drives:** PILOT items 0.2 (meta_visibility), 0.3 (.meta/ gitignore alignment)

---

## Problem

`.meta/scratch/` currently conflates three incompatible lifecycles:
- **Drafts** (real WIP, safe to drop) — e.g. `v2-part2-brainstorm.md`
- **Validated artifacts** (approved, not yet implemented) — e.g. `spec-workflow-gates.md`, `plan-rodin-agent.md`, `launch-plan.md`
- **Archived artifacts** (implemented, historical) — e.g. `mvp-phase-a-plan.md`, `adr-008-implementation-plan.md`

Consequences:
- Impossible to gitignore cleanly: either commit drafts (noise in public repo) or untrack validated plans (loss)
- No semantic home for plans / specs / brainstorms — they all land in `scratch/` fourre-tout
- 14 tracked files mix states; 22 files in `references/` are unsorted research
- Visitors of the public repo see `scratch/` and can't tell what's authoritative

## Goals

### Must have (M)

- **M1** — Single-rule gitignore for ephemeral content: `.meta/drafts/` and nothing else
- **M2** — Filesystem structure makes the lifecycle state of every artifact unambiguous
- **M3** — One canonical filename format across all artifact types: `<type>-<YYYY-MM-DD>-<slug>.md`
- **M4** — Pre-commit hook rejects any file in `active/` or `archive/` that doesn't match the convention
- **M5** — `meta_visibility` copier parameter: binary `public` (default) / `private`
- **M6** — Every currently-tracked file in `scratch/` and `references/` is triaged and relocated to its correct destination — nothing gets lost
- **M7** — External visitor can answer "what's alive in this project right now?" in one click (`.meta/active/`)
- **M8** — `git mv` is the lifecycle transition mechanism — state change = file move = reviewable commit

### Should have (S)

- **S1** — GUIDELINES.md documents the convention (types, states, naming)
- **S2** — PILOT.md `scratch/` index section removed or reworked
- **S3** — References tiering (`raw/interim/synthesis/`) reuses the existing `data/` vocabulary of this repo for internal consistency

### Won't have (W)

- **W1** — `trash/` directory — YAGNI, drafts/ covers the use case
- **W2** — Nested state-within-type or type-within-state hierarchies — over-engineering
- **W3** — YAML frontmatter status field — the directory IS the source of truth
- **W4** — Scaffolding skill (`/new plan <topic>`) — deferred until manual creation becomes painful
- **W5** — Automatic promotion based on git events — manual `git mv` is explicit and clear
- **W6** — A third `default` mode distinct from `public` — the convention is designed so default = public makes sense

---

## Design

### Directory structure

```
.meta/
├── active/                          # validated artifacts, not yet superseded
│   ├── spec-2026-04-11-meta-taxonomy.md
│   ├── plan-2026-04-11-workflow-gates.md
│   └── ...
├── archive/                         # implemented / historical artifacts
│   ├── plan-2026-03-15-mvp-phase-a.md
│   ├── debate-2026-04-08-meta-visibility.md
│   ├── session-2026-04-09-l-etudiant.md
│   └── ...
├── drafts/                          # WIP, gitignored
│   └── .gitkeep
├── decisions/                       # ADRs (reste tel quel, déjà bien organisé)
│   ├── adr-001-*.md
│   └── ...
├── references/                      # research — hors cycle de vie
│   ├── raw/                         # dump brut, non trié
│   ├── interim/                     # notes, digest partiel
│   ├── synthesis/                   # synthèse canonique citable
│   └── .gitkeep (dans chaque sous-dossier vide)
├── PILOT.md                         # dashboard — public
├── SESSION-CONTEXT.md                # living context — public
├── ARCHITECTURE.md                   # architecture snapshot — public
├── DECISIONS.md                      # ADR journal — public
└── GUIDELINES.md                     # advisory practices — public
```

**Removed:** `.meta/scratch/`, `.meta/sessions/`, `.meta/debates/` as standalone top-level dirs — their contents merge into `archive/` with the new naming convention. `scratch/` disappears entirely after migration.

### Filename convention

**Format:** `<type>-<YYYY-MM-DD>-<kebab-slug>.md`

**Types:**
- `spec` — formalized requirements (MoSCoW)
- `plan` — implementation plan
- `brainstorm` — structured exploration
- `debate` — adversarial debate record
- `session` — session archive

**Date:** creation date for `active/`; preserved (NOT rewritten) when moved to `archive/`.

**Slug:** kebab-case, ≤ 40 chars, derived from the artifact's subject.

**Examples:**
- `spec-2026-04-11-meta-taxonomy.md` (this file)
- `plan-2026-04-11-workflow-gates.md`
- `debate-2026-04-08-meta-visibility.md`
- `session-2026-04-09-l-etudiant.md`

### Lifecycle transitions

| From | To | Trigger | Command |
|------|----|---------|---------|
| (new) | `drafts/` | start WIP | create file in drafts/ |
| `drafts/` | `active/` | validation | `git mv drafts/X active/<type>-<date>-<slug>.md` |
| `active/` | `archive/` | implemented / superseded | `git mv active/X archive/X` (preserve filename) |
| (external) | `references/raw/` | new research source | `cp` into raw/ |
| `references/raw/` | `references/interim/` | notes taken | `git mv` |
| `references/interim/` | `references/synthesis/` | canonical synthesis written | `git mv` |

### Gitignore

Single rule in both the root `.gitignore` (meta-repo) and `template/.gitignore.jinja` (generated projects in `public` mode):

```
# Meta protocol — ephemeral drafts
.meta/drafts/*
!.meta/drafts/.gitkeep
```

In `private` mode (template only): `.meta/` entirely gitignored.

### Enforcement: pre-commit hook

A local Python script `scripts/check_meta_naming.py` registered in `.pre-commit-config.yaml`:

- Scans staged files under `.meta/active/` and `.meta/archive/`
- For each, validates the filename matches `^(spec|plan|brainstorm|debate|session)-\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$`
- Also allows non-artifact files that already live there (e.g., `.gitkeep`)
- Rejects the commit with a clear error message if a violation is found
- Does NOT run on `drafts/` or `references/` (those have no enforcement)

The hook lives both in this repo (meta-repo dogfood) AND in the template (`template/scripts/` + `template/.pre-commit-config.yaml`) so generated projects inherit it.

### meta_visibility copier parameter (binary)

```yaml
meta_visibility:
  type: str
  help: "How visible should .meta/ be in git? (public = commit everything except drafts; private = gitignore entire .meta/)"
  choices:
    - public
    - private
  default: public
```

**`template/.gitignore.jinja`:**

```jinja
# Meta protocol
{%- if meta_visibility == "private" %}
.meta/
{%- else %}
.meta/drafts/*
!.meta/drafts/.gitkeep
{%- endif %}
```

---

## Migration plan (this repo)

### Phase A — Triage file (user-validated)

1. Generate `.meta/drafts/migration-triage.md` (gitignored, local-only) with a full table of every currently-tracked file in `scratch/` and `references/`:

```markdown
| File | Type | State | Destination | Rename to | Notes |
|------|------|-------|-------------|-----------|-------|
| .meta/scratch/spec-workflow-gates.md | spec | validated | active/ | spec-2026-04-08-workflow-gates.md | already implemented today, consider archive |
| .meta/scratch/plan-workflow-gates.md | plan | implemented | archive/ | plan-2026-04-10-workflow-gates.md | |
| .meta/scratch/launch-plan.md | plan | validated | active/ | plan-2026-04-08-launch.md | large, still in use |
| .meta/scratch/mvp-phase-a-plan.md | plan | implemented | archive/ | plan-2026-04-03-mvp-phase-a.md | |
| ... | | | | | |
| .meta/references/gstack-skill-pack.md | reference | synthesis | references/synthesis/ | gstack-skill-pack.md | cited in PILOT |
| .meta/references/skill-design-sources.md | reference | synthesis | references/synthesis/ | skill-design-sources.md | cited in PILOT |
| .meta/references/claude-code-leak-analysis.md | reference | raw | references/raw/ | claude-code-leak-analysis.md | |
| ... | | | | | |
```

2. User reviews the table, edits disputed rows, validates.

### Phase B — Execute moves (grouped commits)

1. Create new directories: `active/`, `archive/`, `drafts/`, `references/{raw,interim,synthesis}/` with `.gitkeep` files
2. Commit 1 — promotes to `active/`
3. Commit 2 — promotes to `archive/` (including renamed debates and sessions)
4. Commit 3 — references triage (promotes to `raw/`, `interim/`, `synthesis/`)
5. Commit 4 — `git rm` for files the user decided to drop entirely
6. Commit 5 — delete now-empty `scratch/`, `sessions/`, `debates/` directories

### Phase C — Convention enforcement

1. Add `scripts/check_meta_naming.py`
2. Register in `.pre-commit-config.yaml`
3. Test: create a malformed filename in `active/`, verify hook rejects

### Phase D — Template propagation

1. Mirror the directory structure in `template/.meta/` (empty dirs with `.gitkeep`)
2. Add `meta_visibility` to `copier.yml` (binary public/private)
3. Update `template/.gitignore.jinja` with the conditional
4. Propagate `check_meta_naming.py` to `template/scripts/`
5. Update `template/.pre-commit-config.yaml`
6. Update `template/.meta/GUIDELINES.md.jinja` with taxonomy section

### Phase E — Documentation alignment

1. Update `.meta/PILOT.md` — rewrite "Scratch files" section to reference the new structure, mark 0.2/0.3 as DONE
2. Update `CLAUDE.md` (meta-repo) — add taxonomy rule
3. Update `template/CLAUDE.md.jinja` — same rule for generated projects
4. Update `.meta/GUIDELINES.md.jinja` template — document the convention for users

### Phase F — Acceptance

1. `copier copy . /tmp/taxo-pub --defaults --trust --vcs-ref=HEAD` — verify public mode
2. `copier copy . /tmp/taxo-priv --data meta_visibility=private --defaults --trust --vcs-ref=HEAD` — verify private mode
3. `uv run pre-commit run --all-files` on meta-repo — verify enforcement
4. `git ls-files .meta/scratch/` — expect empty (dir no longer exists)
5. `git ls-files .meta/active/` — expect at least the specs the user promoted
6. `uv run ruff check .` — green

---

## Files to modify / create

| File | Action |
|------|--------|
| `.gitignore` (meta-repo root) | Add `.meta/drafts/*` rule |
| `scripts/check_meta_naming.py` | **CREATE** — pre-commit filename validator |
| `.pre-commit-config.yaml` (meta-repo) | Register the new hook |
| `.meta/active/`, `.meta/archive/`, `.meta/drafts/`, `.meta/references/{raw,interim,synthesis}/` | **CREATE** with `.gitkeep` |
| 14 files in `.meta/scratch/` | Triage & relocate per user-validated table |
| 22 files in `.meta/references/` | Triage & relocate to `raw/`/`interim/`/`synthesis/` |
| `.meta/debates/*.md` | Rename with prefix, move to `.meta/archive/` |
| `.meta/scratch/`, `.meta/sessions/`, `.meta/debates/` | Remove (empty dirs) |
| `.meta/PILOT.md` | Update structure section + mark 0.2/0.3 done |
| `copier.yml` | Add `meta_visibility` binary parameter |
| `template/.gitignore.jinja` | Jinja conditional on `meta_visibility` |
| `template/scripts/check_meta_naming.py` | **CREATE** (mirror of meta-repo hook) |
| `template/.pre-commit-config.yaml` | Register the hook |
| `template/.meta/` | Create empty active/, archive/, drafts/, references/* with .gitkeep |
| `template/.meta/GUIDELINES.md.jinja` | Document the taxonomy |
| `template/CLAUDE.md.jinja` | Reference taxonomy in rules |
| `CLAUDE.md` (meta-repo) | Reference taxonomy in rules |

---

## Acceptance criteria

1. `find .meta -type d` returns: `active`, `archive`, `drafts`, `decisions`, `references`, `references/raw`, `references/interim`, `references/synthesis` — plus the root `.meta/`. Nothing else.
2. `git ls-files .meta/scratch/` returns empty — `scratch/` no longer exists
3. Every file in `.meta/active/` and `.meta/archive/` matches the regex `^(spec|plan|brainstorm|debate|session)-\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$`
4. `.gitignore` contains exactly one `.meta/` rule: `.meta/drafts/*` + `!.meta/drafts/.gitkeep`
5. `uv run pre-commit run --all-files` passes
6. `copier copy . /tmp/taxo-pub --defaults --trust --vcs-ref=HEAD` succeeds, generated project has the new structure, `drafts/` is gitignored, everything else committed
7. `copier copy . /tmp/taxo-priv --data meta_visibility=private --defaults --trust --vcs-ref=HEAD` succeeds, entire `.meta/` is gitignored
8. PILOT.md 0.2 and 0.3 marked DONE
9. No file loss — every file that existed before the migration either exists at a new path, is explicitly in `.meta/drafts/` (gitignored but present on disk), or was explicitly deleted by the user via the triage table

---

## Out of scope (future work)

- **Scaffolding skill** `/new <type> <slug>` — defer until manual creation becomes painful
- **Archive index generator** — a script that lists `archive/` contents with dates — defer until archive grows
- **Auto-promotion hooks** (e.g., move plan to archive when all tasks completed) — too magic, manual is clearer
- **References auto-tiering** — suggesting raw→interim→synthesis moves based on usage — defer
- **Retrofitting decisions/ to the date-prefix convention** — ADRs already have their own convention (`adr-NNN-slug.md`), don't disturb

---

## Open questions

None remaining. All decisions taken during the brainstorm+debate:
- ✅ Flat state-outer with filename prefix
- ✅ `trash/` dropped (YAGNI)
- ✅ `meta_visibility` binary public (default) / private
- ✅ References tiered with `raw/interim/synthesis/` (reuses data/ vocabulary)
- ✅ Pre-commit hook enforcement from day 1
- ✅ Migration via triage file in drafts/, user validates, grouped commits
- ✅ Sessions and debates fold into `archive/` with prefix
