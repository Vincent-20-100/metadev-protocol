---
enforcement: hard-block
hooks: [H001, H002, H014, H016]
---

> **Enforcement:** hard-block (except E501 → advisory) — ruff pre-commit + CI fail on violation.

# Linting conventions

## Active ruff ruleset

The project enforces these ruff rule categories (see `pyproject.toml`):

- `E` — pycodestyle errors (except `E501` line-length, see below)
- `F` — Pyflakes (unused imports, undefined names)
- `W` — pycodestyle warnings
- `I` — isort (import sorting)
- `N` — pep8-naming
- `UP` — pyupgrade (modern Python syntax)
- `B` — flake8-bugbear (likely bugs)
- `SIM` — flake8-simplify (code simplification)

## Line length policy

- **`line-length = 100`** — project default. Applied by `ruff format` as a wrap target.
- **`E501` is ignored globally** — line-length is a formatter target, not a hard-block. Rationale: DX. A line at 102 chars should not fail your commit; the formatter handles wrapping what it can.
- **Semantic rules stay hard-block** — `F`, `W`, `B`, `SIM`, etc. are real bugs or refactor signals.

### Why 100 and not 79 / 88 / 80?

- PEP 8 recommends 79 (historical, terminal-width constraint).
- Black's default is 88 (reference: https://black.readthedocs.io/).
- Google Python Style Guide specifies 80 (reference: https://google.github.io/styleguide/pyguide.html#32-line-length).

100 is a **deliberate project deviation**, chosen for:
- CLI error messages and `argparse` help strings that read poorly when wrapped.
- Modern monitors and side-by-side diff views tolerate wider lines.

This is a trade-off, not an alignment with any canonical guide.

## `# noqa` policy

Per-line `# noqa: <rule>` suppressions are **discouraged** and require a 1-line comment justifying the exception, e.g.:

```python
# noqa: N806 — vendor API uses PascalCase, we mirror their naming.
MyVendorObject = vendor.get()
```

Bare `# noqa` (no rule code) is **forbidden**. Always be specific.

## Formatter

`ruff format` is the canonical formatter (Black-compatible). Configuration:

```toml
[tool.ruff.format]
quote-style = "double"
```

Run before committing: `uv run ruff format .`. The pre-commit hook enforces.

## Related

- Docstring length: PEP 257 sets no explicit maximum (https://peps.python.org/pep-0257/). Keep summary lines readable; break prose paragraphs where natural.
- Naming: see `code-style.md`.
- Imports: handled automatically by the `I` ruleset.
