<p align="center">
  <img src="docs/banner.svg" alt="metadev-protocol banner" width="900">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python 3.13+"></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-package%20manager-blueviolet" alt="uv"></a>
  <a href="https://copier.readthedocs.io"><img src="https://img.shields.io/badge/Copier-template%20engine-green" alt="Copier"></a>
  <a href="https://claude.ai/code"><img src="https://img.shields.io/badge/Claude%20Code-AI%20assistant-orange" alt="Claude Code"></a>
</p>

# metadev-protocol

> **Premium vibe-coding set-up in one command.**
> Automatisms, skills, agents, secrets scanning, session memory — so the AI follows the structure, not your prompts.

```bash
copier copy gh:Vincent-20-100/metadev-protocol my-project --trust
cd my-project && claude
```

---

## The Problem

Every AI-assisted project starts the same way, and hits the same walls:

- **You already lost that context.** Each session starts from scratch. You re-explain the architecture, the decisions, the current state. Every. Single. Time.
- **Your codebase is a mess.** Drafts, scratch files, brainstorm notes pile up next to production code. The AI can't tell what ships and what doesn't.
- **Your best prompts stay behind.** You build great workflows and guidelines for one project — then start from zero on the next one.
- **Your rules stopped working.** You wrote instructions in CLAUDE.md. The AI followed them for a while, then drifted. No enforcement, no hooks, just hope.
- **You spend more time supervising than building.** The AI creates files anywhere, skips tests, forgets to update docs. You're prompting the same things over and over instead of coding.

---

## The Solution

**metadev-protocol** generates a **fully wired Python project** where the AI follows the workflow without being told — because the rules are encoded in the structure, not in your prompts.

The core principle: **separate what ships from how you build it.**

### One repo, two spaces

Everyone wants durable AI memory and reusable skills. **metadev-protocol** gives your project a second space — co-located with your code, versioned with it, but never confused with it.

<p align="center">
  <img src="docs/diagrams/01-two-spaces.svg" alt="One repo, two spaces — product vs cockpit" width="900">
</p>

> **one repo, two spaces — the product ships, the cockpit thinks**

### The loop you know vs. the loop you want

<p align="center">
  <img src="docs/diagrams/02-before-after.svg" alt="Raw Claude Code loop vs metadev-protocol loop" width="900">
</p>

### How it works — the rails your prompt rides

One prompt enters, but it doesn't go straight to the model. It passes through four enforced stages before any file is touched — and session memory closes the loop.

<p align="center">
  <img src="docs/diagrams/03-rails.svg" alt="The rails: REMEMBER, PLAN, GUARD, SHIP" width="900">
</p>

Drafts are gitignored. Validated artifacts (`active/`) and history (`archive/`) are committed. Context is preserved — every session picks up where the last one ended.

---

## What You Get

- **11 automatisms** — context loading at session start, mandatory plan before any edit, architecture sync, session handoff, Rule of 3 anti-consensus challenge. Hard-wired in `CLAUDE.md`, they fire without prompting.
- **9 rules** — the non-negotiable contract between you and the AI. Few hard rules that are always followed beat many soft rules that are sometimes ignored.
- **10 skills** — `/brainstorm`, `/spec`, `/debate`, `/plan`, `/orchestrate`, `/research`, `/vision`, `/tech-watch`, `/test`, `/save-progress`. Reusable across every project you generate.
- **6 agent personas** — code-reviewer, test-engineer, security-auditor, data-analyst, devil's-advocate, librarian. Invoked on demand via the `Task` tool.
- **Multi-LLM day one** — Claude Code is the source of truth. `AGENTS.md` (Codex) and `GEMINI.md` (Gemini CLI) are auto-regenerated @import stubs pointing at `CLAUDE.md`. Tier 2 (Cursor, Windsurf, Cline) is a one-line edit in `sync-config.yaml`.
- **Deterministic harness audit** — `evals/harness_audit.py` scores the repo on 6 categories (Skills, Agents, Hosts, Contract, Taxonomy, Safety, 60 pts max). Invariant: a well-formed generated project scores 60/60.
- **Hooks over instructions** — every Python file is auto-linted on save (ruff PostToolUse hook), dangerous operations are blocked or require confirmation, co-authored-by trailers suppressed natively.
- **Session continuity** — `PILOT.md` (project dashboard) + `SESSION-CONTEXT.md` (living context rewritten each session). Claude remembers what you decided three weeks ago.
- **`.meta/` taxonomy** — `active/` · `archive/` · `drafts/` · `decisions/` · `references/`. Filename convention enforced by pre-commit hook.
- **Secret scanning** — 40+ regex patterns, local audit script, pre-commit hook, 2 GitHub Actions (push gate + publicization alert). [Details](docs/public-safety.md)
- **Two execution modes** — `safe` (default, asks before touching repo structure) or `full-auto` (unsupervised runs, safety-net deny only). [Details](docs/execution-modes.md)
- **Versioned updates** — `copier update` propagates template improvements to existing projects. Review the diff, resolve conflicts, done.

