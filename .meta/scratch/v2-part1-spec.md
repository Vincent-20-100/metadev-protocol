# v2 Part 1 — Superpowers Integration Spec

**Date:** 2026-04-02
**Status:** APPROVED — ready for planning
**Scope:** Integrate Superpowers plugin, rename /ship → /save-progress, redirect outputs

---

## Decisions from brainstorm

1. **Skills T2 delegated to Superpowers** — no custom skills to create for /debug, /review, /tdd, /spec
2. **Superpowers outputs redirected** to `.meta/scratch/` via CLAUDE.md instruction
3. **/brainstorm and /plan kept as fallbacks** — Superpowers overrides when installed
4. **/ship renamed to /save-progress** — more explicit for all audiences
5. **/consolidate dropped** — YAGNI, /save-progress covers the need
6. **Auto-install Superpowers** — same pattern as uv: check → propose → install if user says yes

---

## Changes

### 1. template/CLAUDE.md.jinja

**Add to Automatisms section (new item, after current #2):**

```
N. **Superpowers plugin** — if superpowers skills are not available, recommend
   installing the plugin: `/install-plugin obra/superpowers`. It provides
   advanced workflows (brainstorming, debugging, code review, TDD). If the
   user agrees, run the install command.
```

**Add new section — Superpowers output paths:**

```
## Superpowers output paths

Specs and plans go in `.meta/scratch/`, not `docs/superpowers/`:
- Specs → `.meta/scratch/spec-<topic>.md`
- Plans → `.meta/scratch/plan-<topic>.md`
```

**Update Skills section:**

```
## Skills

Project skills (always available):
  /save-progress  — checklist + context update (does NOT commit)
  /lint            — ruff check + format on the whole project
  /test            — run pytest
  /brainstorm      — structured exploration (basic — use superpowers:brainstorming if available)
  /plan            — task decomposition (basic — use superpowers:writing-plans if available)

Recommended plugin (install with /install-plugin obra/superpowers):
  superpowers:brainstorming          — full design process with spec writing
  superpowers:writing-plans          — detailed implementation plans
  superpowers:executing-plans        — guided plan execution with checkpoints
  superpowers:systematic-debugging   — evidence-first debugging (4 phases)
  superpowers:requesting-code-review — two-stage code review
  superpowers:test-driven-development — red-green-refactor cycle
```

### 2. template/.claude/skills/

**Rename:** `ship/SKILL.md` → `save-progress/SKILL.md`
- Update frontmatter: `name: save-progress`
- Update description: `Pre-commit checklist and context update — does NOT commit`
- Content stays the same (checklist + PILOT.md update + SESSION-CONTEXT.md rewrite)

**Delete:** `ship/` directory after creating `save-progress/`

**Update brainstorm/SKILL.md — add fallback note at top:**

```
> Note: If you have the Superpowers plugin installed, prefer `superpowers:brainstorming`
> for a more thorough design process. This skill is a lightweight fallback.
```

**Update plan/SKILL.md — add fallback note at top:**

```
> Note: If you have the Superpowers plugin installed, prefer `superpowers:writing-plans`
> for more detailed implementation plans. This skill is a lightweight fallback.
```

### 3. template/.meta/GUIDE.md.jinja

**Update skills section:**
- Replace /ship with /save-progress everywhere
- Add "Recommended plugin" subsection explaining Superpowers
- Update workflow examples to show /save-progress

**Add new section after Skills:**

```
## Recommended plugin: Superpowers

For advanced workflows (structured debugging, code review, TDD), install the
Superpowers plugin:

    /install-plugin obra/superpowers

The plugin provides skills like `superpowers:brainstorming` (full design process),
`superpowers:systematic-debugging` (evidence-first, 4 phases), and
`superpowers:requesting-code-review` (two-stage review).

The LLM will suggest installing it on first session if it's not already present.
```

### 4. docs/PHILOSOPHY.md

**Update Skills section (principle #5):**
- Explain the strategy: project-specific skills (save-progress, lint, test) + Superpowers plugin for general workflow
- Mention fallback pattern: basic /brainstorm and /plan ship with the project, Superpowers overrides when installed

### 5. No changes to

- template/.claude/settings.json.jinja (no hook needed)
- copier.yml (Superpowers install happens in Claude Code, not at generation)
- template/pyproject.toml.jinja
- template/.pre-commit-config.yaml

---

## Test plan

1. Generate a project without Superpowers installed → verify /save-progress, /brainstorm, /plan, /lint, /test all work
2. Install Superpowers → verify superpowers:brainstorming overrides /brainstorm
3. Verify CLAUDE.md mentions Superpowers recommendation
4. Verify GUIDE.md has the plugin section
5. Verify output redirect instruction is in CLAUDE.md
