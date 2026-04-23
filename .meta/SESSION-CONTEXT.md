# SESSION-CONTEXT.md — metadev-protocol

<!-- RULES: rewrite every session (never append) · target ≤ 50 lines nominal
     Dense session? → create .meta/active/session-YYYY-MM-DD-slug.md, reference here
     Every 5 commits: full rewrite regardless of apparent freshness
     See .claude/rules/memory.md for full protocol -->
<!-- Last full rewrite: 2026-04-21 -->

---

## Architecture snapshot

Template system: `copier.yml` drives generation from `template/`. Meta-repo and
generated projects share `.claude/rules/` and skills (dogfood pattern). Pre-commit
hooks enforce contracts. `.pre-commit-config.yaml.jinja` now gates H008 on
`enable_multi_host`. 5 multi-host artifacts (AGENTS.md, GEMINI.md, sync-config.yaml,
scripts/sync_hosts.py, sync-hosts.yml) excluded by default via Jinja `_exclude`.

## Active decisions

- **Claude-only is the template default (ADR-012).** Multi-host is opt-in via
  `copier copy . proj --data enable_multi_host=true`. No prompt at default copy
  (`when: false`). Rejected: 2 per-host bools (YAGNI), negative flag (silent
  regression on update), sub-template / post-gen script (two sources of truth).
- **D4 clarification:** rule files ship unconditionally, feature artifacts do not.
  v2.0.0 had over-applied D4 by shipping the entire multi-host feature unconditionally.
- SESSION-CONTEXT target ≤ 50 lines nominal (not hard block).
- Session = milestone (commit), not Claude Code conversation.

## Traps to avoid

- **Post-v2.2.0, do not assume AGENTS.md / GEMINI.md / sync-config.yaml exist in a
  generated project** — they are opt-in. Default projects are Claude-only.
- When editing `template/.pre-commit-config.yaml.jinja`, remember the file is now
  Jinja-rendered. Any `{% %}` or `{{ }}` in the YAML body must be escaped.
- Don't commit from remote Claude Code session without identity.yaml (observed
  2026-04-21, fixed via SessionStart hook).
- Don't append SESSION-CONTEXT — stale decisions accumulate silently.
- PostToolUse ruff --fix strips unused imports after each Edit before their usage is
  added. Fix: write usage before import (reverse edit order), or use function-local
  imports for one-off additions.

## Open questions

- Phase 4 launch: vhs install still blocking demo GIF recording.
- Should future opt-in features follow the same `when: false` + `--data` pattern,
  or prompt at copier copy? Case-by-case for now.

## Pending plans

- Phase 4 launch (outreach + demo GIF) — unblocked, awaiting vhs install for GIF.
- Tag v2.2.0 after commits land. Annotated message must include migration note for
  projects that actively use multi-host (they must answer `enable_multi_host=true`
  on `copier update`).
