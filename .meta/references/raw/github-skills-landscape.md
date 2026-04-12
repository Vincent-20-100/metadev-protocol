# GitHub Skills Landscape — April 2026

> Full research on repos providing skills, configurations, and workflow patterns
> for Claude Code and comparable AI coding assistants.

---

## Tier 1 — Mega Repos (10k+ stars)

### 1. obra/superpowers — 130,749 stars
- **URL**: https://github.com/obra/superpowers
- **What**: Agentic skills framework & software development methodology. THE reference in the Claude Code ecosystem.
- **Creator**: Jesse Vincent (created Request Tracker, Perl 5 pumpking, Keyboardio co-founder)
- **Skills provided**:
  - `brainstorming` — Refines rough ideas through questions, explores alternatives, saves design doc
  - `using-git-worktrees` — Creates isolated workspace on new branch, verifies clean test baseline
  - `writing-plans` — Breaks work into bite-sized tasks (2-5 min each) with exact file paths, code, verification steps
  - `subagent-driven-development` / `executing-plans` — Orchestrates subagents through plan tasks
  - `test-driven-development` — Strict TDD: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
  - `systematic-debugging` — Structured bug investigation
  - `using-superpowers` — Meta-skill categorizing rigid vs flexible skills
  - `writing-skills` — Meta-skill for creating new skills
- **Architecture**: Linear pipeline: Brainstorming -> Spec -> Plan -> Subagent Dev -> TDD -> Code Review
- **Key principles**: TDD, YAGNI, DRY, frequent commits
- **Skill format**: Standard SKILL.md with YAML frontmatter
- **Platform**: Agnostic (Claude Code, Cursor, Codex CLI, OpenCode, Gemini CLI, Qwen Code, Goose CLI, Auggie)
- **Clever insight**: Skills are categorized as "Rigid" (TDD, debugging — follow exactly) vs "Flexible" (patterns — adapt to context)

**Related repos**:
- `obra/superpowers-marketplace` (781 stars) — Curated plugin marketplace
- `obra/superpowers-skills` (594 stars, archived) — Community-editable skills
- `obra/superpowers-lab` (265 stars) — Experimental skills
- `obra/superpowers-chrome` (230 stars) — Direct Chrome browser control via DevTools Protocol
- `obra/superpowers-developing-for-claude-code` (115 stars) — Dev tooling for Claude Code itself

### 2. affaan-m/everything-claude-code — 131,763 stars
- **URL**: https://github.com/affaan-m/everything-claude-code
- **What**: Agent harness performance optimization system. Skills, instincts, memory, security, and research-first development.
- **Origin**: Built at Claude Code Hackathon (Cerebral Valley x Anthropic, Feb 2026)
- **Scale**: 36 agents, 147 skills, 68 legacy command shims
- **Skills provided** (notable ones):
  - `/aside` — Answer side question without losing current task context
  - `/build-fix` — Incrementally fix build/type errors with minimal changes
  - `/code-review` — Review for local changes or GitHub PRs
  - `/learn` — Analyze session and extract patterns worth saving as skills
  - `/loop-start` / `/loop-status` — Managed autonomous loop pattern
  - `/model-select` — Recommend best model tier by complexity/budget
  - `/harness-audit` — Deterministic repo harness audit with prioritized scorecard
  - Language-specific: `go-tdd`, `go-review`, `go-build-fix`, `cpp-review`, `cpp-build-fix`, `kotlin-build-fix`, `rust-agent-handoff`
  - Multi-model: `multi-plan`, `multi-execute`, `multi-frontend` (Gemini-led), `multi-backend` (Codex-led)
- **Architecture**: GAN-inspired Generator-Evaluator agent harness
- **Multi-platform**: Skills in `.claude/skills/`, `.cursor/skills/`, `.agents/skills/`, `.codex/`
- **Clever insight**: `/learn` skill that auto-extracts reusable patterns from sessions; instinct-based learning with confidence scoring

