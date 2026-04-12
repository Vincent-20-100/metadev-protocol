---
type: spec
date: 2026-04-12
slug: public-safety
status: active
---

# Spec — Pre-public safety audit (P2)

**Context:** metadev-protocol is about to be published. Before flipping from private to public (and afterwards, permanently), we need mechanical guarantees that no secret, credential, or accidentally-tracked sensitive file lands in the public history. GitHub does not expose a "before visibility change" hook, so the defense is distributed across four contact points that together make risky public transitions mechanically hard.

## Problem

- No pre-visibility hook on GitHub. `gh repo edit --visibility public` flips instantly.
- Manual review is unreliable — one forgotten `.env.local` in a forgotten branch is enough to leak credentials permanently.
- Template users will hit the same problem. metadev-protocol must ship the defense by default so every generated project inherits it.

## Goal

Ship a single Python audit script (`scripts/audit_public_safety.py`) plus four integration points that reuse it:

1. **Local manual run** — full audit, on demand
2. **Pre-commit hook** — quick secret scan on staged files
3. **GitHub Action on push/PR to `main`** — full audit, gates merges via branch protection
4. **GitHub Action on `public` event** — reactive audit, opens a critical issue if violations detected

Propagate everything to the template so generated projects inherit identical defenses.

## Non-goals

- **Not a replacement for GitHub Secret Scanning** — we document how to enable GitHub's native push protection in the README as a complementary layer (catches known token formats from 200+ providers; our script catches custom patterns + structural issues).
- **No branch protection automation** — branch protection rules are configured via API call, not via a file in the repo. Documented as a copy-paste `gh` command in the README.
- **No full history scan** — script audits the current tree (`HEAD`), not every past commit. Rewriting history is out of scope for P2 (covered by Phase 3 task 3.1 — orphan branch → `v1.0.0`).
- **No test suite for the audit script** — deferred to post-v1.0.0 backlog.

## The three checks

### Check A — Sensitive files tracked

Use `git ls-files` to enumerate tracked files. Match against a denylist of filename patterns:

```
.env                    .env.*
*.pem                   *.key
*.p12                   *.pfx
id_rsa*                 id_ed25519*
id_ecdsa*               id_dsa*
.npmrc                  .pypirc
.netrc                  credentials*
secrets*                *.sqlite
*.sqlite3               *.db
*.kdbx                  service-account*.json
```

Any match → violation (exit 1).

### Check B — `.gitignore` coverage

For each of these canonical paths, verify `git check-ignore --no-index` reports them as ignored:

```
.env                    .env.local
.env.production         __pycache__/x.pyc
.venv/lib               venv/lib
*.pyc                   .DS_Store
.idea/workspace.xml     .vscode/settings.json
dist/x                  build/x
*.egg-info/x            .coverage
.pytest_cache/x         .ruff_cache/x
node_modules/x          .mypy_cache/x
```

Any path NOT ignored by current `.gitignore` → violation.

Rationale for `git check-ignore` over "read `.gitignore` and grep for patterns" — the former handles `!` re-inclusion rules, nested `.gitignore` files, and `core.excludesfile` correctly. The latter is fragile.

### Check C — Secret patterns in tracked content

Walk tracked files (excluding binaries via null-byte detection, excluding the audit script itself to avoid self-match, excluding the entire `.meta/` tree because specs, plans, debates, and references legitimately discuss secret shapes in explanatory text).

Scan each file's content against these regex patterns:

