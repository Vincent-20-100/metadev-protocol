# Plan — Skills & agents architecture overhaul (v1.6.0)

**Date:** 2026-04-14
**Based on:** `.meta/drafts/spec-skills-architecture.md`
**Confidence:** AMBER
**Commit count:** 8 (tight, bisectable, each reviewable in <5 min)
**Target release:** v1.6.0

---

## Execution order

```
C1   Honesty baseline      — delete 4 ghost agent rows from trigger tables
C2   Contract script v1    — per-tree checks (no parity yet)
C3   Meta dogfooding       — bring meta to parity with template + strict parity check
C3a  Ship 4 new agents     — code-reviewer, test-engineer, security-auditor, data-analyst (dual-maintained)
C4   Thin skills           — refactor /test and /save-progress under skill-vs-tool
C5   Tech-watch fusion     — merge /radar + /audit-repo into /tech-watch
C6   Doc cascade           — ADR, ARCHITECTURE, PILOT, CHANGELOG, README
C7   Tag v1.6.0            — annotated release
```

Each commit passes `uv run pytest` + pre-commit hooks independently.
Stopping at any intermediate commit leaves the repo in a shippable state.

---

## Commit C1 — Honesty baseline

**Goal:** remove the 4 ghost agent rows from both trigger tables. The rows will come back in C3a with real files backing them. Between C1 and C3a, the trigger tables reference only `devils-advocate` as local agent. No plugin pointer row — the superpowers reference lives in the existing "Recommended plugin" section already present in CLAUDE.md.

### Files involved

- `CLAUDE.md` (meta)
- `template/CLAUDE.md.jinja`
- `tests/test_template_generation.py` (if any test references ghost agents)

### Tasks

#### C1.1 — Delete ghost agent rows from meta CLAUDE.md
- **File:** `CLAUDE.md`
- **Do:** In the Skills & Agents trigger table, delete rows for `code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst`. Keep `devil's-advocate`. Do NOT add a plugin-pointer row — the existing `## Superpowers` or `Recommended plugin` section already covers superpowers discoverability.
- **Verify:** `grep -E "code-reviewer|test-engineer|security-auditor|data-analyst" CLAUDE.md` returns no matches in the trigger table region (matches in prose, if any, are fine).

#### C1.2 — Delete ghost agent rows from template CLAUDE.md.jinja
- **File:** `template/CLAUDE.md.jinja`
- **Do:** Same operation on `template/CLAUDE.md.jinja`. Preserve the existing "Recommended plugin" section which already mentions superpowers.
- **Verify:** `grep -E "code-reviewer|test-engineer|security-auditor|data-analyst" template/CLAUDE.md.jinja` returns no matches in the trigger table region.

#### C1.3 — Update tests if any reference ghost agents
- **File:** `tests/test_template_generation.py`
- **Do:** Grep for ghost agent names; if any assertions reference them, update or remove.
- **Verify:** `uv run pytest tests/test_template_generation.py -k "agent" -v` — green.

#### C1.4 — Commit
```bash
git add CLAUDE.md template/CLAUDE.md.jinja tests/test_template_generation.py
git commit -m "docs(contract): delete 4 ghost agent rows from trigger tables (pre-ship cleanup)"
```

---

## Commit C2 — Contract script v1 (per-tree only)

**Goal:** ship `scripts/check_skills_contract.py` with per-tree invariants (every row maps to an existing file in the same tree; every directory is referenced). Do NOT enforce meta ↔ template parity yet — that arrives in C3 after meta is brought to parity.

### Files involved

- `scripts/check_skills_contract.py` (new)
- `template/scripts/check_skills_contract.py` (new, identical)
- `.pre-commit-config.yaml` (meta)
- `template/.pre-commit-config.yaml`
- `tests/test_template_generation.py`

### Tasks

#### C2.1 — Write the script
- **Files:** `scripts/check_skills_contract.py`, `template/scripts/check_skills_contract.py`
- **Do:** Python 3.13 script. Input: optional `--path` flag (default `.`). For each of `CLAUDE.md` (if exists) and `template/CLAUDE.md.jinja` (if exists), parse the Skills & Agents trigger table, validate each row per the spec §4.1. Exit 0 on success, 1 on any failure. Print specific violations to stderr. Plugin allowlist initially: `{"obra/superpowers", "superpowers"}`. No external deps — stdlib only.
- **Shared content:** the two files are identical. To avoid drift, keep the template version as the canonical copy and let the meta version be a symlink OR a byte-for-byte copy — pick copy (Windows symlink friction). Pre-commit hook C2.3 asserts byte-for-byte equality between the two copies.
- **Verify:** `uv run python scripts/check_skills_contract.py` exits 0 on the current tree (post-C1, where ghost rows have been removed).

#### C2.2 — Add pre-commit hook (meta)
- **File:** `.pre-commit-config.yaml`
- **Do:** Add a local hook:
  ```yaml
  - repo: local
    hooks:
      - id: check-skills-contract
        name: Skills & agents trigger table ↔ filesystem contract
        entry: uv run python scripts/check_skills_contract.py
        language: system
        pass_filenames: false
        always_run: true
  ```
