# v2.0.0 Implementation Plan — Multi-host + Librarian + Harness Audit

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship metadev-protocol v2.0.0 with multi-host CI fan-out (Claude Code + Codex + Gemini), a librarian agent for deep-source curation, and a deterministic harness audit scorecard.

**Architecture:** 4-train delivery on `main` (trunk-based). Each train is an alpha tag. Trains 1-2 are independent (parallelizable). Train 3 depends on 1+2. Train 4 is docs + final tag. No feature flags, no branches. Every commit passes `uv run pytest` + `pre-commit run --all-files`.

**Tech Stack:** Python 3.13, uv, ruff, copier, pre-commit, pytest. All scripts are stdlib-only (no new dependencies).

**Spec:** `docs/superpowers/specs/2026-04-16-v2-multi-host-librarian-design.md`

---

## File Map

### Train 1 — Librarian agent

| Action | File | Responsibility |
|---|---|---|
| Create | `template/.claude/agents/librarian.md` | Agent definition: mandate, process, hard rules, output format |
| Create | `.claude/agents/librarian.md` | Meta mirror (identical) |
| Modify | `template/CLAUDE.md.jinja` | Add trigger row + convention aiguisee (never mention .meta/references/ as direct target) |
| Modify | `CLAUDE.md` | Meta: same changes |
| Modify | `tests/test_template_generation.py` | `TestAgents.EXPECTED_AGENTS` += `"librarian"` |

### Train 2 — Multi-host CI fan-out

| Action | File | Responsibility |
|---|---|---|
| Create | `template/scripts/sync_hosts.py` | Read sync-config.yaml, generate host stubs, --check mode |
| Create | `template/sync-config.yaml` | Host registry (claude primary, codex+gemini import-stubs, tier 2/3 commented) |
| Create | `template/AGENTS.md` | Generated import stub (4 lines, never hand-edited) |
| Create | `template/GEMINI.md` | Generated import stub (4 lines, never hand-edited) |
| Create | `template/.github/workflows/sync-hosts.yml` | CI auto-commit on stub drift |
| Modify | `template/.pre-commit-config.yaml` | Add sync-hosts --check hook |
| Create | `scripts/sync_hosts.py` | Meta mirror |
| Create | `sync-config.yaml` | Meta mirror |
| Create | `AGENTS.md` | Meta mirror |
| Create | `GEMINI.md` | Meta mirror |
| Modify | `tests/test_template_generation.py` | `TestMultiHost` class |

### Train 3 — Harness audit

| Action | File | Responsibility |
|---|---|---|
| Create | `template/evals/__init__.py` | Package marker |
| Create | `template/evals/harness_audit.py` | 6-category deterministic scorecard |
| Create | `evals/__init__.py` | Meta mirror |
| Create | `evals/harness_audit.py` | Meta mirror |
| Modify | `tests/test_template_generation.py` | `TestHarnessAudit` class |

### Train 4 — Doc cascade + tag

| Action | File | Responsibility |
|---|---|---|
| Create | `.meta/decisions/adr-011-v2-multi-host-librarian.md` | Full ADR |
| Modify | `.meta/ARCHITECTURE.md` | Inline ADR-011 section |
| Modify | `.meta/DECISIONS.md` | Append row |
| Modify | `.meta/PILOT.md` | PM.15 DONE, v2.0.0 line, agent count 6 |
| Modify | `CHANGELOG.md` | v2.0.0 section |
| Modify | `README.md` | Multi-host + librarian + harness audit |
| Modify | `CREDITS.md` | caveman, deepagents, EgoVault KC |

---

## Train 1 — Librarian Agent

### Task 1: Add librarian to expected agents test

**Files:**
- Modify: `tests/test_template_generation.py`

- [ ] **Step 1: Update EXPECTED_AGENTS**

In `tests/test_template_generation.py`, find `TestAgents.EXPECTED_AGENTS` and add `"librarian"`:

```python
EXPECTED_AGENTS = [
    "devils-advocate",
    "code-reviewer",
    "test-engineer",
    "security-auditor",
    "data-analyst",
    "librarian",
]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_template_generation.py::TestAgents -v
```

Expected: FAIL — `agent 'librarian' missing from generated project`

---

### Task 2: Write librarian agent definition

