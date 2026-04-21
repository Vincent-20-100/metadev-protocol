---
enforcement: hard-block
hooks: [H008, H031]
applies_when: enable_multi_host == true
---

> **Enforcement:** hard-block when multi-host is opted in — `scripts/sync_hosts.py` regenerates stubs, pre-commit hook `H008` verifies they are up to date, CI workflow `H031` double-checks.

> **Note:** This rule applies only in projects generated with `--data enable_multi_host=true`. In Claude-only projects (the default), the rule is inert — `sync-config.yaml`, `AGENTS.md`, `GEMINI.md`, and `scripts/sync_hosts.py` are absent. The rule file itself ships unconditionally so that a project opting into multi-host mid-life has the doctrine already present (per debate D4, 2026-04-20: avoid silent Jinja-gated rules). See ADR-012 for the distinction between **rule files** (ship unconditionally) and **feature artifacts** (opt-in).

# Multi-host agent coordination

## Source of truth

`sync-config.yaml` at the project root is the **single source of truth** for multi-host agent settings (Claude Code, Codex, Gemini, etc.).

## Generated stubs (never edit directly)

The following files are auto-generated from `sync-config.yaml` by `scripts/sync_hosts.py`:

- `AGENTS.md` — Codex / OpenAI agents directive.
- `GEMINI.md` — Gemini CLI directive.
- Additional host-specific stubs declared in `sync-config.yaml`.

Each stub starts with a warning header: "⚠ Generated from sync-config.yaml — do not edit directly."

## Workflow

1. Edit `sync-config.yaml`.
2. Run `python scripts/sync_hosts.py` (or `uv run python scripts/sync_hosts.py`).
3. Commit `sync-config.yaml` **and** the regenerated stubs together.

Pre-commit hook `H008` refuses the commit if stubs are out of sync with `sync-config.yaml`.

## Common failure modes

- **Editing the stub directly** — your edit gets overwritten on the next sync. The hook rejects the commit to catch this early.
- **Forgetting to regenerate** — you modified `sync-config.yaml` but committed only that file. Hook catches the drift.
- **Partial host coverage** — adding a new host in `sync-config.yaml` but not regenerating. Hook catches missing stubs.

## Related

- `sync-config.yaml` — schema and field documentation in the file's header comments.
- `scripts/sync_hosts.py --help` — CLI options (dry-run, verbose).
- ADR-011 (if present in `.meta/decisions/`) — architectural rationale for multi-host.