- **Verify:** `pre-commit run check-skills-contract --all-files` → success on the current tree.

#### C2.3 — Add pre-commit hook (template)
- **File:** `template/.pre-commit-config.yaml`
- **Do:** Same hook, pointing at `template/scripts/check_skills_contract.py`. Also add a byte-identity hook ensuring `scripts/check_skills_contract.py` and `template/scripts/check_skills_contract.py` have identical content (uses `scripts/assert_files_identical.py` OR a shell one-liner `diff -q` via `entry`).
- **Verify:** generated project (via `copier copy . /tmp/test-proj --defaults`) contains `scripts/check_skills_contract.py` and its pre-commit hook.

#### C2.4 — Test the contract check via pytest
- **File:** `tests/test_template_generation.py`
- **Do:** Add `TestSkillsContract` class with `test_generated_project_passes_contract_check` — generates a project, runs `python scripts/check_skills_contract.py` in it via subprocess, asserts exit 0.
- **Verify:** `uv run pytest tests/test_template_generation.py::TestSkillsContract -v` — green.

#### C2.5 — Commit
```bash
git add scripts/check_skills_contract.py template/scripts/check_skills_contract.py \
        .pre-commit-config.yaml template/.pre-commit-config.yaml \
        tests/test_template_generation.py
git commit -m "feat(contract): add check_skills_contract.py — every trigger row must map to a real artifact"
```

---

## Commit C3 — Meta dogfooding baseline

**Goal:** bring the meta-repo's `.claude/` and `.meta/` trees to symmetric parity with the template's output. Then tighten the contract script to assert meta ↔ template parity.

### Files involved (all new or updated in meta)

- `.claude/skills/brainstorm/` (copy from template — SKILL.md)
- `.claude/skills/debate/` (same)
- `.claude/skills/orchestrate/` (same)
- `.claude/skills/plan/` (same)
- `.claude/skills/spec/` (same)
- `.claude/skills/save-progress/` (same)
- `.claude/skills/test/` (same)
- `.claude/skills/research/SKILL.md` + `.claude/skills/research/output-schema.md` — **sync from template v1.5.0 thin version**, delete the stale 156-line meta version
- `.claude/skills/vision/` — already parity; verify no drift
- `.claude/agents/` — **create directory**; copy `devils-advocate.md` from `template/.claude/agents/`
- `.claude/rules/` — **create directory**; copy `code-style.md` + `testing.md` from `template/.claude/rules/`
- `.claude/settings.json` — **create** (Jinja-rendered with `execution_mode=full-auto`, `meta_visibility=public`, `enable_server_auth_check=true`) — Vincent's actual preferences. No more "only `settings.local.json`".
- `.meta/GUIDELINES.md` — **create** by copying the rendered content of `template/.meta/GUIDELINES.md.jinja` (use `copier copy . /tmp/test-meta --defaults`; lift the file; adjust for meta-repo context)
- `scripts/check_skills_contract.py` — **tighten** with meta ↔ template parity check
- `tests/test_template_generation.py` — update

### Tasks

#### C3.1 — Copy missing skills to meta
- **Files:** 7 new directories under `.claude/skills/`
- **Do:** For each of `brainstorm`, `debate`, `orchestrate`, `plan`, `spec`, `save-progress`, `test`: copy the entire directory from `template/.claude/skills/<name>/` to `.claude/skills/<name>/`. If any files are `.jinja` templates, render them with the meta-repo context (project_name=metadev-protocol, etc.) — for pure `.md` skills, direct copy.
- **Verify:** `ls .claude/skills/` shows all 10 skills (after C5 includes tech-watch; at this commit, 10 minus audit-repo plus the 7 new = old state of 3 + 7 = 10 including stale research and existing audit-repo). At this commit we still have old `audit-repo/` and stale research; both get cleaned in C5.

#### C3.2 — Sync `.claude/skills/research/` with template v1.5.0 version
- **Files:** `.claude/skills/research/SKILL.md`, `.claude/skills/research/output-schema.md`
- **Do:** Overwrite meta's stale 156-line SKILL.md with the template version (74 lines). Create `output-schema.md` by copying from template.
- **Verify:** `diff template/.claude/skills/research/SKILL.md .claude/skills/research/SKILL.md` shows zero difference (except any Jinja variable substitution, which research SKILL.md does not have).

#### C3.3 — Create `.claude/agents/` in meta
- **Files:** `.claude/agents/devils-advocate.md`
- **Do:** `mkdir -p .claude/agents && cp template/.claude/agents/devils-advocate.md .claude/agents/devils-advocate.md`.
- **Verify:** `test -f .claude/agents/devils-advocate.md`.

#### C3.4 — Create `.claude/rules/` in meta
- **Files:** `.claude/rules/code-style.md`, `.claude/rules/testing.md`
- **Do:** `mkdir -p .claude/rules && cp template/.claude/rules/*.md .claude/rules/`.
- **Verify:** `ls .claude/rules/` shows both files.

