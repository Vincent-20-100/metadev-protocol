# PR-4 Part B — Hard-block DX audit (narrow scope)

**Date:** 2026-04-21
**Status:** COMPLETE
**Agent:** Sonnet, incremental write mode

## Progress tracker

- [x] H001-H010 analyzed
- [x] H011-H020 analyzed
- [x] H021-H030 analyzed
- [x] H031-H033 analyzed

---

## Hook inventory (as mapped from synthesis + actual files)

| H-ID | Hook id / mechanism | Location |
|---|---|---|
| H001 | `ruff` (lint --fix) | meta-repo `.pre-commit-config.yaml` |
| H002 | `ruff-format` | meta-repo `.pre-commit-config.yaml` |
| H003 | `check-meta-naming` | meta-repo `.pre-commit-config.yaml` |
| H004 | `check-git-author` | meta-repo `.pre-commit-config.yaml` |
| H005 | `check-coauthor-trailer` | meta-repo `.pre-commit-config.yaml` |
| H006 | `audit-public-safety-quick` (--mode=quick, staged files) | meta-repo `.pre-commit-config.yaml` |
| H007 | `check-skills-contract` | meta-repo `.pre-commit-config.yaml` |
| H008 | `sync-hosts` (--check) | meta-repo `.pre-commit-config.yaml` |
| H009 | `trailing-whitespace` | meta-repo `.pre-commit-config.yaml` |
| H010 | `end-of-file-fixer` | meta-repo `.pre-commit-config.yaml` |
| H011 | `check-yaml` | meta-repo `.pre-commit-config.yaml` |
| H012 | `check-toml` | meta-repo `.pre-commit-config.yaml` |
| H013 | `no-commit-to-branch main` | template `.pre-commit-config.yaml` |
| H014 | `ruff` (lint --fix) | template `.pre-commit-config.yaml` |
| H015 | `SessionStart` welcome (PILOT.md head-30) | meta-repo `.claude/settings.json` |
| H016 | `ruff-format` | template `.pre-commit-config.yaml` |
| H017 | `SessionStart` welcome (PILOT.md head-30) | template `.claude/settings.json.jinja` |
| H018 | `check-meta-naming` | template `.pre-commit-config.yaml` |
| H019 | `check-git-author` | template `.pre-commit-config.yaml` |
| H020 | `check-coauthor-trailer` | template `.pre-commit-config.yaml` |
| H021 | `check-skills-contract` | template `.pre-commit-config.yaml` |
| H022 | `sync-hosts` (--check) | template `.pre-commit-config.yaml` |
| H023 | CI `lint` job (ruff check + format --check) | `.github/workflows/ci.yml` |
| H024 | CI `pre-commit` job (run --all-files) | `.github/workflows/ci.yml` |
| H025 | CI `template-test` job (copier + ruff matrix) | `.github/workflows/ci.yml` |
| H026 | CI `public-safety` job (--mode=full) | `.github/workflows/public-safety.yml` |
| H027 | CI `public-alert` (repo goes public event) | `.github/workflows/public-alert.yml` |
| H028 | `audit_public_safety` check A (filename denylist) | `scripts/audit_public_safety.py` |
| H029 | `audit_public_safety` check B (.gitignore canonical paths) | `scripts/audit_public_safety.py` |
| H030 | `audit_public_safety` check C (content SECRET_PATTERNS) | `scripts/audit_public_safety.py` |
| H031 | CI `sync-hosts` check | `.github/workflows/sync-hosts.yml` |
| H032 | `save_progress_preflight` (pytest + ruff + stray-draft check) | `scripts/save_progress_preflight.py` |
| H033 | `[tool.pytest.ini_options] testpaths = ["tests"]` | `template/pyproject.toml.jinja` |

---

## Demotion candidates

| Hook ID | Current | Proposed | Rationale | Effort |
|---|---|---|---|---|
| H004 | hard-block (pre-commit) | demote to advisory | Blocks commits where git author is not set up; a fresh clone or CI environment with no author config triggers a false positive. The real risk (LLM claiming authorship) is a policy violation, not a code defect — better as a warning with a clear message than a commit-stopper that confuses legitimate contributors. | ~10 lines in script + pre-commit stage change |
| H005 | hard-block (commit-msg) | demote to advisory | Same rationale as H004 — co-author trailer check fires on any commit where the LLM forgot the trailer, converting every non-LLM-assisted commit into a manual bypass friction point; advisory surfacing is sufficient. | ~10 lines in script |
| H008 | hard-block (pre-commit) | demote to soft-warn (only when sync-config.yaml changed) | Currently fires on any change to `.claude/skills/`, `.claude/agents/`, `CLAUDE.md`, or `sync-config.yaml` — adding a new skill file in a project that never set up multi-host blocks commit until stubs are regenerated, even though the feature is not active. Single-host projects (the majority) pay friction for a multi-host invariant. | Tighten `files:` scope or gate on `sync-config.yaml` existence |
| H022 | hard-block (template pre-commit) | demote to soft-warn | Same as H008 — template ships `sync-hosts --check` unconditionally; generated projects that never configure `sync-config.yaml` hit a no-op check that may error if the script assumes file existence. Soft-warn + skip-if-no-config is cleaner DX. | ~5 lines in `sync_hosts.py` + pre-commit `verbose: true` |
| H027 | hard-block (CI on `public` event) | demote to advisory/informational | This fires a GitHub issue on repo visibility change; that's notification, not enforcement. It already uses `continue-on-error: true` on the audit step — calling it hard-block overstates its teeth. Reclassify as "informational CI alert" to match actual behavior. | Docs/label change only, zero code |
| H033 | hard-block | demote to advisory | `testpaths = ["tests"]` in pyproject.toml is pytest configuration, not a hook — it has no enforcement mechanism, it merely scopes discovery. Labeling it hard-block misrepresents what it does; if tests are absent the suite passes vacuously. Remove from hard-block category. | Docs-only |
| H015 | hard-block | demote to advisory | SessionStart outputs PILOT.md head-30 — purely informational, never fails, never blocks. Already labeled wrong as hard-block in the synthesis. Zero enforcement value; reclassify as advisory to avoid confusion. | Docs-only |
| H017 | hard-block | demote to advisory | Same as H015 — identical mechanism in template settings.json.jinja. | Docs-only |
| H032 | hard-block | keep hard-block BUT add --no-fail-fast option | `save_progress_preflight` runs pytest + ruff + stray-draft check before `/save-progress`. The block is correct, but it currently runs pytest which can be slow (> 60 s on large suites), blocking a "pause session" that should be fast. Not a demotion — needs a `--skip-tests` flag for quick-save scenarios. | ~15 lines in script |

