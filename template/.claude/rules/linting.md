---
enforcement: hard-block
hooks: [H001, H002, H014, H016]
---

> **Enforcement:** hard-block on `src/` (E501 active), advisory on `scripts/` and `tests/` (per-file-ignores) — ruff pre-commit + CI fail on violation in `src/`.

# Linting conventions

## Active ruff ruleset

The project enforces these ruff rule categories (see `pyproject.toml`):

- `E` — pycodestyle errors
- `F` — Pyflakes (unused imports, undefined names)
- `W` — pycodestyle warnings
- `I` — isort (import sorting)
- `N` — pep8-naming
- `UP` — pyupgrade (modern Python syntax)
- `B` — flake8-bugbear (likely bugs)
- `SIM` — flake8-simplify (code simplification)

## Line length policy

- **`line-length = 100`** — project default. Applied by `ruff format` as a wrap target.
- **`E501` active on `src/`, ignored on `scripts/` and `tests/`** (via `per-file-ignores`).
  - On `src/` the rule stays hard-block: line-length is a **complexity proxy** — a 150-char line in application code usually signals a function doing too much.
  - On `scripts/` and `tests/` the rule is advisory: CLI help strings, error messages, and test fixtures read better unwrapped.
- **Semantic rules stay hard-block everywhere** — `F`, `W`, `B`, `SIM`, etc. are real bugs or refactor signals regardless of directory.

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
