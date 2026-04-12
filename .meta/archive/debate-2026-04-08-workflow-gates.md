# Debate Record — Workflow obligatoire brainstorm/spec/plan/debate

**Date:** 2026-04-08
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (Le Product Owner)
**Status:** USER DECISION NEEDED

---

## Subject

Comment structurer le workflow obligatoire dans le template metadev-protocol :
quand chaque outil s'applique (brainstorm, spec, plan, debate), comment gérer
les plans de plans (orchestration autonome), garantir qu'aucune implémentation
ne démarre sans aval explicite — même les petites — et comment les plans créés
tiennent compte des plans non-implémentés pour éviter les conflits.

Contexte critique : Claude fonce trop souvent en implémentation directe sans
demander confirmation. L'utilisateur a signalé ce problème plusieurs fois.

## Angles

- **A (Le Gardien):** Tout doit passer par un gate formel non-négociable. Aucune exception. [insider]
- **B (Le Pragmatique):** Les gates doivent être proportionnels au risque. Trop de friction tue l'adoption. [insider]
- **C (Le Product Owner):** L'utilisateur veut du contrôle sans micro-management. Maximiser la confiance, pas les checkpoints. [lone wolf]

---

## Strong arguments (survived cross-critique)

- **Approbation explicite obligatoire** — raised by A, conceded by B and C.
  Claude doit DEMANDER ("Ready to implement? OK to proceed?") et ATTENDRE
  une réponse affirmative avant tout Edit/Write. Silence != approbation.

- **Proportionnalité structurée (3 tiers)** — raised by B, conceded by A and C.
  La cérémonie doit être proportionnelle au risque. Un typo et une refonte
  architecturale ne méritent pas le même processus. Mais l'approbation
  explicite est requise dans TOUS les cas.

- **Design approval vs execution approval** — raised by C, conceded by A and B.
  Approuver le plan ≠ approuver chaque fichier. Une fois le plan validé,
  l'exécution est déterministe. Pas de micro-approbation par étape.

- **Brainstorm = idée floue uniquement** — raised by A, uncontested.
  Si la demande est claire, skip brainstorm. Si elle est vague, proposer
  /brainstorm. Si une décision est bloquée, proposer /debate.

- **Tracking des plans non-implémentés** — raised by A, conceded by B and C.
  Les plans en attente doivent être listés dans SESSION-CONTEXT.md et
  vérifiés au démarrage de session pour détecter les conflits.

## Lone wolf insights

