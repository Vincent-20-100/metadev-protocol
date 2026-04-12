---
type: plan
date: 2026-04-12
slug: execution-mode
status: active
---

# Plan — Full-auto execution mode (P1)

Implements `spec-2026-04-12-execution-mode.md`. Five commit-sized tasks.

## T1 — Add `execution_mode` to `copier.yml`

**Files:** `copier.yml`

**Steps:**
1. Insert `execution_mode` block after the `meta_visibility` block, with choices `safe` / `full-auto`, default `safe`, explicit help text.
2. Smoke-test: `copier copy . /tmp/test-em --defaults --trust --vcs-ref=HEAD` succeeds and generates without error.

**Commit:** `feat(copier): add execution_mode parameter (safe/full-auto)`

## T2 — Convert `template/.claude/settings.json.jinja` to conditional

**Files:** `template/.claude/settings.json.jinja`

**Steps:**
1. Read current file (already done).
2. Rewrite as jinja conditional:
   - Shared: `attribution`, `hooks`, and the full `deny` array (exact list from spec §2).
   - `{% if execution_mode == 'safe' %}` block: `allow` + `ask` per spec §2 safe preset.
   - `{% else %}` block: `allow` + empty `ask` per spec §2 full-auto preset.
3. Validate JSON for both modes:
   - `copier copy . /tmp/test-safe --defaults --trust --vcs-ref=HEAD` → `python -m json.tool /tmp/test-safe/.claude/settings.json`
   - `copier copy . /tmp/test-auto --data execution_mode=full-auto --trust --vcs-ref=HEAD` → `python -m json.tool /tmp/test-auto/.claude/settings.json`
4. Diff the two deny blocks to confirm byte-identical:
   - `diff <(jq .permissions.deny /tmp/test-safe/.claude/settings.json) <(jq .permissions.deny /tmp/test-auto/.claude/settings.json)` → empty.

**Commit:** `feat(template): conditional settings.json permissions per execution_mode`

## T3 — Add CLAUDE.md prose rule

**Files:** `template/CLAUDE.md.jinja`

**Steps:**
1. Open `template/CLAUDE.md.jinja` at the automatisms section.
2. Insert a new automatism (number 11, at the end of the numbered list, before "Always") OR extend automatism #4 with the new paragraph. Decision at implementation time: extend #4 if it keeps decision-tree context close; add #11 if extending makes #4 too long.
3. Verbatim text from spec §3.
4. Regenerate and verify the rule is present:
   - `copier copy . /tmp/test-prose --defaults --trust --vcs-ref=HEAD`
   - `grep -q "Plan validated = all actions validated" /tmp/test-prose/CLAUDE.md`

**Commit:** `feat(template): add plan-validated prose rule to CLAUDE.md`

## T4 — Document both modes in README

**Files:** `README.md` (repo root — the template README, which is the public-facing doc)

**Steps:**
1. Open `README.md`, locate the "Visibility modes" section (or the closest section about copier parameters).
2. Add a new section "Execution modes" with:
   - Short intro: what `execution_mode` is, why it exists
   - Table or bullet comparison: safe vs full-auto
   - Warning block for full-auto (bold, explicit about the risk model)
   - "Switching modes" paragraph: edit `.claude/settings.json` directly, or re-run `copier update` and change the answer
3. No code change needed — documentation only.

**Commit:** `docs(readme): document execution modes (safe/full-auto)`

## T5 — Acceptance criteria checklist + final validation

**Files:** none (validation only)

**Steps:**
1. Walk through AC1–AC10 from the spec one by one, testing each.
2. Run the 4-case generation matrix:
   - `meta_visibility=public` + `execution_mode=safe`
   - `meta_visibility=public` + `execution_mode=full-auto`
   - `meta_visibility=private` + `execution_mode=safe`
   - `meta_visibility=private` + `execution_mode=full-auto`
   All four must generate without error and produce valid JSON in `.claude/settings.json`.
3. Run `uv run pre-commit run --all-files` on the meta-repo.
4. If any AC fails, create a follow-up fix commit (do not modify existing T1–T4 commits).

**Commit (if fixes needed):** `fix(execution-mode): <specific fix>`

No new commit if all ACs pass on first try — T1–T4 commits are the deliverable.

## Commit granularity rationale

Four feature commits + optional fix commit. Each of T1–T4 is independently reviewable (<5 min) and bisectable:
- T1 alone adds the param but doesn't use it → generation still works, no regression.
- T2 adds the conditional → relies on T1 for the variable but falls back to `safe` default.
- T3 is a pure prose addition → independent of T1/T2.
- T4 is documentation → independent.

Order T1 → T2 is required (T2 depends on the param). T3 and T4 could be in any order after T2, but sequential execution is simpler.

## Rollback

If a later review reveals the permission matcher syntax is wrong in Claude Code:
- `git revert` T2 alone → param becomes vestigial but safe (default `safe` still matches today's behavior).
- Fix syntax in a new commit on top.

T1 never rolls back alone (harmless param).
