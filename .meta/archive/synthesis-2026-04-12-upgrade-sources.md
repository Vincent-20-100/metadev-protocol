---
type: synthesis
date: 2026-04-12
slug: upgrade-sources
status: active
---

# Synthesis — Upgrade sources for metadev-protocol post-v1.0.0

**Sources audited:**
1. safishamsi/graphify — knowledge graph tool (audit 2026-04-12)
2. GuillaumeDesforges/claude-ai-project-starter — AI-native project template (brainstorm 2026-04-12)
3. getcompanion-ai/feynman — multi-agent research system (audit 2026-04-12)
4. yedanzhang-ai/earnings-call-analyst — LLM pipeline with tiered verification (audit 2026-04-12)

---

## Tier 1 — Implemented (v1.0.1) — post-debate

| Pattern | Source | Status | Notes |
|---------|--------|--------|-------|
| Honesty guardrails | Feynman | DONE | Rule #9 in CLAUDE.md.jinja — consensus 3/3 in debate |
| Tiered confidence gates | earnings-call | DONE | GREEN/AMBER/RED in plan skill |
| Synthesis type + slug lineage | Feynman | DONE | New type in check_meta_naming.py + convention in GUIDELINES |
| Working with AI (trimmed) | claude-ai-starter | DONE | Anti-patterns trio, ADR 4-question template, practical defaults only |
| CREDITS.md update | Feynman + earnings-call | DONE | Added both repos |
| ~~Provenance sidecar~~ | Feynman | DEFERRED | Debate: useful at week 3+, not day 1. Moved to PM.5 |
| ~~Philosophy batch (full)~~ | claude-ai-starter | TRIMMED | Debate: manifesto not scaffold. Kept actionable items, removed opinions |

## Tier 2 — Medium effort, needs spec (v1.1.0)

| Pattern | Source | Description |
|---------|--------|-------------|
| Versioned prompt files | earnings-call | Extract prompts from skills into versioned files with config selector |
| Verification persona | Feynman | /verify skill that cross-checks claims vs actual code state |
| Vision scaffolding (C1) | claude-ai-starter | /vision skill: problem statement, target user, principles, V1 scope, north star |
| /research skill (C3) | claude-ai-starter | User discovery + competitive + sector research |
| Resumable session state | Feynman | Structured "last action / next step" block in SESSION-CONTEXT.md |

## Tier 3 — Backlog (post v1.1.0)

| Pattern | Source |
|---------|--------|
| Wiki tier (C2) | claude-ai-starter |
| Eval/verification history | earnings-call |
| Schema-as-governance (Pydantic) | earnings-call |
| Work-stream tags (C5) | claude-ai-starter |
| Cache incremental SHA256 | Graphify |
| Surprise scoring | Graphify |

## Rejected

| Pattern | Reason |
|---------|--------|
| Shape Up / PostHog defaults | Too opinionated for a template |
| Nix-adjacent defaults | Not portable to Python-first stance |
| Manual bootstrap playbook | Redundant with Copier |
| Scale-aware delegation | Relevant for multi-agent runtime, not a template |

---

## References

- Brainstorm: `.meta/active/brainstorm-2026-04-12-claude-ai-project-starter.md`
- Memory: `reference_graphify_audit.md`
- Feynman repo: https://github.com/getcompanion-ai/feynman
- Earnings-call repo: https://github.com/yedanzhang-ai/earnings-call-analyst
