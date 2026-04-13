# Credits

## Creator

**Vincent** ([@Vincent-20-100](https://github.com/Vincent-20-100)) — design, architecture, and implementation.

## AI assistance

Built with **Claude** (Anthropic) as AI pair. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the attribution philosophy.

## Inspirations

| Project | Author | What we learned |
|---------|--------|-----------------|
| [nix-copier-python](https://github.com/GuillaumeDesworkes/nix-copier-python) | Guillaume Desforges | Copier + Nix template architecture — proved that opinionated scaffolding with reproducible builds works at scale |
| [claude-ai-project-starter](https://github.com/GuillaumeDesforges/claude-ai-project-starter) | Guillaume Desforges | v1.2.0 — absorbed philosophy prose and engineering defaults: three pillars (A2), working rhythm (A3), anti-patterns (A4), correction-loop rule (A6), doc-decay rule (A7), trunk-based (B1), modular monolith (B2), stdlib-first (B4), errors as knowledge (B5), third-occurrence automation (B6), ADR template (B8) |
| [Graphify](https://github.com/safishamsi/graphify) | Safi Shamsi | Knowledge graph patterns — deterministic AST extraction, confidence-tagged edges, transactional pipelines, cost tracking |
| [Feynman](https://github.com/getcompanion-ai/feynman) | Companion AI | Multi-agent research system — provenance sidecars, honesty constraints, verification persona |
| [Earnings Call Analyst](https://github.com/yedanzhang-ai/earnings-call-analyst) | Yedan Zhang | LLM pipeline with tiered verification — green/amber/red confidence scoring, versioned prompt files |
| [Superpowers](https://github.com/toddgilb/superpowers) | Todd Gilbert | Skills ecosystem — brainstorming, planning, and code review as composable skills |
| [Everything Claude Code](https://github.com/mrpbennett/everything-claude-code) | Various | Community-driven skill collection — patterns for linting, TDD, security review |

## Vendored code

| Project | Author | License | What was vendored |
|---------|--------|---------|-------------------|
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | Panniantong | MIT | `Channel` ABC → `Source` ABC (renamed), `channels/github.py` and `channels/rss.py` structure patterns. Vendored into `template/scripts/radar/sources/` with attribution headers. |

## Tools

| Tool | Role |
|------|------|
| [Copier](https://github.com/copier-org/copier) | Template engine + versioned updates |
| [uv](https://github.com/astral-sh/uv) | Package manager + venv |
| [ruff](https://github.com/astral-sh/ruff) | Lint + format |
| [pre-commit](https://pre-commit.com/) | Git hooks |
| [Claude Code](https://claude.ai/code) | AI-assisted development |

## License

[MIT](LICENSE) — use it, fork it, improve it.