| Pattern | Matches |
|---|---|
| `sk-[a-zA-Z0-9]{20,}` | OpenAI API keys |
| `ghp_[a-zA-Z0-9]{36}` | GitHub personal access tokens |
| `gho_[a-zA-Z0-9]{36}` | GitHub OAuth tokens |
| `ghs_[a-zA-Z0-9]{36}` | GitHub server tokens |
| `ghu_[a-zA-Z0-9]{36}` | GitHub user-to-server tokens |
| `ghr_[a-zA-Z0-9]{36}` | GitHub refresh tokens |
| `github_pat_[a-zA-Z0-9_]{82}` | GitHub fine-grained PATs |
| `AKIA[0-9A-Z]{16}` | AWS access key IDs |
| `ASIA[0-9A-Z]{16}` | AWS temporary access keys |
| `AIza[0-9A-Za-z\-_]{35}` | Google API keys |
| `ya29\.[0-9A-Za-z\-_]+` | Google OAuth access tokens |
| `"type":\s*"service_account"` | Google service-account JSON |
| `xox[baprs]-[a-zA-Z0-9\-]{10,}` | Slack tokens (bot/user/app/refresh/webhook) |
| `https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+` | Slack webhooks |
| `sk_live_[0-9a-zA-Z]{24,}` | Stripe secret live keys |
| `rk_live_[0-9a-zA-Z]{24,}` | Stripe restricted live keys |
| `pk_live_[0-9a-zA-Z]{24,}` | Stripe publishable live keys |
| `SG\.[a-zA-Z0-9_\-]{22}\.[a-zA-Z0-9_\-]{43}` | SendGrid API keys |
| `key-[a-z0-9]{32}` | Mailgun API keys |
| `AC[a-f0-9]{32}` | Twilio Account SIDs |
| `SK[a-f0-9]{32}` | Twilio API keys |
| `dop_v1_[a-f0-9]{64}` | DigitalOcean personal tokens |
| `doo_v1_[a-f0-9]{64}` | DigitalOcean OAuth tokens |
| `dor_v1_[a-f0-9]{64}` | DigitalOcean refresh tokens |
| `npm_[a-zA-Z0-9]{36}` | npm access tokens |
| `glpat-[a-zA-Z0-9\-_]{20}` | GitLab personal access tokens |
| `[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}` | Discord bot tokens |
| `\d{9,10}:[a-zA-Z0-9_-]{35}` | Telegram bot tokens |
| `eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+` | JSON Web Tokens |
| `-----BEGIN (RSA \|EC \|DSA \|OPENSSH )?PRIVATE KEY-----` | SSH/TLS private keys |
| `-----BEGIN PGP PRIVATE KEY [BLOCK]-----` | PGP private keys |
| `(?i)bearer\s+[a-zA-Z0-9_\-\.=]{20,}` | Bearer auth tokens |
| `(?i)(api[_-]?key\|access[_-]?token\|secret[_-]?key\|auth[_-]?token\|client[_-]?secret)["':\s=]+["']?[a-zA-Z0-9_\-]{20,}` | Generic named secrets in assignments |
| `postgres(ql)?://[^:\s]+:[^@\s]+@` | Postgres URIs with credentials |
| `mongodb(\+srv)?://[^:\s]+:[^@\s]+@` | MongoDB URIs with credentials |
| `mysql:// [^:\s]+:[^@\s]+@` | MySQL URIs with credentials |
| `redis:// [^:\s]*:[^@\s]+@` | Redis URIs with credentials |
| `amqps?://[^:\s]+:[^@\s]+@` | AMQP URIs with credentials |

Any match → violation, report file + line number (but NEVER print the matched content — print a placeholder like `<REDACTED>` to avoid propagating the secret into CI logs).

## Script CLI

```
uv run python scripts/audit_public_safety.py [--mode=full|quick] [FILE ...]
```

| Mode | Scope | Checks | Use |
|---|---|---|---|
| `full` (default) | Entire tracked tree | A, B, C | Manual + CI |
| `quick` | Files passed as args (pre-commit gives staged files) | C only (secret scan) | Pre-commit hook |

Exit codes:
- `0` — clean
- `1` — violations found (one or more checks failed)
- `2` — usage error

Output format:
- Structured sections per check
- Colored in TTY (ANSI), plain in non-TTY (CI)
- Secrets never printed verbatim — always `<REDACTED>` with file + line

## Four integration points

### 1. Local manual run

Just the script. Documented in README:

```bash
uv run python scripts/audit_public_safety.py
```

### 2. Pre-commit hook (both meta-repo and template)

New hook in `.pre-commit-config.yaml` and `template/.pre-commit-config.yaml`:

```yaml
- id: audit-public-safety-quick
  name: Quick secret scan on staged files
  entry: python scripts/audit_public_safety.py --mode=quick
  language: system
  pass_filenames: true
```

Runs on every commit. Fast (only scans staged files for secret patterns).

### 3. GitHub Action — `public-safety.yml`

`.github/workflows/public-safety.yml` (meta-repo) and `template/.github/workflows/public-safety.yml` (template, plain file, no jinja):

```yaml
name: Public safety audit
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run python scripts/audit_public_safety.py --mode=full
```

Combined with branch protection (documented in README), this gates all merges to `main`.

### 4. GitHub Action — `public-alert.yml`

`.github/workflows/public-alert.yml` (meta-repo) and `template/.github/workflows/public-alert.yml` (template):

