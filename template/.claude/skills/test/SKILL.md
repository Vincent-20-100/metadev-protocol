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

## Verification

Evidence that testing is complete:
- [ ] Test command ran without import errors or collection failures
- [ ] All failures are explained (not just listed)
- [ ] If tests were added: they test behavior, not implementation

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "The code works, I checked manually" | Manual checks don't persist. Tests do. |
| "I'll add tests after the feature is done" | You won't. And if you do, they'll test what you built, not what you should have built. |
| "This is too simple to test" | Simple code that breaks silently is worse than complex code that fails loudly. |
