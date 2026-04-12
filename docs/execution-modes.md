# Execution Modes

At `copier copy` time you pick one of two Claude Code permission presets
via the `execution_mode` parameter:

| Mode | Use case | `permissions.allow` | `permissions.ask` |
|------|----------|---------------------|-------------------|
| **`safe`** (default) | Interactive dev, public forks, new users | `src/`, `tests/`, `.meta/`, `docs/` writes; `uv`, `git` (read/commit), `pytest`, `ruff`, `pre-commit`, `copier` | Touches to `pyproject.toml`, `CLAUDE.md`, `README.md`, `.claude/`, `.github/`, `git push`, `rm`, `mv`, `mkdir` |
| **`full-auto`** | Unsupervised runs (VPS, overnight spec execution) | Everything | Empty |

The `permissions.deny` safety net is **identical** in both modes and
covers the non-negotiable catastrophes: `rm -rf`, `sudo`, `dd`, `mkfs`,
`chmod -R 777`, `curl|sh`, `wget|sh`, `.env*`, `.git/**`, `~/.ssh`,
`~/.aws`, `~/.gnupg`, `~/.pypirc`, `~/.netrc`.

> [!WARNING]
> **Full-auto warning.** Use `full-auto` only on environments where
> you accept that the AI can modify any file in the project without
> prompting. Never use it on a machine that holds production credentials
> outside the deny list, and never on a shared workstation.

## Switching modes after generation

Two options:

1. Edit `.claude/settings.json` directly — it is plain JSON, nothing
   stops you from moving entries between `allow`, `ask`, and `deny`.
2. Re-run `copier update` with a different answer — copier will surface
   the diff; accept or reject it as you would any other template update.

Pair this with the `CLAUDE.md` rule *"Plan validated = all actions
validated"* (automatism #4) and a validated plan runs end-to-end
without mid-execution friction.
