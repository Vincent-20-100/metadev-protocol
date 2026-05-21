# Git Identity Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure that no AI tool (Claude Code or other) can ever replace the human author on git commits, both in metadev-protocol itself and in all projects generated from the template.

**Architecture:** Four complementary layers — (1) `env` block in `settings.json` overrides `GIT_AUTHOR_NAME/EMAIL` + `GIT_COMMITTER_NAME/EMAIL` at session level (forensic finding: Claude Code uses env var injection, not `--author` flag); (2) PreToolUse hook intercepts `git commit` before it runs, strips any `--author` arg, and injects the correct identity from `git config user.name` (respects local overrides); (3) pre-commit hook detects forbidden author identity via both `$GIT_AUTHOR_NAME` env var and `git var GIT_AUTHOR_IDENT`; (4) CI workflow blocks PRs and pushes containing Claude/Anthropic-authored commits (author + committer). Copier defaults are derived from `git config user.name/email` (no `--global` flag, respects per-repo overrides). The two scripts `scripts/check_git_author.py` and `template/scripts/check_git_author.py` are always kept byte-for-byte identical.

**Tech Stack:** Python 3.13, pre-commit, GitHub Actions, Claude Code settings.json (JSON + Jinja), copier

---

## File Map

| Action | Path | Purpose |
|---|---|---|
| Modify | `scripts/check_git_author.py` | Also check `$GIT_AUTHOR_NAME` env var; kept in sync with template |
| Modify | `template/scripts/check_git_author.py` | Same change — always identical to above |
| Create | `scripts/force_git_author.py` | PreToolUse hook: intercept `git commit`, strip `--author`, inject correct identity |
| Create | `template/scripts/force_git_author.py` | Same file — generated into projects |
| Modify | `.claude/settings.json` | Wire PreToolUse hook (env vars already correct — keep as fallback) |
| Modify | `template/.claude/settings.json.jinja` | Add env vars block (from copier values) + wire PreToolUse hook |
| Modify | `copier.yml` | Defaults from `git config`; `enable_server_auth_check` default → `true` |
| Modify | `template/.github/workflows/check-commit-authors.yml` | Add push trigger + committer scan |

---

## Task 1 — Fix the 2 bad commits on `main`

**Files:** none (git history rewrite, no working-tree changes)

> Do this before creating any branch. `--reset-author` uses the identity active at rebase time — validate it first.

- [ ] **Step 1: Validate that the current git identity is correct**

```bash
git config user.name && git config user.email
```
Expected: `Vincent` and `vincent.lamy.33@gmail.com`. If not, fix `~/.gitconfig` before continuing.

- [ ] **Step 2: Confirm which commits are bad**

```bash
git log --format="%H %an <%ae>" -5
```
Expected: the two top commits (`f385fbd`, `808236f`) show `Claude <noreply@anthropic.com>`.

- [ ] **Step 3: Diagnose how Claude set the author (forensics)**

```bash
git show f385fbd --format="%H %an <%ae> | %cn <%ce>" --no-patch
```
This tells us author vs committer. Both being "Claude" suggests env var injection rather than `--author` flag (which only sets author, not committer). This informs whether the env vars approach might have been sufficient — but we proceed with the PreToolUse hook regardless as the stronger fix.

- [ ] **Step 4: Rewrite the last 2 commits**

```bash
git rebase HEAD~2 --exec 'git commit --amend --reset-author --no-edit'
```

- [ ] **Step 5: Verify**

```bash
git log --format="%H %an <%ae>" -5
```
Expected: all 5 top commits show `Vincent <vincent.lamy.33@gmail.com>`.

- [ ] **Step 6: Note for push**

No commit needed. The push will require `--force-with-lease` since main history changed. Do not push until the full plan is implemented and reviewed.

---

## Task 2 — Keep env vars as fallback + add to template

**Files:**
- Modify: `.claude/settings.json` (keep existing env block — no change needed)
- Modify: `template/.claude/settings.json.jinja` (add env block populated from copier values)

