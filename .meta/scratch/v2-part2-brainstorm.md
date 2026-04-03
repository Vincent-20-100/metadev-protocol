# Brainstorm — Knowledge Hierarchy (Part 2)

**Date:** 2026-04-03
**Status:** DONE — decisions finalized

---

## Problem

Context compaction in Claude Code is flat:
- Keeps too many tokens of low-value detail (debug traces from 3 sessions ago)
- Loses high-value decisions (architectural choices)
- No way to "go back" to older conversations once compacted
- No multi-layer structure = no selective recall

The pain is: **context loss between sessions**, even with SESSION-CONTEXT.md and auto-compaction.

## Research inputs

### Claude Code native (Anthropic docs)
- CLAUDE.md: always loaded, shared via git
- MEMORY.md: auto-memory, **capped at 200 lines / 25KB**, truncated silently beyond
- Topic files `memory/*.md`: loaded **on-demand only**
- `/compact` re-reads all files from disk — file-based instructions survive compaction
- No automatic promotion from conversation to CLAUDE.md

### DeepAgents (langchain-ai/deepagents)
- 3 tiers: system prompt (AGENTS.md) → active conversation → archived markdown
- Compaction trigger at **85% capacity**, keeps 10% most recent
- Evicted messages → timestamped markdown files (accessible but never auto-loaded)

## Decision 1: Temporal layers (L1/L2/L3)

**Choice:** Cache-like temporal layers aligned with Claude Code native mechanisms.

| Layer | Maps to | Content | Loaded when |
|-------|---------|---------|-------------|
| **L1 (hot)** | SESSION-CONTEXT.md | Current session state — rewritten live | Every session (CLAUDE.md says "read first") |
| **L2 (warm)** | Native MEMORY.md + PILOT.md | Key decisions, project state | Every session (auto-loaded by Claude Code) |
| **L3 (cold)** | `.meta/sessions/` archive | Full session summaries | On demand (CLAUDE.md instruction) |

**Key insight:** Claude Code already HAS an L2 (MEMORY.md + topic files). We don't reinvent it — we **orchestrate** it. Our value-add is the `.meta/` structure (PILOT.md, SESSION-CONTEXT.md, sessions/) that gives semantic meaning above the raw mechanism.

## Decision 2: Mini-RAG — deferred

**Status:** Too ambitious for v2. L1/L2/L3 solves 90% of the problem with 10% of the complexity. Revisit as Part 6 if need confirmed after using L1/L2/L3.

## Decision 3: Answers to open questions

| # | Question | Answer |
|---|----------|--------|
| 1 | What goes in L2? | **Native MEMORY.md** (auto) + **PILOT.md** (manual via /save-progress). No new file. |
| 2 | L1 → L2 promotion? | **Hybrid**: auto-memory writes to MEMORY.md + /save-progress updates PILOT.md and SESSION-CONTEXT.md |
| 3 | L3 format? | **Structured summary** in `sessions/YYYY-MM-DD.md` (like DeepAgents' conversation_history/) |
| 4 | Skills needed? | **/save-progress only**. /digest, /dream, /tidy = YAGNI. Revisit if L1/L2/L3 proves insufficient. |
| 5 | When to consult L3? | **Instruction in CLAUDE.md**: "if you lack context on a past decision, check `.meta/sessions/`" |

## Impact on Part 1 spec

No changes needed — Part 1 spec already covers /save-progress correctly. The knowledge hierarchy decisions validate the approach without adding scope.
