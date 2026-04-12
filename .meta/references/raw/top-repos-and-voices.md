# Top Repos, People, and Resources for AI-Assisted Development

> Research compiled 2026-04-01. Reference material for metadev-protocol template design.

---

## Tier 1: Essential References

### Official Anthropic Documentation

| Resource | URL | Why it matters |
|----------|-----|----------------|
| Claude Code Best Practices | https://code.claude.com/docs/en/best-practices | The definitive guide. Covers CLAUDE.md, hooks, skills, context management, scaling patterns. Everything else derives from this. |
| Claude Code Skills docs | https://code.claude.com/docs/en/skills | Official skill format, frontmatter spec, progressive disclosure model |
| Claude Code Hooks Guide | https://code.claude.com/docs/en/hooks-guide | 12 hook events, deterministic enforcement vs advisory CLAUDE.md |
| How Anthropic teams use Claude Code | https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf | Internal Anthropic workflows -- Data Infra, Applied AI teams. Real-world patterns. |
| Claude Code Advanced Patterns (webinar) | https://www.anthropic.com/webinars/claude-code-advanced-patterns | Subagents, MCP, scaling to real codebases |

### Boris Cherny (Creator of Claude Code)

| Resource | URL | Why it matters |
|----------|-----|----------------|
| Creator's 100-Line Workflow | https://mindwiredai.com/2026/03/25/claude-code-creator-workflow-claudemd/ | Keeps CLAUDE.md at ~2,500 tokens (~100 lines). Runs 10-15 sessions simultaneously. Rule: "When Claude does something wrong, add it to CLAUDE.md so it doesn't repeat it." |

---

## Tier 2: Best Community Repos

### Claude Code Configuration & Skills

| Repo | Stars | URL | Why it matters |
|------|-------|-----|----------------|
| **awesome-claude-code** (hesreallyhim) | High | https://github.com/hesreallyhim/awesome-claude-code | Curated list of skills, hooks, slash-commands, agent orchestrators, plugins. Good overview of the ecosystem. |
| **awesome-claude-code-toolkit** (rohitg00) | High | https://github.com/rohitg00/awesome-claude-code-toolkit | Most comprehensive: 135 agents, 35 skills (+400K via SkillKit), 42 commands, 150+ plugins, 19 hooks, 15 rules, 7 templates, 8 MCP configs. Good for browsing what's possible. |
| **everything-claude-code** (affaan-m) | High | https://github.com/affaan-m/everything-claude-code | "Agent harness performance optimization system." Cognitive architecture, instinct-based learning, research-first development. Built at Claude Code Hackathon (Cerebral Valley x Anthropic, Feb 2026). Novel patterns: continuous learning pipeline, instinct extraction, checkpoint verification. |
| **claude-code-best-practice** (shanraisshan) | Medium | https://github.com/shanraisshan/claude-code-best-practice | Clean reference implementation of Command > Agent > Skill architecture. Good CLAUDE.md example. Configuration hierarchy documented. |
| **claude-code-ultimate-guide** (FlorianBruniaux) | Medium | https://github.com/FlorianBruniaux/claude-code-ultimate-guide | Beginner to power user. Production-ready templates, agentic workflow guides, quizzes, cheatsheet. Good for learning. |
| **awesome-claude-skills** (BehiSecc) | Medium | https://github.com/BehiSecc/awesome-claude-skills | Focused specifically on the skill ecosystem |

### Claude Code System Internals

| Repo | URL | Why it matters |
|------|-----|----------------|
| **claude-code-system-prompts** (Piebald-AI) | https://github.com/Piebald-AI/claude-code-system-prompts | All system prompts, 24 builtin tool descriptions, sub-agent prompts, utility prompts. Updated per version (v2.1.89, March 2026). CHANGELOG across 138 versions. Essential for understanding what Claude Code does internally. |
| **claw-code** (instructkr) | https://github.com/instructkr/claw-code | Clean-room Rust rewrite of Claude Code architecture. Reveals: one agent loop, 40+ tools, on-demand skill loading, context compression, subagent spawning, worktree isolation, 19 permission-gated tools. Fastest repo to 100K stars. |

### Tooling

| Tool | URL | Why it matters |
|------|-----|----------------|
| **agnix** (agent-sh) | https://github.com/agent-sh/agnix | Linter for AI agent configurations. Validates SKILL.md, CLAUDE.md, hooks, MCP configs. 156 rules, auto-fix, LSP server. Could be integrated into pre-commit. |

---

## Tier 3: Python Scaffolding Templates

### Copier Templates (directly relevant to metadev-protocol)

