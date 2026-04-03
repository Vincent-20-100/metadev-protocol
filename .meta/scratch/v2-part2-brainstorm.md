# Brainstorm — Knowledge Hierarchy (Part 2)

**Date:** 2026-04-02
**Status:** IN PROGRESS — L1/L2/L3 approach selected, RAG question open

---

## Problem

Context compaction in Claude Code is flat:
- Keeps too many tokens of low-value detail (debug traces from 3 sessions ago)
- Loses high-value decisions (architectural choices)
- No way to "go back" to older conversations once compacted
- No multi-layer structure = no selective recall

The pain is: **context loss between sessions**, even with SESSION-CONTEXT.md and auto-compaction.

## Decision 1: Temporal layers (L1/L2/L3)

**Choice:** Cache-like temporal layers. Rejected: thematic-only (too complex to maintain), hybrid (premature).

| Layer | File | Content | Loaded when |
|-------|------|---------|-------------|
| **L1 (hot)** | SESSION-CONTEXT.md | Current session — rewritten live | Every session, automatically |
| **L2 (warm)** | INDEX.md or MEMORY.md | Key decisions from last ~5 sessions, condensed | Every session, automatically |
| **L3 (cold)** | sessions/ archive | Full session summaries, consultable | On demand, when LLM needs to dig |

LLM loads L1+L2 at session start. L3 only when searching for something specific.

## Open question: Mini-RAG on all conversations?

**Idea:** Keep ALL conversation exports, index them, let the LLM search semantically.

**For:**
- Total recall — nothing is ever lost
- Could find patterns across sessions

**Against:**
- Needs embedding infra (local or API) — significant complexity
- Claude Code doesn't natively export conversations in a structured format
- Retrieval quality depends on chunking strategy
- The L1/L2/L3 system already captures the SIGNAL — RAG keeps everything including noise
- ROI unclear: how often do you actually need session #3's exact conversation?

**Preliminary assessment:** Too ambitious for v2. The L1/L2/L3 system solves 90% of the problem with 10% of the complexity. RAG could be Part 6 if the need is confirmed after using L1/L2/L3.

## Next questions to brainstorm (next session)

1. What goes in L2 (INDEX.md/MEMORY.md)? Structure, size limit, what gets promoted from L1
2. How does L1 → L2 promotion work? Manual (/save-progress does it) or automatic?
3. What format for L3 session archives? Full dump or structured summary?
4. Skills involved: /digest (L3 → L2 extraction), /tidy (cleanup), /dream (auto-pattern extraction)
5. How does the LLM know when to consult L3? Explicit instruction or automatic detection?
