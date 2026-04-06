# gstack — Garry Tan's Claude Code skill pack

**Source:** https://github.com/garrytan/gstack
**Date:** 2026-04-06
**Type:** Reference (bronze)

---

## What it is

23 specialized AI agents organized as a sprint workflow:
Think → Plan → Build → Review → Test → Ship → Reflect.

Created by Garry Tan (YC President). Reports 600k+ LOC in 60 days solo.

Not a template/bootstrapper — a **skill pack** installed via symlinks into `~/.claude/skills/`.
Also serves OpenAI Codex and Factory Droid from the same codebase.

---

## Notable patterns

### 1. Template-generated skill docs (SKILL.md.tmpl → SKILL.md)
- Skills use `.tmpl` templates that auto-generate SKILL.md
- Never hand-edit the output — regenerate from source
- Prevents docs/code drift

### 2. Sequential workflow with approval gates
- Design review → code review → QA → ship
- Each stage validates upstream before allowing downstream
- Changes must pass all gates before release

### 3. Fix-first code review (/review)
- Findings classified as AUTO-FIX (applied immediately) or ASK (user approval)
- Every finding gets action, not just critical ones
- Results logged for downstream /ship workflow
- Special checks: enum completeness, SQL injection, race conditions

### 4. Diff-based test selection
- Only re-test code affected by changes
- Reduces API costs from ~$50 to ~$4 per eval cycle
- Tiered: static validation (free) → E2E via API (~$3.85) → LLM-as-judge (~$0.15)

### 5. Browser daemon (browse/)
- Long-lived Bun HTTP server + Playwright for QA
- Sub-second latency (vs 3-5s cold start)
- Reference system (@e1, @e2) instead of CSS selectors
- Random port + bearer token auth + 30min idle shutdown

### 6. Multi-agent distribution via symlinks
- `setup` script creates symlinks in ~/.claude/skills/, ~/.codex/skills/, ~/.factory/
- One codebase, multiple agent frameworks
- Idempotent migrations for version updates

### 7. Project context via CLAUDE.md
- Skills read the project's CLAUDE.md to determine framework, deployment, constraints
- Makes skills portable across projects/frameworks

---

## What they don't have (that we do)

- No settings.json in repo — delegated to users
- No context framework (.meta/, PILOT.md, SESSION-CONTEXT.md)
- No project template — skill pack only, no bootstrapping
- No pre-commit, no profile system
- No attribution config or security deny rules

---

## Takeaways for metadev-protocol

| Insight | Priority | Action |
|---------|----------|--------|
| SKILL.md.tmpl pattern (generate docs from template) | Medium | Consider for skill maintenance if we grow beyond 5 skills |
| Sequential gates (design → review → QA → ship) | Low | Our automatism #4 is lighter but same spirit. Revisit if adding /review |
| Fix-first review (auto-fix vs ask classification) | Medium | Good pattern for a future /review skill (Part 4) |
| Diff-based test selection | Low | Too ambitious for v2, note for v3 |
| Multi-agent symlink distribution | Medium | Relevant for Part 5 (AGENTS.md). Different model than copier but worth studying |
| /btw native command | High | Already noted — document in template for user discovery |
