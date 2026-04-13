---
type: plan
date: 2026-04-13
slug: tech-watch-script
status: active
---

# Plan — Tech watch script (PM.3)

**Goal:** A stdlib-first Python script that queries the GitHub Search API for
trending repos on AI-coding topics and appends structured results to
`.meta/references/raw/` so the meta-repo accumulates a living feed of
references to mine for cross-pollination (PM.4 synthesis, PM.6 audits).

**Scope:** meta-repo only. NOT shipped in the template.

**Confidence:** GREEN — all decisions locked, full-auto ready.

---

## Decisions (locked)

| # | Decision | Chosen | Reason |
|---|---|---|---|
| D1 | Placement | meta-repo only (`scripts/tech_watch.py`) | Personal curation tool, not a user-facing feature |
| D2 | Runtime | Python stdlib only (`urllib.request`, `json`, `pathlib`, `hashlib`, `datetime`) | GUIDELINES stdlib-first; zero deps |
| D3 | Auth | `GITHUB_TOKEN` env var, loaded from `.env` via manual parser | User wants reuse of personal token; `.env` already gitignored |
| D4 | `.env` parser | ~15 lines, reads `KEY=value`, ignores comments and blank lines | Avoid `python-dotenv` dep |
| D5 | Source | GitHub Search API `/search/repositories` only | No HN/Reddit/news scraping in v1 — scope discipline |
| D6 | Topics | `claude-code`, `agentic-coding`, `ai-coding`, `copier`, `llm-agents`, `claude-sdk` | Direct match with our positioning |
| D7 | Query shape | `topic:<t> pushed:>YYYY-MM-DD sort:stars-desc` per topic, `pushed:` window = 30 days | Recent activity filter |
| D8 | Output file | `.meta/references/raw/session-YYYY-MM-DD-tech-watch.md` | Fits existing meta naming (type `session`) |
| D9 | Dedup | SHA256(repo_full_name) cache in `.meta/references/raw/.tech-watch-seen.json`, gitignored | Prevent re-listing repos across runs |
| D10 | Rate limit handling | Fail fast with clear error on 403/401; no retry loop | Simplicity; user re-runs manually |
| D11 | Output columns | `repo` / `stars` / `pushed` / `description` / `topics` / `url` | Minimum viable for downstream synthesis |
| D12 | Nightshift hook | None in v1 — pure one-shot CLI | User confirmed: "on pluggera au moment de faire le nightshift" |
| D13 | Unauth fallback | No — hard error if `GITHUB_TOKEN` missing | Unauth rate limit (60/h) is not viable for 6 topics |

---

## Tasks

### Task 1 — `.env` setup

- [ ] Create `.env.example` at meta-repo root with `GITHUB_TOKEN=` placeholder and a comment pointing to https://github.com/settings/tokens (scope: public_repo)
- [ ] Verify `.env` is in `.gitignore` (already done, line 10-11)
- [ ] Document in `CLAUDE.md` under "Commands" section: how to create the token

**Files:**
- `.env.example` (new)
- `CLAUDE.md` (one-line addition under Commands)

### Task 2 — Script skeleton

- [ ] Create `scripts/tech_watch.py` with:
  - Module docstring explaining purpose and usage
  - `load_env(path: Path) -> dict[str, str]` — minimal `.env` parser
  - `github_search(topic: str, since: str, token: str) -> list[dict]` — one `urllib.request.Request` with `Authorization: Bearer ...`
  - `format_row(repo: dict) -> str` — markdown table row
  - `load_seen(path: Path) -> set[str]` / `save_seen(path: Path, seen: set[str])` — SHA256 cache
  - `main()` — CLI entry, writes output file, prints summary
- [ ] Shebang `#!/usr/bin/env python3`, `from __future__ import annotations`
- [ ] Use `argparse` for `--since DAYS` (default 30) and `--topics t1,t2,...` (default list from D6)

**Files:**
- `scripts/tech_watch.py` (new)

### Task 3 — Output format

Target output file header:
```markdown
---
type: session
date: YYYY-MM-DD
slug: tech-watch
status: active
---

# Tech watch — YYYY-MM-DD

**Topics:** claude-code, agentic-coding, ai-coding, copier, llm-agents, claude-sdk
**Window:** last 30 days
**New this run:** N repos

| Repo | Stars | Pushed | Topics | Description | URL |
|------|-------|--------|--------|-------------|-----|
| ... | ... | ... | ... | ... | ... |
```

Filename respects `check_meta_naming.py` — `session-YYYY-MM-DD-tech-watch.md` under `.meta/references/raw/`. Since `raw/` is NOT a guarded dir, filename convention does not apply, but we use it anyway for consistency.

- [ ] Escape `|` in descriptions (replace with `\|`) to keep the table valid
- [ ] Truncate descriptions at 120 chars with `…`
- [ ] If zero new repos this run, still write a file with "no new entries" note (audit trail)

### Task 4 — Error handling

- [ ] Missing `GITHUB_TOKEN` → `sys.exit("tech_watch: GITHUB_TOKEN missing (set in .env)")`
- [ ] HTTP 401/403 → print response body and exit non-zero
- [ ] HTTP 200 but malformed JSON → exit non-zero with raw response preview
- [ ] Network error (`urllib.error.URLError`) → exit non-zero with message

No try/except swallowing. Fail fast.

### Task 5 — Smoke test

- [ ] Manually run `GITHUB_TOKEN=xxx python scripts/tech_watch.py --since 7` and verify:
  - A `.meta/references/raw/session-YYYY-MM-DD-tech-watch.md` is created
  - `.tech-watch-seen.json` is created and populated
  - Second run produces "no new entries" file (or very few) proving dedup works
  - `uv run ruff check scripts/tech_watch.py` passes
- [ ] No pytest integration test in v1 (external API dependency, not worth the mocking)

---

## Verification checklist

- [ ] `scripts/tech_watch.py` runs end-to-end with a real token
- [ ] Dedup cache prevents listing the same repo twice across runs
- [ ] Output file is valid markdown, opens cleanly in VS Code
- [ ] `ruff check` + `ruff format` pass
- [ ] `.env.example` documents the required token scope
- [ ] `CLAUDE.md` "Commands" section mentions `python scripts/tech_watch.py`
- [ ] No new dependencies in `pyproject.toml` (stdlib-only confirmed)
- [ ] Script is idempotent — second run without new repos produces empty result, not errors

---

## Out of scope (deferred)

- News / HN / Reddit / newsletter fetchers — v2 if ever
- Auto-enrichment (why-relevant column with LLM reasoning) — feeds PM.4 synthesis, separate task
- Nightshift orchestration wrapper — PM.4 / Nightshift micro-project
- Cron / scheduled run — user runs manually
- Multi-language topic coverage (e.g., Rust, Go AI tooling) — Python-first bias acceptable for v1

---

## File summary (for full-auto execution)

**New files:**
- `.env.example`
- `scripts/tech_watch.py`
- `.meta/references/raw/.tech-watch-seen.json` (created at first run, gitignored)

**Modified files:**
- `CLAUDE.md` (Commands section: one line)
- `.gitignore` (add `.meta/references/raw/.tech-watch-seen.json`)

**Commit:** `feat(tools): add tech watch script for AI-coding repo discovery`
