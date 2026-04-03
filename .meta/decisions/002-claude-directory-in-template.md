# ADR-002 — Generating a .claude/ directory in the template

**Date:** 2026-04-01
**Status:** IMPLEMENTED
**Sources:**
- `.meta/references/claude-code-hooks-skills-reference.md` (official docs)
- `.meta/references/state-of-the-art-vibe-coding.md` (finding #2: hooks > CLAUDE.md)
- `.meta/references/claude-code-leak-analysis.md` (Claude Code internal architecture)
- ADR-001 decision #4 (hooks > CLAUDE.md for enforcement)

---

## Problem

Instructions in CLAUDE.md have a compliance rate of ~70-80% (source: Boris Cherny,
creator of Claude Code, confirmed by the community). This means that 1 time in 4-5,
Claude ignores a rule written in CLAUDE.md.

For critical rules (formatting, lint, forbidden files), this is unacceptable.

EgoVault illustrates the problem: 13 rules in CLAUDE.md, 0 hooks, 0 automatic enforcement.
Result: no ruff configured, no pre-commit, no type checking. Rules are
documented but not enforced.

## Decision

The template generates a pre-configured `.claude/` directory with:

### 1. `settings.json` — Permissions and hooks

**What:** Claude Code configuration file, loaded automatically at each session.

**Permissions:**
- **Allow:** `Bash(uv *)`, `Bash(git status/diff/log/add/commit *)`, `Read`, `Edit(src/**)`, `Edit(tests/**)`
- **Deny:** `Bash(rm -rf *)`, `Bash(sudo *)`, `Edit(.env)`, `Edit(.git/**)`

**Why these permissions:**
- `uv` and `git` = daily tools, requesting them each time kills productivity
- `Read` = always safe, no need to ask
- `Edit` restricted to `src/` and `tests/` = prevents Claude from accidentally modifying config
- Deny `rm -rf` and `sudo` = basic security, irreversible
- Deny `.env` = prevents writing secrets into a file often accidentally gitignored

**Confidence level: HIGH** — Permissions are a well-documented pattern widely
adopted by the community. Worst case = too restrictive, user adjusts.

### 2. PostToolUse Hook — Auto-format ruff

**What:** After each `Edit` or `Write` of a `.py` file, automatically runs
`uv run ruff format` + `uv run ruff check --fix`.

**Why:**
- This is finding #2 from the state of the art: hooks = 100% compliance, CLAUDE.md = ~70-80%
- Writing "run ruff before committing" in CLAUDE.md is not enough
- The hook is silent (stderr redirected to /dev/null) — no noise if ruff is not installed
- The hook does not block (always exit 0) — it corrects but does not break the flow

**Where the idea comes from:**
- Official Claude Code docs (hook patterns for Python)
- Confirmed by the leak: internal Claude Code uses similar hooks
- ADR-001 pattern #4

**How to use it:** Transparent. The user has nothing to do. Each .py file
edited is auto-formatted. If the user wants to disable it: remove the block in settings.json.

**Confidence level: HIGH** — Standard pattern, well-documented, fail-safe (exit 0).
The only risk: ruff changes an import Claude just wrote → rare and fixable.

### 3. SessionStart Hook (compact) — Re-inject PILOT.md

**What:** When the context is compacted (context window full), the hook re-injects
the first 30 lines of `.meta/PILOT.md` so Claude does not lose the project state.

**Why:**
- Compaction deletes context to free up space
- CLAUDE.md is reloaded automatically, but PILOT.md is not
- Without this hook, after compaction Claude loses the session objective and project state
- 30 lines = enough for the title, phase, and status table

**Where the idea comes from:**
- Official docs: the `compact` matcher on `SessionStart` is built for this
- The "Dream Mode" pattern from the leak confirms the importance of inter-context persistence
- Our own experience: the PILOT.md cockpit is useless if it is not read

**Confidence level: MEDIUM** — The pattern is documented but has not yet been tested
in real conditions on a long project. The `head -30` is arbitrary. To be adjusted if
the PILOT.md format changes.

**Risk:** If PILOT.md does not exist, the `|| true` prevents the crash. But the hook is
silent = the user does not know if it works. No visible feedback.

### 4. Skill `/test` — pytest shortcut

**What:** `/test` command in Claude Code that runs `uv run pytest` with optional arguments.

**Why:**
- This is use case #1 for skills: shortcut for a frequent command
- The skill also parses the result (passed/failed/skipped) and suggests fixes
- Progressive disclosure: the description is always in context (~10% window),
  full content is only loaded when `/test` is invoked

**Where the idea comes from:**
- Official skills system docs
- Pattern "verification commands are highest-leverage CLAUDE.md content" (state of the art finding #4)
- Rather than putting "run pytest" in CLAUDE.md, make it an invocable skill

**How to use it:** Type `/test` in Claude Code, or `/test tests/tools/` for a subset.

**Confidence level: MEDIUM** — The skills system is relatively new. The SKILL.md
format and frontmatter could evolve. The skill is simple, so the risk of breakage is low.

---

## What we did NOT do (and why)

### settings.local.json
- Not generated — it is a personal file (gitignored by default by Claude Code)
- The user creates it if they want to override project permissions

### .mcp.json
- Not generated — MCP config is too specific to each user/environment
- Generating an empty file would be confusing ("what is MCP?")
- The user adds their MCP servers when needed

### Skills deploy, review, fix-issue
- Not generated — too specific, each project has different needs
- `/test` is the only universal skill
- Examples are documented in references, the user creates their own

### PreToolUse hook to block rm
- Not implemented — the `deny` in permissions does the same job more simply
- A hook would be redundant

### Sandbox
- Not enabled — sandbox is an advanced feature, not relevant for a bootstrap
- The user enables it if they have specific security needs

---

## Impacted files

| File | Action |
|------|--------|
| `template/.claude/settings.json.jinja` | CREATED — permissions + 2 hooks |
| `template/.claude/skills/test/SKILL.md` | CREATED — skill /test |

## How to modify

- Permissions: edit `permissions.allow` / `permissions.deny` in settings.json
- Hooks: add/remove blocks in `hooks.PostToolUse` / `hooks.SessionStart`
- Skills: create a folder in `.claude/skills/<name>/SKILL.md`
- MCP: create `.claude/.mcp.json` with server config