- **Distinguer types de décision** — C a identifié que le vrai problème n'est
  pas "trop ou pas assez de checkpoints" mais "checkpoints au mauvais endroit".
  Approuver les DESIGNS (spec, plan, architecture), pas l'EXECUTION (lint,
  test, commit). Insight concédé par A ("gate is at plan approval, never
  execution approval") et B.

- **Le gate doit être dans le harness, pas dans le jugement de Claude** —
  C a bougé vers cette position après cross-critique. Une règle soft dans
  GUIDELINES ne suffit pas. Il faut une règle hard dans CLAUDE.md que Claude
  ne peut pas contourner par rationalisation.

- **Rendre le scope visible** — C propose : Claude doit toujours rendre
  transparent ce qu'il va faire ("I'll change X in Y files") avant de
  demander le go. L'utilisateur approuve un scope concret, pas une intention
  vague.

## Contested arguments (no consensus)

- **Qui catégorise le tier ?** — B for user self-assessment, C for Claude assessment + transparency, A for explicit rules
  - **For user (B):** L'utilisateur sait si c'est trivial. Respecter son jugement.
  - **For Claude (C):** L'utilisateur ne peut pas savoir si c'est trivial avant que Claude ait analysé. Claude doit évaluer et rendre transparent.
  - **For rules (A):** Ni l'utilisateur ni Claude ne devraient juger — des critères objectifs décident (ex: <5 lignes + pas de test = trivial).
  - **Why it matters:** Si Claude catégorise mal (tier 1 pour un changement complexe), il bypass le processus. Si des règles trop rigides, elles cassent sur les edge cases.

- **Audit trail vs pre-approval pour l'exécution** — C for audit trail, A for pre-approval
  - **For (C):** Post-review est asynchrone et moins coûteux. Logger chaque action avec lien vers le plan approuvé.
  - **Against (A):** Les utilisateurs ne reviewent pas après coup. Le code committé reste. L'audit trail documente l'erreur, ne la prévient pas.
  - **Why it matters:** Détermine si /orchestrate peut exécuter en autonomie totale après approbation du plan, ou s'il doit checkpointer aux décisions émergentes.

## Dismissed arguments (refuted or irrelevant)

- **"Tout doit passer par /orchestrate"** — raised by A, refined after cross-critique.
  Révisé : /orchestrate est pour le travail composé multi-étape. Les changements
  simples n'en ont pas besoin. A a concédé ce point.

- **"Approve the plan, execute deterministically"** — raised by C, partially refuted by A.
  L'exécution n'est pas toujours déterministe en travail de template. Des décisions
  émergent pendant l'implémentation. C a concédé que les décisions émergentes
  doivent remonter à l'utilisateur.

## Convergence points

- L'approbation explicite avant implémentation est non-négociable (3/3)
- Système à 3 tiers : Trivial / Standard / Complexe (3/3)
- Brainstorm uniquement quand l'idée est floue (3/3)
- Plans non-implémentés trackés dans SESSION-CONTEXT.md (3/3)
- Le gate est sur l'approbation du PLAN, pas sur chaque action d'exécution (3/3)
- La règle doit être dans CLAUDE.md (hard), pas GUIDELINES.md (soft) (3/3)
- Les décisions émergentes pendant l'exécution doivent remonter à l'utilisateur (2/3, C concédé)

## Irreducible tensions

- **Qui catégorise le tier** — règles objectives vs jugement de Claude vs auto-évaluation utilisateur. Nécessite un choix de valeur : confiance en l'AI, en l'utilisateur, ou en des règles mécaniques.

## Recommendation

**Synthèse recommandée (confidence: haute — convergence 3/3 sur les principes) :**

### Règle absolue (CLAUDE.md)
"NEVER implement without explicit user approval. Before any Edit or Write:
propose what you intend to do, ask for confirmation, wait for the user's go."

### Arbre de décision (CLAUDE.md ou GUIDELINES.md)

```
User request arrives
  │
  ├─ Idea is vague/unclear?
  │   └─ Propose /brainstorm → clarify → then re-enter tree
  │
  ├─ Hard decision with trade-offs?
  │   └─ Propose /debate → decision → then re-enter tree
  │
  ├─ Requirements need formalization?
  │   └─ Propose /spec → MoSCoW → then continue
  │
  └─ Ready to plan implementation?
      │
      ├─ Simple scope (few files, clear change)
      │   └─ State what you'll do + ask "OK to proceed?"
      │
      ├─ Standard scope (feature, refactor, bugfix)
      │   └─ Write brief plan + ask for approval
      │
      └─ Complex scope (architecture, multi-file, template/)
          └─ Write detailed plan (or /orchestrate) + ask for approval
```

### Plans de plans (/orchestrate)
- Pour le travail composé multi-étape uniquement
- L'utilisateur approuve le plan global avant exécution
- Les décisions émergentes remontent à l'utilisateur
- Chaque sous-plan vérifie les conflits avec les plans en attente

### Tracking des conflits
- Plans en attente listés dans SESSION-CONTEXT.md section "Pending plans"
- Vérification automatique au démarrage de session
- Conflit détecté → signaler à l'utilisateur avant de proposer un nouveau plan

## Decision

**USER DECISION NEEDED**

To decide, consider:
- Pour la catégorisation des tiers : préfères-tu des règles mécaniques (ex: <5 lignes = trivial), le jugement de Claude rendu transparent, ou ta propre auto-évaluation ?
- Pour les décisions émergentes pendant /orchestrate : checkpoint systématique ou seulement si ça dévie du plan ?
- L'arbre de décision ci-dessus correspond-il à ton workflow mental ?
