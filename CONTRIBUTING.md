# Contributing

Thanks for your interest in metadev-protocol!

## Getting started

```bash
git clone https://github.com/Vincent-20-100/metadev-protocol.git
cd metadev-protocol
uv sync
uv run pre-commit install
```

## Before you code

1. **Read `.meta/PILOT.md`** for current state and roadmap.
2. **Open an issue** to discuss your proposed change before writing code.
3. **Check `.meta/decisions/`** for past architectural decisions (ADRs).

## Workflow

1. Create a branch from `main`: `git switch -c feat/your-feature`
2. Make your changes following the rules below
3. Test template generation: `copier copy . /tmp/test --defaults --trust --vcs-ref=HEAD`
4. Run checks: `uv run ruff check . && uv run ruff format --check .`
5. Run pre-commit: `uv run pre-commit run --all-files`
6. Commit with [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
7. Open a PR against `main`

## Rules

- **One commit per logical unit** — not per file, not per timer. Reviewable in <5 minutes, bisectable.
- **Template changes must be tested** — any change in `template/` requires a local generation test.
- **All template output in English** — code, docs, skills, comments.
- **No temp files at root** — WIP goes in `.meta/drafts/` (gitignored).
- **`.meta/` filename convention** — `<type>-<YYYY-MM-DD>-<slug>.md` (enforced by pre-commit hook).
- **Semver tags are immutable** — never rewrite or move a tag, always bump the version.
- **YAGNI** — no over-engineering, complexity must be justified.

## Two spheres

| Sphere | Content | Rule |
|--------|---------|------|
| `template/` | What gets copied into new projects | Stable, tested, intentional |
| `.meta/` | Development cockpit for this repo | Ephemeral, draft, OK |

## AI-assisted contributions

This project is developed with Claude Code. If you use an AI assistant:

- **You are the author.** Review and understand every line before committing.
- AI authorship is suppressed by design (`attribution.commit: ""`) and enforced by the `check_git_author` pre-commit hook.
- Never commit secrets, even fictional ones. The `audit-public-safety-quick` hook enforces this.

## Questions?

Open an issue. We'll figure it out together.
