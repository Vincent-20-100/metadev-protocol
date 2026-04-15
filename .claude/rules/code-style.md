# Code style conventions

## Naming
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Private attributes: `_leading_underscore`

## Language
- All code, comments, docstrings, and commit messages in English
- Variable and function names should be self-documenting

## Docstrings
- Describe WHAT the function does, not HOW it does it
- Include parameter types and return values for public APIs
- Skip docstrings for obvious one-liners (e.g., simple property getters)

## Comments
- Explain WHY, never WHAT — the code explains the what
- Surgical: 1-2 lines max, placed above the relevant code
- No commented-out code — delete it, git remembers

## Imports
- Handled automatically by ruff (isort rules)
- Order: stdlib → third-party → local

## Error handling
- Every `except` must log or re-raise — never `except: pass`
- Use specific exception types, not bare `except Exception`
- Let unexpected errors propagate — don't catch what you can't handle