#### C3.5 — Create `.claude/settings.json` in meta
- **File:** `.claude/settings.json`
- **Do:** Render `template/.claude/settings.json.jinja` with `execution_mode=full-auto`, `meta_visibility=public`, `enable_server_auth_check=true`. Save the rendered JSON to `.claude/settings.json`. Do NOT delete `.claude/settings.local.json` — it remains a personal overlay (gitignored).
- **Verify:** `uv run python -c "import json; json.load(open('.claude/settings.json'))"` — parses clean; `jq .permissions.allow .claude/settings.json` shows `["Bash(*)", ...]` or the full-auto equivalent.

#### C3.6 — Create `.meta/GUIDELINES.md` in meta
- **File:** `.meta/GUIDELINES.md`
- **Do:** Generate a test project (`copier copy . /tmp/metadev-sync --defaults --trust --vcs-ref=HEAD`), copy `.meta/GUIDELINES.md` from the generated project to this repo's `.meta/GUIDELINES.md`. Adjust any project-specific phrasing if needed (minimal — the content is advisory and project-agnostic).
- **Verify:** `test -f .meta/GUIDELINES.md && wc -l .meta/GUIDELINES.md` — file exists, ≥200 lines.

#### C3.7 — Tighten contract script with parity check
- **File:** `scripts/check_skills_contract.py` (and its template twin)
- **Do:** Add a new assertion: for each skill directory in `template/.claude/skills/<name>/`, assert `.claude/skills/<name>/` exists in the meta tree (when the script runs from a meta-repo, detected by presence of `template/` + `copier.yml`). Whitelist `audit-repo` as meta-only for the duration of C3 → C5 (removed in C5).
- **Verify:** `uv run python scripts/check_skills_contract.py` exits 0 on the current post-C3.6 tree.

#### C3.8 — Update tests
- **File:** `tests/test_template_generation.py`
- **Do:** Add `TestMetaParity::test_meta_skills_mirror_template` — walks `template/.claude/skills/` and asserts each has a counterpart in `.claude/skills/`. Parameterize with the whitelist.
- **Verify:** `uv run pytest tests/test_template_generation.py::TestMetaParity -v` — green.

#### C3.9 — Commit
```bash
git add .claude/ .meta/GUIDELINES.md scripts/check_skills_contract.py \
        template/scripts/check_skills_contract.py tests/test_template_generation.py
git commit -m "feat(meta): dogfood template — symmetric .claude/ tree, settings.json, GUIDELINES, parity-checked contract"
```

---

## Commit C3a — Ship 4 new agents (code-reviewer, test-engineer, security-auditor, data-analyst)

**Goal:** create the 4 agent files per the scopes defined in the spec §2.4, ship them in both template and meta (full symmetry per user Q6), re-add the 4 rows to both trigger tables, update tests. After this commit, the 4 agents are real and invocable.

### Files involved

**Created:**
- `template/.claude/agents/code-reviewer.md`
- `template/.claude/agents/test-engineer.md`
- `template/.claude/agents/security-auditor.md`
- `template/.claude/agents/data-analyst.md`
- `.claude/agents/code-reviewer.md` (meta — identical to template)
- `.claude/agents/test-engineer.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/data-analyst.md`

**Updated:**
- `CLAUDE.md` (meta) — re-add 4 agent rows
- `template/CLAUDE.md.jinja` — re-add 4 agent rows
- `tests/test_template_generation.py` — add `TestAgents::EXPECTED_AGENTS` + parity test

### Tasks

#### C3a.1 — Write `code-reviewer.md`
- **Files:** `template/.claude/agents/code-reviewer.md` + `.claude/agents/code-reviewer.md` (identical)
- **Do:** Follow spec §2.4 scope. Frontmatter: `name: code-reviewer`, `description: Post-implementation code review — applies project rules, catches non-trivial logic bugs, verifies coherence with in-flight spec/plan. Auto-triggered when ≥3 files touched or a plan step just completed. Distinct from devils-advocate (which challenges decisions, not code).`, `model: sonnet`. Body: mandate / process (5 steps per spec) / hard rules / output format (CRITICAL / WARN / NIT tiered report with file:line + fix + rationale) / rationalizations table (why you must NOT skip steps). ~100–120 lines.
- **Verify:** `wc -l template/.claude/agents/code-reviewer.md` in range [80, 150]; `diff template/.claude/agents/code-reviewer.md .claude/agents/code-reviewer.md` returns empty.

#### C3a.2 — Write `test-engineer.md`
- **Files:** `template/.claude/agents/test-engineer.md` + meta mirror
- **Do:** Per spec §2.4. Frontmatter: `name: test-engineer`, `description: Generative test author — given an implementation, propose and write missing tests following rules/testing.md conventions. Propose-triggered on new module, new public API, or missing coverage. Not a runner (/test does that), not a coverage checker.`, `model: sonnet`. Body: mandate / process (4 steps) / hard rules (no assertion-less test, no duplicates, no internal mocks) / output format (pytest files + summary) / rationalizations table.
- **Verify:** same as C3a.1.

