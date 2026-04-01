# Prompt — Audit complet pour extraction de bonnes pratiques

> Ce prompt est destiné à l'agent Claude Code du projet à auditer.
> Colle-le tel quel dans une session Claude Code ouverte dans le repo cible.

---

## Ton rôle

Tu es un **auditeur d'architecture et de méthodes de développement**. Tu ne codes rien.
Tu produis un livrable structuré : un état des lieux exhaustif de ce repo, destiné à alimenter
un système de templates (`metadev-protocol`) qui bootstrappe des projets Python assistés par IA.

## Contexte

Le repo `metadev-protocol` est un générateur de projets (via `copier`) qui produit une structure
standardisée : code source, tests, configuration IA (CLAUDE.md), cockpit de session (.meta/),
pre-commit hooks, et pyproject.toml profilé.

Ton audit va servir à **cherry-pick les meilleures pratiques** de ce projet pour les rendre
généralisables dans un template. Tout ne sera pas retenu — c'est normal.

## Ce que tu dois produire

Un seul fichier markdown structuré en **6 sections** :

### Section 1 — Architecture du repo

- Arborescence complète (2 niveaux max, annoter le rôle de chaque dossier/fichier clé)
- Patterns architecturaux utilisés (layered, hexagonal, pipeline, monolith, etc.)
- Séparation des responsabilités : où est le code métier, la config, les tests, la doc
- Points forts ET points faibles de l'organisation

### Section 2 — Stack et tooling

- Dépendances principales (avec versions) et pourquoi elles sont là
- Outils de développement : linter, formatter, type checker, test runner
- CI/CD : pipeline, étapes, checks automatiques
- Scripts / Makefile / tâches automatisées
- Gestion des dépendances (uv, pip, poetry ?)

### Section 3 — Conventions et garde-fous

- Format de commits (conventional commits ? autre ?)
- Pre-commit hooks en place (listés avec leur rôle)
- Règles de linting / formatting (config ruff, pyright, etc.)
- Stratégie de tests : couverture, organisation, patterns (fixtures, factories, mocks)
- Gestion des secrets / .env / variables d'environnement

### Section 4 — Pratiques IA / Vibe coding

- **CLAUDE.md** : contenu complet ou chemin vers le fichier si > 50 lignes
- Instructions spécifiques à l'IA : contraintes, interdictions, workflow imposé
- Existe-t-il un cockpit de session (.meta/ ou équivalent) ?
- Comment les brouillons/explorations sont-ils séparés du code validé ?
- Y a-t-il des patterns de prompt engineering intégrés au repo ?
- Comment l'IA est-elle guidée pour éviter les erreurs courantes ?

### Section 5 — Patterns remarquables

Pour chaque pattern identifié, fournir :
- **Nom** : un nom court et descriptif
- **Où** : fichier(s) concerné(s) avec chemin
- **Quoi** : description en 2-3 phrases
- **Transférable ?** : un tag parmi :
  - `TEMPLATE` — directement généralisable dans un template
  - `PROFILE:app|data|quant` — pertinent pour un profil spécifique
  - `INSPIRATION` — bonne idée mais nécessite adaptation
  - `SPECIFIC` — trop lié à ce projet, non transférable
  - `OVER-ENGINEERED` — complexité non justifiée pour un bootstrap

### Section 6 — Fichiers clés à lire

Liste des fichiers .md, configs, et modules qui contiennent l'essentiel de la
connaissance du projet. Format :

```
chemin/vers/fichier.md — Raison de le lire (1 ligne)
```

Si un fichier contient déjà tout le contexte nécessaire (bon CLAUDE.md, bonne doc),
**indique-le plutôt que de le paraphraser**. L'objectif est d'éviter un livrable de
1000+ lignes quand les fichiers sources sont déjà bien écrits.

## Contraintes

- **Pas de code** — tu audites, tu ne modifies rien
- **Pas de recommandations** — tu constates, tu ne proposes pas de fix
- **Sois factuel** — cite des fichiers, des lignes, des configs réelles
- **Si un fichier .md couvre déjà bien un sujet** — donne le chemin au lieu de paraphraser
- **Longueur cible** : 200-400 lignes. Si le repo est très bien documenté, ça peut être
  plus court (liens vers les fichiers existants)

## Format de sortie

Nomme le fichier : `audit-pour-metadev.md`
Place-le dans `.meta/scratch/` si le dossier existe, sinon à la racine du repo.

## Commence maintenant

Lis d'abord la structure du repo (`ls -laR` ou équivalent), puis CLAUDE.md s'il existe,
puis les fichiers de configuration (pyproject.toml, pre-commit, CI), puis le code source
principal. Produis le livrable d'un seul tenant.
