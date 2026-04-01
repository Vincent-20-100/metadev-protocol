# State of the Art: Vibe Coding & AI-Assisted Development

> Research compiled 2026-04-01. Raw reference material for metadev-protocol template design.

---

## 1. CLAUDE.md Best Practices (Anthropic Official + Community)

### What to include

| Include | Exclude |
|---------|---------|
| Bash commands Claude cannot guess | Anything Claude figures out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API docs (link instead) |
| Repo etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to the project | Long explanations or tutorials |
| Dev environment quirks (required env vars) | File-by-file codebase descriptions |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

### Sizing and compliance

- Anthropic internal guidance: keep CLAUDE.md **under 200 lines per file**. General consensus: under 300 lines.
- There is a ~150-200 instruction budget before compliance drops off; the system prompt already uses ~50 of those.
- For every line, ask: "Would Claude make a mistake without this?" If not, it is noise.
- CLAUDE.md instructions are followed ~70-80% of the time. Hooks enforce rules at 100%.
- If Claude keeps ignoring a rule, the file is probably too long and the rule is getting lost.
- You can tune adherence by adding emphasis ("IMPORTANT", "YOU MUST") but use sparingly.

### Structure pattern (WHAT / WHY / HOW framework)

1. **WHAT**: Tech stack, project structure, codebase map (especially for monorepos)
2. **WHY**: Purpose of the project, what each part does
3. **HOW**: How to work on the project -- build commands, verification steps, test runners, unique tooling

Recommended section order: context first, then commands, then project structure, then conventions, then references. Each section should be scannable.

### Progressive disclosure

- CLAUDE.md loads every session. Only include broadly applicable content.
- Use **Skills** (`.claude/skills/`) for specialized domain knowledge that loads on demand.
- Use **`@path/to/file`** imports in CLAUDE.md to reference other docs without inlining them.
- CLAUDE.md in child directories loads on demand when Claude works in those directories.
- Hierarchy: `~/.claude/CLAUDE.md` (global) > project root > parent dirs > child dirs.

### Anti-patterns

- The "kitchen sink session": mixing unrelated tasks without `/clear`
- The "hotfix dump": appending reactive instructions that bloat the file
- Over-specification: documenting what Claude already does correctly
- Correcting over and over: after 2 failed corrections, `/clear` and write a better prompt

Source: https://code.claude.com/docs/en/best-practices

---

## 2. Claude Code Architecture & Extension Model

### The extension hierarchy (2026)

Claude Code is now a full agent platform with five extension types:

| Extension | Purpose | Loads when |
|-----------|---------|------------|
| **CLAUDE.md** | Persistent project context and rules | Every session (advisory) |
| **Skills** (`.claude/skills/`) | Domain knowledge, reusable workflows | On demand / when relevant |
| **Hooks** (`.claude/settings.json`) | Deterministic automation at lifecycle events | Always (guaranteed execution) |
| **Subagents** (`.claude/agents/`) | Specialized delegates with own context | When explicitly invoked |
| **MCP servers** | External tool integrations | When tools are needed |
| **Plugins** | Bundled packages of above | When installed |

### Skills pattern

```
.claude/skills/
  api-conventions/
    SKILL.md          # Frontmatter + instructions
    references/       # Supporting docs
    scripts/          # Utility scripts
    examples/         # Example code
```