### 3. anthropics/skills — 108,625 stars
- **URL**: https://github.com/anthropics/skills
- **What**: Official Anthropic agent skills repository. THE reference implementation for SKILL.md format.
- **Skills provided**:
  - **Document skills** (source-available): `xlsx`, `docx`, `pptx`, `pdf`
  - **Example skills** (Apache 2.0): `algorithmic-art`, `brand-guidelines`, `skill-creator` (meta-skill)
  - Additional: MCP server generation, web testing, internal communications, Slack GIFs, theme styling
- **Skill format** (canonical):
  ```
  skill-name/
  ├── SKILL.md           # Required: YAML frontmatter + markdown body
  │   ├── frontmatter    # name (64 chars max), description (1024 chars max)
  │   └── body           # Keep under 500 lines
  └── Optional resources/
      ├── scripts/       # Executable code for deterministic tasks
      ├── references/    # Docs loaded into context as needed
      └── assets/        # Templates, icons, fonts
  ```
- **Frontmatter fields**: `name` (required), `description` (required), `disable-model-invocation` (optional), `allowed-tools` (optional)
- **Discovery**: Progressive disclosure — name+description in system prompt; full SKILL.md loaded on demand
- **Scan locations**: `~/.config/claude/skills/`, `.claude/skills/`, plugin-provided, built-in
- **Clever insight**: The spec became an open standard (agentskills.io) adopted by OpenAI for Codex CLI and ChatGPT

### 4. thedotmack/claude-mem — 44,472 stars
- **URL**: https://github.com/thedotmack/claude-mem
- **What**: Plugin that captures everything Claude does, compresses with AI (agent-sdk), injects relevant context into future sessions.
- **Stack**: ChromaDB, SQLite, embeddings, RAG
- **Clever insight**: Automatic session capture + AI compression + contextual re-injection = persistent memory without manual management

### 5. PatrickJS/awesome-cursorrules — 38,836 stars
- **URL**: https://github.com/PatrickJS/awesome-cursorrules
- **What**: Curated collection of `.cursorrules` configuration files for Cursor AI editor.
- **Format**: `.cursorrules` files (plain text system prompts) placed at project root
- **Notable rules**:
  - Next.js + Vercel + TypeScript (App Router, Shadcn UI, Radix, Tailwind)
  - React + TypeScript + Shadcn UI
  - TypeScript + NestJS best practices
  - JS/TS Code Quality Pro
  - Angular, Astro, clean-code, database, fastapi, gitflow, rust, svelte, python
- **Newer format**: `.mdc` files (Cursor Rules v2)
- **Clever insight**: One file per stack/domain — simple, composable, shareable. The simplest possible skill format.

### 6. hesreallyhim/awesome-claude-code — 35,618 stars
- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **What**: Curated list of skills, hooks, slash-commands, agent orchestrators, applications, and plugins.
- **Value**: Discovery hub — the "awesome list" for the ecosystem. Good for finding what exists.

### 7. sickn33/antigravity-awesome-skills — 29,883 stars
- **URL**: https://github.com/sickn33/antigravity-awesome-skills
- **What**: Installable library of 1,340+ agentic skills with installer CLI, bundles, workflows.
- **Platform**: Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity
- **Clever insight**: Skills as an installable package with bundles — npm-style distribution for skills

### 8. OthmanAdi/planning-with-files — 17,843 stars
- **URL**: https://github.com/OthmanAdi/planning-with-files
- **What**: Manus-style persistent markdown planning skill.
- **Core concept**: "Context Window = RAM (volatile); Filesystem = Disk (persistent)"
- **Three files**:
  - `task_plan.md` — Track phases and progress
  - `findings.md` — Store research and findings
  - `progress.md` — Session log and test results
- **Key feature**: Automatic recovery after `/clear` — reads files back from disk
- **Clever insight**: The simplest possible "memory" — just write plans to files. Works across context resets. Non-negotiable: never start a complex task without task_plan.md.

