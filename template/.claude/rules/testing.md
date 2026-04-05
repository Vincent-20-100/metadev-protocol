# Testing conventions

## Structure
- Test files mirror `src/` layout: `src/pkg/module.py` → `tests/test_module.py`
- Shared fixtures go in `tests/conftest.py`
- One test function per behavior, not per method

## Naming
- Files: `test_<module>.py`
- Functions: `test_<behavior>_<scenario>` (e.g., `test_search_returns_empty_when_no_match`)
- No class-based tests unless grouping related scenarios

## Fixtures
- Use `tmp_path` for file operations (built-in pytest fixture)
- Use `conftest.py` fixtures for shared setup
- Mock external services (APIs, databases) — never call real services in tests

## Running
- Full suite: `uv run pytest`
- Single file: `uv run pytest tests/test_module.py`
- Single test: `uv run pytest tests/test_module.py::test_name`
- Verbose: `uv run pytest -v`

## Before committing
- All tests must pass: `uv run pytest`
- New code should have corresponding tests
- Failing test = don't commit (fix or mark with `@pytest.mark.skip(reason="...")`)