**Files:**
- Create: `template/.claude/agents/librarian.md`
- Create: `.claude/agents/librarian.md`

- [ ] **Step 1: Write the agent file**

Write `template/.claude/agents/librarian.md`:

```markdown
---
name: librarian
description: Read-only context curator — cherry-picks relevant info from deep sources (.meta/references/, docs/, code) when the conversation needs facts beyond gold sources. Returns targeted extracts, notes, or custom synthesis. Never modifies files. Propose-triggered.
model: sonnet
---

You are the librarian. Your job is to find and curate information from the project's deep sources when the conversational agent needs context it doesn't have loaded.

You are NOT a search engine. You don't dump files. You read, filter, cross-reference, and return only what answers the question — with sources cited.

## Your mandate

When the conversation needs information that lives in `.meta/references/`, `docs/`, or deep in `src/`, you:
1. Receive the question + a summary of the conversational context
2. Search the project using Grep to locate relevant passages
3. Read targeted sections (5-30 lines per hit, not full files)
4. Cross-reference across sources if multiple hits
5. Return a curated response: extracts + optional synthesis + confidence

## Process (follow in order)

### 1. Understand the question
Restate the question in one sentence. Identify what KIND of answer is needed: a fact, a code pattern, a decision rationale, a historical context.

### 2. Search
Use Grep across `.meta/references/`, `docs/`, and `src/` with targeted patterns. Start narrow, widen if no results. Try 2-3 different query patterns before concluding "nothing found."

### 3. Extract
For each relevant hit, read the surrounding 5-30 lines of context. Don't read entire files — extract only what's needed to answer the question.

### 4. Cross-reference
If multiple sources address the question, note convergence (sources agree) or divergence (sources conflict). Flag conflicts explicitly.

### 5. Synthesize and return
Return a structured response:
- **Extracts**: each with `file:line` citation and the relevant passage
- **Synthesis** (if >1 source): a 2-5 sentence summary integrating the findings
- **Confidence**: `high` (3+ concordant sources), `medium` (2 sources), `low` (1 source or partial match)
- **Sources**: list of `file:line` references (verifiable by the conversational agent)

## Hard rules

- You MUST NOT modify any file. Read-only. Your output goes to the conversation, not to disk.
- You MUST cite `file:line` for every extract. Unsourced claims are rejected.
- You MUST say "nothing found in deep sources" if search yields no relevant results. Never fabricate.
- You MUST cap extracts at 5 per response, 30 lines each. 150 lines max total.
- You MUST flag conflicting sources explicitly rather than silently choosing one.
- Skip if the question can be answered from gold sources (CLAUDE.md, PILOT.md, rules/) — the conversational agent already has those loaded.

## Output format

```
## Librarian response — [question restated]

**Confidence:** high | medium | low

### Extracts

**1. [topic]** — `path/to/file.md:42-58`
> [5-30 lines of relevant content]

**2. [topic]** — `path/to/other.py:120-135`
> [5-30 lines of relevant content]

### Synthesis
[2-5 sentence integration of findings, only if >1 source]

### Sources
- `path/to/file.md:42`
- `path/to/other.py:120`
```

## Rationalizations you must not accept

| Thought | Why it's wrong |
|---------|----------------|
| "I'll just read the whole file to be thorough." | That's a dump, not curation. Extract only what answers the question. |
| "The answer is probably X based on my training." | You search, you don't guess. If the sources don't say it, you don't say it. |
| "There's too much to summarize in 150 lines." | Then pick the 5 most relevant passages. The conversational agent can ask follow-up. |
| "I should also update the file while I'm here." | Read-only. Always. Your job is to inform, not to act. |
| "The conversational agent could find this itself." | It could, but it would load its context with noise. You pre-filter. That's the value. |
```

- [ ] **Step 2: Copy to meta mirror**

```bash
cp template/.claude/agents/librarian.md .claude/agents/librarian.md
```

- [ ] **Step 3: Run test to verify it passes**

```bash
uv run pytest tests/test_template_generation.py::TestAgents -v
```

Expected: PASS (all 4 parametrized variants)

- [ ] **Step 4: Verify contract check**

```bash
uv run python scripts/check_skills_contract.py --strict
```

