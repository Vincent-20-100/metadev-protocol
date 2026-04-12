---
type: plan
date: 2026-04-11
slug: meta-taxonomy
status: active
---

# `.meta/` Taxonomy Migration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate `.meta/` from the broken scratch/references/debates/sessions/gold layout to the flat state-outer taxonomy defined in `spec-2026-04-11-meta-taxonomy.md`, and propagate the convention to the Copier template.

**Architecture:** Pure file reorganization + one Python pre-commit hook + Jinja template changes. Migration is user-gated at the triage step (Task 2 STOPS for user validation). No code logic — markdown moves, `.gitignore` rules, and a regex validator.

**Tech Stack:** git, Python 3.13 (stdlib only for the hook), pre-commit, Copier, Jinja2.

**Source spec:** `.meta/active/spec-2026-04-11-meta-taxonomy.md`
**Source debate:** `.meta/debates/debate-meta-taxonomy.md`
**Branch:** `feat/phase-0` (do NOT merge to main until the end of Phase 0)
**PILOT tasks driven:** 0.2 (meta_visibility), 0.3 (.meta/ gitignore alignment)

---

## File Structure

New top-level layout (after migration):

| Path | Responsibility |
|------|----------------|
| `.meta/active/` | Validated artifacts, not yet implemented / still referenced |
| `.meta/archive/` | Implemented or historical artifacts (absorbs old `scratch/` archives, `debates/`, `sessions/`) |
| `.meta/drafts/` | WIP — gitignored, only `.gitkeep` committed |
| `.meta/decisions/` | ADRs — **unchanged**, keep existing `adr-NNN-slug.md` convention |
| `.meta/references/raw/` | Untriaged research dumps |
| `.meta/references/interim/` | Partial notes / digests |
| `.meta/references/synthesis/` | Canonical, citable synthesis (absorbs old `gold/`) |
| `.meta/PILOT.md` | Dashboard — unchanged |
| `.meta/SESSION-CONTEXT.md` | Living context — unchanged |
| `.meta/ARCHITECTURE.md` | Architecture snapshot — unchanged |
| `.meta/DECISIONS.md` | ADR journal — unchanged |
| `.meta/GUIDELINES.md` | Advisory practices — (created by this plan if missing) |

Files to **remove** after migration: `.meta/scratch/`, `.meta/debates/`, `.meta/sessions/`, `.meta/gold/`.

New tooling files:

| Path | Responsibility |
|------|----------------|
| `scripts/check_meta_naming.py` | Pre-commit validator: enforces `<type>-<YYYY-MM-DD>-<slug>.md` in `active/` + `archive/` |
| `template/scripts/check_meta_naming.py` | Mirror — propagated to generated projects |

Files to modify:

| Path | Change |
|------|--------|
| `.gitignore` (meta-repo root) | Add `.meta/drafts/*` + `!.meta/drafts/.gitkeep` |
| `.pre-commit-config.yaml` (meta-repo) | Register `check_meta_naming` hook |
| `copier.yml` | Add `meta_visibility` binary parameter (public / private) |
| `template/.gitignore.jinja` | Jinja conditional on `meta_visibility` |
| `template/.pre-commit-config.yaml` | Register `check_meta_naming` hook |
| `template/.meta/GUIDELINES.md.jinja` | Add taxonomy section |
| `template/CLAUDE.md.jinja` | Reference taxonomy rule |
| `CLAUDE.md` (meta-repo) | Reference taxonomy rule + update architecture diagram |
| `.meta/PILOT.md` | Replace scratch index with new structure notes; mark 0.2 + 0.3 DONE |

---

## Known inventory (snapshot taken 2026-04-11)

**`.meta/scratch/` (13 tracked files):**
- `adr-008-implementation-plan.md`
- `adr-009-brainstorm.md`
- `debate-skill-v1-spec.md`
- `debate-v2-plan.md`
- `launch-plan.md`
- `mvp-phase-a-plan.md`
- `mvp-phase-a-spec.md`
- `plan-rodin-agent.md`
- `plan-spec-skill.md`
- `spec-workflow-gates.md`
- `v2-architecture-separation.md`
- `v2-part1-spec.md`
- `v2-part2-brainstorm.md`
- `v2-roadmap.md`

**`.meta/debates/` (4 files):**
- `debate-commit-strategy.md`
- `debate-git-history.md`
- `debate-meta-visibility.md`
- `debate-workflow-gates.md`

**`.meta/references/` (22 files):** `audit-egovault.md`, `claude-code-docs-audit.md`, `claude-code-ecosystem-54-resources.md`, `claude-code-hooks-skills-reference.md`, `claude-code-leak-analysis.md`, `claude-code-security-deepdive.md`, `claude-code-undercover-mode.md`, `context-management-patterns.md`, `dev-workflow-skills-patterns.md`, `ecosystem-54-triage.md`, `ecosystem-deep-dive.md`, `github-skills-landscape.md`, `gstack-skill-pack.md`, `hermes-agent-nous-research.md`, `linkedin-curated-posts.md`, `python-templating-best-practices.md`, `skill-design-sources.md`, `sota-mcp-patterns.md`, `state-of-the-art-vibe-coding.md`, `superpowers-and-everything-claude-code.md`, `top-repos-and-voices.md`, `watchlist.md`

**`.meta/gold/` (5 files):** `claude-code-architecture.md`, `context-management.md`, `python-dev-and-templating.md`, `skills-workflow-and-utilities.md`, `vibe-coding-practices.md`

**`.meta/sessions/`:** to verify at Task 1 (none tracked in git at snapshot time, but directory exists).

**Already in `.meta/active/` (created in prior session, pending this migration to validate):**
- `spec-2026-04-11-meta-taxonomy.md`
- `plan-2026-04-11-meta-taxonomy.md` (this file)

Both will be committed in Task 1.

---

## Task 1: Create directory skeleton + commit the taxonomy spec/plan

**Files:**
- Create: `.meta/active/.gitkeep`
- Create: `.meta/archive/.gitkeep`
- Create: `.meta/drafts/.gitkeep`
- Create: `.meta/references/raw/.gitkeep`
- Create: `.meta/references/interim/.gitkeep`
- Create: `.meta/references/synthesis/.gitkeep`

- [ ] **Step 1: Verify current branch is `feat/phase-0`**

