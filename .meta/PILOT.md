# PILOT.md — metadev-protocol

**Date:** 2026-04-20
**Phase:** v2.0.0 shipped — chantier hooks↔rules en cours

> **⚠ Session interrompue 2026-04-20 — chantier en cours :** lis `.meta/active/session-2026-04-20-resume-hooks-rules.md` AVANT toute action. Spec + audit + débat produits dans `.meta/active/`, attend validation Vincent sur 4 décisions D1-D4.

---

## Vision

_Last updated: 2026-04-13_

### Problem
Solo developers starting AI-assisted Python projects lose hours to setup friction and structural drift. Without conventions, the LLM reinvents context each session, drafts pollute the repo, and quality erodes silently. Every project starts from zero.

### Target user
- Solo developers or small teams (1-3) beginning vibe-coding with Claude Code
- Currently spending 30-60 min per project on boilerplate setup
- Frustrated by LLM context loss between sessions and lack of structural discipline

### V1 scope
- Must: `copier copy` generates a fully configured Python project (CLAUDE.md + .meta/ + skills + hooks + pre-commit)
- Must: versioned semver tags enable `copier update` to propagate improvements to existing projects
- Should: 10 skills covering the full dev loop (brainstorm → plan → ship), plus 5 local agents
- Won't (v1): multi-language support, IDE plugins, hosted registry

### North star metric
≥10 external projects using metadev-protocol via `copier copy` within 30 days of public launch.

---

## Current state

v2.0.0 shipped. Full changelog:
- **v1.0.0** — public release, universal scaffold, 7 skills, pre-commit hooks, CI
- **v1.0.1** — governance polish (honesty constraint, confidence gates, synthesis type, banner, demo script)
- **v1.1.0** — skill discoverability (trigger table, Rule of 3), README rework, /research, /vision, /audit-repo, tech-watch script
- **v1.2.0** — /radar skill (5-source tech-watch pipeline, progressive KB), devil's-advocate agent, skill-vs-tool principle in GUIDELINES
- **v1.3.0** — enable_server_auth_check param (optional GitHub Action blocking Claude-authored PRs), GUIDELINES commit authorship section fixed
- **v1.4.0** — git history cleaned (Co-authored-by stripped), dual-stage authorship hook (pre-commit + commit-msg), OpenTimestamps proof anchored in Bitcoin
- **v1.5.0** — /research and /audit-repo thinned under skill-vs-tool principle, multi-agent synthesis run (emergent-patterns.md), skills contract script v1
- **v1.6.0** — skills architecture overhaul (ADR-010): ghost agents deleted then re-shipped as real files (code-reviewer, test-engineer, security-auditor, data-analyst), meta ↔ template full parity enforced, /radar + /audit-repo fused into /tech-watch (sweep + deep), /test and /save-progress thinned
- **v2.0.0** — multi-host + librarian + harness audit (ADR-011): AGENTS.md/GEMINI.md auto-generated @import stubs (Claude primary, Codex + Gemini import-stubs, tier 2 commented), 6th local agent `librarian` (read-only deep-source curator with file:line citations + confidence), `evals/harness_audit.py` 6-category deterministic scorecard (60 pts, meta invariant 60/60), deep-sources convention in CLAUDE.md (librarian-only, not enforced by gate hook — debate-resolved)

Phase 4 (launch) is unblocked: outreach messages drafted, platform posts drafted. Pending: demo GIF (vhs), launch sequence execution.

---

## Roadmap

