---
enforcement: hard-block
hooks: [H013]
---

> **Enforcement:** hard-block in generated projects — pre-commit hook `no-commit-to-branch` refuses direct commits on `main`.

# Branching

## The pattern

**Create your feature branch BEFORE the first edit.** Not after. Not at commit time.

```bash
git checkout -b feat/<scope>-<short-description>
# then start editing
```

## Why AVANT and not APRÈS

If you edit first and branch later, you force yourself into a `git stash` + `git checkout -b` + `git stash pop` dance mid-context. You lose your train of thought, risk a bad stash apply, and the pre-commit hook on `main` blocks you until you resolve — exactly the friction this rule prevents.

Branching first is a ~5-second action. Skipping it costs minutes and breaks flow.

## Branch naming

Prefix by change kind:

- `feat/<slug>` — new feature
- `fix/<slug>` — bug fix
- `refactor/<slug>` — non-functional change
- `docs/<slug>` — docs-only change
- `chore/<slug>` — tooling, deps, CI

The slug is short, lowercase, hyphen-separated. 2-5 words max.

## Meta-repo vs generated projects (doctrinal clarification)

The parent `metadev-protocol` repository permits trunk-based development on `main` for solo-dev convenience (no `no-commit-to-branch` hook at that level).

**Generated projects from this template DO NOT inherit that exception.** Hook `H013` is installed by default in the template's `.pre-commit-config.yaml`, enforcing feature branches for every generated project. Rationale:

- Solo-dev trunk-based is a calculated choice for a stable, low-contributor repo.
- A generated project might have multiple contributors, CI gates, release branches — defaults should be cautious.
- You can override by removing `H013` from your project's `.pre-commit-config.yaml` if you truly want trunk-based. The template ships safe-by-default.

## Common failure modes

- **"I'll branch later"** — forget, hit the hook on commit, hasty `git reset`, lose work.
- **Commit to main directly** — blocked by `H013`. Don't try to bypass with `--no-verify` (violates the no-hook-skip rule in `CLAUDE.md`).
- **Feature branch from a stale main** — always `git pull --rebase origin main` before creating.

## Related

- `CLAUDE.md` automatism #7 — commit per logical unit.
- `CLAUDE.md` rule on hook skipping — never `--no-verify` without explicit user approval.