### 9. anthropics/claude-plugins-official — 15,729 stars
- **URL**: https://github.com/anthropics/claude-plugins-official
- **What**: Official Anthropic-managed directory of high-quality Claude Code plugins.
- **Notable plugins**: pr-review-toolkit (6 parallel review agents), hookify (hooks from plain English), plugin-dev (skill extraction)

### 10. VoltAgent/awesome-agent-skills — 13,734 stars
- **URL**: https://github.com/VoltAgent/awesome-agent-skills
- **What**: 1000+ agent skills from official dev teams and community. Compatible with Codex, Antigravity, Gemini CLI, Cursor.

### 11. blader/humanizer — 12,012 stars
- **URL**: https://github.com/blader/humanizer
- **What**: Skill that removes signs of AI-generated writing from text.

### 12. travisvn/awesome-claude-skills — 10,339 stars
- **URL**: https://github.com/travisvn/awesome-claude-skills
- **What**: Curated list of Claude Skills, resources, and tools.

---

## Tier 2 — Significant Repos (1,000-10,000 stars)

### 13. Aider-AI/aider — 42,685 stars
- **URL**: https://github.com/Aider-AI/aider
- **What**: AI pair programming in terminal. Different paradigm from Claude Code but relevant patterns.
- **Convention system**:
  - `CONVENTIONS.md` file loaded via `--read` (read-only, cached)
  - `.aider.conf.yml` for persistent config (model, lint-cmd, test-cmd, auto-commits)
  - `.env` for environment variables (`AIDER_LINT_CMD`, `AIDER_TEST_CMD`)
  - Lint/test integration: auto-runs after each AI edit, feeds errors back
- **Clever insight**: Conventions as a read-only file (never edited by AI) that shapes all output. The `--lint-cmd` / `--test-cmd` feedback loop is elegant — AI edits, lint runs, errors fed back, AI fixes.

### 14. diet103/claude-code-infrastructure-showcase — 9,397 stars
- **URL**: https://github.com/diet103/claude-code-infrastructure-showcase
- **What**: Examples of Claude Code infrastructure with skill auto-activation, hooks, and agents.

### 15. alirezarezvani/claude-skills — 8,717 stars
- **URL**: https://github.com/alirezarezvani/claude-skills
- **What**: 220+ skills & agent plugins for engineering, marketing, product, compliance, C-level advisory.

### 16. Jeffallan/claude-skills — 7,553 stars
- **URL**: https://github.com/Jeffallan/claude-skills
- **What**: 66 specialized skills for full-stack developers.

### 17. Lum1104/Understand-Anything — 7,542 stars
- **URL**: https://github.com/Lum1104/Understand-Anything
- **What**: Turns any codebase into an interactive knowledge graph you can explore, search, and query.
- **Clever insight**: Codebase understanding as a navigable graph rather than flat text

### 18. refly-ai/refly — 7,162 stars
- **URL**: https://github.com/refly-ai/refly
- **What**: Open-source agent skills builder. Define skills by "vibe workflow". Build bots for Slack & Lark.
- **Clever insight**: "Skills are infrastructure, not prompts" — visual workflow builder for skills

### 19. grapeot/devin.cursorrules — 5,964 stars
- **URL**: https://github.com/grapeot/devin.cursorrules
- **What**: Magic to turn Cursor/Windsurf into 90% of Devin — agentic loop with planning.

### 20. UfoMiao/zcf — 5,842 stars
- **URL**: https://github.com/UfoMiao/zcf
- **What**: Zero-Config Code Flow for Claude Code & Codex. BMAD method implementation.

### 21. centminmod/my-claude-code-setup — 2,146 stars
- **URL**: https://github.com/centminmod/my-claude-code-setup
- **What**: Starter template configuration and CLAUDE.md memory bank system.