---

## The Toolkit

Every generated project ships with 10 skills, 6 agent personas, 4 guardrail scripts, and a harness audit scorecard. Skills and agents are invoked by name; scripts run as pre-commit hooks and CI steps.

### Skills — `/command` in Claude Code

| Skill | When to reach for it | What it does |
|-------|---------------------|--------------|
| `/brainstorm` | Idea is vague, scope fuzzy | One question at a time, 2–3 alternatives per decision, YAGNI pressure, artifact in `.meta/` |
| `/spec` | Feature needs formalization | MoSCoW requirements with acceptance criteria and verification checklist |
| `/debate` | Hard trade-off with 2+ defensible options | 3-agent adversarial debate (2 insiders + 1 lone wolf), 6 domain presets, debate record |
| `/plan` | Scope is clear, need task breakdown | Tasks mapped to files, tiered confidence gates (GREEN/AMBER/RED), verification checklist |
| `/orchestrate` | Multi-step objective across phases | Session orchestrator with dependency tracking and phase transitions |
| `/research` | Question needs external facts or recent state-of-the-art | WebSearch + WebFetch + MCP, 8-call soft budget, structured output to `.meta/references/raw/` |
| `/vision` | Vision section empty or product framing unclear | Guided 4-question dialogue → fills Problem / Target user / V1 scope / North star in PILOT.md |
| `/tech-watch` | Weekly veille or ad-hoc deep analysis of a specific repo | Sweep mode: fetches emerging repos/articles near your themes into `.meta/references/research/`. Deep mode: `/tech-watch <url>` produces a tiered structural audit of one repo |
| `/test` | After implementation | Runs `pytest` with optional arguments, reports failures |
| `/save-progress` | End of session | Pre-commit checklist (auto-extracted to `scripts/save_progress_preflight.py`), updates `PILOT.md`, rewrites `SESSION-CONTEXT.md` |

### Agent personas — invoked on demand via `Task` tool

| Agent | When it fires | What it does |
|-------|--------------|--------------|
| `code-reviewer` | ≥3 files touched or plan step completed | Reviews diff for bugs, style drift, convention breaks |
| `test-engineer` | New module, new public API, missing coverage | Designs test cases, asserts on edge cases, proposes fixtures |
| `security-auditor` | Auth, secrets, input validation, crypto, network boundaries | Threat-models the change, flags OWASP categories |
| `data-analyst` | Pipeline, ETL, metric computation, statistical claim | Validates methodology, challenges sampling, checks reproducibility |
| `devil's-advocate` | Auto-triggered by Rule of 3 (3 user agreements without friction) | Adversarial challenge to surface blind spots |
| `librarian` | Conversation needs facts from `.meta/references/`, `docs/`, or deep in `src/` | Cherry-picks extracts with `file:line` citations and confidence; read-only |

### Guardrail scripts — pre-commit + CI

| Script | Trigger | What it blocks |
|--------|---------|----------------|
| `audit_public_safety.py` | pre-commit hook + 2 GitHub Actions | 40+ secret regex patterns, sensitive files (`.env`, `id_rsa`, etc.), `.gitignore` coverage gaps |
| `check_git_author.py` | pre-commit hook | Commits authored as `Claude` / `Anthropic` / co-authored-by trailers |
| `check_meta_naming.py` | pre-commit hook | `.meta/active/` and `.meta/archive/` files that violate the `<type>-<YYYY-MM-DD>-<slug>.md` convention |
| `check_skills_contract.py` | pre-commit hook | Trigger-table rows that don't map to real skill or agent files on disk |
| `sync_hosts.py` | pre-commit hook + CI workflow | Drift between `CLAUDE.md` / `.claude/` and the auto-generated `AGENTS.md` / `GEMINI.md` stubs |
| `evals/harness_audit.py` | manual + CI | 6-category scorecard (60 pts). Invariant: generated project = 60/60 |

### Just the skills, no template

