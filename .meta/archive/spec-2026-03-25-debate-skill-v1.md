# /debate skill — V1 spec

**Date:** 2026-04-06
**Status:** SPEC — ready to implement

---

## V1 scope

- 3-agent structured debate with orchestrator
- 3 phases: P1 arguments (parallel) → P2 cross-critique (parallel) → P3 synthesis
- Deep mode: P2b feedback loop on divergence
- 6 domain presets with specialized attack taxonomies
- Debate Record output to `.meta/debates/`
- Single debate execution (no queue mode in V1)

## V2+ vision (NOT in scope)

- Queue mode (`/debate-queue`) — batch debates in background
- Workflow integration: debate as brainstorm replacement in autonomous dev loops
- Decision forks: continue both options when decision is hard, choose a posteriori
- Full spec/plan generation from debate output
- Cross-model debates (different LLMs as different agents)

## Deployment

- V1: skill in the metadev-protocol template (`template/.claude/skills/debate/`)
- Future: extract as standalone plugin for broader distribution
