# ARCHITECTURE.md — metadev-protocol

> Les décisions structurantes et le raisonnement derrière chaque choix.
> Pour les décisions en cours de réflexion → voir `.meta/decisions/`

## Vision centrale

**"Sépare le produit du process."**

Un projet propre maintient deux sphères distinctes :
- **Le produit** (`src/`, `docs/`) : ce qui est livré, révisé, stable
- **Le process** (`.meta/`) : les notes de session, brouillons d'idées, contexte IA

La pollution de `src/` par du code "en cours" ou de la racine par des notes de session
est le vecteur principal de dette cognitive et d'instabilité des projets.

---

## ADR-001 : `copier` comme moteur de templating

**Statut :** Accepté  
**Date :** 2026-04-01

**Contexte :** Le repo doit générer des projets typés (minimal, app, data, quant) à partir
d'une base commune. Plusieurs approches envisagées.

**Décision :** `copier` (Python), pas de branches orphelines, pas de script shell.

**Raisonnement :**
- Les **branches orphelines** nécessitent de cherry-pick chaque amélioration vers chaque branche — une mise à jour de hook = 4 opérations manuelles. Fragile.
- Un **script shell** est non-typé, non-versionné proprement, dépendant du shell cible.
- **`copier`** est déclaratif (`copier.yml`), supporte Jinja2 pour les conditionnels, et permet surtout `copier update` pour propager les améliorations du template vers les projets existants.

**Conséquence :** Un seul template avec des blocs `{% if project_type == "quant" %}`.
Maintenabilité maximale — une seule source de vérité.

---

## ADR-002 : `.meta/` obligatoire dans chaque projet

**Statut :** Accepté  
**Date :** 2026-04-01

**Contexte :** Les sessions de vibe-coding accumulent des brouillons, notes, versions
intermédiaires qui polluent le repo.

**Décision :** Chaque projet généré contient un `.meta/` à la racine.

**Contenu :**
```
.meta/
├── PILOT.md        # État de session — versionné, mis à jour à chaque session
├── sessions/       # Archives des sessions passées — versionnées
├── decisions/      # ADRs en incubation — versionnés
└── scratch/        # Brouillons temporaires — .gitignored
```

**Règle de gitignore :**
```gitignore
# .meta/scratch est ignoré — brouillons éphémères
.meta/scratch/*
!.meta/scratch/.gitkeep

# Tout le reste de .meta est versionné
```

**Anti-pattern à éviter :** Ignorer tout `.meta/` (perte de la mémoire de session)
ou versionner `scratch/` (pollution du git log).

---

## ADR-003 : `CLAUDE.md` comme contrat de session

**Statut :** Accepté  
**Date :** 2026-04-01

**Contexte :** Claude Code lit automatiquement `CLAUDE.md` à chaque initialisation de session.
Ce fichier est le point d'entrée principal pour contextualiser l'IA.

**Décision :** `CLAUDE.md` à la racine de chaque projet généré, avec des sections standardisées.

**Sections obligatoires :**
1. Architecture du projet (arbre de dossiers)
2. Règles absolues (5 max — au-delà, elles ne sont plus lues)
3. Commandes (build, test, lint)
4. Ce que l'IA NE fait pas (aussi important que ce qu'elle fait)

**Note critique sur la doc Gemini :** Gemini indiquait que CLAUDE.md nécessite une
instruction manuelle de lecture. C'est vrai pour claude.ai (interface web). Pour **Claude Code**
(CLI), la lecture est automatique et native. Ce repo cible Claude Code.

---

## ADR-004 : 4 profils de projet dans `copier.yml`

**Statut :** Accepté  
**Date :** 2026-04-01

**Contexte :** Les besoins en garde-fous, dépendances et structure divergent fortement
entre un side-project rapide et un projet quant sérieux.

**Décision :** 4 profils — `minimal`, `app`, `data`, `quant`.

| Profil | Cas d'usage | Garde-fous | Dépendances |
|---|---|---|---|
| `minimal` | Side project, expérimentation | ruff only | stdlib + pytest |
| `app` | API, backend, web | ruff + pyright + tests | fastapi, pydantic, httpx |
| `data` | ETL, pipelines | ruff + data validation | polars, dbt, great-expectations |
| `quant` | Backtesting, modélisation | ruff + shape checks | numpy, pandas, vectorbt |

**Règle :** Le profil `minimal` ne reçoit **jamais** de dépendances lourdes.
Si un side-project grandit, on migre vers le bon profil — on n'alourdit pas le minimal.

---

## ADR-005 : `uv` exclusivement

**Statut :** Accepté  
**Date :** 2026-04-01

**Décision :** `uv` comme unique gestionnaire de packages et d'environnements.
Pas de pip direct, pas de poetry, pas de conda.

**Raisonnement :** Vitesse (Rust), lockfile natif (`uv.lock`), remplace pip + venv + virtualenv
en une seule commande, conforme au standard `pyproject.toml` PEP 517/518.

---

## Ce qui est explicitement hors scope

- **CI/CD** sur ce repo template : overhead non justifié tant que le repo ne sert qu'au solo
- **Tests automatisés du template** : `copier copy . /tmp/test --defaults` en local est suffisant
- **Multi-language** : ce template est Python-only, intentionnellement
- **Docker** dans le profil minimal : ne pas over-engineer les petits projets