Want the skills in an existing project without regenerating? The [`skills-pack/`](skills-pack/) directory ships all 10 skills as drop-ins:

```bash
git clone https://github.com/Vincent-20-100/metadev-protocol.git
cp -r metadev-protocol/skills-pack/skills/* your-project/.claude/skills/
```

No `.meta/` taxonomy, no hooks, no CLAUDE.md contract — just the skills.

---

## Generated Structure

```
my-project/
├── CLAUDE.md                       # Session contract (source of truth)
├── AGENTS.md                       # Auto-generated Codex stub → CLAUDE.md
├── GEMINI.md                       # Auto-generated Gemini stub → CLAUDE.md
├── sync-config.yaml                # Host registry (tier 1 active, tier 2 commented)
├── pyproject.toml                  # uv, ruff, pytest
├── .pre-commit-config.yaml         # Lint + hooks + secret scan + sync-hosts check
│
├── src/my_project/                 # Package source
├── tests/                          # Test suite
├── scripts/
│   ├── check_meta_naming.py        # .meta/ filename convention
│   ├── check_git_author.py         # Block AI authorship
│   ├── audit_public_safety.py      # Secret + sensitive file scanner
│   └── sync_hosts.py               # Regenerate AGENTS.md / GEMINI.md stubs
├── evals/
│   └── harness_audit.py            # Deterministic 6-category scorecard
├── data/                           # raw/ → interim/ → processed/
│
├── .github/workflows/
│   ├── public-safety.yml           # Audit on push/PR to main
│   ├── public-alert.yml            # Alert on repo publicization
│   └── sync-hosts.yml              # Fail on stub drift
│
├── .claude/
│   ├── settings.json               # Permissions, hooks, security
│   ├── skills/                     # 10 built-in skills
│   └── agents/                     # 6 agent personas (incl. librarian)
│
└── .meta/
    ├── PILOT.md                    # Project dashboard (AI reads first)
    ├── SESSION-CONTEXT.md          # Living context (rewritten each session)
    ├── GUIDELINES.md               # Best practices (advisory)
    ├── active/                     # Validated plans/specs in flight
    ├── archive/                    # Implemented artifacts
    ├── drafts/                     # WIP (gitignored)
    ├── decisions/                  # Architecture Decision Records
    └── references/                 # raw/ → interim/ → synthesis/
```

---

## How It Works

### Law and Mentor

| File | Authority | Role |
|------|-----------|------|
| `CLAUDE.md` | **Law** | 11 automatisms + 9 rules. Non-negotiable. |
| `GUIDELINES.md` | **Mentor** | Best practices, anti-patterns, ADR templates. Proposed, not imposed. |

### Session lifecycle

Each session follows the same enforced sequence: read context → propose plan → get approval → implement (auto-lint on every edit) → test → conventional commit → rewrite context for the next session. If scope is unclear, the AI reaches for `/brainstorm → /spec → /debate` before writing any code.

This isn't a suggestion — it's what the 11 automatisms enforce. The AI does this because the structure tells it to, not because you asked.

---

## Quick Start

```bash
# 1. Install prerequisites
curl -LsSf https://astral.sh/uv/install.sh | sh        # macOS/Linux
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
uv tool install copier

# 2. Generate your project
copier copy gh:Vincent-20-100/metadev-protocol my-project --trust

# 3. Start building
cd my-project && claude
```

> [!NOTE]
> Requires [uv](https://github.com/astral-sh/uv), [copier](https://copier.readthedocs.io), and a [Claude Code](https://claude.ai/code) subscription.

### Update an existing project

```bash
copier update --trust
```

Template improvements are propagated via semver tags. Review the diff, resolve conflicts, done.

---

## Stack

| Tool | Role |
|------|------|
| [Python 3.13+](https://www.python.org) | Language |
| [uv](https://github.com/astral-sh/uv) | Package manager + venv |
| [ruff](https://github.com/astral-sh/ruff) | Lint + format |
| [copier](https://copier.readthedocs.io) | Template generation + updates |
| [pre-commit](https://pre-commit.com/) | Git hooks |
| [Claude Code](https://claude.ai/code) | AI assistant |

---

## Contributing

This repo applies the method to build the method.

```bash
git clone https://github.com/Vincent-20-100/metadev-protocol.git
cd metadev-protocol && uv sync
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow, [CREDITS.md](CREDITS.md) for inspirations, [CHANGELOG.md](CHANGELOG.md) for version history.

## License

[MIT](LICENSE)
