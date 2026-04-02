# Context Management Patterns for AI-Assisted Development

**Date:** 2026-04-02
**Purpose:** Reference catalogue for metadev-protocol template design

---

## 1. Context Compaction

### 1a. Auto-Compact Threshold
- **What:** Claude Code auto-compacts at ~95% capacity (~33K token buffer as of 2026).
- **Key insight:** Compaction is lossy. Project conventions stated once at session start are prime candidates for loss.
- **Best practice:** Manual `/compact` at natural breakpoints (task done, before complex ops) beats random auto-compact.
- **Source:** [Claude API Docs - Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction), [Context Buffer Analysis](https://claudefa.st/blog/guide/mechanics/context-buffer-management)
- **Complexity:** Low (built-in)

### 1b. Directed Compact
- **What:** `/compact focus on the API changes` -- tell compaction what to preserve.
- **Source:** [Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)
- **Complexity:** Low

### 1c. Post-Compaction Hook (Context Re-injection)
- **What:** A `SessionStart` hook with matcher `"compact"` fires after compaction and re-injects 10-50 lines of critical context via stdout.
- **Key insight:** CLAUDE.md (200 lines, permanent) vs. "context essentials" (10-50 lines, surgical post-compact injection). Keep them separate.
- **Source:** [Nick Porter - Post-Compaction Hooks](https://medium.com/@porter.nicholas/claude-code-post-compaction-hooks-for-context-renewal-7b616dcaa204), [post_compact_reminder](https://github.com/Dicklesworthstone/post_compact_reminder)
- **Complexity:** Medium (requires hooks config)

### 1d. Pre-Compact Context Backup (claude-code-soul)
- **What:** Captures conversation context before compaction, writes to daily log. Restores identity + recent history on every session start.
- **Source:** [claude-code-soul](https://github.com/israelmirsky/claude-code-soul)
- **Complexity:** Medium

---

## 2. Memory Persistence Across Sessions

### 2a. CLAUDE.md Hierarchy (Built-in)
- **What:** Three-tier file-based memory: Global (~/.claude/CLAUDE.md) > Project (CLAUDE.md) > Personal. Loaded every session start.
- **Rule of thumb:** Keep under 200 lines per file. Use markdown structure. Split with .claude/rules/ if growing.
- **Source:** [Claude Code Docs - Memory](https://code.claude.com/docs/en/memory)
- **Complexity:** Low

### 2b. Scoped Rules Directory
- **What:** Place .claude/rules/*.md files, each covering one topic. Rules can be path-scoped (only load when Claude touches matching files).
- **Key insight:** Reduces noise and saves context by loading rules on-demand, not all at once.
- **Source:** [CLAUDE.md Hierarchy - DeepWiki](https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/4.1-claude.md-files-and-memory-hierarchy)
- **Complexity:** Low

### 2c. Auto Memory (Claude-Managed)
- **What:** Claude saves notes for itself across sessions (~/.claude/projects/.../MEMORY.md). First 200 lines / 25KB auto-loaded. Requires Claude Code >= v2.1.59.
- **Source:** [Claude Code Docs - Memory](https://code.claude.com/docs/en/memory)
- **Complexity:** Low (built-in, opt-in)

### 2d. Rewrite-Don't-Append Pattern
- **What:** Session context file is fully rewritten each session, not appended to. Prevents unbounded growth and stale context accumulation.
- **Relevance:** Already used in our template (SESSION-CONTEXT.md.jinja).
- **Source:** Community pattern, [context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit)
- **Complexity:** Low

### 2e. Tiered Memory (memory-mcp)
- **What:** Tier 1 = CLAUDE.md (~150 lines, auto-generated briefing). Tier 2 = .memory/state.json (unlimited, full fact store, accessed via MCP tools mid-conversation).
- **Source:** [DEV Community - Persistent Memory Architecture](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d)
- **Complexity:** High (MCP server)

---

## 3. Subagent Context Isolation

### 3a. Verbose Task Delegation
- **What:** Farm out test runs, log processing, doc fetching to subagents. Only summary returns to main context. Saves (X + Y) * N tokens.
- **Rule of thumb:** If a task touches >5 files, isolate it in a subagent.
- **Source:** [RichSnapp - Context Management with Subagents](https://www.richsnapp.com/article/2025/10-05-context-management-with-subagents-in-claude-code)
- **Complexity:** Medium

### 3b. Parallel Research Subagents
- **What:** Spawn multiple subagents for independent investigations (different modules, different questions). Results merge in main context as summaries only.
- **Source:** [AWS Builder Center - Subagents Guide](https://builder.aws.com/content/2wsHNfq977mGGZcdsNjlfZ2Dx67/unleashing-claude-codes-hidden-power-a-guide-to-subagents)
- **Complexity:** Medium

### 3c. Master-Clone Architecture
- **What:** Put all key context in CLAUDE.md, then let the main agent dynamically delegate to copies of itself. All clones inherit project context via CLAUDE.md.
- **Key insight:** Avoids the "handoff problem" where subagents start with blank slate.
- **Source:** [Level Up Coding - Mental Model for Claude Code](https://levelup.gitconnected.com/a-mental-model-for-claude-code-skills-subagents-and-plugins-3dea9924bf05)
- **Complexity:** Medium

### 3d. /btw for Quick Questions
- **What:** Use /btw instead of a subagent for quick questions. Sees full context, no tool access, answer discarded (does not pollute history).
- **Source:** [Shrivu Shankar - Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- **Complexity:** Low

---

## 4. Session Handoff

### 4a. Structured Handoff Document
- **What:** At session end, generate a markdown handoff: completed tasks, decisions made (with rationale), current state, blockers, next steps. Next session reads it first.
- **Key insight:** "Fixed race condition by adding mutex" >> "fixed bug". Rationale matters.
- **Source:** [DEV - Session Handoffs](https://dev.to/dorothyjb/session-handoffs-giving-your-ai-assistant-memory-that-actually-persists-je9)
- **Complexity:** Low

### 4b. Branch-Scoped Handoffs
- **What:** Store handoffs at `.agents/handoffs/{branch}/{session}.md`. Delete when branch merges. Handoffs are read-only context, never modified during active work.
- **Source:** [DeepWiki - ai-agents Session Logs](https://deepwiki.com/rjmurillo/ai-agents/4.6-session-logs-and-handoff.md)
- **Complexity:** Low

### 4c. Handoff Chains
- **What:** Linked chain: handoff-1.md -> handoff-2.md -> handoff-3.md. Read most recent first, reference predecessors as needed.
- **Source:** [DEV - Never Lose Context](https://dev.to/nao_lore/how-to-never-lose-context-between-ai-sessions-6ci)
- **Complexity:** Low

### 4d. Plan-Then-Clear Pattern
- **What:** Plan in one session, write spec to file, start fresh session for execution. Clean context focused entirely on implementation.
- **Source:** [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices), [context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit)
- **Complexity:** Low

---

## 5. Notable Toolkits

| Toolkit | Focus | Link |
|---------|-------|------|
| everything-claude-code (affaan-m) | Skills, memory, security, token optimization | [GitHub](https://github.com/affaan-m/everything-claude-code) |
| Superpowers | Active Workflow Engine, shared JSON state, VS Code extension | [GitHub](https://github.com/abudhahir/superpowers) |
| context-engineering-kit (NeoLab) | Minimal-token skills, spec-driven dev, subagent-driven dev | [GitHub](https://github.com/NeoLabHQ/context-engineering-kit) |
| CONTINUITY | MCP server: crash recovery, decision registry, context compression | [GitHub](https://github.com/duke-of-beans/CONTINUITY) |
| awesome-claude-code-subagents | Curated subagent patterns incl. context-manager | [GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents) |

**Key warning from everything-claude-code:** Don't enable all MCPs at once -- your 200K context window can shrink to 70K with too many tools loaded.

---

## Relevance to metadev-protocol

| Pattern | Already in template | Action |
|---------|-------------------|--------|
| Rewrite-don't-append (2d) | Yes (SESSION-CONTEXT.md) | Keep |
| PILOT.md as session start (4a) | Yes | Keep |
| Post-compact hook (1c) | No | Consider for template/.claude/settings.json |
| Scoped rules (2b) | No | Consider for .claude/rules/ |
| Plan-then-clear (4d) | Partially (5-phase workflow) | Reinforce in CLAUDE.md |
| Subagent delegation (3a) | Not explicit | Document as guidance in CLAUDE.md |
