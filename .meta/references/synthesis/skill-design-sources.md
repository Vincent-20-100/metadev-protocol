# Skill design — Sources and inspirations

References that informed the design of our skills and agent system.

---

## Multi-agent debate architecture

- **MAD paper (Multi-Agents Debate)** — arxiv.org/abs/2305.14325
  3-role architecture: Devil/Angel/Judge. Foundational academic work.
  → Inspired our 3-agent structure in /debate

- **Debate Workflow** (hongbietcode) — mcpmarket.com/tools/skills/debate-workflow
  3-phase workflow: parallel arguments → cross-critique → synthesis.
  → Inspired our Phase 1/2/3 structure

- **adversarial-spec** (zscole) — github.com/zscole/adversarial-spec
  Multi-model debate with checkpointing, session management, cost tracking.
  → Inspired future queue mode and session persistence

- **claude-devils-advocate** (richiethomas) — github.com/richiethomas/claude-devils-advocate
  Forced disagreement rules, prioritized topic sequence, transcript output.
  → Inspired our anti-rationalization approach

- **Math Olympiad skill** (Claude Code plugin) — pattern-armed adversarial verification
  Context isolation, asymmetric voting, 7 attack patterns.
  → Inspired our context isolation in Phase 1 and attack taxonomies

## Anti-consensus / objectivity

- **Rodin agent** (bdebon) — gist.github.com/bdebon/e22d0b728abc5f393227440907b334cf
  Anti-complaisance rules, systematic steelmanning, affirmation classification.
  → To integrate: steelmanning in cross-critique, classification system,
  "if you validated 3 positions in a row, something is wrong" rule

- **BMAD adversarial review** — github.com/bmad-code-org/BMAD-METHOD
  Information asymmetry principle, severity classification, forced findings.
  → Inspired severity-based filtering in agent personas

## Engineering discipline

- **agent-skills** (Addy Osmani / Google) — github.com/addyosmani/agent-skills
  19 skills + 7 slash commands encoding Google engineering culture.
  Anti-rationalization tables, verification evidence, agent personas.
  → Inspired: verification checklists, rationalizations tables, /spec skill,
  AGENTS.md personas (code-reviewer, test-engineer, security-auditor)

## Orchestration patterns

- **Superpowers plugin** (obra) — github.com/obra/superpowers
  Subagent-driven development, brainstorming dialogue, plan execution.
  → Our skills delegate to superpowers when available

- **gstack skill pack** (garrytan) — 23-agent sprint workflow
  → Referenced in .meta/references/gstack-skill-pack.md

- **dmux workflows** (everything-claude-code) — parallel multi-agent orchestration
  → Pattern reference for future /orchestrate parallel execution