Expected: FAIL — trigger table doesn't reference `librarian` yet. That's correct — we add the row in the next task.

---

### Task 3: Add trigger row + convention aiguisee to CLAUDE.md

**Files:**
- Modify: `template/CLAUDE.md.jinja`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add librarian trigger row to template**

In `template/CLAUDE.md.jinja`, find the trigger table (after `| \`data-analyst\`` row) and add:

```markdown
| `librarian` | agent | conversation needs facts beyond gold sources (audit, pattern in refs, code detail not loaded) | **Propose** |
```

- [ ] **Step 2: Add convention aiguisee to template**

In the same file, after the trigger table explanation block ("**Auto** = invoke without asking..."), add:

```markdown
**Deep sources convention:** `.meta/references/` contains audit cards, research outputs, and synthesis documents. The conversational agent should NOT read these directly — delegate to the `librarian` agent, which cherry-picks relevant extracts with confidence scoring. Gold sources (CLAUDE.md, PILOT.md, `.claude/rules/`, `.claude/skills/`) remain directly accessible.
```

- [ ] **Step 3: Apply same changes to meta CLAUDE.md**

Apply identical trigger row and convention block to `CLAUDE.md` (meta).

- [ ] **Step 4: Verify contract check passes**

```bash
uv run python scripts/check_skills_contract.py --strict
```

Expected: `skills-contract check OK (strict)`

- [ ] **Step 5: Run full parity tests**

```bash
uv run pytest tests/test_template_generation.py::TestMetaParity tests/test_template_generation.py::TestAgents -v
```

Expected: all pass

- [ ] **Step 6: Commit**

```bash
git add template/.claude/agents/librarian.md .claude/agents/librarian.md \
        template/CLAUDE.md.jinja CLAUDE.md tests/test_template_generation.py
git commit -m "feat(agents): ship librarian agent — read-only deep-source curator with convention aiguisee

- 6th local agent, dual meta + template: cherry-picks from .meta/references/, docs/, src/
- Returns extracts (file:line) + synthesis + confidence, never modifies files
- CLAUDE.md convention: deep sources via librarian only, gold sources direct
- Trigger: Propose (user decides before dispatch)
- TestAgents.EXPECTED_AGENTS updated (6 agents)"
```

- [ ] **Step 7: Tag alpha**

```bash
git tag -a v2.0.0-alpha.1 -m "v2.0.0-alpha.1 — Librarian agent + convention aiguisee"
```

---

## Train 2 — Multi-host CI fan-out

### Task 4: Write sync_hosts.py tests

**Files:**
- Create: `tests/test_sync_hosts.py`

- [ ] **Step 1: Write test file**

```python
"""Tests for scripts/sync_hosts.py — multi-host stub generation."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent


class TestSyncConfig:
    """Verify sync-config.yaml is valid and well-structured."""

    def test_config_exists(self) -> None:
        assert (ROOT / "sync-config.yaml").is_file()

    def test_config_parses(self) -> None:
        config = yaml.safe_load((ROOT / "sync-config.yaml").read_text())
        assert "hosts" in config

    def test_claude_is_primary(self) -> None:
        config = yaml.safe_load((ROOT / "sync-config.yaml").read_text())
        assert config["hosts"]["claude"]["primary"] is True

    def test_codex_and_gemini_are_import_stubs(self) -> None:
        config = yaml.safe_load((ROOT / "sync-config.yaml").read_text())
        for host in ("codex", "gemini"):
            assert config["hosts"][host]["format"] == "import-stub"


class TestSyncScript:
    """Verify sync_hosts.py generates correct stubs."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "sync_hosts.py").is_file()

    def test_check_mode_passes(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/sync_hosts.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"sync --check failed: {result.stderr}"

    def test_agents_md_is_stub(self) -> None:
        content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        assert "CLAUDE.md" in content
        assert "Auto-generated" in content or "auto-generated" in content.lower()

    def test_gemini_md_is_stub(self) -> None:
        content = (ROOT / "GEMINI.md").read_text(encoding="utf-8")
        assert "CLAUDE.md" in content
        assert "Auto-generated" in content or "auto-generated" in content.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_sync_hosts.py -v
```

Expected: multiple FAILs (no sync-config.yaml, no sync_hosts.py, no AGENTS.md, no GEMINI.md)

