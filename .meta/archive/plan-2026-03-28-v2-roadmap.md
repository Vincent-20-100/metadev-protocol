# v2 Phase C — Roadmap

**Date:** 2026-04-02
**Status:** Part 1 DONE, Part 2 brainstorm DONE, Parts 3-5 pending

---

## Part 1: Superpowers Integration (SPEC DONE)
- Integrate Superpowers plugin (output redirect, auto-install recommendation)
- Rename /ship → /save-progress
- Keep /brainstorm + /plan as fallbacks
- Drop /consolidate (YAGNI)
- Spec: `.meta/scratch/v2-part1-spec.md`

## Part 2: Knowledge Hierarchy (BRAINSTORM DONE)
- L1/L2/L3 temporal layers aligned with Claude Code native memory
- L1 = SESSION-CONTEXT.md (hot), L2 = native MEMORY.md + PILOT.md (warm), L3 = sessions/ archive (cold)
- /digest, /dream, /tidy dropped (YAGNI) — /save-progress covers L1→L2 promotion
- Mini-RAG deferred to Part 6 if L1/L2/L3 proves insufficient
- Spec: `.meta/scratch/v2-part2-brainstorm.md`

## Part 3: Infrastructure (TO BRAINSTORM)
- GitHub Actions CI for the template repo
- Config 3 levels (app profile — system/user/install)
- Language params in copier.yml (project_language, dev_language)

## Part 4: Profile-Specific Skills (TO BRAINSTORM)
- Depends on Parts 1+2 (follows established patterns)
- /api-test (app profile)
- /pipeline-run (data profile)
- /backtest (quant profile)

## Part 5: Multi-Agent Support — AGENTS.md (TO BRAINSTORM)
- Generate AGENTS.md alongside CLAUDE.md in template
- AGENTS.md = universal instructions (automatisms, rules, workflow) — works with any agent
- CLAUDE.md = Claude Code-specific features (skills, hooks, settings.json)
- Split is mechanical — content already exists, just needs separation
- Opens compatibility with: OpenAI Codex, Google Jules, Cursor, Gemini CLI, GitHub Copilot, Devin, Deep Agents, etc.
- Reference: https://agents.md/ (Linux Foundation, 60K+ projects)

---

## Recommended ecosystem

Repos and tools to watch/recommend in generated projects:

| Name | What | Link |
|------|------|------|
| **obra/superpowers** | Claude Code plugin — 14 workflow skills (brainstorming, debugging, TDD, code review) | https://github.com/obra/superpowers |
| **anthropics/claude-code** | Claude Code official — the CLI our template targets | https://github.com/anthropics/claude-code |
| **langchain-ai/deepagents** | Open-source agent harness + CLI — any LLM, LangGraph-based, skills/memory/sub-agents | https://github.com/langchain-ai/deepagents |
| **agentsmd/agents.md** | AGENTS.md standard — universal instruction file for AI coding agents | https://github.com/agentsmd/agents.md |
| **anthropics/ecc (everything-claude-code)** | 130+ skills collection — reference for skill patterns | https://github.com/anthropics/ecc |

---

## Sequence

```
Part 1 (Superpowers) → Part 2 (Knowledge) → Part 3 & 4 (parallel) → Part 5 (Multi-Agent)
```

Each part gets its own brainstorm → spec → plan → implement cycle.