```bash
cd C:/Users/Vincent/GitHub/Vincent-20-100/metadev-protocol && git rev-parse --abbrev-ref HEAD
```
Expected: `feat/phase-0`. If not, STOP and ask user.

- [ ] **Step 2: Create the directory skeleton**

```bash
cd C:/Users/Vincent/GitHub/Vincent-20-100/metadev-protocol
mkdir -p .meta/active .meta/archive .meta/drafts .meta/references/raw .meta/references/interim .meta/references/synthesis
touch .meta/active/.gitkeep .meta/archive/.gitkeep .meta/drafts/.gitkeep .meta/references/raw/.gitkeep .meta/references/interim/.gitkeep .meta/references/synthesis/.gitkeep
```

- [ ] **Step 3: Verify directory layout**

```bash
find .meta -maxdepth 2 -type d | sort
```
Expected (order may vary): `.meta`, `.meta/active`, `.meta/archive`, `.meta/debates`, `.meta/decisions`, `.meta/drafts`, `.meta/gold`, `.meta/references`, `.meta/references/interim`, `.meta/references/raw`, `.meta/references/synthesis`, `.meta/scratch`, `.meta/sessions`.

- [ ] **Step 4: Stage skeleton + the spec + the plan (already on disk in active/)**

```bash
git add .meta/active/.gitkeep .meta/archive/.gitkeep .meta/drafts/.gitkeep .meta/references/raw/.gitkeep .meta/references/interim/.gitkeep .meta/references/synthesis/.gitkeep .meta/active/spec-2026-04-11-meta-taxonomy.md .meta/active/plan-2026-04-11-meta-taxonomy.md .meta/debates/debate-meta-taxonomy.md
git status --short
```
Expected: all 9 paths above shown as `A` (added) or `??` → staged.

- [ ] **Step 5: Commit**

```bash
git commit -m "chore(meta): bootstrap taxonomy skeleton + commit spec/plan/debate"
```

---

## Task 2: Generate triage table in drafts/ and STOP for user validation

**Files:**
- Create: `.meta/drafts/migration-triage.md`

**⚠️ USER-GATED TASK — do NOT proceed to Task 3 without explicit user approval of the triage table.**

- [ ] **Step 1: Create the triage file with a pre-filled proposal**

