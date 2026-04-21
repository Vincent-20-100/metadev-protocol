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
hooks enforce contracts (skills, secrets, naming, git author). identity.yaml drives
SessionStart git-author override in remote Claude Code sessions.

## Active decisions

- memory.md ships as advisory rule (no hook). Rejected: hook on line count.
- SESSION-CONTEXT target ≤ 50 lines nominal (not hard block). Rejected: adaptive 50/80.
- Session = milestone (commit), not Claude Code conversation.
- H004/H005 CI bypass (not CLAUDE_CODE env var conditioning): CI covers the real false-positive
  scenario (fresh clone, runner). CLAUDE_CODE var detection is added complexity without coverage gain.
- H008/H022 feature flag (sync_hosts): `if not config_exists: exit 0` — already implemented
  before PR-4-B2. Single-host projects skip silently, multi-host invariant preserved.

## Traps to avoid

- Don't commit from remote Claude Code session without identity.yaml — container
  overwrites git author with Claude (observed 2026-04-21, fixed via SessionStart hook).
- Don't append SESSION-CONTEXT — stale decisions accumulate silently.
- `uv sync --extra test` required (not just `uv sync`) to get pytest + pyyaml in venv.
- Branch `claude/prevent-scope-creep-MCwhs` was 21 commits behind main — always rebase
  before working on a long-lived feature branch.

## Open questions

- Phase 4 launch: vhs install blocking demo GIF recording.

## Pending plans

- Phase 4 launch (outreach + demo GIF) — unblocked, awaiting vhs install for GIF.