| Repo | URL | Why it matters |
|------|-----|----------------|
| **copier-uv** (pawamoy) | https://github.com/pawamoy/copier-uv | Mature Copier+uv template. ruff, ty, pytest+coverage, duty task runner, auto-changelog. Good reference for pyproject.toml.jinja patterns. |
| **simple-modern-uv** (jlevy) | https://github.com/jlevy/simple-modern-uv | Minimal and opinionated. uv, ruff, mypy, codespell, pytest, GitHub Actions, dynamic versioning. Good "less is more" reference. |
| **Substrate** (superlinear.eu) | https://superlinear.eu/about-us/news/announcing-substrate-a-modern-copier-template-for-scaffolding-python-projects | Conventional Commits, Semantic Versioning, Keep a Changelog, one-click dev environments. Migrated from Cookiecutter to Copier. |
| **python-package-copier-template** (mgaitan) | https://github.com/mgaitan/python-package-copier-template | Python 3.12+, src/ layout, uv_build backend, PEP 735 dependency groups, ruff at 120 chars, comprehensive pyproject.toml.jinja example. |
| **scaffold-py** (Aaronontheweb) | https://github.com/Aaronontheweb/scaffold-py | Simple project scaffolding focused on getting started fast |

### Python Setup Guides

| Resource | URL | Why it matters |
|----------|-----|----------------|
| Modern Python Project Setup for AI Assistants | https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/ | Standardized AI-assistant guidance for scaffolding. Recommends `uv run` and `uvx`. |
| Simple, Modern Python (blog) | https://pydevtools.com/blog/simple-modern-uv/ | Rationale for the minimal modern Python stack |

---

## Tier 4: Vibe Coding Methodology

### Key Articles & Guides

| Resource | URL | Why it matters |
|----------|-----|----------------|
| Sitepoint: Vibe Coding Guide 2026 | https://www.sitepoint.com/vibe-coding-2026-complete-guide/ | Comprehensive overview of the methodology's maturation |
| The Orchestrator framework | https://medium.com/@techie.fellow/the-vibe-coding-revolution-why-2026-belongs-to-the-orchestrators-46b32d530133 | Three pillars: Context Architecture, Recursive Arguing, Product Intuition |
| Builder.io: 50 Claude Code Tips | https://www.builder.io/blog/claude-code-tips-best-practices | Practical daily-use tips, well-organized |
| Builder.io: How I use Claude Code | https://www.builder.io/blog/claude-code | Workflow-focused, real practitioner perspective |
| DataCamp: Planning, Context Transfer, TDD | https://www.datacamp.com/tutorial/claude-code-best-practices | Structured practices with emphasis on TDD |
| F22 Labs: 10 Productivity Workflows | https://www.f22labs.com/blogs/10-claude-code-productivity-tips-for-every-developer/ | Focused workflow patterns |
| Substack: Complete Guide to Vibe Coding | https://natesnewsletter.substack.com/p/the-claude-code-complete-guide-learn | Learn vibe coding and agentic AI -- good for onboarding |

### Academic

| Resource | URL | Why it matters |
|----------|-----|----------------|
| VibeX 2026 Workshop | https://conf.researchr.org/home/ease-2026/vibex-2026 | 1st academic workshop on vibe coding. Signal that it is being taken seriously. |
| Vibe Coding in Practice (ICSE 2026) | https://kblincoe.github.io/publications/2026_ICSE_SEIP_vibe-coding.pdf | Empirical research on motivations, challenges, future outlook |
| Advait Sarkar: Vibe Coding (2025) | https://advait.org/files/sarkar_2025_vibe_coding.pdf | Early academic framing of the concept |

---

## Key People to Watch

| Person | Context | Why they matter |
|--------|---------|-----------------|
| **Boris Cherny** | Creator of Claude Code | His workflow (100-line CLAUDE.md, 10-15 parallel sessions) is the gold standard |
| **Andrej Karpathy** | Coined "vibe coding" (2025) | Originated the concept and continues to shape the conversation |
| **Sigrid Jin** (@instructkr) | Created claw-code | Deep understanding of Claude Code architecture from the leak analysis |
| **affaan-m** | everything-claude-code | Cognitive architecture patterns, instinct-based learning, research-first development |
| **pawamoy** | copier-uv | Best reference for Copier+uv Python template patterns |
| **shanraisshan** | claude-code-best-practice | Clean reference implementation of Claude Code configuration patterns |

---

## What Matters Most for metadev-protocol

### Direct applicability (use now)

1. **copier-uv** and **simple-modern-uv** -- reference their pyproject.toml.jinja, copier.yml patterns
2. **Anthropic best practices doc** -- CLAUDE.md sizing, progressive disclosure, hooks vs advisory
3. **claude-code-best-practice** -- Command > Agent > Skill architecture pattern
4. **Boris Cherny's workflow** -- keep it small, add rules reactively not proactively

### Aspirational (consider for future iterations)

1. **everything-claude-code** -- instinct extraction, continuous learning pipeline
2. **agnix linter** -- could validate generated CLAUDE.md files
3. **Agent teams** -- Writer/Reviewer pattern for quality
4. **Profile-based configuration** -- selective skill/hook installation by project type

### Anti-patterns to avoid

1. Over-engineering the CLAUDE.md template (keep under 200 lines)
2. Including skills/hooks/agents in v1 -- start simple, prove need first
3. Copying community mega-repos wholesale -- they are reference material, not templates
4. Optimizing for features over simplicity -- the template should generate the minimum viable AI-assisted project