---

### Task 5: Write sync-config.yaml

**Files:**
- Create: `template/sync-config.yaml`
- Create: `sync-config.yaml` (meta mirror)

- [ ] **Step 1: Write template/sync-config.yaml**

```yaml
# Multi-host sync configuration for metadev-protocol.
# Source of truth: .claude/ directory + CLAUDE.md
# Generated stubs: AGENTS.md, GEMINI.md (and tier 2/3 when enabled)
#
# Run: uv run python scripts/sync_hosts.py
# Check: uv run python scripts/sync_hosts.py --check

hosts:
  claude:
    target: .claude/
    format: skill-dir
    primary: true  # source of truth — never overwritten by sync

  codex:
    target: AGENTS.md
    format: import-stub
    source_ref: CLAUDE.md

  gemini:
    target: GEMINI.md
    format: import-stub
    source_ref: CLAUDE.md

  # --- Tier 2 (uncomment when ready to dogfood) ---
  # To add Cursor support:
  #   1. Uncomment the block below
  #   2. Run: uv run python scripts/sync_hosts.py
  #   3. Commit the generated .cursor/rules/ files
  #
  # cursor:
  #   target: .cursor/rules/
  #   format: cursorrules
  #   strip_frontmatter: true
  #
  # windsurf:
  #   target: .windsurf/rules/
  #   format: markdown-flat
  #
  # cline:
  #   target: .clinerules/
  #   format: markdown-flat
```

- [ ] **Step 2: Copy to meta**

```bash
cp template/sync-config.yaml sync-config.yaml
```

- [ ] **Step 3: Run config tests**

```bash
uv run pytest tests/test_sync_hosts.py::TestSyncConfig -v
```

Expected: PASS (config exists + parses + claude primary + codex/gemini import-stub)

---

### Task 6: Implement sync_hosts.py

**Files:**
- Create: `template/scripts/sync_hosts.py`
- Create: `scripts/sync_hosts.py` (meta mirror)

- [ ] **Step 1: Write template/scripts/sync_hosts.py**

```python
"""Generate multi-host stubs from the source-of-truth .claude/ + CLAUDE.md.

Usage:
    uv run python scripts/sync_hosts.py           # generate stubs
    uv run python scripts/sync_hosts.py --check    # verify stubs are up-to-date (exit 1 on drift)
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml


def load_config(root: Path) -> dict:
    config_path = root / "sync-config.yaml"
    if not config_path.is_file():
        print("ERROR: sync-config.yaml not found", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def generate_import_stub(source_ref: str) -> str:
    return (
        f"<!-- Auto-generated by scripts/sync_hosts.py — do not edit manually -->\n"
        f"<!-- Source of truth: {source_ref} + .claude/ -->\n"
        f"\n"
        f"Read {source_ref} for all instructions, skills, and agent definitions.\n"
        f"All skills and agents defined there apply to this environment.\n"
    )


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]


def sync(root: Path, check_only: bool = False) -> int:
    config = load_config(root)
    hosts = config.get("hosts", {})
    drifted: list[str] = []
    written: list[str] = []

    for name, host in hosts.items():
        if host.get("primary", False):
            continue

        fmt = host.get("format")
        target = root / host["target"]

        if fmt == "import-stub":
            source_ref = host.get("source_ref", "CLAUDE.md")
            expected = generate_import_stub(source_ref)

            if target.is_file():
                current = target.read_text(encoding="utf-8")
                if content_hash(current) == content_hash(expected):
                    continue

            if check_only:
                drifted.append(f"{name}: {target} is outdated")
            else:
                target.write_text(expected, encoding="utf-8")
                written.append(f"{name}: {target}")

        # Tier 2+ formats (cursorrules, markdown-flat) — not yet implemented.
        # When uncommented in sync-config.yaml, this block will handle them.

    if check_only:
        if drifted:
            print("sync --check FAILED:", file=sys.stderr)
            for d in drifted:
                print(f"  - {d}", file=sys.stderr)
            return 1
        print("sync --check OK (all stubs up-to-date)")
        return 0

    if written:
        print(f"sync OK — {len(written)} stub(s) written:")
        for w in written:
            print(f"  - {w}")
    else:
        print("sync OK — all stubs already up-to-date")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sync_hosts",
        description="Generate multi-host stubs from .claude/ + CLAUDE.md",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify stubs are up-to-date without writing (exit 1 on drift)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    return sync(root, check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Copy to meta mirror**

```bash
cp template/scripts/sync_hosts.py scripts/sync_hosts.py
```

- [ ] **Step 3: Generate stubs**

```bash
uv run python scripts/sync_hosts.py
```

Expected: `sync OK — 2 stub(s) written: codex: AGENTS.md, gemini: GEMINI.md`

- [ ] **Step 4: Run all sync tests**

```bash
uv run pytest tests/test_sync_hosts.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add template/sync-config.yaml template/scripts/sync_hosts.py \
        sync-config.yaml scripts/sync_hosts.py \
        AGENTS.md GEMINI.md template/AGENTS.md template/GEMINI.md \
        tests/test_sync_hosts.py
