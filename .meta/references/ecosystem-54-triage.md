# Ecosystem 54 Resources — Triage (2026-04-04)

11 web searches performed. Findings below.

---

## Priority 1 — Skills Directories

### ecc.tools / Everything Claude Code (ECC)
- **What**: GitHub App + OSS repo (156 skills, 38 agents, 72 commands). Generates custom skills from git history. Profiles: core/developer/security/full.
- **Relevant?** LATER — Too heavy for a template generator. But their profile-based install pattern is worth studying.
- **Take**: The "selective install builder" pattern (pick a profile, get matching skills) mirrors our copier profiles.
- **Links**: [ecc.tools](https://ecc.tools), [github](https://github.com/affaan-m/everything-claude-code)

### skillsdirectory.com
- **What**: Security-tested agent skills marketplace. Every skill scanned for malware, prompt injection, credential theft.
- **Relevant?** NO — Discovery platform, not a source of template patterns.
- **Link**: [skillsdirectory.com](https://www.skillsdirectory.com/)

### mcpmarket.com/tools/skills
- **What**: Agent skills directory for Claude, ChatGPT, Codex. Categories: Dev Tools, API Dev, Data Science, Productivity.
- **Relevant?** YES — Has Python-specific skills worth reviewing:
  - "uv Python Project Manager" — standardized uv workflow for pyproject.toml
  - "Python Best Practices" — modern Python 3.10+ patterns
  - "UV Python Workspaces" — monorepo patterns with uv
- **Take**: Review the uv skill's SKILL.md for patterns we could embed in our template.
- **Link**: [mcpmarket.com/tools/skills](https://mcpmarket.com/tools/skills)

### agentskills.so
- **What**: Another skill browser, indexes skills from GitHub repos.
- **Relevant?** NO — Just another directory, no unique content.

### skillsmp.com
- **What**: Agent skills marketplace for Claude, Codex, ChatGPT.
- **Relevant?** NO — Same category as above.

### awesome-claude-skills (travisvn, ComposioHQ, BehiSecc)
- **What**: Curated GitHub lists of skills. ComposioHQ version has 1,234+ skills.
- **Relevant?** LATER — Good for discovering skills to recommend in generated projects.
- **Links**: [travisvn](https://github.com/travisvn/awesome-claude-skills), [ComposioHQ](https://github.com/ComposioHQ/awesome-claude-skills)

---

## Priority 2 — Key Repos

### hesreallyhim/awesome-claude-code (the "mega repo")
- **What**: Curated list of 75+ repos: skills, hooks, slash-commands, agent orchestrators, plugins.
- **Relevant?** YES — Best single index of the ecosystem. Notable finds:
  - **agnix**: linter for CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP configs
  - **claude-devtools**: observability into sessions, compaction visualization
  - **Claude Code Templates** (Daniel Avila): collection of resources with polished UI
- **Take**: Use as discovery hub. agnix could be added to our pre-commit pipeline later.
- **Link**: [github](https://github.com/hesreallyhim/awesome-claude-code)

### trailofbits/claude-code-config (optimized settings)
- **What**: Security-hardened settings.json with deny rules, sandboxing, hooks, skills.
- **Relevant?** YES — Directly applicable to our template.
- **Take**:
  - Deny rules for `rm -rf *`, `sudo *`, `git push --force*`, SSH key access
  - Deny rules evaluated: deny > ask > allow (first match wins)
  - Security settings must be global (repos can't weaken them)
  - Sandbox mode enforces deny rules at OS level (Seatbelt/bubblewrap)
- **Link**: [github](https://github.com/trailofbits/claude-code-config)

### shanraisshan/claude-code-best-practice
- **What**: Documents 60+ settings and 170+ env vars (as of v2.1.91).
- **Relevant?** YES — Reference for which settings to expose in our template.
- **Link**: [github](https://github.com/shanraisshan/claude-code-best-practice)

### centminmod/my-claude-code-setup
- **What**: Starter template config + CLAUDE.md memory bank system.
- **Relevant?** LATER — Memory bank pattern is interesting but out of scope for now.
- **Link**: [github](https://github.com/centminmod/my-claude-code-setup)

---

## Priority 3 — Multiplexers

### cmux (craigsc/cmux)
- **What**: "tmux for Claude Code" — manages git worktrees, spins up parallel agents, each in own directory.
- **Relevant?** NO for template. Advanced user tool for running multiple agents.
- **Link**: [github](https://github.com/craigsc/cmux), [cmux.com](https://cmux.com)

### dmux (formkit/dmux, standardagents/dmux)
- **What**: Dev agent multiplexer — creates tmux pane + git worktree + launches agent.
- **Relevant?** NO for template. Same category as cmux.
- **Link**: [github](https://github.com/formkit/dmux)

### amux (mixpeek/amux)
- **What**: tmux-based multiplexer for running dozens of parallel Claude agents unattended. Has shared kanban board.
- **Relevant?** NO for template. Interesting but for power users only.
- **Link**: [github](https://github.com/mixpeek/amux)

### coder/mux
- **What**: Desktop app for isolated, parallel agentic development.
- **Relevant?** NO for template.

### Agent Teams (Anthropic, experimental)
- **What**: Native Anthropic feature (Opus 4.6). One lead session coordinates teammates. Shared task list, peer messaging, file locking.
- **Relevant?** LATER — When mature, could be documented in generated projects' CLAUDE.md.
- **Enable**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in settings.json
- **Link**: [docs](https://code.claude.com/docs/en/agent-teams)

---

## Summary — What matters for metadev-protocol

| Action | Source | Priority |
|--------|--------|----------|
| Add deny rules to template `.claude/settings.json` | trailofbits/claude-code-config | HIGH |
| Review uv skill SKILL.md for template patterns | mcpmarket.com uv skill | HIGH |
| Document settings/env vars reference | shanraisshan best-practice | MED |
| Bookmark awesome-claude-code as discovery hub | hesreallyhim/awesome-claude-code | MED |
| Consider agnix linter in pre-commit | awesome-claude-code | LOW |
| Monitor Agent Teams for future integration | Anthropic docs | LOW |
| Multiplexers: not relevant for template | cmux, dmux, amux | NONE |
