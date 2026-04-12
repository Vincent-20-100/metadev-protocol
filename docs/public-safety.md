# Before Going Public

Four contact points defend against accidental secret leaks when transitioning a repo from private to public:

1. **Local manual run** — full audit on demand:
   ```bash
   uv run python scripts/audit_public_safety.py --mode=full
   ```
2. **Pre-commit hook** — quick secret scan on every commit (staged files only, automatic)
3. **GitHub Action on push/PR to `main`** — full audit gates merges via branch protection
4. **GitHub Action on `public` event** — reactive audit opens a critical issue if violations are detected

All four are propagated to every generated project.

## Enable branch protection on `main`

```bash
gh api -X PUT repos/OWNER/REPO/branches/main/protection \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=audit \
  -f enforce_admins=false \
  -f required_pull_request_reviews=null \
  -f restrictions=null
```

## Enable GitHub Secret Scanning

Go to **Settings > Code security and analysis** and enable:
- **Secret scanning** (detects known token formats from 200+ providers)
- **Push protection** (blocks pushes containing detected secrets)

These complement the local audit script, which catches custom patterns and structural issues.