Frontmatter fields: `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `hooks`.

Best practice: "Skills are folders, not files." Use subdirectories for progressive disclosure. Give goals and constraints, not prescriptive step-by-step instructions.

Skills follow the Agent Skills open standard -- same SKILL.md format works across Claude Code, Cursor, Gemini CLI, Codex CLI, and Antigravity IDE.

### Hooks pattern

12 hook events in 5 categories. Key use cases:
- Security: block secrets before they reach the repo (25 regex patterns)
- Quality: auto-run eslint/ruff after every file edit
- Safety: block writes to protected directories (migrations, etc.)
- Notification: cross-platform sound effects on events

Hooks are deterministic. CLAUDE.md is advisory. For critical rules, always prefer hooks.

### Subagent orchestration

- Subagents run in their own context window -- exploration does not pollute main context
- Writer/Reviewer pattern: one session writes, another reviews with fresh context
- Fan-out/fan-in: parallel subagents for multi-dimensional analysis
- Subagents cannot invoke other subagents via bash; must use the Agent tool

### Configuration hierarchy (6 levels)

Managed settings > CLI arguments > `.claude/settings.local.json` > `.claude/settings.json` > `~/.claude/settings.json` > hooks config overrides

Source: https://github.com/shanraisshan/claude-code-best-practice

---

## 3. Core Workflow: Research > Plan > Execute > Review > Ship

All high-quality sources converge on this pattern:

1. **Explore** (Plan Mode): Read files, understand the codebase, no changes
2. **Plan** (Plan Mode): Create detailed implementation plan. Ctrl+G to edit plan in editor
3. **Implement** (Normal Mode): Execute against the plan with verification
4. **Commit**: Descriptive message, create PR

When to skip planning: if you can describe the diff in one sentence.

### Context management

- Context window is the most important resource to manage
- At 70% context, precision drops. At 85%, hallucinations increase. At 90%+, erratic behavior.
- Use `/compact` at 70-90%. `/clear` is mandatory at 90%+.
- `/clear` between unrelated tasks
- Customize compaction: add to CLAUDE.md "When compacting, always preserve the full list of modified files and any test commands"
- `/btw` for quick questions that don't enter conversation history
- Use subagents for investigation to keep main context clean

### Verification is the highest-leverage practice

"Give Claude a way to verify its work" -- this is the single most impactful thing you can do.
- Provide test cases, screenshots, expected outputs
- Include test commands in CLAUDE.md
- Use the Claude in Chrome extension for UI verification
- Without verification criteria, Claude produces plausible-looking but broken code

Source: https://code.claude.com/docs/en/best-practices

---

## 4. Vibe Coding: From Buzzword to Methodology (2026)

### Origin and evolution

- Coined by Andrej Karpathy in early 2025: surrender detailed control to LLM, accept generated code, focus on describing intent
- Collins English Dictionary "Word of the Year" 2025
- By 2026: structured development approach with dedicated tools, established workflows, projected $8.5B global market
- Stack Overflow 2025: 82% of professional developers use AI assistants daily (up from 48% in 2024)

### The maturation

2025 was "the year of the vibe hangover" -- organizations that replaced engineers with prompts hit security, maintenance, and architectural walls. 2026 brought discipline:

- **Red Zone / Green Zone**: Green Zone = UI/UX where AI excels. Red Zone = auth, data sanitization, financial calculations -- AI suggests, humans verify.
- **Automated Quality Gates**: treat AI code as untrusted code. Scan with Snyk/Semgrep, generate unit tests at every integration point.
- **Comprehensive Upfront Planning**: draft technical PRDs, define data models, outline security guardrails BEFORE generating code.

### The Orchestrator framework

Three pillars:
1. **Context Architecture** -- structure the environment so the AI cannot fail
2. **Recursive Arguing** -- use one AI to write code and a second AI to break it
3. **Product Intuition** -- "How it works" is commodity; "Why it matters" sells

### Key statistics

- 3-5x faster prototyping, 25-50% acceleration on routine tasks
- Up to 45% of AI-generated code contains security vulnerabilities
- AI writes 60-70% of first drafts in modern stacks

### Academic validation

- VibeX 2026: 1st International Workshop on Vibe Coding and Vibe Researching (at EASE 2026)
- ICSE-SEIP 2026: "Vibe Coding in Practice: Motivations, Challenges, and a Future Outlook"

Sources:
- https://www.sitepoint.com/vibe-coding-2026-complete-guide/
- https://medium.com/@techie.fellow/the-vibe-coding-revolution-why-2026-belongs-to-the-orchestrators-46b32d530133

---

## 5. Claw Code: What the Claude Code Leak Revealed

### The event (March 31, 2026)

Anthropic accidentally exposed ~512K lines of Claude Code source via a .map file on npm (~1,900 files). The `claw-code` repo by Sigrid Jin (@instructkr) became the fastest-growing GitHub repo in history (50K stars in 2 hours, surpassed original Claude Code repo).

### Architecture insights

Claude Code is not a single chatbot loop. It is:

- **One agent loop** with 40+ discrete tools
- **On-demand skill loading** (not everything loaded at once)
- **Context compression** (strategic compaction, not naive truncation)
- **Subagent spawning** with task dependency graphs
- **Worktree isolation** for parallel execution
- **19 built-in permission-gated tools** (file reading, Bash, web scraping, LSP, Git)
- **Plugin-based architecture** with hook pipeline

### Claw-code's clean-room implementation

Rust workspace structure (`rust/crates/`):
- API Client Layer: provider abstraction, OAuth, streaming
- Runtime Engine: session state, context compaction, MCP orchestration, prompt construction
- Tool Framework: manifest definitions + execution pipeline
- Command System: slash commands, skill discovery, config inspection
- Plugin Architecture: hook-based pipeline with bundled plugins
- CLI Interface: interactive REPL with markdown rendering

### Hidden features discovered

- **ULTRAPLAN**: offloads complex planning to a remote Cloud Container Runtime session running Opus 4.6, gives up to 30 minutes, user approves from browser
- **Buddy**: Tamagotchi-style companion pet system (gacha, species rarity, shiny variants) -- gated behind compile-time feature flag
- **Anti-distillation features**: designed to pollute training data competitors might extract

Source: https://github.com/instructkr/claw-code

---

## 6. Modern Python Project Scaffolding (2026)

### Consensus stack

| Layer | Tool | Notes |
|-------|------|-------|
| Package management | `uv` | Replaces pip, poetry, conda entirely |
| Linting + formatting | `ruff` | Replaces black, isort, flake8 in one tool |
| Config | `pyproject.toml` | PEP 621, single config file for everything |
| Templating | `copier` | Versioned templates, auto-updates, better than cookiecutter |
| Hooks | `pre-commit` | Git hooks for quality gates |
| Testing | `pytest` | With coverage plugins |
| Type checking | `mypy` or `ty` (by Astral) | Static analysis |
| Python version | >= 3.12 | Minimum for modern features |

### Copier advantages over Cookiecutter

- Templates are versioned by default
- `copier update` pulls template improvements into existing projects
- `when` key reduces questions during project creation
- `_tasks` section runs post-creation commands (git init, install deps, run tests)
- Jinja2 templating with conditionals

### Template design best practices

- Strip questions to essentials: project name, module name, Python version, description
- Everything else should have sensible defaults changeable later
- Provide a consistent interface (Makefile or similar) -- same commands across all generated projects
- Use dependency groups (PEP 735) for organizing deps by purpose (test, docs, dev)
- `src/` layout for packages
- Line length: 120 chars (modern consensus)

### Notable Copier templates

- **copier-uv** (pawamoy): ruff, ty, pytest+coverage, duty task runner, auto-changelog from conventional commits
- **simple-modern-uv** (jlevy): minimal but complete -- uv, ruff, mypy, codespell, pytest, GitHub Actions, dynamic versioning
- **Substrate** (superlinear.eu): Conventional Commits, Semantic Versioning, Keep a Changelog, one-click dev environments

### AI-assistant-specific guidance

- AI assistants should prefer `uv run <command>` (dev deps) and `uvx <command>` (one-off tools)
- `uv init` auto-creates PEP 621 pyproject.toml + .gitignore
- AI writes 60-70% of first drafts; linting, tests, and refactors suggested in real time
- Provide verification commands in CLAUDE.md so Claude can self-check

Source: https://github.com/pawamoy/copier-uv, https://github.com/jlevy/simple-modern-uv

---

## 7. Everything Claude Code: Cognitive Architecture Patterns

### Harness performance optimization

Treats Claude Code configuration as an engineering discipline, not ad-hoc customization:
- **Checkpoint-based verification** mirrors software testing
- **Instinct extraction** mirrors knowledge management
- **Hook-based automation** mirrors infrastructure as code

### Research-first development

"Search-first" skill embeds documentation research as a prerequisite before code generation. Structured exploration beats hallucination.

### Continuous learning pipeline

Sessions automatically extract reusable patterns through "learn" and "learn-eval" commands. Extracted instincts (confidence-scored micro-patterns) cluster into shareable skills. Individual sessions inform team knowledge.

### Instinct-based knowledge base

Learned patterns stored as structured instincts with metadata:
- Confidence score
- Applicability context
- Evolution history
- Schema: frontmatter, action, evidence, examples

### Profile-based installation

Selective profiles (`--profile full`, language-specific targets) and cross-platform compatibility. Five-tier package manager auto-detection. Runtime hook gating via environment variables.

### Scale

- 36 specialized subagents
- 147 domain-specific skills
- 68 legacy command shims
- 17 of 37 skills use parallel sub-agents
- 3 orchestration patterns: fan-out/fan-in, batch processing, triage-then-deep-process

Source: https://github.com/affaan-m/everything-claude-code

---

## 8. Actionable Patterns for metadev-protocol

### What this means for our template system

1. **CLAUDE.md.jinja must be lean**: under 200 lines, scannable sections, no noise
2. **Include verification commands**: build, test, lint commands are the highest-leverage content
3. **Use the WHAT/WHY/HOW framework** for CLAUDE.md structure
4. **Progressive disclosure via skills**: domain-specific guidance goes in `.claude/skills/`, not CLAUDE.md
5. **Hooks for non-negotiable rules**: format-on-save, lint-on-commit, blocked directories
6. **Compaction instructions**: add "When compacting, preserve..." guidance in CLAUDE.md
7. **Template should generate `.claude/` directory structure**: settings.json, skills/, agents/
8. **Copier `_tasks`**: auto-run `uv sync`, `pre-commit install`, initial git setup after generation
9. **Dependency groups (PEP 735)**: organize pyproject.toml deps by purpose
10. **Red Zone / Green Zone thinking**: template should flag areas where AI suggestions need human review
11. **Research > Plan > Execute > Review > Ship**: embed this workflow in generated PILOT.md
12. **Context architecture**: structure the project so Claude cannot fail -- clear names, obvious paths, discoverable patterns