```yaml
name: Public visibility alert
on:
  public:
jobs:
  alert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - id: audit
        continue-on-error: true
        run: uv run python scripts/audit_public_safety.py --mode=full
      - if: steps.audit.outcome == 'failure'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '[CRITICAL] Public visibility audit failed',
              body: `The repository just transitioned to public visibility, but the safety audit detected violations.\n\n**Action required:**\n1. Review the failing workflow run above\n2. Consider reverting to private: \`gh repo edit --visibility private\`\n3. Remediate before re-publishing`,
              labels: ['critical', 'security']
            })
```

## README documentation

Add a new section "Before going public" in the meta-repo README covering:

1. The four contact points (brief)
2. How to run the audit manually (`uv run python scripts/audit_public_safety.py`)
3. How to enable branch protection on `main` via `gh`:
   ```bash
   gh api -X PUT repos/:owner/:repo/branches/main/protection \
     -f required_status_checks[strict]=true \
     -f required_status_checks[contexts][]=audit \
     -f enforce_admins=false \
     -f required_pull_request_reviews=null \
     -f restrictions=null
   ```
4. How to enable GitHub's native Secret Scanning + Push Protection (Settings → Code security)

## Acceptance criteria

1. **AC1 — script exists** at `scripts/audit_public_safety.py`, has CLI matching spec, passes `ruff check` and `ruff format`.
2. **AC2 — check A detects** a planted test case (a file `test_leak.env` tracked in git) and exits 1.
3. **AC3 — check B detects** a missing `.env` entry in `.gitignore` when temporarily corrupted.
4. **AC4 — check C detects** a planted `AKIA<EXAMPLE>` in a test file and exits 1, reporting `<REDACTED>` not the content.
5. **AC5 — quick mode** scans only files passed as args, runs check C only.
6. **AC6 — pre-commit hook** is registered in meta-repo and template `.pre-commit-config.yaml`, runs the quick mode, rejects a commit containing a planted secret.
7. **AC7 — clean baseline** — `audit_public_safety.py --mode=full` exits 0 on the current meta-repo main branch (no pre-existing violations).
8. **AC8 — workflow files** — `.github/workflows/public-safety.yml` and `.github/workflows/public-alert.yml` are valid YAML (parseable by Python's yaml module).
9. **AC9 — template propagation** — `copier copy . /tmp/test --defaults --trust --vcs-ref=HEAD` generates a project containing the script, pre-commit hook, and both workflows.
10. **AC10 — README documents** the four contact points, the manual run, the `gh` branch protection command, and the GitHub Secret Scanning activation.
11. **AC11 — no secret leaked in output** — running the script against a file containing a known pattern must print `<REDACTED>` and never the matched text.
12. **AC12 — pre-commit green** — `uv run pre-commit run --all-files` passes on the meta-repo after implementation.

## Risks

- **Risk 1 — False positives in check C.** Regex patterns may match legitimate content (e.g., documentation examples, test fixtures, generic-named-secret regex on harmless config). Mitigation: exclude the entire `.meta/` tree and the audit script itself; allow a per-file allowlist comment (`# audit-ignore: secret-scan`) — deferred if not needed immediately.
- **Risk 2 — Check B false positives on novel project structures.** Some projects legitimately commit `.env.example` or similar. Mitigation: check B only flags the canonical paths, and `.env.example` is not in the list.
- **Risk 3 — Performance of check C on large repos.** Scanning every tracked file on every CI run could be slow. Mitigation: acceptable for metadev-protocol (tiny repo); documented as a known limitation for downstream projects; future optimization is out of scope.
- **Risk 4 — CI workflow requires uv.** `astral-sh/setup-uv@v3` is the standard action. If it breaks, fallback is `pip install` the stdlib-only dependencies (there are none — audit script is stdlib-only by design).
- **Risk 5 — `on: public` trigger subtlety.** The workflow only runs when visibility flips from private to public, not on creation of a public repo. Documented but not worked around.

## Implementation constraints

- **Stdlib only.** The audit script must not require third-party dependencies. It runs via `uv run python` but only imports from `re`, `sys`, `subprocess`, `pathlib`, `argparse`, `os`, `dataclasses`. Reason: simplicity, speed, no dependency drift in CI.
- **No network calls.** Script is 100% local — no API calls, no remote scanning.
- **Idempotent.** Running the script twice produces identical output.
- **Python 3.13+.** Same as the rest of the project.

## References

- `scripts/check_meta_naming.py` and `scripts/check_git_author.py` — precedents for the "stdlib-only local hook" shape
- `template/.pre-commit-config.yaml` — where new hook registers
- GitHub Actions `on: public` event — https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#public
- GitHub branch protection API — https://docs.github.com/en/rest/branches/branch-protection