### Phase 0 — Core product
| # | Task | Status |
|---|---|---|
| 0.1 | Workflow gates — implement spec | DONE |
| 0.2 | `meta_visibility` copier parameter | DONE |
| 0.3 | `.meta/` taxonomy + gitignore alignment | DONE |
| 0.4 | PILOT.md cleanup (public-ready) | DONE |
| 0.5 | Rodin agent (devil's advocate persona) | DONE (folded into 0.1) |
| 0.6 | Commit strategy — CLAUDE.md + GUIDELINES | DONE |
| P1  | Full-auto plan execution mode (safe/full-auto) | DONE |
| P2  | Pre-public audit hook (gitignore + secrets scan) | DONE |

### Phase 1 — Publication essentials
| # | Task | Status |
|---|---|---|
| 1.0 | CREDITS.md (inspirations + attributions) | DONE |
| 1.1 | CONTRIBUTING.md | DONE |
| 1.2 | CODE_OF_CONDUCT.md | DONE |
| 1.3 | CHANGELOG.md | DONE |
| 1.4 | `.github/` issue + PR templates | DONE |
| 1.5 | `.github/workflows/` (CI lint + template test) | DONE |
| 1.6 | README update (meta_visibility, copier modes) | DONE |
| 1.7 | `.gitignore` + pre-commit enrichment (meta-repo) | DONE (covered by P2) |

### Phase 2 — CI/CD & tests
| # | Task | Status |
|---|---|---|
| 2.1 | GitHub Actions: lint | DONE (ci.yml) |
| 2.2 | GitHub Actions: template validation | DONE (ci.yml matrix) |
| 2.3 | Template generation tests (pytest) | DONE |

### Phase 3 — Git hygiene (before public access)
| # | Task | Status |
|---|---|---|
| 3.1 | History cleanup — strip Co-authored-by, delete ghost branch | DONE (v1.4.0) |
| 3.2 | Pre-commit hook: block `GIT_AUTHOR_NAME == Claude` | DONE |
| 3.3 | CONTRIBUTORS.md | DONE |
| 3.4 | README staleness re-check (pre-merge audit) | DONE |
| 3.5 | Block Co-authored-by trailers (commit-msg hook) | DONE (v1.4.0) |
| 3.6 | OpenTimestamps proof anchored in Bitcoin | DONE (v1.4.0) |

### Phase 4 — Launch
| # | Task | Status |
|---|---|---|
| 4.1 | Beta outreach (19 contacts + dream targets) | DRAFTED |
| 4.2 | Draft posts (LinkedIn, X, Reddit, HN) | DRAFTED |
| 4.3 | Demo script + VHS tape | DONE |
| 4.4 | Banner SVG + brand guide | DONE |
| 4.5 | Outreach messaging spec (lead table, templates, tone) | DONE |
| 4.6 | Record demo GIF (needs vhs install) | TODO |
| 4.7 | Public launch sequence | TODO |

### v1.0.1 — Governance polish (post-debate)
| # | Task | Status |
|---|---|---|
| T1.1 | Honesty constraint (Rule #9 in CLAUDE.md.jinja) | DONE |
| T1.2 | Tiered confidence gates (GREEN/AMBER/RED in plan skill) | DONE |
| T1.3 | Synthesis type + slug lineage convention | DONE |
| T1.4 | Working with AI section (anti-patterns, ADR template, practical defaults) | DONE |
| T1.5 | CREDITS.md — add Feynman + Earnings Call Analyst | DONE |
| T1.6 | Philosophy batch (3 pillars, trunk-based, stdlib-first) | DEFERRED (trimmed by debate — manifesto, not scaffold) |
| T1.7 | Provenance sidecar convention | DEFERRED (useful at week 3+, not day 1) |

### Post-merge backlog (v1.0.x → v1.1.0)
| # | Task | Source | Status |
|---|---|---|---|
| PM.1a | Absorb §4.1 doc-only batch from claude-ai-project-starter brainstorm into PHILOSOPHY, GUIDELINES, CLAUDE.md, new ADR template | brainstorm-2026-04-12 | DONE |
| PM.1b | `/research` skill — external research (WebSearch + WebFetch + MCP), standardized output to `raw/`, orthogonal to `/brainstorm`. Reference: Agent-Reach | brainstorm-2026-04-13-research-skill | DONE |
| PM.1c | `/vision` skill — fills a Vision section in PILOT.md (problem / user / V1 scope / north star). Auto-proposed on first session | brainstorm-2026-04-13-vision-skill | DONE |
| PM.1d | C2 wiki tier — **REJECTED for v1.2**, gap acknowledged, revisit when ≥3 real projects demand it | brainstorm-2026-04-13-wiki-tier | REJECTED |
| PM.2 | Add Guillaume Desforges to launch outreach list with hook from §6 | brainstorm-2026-04-12 | DONE (v1.1.0 — included in outreach spec) |
| PM.3 | Tech watch script — scrape GitHub trending for claude-code/agentic/ai-coding/copier topics, feed `.meta/references/raw/` automatically. Script not skill (lightweight, cron-friendly). Connects to Nightshift vision | session-2026-04-12 | DONE |
| PM.4 | Multi-agent synthesis run — cross-pollinate ALL reference sources for emergent structural innovations (not feature-picking) | debate-2026-04-12 | PENDING |
| PM.5 | Provenance sidecar convention (deferred from T1.7) | synthesis-2026-04-12 | PENDING |
| PM.8 | `/radar` skill — automated tech-watch (script + thin skill, 5 tier-0 sources, progressive disclosure KB) | brainstorm-2026-04-13-radar-skill | DONE (v1.2.0) → ABSORBED into `/tech-watch` sweep mode (v1.6.0) |
| PM.9 | `devil's-advocate` agent — Rule of 3 auto-invoke, steelman + contest + expose | feedback_devils_advocate | DONE (v1.2.0) |
| PM.10 | Skill vs tool principle — codified in GUIDELINES.md.jinja, applied retroactively at next touch | session-2026-04-13 | DONE (v1.2.0) |
| PM.11 | Refactor `/research` under skill-vs-tool principle | session-2026-04-13 | DONE (v1.5.0) |
| PM.12 | Refactor `/audit-repo` under skill-vs-tool principle | session-2026-04-13 | SUPERSEDED by fusion into `/tech-watch` (v1.6.0) |
| PM.13 | enable_server_auth_check param + GitHub Action (commit author enforcement) | debate-2026-04-13 | DONE (v1.3.0) |
| PM.14 | Multi-agent synthesis run — cross-pollinate all refs for emergent innovations | session-2026-04-13 | DONE (v1.5.0) — `.meta/references/synthesis/emergent-patterns.md` |
| PM.6 | `/audit-repo` skill (meta-repo only, not shipped) — structured analysis of external repos with tiered output: use as-is → extract parts → borrow concepts → inspiration → reject. Standardized format enables cross-pollination when 10+ audits accumulated. Feeds PM.4 synthesis run. Source: Agent-Reach audit session | session-2026-04-12 | DONE → ABSORBED into `/tech-watch` deep mode (v1.6.0) |
| PM.7 | Skill/agent discoverability problem — the LLM doesn't proactively propose skills and agents enough. New users who don't know features exist won't get full value. Need to improve CLAUDE.md automatisms, onboarding, and/or skill suggestion triggers | session-2026-04-12 | DONE (v1.1.0 — automatism #11 + trigger table) |
| PM.15 | **Deep audit + brainstorm on `JuliusBrussee/caveman` + 10 other refs** — gold mine of patterns: multi-LLM native (CLAUDE.md + AGENTS.md + GEMINI.md side-by-side), multi-IDE plugin distribution (`.cursor/`, `.windsurf/`, `.clinerules/`, `.codex/`, `.claude-plugin/`), benchmarks/evals first-class, TOML commands, statusline, install/uninstall hooks. Cross-pollinated with everything-claude-code, gstack, claude-mem, BMAD-METHOD, graphify, Agent-Reach, feynman, claude-ai-project-starter, deepagents, stromboli. Full audit via parallel subagents → brainstorm synthesis → shipped as v2.0.0 (multi-host fan-out, librarian, harness audit). See ADR-011 | session-2026-04-15 | DONE (v2.0.0) |
| PM.16 | `--persist` flag on `/tech-watch` deep mode — opt-in Layer 3 vendoring (persistent clones under `~/.cache/metadev-audits/`) for iterative synthesis workflows. Codify the 4-layer progressive disclosure pattern as a metadev convention once PM.15 validates its utility. See `reference_progressive_disclosure_4layer.md` | session-2026-04-15 | BACKLOG — post PM.15 |

---

## Key conventions

- **Explicit approval before any implementation** — no exceptions, even trivial
- **Commit per complete logical unit** — not per file, not per timer; plan determines granularity; bisectable
- **Conventional commits** — `feat:` `fix:` `docs:` `chore:` `refactor:`
- **Semver tags are immutable** — never rewrite, always bump
- **`.meta/` taxonomy** — `<type>-<YYYY-MM-DD>-<slug>.md`, enforced by `scripts/check_meta_naming.py`
- **Debate is optional, brainstorm is always valid** — debate is expensive in tokens
- **Template changes must be tested** — `copier copy . /tmp/test --defaults --trust --vcs-ref=HEAD`
- **All template output in English** — code, docs, skills, comments

---

## `.meta/` structure

- `active/` — validated plans/specs currently in flight
- `archive/` — implemented or historical artifacts (chronological memory)
- `drafts/` — WIP (gitignored)
- `decisions/` — ADRs (`adr-NNN-slug.md`)
- `references/{raw,interim,synthesis}/` — external research by maturity

Full taxonomy in `.meta/GUIDELINES.md`.

---

## For AI sessions

- Read `PILOT.md` → `ARCHITECTURE.md` → relevant `decisions/adr-*.md` before acting
- Write a plan and get user validation before implementing
- Check `.meta/archive/` for past decisions before asking the user
- Superpowers plugin is the recommended complement (not a dependency)
- Stack: Python 3.13+, uv, ruff, copier, pre-commit