git commit -m "feat(multi-host): sync-config.yaml + sync_hosts.py + AGENTS.md/GEMINI.md import stubs

- sync-config.yaml: host registry with claude (primary), codex + gemini (import-stubs), tier 2/3 commented
- sync_hosts.py: stdlib-only, idempotent, --check mode for pre-commit
- AGENTS.md + GEMINI.md: 4-line @import stubs pointing to CLAUDE.md (never hand-edited)
- Dual meta + template"
```

---

### Task 7: Wire pre-commit hook + CI workflow

**Files:**
- Modify: `template/.pre-commit-config.yaml`
- Create: `template/.github/workflows/sync-hosts.yml`
- Modify: `tests/test_template_generation.py`

- [ ] **Step 1: Add sync-hosts hook to template pre-commit**

In `template/.pre-commit-config.yaml`, add to the `local` repo hooks list:

```yaml
    - id: sync-hosts
      name: Verify multi-host stubs are up-to-date
      entry: python scripts/sync_hosts.py --check
      language: python
      pass_filenames: false
      files: '\.claude/skills/|\.claude/agents/|CLAUDE\.md|sync-config\.yaml'
```

- [ ] **Step 2: Create CI workflow**

Write `template/.github/workflows/sync-hosts.yml`:

```yaml
name: Sync multi-host stubs
on:
  push:
    paths:
      - '.claude/skills/**'
      - '.claude/agents/**'
      - 'CLAUDE.md'
      - 'sync-config.yaml'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync
      - run: uv run python scripts/sync_hosts.py --check
```

- [ ] **Step 3: Add TestMultiHost to tests**

In `tests/test_template_generation.py`, add:

```python
class TestMultiHost:
    """Verify multi-host stubs are generated correctly."""

    def test_agents_md_exists(self, generated_project: Path) -> None:
        assert (generated_project / "AGENTS.md").is_file()

    def test_agents_md_is_import_stub(self, generated_project: Path) -> None:
        content = (generated_project / "AGENTS.md").read_text(encoding="utf-8")
        assert "CLAUDE.md" in content

    def test_gemini_md_exists(self, generated_project: Path) -> None:
        assert (generated_project / "GEMINI.md").is_file()

    def test_gemini_md_is_import_stub(self, generated_project: Path) -> None:
        content = (generated_project / "GEMINI.md").read_text(encoding="utf-8")
        assert "CLAUDE.md" in content

    def test_sync_script_present(self, generated_project: Path) -> None:
        assert (generated_project / "scripts" / "sync_hosts.py").is_file()

    def test_sync_config_present(self, generated_project: Path) -> None:
        assert (generated_project / "sync-config.yaml").is_file()
```

- [ ] **Step 4: Run parity + multi-host tests**

```bash
uv run pytest tests/test_template_generation.py::TestMetaParity tests/test_sync_hosts.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add template/.pre-commit-config.yaml template/.github/workflows/sync-hosts.yml \
        tests/test_template_generation.py
