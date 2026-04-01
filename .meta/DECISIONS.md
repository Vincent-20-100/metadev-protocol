# DECISIONS.md — Journal des décisions

> Toutes les décisions structurantes, y compris les alternatives rejetées.
> Format : date — décision — contexte — alternatives rejetées
>
> Les ADRs en cours de maturation sont dans `.meta/decisions/` avant d'atterrir ici.

---

## 2026-04-01 — Nom du projet : `metadev-protocol`

**Décision :** Nom de repo `metadev-protocol`, concept nommé "The Meta Protocol".

**Contexte :** Tension entre `pilot-protocol`, `meta-protocol`, `metadev-protocol`.
"Meta" seul risquait la confusion avec Meta (Facebook) dans les recherches Google.
"Pilot" était trop spécifique au pattern `.meta/PILOT.md`.

**Rejeté :** `pilot-protocol` (trop narrow), `meta-protocol` (collision possible).

---

## 2026-04-01 — `copier` plutôt que branches orphelines

**Décision :** Système de templating via `copier` + `copier.yml`.

**Contexte :** Première idée explorée avec Gemini = branches orphelines Git
(`template/quant`, `template/app`). Abandonné en cours de conversation.

**Pourquoi les branches orphelines ont été rejetées :**
- Toute amélioration d'un hook commun = cherry-pick sur N branches
- `git archive` pour extraire est fragile et non-standard
- Pas de mécanisme de mise à jour des projets déjà générés

**Avantage décisif de `copier` :** `copier update` permet de propager
les évolutions du template vers les projets existants — critique pour la maintenabilité long terme.

---

## 2026-04-01 — `pre-commit` plutôt que `lefthook`

**Décision :** `pre-commit` (Python ecosystem) pour les git hooks.

**Contexte :** Gemini suggérait `lefthook` (binaire Go). Les deux font le job.

**Rejeté :** `lefthook` — ajoute une dépendance binaire non-Python dans un stack Python-only.
`pre-commit` s'installe via uv, cohérent avec le reste du stack.

---

## 2026-04-01 — `.meta/scratch/` gitignored, reste de `.meta/` versionné

**Décision :** Gitignore sélectif sur `.meta/`.

**Contexte :** Tension entre "garder la mémoire de session" et "ne pas polluer l'historique git".

**Solution :** Séparer les brouillons éphémères (`scratch/`) des artefacts de valeur
(`PILOT.md`, `sessions/`, `decisions/`). `PILOT.md` versionné = contexte récupérable
après un `git clone` ou un changement de machine.

---

## 2026-04-01 — 4 profils `copier.yml` (pas 3, pas 10)

**Décision :** `minimal`, `app`, `data`, `quant`.

**Contexte :** Discussion sur la granularité des profils. Risque de sur-spécifier
(un profil par framework) vs sous-spécifier (tout dans minimal).

**Ligne directrice adoptée :** Un profil = une catégorie de garde-fous pertinents.
Les divergences techniques internes à un profil (FastAPI vs Django) sont gérées
dans le `CLAUDE.md` du projet, pas dans le template.