#### C3a.3 — Write `security-auditor.md`
- **Files:** `template/.claude/agents/security-auditor.md` + meta mirror
- **Do:** Per spec §2.4. Frontmatter: `name: security-auditor`, `description: OWASP-style sweep on touched code. Propose-triggered on auth, secrets, input validation, crypto, network boundaries, file uploads, path traversal, command injection. Scoped to diff/module (not the whole repo — that's audit_public_safety.py's job).`, `model: sonnet`. Body: mandate / process (4 steps: surface map → category sweep → tiered findings EXPLOIT/HARDENING/INFO → concrete fix) / hard rules / output format / rationalizations.
- **Verify:** same.

#### C3a.4 — Write `data-analyst.md`
- **Files:** `template/.claude/agents/data-analyst.md` + meta mirror
- **Do:** Per spec §2.4. Frontmatter: `name: data-analyst`, `description: Audit statistical claims, pipelines, metric computations. Propose-triggered on ETL, metric, statistical claim, dataset quality question. Catches sampling bias, data leakage, reproducibility gaps, metric gaming, off-by-one on temporal windows.`, `model: sonnet`. Body: mandate / process (4 steps) / hard rules (never "looks correct", reproducibility check mandatory, skip if code doesn't manipulate data) / output format / rationalizations.
- **Verify:** same.

#### C3a.5 — Re-add 4 agent rows to meta `CLAUDE.md`
- **File:** `CLAUDE.md`
- **Do:** In the Skills & Agents trigger table, add 4 rows:
  ```markdown
  | `code-reviewer` | agent | ≥3 files touched in current plan, or a plan step just completed | **Auto** |
  | `test-engineer` | agent | new module, new public API, or missing coverage on touched code | **Propose** |
  | `security-auditor` | agent | auth, secrets, input validation, crypto, network boundaries, file uploads | **Propose** |
  | `data-analyst` | agent | pipeline, ETL, metric computation, statistical claim, or dataset quality question | **Propose** |
  ```
- **Verify:** `grep -c "^| \`code-reviewer\`" CLAUDE.md` returns 1; markdown table still valid (no orphan pipes).

#### C3a.6 — Re-add 4 agent rows to `template/CLAUDE.md.jinja`
- **File:** `template/CLAUDE.md.jinja`
- **Do:** Identical additions to the template trigger table.
- **Verify:** grep checks as above.

#### C3a.7 — Strengthen superpowers framing
- **Files:** `CLAUDE.md` + `template/CLAUDE.md.jinja`
- **Do:** In the existing "Recommended plugin" / "Superpowers" section, add a framing sentence explicit about the fallback relationship: *"The local skills `brainstorm`, `plan`, `spec`, `debate`, `orchestrate`, `research`, `test`, `save-progress` are fallbacks — they work out-of-the-box. The `superpowers` plugin ships superior and more complete versions of the same workflows (`superpowers:brainstorming`, `superpowers:writing-plans`, `superpowers:executing-plans`, etc.). When the plugin is installed, prefer its versions. The 4 local agents (`code-reviewer`, `test-engineer`, `security-auditor`, `data-analyst`) are additive, not fallbacks — they complement superpowers' own agents."*
- **Verify:** `grep "fallbacks" CLAUDE.md` returns the new sentence; same in `template/CLAUDE.md.jinja`.

#### C3a.8 — Update tests
- **File:** `tests/test_template_generation.py`
- **Do:** Add:
  ```python
  class TestAgents:
      EXPECTED_AGENTS = [
          "devils-advocate",
          "code-reviewer",
          "test-engineer",
          "security-auditor",
          "data-analyst",
      ]
      def test_all_agents_present(self, generated_project: Path) -> None:
          agents_dir = generated_project / ".claude" / "agents"
          assert agents_dir.is_dir()
          present = {p.stem for p in agents_dir.iterdir() if p.is_file() and p.suffix == ".md"}
          for a in self.EXPECTED_AGENTS:
              assert a in present, f"agent {a} missing from generated project"
  ```
  Update `TestMetaParity` to also check `.claude/agents/` parity (was skills-only before).
- **Verify:** `uv run pytest tests/test_template_generation.py::TestAgents tests/test_template_generation.py::TestMetaParity -v` — green.

#### C3a.9 — Run contract script
- **Do:** `uv run python scripts/check_skills_contract.py`
- **Verify:** exit 0 — every row in both trigger tables now maps to a real file.

#### C3a.10 — Commit
```bash
git add template/.claude/agents/ .claude/agents/ \
        CLAUDE.md template/CLAUDE.md.jinja \
        tests/test_template_generation.py
git commit -m "feat(agents): ship code-reviewer, test-engineer, security-auditor, data-analyst (4 local agents, dual-maintained)"
```

---

## Commit C4 — Thin `/test` and `/save-progress`

**Goal:** apply the skill-vs-tool filter to the two skills memo-flagged as sur-LLMisés. Both are quasi-deterministic. Replace their bodies with thin wrappers that invoke scripts.

### Files involved

- `template/.claude/skills/test/SKILL.md` + new `template/scripts/run_tests.py` (if thinning requires a script)
- `template/.claude/skills/save-progress/SKILL.md` + new `template/scripts/save_progress.py`
- `.claude/skills/test/SKILL.md` + `scripts/run_tests.py` (meta mirror)
- `.claude/skills/save-progress/SKILL.md` + `scripts/save_progress.py`

### Tasks

#### C4.1 — Analyze and thin `/test`
- **Do:** Read current `template/.claude/skills/test/SKILL.md`. Identify LLM steps vs deterministic steps. If ≥80% deterministic, extract a `scripts/run_tests.py` (or keep a single bash line, whichever is simpler). The thin SKILL.md is ≤50 lines: invoke the script, frame pass/fail/summary for the user, propose next step.
- **Verify:** `wc -l template/.claude/skills/test/SKILL.md` ≤ 50. `uv run pytest tests/test_template_generation.py::TestSkills` — green.

#### C4.2 — Analyze and thin `/save-progress`
- **Do:** Same filter. `/save-progress` currently updates `.meta/PILOT.md` and writes `.meta/SESSION-CONTEXT.md`. File I/O is deterministic; writing the narrative is LLM. Script handles git status + file reads; skill asks LLM to produce the narrative and invokes a writer. Thin SKILL.md ≤50 lines.
- **Verify:** `wc -l template/.claude/skills/save-progress/SKILL.md` ≤ 50.

#### C4.3 — Sync meta mirrors
- **Do:** Copy the thinned SKILL.md + any new script to the meta tree.
- **Verify:** `diff template/.claude/skills/test/SKILL.md .claude/skills/test/SKILL.md` — zero diff.

#### C4.4 — Commit
```bash
git add template/.claude/skills/test/ template/.claude/skills/save-progress/ \
        template/scripts/run_tests.py template/scripts/save_progress.py \
        .claude/skills/test/ .claude/skills/save-progress/ \
        scripts/run_tests.py scripts/save_progress.py
git commit -m "refactor(skills): thin /test and /save-progress — max deterministic under skill-vs-tool filter"
```

---

## Commit C5 — Tech-watch fusion (the big one)

**Goal:** merge `/radar` + `/audit-repo` into a unified `/tech-watch` skill with two modes (sweep + deep) sharing a common card schema. Ship in both meta and template.

### Files involved

**Created:**
- `template/scripts/tech_watch/__init__.py`
- `template/scripts/tech_watch/__main__.py`
- `template/scripts/tech_watch/core.py` (shared card writer, schema validator)
- `template/scripts/tech_watch/report.py` (card writing used by both modes)
- `template/scripts/tech_watch/index.py` (regenerates INDEX.md)
- `template/scripts/tech_watch/sweep/__init__.py`
- `template/scripts/tech_watch/sweep/fetch.py`
- `template/scripts/tech_watch/sweep/score.py`
- `template/scripts/tech_watch/sweep/dedup.py`
- `template/scripts/tech_watch/sweep/themes.py`
- `template/scripts/tech_watch/sweep/sources/` (migrated from `template/scripts/radar/sources/`)
- `template/scripts/tech_watch/deep/__init__.py`
- `template/scripts/tech_watch/deep/clone.py`
- `template/scripts/tech_watch/deep/fingerprint.py`
- `template/scripts/tech_watch/deep/tree.py`
- `template/scripts/tech_watch/deep/scan.py`
- `template/.claude/skills/tech-watch/SKILL.md` (new, thin, ≤100 lines)
- Same package in meta `scripts/tech_watch/`
- Meta `.claude/skills/tech-watch/SKILL.md`

**Deleted:**
- `template/scripts/radar/` (absorbed)
- `template/.claude/skills/radar/` (renamed)
- `scripts/audit_repo/` (meta — absorbed)
- `.claude/skills/audit-repo/` (meta — absorbed into tech-watch)
- `.claude/skills/research/` — STAYS, not affected
- `scripts/tech_watch.py` (meta — legacy v1.0.0 orphan, now superseded by the new package with the same directory name)

**Updated:**
- `CLAUDE.md` (meta) — rename `/radar` → `/tech-watch`, delete `/audit-repo` row (or confirm absent from the start if it was meta-only in the trigger table)
- `template/CLAUDE.md.jinja` — rename `/radar` → `/tech-watch`, remove `/audit-repo` row if present
- `tests/test_template_generation.py` — `EXPECTED_SKILLS` swap `radar` → `tech-watch`; add `test_tech_watch_has_sweep_and_deep_modes`
- `README.md` — rename refs
- Any cross-referencing SKILL.md files (e.g., `research/SKILL.md` mentions `/audit-repo`) — rename to `/tech-watch`

### Tasks

#### C5.1 — Preflight: confirm no conflicts
- **Do:** `git status` clean from C4. `test ! -d scripts/tech_watch` confirms the target package name is free (after the old `scripts/tech_watch.py` is deleted). `test ! -d template/scripts/tech_watch` same for template.
- **Verify:** both conditions hold.

#### C5.2 — Delete legacy `scripts/tech_watch.py`
- **Do:** `git rm scripts/tech_watch.py`
- **Verify:** `ls scripts/tech_watch.py 2>&1` → not found.

#### C5.3 — Create `template/scripts/tech_watch/` package skeleton
- **Do:** `mkdir -p template/scripts/tech_watch/{sweep/sources,deep}` and create empty `__init__.py` in each. Create `__main__.py` with the CLI dispatcher (sweep vs deep based on presence of positional URL).
- **Verify:** `uv run python -m template.scripts.tech_watch --help` → prints usage.

#### C5.4 — Migrate radar code to `tech_watch/sweep/`
- **Do:** `git mv template/scripts/radar/cards.py template/scripts/tech_watch/report.py` (renamed because the fusion calls them "cards" but we're unifying; cards.py handled card writing — becomes shared report.py). `git mv template/scripts/radar/core.py template/scripts/tech_watch/core.py`. `git mv template/scripts/radar/dedup.py template/scripts/tech_watch/sweep/dedup.py`. Similarly for `index.py`, `themes.py`, `report.py`, `sources/`. Update all import paths from `scripts.radar.*` to `scripts.tech_watch.*` (or `scripts.tech_watch.sweep.*` as appropriate).
- **Verify:** `uv run python -c "from scripts.tech_watch import core"` — imports cleanly. `uv run python -m scripts.tech_watch --refresh-themes` runs (or fails cleanly on missing config).

#### C5.5 — Migrate audit_repo code to `tech_watch/deep/`
- **Do:** Split current `scripts/audit_repo/__main__.py` into `tech_watch/deep/clone.py` (clone function), `deep/fingerprint.py` (fingerprint + language + type + license + pitch + gh metadata), `deep/tree.py` (tree builder), `deep/scan.py` (category scanning — new, implements the 5-category structural analysis). Do the same in the meta tree.
- **Verify:** `uv run python -m scripts.tech_watch https://github.com/astral-sh/ruff` produces a valid card at `.meta/references/research/deep-ruff-<date>.md`.

#### C5.6 — Write the unified card schema writer
- **File:** `template/scripts/tech_watch/report.py` (+ meta mirror)
- **Do:** Implement `write_card(mode, fingerprint, sweep_context=None, deep_findings=None, path)`. Uses front-matter with `mode: sweep|deep` and emits only the sections relevant to the mode. Cards written to `.meta/references/research/<slug>.md`.
- **Verify:** unit test `tests/test_tech_watch_card.py::test_sweep_card_schema` + `test_deep_card_schema` — both valid markdown, both have expected front-matter keys.

#### C5.7 — Create thin SKILL.md
- **Files:** `template/.claude/skills/tech-watch/SKILL.md`, `.claude/skills/tech-watch/SKILL.md`
- **Do:** Write per spec §3.5. ≤100 lines. Identical content in both trees (no Jinja vars).
- **Verify:** `wc -l template/.claude/skills/tech-watch/SKILL.md` ≤ 100. `diff template/.claude/skills/tech-watch/SKILL.md .claude/skills/tech-watch/SKILL.md` → zero.

#### C5.8 — Delete old radar and audit-repo directories
- **Do:** `git rm -r template/.claude/skills/radar/`. `git rm -r .claude/skills/audit-repo/`. `git rm -r scripts/audit_repo/` (meta).
- **Verify:** `ls template/.claude/skills/radar 2>&1` not found; same for meta `audit-repo`.

#### C5.9 — Update trigger tables
- **Files:** `CLAUDE.md`, `template/CLAUDE.md.jinja`
- **Do:** Replace `/radar` row with `/tech-watch` row. Remove any `/audit-repo` row from meta CLAUDE.md (it was meta-specific). Update descriptions and triggers to reflect the fusion (one skill, two modes, invoked differently).
- **Verify:** `grep -c "/radar" CLAUDE.md template/CLAUDE.md.jinja` → 0. `grep -c "/tech-watch" CLAUDE.md template/CLAUDE.md.jinja` → ≥1 each.

#### C5.10 — Update tests
- **File:** `tests/test_template_generation.py`
- **Do:** In `TestSkills.EXPECTED_SKILLS`, replace `"radar"` with `"tech-watch"`. Add `TestTechWatch::test_sweep_mode_produces_card` (generate project, run sweep dry-run, assert card emitted). Add `test_deep_mode_produces_card` (run deep on a public repo, assert card emitted). Update `TestMetaParity` if the whitelist previously excluded `audit-repo` — remove the whitelist entry.
- **Verify:** `uv run pytest tests/test_template_generation.py -v` — green.

#### C5.11 — Update cross-references
- **Do:** `grep -rln "/radar\|/audit-repo" .meta/ README.md template/.claude/skills/ .claude/skills/ | grep -v drafts/ | grep -v archive/` — for each hit, decide: rename to `/tech-watch` if it's a live doc; leave if it's a historical archive or draft.
- **Verify:** Only archived/draft files still contain the old names.

#### C5.12 — Commit
```bash
git add -A
git commit -m "feat(tech-watch): fuse /radar + /audit-repo into /tech-watch with unified card schema (sweep + deep modes)"
```

---

## Commit C6 — Doc cascade

**Goal:** update all narrative documentation: ADR, ARCHITECTURE, PILOT, CHANGELOG, README, and the skills memo.

### Files involved

- `.meta/decisions/adr-007-skills-architecture.md` (new — or next NNN)
- `.meta/ARCHITECTURE.md` — supersede ADR-006
- `.meta/DECISIONS.md` — add ADR-007 row
- `.meta/PILOT.md` — update skill count, add v1.6.0 changelog line, update roadmap
- `CHANGELOG.md` — add v1.6.0 section
- `README.md` — rewrite skill listing, update command examples
- Memory files (external, `C:\Users\Vincent\.claude\projects\...`) — flag backlog entry as closed

### Tasks

#### C6.1 — Write ADR-007
- **File:** `.meta/decisions/adr-007-skills-architecture.md`
- **Do:** Follow the ADR-001 to ADR-006 format. Context: audit of v1.5.0 found broken contracts and fake dogfooding. Decision: dual-maintenance meta ↔ template, mechanical contract check, fusion of /radar + /audit-repo into /tech-watch. Reasoning: debate record. Consequence: v1.6.0 invariants.
- **Verify:** `test -f .meta/decisions/adr-007-skills-architecture.md`.

#### C6.2 — Supersede ADR-006 in ARCHITECTURE.md
- **File:** `.meta/ARCHITECTURE.md`
- **Do:** Mark ADR-006 as `Status: Superseded by ADR-007`. Add ADR-007 as a new section with the 10-skill inventory and the dual-maintenance rule.
- **Verify:** `grep -A2 "ADR-006" .meta/ARCHITECTURE.md | grep "Superseded"`.

#### C6.3 — Update DECISIONS.md index
- **File:** `.meta/DECISIONS.md`
- **Do:** Add ADR-007 to the index table.

#### C6.4 — Update PILOT.md
- **File:** `.meta/PILOT.md`
- **Do:** Vision "8+ skills" → "10 skills"; add v1.6.0 changelog line "skills architecture overhaul — ghost agents deleted, contract check shipped, tech-watch fusion, meta dogfooding symmetric". Update roadmap table if applicable.

#### C6.5 — Update CHANGELOG
- **File:** `CHANGELOG.md`
- **Do:** Add v1.6.0 section with Added / Changed / Removed / Fixed / Migration notes. Flag it as a structural release.
- **Verify:** `grep "v1.6.0" CHANGELOG.md`.

#### C6.6 — Update README
- **File:** `README.md`
- **Do:** Rewrite skill listing (10 skills, no ghost agents). Update command examples from `/radar` to `/tech-watch`. Add migration note for v1.5.0 users upgrading via `copier update`.
- **Verify:** `grep -c "/radar" README.md` → 0; `grep "/tech-watch" README.md` → ≥1.

#### C6.7 — Commit
```bash
git add .meta/decisions/adr-007-skills-architecture.md .meta/ARCHITECTURE.md \
        .meta/DECISIONS.md .meta/PILOT.md CHANGELOG.md README.md
git commit -m "docs(v1.6.0): ADR-007 skills architecture, ARCHITECTURE supersede, PILOT + CHANGELOG + README cascade"
```

---

## Commit C7 — Tag v1.6.0

**Goal:** annotated semver tag with changelog summary, push to origin.

### Tasks

#### C7.1 — Final sanity sweep
- **Do:** `uv run pytest` full suite. `pre-commit run --all-files`. `copier copy . /tmp/test-v1.6.0 --defaults --trust --vcs-ref=HEAD` — new project generates cleanly, `cd /tmp/test-v1.6.0 && pre-commit run --all-files` — green.
- **Verify:** all three green.

#### C7.2 — Tag
- **Do:**
  ```bash
  git tag -a v1.6.0 -m "$(cat <<'EOF'
  v1.6.0 — Skills architecture overhaul

  Added:
  - scripts/check_skills_contract.py — pre-commit hook asserting every
    trigger-table row maps to a real artifact (skill file or agent file)
  - .claude/settings.json (meta) — committed session settings for the
    meta-repo; dogfooding is now explicit, not aspirational
  - .meta/GUIDELINES.md (meta) — symmetric with template output
  - .claude/agents/ and .claude/rules/ (meta) — meta now mirrors the
    template's full .claude/ tree
  - 4 new local agents shipped in both meta and template:
    - code-reviewer (auto on ≥3 files touched): post-implementation review,
      CRITICAL/WARN/NIT tiered, distinct from devils-advocate
    - test-engineer (propose on new module/API): generative test author
    - security-auditor (propose on auth/secrets/input/crypto/network/fs):
      OWASP sweep scoped to touched code
    - data-analyst (propose on ETL/metric/statistical claim): catches
      sampling bias, leakage, reproducibility gaps
  - /tech-watch unified skill — fuses /radar (sweep) and /audit-repo (deep)
    into a single skill with a shared card schema at
    .meta/references/research/
  - scripts/tech_watch/ package — sweep/ and deep/ submodules
  - tests: TestSkillsContract, TestMetaParity (skills + agents), TestAgents,
    TestTechWatch

  Changed:
  - CLAUDE.md (meta + template) trigger tables: 4 ghost agents that
    previously advertised unshipped functionality are now real, invocable
    agent files
  - "Recommended plugin" section strengthened to make the fallback
    relationship explicit: local brainstorm/plan/spec/debate/orchestrate/
    research/test/save-progress are fallbacks; superpowers plugin ships
    superior versions and is preferred when installed; the 4 local agents
    are additive
  - /test and /save-progress thinned under the skill-vs-tool filter
  - ADR-006 (5 skills) superseded by ADR-007 (10 skills + 5 agents +
    dual-maintenance dogfooding rule)
  - README skill listing rewritten for the new inventory

  Removed:
  - /radar skill and scripts/radar/ package — absorbed into /tech-watch
  - /audit-repo skill (meta) and scripts/audit_repo/ — absorbed into /tech-watch
  - scripts/tech_watch.py (meta legacy single-file, v1.0.0 orphan)
  - stale meta .claude/skills/research/ (was v1.4.0 era) — synced with
    template v1.5.0 thin version

  Migration notes for v1.5.0 → v1.6.0 via copier update:
  - /radar invocations become /tech-watch (no args = sweep, same behavior)
  - /audit-repo invocations become /tech-watch <url> (deep mode)
  - Card output path is unchanged: .meta/references/research/
  - Card schema is extended but backward compatible — old cards still parse
  - 4 new agents appear under .claude/agents/ — nothing to migrate
  EOF
  )"
  git push origin main v1.6.0
  ```
- **Verify:** `git tag -l v1.6.0` returns `v1.6.0`. `git log --oneline -8` shows C1..C6 + tag.

---

## Global pre-conditions

Before starting C1:

- Working tree clean (`git status` shows only `.meta/scratch/` untracked)
- On `main`, at `31e8778` (v1.5.0 HEAD)
- `uv sync` succeeded
- `uv run pytest` passes on current state

## Global post-conditions

After C7:

- `git tag -l` shows `v1.6.0`
- `uv run pytest` passes
- `uv run python scripts/check_skills_contract.py` exits 0
- `copier copy . /tmp/final-check --defaults --trust --vcs-ref=HEAD` generates a project that passes its own pre-commit run
- `.meta/drafts/skills-architecture-audit.md` and `.meta/drafts/spec-skills-architecture.md` and `.meta/drafts/plan-skills-architecture.md` moved to `.meta/archive/` with proper date-stamped filenames (follow-up hygiene step after C7, optional)

---

## Risks and rollback

**If C5 (tech-watch fusion) goes wrong:**
- The commit is self-contained. `git revert` restores v1.5.0 state. The contract script will fail because ghost agents are back in the trigger table — acceptable, rollback is explicitly emergency.
- Alternative: abort mid-fusion by reverting only the problematic file moves; the SKILL.md rewrites can be rolled back independently.

**If the contract script has a false positive:**
- Adjust the allowlist in `scripts/check_skills_contract.py`. New script version ships in the same commit as the adjustment.

**If `copier update` from v1.5.0 to v1.6.0 breaks downstream projects:**
- Low risk in practice (only Vincent's own projects depend on this template as of 2026-04-14). Migration notes in the CHANGELOG cover the 3 breaking renames.

---

## Estimated effort

| Commit | LOC delta | Time |
|---|---|---|
| C1 Honesty | ~20 | 15 min |
| C2 Contract script | ~150 | 45 min |
| C3 Meta dogfooding | ~50 net (mostly copies) | 40 min |
| C3a Ship 4 agents | ~500 new (8 files × ~100 lines + rows + tests) | 2 h |
| C4 Thin skills | ~-100 net | 30 min |
| C5 Tech-watch fusion | ~+300 new, ~-200 deleted | 2-3 h |
| C6 Doc cascade | ~200 | 45 min |
| C7 Tag | 0 | 5 min |
| **Total** | **~900 net** | **~7 h** |

This fits a single focused session. If any single commit blows up, stop at the previous one and ship that as v1.5.1 instead of v1.6.0.

**Full-auto execution note:** per user directive 2026-04-14, run all 8 commits without intermediate validation. Stop only on (a) test failures that cannot be self-resolved, (b) pre-commit hook failures that require design judgment, (c) deviation from the plan itself discovered during execution. For all normal decisions (filename choice, exact prompt wording for agents, import path after refactor), use best judgment without pausing.