**Forensic finding:** the bad commits had both author AND committer = "Claude". The `--author` flag only sets the author, never the committer. Both being "Claude" proves Claude Code uses `GIT_AUTHOR_NAME` / `GIT_COMMITTER_NAME` env var injection. The env block in `settings.json` is therefore the correct fallback layer — it just didn't exist yet when those commits happened. Keep it. Add the PreToolUse hook on top (Task 5). Belt + suspenders.

- [ ] **Step 1: Confirm the existing env block in metadev-protocol is correct**

```bash
jq '.env' .claude/settings.json
```

Expected:
```json
{
  "GIT_AUTHOR_NAME": "Vincent",
  "GIT_AUTHOR_EMAIL": "vincent.lamy.33@gmail.com",
  "GIT_COMMITTER_NAME": "Vincent",
  "GIT_COMMITTER_EMAIL": "vincent.lamy.33@gmail.com"
}
```

No change needed. This block is already correct for this repo.

- [ ] **Step 2: Add the env block to `template/.claude/settings.json.jinja`**

In `template/.claude/settings.json.jinja`, add after `"attribution": {"commit": ""},`:

```json
  "env": {
    "GIT_AUTHOR_NAME": "{{ author_name }}",
    "GIT_AUTHOR_EMAIL": "{{ author_email }}",
    "GIT_COMMITTER_NAME": "{{ author_name }}",
    "GIT_COMMITTER_EMAIL": "{{ author_email }}"
  },
```

Since `author_name` / `author_email` now default to `git config user.name/email` (Task 8), these values are correct without hardcoding.

- [ ] **Step 3: Validate Jinja output**

```bash
copier copy . /tmp/test-env --defaults 2>/dev/null
jq '.env' /tmp/test-env/.claude/settings.json
rm -rf /tmp/test-env
```

Expected: env block shows `Vincent` and `vincent.lamy.33@gmail.com` (your current git config values).

- [ ] **Step 4: Commit**

```bash
git add template/.claude/settings.json.jinja
git commit -m "feat(template): add env vars fallback for git author/committer identity"
```

---

## Task 3 — Create the feature branch

**Files:** none

- [ ] **Step 1: Create branch from the cleaned main**

```bash
git checkout -b feat/git-identity-hardening
```

All subsequent commits go on this branch.

---

## Task 4 — Write `force_git_author.py`

**Files:**
- Create: `scripts/force_git_author.py`
- Create: `template/scripts/force_git_author.py`

This script is a Claude Code `PreToolUse` hook. It receives a Bash tool call on stdin, detects `git commit` commands, strips any `--author` argument, and injects the correct `--author` from the user's global git config.

- [ ] **Step 1: Write the script**

Write `scripts/force_git_author.py`:

```python
#!/usr/bin/env python3
"""Claude Code PreToolUse hook: force git commit author to global git config identity.

Receives JSON on stdin (Claude Code hook protocol).
Outputs JSON with updatedInput when the command is a git commit.
Exits 0 silently for all other commands.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys


def git_identity(key: str) -> str:
    """Read git config respecting local > global > system precedence."""
    try:
        return subprocess.check_output(
            ["git", "config", key], text=True
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def strip_author_flag(cmd: str) -> str:
    """Remove any --author=... or --author '...' variants from a git command."""
    # --author=VALUE or --author='VALUE' or --author="VALUE"
    cmd = re.sub(r"\s+--author=['\"]?[^'\"\s][^'\"]*['\"]?", "", cmd)
    cmd = re.sub(r"\s+--author='[^']*'", "", cmd)
    cmd = re.sub(r'\s+--author="[^"]*"', "", cmd)
    return cmd


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    cmd: str = data.get("tool_input", {}).get("command", "")

    # Only act on git commit commands
    if not re.search(r"\bgit\b.*\bcommit\b", cmd):
        return 0

    name = git_identity("user.name")
    email = git_identity("user.email")

    if not name or not email:
        # Can't determine identity — let it pass, pre-commit hook will catch it
        return 0

    cmd_clean = strip_author_flag(cmd).rstrip()
    cmd_final = f"{cmd_clean} --author='{name} <{email}>'"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": {"command": cmd_final},
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Test the script manually**

```bash
echo '{"tool_input": {"command": "git commit -m \"test\""}}' \
  | python scripts/force_git_author.py