Write the following content to `.meta/drafts/migration-triage.md` (this file lives in `drafts/` so it is gitignored after Task 8; for now it is tracked because the ignore rule is not yet in place — that's fine, it will be removed at the end).

```markdown
# Migration Triage — `.meta/` taxonomy

**Instructions for user:** review each row, edit the `Destination` or `Action` column if needed,
then tell the implementer "triage approved" (or list the rows you changed).

Legend:
- **Destination**: `active` (validated, still live) / `archive` (implemented/historical) / `drop` (git rm)
- **Rename**: new filename under the destination
- **Keep date**: preserved from first commit of the file unless noted

## `.meta/scratch/` → ?

| # | Current path | Destination | Rename to | Notes |
|---|-------------|-------------|-----------|-------|
| 1 | scratch/adr-008-implementation-plan.md | archive | plan-2026-03-20-adr-008-settings-v2.md | implemented |
| 2 | scratch/adr-009-brainstorm.md | archive | brainstorm-2026-03-22-universal-architecture.md | ADR-009 landed |
| 3 | scratch/debate-skill-v1-spec.md | archive | spec-2026-03-25-debate-skill-v1.md | superseded by v2 |
| 4 | scratch/debate-v2-plan.md | archive | plan-2026-04-01-debate-skill-v2.md | implemented |
| 5 | scratch/launch-plan.md | active | plan-2026-04-08-launch.md | still in use |
| 6 | scratch/mvp-phase-a-plan.md | archive | plan-2026-03-15-mvp-phase-a.md | done |
| 7 | scratch/mvp-phase-a-spec.md | archive | spec-2026-03-15-mvp-phase-a.md | done |
| 8 | scratch/plan-rodin-agent.md | archive | plan-2026-04-08-rodin-agent.md | folded into workflow-gates |
| 9 | scratch/plan-spec-skill.md | archive | plan-2026-04-02-spec-skill.md | implemented |
| 10 | scratch/spec-workflow-gates.md | archive | spec-2026-04-08-workflow-gates.md | implemented in 0.1 |
| 11 | scratch/v2-architecture-separation.md | archive | brainstorm-2026-03-28-v2-architecture.md | conceptual |
| 12 | scratch/v2-part1-spec.md | archive | spec-2026-03-30-v2-superpowers.md | implemented |
| 13 | scratch/v2-part2-brainstorm.md | archive | brainstorm-2026-03-30-v2-knowledge.md | exploratory |
| 14 | scratch/v2-roadmap.md | archive | plan-2026-03-28-v2-roadmap.md | superseded |

## `.meta/debates/` → archive/ (all get `debate-` prefix + date)

| # | Current path | Destination | Rename to | Notes |
|---|-------------|-------------|-----------|-------|
| 15 | debates/debate-commit-strategy.md | archive | debate-2026-04-08-commit-strategy.md | |
| 16 | debates/debate-git-history.md | archive | debate-2026-04-08-git-history.md | |
| 17 | debates/debate-meta-visibility.md | archive | debate-2026-04-08-meta-visibility.md | |
| 18 | debates/debate-workflow-gates.md | archive | debate-2026-04-08-workflow-gates.md | |

Note: `debates/debate-meta-taxonomy.md` was already moved to archive location via Task 1? NO — it stays in `.meta/debates/` until Task 4. Add row 18.5:

| 18.5 | debates/debate-meta-taxonomy.md | archive | debate-2026-04-11-meta-taxonomy.md | |

## `.meta/gold/` → references/synthesis/

| # | Current path | Destination | Rename to | Notes |
|---|-------------|-------------|-----------|-------|
| 19 | gold/claude-code-architecture.md | references/synthesis | claude-code-architecture.md | keep name |
| 20 | gold/context-management.md | references/synthesis | context-management.md | |
| 21 | gold/python-dev-and-templating.md | references/synthesis | python-dev-and-templating.md | |
| 22 | gold/skills-workflow-and-utilities.md | references/synthesis | skills-workflow-and-utilities.md | |
| 23 | gold/vibe-coding-practices.md | references/synthesis | vibe-coding-practices.md | |

## `.meta/references/` → references/{raw,interim,synthesis}/

Default proposal: all raw research → `raw/`; cited-in-PILOT files → `synthesis/`.
User may override per-file.

| # | Current path | Destination | Notes |
|---|-------------|-------------|-------|
| 24 | references/audit-egovault.md | raw | project-specific audit |
| 25 | references/claude-code-docs-audit.md | raw | |
| 26 | references/claude-code-ecosystem-54-resources.md | raw | |
| 27 | references/claude-code-hooks-skills-reference.md | interim | partial digest |
| 28 | references/claude-code-leak-analysis.md | raw | |
| 29 | references/claude-code-security-deepdive.md | raw | |
| 30 | references/claude-code-undercover-mode.md | raw | |
| 31 | references/context-management-patterns.md | interim | |
| 32 | references/dev-workflow-skills-patterns.md | interim | |
| 33 | references/ecosystem-54-triage.md | interim | digest |
| 34 | references/ecosystem-deep-dive.md | raw | |
| 35 | references/github-skills-landscape.md | raw | |
| 36 | references/gstack-skill-pack.md | synthesis | cited in PILOT |
| 37 | references/hermes-agent-nous-research.md | raw | |
| 38 | references/linkedin-curated-posts.md | raw | |
| 39 | references/python-templating-best-practices.md | interim | |
| 40 | references/skill-design-sources.md | synthesis | cited in PILOT |
| 41 | references/sota-mcp-patterns.md | raw | |
| 42 | references/state-of-the-art-vibe-coding.md | raw | |
| 43 | references/superpowers-and-everything-claude-code.md | raw | |
| 44 | references/top-repos-and-voices.md | raw | |
| 45 | references/watchlist.md | raw | |

## Drops (if any)

None proposed by default. User may mark rows above as `drop` to `git rm` them instead.
```

- [ ] **Step 2: Commit the triage file (tracked for now — gitignore rule comes later)**

```bash
git add .meta/drafts/migration-triage.md
git commit -m "chore(meta): propose migration triage for user validation"
```

- [ ] **Step 3: STOP and report to the user**

Report verbatim:

```
Triage table written to .meta/drafts/migration-triage.md (45 files).

STOPPED — waiting for user validation before any file move.

Please:
1. Open .meta/drafts/migration-triage.md
2. Edit any row where you disagree with Destination / Rename to / Action
3. Reply "triage approved" or list the rows you changed

No git mv will happen until you confirm.
```

**DO NOT proceed to Task 3 without the user's explicit approval.**

---

## Task 3: Execute promotes to `.meta/active/`

**Files:** depends on user-approved triage (default: row 5 — `launch-plan.md`).

- [ ] **Step 1: Re-read the user-validated triage file**

```bash
cat .meta/drafts/migration-triage.md
```

For each row with `Destination == active`, run:

- [ ] **Step 2: `git mv` each approved `active` row**

For the default row 5:
```bash
git mv .meta/scratch/launch-plan.md .meta/active/plan-2026-04-08-launch.md
```

(Apply the same pattern to every other `active` row the user approved. One `git mv` per row.)

- [ ] **Step 3: Verify moves**

```bash
git status --short | grep "^R"
```
Expected: one `R  old -> new` line per approved row.

- [ ] **Step 4: Commit**

```bash
git commit -m "chore(meta): promote validated artifacts to active/"
```

---

## Task 4: Execute promotes to `.meta/archive/`

**Files:** all rows with `Destination == archive` from the triage + all 4 `debates/` files + `debate-meta-taxonomy.md`.

- [ ] **Step 1: `git mv` each approved archive row from scratch/**

Example for rows 1–14 with archive destination (minus row 5 already moved):
```bash
git mv .meta/scratch/adr-008-implementation-plan.md .meta/archive/plan-2026-03-20-adr-008-settings-v2.md
git mv .meta/scratch/adr-009-brainstorm.md .meta/archive/brainstorm-2026-03-22-universal-architecture.md
git mv .meta/scratch/debate-skill-v1-spec.md .meta/archive/spec-2026-03-25-debate-skill-v1.md
git mv .meta/scratch/debate-v2-plan.md .meta/archive/plan-2026-04-01-debate-skill-v2.md
git mv .meta/scratch/mvp-phase-a-plan.md .meta/archive/plan-2026-03-15-mvp-phase-a.md
git mv .meta/scratch/mvp-phase-a-spec.md .meta/archive/spec-2026-03-15-mvp-phase-a.md
git mv .meta/scratch/plan-rodin-agent.md .meta/archive/plan-2026-04-08-rodin-agent.md
git mv .meta/scratch/plan-spec-skill.md .meta/archive/plan-2026-04-02-spec-skill.md
git mv .meta/scratch/spec-workflow-gates.md .meta/archive/spec-2026-04-08-workflow-gates.md
git mv .meta/scratch/v2-architecture-separation.md .meta/archive/brainstorm-2026-03-28-v2-architecture.md
git mv .meta/scratch/v2-part1-spec.md .meta/archive/spec-2026-03-30-v2-superpowers.md
git mv .meta/scratch/v2-part2-brainstorm.md .meta/archive/brainstorm-2026-03-30-v2-knowledge.md
git mv .meta/scratch/v2-roadmap.md .meta/archive/plan-2026-03-28-v2-roadmap.md
```

(Substitute user-edited rows as needed.)

- [ ] **Step 2: `git mv` the 4 pre-existing debates to archive/ with prefix rename**

```bash
git mv .meta/debates/debate-commit-strategy.md .meta/archive/debate-2026-04-08-commit-strategy.md
git mv .meta/debates/debate-git-history.md .meta/archive/debate-2026-04-08-git-history.md
git mv .meta/debates/debate-meta-visibility.md .meta/archive/debate-2026-04-08-meta-visibility.md
git mv .meta/debates/debate-workflow-gates.md .meta/archive/debate-2026-04-08-workflow-gates.md
git mv .meta/debates/debate-meta-taxonomy.md .meta/archive/debate-2026-04-11-meta-taxonomy.md
```

- [ ] **Step 3: If `.meta/sessions/` contains any tracked files, move them**

```bash
git ls-files .meta/sessions/
```
If output is non-empty: for each file, `git mv` it to `.meta/archive/session-<YYYY-MM-DD>-<slug>.md` (pick the date from the file's first commit with `git log --diff-filter=A --format=%ad --date=short -- <file> | tail -1`).

If output is empty: skip.

- [ ] **Step 4: Verify**

```bash
git status --short | grep "^R" | wc -l
```
Expected: ≥ 18 renames (13 scratch archives + 5 debates + any sessions).

- [ ] **Step 5: Commit**

```bash
git commit -m "chore(meta): archive historical plans, specs, debates, sessions"
```

---

## Task 5: Migrate `.meta/gold/` and `.meta/references/`

**Files:** all 5 gold/ files + all 22 references/ files, per user-approved triage.

- [ ] **Step 1: Move gold/ files to references/synthesis/**

```bash
git mv .meta/gold/claude-code-architecture.md .meta/references/synthesis/claude-code-architecture.md
git mv .meta/gold/context-management.md .meta/references/synthesis/context-management.md
git mv .meta/gold/python-dev-and-templating.md .meta/references/synthesis/python-dev-and-templating.md
git mv .meta/gold/skills-workflow-and-utilities.md .meta/references/synthesis/skills-workflow-and-utilities.md
git mv .meta/gold/vibe-coding-practices.md .meta/references/synthesis/vibe-coding-practices.md
```

- [ ] **Step 2: Move references/ files to their approved tier**

For the default proposal (rows 24–45), execute in three batches:

**Synthesis (cited in PILOT):**
```bash
git mv .meta/references/gstack-skill-pack.md .meta/references/synthesis/gstack-skill-pack.md
git mv .meta/references/skill-design-sources.md .meta/references/synthesis/skill-design-sources.md
```

**Interim (digests/partial notes):**
```bash
git mv .meta/references/claude-code-hooks-skills-reference.md .meta/references/interim/claude-code-hooks-skills-reference.md
git mv .meta/references/context-management-patterns.md .meta/references/interim/context-management-patterns.md
git mv .meta/references/dev-workflow-skills-patterns.md .meta/references/interim/dev-workflow-skills-patterns.md
git mv .meta/references/ecosystem-54-triage.md .meta/references/interim/ecosystem-54-triage.md
git mv .meta/references/python-templating-best-practices.md .meta/references/interim/python-templating-best-practices.md
```

**Raw (everything else):**
```bash
git mv .meta/references/audit-egovault.md .meta/references/raw/audit-egovault.md
git mv .meta/references/claude-code-docs-audit.md .meta/references/raw/claude-code-docs-audit.md
git mv .meta/references/claude-code-ecosystem-54-resources.md .meta/references/raw/claude-code-ecosystem-54-resources.md
git mv .meta/references/claude-code-leak-analysis.md .meta/references/raw/claude-code-leak-analysis.md
git mv .meta/references/claude-code-security-deepdive.md .meta/references/raw/claude-code-security-deepdive.md
git mv .meta/references/claude-code-undercover-mode.md .meta/references/raw/claude-code-undercover-mode.md
git mv .meta/references/ecosystem-deep-dive.md .meta/references/raw/ecosystem-deep-dive.md
git mv .meta/references/github-skills-landscape.md .meta/references/raw/github-skills-landscape.md
git mv .meta/references/hermes-agent-nous-research.md .meta/references/raw/hermes-agent-nous-research.md
git mv .meta/references/linkedin-curated-posts.md .meta/references/raw/linkedin-curated-posts.md
git mv .meta/references/sota-mcp-patterns.md .meta/references/raw/sota-mcp-patterns.md
git mv .meta/references/state-of-the-art-vibe-coding.md .meta/references/raw/state-of-the-art-vibe-coding.md
git mv .meta/references/superpowers-and-everything-claude-code.md .meta/references/raw/superpowers-and-everything-claude-code.md
git mv .meta/references/top-repos-and-voices.md .meta/references/raw/top-repos-and-voices.md
git mv .meta/references/watchlist.md .meta/references/raw/watchlist.md
```

(Substitute any user edits.)

- [ ] **Step 3: Verify references/ and gold/ are empty**

```bash
git ls-files .meta/gold/ .meta/references/ | grep -v '^\.meta/references/\(raw\|interim\|synthesis\)/'
```
Expected: empty output (no leftover files at the old paths).

- [ ] **Step 4: Commit**

```bash
git commit -m "chore(meta): tier references into raw/interim/synthesis (absorbs gold/)"
```

---

## Task 6: Drop any files the user marked `drop`

**Files:** only rows the user explicitly marked `Destination == drop` in the triage.

- [ ] **Step 1: Check if any drops exist**

```bash
grep -i "drop" .meta/drafts/migration-triage.md || echo "no drops"
```

If "no drops": skip to Step 4.

- [ ] **Step 2: For each drop row, `git rm` the file**

```bash
git rm .meta/<path-from-triage>
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore(meta): drop obsolete artifacts per user triage"
```

- [ ] **Step 4: (no drops path) — continue**

---

## Task 7: Delete the now-empty legacy directories

**Files:**
- Delete: `.meta/scratch/`, `.meta/debates/`, `.meta/sessions/`, `.meta/gold/`

- [ ] **Step 1: Verify each is empty of tracked files**

```bash
for d in scratch debates sessions gold; do
  n=$(git ls-files .meta/$d/ | wc -l)
  echo "$d: $n tracked"
done
```
Expected: all four report `0 tracked`.

If any is non-zero: STOP, investigate, re-run Task 4 or Task 5.

- [ ] **Step 2: Remove on-disk .gitkeep files (if any) and empty dirs**

```bash
rm -f .meta/scratch/.gitkeep .meta/debates/.gitkeep .meta/sessions/.gitkeep .meta/gold/.gitkeep
rmdir .meta/scratch .meta/debates .meta/sessions .meta/gold 2>/dev/null || true
# If rmdir fails, list leftover contents:
ls -la .meta/scratch .meta/debates .meta/sessions .meta/gold 2>/dev/null
```

If any directory still has on-disk untracked files, STOP and report to user.

- [ ] **Step 3: Stage any .gitkeep deletions**

```bash
git add -u .meta/
git status --short
```

- [ ] **Step 4: Commit**

```bash
git commit -m "chore(meta): remove legacy scratch/debates/sessions/gold directories"
```
(If nothing is staged at this step — i.e., no `.gitkeep` was tracked — skip the commit.)

---

## Task 8: Add gitignore rule for `.meta/drafts/` in meta-repo root

**Files:**
- Modify: `.gitignore` (root of metadev-protocol)

- [ ] **Step 1: Append the rule**

old_string:
```
# Build artifacts and cache
.venv/
.env
__pycache__/
```

new_string:
```
# Build artifacts and cache
.venv/
.env
__pycache__/

# Meta protocol — ephemeral drafts
.meta/drafts/*
!.meta/drafts/.gitkeep
```

- [ ] **Step 2: Verify the migration-triage.md is now ignored**

```bash
cd C:/Users/Vincent/GitHub/Vincent-20-100/metadev-protocol
git check-ignore .meta/drafts/migration-triage.md
```
Expected: prints `.meta/drafts/migration-triage.md` (meaning: matched by an ignore rule).

- [ ] **Step 3: Untrack the triage file (keep on disk)**

```bash
git rm --cached .meta/drafts/migration-triage.md
```

- [ ] **Step 4: Verify `.gitkeep` still tracked**

```bash
git ls-files .meta/drafts/
```
Expected: `.meta/drafts/.gitkeep` (and nothing else).

- [ ] **Step 5: Commit**

```bash
git add .gitignore .meta/drafts/migration-triage.md 2>/dev/null
git commit -m "chore: gitignore .meta/drafts/ and untrack migration triage"
```

---

## Task 9: Create the pre-commit naming hook (meta-repo)

**Files:**
- Create: `scripts/check_meta_naming.py`
- Create: `scripts/__init__.py` (if scripts/ doesn't exist)

- [ ] **Step 1: Check whether `scripts/` exists**

```bash
ls scripts/ 2>/dev/null || mkdir scripts
```

- [ ] **Step 2: Write the hook**

Create `scripts/check_meta_naming.py` with the following content:

```python
#!/usr/bin/env python3
"""Pre-commit hook: enforce .meta/ filename taxonomy.

Validates that every staged file under .meta/active/ or .meta/archive/
matches the canonical pattern:

    <type>-<YYYY-MM-DD>-<kebab-slug>.md

Allowed types: spec, plan, brainstorm, debate, session.
Exempt filenames: .gitkeep (so empty dir markers remain valid).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r"^(spec|plan|brainstorm|debate|session)-\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$"
)
EXEMPT = {".gitkeep"}
GUARDED_DIRS = ("active", "archive")


def is_guarded(path: Path) -> bool:
    parts = path.parts
    return (
        len(parts) >= 3
        and parts[0] == ".meta"
        and parts[1] in GUARDED_DIRS
    )


def check(paths: list[str]) -> int:
    errors: list[str] = []
    for raw in paths:
        p = Path(raw)
        if not is_guarded(p):
            continue
        name = p.name
        if name in EXEMPT:
            continue
        if not PATTERN.match(name):
            errors.append(
                f"  {raw}\n"
                f"    expected: <type>-<YYYY-MM-DD>-<slug>.md "
                f"(type ∈ spec|plan|brainstorm|debate|session)"
            )
    if errors:
        print(
            "check_meta_naming: invalid filename(s) under .meta/active/ "
            "or .meta/archive/:",
            file=sys.stderr,
        )
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1:]))
```

- [ ] **Step 3: Make it executable (noop on Windows, still safe)**

```bash
chmod +x scripts/check_meta_naming.py 2>/dev/null || true
```

- [ ] **Step 4: Smoke-test manually**

```bash
uv run python scripts/check_meta_naming.py .meta/active/spec-2026-04-11-meta-taxonomy.md .meta/active/.gitkeep
echo "exit=$?"
```
Expected: `exit=0` (both files valid).

```bash
uv run python scripts/check_meta_naming.py .meta/active/garbage.md
echo "exit=$?"
```
Expected: `exit=1` and an error message about the invalid filename.

- [ ] **Step 5: Commit**

```bash
git add scripts/check_meta_naming.py
git commit -m "feat(meta): add check_meta_naming pre-commit validator"
```

---

## Task 10: Register the hook in `.pre-commit-config.yaml` (meta-repo)

**Files:**
- Modify: `.pre-commit-config.yaml`

- [ ] **Step 1: Append a local hook entry**

old_string:
```
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

new_string:
```
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: check-meta-naming
        name: Check .meta/ filename taxonomy
        entry: python scripts/check_meta_naming.py
        language: system
        files: ^\.meta/(active|archive)/
```

- [ ] **Step 2: Install and run the hook**

```bash
uv run pre-commit install
uv run pre-commit run check-meta-naming --all-files
echo "exit=$?"
```
Expected: `exit=0`, message `Passed` for `Check .meta/ filename taxonomy`.

- [ ] **Step 3: Negative test — create a bad filename and run the hook**

```bash
touch .meta/active/bad-name.md
git add .meta/active/bad-name.md
uv run pre-commit run check-meta-naming --files .meta/active/bad-name.md
echo "exit=$?"
```
Expected: `exit=1`, error mentions `bad-name.md`.

Cleanup:
```bash
git rm -f .meta/active/bad-name.md
rm -f .meta/active/bad-name.md
```

- [ ] **Step 4: Commit**

```bash
git add .pre-commit-config.yaml
git commit -m "chore: register check-meta-naming in pre-commit"
```

---

## Task 11: Add `meta_visibility` parameter to `copier.yml`

**Files:**
- Modify: `copier.yml`

- [ ] **Step 1: Read current copier.yml**

```bash
cat copier.yml
```
Identify the last question before the `_` copier-config block (likely `python_version`).

- [ ] **Step 2: Insert `meta_visibility` after `python_version`**

Use Edit on `copier.yml`. Find the exact lines around `python_version:` and append after them. Example pattern — adapt to the actual file content read in Step 1.

old_string (example — use the real lines from Step 1):
```yaml
python_version:
  type: str
  help: "Minimum Python version"
  default: "3.13"
```

new_string:
```yaml
python_version:
  type: str
  help: "Minimum Python version"
  default: "3.13"

meta_visibility:
  type: str
  help: "How visible should .meta/ be in git? (public = commit everything except drafts; private = gitignore entire .meta/)"
  choices:
    - public
    - private
  default: public
```

- [ ] **Step 3: Verify copier accepts the question**

```bash
rm -rf /tmp/mv-test && copier copy . /tmp/mv-test --defaults --trust --vcs-ref=HEAD
echo "exit=$?"
```
Expected: `exit=0`, no jinja error, `/tmp/mv-test/` generated.

- [ ] **Step 4: Commit**

```bash
git add copier.yml
git commit -m "feat(copier): add meta_visibility binary parameter"
```

---

## Task 12: Make `template/.gitignore.jinja` conditional on `meta_visibility`

**Files:**
- Modify: `template/.gitignore.jinja`

- [ ] **Step 1: Replace the current Meta protocol block**

old_string:
```
# Meta protocol
.meta/scratch/*
!.meta/scratch/.gitkeep
```

new_string:
```
# Meta protocol — controlled by meta_visibility copier parameter
{%- if meta_visibility == "private" %}
.meta/
{%- else %}
.meta/drafts/*
!.meta/drafts/.gitkeep
{%- endif %}
```

- [ ] **Step 2: Verify public mode**

```bash
rm -rf /tmp/mv-pub && copier copy . /tmp/mv-pub --defaults --trust --vcs-ref=HEAD
grep -A2 "Meta protocol" /tmp/mv-pub/.gitignore
```
Expected output contains:
```
.meta/drafts/*
!.meta/drafts/.gitkeep
```
and does NOT contain a bare `.meta/` line.

- [ ] **Step 3: Verify private mode**

```bash
rm -rf /tmp/mv-priv && copier copy . /tmp/mv-priv --defaults --trust --vcs-ref=HEAD --data meta_visibility=private
grep -A2 "Meta protocol" /tmp/mv-priv/.gitignore
```
Expected output contains a bare `.meta/` line.

- [ ] **Step 4: Commit**

```bash
git add template/.gitignore.jinja
git commit -m "feat(template): gate .meta/ visibility by meta_visibility param"
```

---

## Task 13: Mirror the taxonomy skeleton in `template/.meta/`

**Files:**
- Delete: `template/.meta/scratch/` (and its `.gitkeep`)
- Delete: `template/.meta/sessions/` (and its `.gitkeep`)
- Create: `template/.meta/active/.gitkeep`
- Create: `template/.meta/archive/.gitkeep`
- Create: `template/.meta/drafts/.gitkeep`
- Create: `template/.meta/references/raw/.gitkeep`
- Create: `template/.meta/references/interim/.gitkeep`
- Create: `template/.meta/references/synthesis/.gitkeep`

- [ ] **Step 1: Remove the old scratch/sessions skeleton**

```bash
git rm -rf template/.meta/scratch template/.meta/sessions 2>/dev/null || true
```
(If neither was tracked, this is a no-op.)

- [ ] **Step 2: Create new skeleton**

```bash
mkdir -p template/.meta/active template/.meta/archive template/.meta/drafts template/.meta/references/raw template/.meta/references/interim template/.meta/references/synthesis
touch template/.meta/active/.gitkeep template/.meta/archive/.gitkeep template/.meta/drafts/.gitkeep template/.meta/references/raw/.gitkeep template/.meta/references/interim/.gitkeep template/.meta/references/synthesis/.gitkeep
```

- [ ] **Step 3: Verify template generation succeeds in public mode**

```bash
rm -rf /tmp/mv-pub && copier copy . /tmp/mv-pub --defaults --trust --vcs-ref=HEAD
find /tmp/mv-pub/.meta -maxdepth 2 -type d | sort
```
Expected: includes `active`, `archive`, `drafts`, `decisions`, `references/raw`, `references/interim`, `references/synthesis`. Does NOT include `scratch` or `sessions`.

- [ ] **Step 4: Stage and commit**

```bash
git add template/.meta/
git commit -m "feat(template): mirror taxonomy skeleton in template/.meta/"
```

---

## Task 14: Propagate `check_meta_naming.py` to the template

**Files:**
- Create: `template/scripts/check_meta_naming.py`

- [ ] **Step 1: Copy the meta-repo hook verbatim (no jinja templating — it's pure Python)**

```bash
mkdir -p template/scripts
cp scripts/check_meta_naming.py template/scripts/check_meta_naming.py
```

- [ ] **Step 2: Verify it still runs in a generated project**

```bash
rm -rf /tmp/mv-pub && copier copy . /tmp/mv-pub --defaults --trust --vcs-ref=HEAD
uv run python /tmp/mv-pub/scripts/check_meta_naming.py /tmp/mv-pub/.meta/active/.gitkeep
echo "exit=$?"
```
Expected: `exit=0`.

- [ ] **Step 3: Commit**

```bash
git add template/scripts/check_meta_naming.py
git commit -m "feat(template): propagate check_meta_naming hook"
```

---

## Task 15: Register the hook in `template/.pre-commit-config.yaml`

**Files:**
- Modify: `template/.pre-commit-config.yaml`

- [ ] **Step 1: Read the current file**

```bash
cat template/.pre-commit-config.yaml
```

- [ ] **Step 2: Append the local hook entry**

Use Edit. Append `check-meta-naming` as a new `local` repo entry at the end of the `repos:` list, matching the exact structure used in meta-repo Task 10. If a `local` repo already exists, append the hook to its `hooks:` list instead.

Canonical block to add:
```yaml
  - repo: local
    hooks:
      - id: check-meta-naming
        name: Check .meta/ filename taxonomy
        entry: python scripts/check_meta_naming.py
        language: system
        files: ^\.meta/(active|archive)/
```

- [ ] **Step 3: Verify via copier render**

```bash
rm -rf /tmp/mv-pub && copier copy . /tmp/mv-pub --defaults --trust --vcs-ref=HEAD
grep -A4 "check-meta-naming" /tmp/mv-pub/.pre-commit-config.yaml
```
Expected: the hook block is present.

- [ ] **Step 4: Commit**

```bash
git add template/.pre-commit-config.yaml
git commit -m "feat(template): register check-meta-naming pre-commit hook"
```

---

## Task 16: Document the taxonomy in `template/.meta/GUIDELINES.md.jinja`

**Files:**
- Modify: `template/.meta/GUIDELINES.md.jinja`

- [ ] **Step 1: Read current file**

```bash
cat template/.meta/GUIDELINES.md.jinja
```
Note the last stable section to anchor the edit.

- [ ] **Step 2: Append a `.meta/ taxonomy` section at the end of the file**

Append this block (adapt the `old_string` anchor to a real stable line from Step 1):

```markdown

## .meta/ taxonomy

This project was generated with `meta_visibility={{ meta_visibility }}`.

### Directories

| Dir | Purpose |
|-----|---------|
| `active/` | Validated artifacts, not yet implemented or still referenced |
| `archive/` | Implemented or superseded artifacts — chronological memory |
| `drafts/` | Work-in-progress — **gitignored**, safe to throw away |
| `decisions/` | ADRs (`adr-NNN-slug.md`) |
| `references/raw/` | Untriaged external research |
| `references/interim/` | Partial notes and digests |
| `references/synthesis/` | Canonical, citable syntheses |

### Filename convention (enforced by pre-commit)

Every file in `active/` and `archive/` must match:

    <type>-<YYYY-MM-DD>-<kebab-slug>.md

Allowed types: `spec`, `plan`, `brainstorm`, `debate`, `session`.

### Lifecycle

- New WIP → `drafts/<anything>.md` (not tracked)
- Validated → `git mv drafts/X active/<type>-<date>-<slug>.md`
- Implemented/superseded → `git mv active/X archive/X` (keep the filename)

### Visibility modes

| Mode | Committed |
|------|-----------|
| `public` (default) | Everything except `drafts/` |
| `private` | Nothing — entire `.meta/` gitignored |

Change later with `copier update --data meta_visibility=<mode>`.
```

- [ ] **Step 3: Verify**

```bash
rm -rf /tmp/mv-pub && copier copy . /tmp/mv-pub --defaults --trust --vcs-ref=HEAD
grep -c ".meta/ taxonomy" /tmp/mv-pub/.meta/GUIDELINES.md
grep -c "Filename convention" /tmp/mv-pub/.meta/GUIDELINES.md
grep -c "meta_visibility=public" /tmp/mv-pub/.meta/GUIDELINES.md
```
Expected: each returns `1`.

- [ ] **Step 4: Commit**

```bash
git add template/.meta/GUIDELINES.md.jinja
git commit -m "docs(template): document .meta/ taxonomy in GUIDELINES"
```

---

## Task 17: Reference the taxonomy in `template/CLAUDE.md.jinja`

**Files:**
- Modify: `template/CLAUDE.md.jinja`

- [ ] **Step 1: Read current file and find the rules section**

```bash
grep -n "^## Rules\|^1\. \|^2\. \|^3\. " template/CLAUDE.md.jinja | head -20
```

- [ ] **Step 2: Append a new rule under the Rules section**

Find the last numbered rule in the `## Rules` section. Add a new rule after it.

Example — if the last rule is rule N, append:

```markdown
N+1. **`.meta/` taxonomy** — artifacts in `.meta/active/` and `.meta/archive/` must follow `<type>-<YYYY-MM-DD>-<slug>.md` (types: spec, plan, brainstorm, debate, session). WIP lives in `.meta/drafts/` (gitignored). See `.meta/GUIDELINES.md`.
```

Use Edit on `template/CLAUDE.md.jinja`. Anchor the replacement on an existing stable line near the end of the rules list — fetch that line via Step 1's grep output.

- [ ] **Step 3: Verify**

```bash
rm -rf /tmp/mv-pub && copier copy . /tmp/mv-pub --defaults --trust --vcs-ref=HEAD
grep -c ".meta/ taxonomy" /tmp/mv-pub/CLAUDE.md
```
Expected: `≥ 1`.

- [ ] **Step 4: Commit**

```bash
git add template/CLAUDE.md.jinja
git commit -m "docs(template): reference .meta/ taxonomy in CLAUDE.md rules"
```

---

## Task 18: Reference the taxonomy in the meta-repo `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md` (root of metadev-protocol)

- [ ] **Step 1: Update the architecture diagram + rules section**

Find the ASCII tree in the `## Architecture` section. Replace the `.meta/` subtree.

old_string:
```
├── .meta/                       # Development cockpit for THIS repo
│   ├── PILOT.md                 # Current state → READ FIRST
│   ├── ARCHITECTURE.md          # Validated architectural decisions
│   ├── DECISIONS.md             # ADR journal
│   ├── decisions/               # Individual ADRs
│   ├── gold/                    # Synthesized research (source of truth)
│   ├── references/              # Raw research sources (bronze)
│   ├── sessions/                # Past session archives
│   └── scratch/                 # Drafts — never committed (.gitignored)
```

new_string:
```
├── .meta/                       # Development cockpit for THIS repo
│   ├── PILOT.md                 # Current state → READ FIRST
│   ├── ARCHITECTURE.md          # Validated architectural decisions
│   ├── DECISIONS.md             # ADR journal
│   ├── GUIDELINES.md            # Advisory practices
│   ├── active/                  # Validated artifacts, not yet archived
│   ├── archive/                 # Implemented / historical
│   ├── drafts/                  # WIP — gitignored
│   ├── decisions/               # Individual ADRs (adr-NNN-slug.md)
│   └── references/              # raw/ · interim/ · synthesis/
```

- [ ] **Step 2: Update the `## Rules` section — replace rule #1**

old_string:
```
1. **No temp files at root** — everything goes in `.meta/scratch/`
```

new_string:
```
1. **No temp files at root** — WIP goes in `.meta/drafts/` (gitignored). Validated artifacts in `.meta/active/`, implemented in `.meta/archive/`. Filename format: `<type>-<YYYY-MM-DD>-<slug>.md` (types: spec, plan, brainstorm, debate, session) — enforced by `scripts/check_meta_naming.py`
```

- [ ] **Step 3: Verify**

```bash
grep -c "active/" CLAUDE.md
grep -c "drafts/" CLAUDE.md
grep -c "check_meta_naming" CLAUDE.md
! grep -q "scratch/" CLAUDE.md && echo "no scratch ref ok"
```
Expected: each positive grep ≥ 1; the negation line prints `no scratch ref ok`.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md architecture + rule #1 for taxonomy"
```

---

## Task 19: Update `.meta/PILOT.md`

**Files:**
- Modify: `.meta/PILOT.md`

- [ ] **Step 1: Replace the `## Scratch files` / `## Debate records` / `## References` sections with a single structure section**

Read the file to locate the exact blocks. Use Edit to replace all three sections with:

```markdown
## `.meta/` structure

See `.meta/GUIDELINES.md` for the full taxonomy. Quick map:

- `active/` — validated plans/specs currently in flight
- `archive/` — implemented or historical artifacts (chronological memory)
- `drafts/` — WIP (gitignored)
- `decisions/` — ADRs
- `references/{raw,interim,synthesis}/` — external research by maturity

Filename convention: `<type>-<YYYY-MM-DD>-<slug>.md` (types: spec, plan, brainstorm, debate, session). Enforced by pre-commit.
```

- [ ] **Step 2: Update Phase 0 status table — mark 0.2 and 0.3 DONE**

Find rows:
```
| 0.2 | meta_visibility copier parameter | PLAN NEEDED |
| 0.3 | .meta/ gitignore alignment (this repo) | PLAN NEEDED |
```
Replace with:
```
| 0.2 | meta_visibility copier parameter | DONE |
| 0.3 | .meta/ gitignore alignment (this repo) | DONE |
```

- [ ] **Step 3: Verify**

```bash
grep -c "0.2 | meta_visibility copier parameter | DONE" .meta/PILOT.md
grep -c "0.3 | .meta/ gitignore alignment" .meta/PILOT.md
! grep -q "## Scratch files" .meta/PILOT.md && echo "scratch section removed"
```
Expected: counts ≥ 1 and `scratch section removed` printed.

- [ ] **Step 4: Commit**

```bash
git add .meta/PILOT.md
git commit -m "docs(pilot): replace scratch index with taxonomy + mark 0.2/0.3 done"
```

---

## Task 20: Final acceptance — verify every spec criterion

**Files:** none (verification only).

- [ ] **Step 1: AC1 — directory layout**

```bash
find .meta -maxdepth 2 -type d | sort
```
Expected (exactly, order insensitive): `.meta`, `.meta/active`, `.meta/archive`, `.meta/decisions`, `.meta/drafts`, `.meta/references`, `.meta/references/interim`, `.meta/references/raw`, `.meta/references/synthesis`. NOTHING else. Specifically: no `scratch`, `debates`, `sessions`, `gold`.

- [ ] **Step 2: AC2 — `scratch/` ghost-free**

```bash
git ls-files .meta/scratch/ | wc -l
```
Expected: `0`.

- [ ] **Step 3: AC3 — every file in active/ + archive/ matches the pattern**

```bash
uv run python scripts/check_meta_naming.py $(git ls-files .meta/active/ .meta/archive/)
echo "exit=$?"
```
Expected: `exit=0`.

- [ ] **Step 4: AC4 — gitignore rule**

```bash
grep -A1 "Meta protocol" .gitignore
```
Expected: exactly the two lines `.meta/drafts/*` and `!.meta/drafts/.gitkeep`.

- [ ] **Step 5: AC5 — full pre-commit run**

```bash
uv run pre-commit run --all-files
echo "exit=$?"
```
Expected: `exit=0`.

- [ ] **Step 6: AC6 — copier public mode**

```bash
rm -rf /tmp/taxo-pub && copier copy . /tmp/taxo-pub --defaults --trust --vcs-ref=HEAD
find /tmp/taxo-pub/.meta -maxdepth 2 -type d | sort
grep -A1 "Meta protocol" /tmp/taxo-pub/.gitignore
```
Expected: same directory layout as meta-repo; gitignore shows `.meta/drafts/*` + `!.gitkeep`.

- [ ] **Step 7: AC7 — copier private mode**

```bash
rm -rf /tmp/taxo-priv && copier copy . /tmp/taxo-priv --defaults --trust --vcs-ref=HEAD --data meta_visibility=private
grep -A1 "Meta protocol" /tmp/taxo-priv/.gitignore
```
Expected: line containing bare `.meta/`.

- [ ] **Step 8: AC8 — PILOT updated**

```bash
grep "0.2 | meta_visibility copier parameter | DONE" .meta/PILOT.md
grep "0.3 | .meta/ gitignore alignment" .meta/PILOT.md | grep DONE
```
Expected: both print a match.

- [ ] **Step 9: AC9 — no file loss**

```bash
# Spot-check: a known validated artifact survived
test -f .meta/active/plan-2026-04-08-launch.md && echo "launch ok"
# Spot-check: a known archive
test -f .meta/archive/spec-2026-04-08-workflow-gates.md && echo "workflow-gates ok"
# Spot-check: gold migration
test -f .meta/references/synthesis/gstack-skill-pack.md && echo "gstack ok"
```
Expected: three `ok` lines. (Substitute filenames per user-edited triage.)

- [ ] **Step 10: Ruff**

```bash
uv run ruff check .
```
Expected: `All checks passed`.

- [ ] **Step 11: Final report to user**

Report verbatim:
```
Migration complete.

- Branch: feat/phase-0 (NOT merged to main — per Phase 0 rule)
- Commits added: ~20
- Taxonomy enforced by scripts/check_meta_naming.py (pre-commit)
- Template propagates: copier.yml meta_visibility, template/scripts/, template/.meta/
- PILOT.md: 0.2 and 0.3 marked DONE
- Remaining in Phase 0: 0.4 (PILOT cleanup) + 0.6 (commit strategy)

Ready to continue with 0.4 and 0.6, or inspect the branch first.
```

---

## Self-review (done inline while drafting)

- **Spec M1** (single gitignore rule) → Task 8 ✅
- **Spec M2** (unambiguous lifecycle) → Tasks 1, 3, 4, 5, 7 ✅
- **Spec M3** (one filename format) → Tasks 3, 4 (renames) + Task 9 (hook) ✅
- **Spec M4** (pre-commit rejects non-conforming) → Tasks 9, 10 + AC3 ✅
- **Spec M5** (meta_visibility binary) → Tasks 11, 12 + AC6, AC7 ✅
- **Spec M6** (no file loss) → Tasks 3–5 cover all 45 known files, Task 6 handles explicit drops, AC9 spot-checks ✅
- **Spec M7** (visitor can answer "what's alive?" in 1 click) → Task 1 creates `active/` ✅
- **Spec M8** (`git mv` is the transition) → used throughout Tasks 3, 4, 5 ✅
- **Spec S1** (GUIDELINES documents convention) → Task 16 ✅
- **Spec S2** (PILOT scratch section reworked) → Task 19 ✅
- **Spec S3** (references tiered with data/ vocab) → Task 5 ✅
- **Spec W1** (no trash/) → not created in Task 1 ✅
- **Spec W3** (directory is source of truth, no YAML status) → hook ignores frontmatter ✅
- **"No merge to main"** → explicit in header + final report ✅
- **User-gated triage** → Task 2 STOPS with explicit instructions ✅

All 9 acceptance criteria from the spec are exercised in Task 20 (AC1–AC9).
