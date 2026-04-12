# PILOT.md — metadev-protocol

**Date:** 2026-04-12
**Phase:** Pre-launch — preparing `v1.0.0` public release

---

## Current state

Template is feature-complete for v1.0.0: universal Python scaffold (src/tests/scripts/data/docs), copier-driven generation with `meta_visibility` public/private, workflow gates with explicit approval, `.meta/` taxonomy with filename enforcement, commit-per-logical-unit rule. Remaining work is publication hygiene (CREDITS, CI, git history cleanup) before tagging and outreach.

Historical milestones (MVP Phase A, ADR-008 settings v2, ADR-009 universal architecture, v0.2 skills ecosystem) are preserved in `.meta/archive/` and `.meta/decisions/`.

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
| 4.1 | Beta outreach (19 contacts + dream targets) | TODO |
| 4.2 | Draft posts (LinkedIn, X, Reddit, HN) | TODO |
| 4.3 | Demo GIF / video | TODO |
| 4.4 | Public launch sequence | TODO |

### Post-merge backlog (v1.0.x → v1.1.0)
| # | Task | Source | Status |
|---|---|---|---|
| PM.1 | Turn `active/brainstorm-2026-04-12-claude-ai-project-starter.md` into spec(s) — decide scope of C1 (vision scaffolding), C2 (wiki tier), C3 (/research skill); execute doc-only batch §4.1 | brainstorm-2026-04-12 | PENDING (post-merge) |
| PM.2 | Add Guillaume Desforges to launch outreach list with hook from §6 | brainstorm-2026-04-12 | PENDING (post-merge) |
| PM.3 | Tech watch script — scrape GitHub trending for claude-code/agentic/ai-coding/copier topics, feed `.meta/references/raw/` automatically. Script not skill (lightweight, cron-friendly). Connects to Nightshift vision | session-2026-04-12 | PENDING (post-merge) |

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
