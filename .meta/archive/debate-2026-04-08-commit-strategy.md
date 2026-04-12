# Debate Record — Git commit strategy for AI-assisted projects

**Date:** 2026-04-08
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (The Open-Source Reviewer)
**Status:** USER DECISION NEEDED

---

## Subject

When should you commit in an AI-assisted development project? The current
practice of committing every ~5 minutes (forced by a stop-hook) pollutes
the git history. What's the right strategy — and what becomes the
recommendation for ALL projects generated from this template?

## Angles

- **A (Le Conventionnel):** 1 changement logique = 1 commit, toujours [insider]
- **B (Le Minimaliste):** 1 feature complète = 1 commit, squash le bruit [insider]
- **C (The Reviewer):** qu'est-ce qui rend un historique lisible pour un contributeur externe? [lone wolf]

---

## Strong arguments (survived cross-critique)

- **Le stop-hook 5-min est un anti-pattern** — raised by B, conceded by A and C.
  Le hook force des commits fréquents par peur de perte de données. C'est un
  problème de backup, pas de commit strategy. Solution : stash, branches, ou
  hook de rappel (pas de bloqueur).

- **Commit par unité logique complète, pas par fichier** — convergence 3/3.
  Un "feat:" qui touche 5 fichiers est UN commit. Pas 5 micro-commits.

- **Le template enseigne par l'exemple** — raised by A, reinforced by B and C.
  L'historique de ce repo DEVIENT la référence pour tous les projets générés.
  Micro-commits ici = micro-commits partout.

- **Conventional commits = semantic intent, pas granularity** — raised by B,
  conceded by A. "feat:", "fix:", "docs:" décrivent le TYPE de changement,
  pas la taille. Un feat: peut être gros.

- **Les "onion commits" sont le bon modèle** — raised by C, conceded by A.
  Chaque commit = décision + implémentation + documentation. Un layer complet
  que le revieweur peut comprendre en <5 minutes.

## Convergence points

- Le stop-hook qui force les commits fréquents doit être retiré/reconfiguré (3/3)
- Commit par unité logique complète (feature ou décision), pas par fichier/temps (3/3)
- Conventional commits format reste obligatoire (3/3)
- Le plan détermine la granularité (décomposition en amont, pas en aval) (3/3)
- L'historique git est un artefact de documentation, pas un journal de bord (3/3)

## Irreducible tensions

- **Bisectabilité vs lisibilité** — des commits plus petits aident git bisect
  mais polluent git log. Résolution : les commits doivent passer les tests
  individuellement (bisectable) tout en étant des unités logiques complètes.

## Recommendation

**Confidence: très haute** — convergence 3/3 sur tous les principes.

### Nouvelle règle pour CLAUDE.md (remplace l'approche actuelle)

```
Commit per complete logical unit:
- Each commit = one feature, one fix, or one decision (not one file)
- Must be reviewable in <5 minutes
- Must pass tests independently (bisectable)
- Conventional format: feat:, fix:, docs:, chore:, refactor:
- The plan determines commit granularity — decompose upfront, not in git
- Never commit partial work to satisfy a timer
```

### Stop-hook à modifier

Le hook actuel force un commit à chaque arrêt. Alternatives :
1. Hook de rappel (warning, pas bloqueur)
2. Auto-stash au lieu de commit forcé
3. Vérification de qualité (tests + lint) au lieu de fréquence

## Decision

**USER DECISION NEEDED**

1. Valides-tu "commit par unité logique complète" comme nouvelle règle ?
2. Comment modifier le stop-hook ? (warning, auto-stash, ou suppression ?)