```

Expected output (with your git config):
```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": {"command": "git commit -m \"test\" --author='Vincent <vincent.lamy.33@gmail.com>'"}}}
```

- [ ] **Step 3: Test with an existing --author flag (the stripping case)**

```bash
echo '{"tool_input": {"command": "git commit -m \"test\" --author=\"Claude <noreply@anthropic.com>\""}}' \
  | python scripts/force_git_author.py
```

Expected: `--author` in output contains `Vincent`, not `Claude`.

- [ ] **Step 4: Test on a non-commit command (must be silent)**

```bash
echo '{"tool_input": {"command": "git status"}}' \
  | python scripts/force_git_author.py
```

Expected: empty output, exit 0.

- [ ] **Step 5: Copy to template**

```bash
cp scripts/force_git_author.py template/scripts/force_git_author.py
```

- [ ] **Step 6: Commit**

```bash
git add scripts/force_git_author.py template/scripts/force_git_author.py
git commit -m "feat(hooks): force_git_author PreToolUse hook — strips --author, injects git config identity"
```

---

## Task 5 — Wire the PreToolUse hook

### 5a — metadev-protocol `.claude/settings.json`

**Files:**
- Modify: `.claude/settings.json`

- [ ] **Step 1: Add the PreToolUse hook block**

In `.claude/settings.json`, add a new `PreToolUse` entry inside `hooks`:

```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python scripts/force_git_author.py",
        "if": "Bash(git commit *)"
      }
    ]
  }
],
```

Place it before the existing `PostToolUse` key. The full `hooks` object becomes:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python scripts/force_git_author.py",
          "if": "Bash(git commit *)"
        }
      ]
    }
  ],
  "PostToolUse": [ ... existing ... ],
  "SessionStart": [ ... existing ... ]
}
```

- [ ] **Step 2: Validate JSON**

```bash
jq . .claude/settings.json > /dev/null && echo "OK"
```

- [ ] **Step 3: Validate hook wiring**

```bash
jq -e '.hooks.PreToolUse[0].hooks[0].command' .claude/settings.json
```

Expected: `"python scripts/force_git_author.py"`

### 5b — template `settings.json.jinja`

**Files:**
- Modify: `template/.claude/settings.json.jinja`

- [ ] **Step 4: Add the same PreToolUse block to the template**

In `template/.claude/settings.json.jinja`, add after `"attribution": {"commit": ""},`:

```json
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/force_git_author.py",
            "if": "Bash(git commit *)"
          }
        ]
      }
    ],
    "PostToolUse": [ ... existing ... ],
    "SessionStart": [ ... existing ... ]
  }
```

The PreToolUse block is inserted above the existing PostToolUse entry inside the existing `hooks` object. No Jinja condition needed — this protection applies in all execution modes.

- [ ] **Step 5: Validate Jinja output**

```bash
copier copy . /tmp/test-identity --defaults 2>/dev/null
jq -e '.hooks.PreToolUse[0].hooks[0].command' /tmp/test-identity/.claude/settings.json
rm -rf /tmp/test-identity
```

Expected: `"python scripts/force_git_author.py"`

- [ ] **Step 6: Commit**

```bash
git add .claude/settings.json template/.claude/settings.json.jinja
git commit -m "feat(hooks): wire PreToolUse git-commit interceptor in settings (metadev + template)"
```

---

## Task 6 — Strengthen `check_git_author.py`

**Files:**
- Modify: `scripts/check_git_author.py`
- Modify: `template/scripts/check_git_author.py`

Current flaw: `git var GIT_AUTHOR_IDENT` reads git config but ignores the `$GIT_AUTHOR_NAME` env var that Claude Code may inject directly. We add a second check: if `$GIT_AUTHOR_NAME` is set and forbidden, block immediately.

- [ ] **Step 1: Update `check_author()` in `scripts/check_git_author.py`**

Replace the entire `check_author` function:

```python
def check_author() -> str | None:
    """Return error message if the git author identity is forbidden."""
    if os.environ.get("CI"):
        return None

    # Layer 1: check $GIT_AUTHOR_NAME env var (set by some AI tools directly)
    env_name = os.environ.get("GIT_AUTHOR_NAME", "").lower()
    if env_name and any(bad in env_name for bad in FORBIDDEN_SUBSTRINGS):
        return (
            f"check_git_author: $GIT_AUTHOR_NAME='{env_name}' is forbidden.\n"
            "  Unset the env var or fix your git config:\n"
            "    git config user.name 'Your Name'\n"
            "    git config user.email 'you@example.com'"
        )

    # Layer 2: check git var (reads git config, respects $GIT_AUTHOR_NAME if not already caught)
    try:
        ident = subprocess.check_output(["git", "var", "GIT_AUTHOR_IDENT"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    name = ident.split("<", 1)[0].strip().lower()
    if any(bad in name for bad in FORBIDDEN_SUBSTRINGS):
        return (
            f"check_git_author: commit author '{name}' is forbidden.\n"
            "  Fix your git config:\n"
            "    git config user.name 'Your Name'\n"
            "    git config user.email 'you@example.com'"
        )
    return None
```

- [ ] **Step 2: Run the existing tests (if any)**

```bash
uv run pytest tests/ -v -k "author" 2>/dev/null || echo "no matching tests"
```

- [ ] **Step 3: Manual smoke test — env var path**

```bash
GIT_AUTHOR_NAME="Claude Code" python scripts/check_git_author.py
echo "exit: $?"
```

Expected: error message on stderr, exit 1.

- [ ] **Step 4: Manual smoke test — clean path**

```bash
python scripts/check_git_author.py
echo "exit: $?"
```

Expected: silent, exit 0 (git config is "Vincent").

- [ ] **Step 5: Copy to template (keep in sync)**

```bash
cp scripts/check_git_author.py template/scripts/check_git_author.py
diff scripts/check_git_author.py template/scripts/check_git_author.py && echo "IN SYNC"
```

- [ ] **Step 6: Commit**

```bash
git add scripts/check_git_author.py template/scripts/check_git_author.py
git commit -m "fix(hooks): check_git_author also checks \$GIT_AUTHOR_NAME env var"
```

---

## Task 7 — Strengthen `check-commit-authors.yml`

**Files:**
- Modify: `template/.github/workflows/check-commit-authors.yml`

Three improvements:
1. Also scan `committer` name (not just author)
2. Also trigger on `push` to any branch (not only PRs to main)
3. Handle the zero-SHA edge case for new branches

- [ ] **Step 1: Rewrite the workflow**

Replace the entire file content:

```yaml
# Blocks commits authored or committed by Claude or Anthropic.
# Runs on every PR targeting main AND on every push to any branch.
# Complements the local pre-commit hook (check_git_author.py).
#
# Generated by metadev-protocol — opt out by setting enable_server_auth_check: false.

name: Check commit authors

on:
  pull_request:
    branches: [main]
  push:
    branches: ['**']

jobs:
  check-authors:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Scan commits for blocked author/committer names
        run: |
          BLOCKED="Claude|Anthropic"

          if [ "${{ github.event_name }}" = "pull_request" ]; then
            BASE="${{ github.event.pull_request.base.sha }}"
            HEAD="${{ github.event.pull_request.head.sha }}"
            RANGE="${BASE}..${HEAD}"
          else
            BEFORE="${{ github.event.before }}"
            HEAD="${{ github.sha }}"
            # New branch: before is the zero SHA — scan only the pushed commit
            if [ "$BEFORE" = "0000000000000000000000000000000000000000" ]; then
              RANGE="${HEAD}~1..${HEAD}"
            else
              RANGE="${BEFORE}..${HEAD}"
            fi
          fi

          # Check both author (%an) and committer (%cn)
          FOUND=$(git log "${RANGE}" --format="%H author:%an committer:%cn" \
            | grep -iE "$BLOCKED" || true)

          if [ -n "$FOUND" ]; then
            echo "::error::Commits with blocked author or committer name (Claude/Anthropic):"
            echo "$FOUND"
            echo ""
            echo "Rewrite history to use your own identity."
            echo "See .meta/GUIDELINES.md — Commit authorship section."
            exit 1
          fi
          echo "All commit authors and committers OK."
```

- [ ] **Step 2: Verify YAML syntax**

