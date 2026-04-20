---
enforcement: hard-block
hooks: [H006, H026, H027, H028, H029, H030]
---

> **Enforcement:** hard-block — `scripts/audit_public_safety.py` runs at every commit (check C, quick mode) and on every CI build (full mode, A + B + C).

# Secrets & sensitive files

## Never commit

- Real credentials of any kind (API keys, tokens, passwords, SSH keys).
- Personal PII, customer data, proprietary datasets.
- `.env` files (use `.env.example` with placeholder values).
- Signed certificates, private keys (`*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`).
- Password manager exports (`*.1pif`, `*.kdbx`), browser cookie dumps.
- Local SQLite/DuckDB databases with real data (`*.sqlite`, `*.db`).

The complete denylist lives in `scripts/audit_public_safety.py` (see `SENSITIVE_FILENAME_PATTERNS`, `SECRET_PATTERNS`).

## Canonical locations

- `.env` → gitignored (template's `.gitignore` covers this). Place at project root.
- `.env.example` → committed, contains only placeholder keys and dummy values:
  ```
  ANTHROPIC_API_KEY=sk-ant-...-REPLACE-ME
  DATABASE_URL=postgres://CREDENTIALS@HOST:5432/DB
  ```
- `data/raw/` → gitignored for anything non-trivial; use a README to document what lives there locally.
- `.claude/settings.local.json` → gitignored; user-specific Claude Code settings.

## Three layers of defense

| Layer | Mode | Checks | Where |
|---|---|---|---|
| **Layer 1** | `--mode=quick FILE ...` | Check C (content patterns) on staged files | Pre-commit hook `H006` |
| **Layer 2** | `--mode=full` | Checks A + B + C on entire tracked tree | CI workflows `H026`, `H027` |
| **Layer 3** | Post-public audit | Full rescan after repo goes public | CI workflow `public-alert.yml` |

- **Check A** — filenames match `SENSITIVE_FILENAME_PATTERNS` (denylist).
- **Check B** — canonical sensitive paths present in `.gitignore`.
- **Check C** — file content matches `SECRET_PATTERNS` (regex for API keys, tokens, RSA headers).

## If a check fails at commit time

1. **Do not force-push or `--no-verify`.** The hook caught a real risk.
2. Identify the flagged file: the hook output names it.
3. Remove the sensitive content. If the file is entirely secret-y, add to `.gitignore`.
4. If it's a false positive (e.g., an example key in a doc), either:
   - Reformat the example (`<YOUR_KEY_HERE>` instead of a realistic-looking string), OR
   - File-scope exception via `audit_public_safety.py`'s allowlist (requires editing the script — don't).
5. Re-stage and re-commit.

## If a secret was already committed

- **Do not just delete in a new commit.** The secret remains in git history. Anyone with the repo can recover it.
- Rotate the credential immediately (revoke + reissue from the provider).
- Optional: scrub git history (`git filter-repo`), force-push — but only if the repo is private and contributor count is small. Otherwise accept the rotation and move on.
- Document the incident in `.meta/GUIDELINES.md` under "Anti-patterns" so future-you doesn't repeat it.

## Related

- `scripts/audit_public_safety.py` — full implementation of the 3 checks.
- `.github/workflows/public-safety.yml` / `public-alert.yml` — CI enforcement.
- ADR-002 / ADR-008 (if present in `.meta/decisions/`) — public-safety architectural decisions.
