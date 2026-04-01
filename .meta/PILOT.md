# PILOT.md — metadev-protocol

**Date :** 2026-04-01
**Phase :** Fondation terminee — patterns P0/P1 implementes

---

## Etat du projet

| Composant | Statut | Notes |
|---|---|---|
| Repo GitHub | ✅ | `metadev-protocol` |
| `pyproject.toml` meta-repo | ✅ | Python >=3.12, copier + ruff + pre-commit |
| `.pre-commit-config.yaml` meta-repo | ✅ | ruff check + format |
| `copier.yml` | ✅ | 5 questions, _tasks: git init, profils minimal/app/data/quant |
| `template/CLAUDE.md.jinja` | ✅ v2 | 57-63 lignes, regles anti-LLM, workflow 5 phases |
| `template/pyproject.toml.jinja` | ✅ | Deps conditionnelles par profil |
| `template/.gitignore.jinja` | ✅ | |
| `template/.pre-commit-config.yaml` | ✅ | ruff hooks |
| `template/.meta/PILOT.md.jinja` | ✅ v2 | Workflow 5 phases integre |
| `template/.meta/SESSION-CONTEXT.md.jinja` | ✅ | Pattern "rewrite, don't append" |
| `template/tests/conftest.py.jinja` | ✅ | Fixture tmp_data minimale |
| Test `copier copy` (minimal + app) | ✅ | Generation fonctionnelle |
| `pre-commit install` | ✅ | Hooks actifs |
| Push to origin | ✅ | Branche claude/setup-metadev-protocol-umMBp |
| Recherche etat de l'art | ✅ | 5 fichiers dans .meta/references/ |
| Audit EgoVault | ✅ | 11 patterns classes |
| ADR-001 (patterns a integrer) | ✅ | 7 adoptes, 2 adaptes, 4 rejetes |

---

## Reste a faire (P2/P3)

| Priorite | Action | Fichier |
|----------|--------|---------|
| P2 | Config 3 niveaux pour profil app | template/config/ (conditionnel) |
| P2 | Ajouter src/{{project_slug}}/__init__.py au template | template/src/ |
| P3 | Explorer hooks Claude Code (.claude/settings.json) | template/.claude/ |
| P3 | Enrichir watchlist au fil de la veille | .meta/references/watchlist.md |

---

## Contexte pour l'IA

- Ce repo EST le template — toute modification dans `template/` doit etre testee
  avec `copier copy . /tmp/test-proj --defaults --trust -d project_name="test"` avant commit
- La philosophie : separer le produit du process via `.meta/`
- Stack : Python 3.12+, uv, ruff, copier, pre-commit
- ADR-001 dans `.meta/decisions/` contient les decisions de design validees

---

## Recap session 2026-04-01

### Infrastructure
- pyproject.toml corrige (Python >=3.12, pre-commit ajoute)
- .pre-commit-config.yaml cree (meta-repo + template)
- Template complet : pyproject.toml.jinja, .gitignore.jinja, .meta/ structure
- copier.yml corrige (choices format) + _tasks: git init
- Generation testee et fonctionnelle

### Recherche et audit
- 3 sources leak Claude Code dans .meta/references/
- Etat de l'art vibe coding (CLAUDE.md sizing, hooks, progressive disclosure)
- Posts LinkedIn curates (MCP vs Skills, 9 couches app IA)
- Audit EgoVault complet (11 patterns identifies et classes)
- ADR-001 : croisement audit + etat de l'art

### Implementation patterns (P0/P1)
- CLAUDE.md.jinja reecrit : 57-63 lignes, regles anti-LLM, workflow 5 phases, hierarchie doc
- SESSION-CONTEXT.md.jinja cree (reecrit chaque session, pas accumule)
- PILOT.md.jinja enrichi (workflow 5 phases)
- tests/conftest.py.jinja cree
- Teste sur profils minimal et app
