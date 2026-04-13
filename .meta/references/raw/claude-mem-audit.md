# Audit — thedotmack/claude-mem

**Source:** https://github.com/thedotmack/claude-mem
**Date:** 2026-04-13
**Stars:** ~unknown (active project)
**License:** AGPL-3.0 core / PolyForm ragtime
**Stack:** TypeScript + Bun + SQLite + Chroma + React

---

## What it is

Claude Code plugin that auto-captures tool usage during sessions, compresses observations via Claude Agent SDK, and injects relevant context at session start. Goal: make Claude remember what it worked on across disconnected sessions — zero manual intervention.

---

## Architecture

```
5 lifecycle hooks  →  Worker HTTP API (:37777)  →  SQLite + Chroma
SessionStart            Express + Bun               FTS5 + vector search
UserPromptSubmit
PostToolUse
Summary
SessionEnd
```

**Key components:**
- `src/hooks/*.ts` — compiled to `plugin/scripts/*-hook.js`
- `src/services/worker-service.ts` — async AI task queue
- `src/services/sqlite/` — persistence layer
- `plugin/skills/mem-search/SKILL.md` — HTTP API skill, auto-invoked on past-session references
- `src/services/sync/ChromaSync.ts` — semantic search
- `src/ui/viewer/` → `plugin/ui/viewer.html` — React debug UI at localhost:37777

---

## Notable patterns

### 1. Progressive disclosure — 3-layer retrieval
Most important pattern. Retrieval in 3 stages:
- **Layer 1:** compact index — IDs + similarity score only (~50-100 tokens/result)
- **Layer 2:** timeline context around matched IDs
- **Layer 3:** full observation for filtered IDs only (~500-1000 tokens)

Claimed: ~10× token savings vs dumping full chunks. Applies whenever you have a large KB that shouldn't be fully injected.

### 2. Exit code strategy — 3 levels
```
Exit 0 → success or graceful shutdown
Exit 1 → non-blocking error (shown to user, Claude continues)
Exit 2 → blocking error (fed to Claude as constraint)
```
More nuanced than binary pass/fail. Prevents Windows Terminal tab accumulation. Directly applicable to pre-commit hooks and skill error handling.

### 3. `<private>` tag filtering
Users wrap sensitive content in `<private>content</private>`. Stripping happens at hook layer before data reaches worker or DB. Fine-grained privacy without schema changes.

### 4. Open-source core / Pro features separation
All localhost:37777 endpoints remain publicly accessible. Pro = headless features with minimal integration points. Future enhanced UI connects to same endpoints without modifying core. Clean separation that doesn't break OSS users.

### 5. Skills as part of plugin
`plugin/skills/mem-search/SKILL.md` auto-invoked on specific triggers. Same SKILL.md pattern as metadev-protocol — confirms the pattern is portable across different Claude Code plugin architectures.

---

## Relevance to metadev-protocol

| Pattern | Applicability | Where |
|---------|--------------|-------|
| Progressive disclosure | HIGH — /radar KB injection | `skills/radar/SKILL.md` — avoid dumping full INDEX.md |
| Exit code 0/1/2 | MEDIUM — hook nuance | `check_git_author.py`, future hooks |
| `<private>` tag | LOW — not a problem metadev solves | — |
| Skill auto-invocation | CONFIRMED — we already do this | pattern validated externally |

---

## What to borrow vs ignore

**Borrow:**
- Progressive disclosure for /radar INDEX.md injection (Layer 1 only by default, full on --deep)
- Exit code 3-level pattern for any hook that has non-blocking vs blocking failure modes

**Ignore:**
- The entire persistence/DB architecture (different problem scope)
- Chroma/vector search (not needed for metadev's use cases)
- HTTP worker / web UI (overkill)
