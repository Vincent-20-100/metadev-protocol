# v2.0.0 Design — Multi-host distribution + Librarian agent + Harness audit

**Date:** 2026-04-16
**Status:** Draft — pending user review
**Based on:** PM.15 deep audit of 7 repos (caveman, everything-claude-code, gstack, claude-mem, BMAD-METHOD, graphify, deepagents)
**Breaking:** Yes (v1.6.0 → v2.0.0). Additive breaking — no files deleted or renamed, only additions and modifications.

---

## Context

PM.15 audited 7 repos to inform metadev-protocol's next structural direction. Three convergent findings emerged:

1. **Multi-IDE converges towards "registry + dispatcher + per-host variants"** — 5/7 sources (caveman, gstack, graphify, BMAD, ECC) independently arrived at the same pattern: one source of truth, one sync mechanism, N host-native destinations.
2. **Claude Code IS the agent harness** — deepagents demonstrated that building a custom runtime harness is unnecessary; the right move is reframing metadev's existing skills + agents using the middleware-stack vocabulary (todos → fs → subagents → summarization → permissions-last).
3. **Benchmarks/evals first-class by convergence** — 3 sources (caveman, gstack, ECC) each ship different but complementary eval harnesses. The minimal viable version is a deterministic scorecard (ECC pattern).

Additionally, the EgoVault Knowledge Compiler architecture (3-tier: raw chunks → compiled notes → compiled context, with a Librarian tool using isolated context) inspired a new local agent: the librarian, which curates deep-source context on behalf of the conversational agent, enforced by a deterministic PreToolUse gate.

---

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Breaking appetite | v2.0.0 (scope strict) | One moment of downstream pain, additive only |
| `.meta/` taxonomy | Untouched | Core project identity, already validated |
| Distribution mechanism | Caveman CI fan-out | Zero runtime, copier-native, validated at 31k★ |
| Multi-host scope | Tier 1: Claude Code + Codex + Gemini | 3 LLM providers, ~8 lines added, tier 2/3 documented for v2.1+ |
| Evals | Harness scorecard (deterministic) | Extension of contract check, $0 cost, CI-safe |
| Agent harness | None (Claude Code is the harness) | deepagents insight — reframe vocabulary, don't build runtime |
| Librarian agent | 6th local agent, read-only curator | Inspired by EgoVault Knowledge Compiler, curate() tier 0/1 pattern |
| Deep-source gate | PreToolUse hook blocking Read on .meta/references/ | Deterministic enforcement, forces librarian usage |

---

## Delivery: 4 trains

### Train 1 — Librarian agent + deep-source gate (`v2.0.0-alpha.1`)

**Files created:**

- `template/.claude/agents/librarian.md` — 6th local agent, dual meta + template
  - Mandate: read-only context curator, cherry-picks from deep sources
  - Process: receives question → Grep in `.meta/references/`, `docs/`, `src/` → Bash extraction (sed/head) → optional tier 1 LLM synthesis → returns {extracts, synthesis, sources, confidence}
  - Hard rules: never modifies files, max 5 extracts of 30 lines each, confidence = source-count-based (1=low, 2=medium, 3+=high), says "nothing found" instead of fabricating
  - Trigger: **Propose** (not Auto) — conversational agent asks user before dispatching
- `.claude/agents/librarian.md` — meta mirror
- `template/scripts/gate_deep_sources.py` (~20 LOC) — reads `tool_input.file_path` from stdin JSON, exits 1 if path matches `.meta/references/`, exits 0 otherwise
- `scripts/gate_deep_sources.py` — meta mirror

**Files modified:**

- `template/.claude/settings.json.jinja` — add PreToolUse hook entry:
  ```json
  { "matcher": "Read", "hooks": [{ "type": "command", "command": "python scripts/gate_deep_sources.py" }] }
  ```
- `.claude/settings.json` — meta: same hook added
- `template/CLAUDE.md.jinja` — add librarian trigger row
- `CLAUDE.md` — meta: same row
- `tests/test_template_generation.py` — TestAgents.EXPECTED_AGENTS adds "librarian" (6 total), new TestLibrarianGate class