### 22. trailofbits/claude-code-config — 1,742 stars
- **URL**: https://github.com/trailofbits/claude-code-config
- **What**: Opinionated defaults from Trail of Bits for security research workflows.
- **Hooks**:
  - Block `rm -rf` (suggest `trash` instead)
  - Block direct push to main/master (require feature branches)
  - Audit logging for CLI tool mutations
  - Bash command log with timestamps
- **Skills** (via trailofbits/skills):
  - Security auditing, smart contract analysis, reverse engineering
  - Fuzz harness generation, vulnerability-class-specific analysis
  - Audit report writing in Trail of Bits house style
- **CLAUDE.md template**: Dev philosophy, code quality hard limits (function length, complexity), language-specific toolchains (Python/uv/ruff, Node/oxlint/vitest, Rust/clippy)
- **Clever insight**: They run in bypass-permissions mode with blocking hooks as guardrails. Hook design: prefer shell+jq over Python, fast-fail early, regex over AST.

### 23. jarrodwatts/claude-code-config — 1,008 stars
- **URL**: https://github.com/jarrodwatts/claude-code-config
- **What**: Personal Claude Code configuration — rules, hooks, agents, skills, and commands.

### 24. ntegrals/10x — 1,425 stars
- **URL**: https://github.com/ntegrals/10x
- **What**: Up to 20x faster AI coding with multi-step superpowers. Smart model routing, BYOK, self-hosted.

### 25. kinopeee/cursorrules — 1,124 stars
- **URL**: https://github.com/kinopeee/cursorrules
- **What**: Japanese-origin cursorrules collection.

### 26. wesammustafa/Claude-Code-Everything-You-Need-to-Know — 1,508 stars
- **URL**: https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know
- **What**: All-in-one guide covering setup, prompt engineering, commands, hooks, workflows, BMAD method.

---

## Tier 3 — Notable Under 1,000 stars (but high signal)

### 27. obra/superpowers-marketplace — 781 stars
- **URL**: https://github.com/obra/superpowers-marketplace

### 28. solatis/claude-config — 784 stars
- **URL**: https://github.com/solatis/claude-config
- **What**: Personal Claude Code customizations/config.

### 29. agent-sh/agentsys — 687 stars
- **URL**: https://github.com/agent-sh/agentsys
- **What**: 19 plugins, 47 agents, 40 skills for Claude Code, OpenCode, Codex, Cursor, Kiro.

### 30. s-smits/agentic-cursorrules — 648 stars
- **URL**: https://github.com/s-smits/agentic-cursorrules
- **What**: Multi-agent management in Cursor through strict file-tree partitioning and domain boundaries.

### 31. tw93/claude-health — 637 stars
- **URL**: https://github.com/tw93/claude-health
- **What**: Skill to audit your Claude Code config health across all layers.

### 32. josix/awesome-claude-md — 189 stars
- **URL**: https://github.com/josix/awesome-claude-md
- **What**: Curated collection of exemplary CLAUDE.md files with analyses and best practices.

### 33. ThaddaeusSandidge/BorisChernyClaudeMarkdown — 138 stars
- **URL**: https://github.com/ThaddaeusSandidge/BorisChernyClaudeMarkdown
- **What**: Template CLAUDE.md implementing Agentic Context Engineering (ACE).

---

## SKILL.md Format Reference (Canonical)

From anthropics/skills and official docs:

```yaml
---
name: my-skill-name           # Required. Max 64 chars. Lowercase + hyphens.
description: >                # Required. Max 1024 chars. Third person.
  Does X when Y happens.
  Triggers on Z conditions.
disable-model-invocation: true  # Optional. Manual-only if true.
allowed-tools: [Bash, Read]     # Optional. Restricts tool access.
---

# Skill Title

Instructions in markdown. Keep under 500 lines.

## When to Use
- Trigger condition 1
- Trigger condition 2

## Procedure
1. Step one
2. Step two

## Examples
- Example usage
```

