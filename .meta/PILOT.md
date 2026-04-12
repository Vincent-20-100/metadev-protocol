# PILOT.md — metadev-protocol

**Date:** 2026-04-12
**Phase:** Pre-launch — v1.1.0 shipped, preparing Phase 4 (launch)

---

## Current state

v1.0.0 shipped (clean orphan branch, tagged). v1.0.1 added governance polish from 4-repo audit (honesty constraint, confidence gates, synthesis type, brand guide, demo script, banner). v1.1.0 adds skill discoverability mechanism (automatism #11 Rule of 3 + inverted-default trigger table) and full README rework (pixel-art banner, Before/After + Rails diagrams). Phase 4 (launch) in progress: outreach spec and post drafts ready, messaging system specified.

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
| 3.1 | Orphan branch → `v1.0.0` (clean break) | DEFERRED (final merge step) |
| 3.2 | Pre-commit hook: block `GIT_AUTHOR_NAME == Claude` | DONE |
| 3.3 | CONTRIBUTORS.md | DONE |
| 3.4 | README staleness re-check (pre-merge audit) | DONE |

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
| PM.1a | Absorb §4.1 doc-only batch from claude-ai-project-starter brainstorm into PHILOSOPHY, GUIDELINES, CLAUDE.md, new ADR template | brainstorm-2026-04-12 | PLAN READY (`active/plan-2026-04-13-absorb-claude-starter-prose.md`) |
| PM.1b | `/research` skill — external research (WebSearch + WebFetch + MCP), standardized output to `raw/`, orthogonal to `/brainstorm`. Reference: Agent-Reach | brainstorm-2026-04-13-research-skill | PLAN READY (`active/plan-2026-04-13-research-skill.md`) |
| PM.1c | `/vision` skill — fills a Vision section in PILOT.md (problem / user / V1 scope / north star). Auto-proposed on first session | brainstorm-2026-04-13-vision-skill | PLAN READY (`active/plan-2026-04-13-vision-skill.md`) |
| PM.1d | C2 wiki tier — **REJECTED for v1.2**, gap acknowledged, revisit when ≥3 real projects demand it | brainstorm-2026-04-13-wiki-tier | REJECTED |
| PM.2 | Add Guillaume Desforges to launch outreach list with hook from §6 | brainstorm-2026-04-12 | DONE (v1.1.0 — included in outreach spec) |
| PM.3 | Tech watch script — scrape GitHub trending for claude-code/agentic/ai-coding/copier topics, feed `.meta/references/raw/` automatically. Script not skill (lightweight, cron-friendly). Connects to Nightshift vision | session-2026-04-12 | PLAN READY (`active/plan-2026-04-13-tech-watch-script.md`) |
| PM.4 | Multi-agent synthesis run — cross-pollinate ALL reference sources for emergent structural innovations (not feature-picking) | debate-2026-04-12 | PENDING |
| PM.5 | Provenance sidecar convention (deferred from T1.7) | synthesis-2026-04-12 | PENDING |
| PM.6 | `/audit-repo` skill (meta-repo only, not shipped) — structured analysis of external repos with tiered output: use as-is → extract parts → borrow concepts → inspiration → reject. Standardized format enables cross-pollination when 10+ audits accumulated. Feeds PM.4 synthesis run. Source: Agent-Reach audit session | session-2026-04-12 | PLAN READY (`active/plan-2026-04-13-audit-repo-skill.md`) |
| PM.7 | Skill/agent discoverability problem — the LLM doesn't proactively propose skills and agents enough. New users who don't know features exist won't get full value. Need to improve CLAUDE.md automatisms, onboarding, and/or skill suggestion triggers | session-2026-04-12 | DONE (v1.1.0 — automatism #11 + trigger table) |

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
