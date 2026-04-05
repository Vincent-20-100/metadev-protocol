# Claude Code Official Docs — Comprehensive Audit

> Source: claude-code-guide agent, official documentation scan
> Date: 2026-04-05
> Purpose: Find features missed for metadev-protocol template

---

## New features discovered (not in our knowledge base)

### 1. AGENTS.md — Multi-agent standard (HIGH RELEVANCE)
- Shared instruction file for projects using multiple AI coding agents
- Claude Code reads CLAUDE.md, can import AGENTS.md via `@AGENTS.md`
- Standard format across Deep Agents, Codeium, etc.
- **Action:** Add optional import in CLAUDE.md.jinja, mention in GUIDELINES.md

### 2. .claude/rules/ — Path-scoped modular instructions (HIGH RELEVANCE)
- Split instructions into topic-specific .md files
- Path-scoped via frontmatter: `paths: ["src/api/**"]`
- Lazy-loaded: only loaded when Claude touches matching files
- User-level rules in `~/.claude/rules/` apply to all projects
- **Action:** Generate starter rules files (testing.md, security.md, code-style.md)

### 3. Plan mode — Read-only analysis mode (MEDIUM RELEVANCE)
- `--permission-mode plan` or Shift+Tab
- Claude explores, asks questions, proposes plan before changes
- Can set `defaultMode: "plan"` in settings.json
- **Action:** Document in GUIDELINES.md as recommended practice for complex refactors

### 4. Subagent persistent memory (MEDIUM RELEVANCE)
- `memory: user` → persistent memory across all projects for an agent role
- `memory: project` → project-specific agent memory
- Stored in `~/.claude/agent-memory/<name>/MEMORY.md` or `.claude/agent-memory/`
- **Action:** Document in GUIDELINES.md for long-lived roles (reviewer, debugger)

### 5. Status line (LOW-MEDIUM RELEVANCE)
- Custom status bar via shell script
- Shows context %, cost, git branch, model, rate limits
- Configured in settings.json: `"statusLine": {"type": "command", "command": "script.sh"}`
- **Action:** Could generate a basic statusline.sh in template

### 6. Agent Teams — experimental (TRACK FOR PART 5)
- Multiple Claude Code sessions as coordinated team
- Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Lead session + teammates with shared task list
- **Action:** Already planned for Part 5, confirmed aligned

### 7. Channels — research preview (TRACK FOR FUTURE)
- MCP servers push events from external systems (Slack, Discord, webhooks)
- Two-way communication (Claude can reply)
- Permission relay: remote approval from chat
- **Action:** Note in GUIDELINES.md for CI/monitoring integration

### 8. Output styles (LOW RELEVANCE)
- Custom response format via .md files in `.claude/output-styles/`
- Built-in: default, verbose, concise, thinking
- **Action:** YAGNI for template, document if needed

### 9. Hook: InstructionsLoaded (LOW RELEVANCE)
- Fires when CLAUDE.md or rules files are loaded
- Useful for debugging "why isn't my rule working?"
- **Action:** Mention in troubleshooting section of GUIDELINES.md

### 10. Hook: FileChanged / CwdChanged (LOW RELEVANCE)
- Fires when files change or directory changes
- Use case: reload direnv, detect new config files
- **Action:** Optional example for direnv users

### 11. Worktree config (MONOREPO-SPECIFIC)
- `symlinkDirectories`: symlink large dirs instead of cloning to worktree
- `sparsePaths`: sparse-checkout for monorepo speed
- **Action:** Not relevant for single-project template, track for monorepo profile

### 12. Subagent isolation: worktree (ADVANCED)
- `isolation: "worktree"` in agent frontmatter
- Agent gets isolated git branch for parallel work
- Auto-cleaned if no changes
- **Action:** Document as advanced pattern in GUIDELINES.md

---

## Summary: what to add to metadev-protocol

| Feature | Priority | Action |
|---------|----------|--------|
| .claude/rules/ directory | **HIGH** | Generate starter rules (testing, security, code-style) |
| AGENTS.md import | **HIGH** | Add `@AGENTS.md` import option in CLAUDE.md.jinja |
| Plan mode recommendation | MEDIUM | Add to GUIDELINES.md |
| Subagent persistent memory | MEDIUM | Document in GUIDELINES.md |
| Status line template | LOW-MED | Optional statusline.sh.jinja |
| Agent Teams | TRACK | Part 5 already planned |
| Channels | TRACK | Future enhancement |
| Output styles | YAGNI | Skip |
| InstructionsLoaded hook | LOW | Troubleshooting guide |
| FileChanged/CwdChanged | LOW | Optional direnv example |
| Worktree config | N/A | Monorepo only |
| Subagent worktree isolation | LOW | Document as advanced pattern |
