# Brainstorm — PM.14 : Multi-agent synthesis run

**Date:** 2026-04-13

---

## Decisions

- **Output format:** `synthesis/emergent-patterns.md` — narrative doc identifiant 3-5 patterns structurels émergents (signal dans quelles sources, implication pour metadev-protocol, décision recommandée). Pas de PM.xx directs en sortie — la narrative d'abord, les backlog items après lecture humaine. Rejeté : items backlog directs (force le format feature avant l'insight) ; amendments in-place (court-circuite la validation humaine).

- **Mécanisme:** Hiérarchique 2 niveaux. L1 : 4 agents parallèles, chacun lit un cluster, produit un rapport de "signaux faibles" — patterns qui semblent mineurs isolément mais récurrents dans le cluster. L2 : 1 agent lit les 7 synthèses existantes + les 4 rapports L1, cherche ce qui apparaît dans plusieurs clusters sans jamais avoir été nommé dans les synthèses. Rejeté : clustering thématique simple (perd les patterns cross-thèmes) ; agent unique séquentiel (noyade sur 23 fichiers).

- **Scope:** Raw + interim uniquement (23 fichiers). Les synthesis/ sont déjà des agrégations humaines — les passer en L1 biaiserait la détection. L2 lit les synthèses en confrontation avec les rapports L1. Rejeté : tout le corpus (re-lire les synthèses en L1 = lire une interprétation, pas la source) ; synthèses seules (perd les signaux jamais encore synthétisés).

- **Clustering L1 (4 clusters thématiques):**

  | Agent | Cluster | Fichiers |
  |-------|---------|----------|
  | L1-A | Context & memory | claude-mem-audit, context-management-patterns, claude-code-undercover-mode, session-2026-04-13-audit-agent-reach, claude-code-docs-audit |
  | L1-B | Skill design | github-skills-landscape, claude-code-hooks-skills-reference, dev-workflow-skills-patterns, feynman-audit, superpowers-and-everything-claude-code |
  | L1-C | Workflow & governance | state-of-the-art-vibe-coding, audit-egovault, sota-mcp-patterns, python-templating-best-practices, hermes-agent-nous-research |
  | L1-D | Ecosystem & signals | claude-code-ecosystem-54-resources, ecosystem-deep-dive, ecosystem-54-triage, top-repos-and-voices, watchlist, linkedin-curated-posts, claude-code-leak-analysis, claude-code-security-deepdive |

  Rejeté : cluster "orphelins" séparé pour watchlist/linkedin (L2 pondère la source, pas besoin de pré-isoler).

---

## Prompt L1 (template pour les 4 agents)

```
Tu es un agent d'analyse de sources (cluster : {NOM_CLUSTER}).

Tu reçois {N} fichiers de références brutes sur l'écosystème Claude Code / AI-assisted development.
Ton seul rôle : identifier des **signaux faibles** — des patterns qui apparaissent dans tes sources
mais qui semblent mineurs isolément.

Un signal faible est :
- Une idée qui revient dans 2+ sources sans jamais être centrale
- Un problème nommé en passant, jamais résolu
- Un pattern implicite qu'aucune source ne nomme explicitement mais que plusieurs illustrent

Ce que tu NE fais PAS :
- Résumer les sources (déjà fait dans synthesis/)
- Feature-picker (lister des fonctionnalités à copier)
- Conclure que metadev-protocol doit faire X

Format de sortie — pour chaque signal :
### Signal : {titre court}
- **Observé dans :** {fichiers}
- **Formulation brute :** {ce que les sources disent, verbatim si possible}
- **Pattern implicite :** {ce que ça suggère sans le dire}
- **Pourquoi c'est faible ici :** {pourquoi aucune source n'en fait un sujet central}

Produis 3-6 signaux. Profondeur > quantité.
```

---

## Prompt L2 (agent synthèse)

```
Tu es l'agent de synthèse d'un run multi-sources sur metadev-protocol.

Tu reçois :
1. Les 7 fichiers synthesis/ du corpus (ce que les humains ont déjà synthétisé)
2. Les rapports des 4 agents L1 (signaux faibles par cluster)

Ton rôle : trouver les **patterns émergents** — ce qui apparaît dans 2+ rapports L1
sans être présent dans les synthèses existantes.

Un pattern émergent est :
- Un signal que plusieurs clusters indépendants ont vu, sans se concerter
- Quelque chose que les synthèses humaines ont manqué ou sous-estimé
- Une tension non résolue qui traverse plusieurs domaines

Pour chaque pattern émergent identifié, structure ainsi :
### Pattern : {titre}
- **Signal dans L1-{A/B/C/D} :** {ce que l'agent L1 a vu}
- **Absent des synthèses :** {confirmer que synthesis/ n'en parle pas, ou en parle marginalement}
- **Implication pour metadev-protocol :** {ce que ça change structurellement, pas une feature}
- **Niveau de confiance :** faible / moyen / fort (selon nombre de sources convergentes)

Produis 3-5 patterns. Si un pattern est fort, dis pourquoi les synthèses l'ont raté.
Output final dans synthesis/emergent-patterns.md.
```

---

## Prérequis avant lancement

- [x] corpus raw+interim complet (23 fichiers dont claude-mem-audit + feynman-audit)
- [ ] `synthesis/emergent-patterns.md` n'existe pas encore (éviter écrasement)
- [ ] /plan à créer avant le run nocturne

---

## Open questions

- **Faut-il un agent "devil's-advocate" sur le rapport L2 ?** L2 peut converger sur des faux patterns si les clusters L1 ont tous les mêmes biais de sources. Un quatrième regard hostile serait utile mais coûteux. Décision : laisser au /plan.
- **PM.5 (provenance sidecar) — un-déférer maintenant ?** feynman le valide empiriquement (4.8k stars). Mais ça peut naître comme output naturel du run si L2 le voit comme pattern émergent. Décision : ne pas forcer, laisser le run décider.
- **Granularité du clustering L1-D** — 8 fichiers pour le cluster Ecosystem & signals, c'est le plus lourd. Si le run plante sur le contexte, scinder en L1-D1 (ecosystem profond) + L1-D2 (signaux sociaux). Décision : laisser au /plan.

---

## Next step

Run `/plan` pour découper en tâches concrètes (orchestration des agents, gestion des outputs, commit du résultat).
