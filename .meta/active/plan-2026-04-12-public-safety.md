---
type: plan
date: 2026-04-12
slug: public-safety
status: active
---

# Plan — Pre-public safety audit (P2)

Implements `spec-2026-04-12-public-safety.md`. Seven commit-sized tasks.

## T1 — Core audit script

**Files:** `scripts/audit_public_safety.py`

**Steps:**
1. Write the script with:
   - `argparse` CLI: `--mode` choice `full` / `quick`, default `full`; positional `FILE...` for quick mode
   - `check_sensitive_files_tracked()` — uses `git ls-files`, matches filename denylist via `fnmatch`
   - `check_gitignore_coverage()` — calls `git check-ignore --no-index --quiet PATH` for each canonical path
   - `check_secret_patterns(files)` — walks given files (or all tracked in full mode), skips binaries (null-byte detection in first 8192 bytes), skips `scripts/audit_public_safety.py` and `.meta/archive/**`, runs regex patterns, prints `<REDACTED>` placeholders
   - `main()` — dispatches on mode, aggregates results, prints report with ANSI colors if `sys.stdout.isatty()`, exits 0/1/2
2. Manual run on current repo:
   - `uv run python scripts/audit_public_safety.py --mode=full` → must exit 0 (AC7 clean baseline)
3. Plant a test secret in a throwaway file, run script, confirm detection with `<REDACTED>`, remove file
4. Run `uv run ruff check scripts/audit_public_safety.py && uv run ruff format scripts/audit_public_safety.py`

**Commit:** `feat(scripts): add public-safety audit script`

## T2 — Register pre-commit hook (meta-repo)

**Files:** `.pre-commit-config.yaml`

**Steps:**
1. Add new local hook `audit-public-safety-quick` after `check-git-author`:
   ```yaml
   - id: audit-public-safety-quick
     name: Quick secret scan on staged files
     entry: python scripts/audit_public_safety.py --mode=quick
     language: system
     pass_filenames: true
   ```
2. `uv run pre-commit run --all-files` → must pass

**Commit:** `feat(pre-commit): register public-safety quick scan hook`

## T3 — GitHub Actions — `public-safety.yml` (push/PR gate)

**Files:** `.github/workflows/public-safety.yml` (create directory if missing)

**Steps:**
1. Write workflow per spec §4 (push + PR on main, checkout, setup-uv, uv sync, run audit in full mode)
2. Validate YAML: `python -c "import yaml; yaml.safe_load(open('.github/workflows/public-safety.yml'))"`

**Commit:** `feat(ci): add public-safety audit workflow on push and PR`

## T4 — GitHub Actions — `public-alert.yml` (reactive on public)

**Files:** `.github/workflows/public-alert.yml`

**Steps:**
1. Write workflow per spec §4 with `on: public` trigger, `continue-on-error` on audit step, conditional `github-script@v7` step that opens an issue on failure
2. Validate YAML parseable
3. Sanity-check the `issues.create` payload structure (labels array, body multiline string)

**Commit:** `feat(ci): add reactive audit workflow on repo publicization`

## T5 — Template propagation

**Files:**
- `template/scripts/audit_public_safety.py` (copy of T1)
- `template/.pre-commit-config.yaml` (add hook)
- `template/.github/workflows/public-safety.yml` (copy of T3)
- `template/.github/workflows/public-alert.yml` (copy of T4)

**Steps:**
1. Copy `scripts/audit_public_safety.py` to `template/scripts/audit_public_safety.py` (byte-identical)
2. Register the hook in `template/.pre-commit-config.yaml` (same block as T2)
3. Create `template/.github/workflows/` directory, copy both workflow files (plain `.yml`, not `.jinja` — no substitution needed)
4. Smoke-test template generation:
   - `copier copy . /tmp/test-p2 --defaults --trust --vcs-ref=HEAD`
   - Verify: script present, pre-commit hook entry present, both workflows present
   - Validate YAML of both generated workflow files

**Commit:** `feat(template): propagate public-safety audit to generated projects`

## T6 — README documentation

**Files:** `README.md`

**Steps:**
1. Add a new section "Before going public" after "Execution modes" (or before "Stack")
2. Content per spec §5:
   - The four contact points (brief bullet list)
   - Manual run command
   - Branch protection `gh` command (copy-paste ready, with `OWNER/REPO` placeholder)
   - How to enable GitHub native Secret Scanning + Push Protection (Settings path)
3. Also add a row in the "What You Get" table: `Public safety audit — stdlib script + pre-commit hook + 2 GitHub workflows, propagated to every generated project`

**Commit:** `docs(readme): document public-safety audit and pre-publish procedure`

## T7 — Final acceptance matrix

**Files:** none (validation only)

**Steps:**
1. Walk AC1–AC12 one by one, test each:
   - AC1 — script exists, ruff passes
   - AC2 — plant `test_leak.env`, run, confirm detection, cleanup
   - AC3 — temporarily rename a `.gitignore` entry, run, confirm detection, restore
   - AC4 — plant AWS example key in throwaway file, confirm `<REDACTED>` output, cleanup
   - AC5 — `--mode=quick scripts/audit_public_safety.py` runs fast and only secret-scans
   - AC6 — commit with planted secret is rejected
   - AC7 — clean baseline, exit 0
   - AC8 — both workflows parse as valid YAML
   - AC9 — generated project has all four pieces
   - AC10 — README sections present
   - AC11 — never prints raw secret content
   - AC12 — pre-commit green on meta-repo
2. Matrix generation (smoke): safe+public, safe+private, full-auto+public, full-auto+private — all four contain the audit pieces

**Commit (if fixes needed):** `fix(public-safety): <specific fix>`

No new commit if all ACs pass first try — T1–T6 are the deliverable.

## Commit granularity rationale

Six feature/doc commits + optional fix. Each is independently reviewable and bisectable:
- T1 ships the script (no hook, no CI, no template) — repo still works, nothing references the script yet
- T2 wires pre-commit — depends on T1 but fails gracefully if script is missing (hook fails loud, not silent)
- T3 and T4 are CI workflows — independent of T2, fire in CI only
- T5 propagates to template — depends on T1–T4 being stable
- T6 is pure doc — independent

Strict order: T1 first (everything else references it). T2, T3, T4 can interleave. T5 must come last among the code commits. T6 can come anywhere after T1.

## Rollback

- If the script has a false positive on clean baseline: fix forward in T1 (iterate regex patterns), not revert
- If a GitHub workflow breaks CI: `git revert` only the workflow commit; script + pre-commit stay functional locally
- If template propagation breaks generation: `git revert` T5; downstream users lose the audit but existing generation flow is intact
