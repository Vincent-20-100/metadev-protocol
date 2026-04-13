# Audit — getcompanion-ai/feynman

**Source:** https://github.com/getcompanion-ai/feynman
**Date:** 2026-04-13
**Stars:** 4.8k / 597 forks
**License:** MIT
**Stack:** TypeScript 59% + JS 18.7% + Astro

---

## What it is

CLI tool for AI-driven research workflows. Runs multi-agent pipelines to do literature reviews, paper audits, experiment replication, and research synthesis. Built on Pi (agent framework) + AlphaXiv (paper search).

---

## Architecture

```
CLI  →  4 specialized agents  →  outputs/ + provenance sidecars
         Researcher
         Reviewer
         Writer
         Verifier
```

**Skills:** 19 Markdown skill files in `skills/`, synced to `~/.feynman/agent/skills/` on startup. Same SKILL.md pattern as metadev-protocol.

**Key commands:**
- `feynman "topic"` → cited research brief
- `/deepresearch` → multi-agent investigation + synthesis
- `/lit` → literature review with consensus/disagreements
- `/audit` → paper-vs-codebase verification
- `/replicate` → experiment replication on GPU

---

## Notable patterns

### 1. Provenance sidecar — `.provenance.md`
**Most important pattern.** Every research output has a companion `.provenance.md` sidecar that tracks:
- Source origins (where each claim came from)
- Evidence chains (how findings were derived)
- Verifiable URLs for all assertions

This is source grounding as a first-class artifact, not just inline citations. The sidecar is separate from the output so it can be audited, diffed, and versioned independently.

**Direct relevance to metadev-protocol PM.5** (provenance sidecar convention — deferred). Feynman ships exactly this pattern. Not speculative.

### 2. Multi-agent research: parallel gather → synthesize
The `/deepresearch` pattern:
1. Multiple Researcher agents run **in parallel**, gathering evidence independently
2. Verifier validates each claim
3. Reviewer synthesizes + detects conflicts between parallel findings
4. Writer produces the final output

Key insight: parallel agents don't coordinate during research (avoid herding), then a dedicated synthesis step handles conflicts. Same isolation principle as the /debate skill.

### 3. Skills as synced markdown files
Skills live in `skills/<name>/SKILL.md` in the repo, synced to `~/.feynman/agent/skills/` at startup. Confirms:
- The SKILL.md pattern is independently converged upon by multiple teams
- Syncing to a user-global dir is a valid distribution mechanism (vs always requiring project-local skills)
- 19 skills in production — the pattern scales

### 4. Session search + resume
Sessions stored as JSONL in `~/.feynman/sessions/`. `grep -ril "topic" ~/.feynman/sessions/` works for lightweight search. `/search` opens interactive UI. Sessions can be resumed.

Observation: metadev-protocol's SESSION-CONTEXT.md is a simpler version of this — single-file vs JSONL store. Feynman's approach is more powerful for long-running multi-session research but heavier.

### 5. Source grounding as invariant
All claims must link to verifiable URLs — no unsourced assertions. Enforced by the Verifier agent, not by the user. This is a quality gate, not a convention.

---

## Relevance to metadev-protocol

| Pattern | Applicability | Where |
|---------|--------------|-------|
| Provenance sidecar (.provenance.md) | HIGH — validates PM.5, should un-defer | `/research` skill output, /radar cards |
| Parallel gather → synthesize (no herding) | HIGH — applies to PM.14 synthesis run design and /debate | Already in /debate; apply to PM.14 |
| Skills as synced markdown | CONFIRMED — we already do this | pattern validated at 4.8k stars |
| Source grounding as Verifier gate | MEDIUM — add to /research skill | `skills/research/SKILL.md` |
| Session JSONL + resume | LOW — SESSION-CONTEXT.md is sufficient for metadev's scope | — |

---

## What to borrow vs ignore

**Borrow:**
- Provenance sidecar pattern for /research and /radar outputs — each synthesis doc gets a `.provenance.md` tracking where its claims came from
- Parallel-then-synthesize agent pattern for PM.14 and any future multi-agent research run
- Source grounding enforcement (Verifier role) in /research skill refactor

**Ignore:**
- The full agent framework (Pi) — different scope
- AlphaXiv / academic paper focus — metadev is code-focused
- GPU compute integrations (Modal, RunPod) — irrelevant
- Session JSONL store — SESSION-CONTEXT.md serves the purpose at lower complexity