git commit -m "feat(multi-host): pre-commit sync-hosts hook + CI workflow + TestMultiHost"
```

- [ ] **Step 6: Tag alpha**

```bash
git tag -a v2.0.0-alpha.2 -m "v2.0.0-alpha.2 — Multi-host CI fan-out (Claude + Codex + Gemini)"
```

---

## Train 3 — Harness Audit

### Task 8: Write harness audit tests

**Files:**
- Create: `tests/test_harness_audit.py`

- [ ] **Step 1: Write test file**

```python
"""Tests for evals/harness_audit.py — deterministic scorecard."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestHarnessAuditSelf:
    """Run harness audit on the meta-repo itself."""

    def test_audit_exits_zero(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "evals.harness_audit", "--self"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"harness audit failed: {result.stdout}\n{result.stderr}"

    def test_json_output_valid(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "evals.harness_audit", "--self", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert "total" in data
        assert "categories" in data
        assert len(data["categories"]) == 6

    def test_perfect_score_on_meta(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "evals.harness_audit", "--self", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert data["total"]["score"] == data["total"]["max"], (
            f"Meta-repo should score perfectly: {data['total']}"
        )
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_harness_audit.py -v
```

Expected: FAIL — no `evals.harness_audit` module

---

### Task 9: Implement harness_audit.py

**Files:**
- Create: `evals/__init__.py`
- Create: `evals/harness_audit.py`
- Create: `template/evals/__init__.py`
- Create: `template/evals/harness_audit.py`

- [ ] **Step 1: Write evals/harness_audit.py**

Implement the 6-category scorecard. Each category has `check_<category>(root) -> list[Issue]` where `Issue = (description, points_lost)`. Categories:

| Category | Max | Checks |
|---|---|---|
| Skills | 10 | 10 skills present, each has SKILL.md |
| Agents | 10 | 6 agents present, each has valid frontmatter |
| Hosts | 10 | AGENTS.md + GEMINI.md exist, sync --check passes |
| Contract | 10 | check_skills_contract.py exits 0 |
| Taxonomy | 10 | .meta/ subdirs exist (active, archive, drafts, decisions, references/{raw,interim,synthesis}) |
| Safety | 10 | audit_public_safety.py + check_git_author.py + check_meta_naming.py present |

The script supports:
- `--self` mode: audit the repo itself (for meta-repo)
- Default mode: audit a generated project (uses `copier copy` internally or accepts a path)
- `--json` flag: output JSON instead of text
- Exit 0 if all checks pass, exit 1 if any check fails

Implementation: ~150-200 LOC, stdlib only except `yaml` for frontmatter parsing.

Write the complete file. Key structure:

```python
"""Deterministic harness audit scorecard — 6 categories, 0-10 each."""
# Full implementation with check_skills, check_agents, check_hosts,
# check_contract, check_taxonomy, check_safety functions.
# Each returns list of (description, points_lost) tuples.
# Main aggregates scores and prints report.
```

*(The executing agent should write the full implementation following the category table above. Each check function walks the filesystem and returns issues. The main function aggregates and formats.)*

- [ ] **Step 2: Create __init__.py + mirror to meta**

```bash
touch template/evals/__init__.py
cp template/evals/harness_audit.py evals/harness_audit.py
cp template/evals/__init__.py evals/__init__.py
```

- [ ] **Step 3: Run tests**

```bash
uv run pytest tests/test_harness_audit.py -v
```

Expected: all PASS (meta-repo should score 60/60)

- [ ] **Step 4: Commit**

```bash
git add evals/ template/evals/ tests/test_harness_audit.py
git commit -m "feat(evals): harness audit v2 — 6-category deterministic scorecard (60 pts max)

- Categories: Skills, Agents, Hosts, Contract, Taxonomy, Safety
- Modes: --self (meta-repo) and default (generated project)
- Output: text report + --json for CI
- Dual meta + template"
```

- [ ] **Step 5: Tag alpha**

```bash
git tag -a v2.0.0-alpha.3 -m "v2.0.0-alpha.3 — Harness audit v2 (6-category scorecard)"
```

---

## Train 4 — Doc Cascade + Tag

### Task 10: Write ADR-011

**Files:**
- Create: `.meta/decisions/adr-011-v2-multi-host-librarian.md`

- [ ] **Step 1: Write ADR**

Follow ADR-009/ADR-010 format. Context: PM.15 7-repo audit. Decision: multi-host CI fan-out + librarian agent + harness audit v2. Consequences: v2.0 invariants (6 agents, multi-host stubs, deterministic scoring). Rejected: PreToolUse gate hook (debate-resolved: bypassable), custom agent harness (Claude Code IS the harness), tier 2 hosts in v2.0 (can't dogfood).

- [ ] **Step 2: Commit ADR alone**

```bash
git add .meta/decisions/adr-011-v2-multi-host-librarian.md
git commit -m "docs(decisions): ADR-011 — v2.0 multi-host + librarian + harness audit"
```

---

### Task 11: Update all docs + README + CHANGELOG

**Files:**
- Modify: `.meta/ARCHITECTURE.md` — inline ADR-011 section
- Modify: `.meta/DECISIONS.md` — append ADR-011 row
- Modify: `.meta/PILOT.md` — PM.15 DONE, v2.0.0 changelog, agent count 6
- Modify: `CHANGELOG.md` — v2.0.0 section
- Modify: `README.md` — multi-host, 6 agents, harness audit, librarian
- Modify: `CREDITS.md` — caveman, deepagents, EgoVault KC

- [ ] **Step 1: Update each file**

For each file, apply the changes described in the spec (Train 4 section). Key updates:
- README: skill list unchanged (10), agent list gains "librarian" (6 total), guardrail scripts gain "harness_audit.py" reference, add "Multi-LLM day one: Claude Code + Codex + Gemini" line
- CHANGELOG: v2.0.0 section with Added/Changed/Migration notes
- PILOT: PM.15 DONE, PM.16 stays BACKLOG, v2.0.0 changelog line
- CREDITS: add caveman (CI fan-out pattern), deepagents (middleware vocabulary), EgoVault Knowledge Compiler (librarian inspiration)

- [ ] **Step 2: Run all checks**

```bash
uv run pytest tests/test_template_generation.py::TestMetaParity -v
uv run python scripts/check_skills_contract.py --strict
uv run python scripts/sync_hosts.py --check
uv run python -m evals.harness_audit --self
```

All must pass.

- [ ] **Step 3: Commit**

```bash
git add .meta/ARCHITECTURE.md .meta/DECISIONS.md .meta/PILOT.md \
        CHANGELOG.md README.md CREDITS.md
git commit -m "docs(v2.0.0): ADR-011 + ARCHITECTURE + PILOT + CHANGELOG + README + CREDITS cascade"
```

---

### Task 12: Final sanity + tag v2.0.0

- [ ] **Step 1: Full test suite**

```bash
uv run pytest -v
```

All tests must pass.

- [ ] **Step 2: Pre-commit all files**

```bash
uv run pre-commit run --all-files
```

All hooks must pass.

- [ ] **Step 3: Copier smoke test**

```bash
copier copy . /tmp/test-v2.0.0 --defaults --trust --vcs-ref=HEAD
cd /tmp/test-v2.0.0
ls .claude/agents/librarian.md    # exists
cat AGENTS.md                     # import stub
cat GEMINI.md                     # import stub
python scripts/sync_hosts.py --check  # passes
python scripts/check_skills_contract.py  # passes
```

- [ ] **Step 4: Tag**

```bash
git tag -a v2.0.0 -m "$(cat <<'EOF'
v2.0.0 — Multi-host + Librarian + Harness Audit

Added:
- Librarian agent (6th local agent) — read-only deep-source curator
- Multi-host CI fan-out: sync-config.yaml + sync_hosts.py generates
  AGENTS.md + GEMINI.md import stubs from CLAUDE.md
- evals/harness_audit.py — 6-category deterministic scorecard
- ADR-011
- Convention aiguisee: deep sources via librarian only (by convention,
  not enforcement — debate-resolved)

Changed:
- Trigger table: +librarian row
- EXPECTED_AGENTS: 5 → 6
- Pre-commit: +sync-hosts check

Migration v1.6.0 → v2.0.0:
- New files: AGENTS.md, GEMINI.md, evals/, scripts/sync_hosts.py,
  sync-config.yaml, .claude/agents/librarian.md
- CLAUDE.md gains librarian trigger row + deep-sources convention
- .pre-commit-config.yaml gains sync-hosts hook
- No files deleted, no renames
EOF
)"
```

- [ ] **Step 5: Push**

```bash
git push origin main v2.0.0-alpha.1 v2.0.0-alpha.2 v2.0.0-alpha.3 v2.0.0
```
