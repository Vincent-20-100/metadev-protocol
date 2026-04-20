---
enforcement: hard-block
hooks: [H007, H021, H022]
---

> **Enforcement:** hard-block — `scripts/check_skills_contract.py` fails pre-commit if the contract is broken.

# Skills & agents contract

## The invariant

Every entry in the `CLAUDE.md` skills/agents trigger table MUST have a matching file on disk, and vice versa:

- A skill `foo` listed in the trigger table → `.claude/skills/foo/SKILL.md` must exist.
- An agent `bar` listed in the trigger table → `.claude/agents/bar.md` must exist.
- A skill/agent file on disk with no entry in the trigger table → must be removed or added.

The hook `H007` / `H021` / `H022` (`scripts/check_skills_contract.py`) enforces both directions.

## Workflow

### Adding a skill or agent

1. Create the file: `.claude/skills/<name>/SKILL.md` (skill) or `.claude/agents/<name>.md` (agent).
2. Add an entry to the `CLAUDE.md` trigger table with:
   - Tool name
   - Type (skill / agent)
   - Trigger (observable signal)
   - Action (Auto / Propose)
3. Commit both files together.

### Removing a skill or agent

1. Delete the trigger-table entry **first**.
2. Then delete the file.
3. Commit both changes together.

Order matters: if you delete the file first, the contract check will fail on a stale trigger-table reference.

### Renaming

Treat as a remove + add. Two atomic commits is fine; a single commit is also fine as long as the contract passes.

## Common failure modes

- **Silent skill** — file exists, no trigger-table entry. The LLM won't discover it. Fix: add the entry.
- **Phantom trigger** — trigger-table entry, no file. The LLM suggests using it, fails on invocation. Fix: create the file or remove the entry.
- **Typo in name** — `brainstorming` vs `brainstorm`. The hook compares exact strings. Fix: align both.

## Related

- `CLAUDE.md` trigger-table is the source of truth for the LLM's routing decisions.
- See `.claude/skills/<name>/SKILL.md` format conventions in existing skills.
