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

metadev-protocol generates a **fully wired Python project** where the AI follows the workflow without being told — because the rules are encoded in the structure, not in your prompts.

The core principle: **separate what ships from how you build it.**

### The loop you know vs. the loop you want

```mermaid
flowchart LR
    classDef pain  fill:#3a2230,stroke:#f38ba8,stroke-width:2px,color:#f2cdcd
    classDef cure  fill:#1e3a2e,stroke:#a6e3a1,stroke-width:2px,color:#d9f7d0
    classDef jump  fill:#2d2a52,stroke:#cba6f7,stroke-width:2px,color:#e0c8ff

    subgraph BEFORE["❌ Raw Claude Code"]
        direction TB
        B1["Re-explain the project"]:::pain
        B2["AI invents a new file layout"]:::pain
        B3["Drafts pile up at repo root"]:::pain
        B4["Tomorrow: start from zero"]:::pain
        B1 --> B2 --> B3 --> B4 --> B1
    end

    subgraph AFTER["✅ metadev-protocol"]
        direction TB
        A1["AI reads where you stopped"]:::cure
        A2["Plans before touching code"]:::cure
        A3["Drafts auto-quarantined"]:::cure
        A4["Session saved for tomorrow"]:::cure
        A1 --> A2 --> A3 --> A4 --> A1
    end

    JUMP["copier copy"]:::jump
    BEFORE ==> JUMP ==> AFTER

    style BEFORE fill:#1e2a52,stroke:#f38ba8,stroke-width:2px,color:#f2cdcd
    style AFTER  fill:#1e2a52,stroke:#a6e3a1,stroke-width:2px,color:#d9f7d0
```

### How it works — the rails your prompt rides

One prompt enters, but it doesn't go straight to the model. It passes through four enforced stages before any file is touched — and session memory closes the loop.

```mermaid
flowchart LR
    classDef io    fill:#a6e3a1,stroke:#40a02b,stroke-width:3px,color:#1e1e2e
    classDef stage fill:#89dceb,stroke:#74c7ec,stroke-width:2px,color:#1e2a52
    classDef out   fill:#f5c2e7,stroke:#ea76cb,stroke-width:3px,color:#1e1e2e

    PROMPT(["one prompt"]):::io

    subgraph RAILS["the rails"]
        direction LR
        REMEMBER["<b>REMEMBER</b><br/>PILOT.md · SESSION-CONTEXT<br/>active plans · decisions"]:::stage
        PLAN["<b>PLAN</b><br/>/brainstorm /spec /plan<br/>/debate /orchestrate"]:::stage
        GUARD["<b>GUARD</b><br/>11 automatisms · 9 rules<br/>reviewer · security · devil"]:::stage
        SHIP["<b>SHIP</b><br/>hooks: lint · secrets · tests<br/>/save-progress"]:::stage
        REMEMBER ==> PLAN ==> GUARD ==> SHIP
    end

    CODE(["shipped code<br/>+ updated memory"]):::out

    PROMPT ==> REMEMBER
    SHIP ==> CODE
    CODE -.->|"next session"| REMEMBER

    style RAILS fill:#1e2a52,stroke:#cba6f7,stroke-width:2px,color:#cdd6f4
```

Drafts are gitignored. Validated artifacts (`active/`) and history (`archive/`) are committed. Context is preserved — every session picks up where the last one ended.

---

## What You Get

- **11 automatisms** — context loading at session start, mandatory plan before any edit, architecture sync, session handoff, Rule of 3 anti-consensus challenge. Hard-wired in `CLAUDE.md`, they fire without prompting.
- **9 rules** — the non-negotiable contract between you and the AI. Few hard rules that are always followed beat many soft rules that are sometimes ignored.
- **8 skills** — `/brainstorm`, `/spec`, `/debate`, `/plan`, `/orchestrate`, `/test`, `/lint`, `/save-progress`. Reusable across every project you generate.
- **5 agent personas** — code-reviewer, test-engineer, security-auditor, data-analyst, devil's-advocate. Defined in `AGENTS.md`, invoked on demand.
- **Hooks over instructions** — every Python file is auto-linted on save (ruff PostToolUse hook), dangerous operations are blocked or require confirmation, co-authored-by trailers suppressed natively.
- **Session continuity** — `PILOT.md` (project dashboard) + `SESSION-CONTEXT.md` (living context rewritten each session). Claude remembers what you decided three weeks ago.
- **`.meta/` taxonomy** — `active/` · `archive/` · `drafts/` · `decisions/` · `references/`. Filename convention enforced by pre-commit hook.
- **Secret scanning** — 40+ regex patterns, local audit script, pre-commit hook, 2 GitHub Actions (push gate + publicization alert). [Details](docs/public-safety.md)
- **Two execution modes** — `safe` (default, asks before touching repo structure) or `full-auto` (unsupervised runs, safety-net deny only). [Details](docs/execution-modes.md)
- **Versioned updates** — `copier update` propagates template improvements to existing projects. Review the diff, resolve conflicts, done.

---

## Generated Structure

```
my-project/
├── CLAUDE.md                       # Session contract (11 automatisms + 9 rules)
├── AGENTS.md                       # Agent personas (5 specialists)
├── pyproject.toml                  # uv, ruff, pytest
├── .pre-commit-config.yaml         # Lint + hooks + secret scan
│
├── src/my_project/                 # Package source
├── tests/                          # Test suite
├── scripts/
│   ├── check_meta_naming.py        # .meta/ filename convention
│   ├── check_git_author.py         # Block AI authorship
│   └── audit_public_safety.py      # Secret + sensitive file scanner
├── data/                           # raw/ → interim/ → processed/
│
├── .github/workflows/
│   ├── public-safety.yml           # Audit on push/PR to main
│   └── public-alert.yml            # Alert on repo publicization
│
├── .claude/
│   ├── settings.json               # Permissions, hooks, security
│   └── skills/                     # 8 built-in skills
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
