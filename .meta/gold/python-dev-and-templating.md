# GOLD — Python Dev & Templating

> Synthese de : python-templating-best-practices.md, audit-egovault.md,
> state-of-the-art-vibe-coding.md, top-repos-and-voices.md
> Date : 2026-04-01

---

## Ce que les meilleurs templates font

### References
- **pawamoy/copier-uv** — gold standard (duty tasks, dynamic versioning, full tooling)
- **jlevy/simple-modern-uv** — reference minimaliste ("3 Ms : minimalist, modern, maintained")
- **mjun0812/python-copier-template** — inclut Claude Code + Cursor + devcontainer

---

## Decisions par composant

### 1. Layout : src/ (consensus 2026)

**Decision : src/ layout.**

Tous les top templates utilisent src/. `uv init --package` le cree par defaut.
pyOpenSci le recommande fortement.

| src/ layout | flat layout |
|---|---|
| Empeche import accidentel de code dev | CWD sur sys.path peut shadow les installs |
| Force install avant import = tests fiables | Tests peuvent passer avec packaging casse |
| Standard 2026 | Legacy (NumPy/SciPy, builds complexes) |

**Confiance : TRES ELEVEE** — Consensus unanime.

**Action :** Ajouter `template/src/{{project_slug}}/__init__.py` au template.

### 2. Build backend : uv_build

**Decision : uv_build par defaut.**

Stable depuis juillet 2025. 10-35x plus rapide que hatchling/setuptools.
`uv init` l'utilise par defaut.

**Confiance : ELEVEE** — Standard uv. Fallback hatchling si besoin de hooks.

**Action :** Deja fait dans template/pyproject.toml.jinja — MAIS on utilise hatchling.
A changer pour uv_build.

### 3. Dependency groups : PEP 735

**Decision : Utiliser `[dependency-groups]` au lieu de `[project.optional-dependencies]`.**

```toml
[dependency-groups]
dev = ["ruff>=0.11.0", "pre-commit>=4.2.0"]
test = ["pytest>=8.3.0", "pytest-cov>=6.0.0", {include-group = "dev"}]
```

- `uv add --dev` ecrit dans dependency-groups.dev par defaut
- pip 25.1+ supporte `pip install --group test`
- `include-group` pour composition (test inclut dev)

**Confiance : ELEVEE** — PEP accepte, supporte par uv et pip.

**Action :** Mettre a jour template/pyproject.toml.jinja.

### 4. Ruff config : regles recommandees

**Decision : Inclure une config ruff dans pyproject.toml.**

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
# E=pycodestyle, F=pyflakes, I=isort, UP=pyupgrade, B=bugbear

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]     # allow assert in tests
```

**Regles par tier :**

| Tier | Regles | Pourquoi |
|------|--------|----------|
| **Minimal** (tous profils) | E, F, I, UP, B | Erreurs de base, imports, upgrades, bugbear |
| **Recommande** (app) | + S, T20, N | + Bandit securite, no-print, naming |
| **Strict** (user choice) | + PT, C4, SIM | + pytest-style, comprehensions, simplify |

**Confiance : ELEVEE** — E/F/I sont universels. B attrape des bugs reels.

**Action :** Ajouter [tool.ruff] dans template/pyproject.toml.jinja.

### 5. Pytest config

**Decision : Inclure config pytest dans pyproject.toml.**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --tb=short"
```

**Confiance : TRES ELEVEE** — Standard.

**Action :** Ajouter dans template/pyproject.toml.jinja.

### 6. Pre-commit : enrichir au-dela de ruff

**Decision : Ajouter pre-commit-hooks standard + gitleaks optionnel.**

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
      - id: no-commit-to-branch  # protect main

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

**Confiance : ELEVEE** — Hooks standard, zero configuration.

**Action :** Mettre a jour template/.pre-commit-config.yaml.

### 7. CI/CD : GitHub Actions minimal

**Decision : Inclure un workflow CI minimal.**

~20 lignes : checkout, setup-uv, uv sync --locked, ruff check, ruff format --check, pytest.
Tous les top templates en incluent un.

**Confiance : ELEVEE** — Universellement utile.

**Action :** Creer template/.github/workflows/ci.yml.jinja.

### 8. Copier avance : _tasks et copier update

**Copier features qu'on utilise :**

| Feature | Status |
|---------|--------|
| `_subdirectory: template` | FAIT |
| `_tasks: git init` | FAIT |
| `_exclude` patterns | FAIT |
| `_message_after_copy` | FAIT |

**Copier features a explorer :**

| Feature | Ce que ca fait | Priorite |
|---------|---------------|----------|
| `when` key | Conditionner une question sur une reponse precedente | T3 |
| `copier update` | Tirer les mises a jour du template dans un projet existant | T3 |
| `_answers_file` | Sauvegarder les reponses pour copier update | T2 |

**Action :** Ajouter `_answers_file: .copier-answers.yml` dans copier.yml.

---

## Plan d'implementation

### Sprint dev/templating

| Priorite | Action | Impact |
|----------|--------|--------|
| **P0** | Ajouter src/{{project_slug}}/__init__.py | Structure standard |
| **P0** | Changer build backend hatchling → uv_build | Aligne avec standard uv |
| **P0** | Ajouter [tool.ruff] + [tool.pytest] dans pyproject.toml.jinja | Config outillee |
| **P1** | Enrichir .pre-commit-config.yaml (pre-commit-hooks) | Meilleurs garde-fous |
| **P1** | Creer .github/workflows/ci.yml.jinja | CI out-of-the-box |
| **P1** | Ajouter _answers_file dans copier.yml | Support copier update |
| **P2** | Dependency groups test = [{include-group = "dev"}] | Composition propre |

---

## Ce qu'on NE fait PAS

| Idee | Pourquoi non |
|------|-------------|
| Dynamic versioning (git tags) | Over-engineering pour un bootstrap |
| duty/just task runner | uv run suffit, pas besoin d'un runner additionnel |
| Sphinx/docs generation | Le template est pour bootstrapper, pas pour publier |
| Docker/devcontainer | Trop specifique, l'user l'ajoute si besoin |
| Licence picker dans copier.yml | Pas critique pour un bootstrap, ajoutable plus tard |
| Monorepo/workspaces | Hors scope template single-project |
