---
name: test
description: Run the test suite and report results
allowed-tools: Bash(uv *)
---

Run the test suite for this project.

If $ARGUMENTS is provided, run only matching tests:
```bash
uv run pytest $ARGUMENTS -v
```

Otherwise run the full suite:
```bash
uv run pytest
```

Report:
- Number of tests passed/failed/skipped
- Any failures with the relevant error message
- Suggest a fix if a test fails