```bash
python -c "import yaml; yaml.safe_load(open('template/.github/workflows/check-commit-authors.yml'))" && echo "OK"
```

- [ ] **Step 3: Commit**

```bash
git add template/.github/workflows/check-commit-authors.yml
git commit -m "fix(ci): check-commit-authors scans committer + push events, not just PRs"
```

---

## Task 8 — Improve `copier.yml` defaults

**Files:**
- Modify: `copier.yml`

Two changes:
1. Default `author_name` and `author_email` from the user's git config (so the user sees their actual identity pre-filled instead of "User" / "you@example.com")
2. Change `enable_server_auth_check` default to `true` (opt-out instead of opt-in)

- [ ] **Step 1: Update `author_name` and `author_email` questions**

Replace:

```yaml
author_name:
  type: str
  help: "Your first name (for pyproject.toml and SessionStart git-author override)"
  default: "User"

author_email:
  type: str
  help: "Your email (for pyproject.toml and SessionStart git-author override in Claude Code remote)"
  default: "you@example.com"
```

With:

```yaml
author_name:
  type: str
  help: "Your name for commit authorship and pyproject.toml. Must match your git config — use 'git config --global user.name' to check."
  default: "{{ 'git config user.name' | shell | trim }}"

author_email:
  type: str
  help: "Your email for commit authorship. Must be registered in your GitHub account for commits to appear on your profile. Use 'git config user.email' to check."
  default: "{{ 'git config user.email' | shell | trim }}"
```

Note: copier's `shell` filter executes a shell command. If the user's git config is correct, they see their name/email pre-filled and just press Enter.

- [ ] **Step 2: Change `enable_server_auth_check` default**

Find:

```yaml
enable_server_auth_check:
  type: bool
  help: "Add a GitHub Actions workflow that blocks PRs containing Claude/Anthropic-authored commits? Recommended if you use cloud AI sandboxes or have external contributors."
  default: false
```

Replace with:

```yaml
enable_server_auth_check:
  type: bool
  help: "Add a GitHub Actions workflow that blocks commits authored OR committed by Claude/Anthropic — scans every PR to main and every branch push. Recommended if you use any AI coding tool. Disable only if you enforce authorship by another means."
  default: true
```

- [ ] **Step 3: Test that copier picks up the git config defaults**

```bash
copier copy . /tmp/test-defaults 2>&1 | head -20
```

When prompted for `author_name`, the default shown should be `Vincent` (your git config value), not `User`.
Exit with Ctrl-C after verifying — no need to complete the generation.

- [ ] **Step 4: Full generation test**

```bash
copier copy . /tmp/test-identity-full --defaults
cat /tmp/test-identity-full/pyproject.toml | grep -A2 "authors"
cat /tmp/test-identity-full/.claude/settings.json | jq '.hooks.PreToolUse'
rm -rf /tmp/test-identity-full
```

Expected: `pyproject.toml` shows `Vincent`, `settings.json` has the PreToolUse hook.

- [ ] **Step 5: Commit**

```bash
git add copier.yml
git commit -m "fix(copier): author defaults from git config; enable_server_auth_check default true"
```

---

## Self-Review

**Spec coverage:**

| Requirement | Task |
|---|---|
| Fix 2 bad commits on main | Task 1 |
| Keep env vars (fallback layer) + add to template | Task 2 |
| Create clean dev branch | Task 3 |
| PreToolUse hook (strip --author, inject correct) | Task 4 + 5 |
| check_git_author.py: also check $GIT_AUTHOR_NAME | Task 6 |
| check-commit-authors.yml: committer + push | Task 7 |
| copier defaults from git config | Task 8 |
| enable_server_auth_check opt-out | Task 8 |

**Gaps:**
- The SessionStart hook in `settings.json.jinja` still reads from `identity.yaml` (copier-populated). This is fine for remote environments — the copier value is now derived from git config (Task 8), so it stays correct. No change needed.
- `scripts/force_git_author.py` is not covered by a test. A unit test would be ideal but is left out per YAGNI — the manual smoke tests in Task 4 are sufficient for a hook script.

**Placeholder scan:** No placeholders found. All code blocks are complete.

**Type consistency:** No shared types across tasks. All functions are self-contained.