---

## Keep as-is (audited, high value)

- **H001 / H014** — ruff lint: catches real bugs (F, B, SIM rules) on every .py file edit; auto-fix means low friction.
- **H002 / H016** — ruff-format: zero friction (formats in place), prevents style drift.
- **H003 / H018** — check-meta-naming: enforces taxonomy that the whole filing system depends on; enforcing at commit is right.
- **H006** — audit-public-safety-quick: catches secrets in staged files before they land; quick mode means low latency.
- **H007 / H021** — check-skills-contract: prevents phantom triggers and silent skills, directly affecting LLM routing correctness.
- **H009 / H010 / H011 / H012** — pre-commit-hooks standard set: mechanical auto-fix, near-zero friction, catches real YAML/TOML parse errors.
- **H013** — no-commit-to-branch main (template): correct default for generated projects with unknown contributor count; override documented in branching.md.
- **H019 / H020** — git-author checks in template: same policy concern as H004/H005 but in generated projects where the LLM-authorship risk is higher (more active AI session use). Keep hard-block there.
- **H023 / H024 / H025** — CI lint + pre-commit + template-test: necessary safety net; CI hard-blocks are appropriate because they protect main.
- **H026** — CI public-safety full: runs full A+B+C audit on every push/PR to main; correct placement.
- **H028 / H029 / H030** — audit_public_safety checks A/B/C: layered defense, each checks a different vector, all justified.
- **H031** — sync-hosts CI: double-check after push; correct (pre-commit might be skipped locally).

---

## Summary

- **Total demotion candidates: 9** (H004, H005, H008, H015, H017, H022, H027, H032 modification, H033)
- **True demotions (code change needed): 4** — H004, H005, H008, H022
- **Docs-only reclassifications: 4** — H015, H017, H027, H033
- **Enhancement (not demotion): 1** — H032 needs `--skip-tests` flag
- **Estimated PR effort:** ~3 files × ~30 lines each for code changes; 2 doc-only files
- **Biggest risk if we DON'T demote:** H008/H022 (sync-hosts on every skill/CLAUDE.md change) will become the #1 commit friction point as the skills library grows — developers will reflexively `--no-verify` which defeats all hooks.

---

### Key finding

The synthesis's hard-block labels were applied inconsistently: H015/H017 (SessionStart), H027 (public-alert), and H033 (pytest config) are called hard-block but have zero blocking behavior. The real demotion candidates with actual DX friction are H004/H005 (author checks in meta-repo) and H008/H022 (sync-hosts scope too broad for single-host projects).

---

## Implementation status (PR-4-B2, 2026-04-21)

### Already implemented before this PR
- **H008/H022** (`sync-hosts --check`) — feature flag already present in `scripts/sync_hosts.py`
  and `template/scripts/sync_hosts.py`: `if args.check and not config_exists(root): exit 0`.
  Single-host projects skip silently; multi-host invariant fully preserved.
- **H032** (`save_progress_preflight --skip-tests`) — flag already in both preflight scripts.

### Implemented in this PR
- **H004** (`check_git_author` pre-commit) — CI bypass: `if os.environ.get("CI"): return None`
  in `check_author()`. Applied to meta-repo and template scripts.
- **H005** (`check_git_author` commit-msg) — CI bypass: same guard in `check_coauthors()`.
- **H032 trailer** — `--skip-tests` now documented in both SKILL.md files with `Skip-Tests: true`
  trailer requirement; auditable in git history.

### Docs-only reclassifications (label corrections, no code)
- **H015** (SessionStart PILOT.md welcome) — reclassified: **informational**, never blocks.
- **H017** (template SessionStart welcome) — reclassified: **informational**, never blocks.
- **H027** (CI public-alert on repo visibility change) — reclassified: **informational**;
  already uses `continue-on-error: true`, enforcement label was wrong.
- **H033** (`testpaths` in pyproject.toml) — reclassified: **pytest config**, not a hook;
  no blocking mechanism, label was wrong.

### Not implemented (out of scope)
- H004/H005 CLAUDE_CODE_* conditioning (DA suggestion): CI bypass covers the real use case
  (fresh clones, CI runners). CLAUDE_CODE env var detection adds complexity without
  additional coverage — the existing forbidden-substring check already targets agent loops.
