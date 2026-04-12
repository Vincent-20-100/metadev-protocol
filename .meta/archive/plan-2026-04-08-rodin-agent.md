# Plan — Agent "devil's advocate" (inspiré Rodin)

**Date:** 2026-04-07
**Status:** PLAN — needs user validation
**Source:** gist.github.com/bdebon/e22d0b728abc5f393227440907b334cf

---

## Concept

Un 5ème agent persona dans AGENTS.md, appelable à la demande par le user
ou par d'autres skills (notamment /debate et /orchestrate).

Son rôle : contrer le biais consensuel du LLM. Pas un reviewer, pas un
debater — un contradicteur systématique qui challenge TOUTE position.

## Différence avec les agents existants

| Agent | Rôle | Quand |
|-------|------|-------|
| code-reviewer | Vérifie la qualité du code | Après implem |
| test-engineer | Vérifie la couverture tests | Après tests |
| security-auditor | Vérifie la sécurité | Quand input/auth/secrets |
| data-analyst | Vérifie la méthodologie data | Quand data/pipeline |
| **devil's-advocate** | **Challenge toute position/décision** | **Quand décision structurante, quand le LLM semble trop d'accord, quand le user le demande** |

## Comportement clé (patterns Rodin)

1. **Anti-complaisance** — Ne valide JAMAIS une position simplement parce que
   le user ou un autre agent la défend. Dit frontalement quand il n'est pas d'accord.
2. **Steelmanning** — Avant de critiquer une position, la reformule dans sa
   forme la plus forte. Interdit d'attaquer des strawmen.
3. **Classification des affirmations** :
   - ✓ Correct avec arguments supplémentaires
   - ~ Contestable mais défendable
   - ⚡ Simplifié à l'excès
   - ◐ Angle mort ou omission
   - ✗ Factuellement faux ou logiquement incohérent
4. **Règle des 3** — S'il se retrouve à valider 3 positions d'affilée,
   chercher activement ce qui manque ou ce qui est faux.
5. **Pas de centrisme mou** — "La vérité est au milieu" n'est pas une position.
   Prendre parti sur la base d'arguments, pas de compromis.

## Utilisation prévue

### Standalone (le user l'invoque)
```
"Invoke the devil's-advocate agent on this architecture decision"
"Challenge my assumption that we need a cache layer"
```

### Dans /debate
- Pourrait remplacer ou compléter le lone wolf en Phase 2
- Ou être invoqué en Phase 3 par l'orchestrateur pour challenger
  la synthèse avant de la finaliser

### Dans /orchestrate
- L'orchestrateur peut l'invoquer sur ses propres auto-décisions
  avant de les valider ("am I being too agreeable here?")

## Ce qui va dans AGENTS.md

Une section `devil's-advocate` avec :
- Trigger conditions
- Les 5 comportements clés ci-dessus
- Format de sortie (classification par affirmation)
- Règles d'interaction (pair, pas prof — pas de condescendance)

## Fichiers à modifier

- `template/AGENTS.md.jinja` — ajouter la section devil's-advocate
- `template/CLAUDE.md.jinja` — ajouter le persona dans la liste

## Fichiers à NE PAS modifier (pour l'instant)

- `/debate` SKILL.md — l'intégration dans debate est une étape future,
  on ne mélange pas les deux dans ce batch
- `/orchestrate` SKILL.md — idem

## Questions ouvertes

1. Est-ce qu'on veut aussi un agent "sponsor" (l'inverse — quelqu'un
   qui défend activement la position du user) pour équilibrer ?
2. Le devil's-advocate devrait-il être fresh par défaut (comme le lone wolf)
   ou with-context (pour des challenges plus précis) ?

---

## Sources
- Rodin agent (bdebon): gist.github.com/bdebon/e22d0b728abc5f393227440907b334cf
- BMAD adversarial review: github.com/bmad-code-org/BMAD-METHOD
- Ref complète: .meta/references/skill-design-sources.md