**Whitelist for gate exceptions:**

The gate script accepts an optional `--allow` flag or env var for skills/agents that legitimately need Read access to `.meta/references/` (e.g., `/save-progress` summarizing recent work). Whitelist is maintained in the script, not in settings.json.

**Access hierarchy (enforced):**

| Source tier | Conversational agent | Librarian agent |
|---|---|---|
| Gold (CLAUDE.md, PILOT.md, rules/, skills/) | Read ✅ | Read ✅ |
| Deep (.meta/references/, docs/) | Read ❌ (gate blocks) | Grep + Bash ✅ |
| Code (src/, tests/, scripts/) | Read ✅ | Grep + Bash ✅ |

**Risks:**

| Risk | Mitigation |
|---|---|
| Librarian invoked too often | Trigger = Propose, user decides |
| Gate blocks legitimate use | Whitelist mechanism in gate script |
| Grep returns too much noise | Hard rule: max 5 extracts × 30 lines = 150 lines cap |

---

### Train 2 — Multi-host CI fan-out + LLM stubs (`v2.0.0-alpha.2`)

**Files created:**

- `template/sync-config.yaml` — host registry declaring Claude (primary), Codex (import-stub), Gemini (import-stub). Tier 2/3 hosts documented as comments.
- `template/scripts/sync_hosts.py` (~80-120 LOC, stdlib-only) — reads sync-config.yaml, generates host variants:
  - `import-stub` format: 4-line Markdown pointing to CLAUDE.md (for Codex, Gemini)
  - `cursorrules` format (tier 2, future): strip frontmatter, write .mdc
  - `markdown-flat` format (tier 2, future): copy with section stripping
  - Idempotent. `--check` mode verifies stubs are up-to-date without writing (exit 1 on drift).
- `template/AGENTS.md` — generated import stub (~4 lines), never hand-edited
- `template/GEMINI.md` — generated import stub (~4 lines), never hand-edited
- `template/.github/workflows/sync-hosts.yml` — CI workflow triggered on `.claude/skills/**`, `.claude/agents/**`, `CLAUDE.md`, `sync-config.yaml` changes. Auto-commits regenerated stubs if drifted.
- Meta mirrors: `sync-config.yaml`, `scripts/sync_hosts.py`, `AGENTS.md`, `GEMINI.md`

**Files modified:**

- `template/.pre-commit-config.yaml` — add `sync-hosts` hook (runs `sync_hosts.py --check`)
- `template/CLAUDE.md.jinja` — update trigger table: `/tech-watch` description mentions multi-host support
- `CLAUDE.md` — meta: same
- `tests/test_template_generation.py` — new TestMultiHost class (agents_md_is_stub, gemini_md_is_stub, sync_script_present, sync_config_present, sync_check_passes)

**Import stub content (AGENTS.md and GEMINI.md identical pattern):**

```markdown
<!-- Auto-generated by scripts/sync_hosts.py — do not edit manually -->
<!-- Source of truth: CLAUDE.md + .claude/ -->
Read CLAUDE.md for all instructions, skills, and agent definitions.
All skills and agents defined there apply to this environment.
```

**Tier 2/3 expansion path (documented in sync-config.yaml comments):**

To add Cursor support in v2.1:
1. Uncomment the `cursor:` block in `sync-config.yaml`
2. Run `python scripts/sync_hosts.py`
3. Commit the generated `.cursor/rules/` files
4. Add to CI sync workflow paths

Zero code changes required — the sync script already handles the `cursorrules` format.

---

### Train 3 — Harness audit v2 (`v2.0.0-alpha.3`)

**Files created:**

- `template/evals/__init__.py`
- `template/evals/harness_audit.py` (~150-200 LOC) — deterministic scorecard, 7 categories:

