# Ecosystem Deep Dive — Claude Code Tools & Patterns

**Date:** 2026-04-05
**Sources:** GitHub repos, mcpmarket.com, DeepWiki, web search (12 queries)

---

## 1. trailofbits/claude-code-config

Security-hardened global `~/.claude/settings.json` for Claude Code.

### Deny rules (full list)

Destructive commands: `rm -rf *`, `rm -fr *`, `sudo *`, `mkfs *`, `dd *`
Supply-chain: `wget *|bash*`, `wget *| bash*`
Git safety: `git push --force*`, `git push *--force*`, `git reset --hard*`
Shell config: `Edit(~/.bashrc)`, `Edit(~/.zshrc)`
Credentials: `Read(~/.ssh/**)`, `Read(~/.gnupg/**)`, `Read(~/.aws/**)`,
`Read(~/.azure/**)`, `Read(~/.config/gh/**)`, `Read(~/.git-credentials)`,
`Read(~/.docker/config.json)`, `Read(~/.kube/**)`, `Read(~/.npmrc)`,
`Read(~/.npm/**)`, `Read(~/.pypirc)`, `Read(~/.gem/credentials)`
Crypto wallets (macOS): metamask, electrum, exodus, phantom, solflare

### Hooks (PreToolUse, Bash matcher)

1. **Block rm -rf**: regex detects `-r`+`-f` flags in any order; prints "Use trash instead"
2. **Block push to main/master**: regex matches `git push.*(main|master)`; prints "Use feature branches"

### Other settings

- Telemetry disabled (`DISABLE_TELEMETRY=1`, `DISABLE_ERROR_REPORTING=1`)
- `enableAllProjectMcpServers: false` (security default)
- `alwaysThinkingEnabled: true`
- `cleanupPeriodDays: 365`
- No skills shipped (config-only repo)

### Take for our template

- **Adopt deny rules for credentials** — add `Read(~/.pypirc)`, `Read(~/.ssh/**)` etc to settings.json.jinja
- **Adopt the 2 hooks** — rm -rf blocker + push-to-main blocker are minimal and high-value
- **Set `enableAllProjectMcpServers: false`** as default
- Telemetry env vars are a user choice, don't force in template

### Ignore

- macOS-specific crypto wallet paths (irrelevant for Python dev template)
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` (experimental flag, may break)

---

## 2. mcpmarket.com — uv Python skills

Multiple competing skills exist. Best reference: `s2005/uv-skill` (GitHub).

### Key patterns from uv skills

- **Decision framework**: `uv tool install` for persistent tools vs `uvx` for ephemeral
- **MCP servers**: always use `uvx`, never `uv tool install`
- **Commands standardized**: `uv sync`, `uv run`, `uv venv`, `uv python install`
- **Version pinning**: use `--from package@version` in production
- **Don't mix**: never mix pip and uv tool installations
- **Python version**: track via `.python-version` file

### Take for our template

- Our CLAUDE.md already enforces `uv` exclusively — validated as correct approach
- Consider adding a `uv` skill to `.claude/skills/` that codifies the decision framework
- The `uvx` vs `uv tool install` distinction is useful for GUIDELINES.md

### Ignore

- MCP server integration patterns (out of scope for project template)
- Most mcpmarket skills are low-quality duplicates; don't reference directly

---

## 3. hesreallyhim/awesome-claude-code — Notable tools

### agnix (agent-sh/agnix)

Linter for AI coding assistant config files. **385 rules** across platforms.

- **CLAUDE.md rules** (CC-*): 53 rules — structure, generic instruction detection, field validation
- **SKILL.md rules** (AS-*, CC-SK-*): 31 rules — frontmatter, naming, content structure
- **AGENTS.md rules** (AGM-*, XP-*): 13 rules
- **MCP rules** (MCP-*): 12 rules
- Install: `npm install -g agnix` or `brew install agnix` or `cargo install agnix-cli`
- IDE plugins: VS Code, JetBrains, Neovim, Zed

**Take:** Add agnix to recommended tooling in GUIDELINES.md. Consider adding a
pre-commit hook: `agnix lint .` to validate CLAUDE.md + SKILL.md on commit.

**Ignore:** IDE plugin setup (user choice, not template concern).

### claude-devtools (matt1398/claude-devtools)

Desktop app for Claude Code session observability. Reads local session logs passively.

- Turn-based context attribution timeline
- Compaction visualization (shows when context window compresses)
- Subagent execution trees (recursive, with token/cost metrics)
- Custom notification triggers

**Take:** Recommend in ecosystem/tooling docs. Not a template dependency.

**Ignore:** No integration needed — it's a standalone desktop app.

### Other relevant tools

- **rulesync** (dyoshikawa/rulesync): generates configs for multiple AI agents with
  bi-directional conversion. Relevant if we ever support non-Claude agents.
- **learn-claude-code** (shareAI-lab): 300-line Python agent reconstruction.
  Educational only.

---

## 4. tadaspetra/loop

**Not a Claude Code skill.** It's a desktop video editing app (Electron + ffmpeg)
for screen recordings. The similarly-named `/loop` is a **built-in Claude Code skill**
(shipped March 2026) that runs prompts on a recurring interval.

### Built-in /loop skill

- Syntax: `/loop 5m /test` — runs /test every 5 minutes
- Session-scoped (dies with terminal), 3-day auto-expiry, 50-task cap
- Use cases: polling CI, watching test results, periodic linting

**Take:** Not relevant for template. It's a built-in, not something we ship.

**Ignore:** Entirely. tadaspetra/loop is unrelated. Built-in /loop needs no template support.

---

## 5. anthropics/skills — Official reference

### Available skills

Categories: Creative & Design, Development & Technical, Enterprise & Communication,
Document skills (docx, pdf, pptx, xlsx — source-available, not Apache 2.0).

Notable: `skill-creator` (meta-skill that creates new skills), `mcp-builder`.

### Canonical SKILL.md format

```yaml
---
name: skill-name
description: What it does and WHEN Claude should use it.
---
```

Followed by markdown instructions. That's it. Minimal by design.

**Required fields:** `name`, `description` (in frontmatter)
**Optional structure:** `# Instructions`, `## Examples`, `## Guidelines`
**Optional resources:** `scripts/`, `references/`, `assets/` subdirectories

### Take for our template

- Our skills already follow this format — validated as correct
- The `description` field should include trigger conditions ("Use when...")
- Consider adding a `skill-creator` equivalent or reference to help users make new skills
- `references/` subdirectory pattern is useful for skills needing external docs

### Ignore

- Document skills (docx/pptx/xlsx) — different license, not relevant
- Plugin configuration (`.claude-plugin/`) — for marketplace distribution only

---

## Summary: Priority actions for metadev-protocol

| Priority | Action | Source |
|----------|--------|--------|
| HIGH | Add credential deny rules to settings.json.jinja | trailofbits |
| HIGH | Add rm-rf + push-to-main hooks to settings.json.jinja | trailofbits |
| HIGH | Set `enableAllProjectMcpServers: false` | trailofbits |
| MED | Add agnix to recommended tooling / pre-commit | agnix |
| MED | Add uv decision framework to GUIDELINES.md | mcpmarket/uv-skill |
| LOW | Document claude-devtools as recommended companion | claude-devtools |
| LOW | Add `references/` subdir convention to skill template | anthropics/skills |
| SKIP | /loop, tadaspetra/loop, crypto wallet paths, rulesync | various |
