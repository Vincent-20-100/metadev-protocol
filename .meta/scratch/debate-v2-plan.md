# Plan — /debate v2 (hybrid context + lone wolf)

**Date:** 2026-04-07
**Status:** PLAN — ready to implement
**Depends on:** debate SKILL.md (current v2)

---

## Changes to implement

### 1. Usage section
- Remove `--with-context` flag
- Add `--wolf-context` (gives lone wolf full project context)
- Add `--all-fresh` (all 3 agents get pitch only)
- Add `--quality` (all agents use sonnet instead of haiku)
- Update usage examples

### 2. Hard rules section
- Replace current fresh-by-default with hybrid context model:
  - Agents A, B = insiders (full project context)
  - Agent C = lone wolf (pitch only: one-liner projet + subject)
- Document the 3 flags

### 3. Phase 0 — Setup
- Replace "Context modes" section with new hybrid model
- Announce format shows: `Context: hybrid (2 insiders + 1 lone wolf)`
- Orchestrator reads PILOT.md first line as "project pitch" for the wolf
- Orchestrator chooses models: haiku for insiders, sonnet for wolf (default)
  Can adapt based on subject complexity — guidance, not hardcode

### 4. Phase 1 — Agent prompt templates
- Insider template: includes CLAUDE.md rules, GUIDELINES.md, PILOT.md
- Lone wolf template: includes ONLY project pitch (one-liner) + subject + persona + attack taxonomy
- Add `{IF --all-fresh}` / `{IF --wolf-context}` conditionals

### 5. Phase 2 — Cross-critique
- No structural change — all agents see each other's arguments
- The wolf may get recadré by insiders ("irrelevant to our context because...")
- The wolf may challenge insiders ("that's your project bias talking")

### 6. Phase 3 — Relevance check
- Simplify: the relevance check now applies primarily to wolf's arguments
- Remove the ">50% irrelevant → suggest --with-context" warning (replaced by hybrid)
- Keep recontextualization logic for wolf's arguments only

### 7. Debate Record format
- Change `Context: fresh|project-aware` to `Context: hybrid|all-fresh|all-context`
- Add "Lone wolf insights" section — arguments from the wolf that survived cross-critique get highlighted (these are the high-value outsider perspectives)

### 8. Rationalizations table
- Update "Fresh agents won't understand" → "The lone wolf has the project pitch, enough to be relevant"
- Update "Let me give agents a little context" → now handled by design (insiders have it, wolf has pitch)
- Remove "Either full fresh or explicit --with-context. No middle ground." (obsolete)

### 9. Implementation notes
- Model guidance: haiku insiders, sonnet wolf (default, orchestrator adapts)
- `--quality` flag: all sonnet
- Sync skills-pack/skills/debate/SKILL.md after edit

### 10. Presets — persona assignment
- Document which persona is the natural lone wolf for each preset:
  - `default`: Pragmatist
  - `architecture`: End-user
  - `strategy`: Outsider
  - `data`: Business
  - `academic`: Reviewer
  - `security`: Attacker
- The 3rd persona in each preset list = the wolf

---

### 11. Rodin patterns (from gist.github.com/bdebon)
- Add to Phase 2 cross-critique instructions:
  - **Steelmanning obligatoire**: before critiquing an argument, reformulate it
    in its strongest form. No strawman attacks allowed.
  - **Anti-complaisance rule**: if an agent concedes 3+ arguments in a row
    without contesting anything, force it to find what's missing or wrong.
- Add to Debate Record format:
  - **Affirmation classification** for each argument:
    ✓ correct | ~ contestable but defensible | ⚡ over-simplified |
    ◐ blind spot | ✗ factually false or logically incoherent

---

## Files to edit
- `template/.claude/skills/debate/SKILL.md` — all changes above
- `skills-pack/skills/debate/SKILL.md` — sync copy

## Test
- Generate template with copier, verify SKILL.md content
- No code to test — this is a prompt/protocol skill

## Sources
- See `.meta/references/skill-design-sources.md` for full reference list
