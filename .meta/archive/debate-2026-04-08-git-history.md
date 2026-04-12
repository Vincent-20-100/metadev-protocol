# Debate Record — Git history cleanup before publication

**Date:** 2026-04-08
**Preset:** strategy
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (The Potential Adopter)
**Status:** USER DECISION NEEDED

---

## Subject

38 commits sur 92 sont signés "Claude" au lieu de Vincent — causé par un
bug de git config, pas par une collaboration intentionnelle. Le projet
ship `attribution.commit: ""` comme feature pour EMPÊCHER exactement ce
problème dans les projets générés. Comment nettoyer l'historique avant
publication ?

## Angles

- **A (Le Clean Slate):** Orphan branch + v1.0.0. Zéro baggage. [insider]
- **B (Le Préservationniste):** Rewrite history, fix author, tag v0.3.0. [insider]
- **C (L'Adopteur Potentiel):** Qu'est-ce qui inspire confiance quand on découvre un repo ? [lone wolf]

---

## Critical fact that changed the debate (Phase 2)

Le projet ship `attribution.commit: ""` dans le template settings.json
comme feature explicite pour supprimer Claude comme co-auteur. Les 38
commits "Claude" sont un BUG de git config, pas une collaboration
intentionnelle. Le projet VEND la suppression d'authorship AI comme
feature — laisser le bug dans l'historique contredit la promesse.

**Agent C a rétracté sa position "proof of concept" après cette découverte.**
Citation : "I was wrong to say AI authorship is proof of concept. These
commits are a bug, not a feature. The template is designed to suppress AI
authorship. Leaving the bug undermines the feature promise."

---

## Strong arguments (survived cross-critique)

- **Les commits Claude sont un bug, pas un feature** — convergence 3/3 après
  Phase 2. Le projet ship la suppression d'authorship AI. Laisser le bug
  = "do what I say, not what I do."

- **La fenêtre de nettoyage est maintenant** — raised by A, conceded by all.
  Zéro forks, zéro clones externes. Après publication, tout nettoyage est
  destructif. C'est le moment ou jamais.

- **Prévention obligatoire dans le template ET ce repo** — convergence 3/3.
  Ajouter un pre-commit hook qui bloque GIT_AUTHOR_NAME == "Claude" dans
  ce repo ET dans le template.

## Contested arguments

- **Orphan branch (v1.0.0) vs rewrite (v0.3.0)**
  - **For orphan (A):** respecte l'immutabilité des tags, sépare dev/produit,
    simple et réversible
  - **For rewrite (B revised):** conserve les 92 commits comme narrative,
    ne touche pas aux anciens tags, crée v0.3.0 comme nouveau point propre
  - **For v0.3.0 boundary (C revised):** pas de rewrite, juste un nouveau tag
    sur le premier commit propre — les anciens tags restent comme archive

## Dismissed arguments (refuted in Phase 2)

- **"Les commits Claude sont un proof of concept"** — raised by C in Phase 1,
  retracted in Phase 2. Réfuté par le fait que `attribution.commit: ""`
  prouve que la suppression était intentionnelle. Le bug contredit le design.

- **"L'historique est sacré"** — weakened by B's own analysis. 90% des commits
  touchent .meta/ et docs, pas template/. Le contenu de valeur est dans les
  ADRs et fichiers, pas dans les messages de commit individuels.

## Convergence points

- Les 38 commits Claude sont un bug à corriger (3/3 après Phase 2)
- Le nettoyage doit se faire AVANT publication (3/3)
- Prévention future obligatoire : pre-commit hook + git config check (3/3)
- Les anciens tags (v0.0.1-v0.2.0) ne doivent PAS être réécrits (3/3)
- Documentation de la décision dans un ADR (3/3)

## Irreducible tensions

- **Orphan branch vs rewrite** — les deux résolvent le problème mais avec
  des philosophies différentes. Orphan = "v0.x was research, v1.0.0 is product."
  Rewrite = "same project, fixed metadata." Le choix est une question de
  narrative, pas de technique.

## Recommendation

**Confidence: haute** — convergence 3/3 sur le diagnostic (bug à fixer),
divergence légère sur la méthode (orphan vs rewrite vs boundary tag).

### Option recommandée : Orphan branch → v1.0.0

1. `git checkout --orphan release` — copie l'état actuel
2. Premier commit propre signé Vincent
3. Tag v1.0.0 avec changelog complet
4. Les anciens tags v0.x restent sur l'ancien branch (archive)
5. Ajouter pre-commit hook pour bloquer GIT_AUTHOR_NAME == "Claude"
6. Documenter dans ADR-010
7. Ajouter CONTRIBUTORS.md : "Built by Vincent with Claude AI assistance"

### Pourquoi orphan plutôt que rewrite

- Respecte la règle d'immutabilité (pas de tags réécrits)
- Plus simple techniquement (1 commande vs git-filter-repo)
- Sépare proprement la phase recherche de la phase produit
- Le contenu de valeur (ADRs, décisions) est dans les fichiers, pas dans git log
- Réversible si on change d'avis

## Decision

**USER DECISION NEEDED**

1. Orphan branch (recommandé) ou rewrite history ?
2. Premier tag : v1.0.0 (clean break) ou v0.3.0 (continuité) ?
3. CONTRIBUTORS.md mentionnant Claude AI comme assistant — oui/non ?
