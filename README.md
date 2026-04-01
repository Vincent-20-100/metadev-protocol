# metadev-protocol

Systeme de templates pour bootstrapper des projets Python assistes par IA.

## Ce que ca fait

Une commande, un projet pret pour Claude Code :

```bash
copier copy gh:vincent-20-100/metadev-protocol mon-projet --trust
```

Tu reponds a 5 questions (nom, type, auteur, python version) et tu obtiens :

- **CLAUDE.md** — instructions IA calibrees (<60 lignes, regles anti-LLM)
- **`.meta/`** — cockpit de session (PILOT.md + SESSION-CONTEXT.md)
- **`.claude/`** — hooks auto-ruff, permissions, skill `/test`
- **pyproject.toml** — dependances par profil, pret pour `uv sync`
- **pre-commit** — ruff check + format automatique
- **tests/** — conftest.py avec fixtures de base

## Profils disponibles

| Profil | Dependances | Regles specifiques |
|--------|------------|-------------------|
| **minimal** | pytest, ruff, pre-commit | Regles universelles uniquement |
| **app** | + fastapi, uvicorn, pyright | Routing mince, injection de dependances |
| **data** | + polars, duckdb | Pipelines idempotents, raw data immutable |
| **quant** | + numpy, pandas, matplotlib | Vectorisation, documenter les hypotheses math |

## Installation

```bash
# Installer uv (si pas deja fait)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Generer un projet
copier copy gh:vincent-20-100/metadev-protocol mon-projet --trust

# Setup
cd mon-projet
uv sync
uv run pre-commit install

# Lancer Claude Code
claude
```

## Ce qui est genere

```
mon-projet/
├── CLAUDE.md                  # Instructions IA (<60 lignes)
├── pyproject.toml             # Deps par profil
├── .pre-commit-config.yaml    # ruff check + format
├── .gitignore
├── tests/
│   ├── __init__.py
│   └── conftest.py            # Fixtures partagees
├── .claude/
│   ├── settings.json          # Permissions + hooks
│   └── skills/test/SKILL.md   # Skill /test (pytest)
└── .meta/
    ├── PILOT.md               # Etat du projet
    ├── SESSION-CONTEXT.md     # Contexte decisionnel (reecrit chaque session)
    ├── decisions/             # ADRs
    ├── sessions/              # Historique
    └── scratch/               # Brouillons (gitignored)
```

## Philosophie

**Separer le produit du process.** Le code (src/, tests/) est le livrable. Le cockpit (.meta/) est l'espace de travail IA. Les deux ne se melangent jamais.

**Hooks > instructions.** Les regles critiques (formatting, lint) sont des hooks automatiques, pas des lignes dans CLAUDE.md que l'IA peut ignorer.

**Progressive disclosure.** CLAUDE.md est court et toujours charge. Les skills sont chargees a la demande. Le contexte est preserve apres compaction.

## Stack

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) — gestion deps et venv
- [ruff](https://github.com/astral-sh/ruff) — lint + format
- [copier](https://github.com/copier-org/copier) — generation de templates
- [pre-commit](https://pre-commit.com/) — hooks git
- [Claude Code](https://claude.ai/code) — assistant IA

## Decisions architecturales

Les ADRs sont dans `.meta/decisions/` :
- **ADR-001** — Patterns selectionnes depuis EgoVault + etat de l'art
- **ADR-002** — Configuration .claude/ (permissions, hooks, skills)
- **ADR-003** — CLAUDE.md sizing, regles anti-LLM, cockpit 2 fichiers

## Developpement de ce repo

```bash
uv sync                                          # Installer les deps
uv run ruff check .                              # Lint
uv run ruff format .                             # Format
copier copy . /tmp/test --defaults --trust -d project_name="test"  # Tester le template
```
