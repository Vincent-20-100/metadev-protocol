# SESSION-CONTEXT.md — metadev-protocol

<!-- RULES: rewrite every session (never append) · target ≤ 50 lines nominal
     Dense session? → create .meta/active/session-YYYY-MM-DD-slug.md, reference here
     Every 5 commits: full rewrite regardless of apparent freshness
     See .claude/rules/memory.md for full protocol -->
<!-- Last full rewrite: 2026-04-21 -->

---

## Architecture snapshot

<!-- ≤ 8 lines — current modules and how they communicate -->

Template system: `copier.yml` drives generation from `template/`. Meta-repo and
generated projects share `.claude/rules/` and skills (dogfood pattern). Pre-commit
hooks enforce contracts (skills, secrets, naming, git author).

## Active decisions

<!-- ≤ 15 lines — format: "We do X because Y. Rejected: Z." -->

- memory.md shipped as advisory rule (no hook). Rejected: hook on line count — enforces
  form not quality, same pattern as code-style.md.
- SESSION-CONTEXT target ≤ 50 lines nominal (not hard block). Rejected: adaptive 50/80
  — upper bound becomes default over time.
- Session defined as milestone (commit) not Claude Code conversation. Aligns with
  existing commit discipline.

## Traps to avoid

<!-- ≤ 10 lines — format: "Don't do X — it causes Y (observed DATE)" -->

- Don't commit from remote Claude Code session without identity.yaml — container
  overwrites git author with Claude (observed 2026-04-21, fixed via SessionStart hook).
- Don't append SESSION-CONTEXT — stale decisions accumulate silently and misdirect
  fresh LLM context.

## Open questions

<!-- ≤ 8 lines — one question per line -->

- hooks↔rules pairing chantier: synthesis-2026-04-21-hard-block-dx-audit.md pending
  implementation (PR-4-B2 not yet opened).

## Pending plans

<!-- ≤ 9 lines — format: "- plan-<slug>.md — <one-line status>" -->

- Phase 4 launch (outreach + demo GIF) — unblocked, awaiting vhs install for GIF.
