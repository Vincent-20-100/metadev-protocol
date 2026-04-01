# ADR-003 — Rewrite CLAUDE.md.jinja et ajout SESSION-CONTEXT.md

**Date :** 2026-04-01
**Statut :** IMPLEMENTED
**Sources :**
- `.meta/references/state-of-the-art-vibe-coding.md` (finding #1 : <200 lignes)
- `.meta/references/audit-egovault.md` (patterns #2, #3, #7)
- ADR-001 decisions #1, #2, #3, #6

---

## Probleme

Le CLAUDE.md initial du template (v1) etait fonctionnel mais :
- Pas de regles anti-LLM (les erreurs recurrentes des IA n'etaient pas adressees)
- Pas de workflow de session (l'IA ne savait pas par ou commencer)
- Pas de hierarchie documentaire (quoi prime sur quoi ?)
- Pas de SESSION-CONTEXT.md (le cockpit n'avait qu'un seul fichier)

## Decisions

### 1. CLAUDE.md < 120 lignes

**Pourquoi :**
- Boris Cherny (createur Claude Code) garde son CLAUDE.md a ~100 lignes / 2500 tokens
- Au-dela de ~200 lignes, la compliance chute significativement
- L'ancien CLAUDE.md d'EgoVault faisait 350 lignes = les regles en fin de fichier
  etaient souvent ignorees

**Resultat :** 57 lignes (profil minimal), 63 lignes (profil app).
Le detail (exemples Wrong/Right des regles G1-G13 d'EgoVault) est dans les
skills et la doc, PAS dans CLAUDE.md.

**Niveau de confiance : ELEVE** — Le sizing est documente par le createur de l'outil.
La logique est simple : plus c'est court, plus c'est lu.

### 2. Regles anti-LLM (G2, G5, G6, G13)

**Quoi :** 4 regles universelles extraites des 13 d'EgoVault, plus 2 profilables.

**Regles universelles :**
- **R4 — Docstrings WHAT pas HOW** (source : EgoVault G2) — Les LLM ont tendance
  a decrire l'implementation plutot que le contrat
- **R5 — Pas d'over-engineering** (source : EgoVault G5) — Le piege #1 des LLM :
  abstractions prematurees, factories de factories, patterns inutiles
- **R6 — Chaque except log ou re-raise** (source : EgoVault G6) — Les LLM ecrivent
  des `except: pass` silencieux par defaut
- **R7 — Commentaires chirurgicaux** (source : EgoVault G13) — Les LLM noient le code
  de commentaires evidents ("# Initialize the variable")

**Regles profilables :**
- **app :** R8 routing mince (<15 lignes) + R9 injection de dependances
- **quant :** R8 zero boucle Python (vectorisation) + R9 documenter hypotheses math
- **data :** R8 pipelines idempotents + R9 raw data immutable

**Pourquoi ces 4 et pas les 13 :**
- Budget de 120 lignes = on ne peut pas tout mettre
- G1 (noms de librairies), G4 (imports inter-couches), G7-G12 sont trop
  specifiques a l'architecture hexagonale d'EgoVault
- Les 4 choisies s'appliquent a TOUT projet Python, quel que soit le profil

**D'ou vient l'idee :** Audit EgoVault section 4, confirme par l'etat de l'art
qui dit "verification commands > style guidelines" mais les anti-patterns LLM
sont une exception — ils DOIVENT etre dans CLAUDE.md.

**Niveau de confiance : ELEVE** — Teste sur 374 tests dans EgoVault. Les 4 regles
sont les plus universelles. Le risque = en ajouter trop, pas en avoir trop peu.

### 3. Cockpit 2 fichiers (PILOT.md + SESSION-CONTEXT.md)

**Quoi :**
- `PILOT.md` = etat factuel (quoi) — tableau de statut, prochaines etapes
- `SESSION-CONTEXT.md` = contexte decisionnel (pourquoi) — decisions actives,
  pieges, questions ouvertes

**Pourquoi 2 fichiers au lieu d'1 :**
- Source : EgoVault utilise PROJECT-STATUS.md + SESSION-CONTEXT.md avec succes
- PILOT.md accumule (on ajoute des lignes au tableau)
- SESSION-CONTEXT.md est REECRIT chaque session (pas complete)
- Le rewrite force a ne garder que le contexte pertinent = pas de bloat
- Un fichier unique finit toujours par devenir un log illisible

**La regle cle : "rewrite, don't append"**
- SESSION-CONTEXT.md n'est PAS un journal
- Chaque session, on reecrit depuis zero les decisions actives
- Le raisonnement obsolete est supprime, pas commente
- Ca garde le fichier sous 50 lignes = toujours lisible

**Comment s'en servir :**
1. Debut de session : Claude lit PILOT.md (etat) + SESSION-CONTEXT.md (contexte)
2. Pendant la session : les decisions sont prises avec le contexte en tete
3. Fin de session : mettre a jour PILOT.md (nouveau statut) et REECRIRE
   SESSION-CONTEXT.md (nouveau contexte pour la prochaine session)

**Niveau de confiance : ELEVE** — Teste et valide sur EgoVault (2+ mois d'utilisation).
Le pattern "rewrite" est contre-intuitif mais c'est ce qui le rend efficace.

### 4. Workflow 5 phases

**Quoi :** Research > Plan > Implement > Test > Ship

**Pourquoi 5 et pas 7 (EgoVault en avait 7) :**
- EgoVault : BRAINSTORM > SPEC > PLAN > IMPLEMENT > TEST > AUDIT > SHIP
- BRAINSTORM et SPEC fusionnes en "Research" — un bootstrap n'a pas besoin
  de specs formelles
- AUDIT supprime — trop lourd pour un nouveau projet, pertinent pour projets matures
- L'etat de l'art confirme : "Research > Plan > Execute > Review > Ship" est
  le workflow universel

**D'ou vient l'idee :**
- EgoVault (simplifie)
- Etat de l'art finding #7 (convergence de toutes les sources)

**Niveau de confiance : MOYEN** — Le workflow est consensuel mais on ne l'a pas
teste tel quel sur un projet from scratch. EgoVault utilisait la version 7 phases.
La simplification est un pari raisonnable.

### 5. Hierarchie documentaire

**Quoi :** CLAUDE.md > `.meta/decisions/` > docstrings > commentaires inline

**Pourquoi :**
- Source : EgoVault CLAUDE.md §3 ("permanent wins on conflict")
- Quand Claude trouve une contradiction entre CLAUDE.md et un commentaire
  dans le code, il doit savoir quoi suivre
- `.meta/` est provisoire (workspace IA), `docs/` est permanent

**Niveau de confiance : ELEVE** — C'est une convention de bon sens. Le risque
est negligeable.

---

## Fichiers impactes

| Fichier | Action |
|---------|--------|
| `template/CLAUDE.md.jinja` | REECRIT — v2 avec regles, workflow, hierarchie |
| `template/.meta/PILOT.md.jinja` | MIS A JOUR — workflow 5 phases ajoute |
| `template/.meta/SESSION-CONTEXT.md.jinja` | CREE — cockpit decisionnel |