**Scan locations** (in priority order):
1. `~/.config/claude/skills/` — User-global skills
2. `.claude/skills/` — Project-level skills
3. Plugin-provided skills
4. Built-in skills

**Progressive disclosure**: Only name+description loaded at startup. Full SKILL.md loaded on demand when relevant.

---

## Patterns Worth Adapting for metadev-protocol

### 1. Planning-with-Files Pattern (from OthmanAdi)
Externalize memory to filesystem. Three files: plan, findings, progress.
Could integrate into our `.meta/` structure naturally — we already have the cockpit concept.

### 2. Superpowers Pipeline (from obra)
Linear chain: Brainstorm -> Spec -> Plan -> Execute -> TDD -> Review.
Each skill's output is the next skill's input. Rigid vs Flexible categorization.

### 3. Trail of Bits Hook Patterns
Blocking hooks as guardrails (rm -rf prevention, main branch protection).
Audit logging of all bash commands. Shell+jq for performance.

### 4. Aider CONVENTIONS.md Pattern
Read-only conventions file that shapes all output. Never edited by AI.
Combined with lint-cmd/test-cmd feedback loop.

### 5. /learn Meta-Skill (from everything-claude-code)
Auto-extract reusable patterns from sessions and save as new skills.
Instinct-based learning with confidence scoring.

### 6. /aside Command (from everything-claude-code)
Answer a side question without losing current task context. Resume automatically.
Simple but extremely useful during deep work.

### 7. Config Health Audit (from tw93/claude-health)
Audit your own configuration for issues. Self-diagnostic skill.

### 8. Context Recovery on /clear (from planning-with-files)
When context fills up, skill automatically recovers previous session from disk files.
Critical for long tasks.

---

## Ecosystem Map

```
                    anthropics/skills (108k) ─── Official spec & reference skills
                           │
                    obra/superpowers (130k) ──── Methodology framework (TDD, planning)
                           │
              ┌────────────┼────────────────┐
              │            │                │
    everything-claude-   awesome-        antigravity-
    code (131k)         claude-code      awesome-skills
    [147 skills,        (35k)            (29k)
     36 agents]         [discovery hub]  [1340+ skills]
              │
              │
    ┌─────────┴──────────┐
    │                    │
  claude-mem (44k)    planning-with-
  [persistent memory] files (17k)
                      [file-based planning]

  === Cursor equivalent ===
  awesome-cursorrules (38k) ── .cursorrules collection

  === Aider equivalent ===
  Aider-AI/aider (42k) ── CONVENTIONS.md + .aider.conf.yml

  === Security-focused ===
  trailofbits/claude-code-config (1.7k) ── Opinionated security defaults + hooks
```

---

## Key Takeaways

1. **The ecosystem has exploded**: obra/superpowers and everything-claude-code both exceed 130k stars. The Agent Skills spec is an adopted open standard.

2. **SKILL.md is the standard**: YAML frontmatter (name + description) + markdown body. Under 500 lines. Progressive disclosure. This is settled.

3. **Three competing philosophies**:
   - **Superpowers**: Methodology-first (TDD, planning, subagent orchestration)
   - **Everything-claude-code**: Kitchen-sink (147 skills for every language/domain)
   - **Trail of Bits**: Security-first with hooks as guardrails

4. **The most actionable skills** are workflow skills (planning, TDD, code review), not domain skills (language-specific patterns). Domain skills are commodity; workflow skills differentiate.

5. **Persistent memory is the frontier**: claude-mem (44k stars), planning-with-files (17k), everything-claude-code's instinct learning. Everyone is trying to solve "Claude forgets between sessions."

6. **Conventions-as-code works everywhere**: Aider's CONVENTIONS.md, Cursor's .cursorrules, Claude's CLAUDE.md — same pattern, different file names. Read-only context that shapes all output.

---

*Research conducted April 2, 2026*
