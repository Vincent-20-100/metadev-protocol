---
type: brainstorm
date: 2026-04-13
slug: research-skill
status: archived
---

# Brainstorm — `/research` skill (PM.1b)

**Parent:** `archive/brainstorm-2026-04-12-claude-ai-project-starter.md` §4.2 C3
**Outcome:** plan-2026-04-13-research-skill.md — full-auto ready
**Status:** decisions locked, plan produced, archived.

---

## 1. Problem

Our `/brainstorm` is **internal ideation** — "one question at a time" to cut scope creep before coding. Guillaume Desforges's `claude-ai-project-starter` has a complementary `/research` that covers **external knowledge gathering** (user discovery, competitive landscape, sector research, library docs). That layer is missing from metadev-protocol.

**Gap:** today, when the user needs external research (e.g., "what are the state-of-the-art patterns for X?"), the LLM either improvises from training data (risk: stale) or the user runs ad-hoc web searches outside any structured artifact. No trace lands in `.meta/references/raw/`.

---

## 2. Decisions

| # | Decision | Chosen | Rejected alternatives |
|---|---|---|---|
| D1 | **Scope** | External research only (web + repo docs + MCP docs) | Mixed internal+external structuration (risk: overlap with C1 vision); wrapper around `/audit-repo` (risk: coupling, unusable before PM.6 ships) |
| D2 | **Output location** | `.meta/references/raw/session-YYYY-MM-DD-research-<slug>.md` | Interim/ direct — would skip the raw → interim → synthesis lifecycle we already have |
| D3 | **Tools used** | WebSearch + WebFetch (Claude Code native) + MCP servers when present (e.g., context7 for library docs) | GitHub API (belongs to `/audit-repo` and `tech_watch.py` — clean separation) |
| D4 | **Relationship to `/brainstorm`** | Strict orthogonality — `/research` gathers facts, `/brainstorm` makes decisions. Can be chained: `/research → /brainstorm → /plan` | Merged skill (would destroy the single-responsibility clarity) |
| D5 | **Output schema** | Standardized: question / sources consulted / findings / open questions / next step | Free-form prose (would defeat future synthesis) |
| D6 | **Invocation** | Manual only in v1 (`/research <query>`) | Auto-proposed via trigger table — defer to post-dogfood |

---

## 3. Reference sources for implementation

- **Guillaume Desforges `/research` command** — prose baseline, covers user discovery + competitive + sector angles
- **Panniantong/Agent-Reach** (https://github.com/Panniantong/Agent-Reach) — user flagged as a super-research reference. Audit for: web-research loop patterns, source-consolidation strategies, relevance-ranking heuristics, output format choices. **Action:** audit this repo with `/audit-repo` (PM.6) once that ships, or manually before implementing PM.1b if PM.6 lands later

Both sources will be credited in `CREDITS.md` when the skill ships.

---

## 4. Open questions (punted to plan phase)

- **Source diversity heuristic** — should the skill enforce minimum 3 sources? Defer: let the skill recommend, not enforce
- **Citation format** — inline `[1]` footnotes or per-section bullets? Defer: plan decides based on what reads best in the raw/ output
- **Time-boxing** — should the skill set a soft budget (e.g., "max 8 WebFetch calls")? Plan decides based on token cost considerations

---

## 5. Out of scope

- **Auto-digest** raw → interim promotion — separate future skill (`/digest` mentioned in ADR 005)
- **Multi-language search** — rely on user query language; no automatic translation
- **Academic paper search** — WebSearch covers this loosely; no dedicated arxiv API in v1
- **Credential-gated sources** (private databases, paywalls) — out of scope permanently

---

## 6. Next step

Execute `plan-2026-04-13-research-skill.md`.
