# Python Templating & Modern Dev Setup — Research Notes (April 2026)

## 1. Top Copier Templates for Python

### pawamoy/copier-uv (most starred)
- Generates: pyproject.toml, ruff+ty, pytest+coverage, docs (Zensical), GitHub workflows, CHANGELOG from conventional commits, all licenses
- Questions: project name, description, author name/email/username, repo provider/namespace/name, copyright holder
- Tasks via `duty` (cross-platform Python task runner): `make setup/format/check/test/release`
- Clever: dynamic versioning from git tags, Angular commit convention, `copier update` pulls template changes

### jlevy/simple-modern-uv (minimalist)
- Philosophy: "3 Ms — minimalist, modern, maintained"
- Generates: ruff, pytest+pytest-sugar, GitHub Actions CI+publish workflows
- Clever: deliberately minimal — easy to understand and extend

### Others notable
- **copier-templates/copier-python-uv** — standardized defaults for modern Python
- **vivienm/copier-python** — CLI (Typer), Rust (maturin), task runner (`just`)
- **mjun0812/python-copier-template** — uv, Docker, Claude Code, Cursor, devcontainer, GH Actions

## 2. pyproject.toml Best Practices

### PEP 735 Dependency Groups (accepted, supported)
```toml
[dependency-groups]
dev = ["ruff", "pre-commit"]
test = ["pytest", "pytest-cov", {include-group = "dev"}]
docs = ["sphinx", "sphinx-rtd-theme"]
```
- Replaces `requirements-dev.txt` and extras-as-dev-deps pattern
- `uv add --dev` writes to `dependency-groups.dev` by default
- pip 25.1+ supports `pip install --group test`
- Use `include-group` for composition (test includes coverage, etc.)

### Ruff Configuration
```toml
[tool.ruff]
line-length = 88          # default, same as Black; 120 is popular for apps
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "S", "T20", "PT", "C4", "N"]
# E=pycodestyle, F=pyflakes, I=isort, UP=pyupgrade, B=bugbear
# S=bandit, T20=print, PT=pytest-style, C4=comprehensions, N=naming

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]     # allow assert in tests

[tool.ruff.format]
quote-style = "double"
```
- Start with `["E", "F", "I"]` minimum, expand gradually
- `S` rules replace standalone Bandit for most cases

### Pytest Configuration
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --tb=short"
markers = ["slow: marks tests as slow"]
```
- Key plugins: pytest-cov, pytest-sugar, pytest-xdist (parallel)

### Build Backend Consensus (2026)
| Backend | When to use |
|---|---|
| **uv_build** | Default for new pure-Python projects (10-35x faster) |
| **hatchling** | Need build hooks, VCS versioning, plugins |
| **setuptools** | Legacy projects only |
| scikit-build-core | C/C++ extensions |
| maturin | Rust extensions |

`uv init` defaults to uv_build since July 2025. Switch to hatchling when you outgrow defaults.

## 3. src/ Layout vs Flat Layout

**Consensus: src/ layout for new projects.**

| Aspect | src/ layout | flat layout |
|---|---|---|
| Import safety | Prevents accidental import of dev code | CWD on sys.path can shadow installs |
| Test isolation | Forces install before import | Tests may pass with broken packaging |
| Complexity | Slightly deeper nesting | Simpler directory tree |
| Adoption | pyOpenSci, Poetry, most templates | NumPy/SciPy (legacy, complex builds) |

- `uv init --package` creates src/ layout
- All top copier templates use src/ layout
- pyOpenSci "strongly suggests" src/ layout

## 4. uv Advanced Features

### Workspaces (monorepo)
- Cargo-style: single `uv.lock` for multiple packages
- Define in root `pyproject.toml` with `[tool.uv.workspace]`
- Consistent dependency resolution across all members

### uv.lock
- Universal/cross-platform lockfile (unlike pip freeze output)
- Commit to VCS; use `--locked` in CI to enforce freshness
- `uv sync --locked` fails if lockfile is out of date

### uv build backend (uv_build)
- Stable since mid-2025; 10-35x faster than alternatives
- Zero-config for pure Python; supports multiple modules, namespace packages, type stubs
- Falls back to hatchling for complex needs

### Scripts
- `uv run script.py` — runs with project dependencies
- Inline script metadata: `# /// script` block for standalone scripts

## 5. Pre-commit Hooks Beyond Ruff

### Recommended Stack
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: no-commit-to-branch    # protect main

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.x
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Optional security
  - repo: https://github.com/gitleaks/gitleaks
    hooks:
      - id: gitleaks            # detect secrets/API keys
```

### Security Options
| Tool | Purpose |
|---|---|
| ruff `S` rules | Bandit-equivalent (built into ruff) |
| gitleaks | Secret/API key detection in commits |
| trufflehog | More comprehensive secret scanning |
| bandit standalone | Only if ruff S rules insufficient |

**Recommendation:** ruff `S` rules + gitleaks covers 95% of needs. Skip standalone bandit.

## 6. CI/CD — Minimal GitHub Actions

### Minimal Workflow
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v6
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}
      - run: uv sync --locked --all-extras --dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pytest
```

### Should a template include workflows?
Yes. Every top template includes `.github/workflows/`. The minimal CI workflow above is ~20 lines and universally useful. Some templates add separate jobs for lint vs test for parallel execution.

---

## Sources
- [pawamoy/copier-uv](https://github.com/pawamoy/copier-uv)
- [jlevy/simple-modern-uv](https://github.com/jlevy/simple-modern-uv)
- [PEP 735 — Dependency Groups](https://peps.python.org/pep-0735/)
- [Dependency Groups to the Rescue](https://metaist.com/blog/2025/12/dependency-groups.html)
- [pip 25.1 Dependency Groups](https://ichard26.github.io/blog/2025/04/whats-new-in-pip-25.1/)
- [Ruff Configuration](https://docs.astral.sh/ruff/configuration/)
- [uv Build Backend](https://docs.astral.sh/uv/concepts/build-backend/)
- [uv Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- [uv GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)
- [src vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [pyOpenSci Package Guide](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html)
- [Build Backends 2025](https://medium.com/@dynamicy/python-build-backends-in-2025-what-to-use-and-why-uv-build-vs-hatchling-vs-poetry-core-94dd6b92248f)
- [uv Build Backend Stable](https://pydevtools.com/blog/uv-build-backend/)
- [Pre-commit Hooks Guide 2025](https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835)
- [GitHub Actions Setup 2025](https://ber2.github.io/posts/2025_github_actions_python/)
- [Python Dev Tooling Handbook](https://pydevtools.com/handbook/tutorial/setting-up-github-actions-with-uv/)
