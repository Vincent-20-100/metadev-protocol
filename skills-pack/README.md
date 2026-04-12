# Meta Protocol — Skills Pack

Standalone skills from the [metadev-protocol](https://github.com/Vincent-20-100/metadev-protocol) template. Use these without generating a full project.

## Installation

Copy the skills you want into your project's `.claude/skills/` directory:

```bash
# All skills
cp -r skills-pack/skills/* .claude/skills/

# Just the debate skill
cp -r skills-pack/skills/debate .claude/skills/

# Just the dev workflow skills
cp -r skills-pack/skills/brainstorm .claude/skills/
cp -r skills-pack/skills/plan .claude/skills/
```

## Available skills

| Skill | Description |
|-------|-------------|
| `/brainstorm` | Structured exploration before coding — one question at a time, 2–3 alternatives per decision |
| `/spec` | MoSCoW requirements formalization with acceptance criteria and verification checklist |
| `/debate` | Multi-agent adversarial debate — 3 agents (2 insiders + 1 lone wolf), 6 domain presets, debate record |
| `/plan` | Task decomposition with file mapping and tiered confidence gates (GREEN/AMBER/RED) |
| `/orchestrate` | Multi-step session orchestrator with dependency tracking across phases |
| `/test` | Run pytest and report results |
| `/lint` | Run ruff check + format on the whole project |
| `/save-progress` | Pre-commit checklist and context update (PILOT.md + SESSION-CONTEXT.md) |

## Recommended companion

These skills work best with the [Superpowers plugin](https://github.com/obra/superpowers) for advanced workflows (TDD, systematic debugging, code review).

## Full template

For a complete project setup with `.meta/` cockpit, CLAUDE.md contract, pre-commit hooks, and all skills pre-configured:

```bash
copier copy gh:Vincent-20-100/metadev-protocol my-new-project
```