| Category | Max | What it checks |
|---|---|---|
| Skills | 10 | 10 skills present, each SKILL.md ≤100 LOC, output-schema where applicable |
| Agents | 10 | 6 agents present, frontmatter valid (name, description, model) |
| Hosts | 10 | AGENTS.md + GEMINI.md exist, are import-stubs, sync check passes |
| Contract | 10 | Trigger table ↔ filesystem (delegates to check_skills_contract.py) |
| Gate | 10 | gate_deep_sources.py present, wired in settings.json PreToolUse hooks |
| Taxonomy | 10 | .meta/ dirs correct (active/, archive/, drafts/, decisions/, references/{raw,interim,synthesis}/) |
| Safety | 10 | audit_public_safety.py + check_git_author.py + check_meta_naming.py present, pre-commit wired |

  Output: text report (category scores + issues) and `--json` mode for CI.
  Runs in two modes: `--self` (audit the metadev repo itself) and default (audit a generated project).
- Meta mirror: `evals/` directory
- CI: new step in `.github/workflows/ci.yml` running harness audit on the test matrix

**Files modified:**

- `tests/test_template_generation.py` — TestHarnessAudit: test_perfect_score_on_fresh_project (70/70), test_json_output_valid

**Future eval tiers (documented, not shipped):**

- **Tier B (v2.1+):** Snapshot tests — freeze rendered SKILL.md content, break on drift without explicit snapshot update. Diff-based touchfile selection (gstack pattern) to run only affected snapshots.
- **Tier C (v3+):** LLM-judge — run a skill on a fixture, capture output, judge quality via LLM. Caveman 3-arm pattern (skill vs terse-control vs baseline).

---

### Train 4 — Doc cascade + tag v2.0.0

**Files created:**

- `.meta/decisions/adr-011-v2-multi-host-librarian.md` — full ADR: context (PM.15 audit), decision (multi-host fan-out + librarian + harness audit), consequences (v2.0 invariants), rejected alternatives

**Files modified:**

- `.meta/ARCHITECTURE.md` — inline ADR-011 section
- `.meta/DECISIONS.md` — append ADR-011 row
- `.meta/PILOT.md` — PM.15 DONE, v2.0.0 changelog, agent count 5→6
- `CHANGELOG.md` — v2.0.0 section (Added / Changed / Migration notes)
- `README.md` — multi-host mention, 6 agents, 5 guardrails, harness audit, librarian
- `CREDITS.md` — caveman (CI fan-out), deepagents (middleware vocabulary), EgoVault Knowledge Compiler (librarian inspiration)

**Tag:** `v2.0.0` annotated with full changelog + migration notes.

**Migration notes v1.6.0 → v2.0.0:**
- New files: AGENTS.md, GEMINI.md, evals/, scripts/sync_hosts.py, sync-config.yaml, .claude/agents/librarian.md, scripts/gate_deep_sources.py
- settings.json gains PreToolUse hook — may conflict if customized
- .pre-commit-config.yaml gains sync-hosts hook
- No files deleted, no renames
- Downstream action: `copier update`, resolve conflicts in settings.json and .pre-commit-config.yaml if customized

---

## What is NOT in v2.0.0

| Feature | Why not | When |
|---|---|---|
| Cursor / Windsurf / Cline support | Can't dogfood what we don't use. Documented in sync-config.yaml comments. | v2.1+ when dogfooded |
| Snapshot eval tests (tier B) | Need stable skill content first | v2.1+ |
| LLM-judge eval (tier C) | Cost + complexity, not enough testable skills yet | v3+ |
| Memory architecture (Knowledge Compiler) | EgoVault scope, not metadev template scope | EgoVault project |
| Custom agent harness | Claude Code IS the harness (deepagents insight) | Never |
| .meta/ taxonomy changes | Core identity, validated, no reason to touch | Never |
| XML workflow DSL (BMAD) | Interesting but alien to metadev's Markdown-first philosophy | Revisit if skill count >15 |
| Surprise scoring (graphify) | No card pipeline in template to score against | v2.1+ with /tech-watch maturity |
