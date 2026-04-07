---
name: lint
description: Run ruff check + format on the whole project
allowed-tools: Bash(uv *)
---

Run the full linting suite:

```bash
uv run ruff check . --fix
uv run ruff format .
```

Report:
- Number of issues found and fixed
- Any remaining issues that need manual attention
- Files modified by the formatter

## Verification

Evidence that linting is complete:
- [ ] `ruff check .` exits with 0 errors
- [ ] `ruff format --check .` confirms all files formatted
- [ ] Any auto-fixed issues are listed (user should review before committing)
