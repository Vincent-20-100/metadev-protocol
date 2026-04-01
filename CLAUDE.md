# CLAUDE.md — metadev-protocol

> Fichier lu automatiquement par Claude Code à chaque session. Pas besoin de le mentionner.

## Ce repo est récursif

`metadev-protocol` est un **système de templates** pour bootstrapper des projets Python assistés par IA.
Il applique la méthode pour créer la méthode. Ce que tu travailles ici deviendra le standard
de tous les projets futurs.

## Deux sphères, deux règles

| Sphère | Contenu | Règle |
|---|---|---|
| `template/` | Ce qui sera copié dans les nouveaux projets | Stable, testé, intentionnel |
| `.meta/` | Cockpit de développement de CE repo | Éphémère, brouillon, OK |

## Première action à chaque session

**Lis `.meta/PILOT.md`** — il contient l'objectif courant, l'état du projet, et les bloquants.
Ne code rien avant de l'avoir lu.

## Architecture du repo

```
metadev-protocol/
├── template/                    # Ce qui est injecté dans les nouveaux projets
│   ├── copier.yml               # Questions d'init (à la racine du template)
│   ├── CLAUDE.md.jinja          # Instructions Claude Code du projet généré
│   ├── pyproject.toml.jinja     # Dépendances par profil
│   ├── .gitignore.jinja
│   └── {{project_slug}}/
│       └── .meta/
│           ├── PILOT.md.jinja   # Cockpit de session du projet généré
│           └── scratch/.gitkeep
├── .meta/                       # Cockpit de CE repo (développement du template)
│   ├── PILOT.md                 # État de session courant → LIS EN PREMIER
│   ├── sessions/                # Historique des sessions passées
│   ├── decisions/               # ADRs en cours de maturation
│   └── scratch/                 # Brouillons — jamais committés (.gitignored)
├── docs/
│   ├── PHILOSOPHY.md            # Le pourquoi en profondeur
│   └── PATTERNS.md              # Patterns et anti-patterns documentés
├── CLAUDE.md                    # Ce fichier
├── ARCHITECTURE.md              # Décisions architecturales validées
├── DECISIONS.md                 # Journal des ADRs
├── copier.yml                   # Moteur de templating (questions d'init)
└── pyproject.toml               # Dépendances du meta-repo lui-même
```

## Règles absolues

1. **Jamais de fichiers temporaires à la racine** — tout va dans `.meta/scratch/`
2. **`template/` ne reçoit du code que s'il est validé** — tester avec `copier copy . /tmp/test-proj` avant commit
3. **Conventional Commits** — format obligatoire : `feat:`, `fix:`, `docs:`, `chore:`
4. **Modifier le template = tester le template** — tout changement dans `template/` déclenche un test local

## Stack

- Python >= 3.12
- `uv` exclusivement (pas pip, pas poetry, pas conda)
- `ruff` pour lint + format
- `copier` pour la génération de templates
- `pre-commit` pour les git hooks

## Commandes

```bash
uv sync                              # Installer les dépendances
uv run ruff check .                  # Linter
uv run ruff format .                 # Formatter
uv run pytest                        # Tests
copier copy . /tmp/test-proj --defaults   # Tester le template localement
```

## Ce que tu NE fais pas ici

- Pas de code applicatif — ce repo est de la configuration et des templates
- Pas de notebooks — mauvais signal dans un repo de standards
- Pas d'installation globale de packages — tout passe par `uv run`
