# Debate Record — Borne SESSION-CONTEXT : stricte (≤ 50 lignes) vs adaptative (50/80)

**Date:** 2026-04-21
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C — Solo dev terrain (praticien, pas concepteur du template)
**Status:** USER DECISION NEEDED

---

## Sujet

Règle `memory.md` pour metadev-protocol : la borne SESSION-CONTEXT doit-elle être
stricte (≤ 50 lignes hard) ou adaptative (50 lignes nominal / 80 lignes max pour
sessions denses) ?

Enjeu : protéger contre R1 (faux contexte → fresh LLM repart sur mauvaise piste)
sans sacrifier R2 (compaction LLM perd un détail technique critique).

---

## Angles

- **A (Puriste) :** la borne fixe ≤ 50 lignes est le mécanisme anti-R1 [insider]
- **B (Pragmatique) :** la borne adaptative réduit le contournement, source cachée de R1 [insider]
- **C (Terrain) :** ce qui marche vraiment pour un solo dev au quotidien [lone wolf]

---

## Arguments forts (survivé au cross-critique)

- **Rewrite (non-appending) est le vrai mécanisme anti-R1** — A, B et C convergent.
  La taille n'est pas le proxy de qualité ; c'est l'acte de réécriture qui élimine le stale.

- **Contournement (appending silencieux) est l'ennemi principal** — tous trois concèdent.
  Une règle qui génère rationnellement son propre contournement n'est pas une règle.

- **"Tri impérieux" a une valeur cognitive** (A arg 3, validé par C Phase 2) — forcer
  la sélection active à chaque session *capture* le stale que l'intention seule rate.

- **Options rejetées sacrifiées en premier sous compression** (C arg 2, concédé par B et A) —
  c'est le contenu le plus précieux pour le LLM (empêche de réinventer ce qui a déjà
  échoué). Toute règle qui le sacrifie systématiquement est contre-productive.

- **Borne adaptative sans reset périodique = pente glissante déguisée** (C Phase 2, nouveau) —
  warn + fail à 81 lignes ne résout pas le problème si l'agent est juge de sa propre
  exception en fin de session sous pression.

---

## Lone wolf insights (C) — survivé au cross-critique

- **Rewrite complet est une fiction de fin de session calme** — sessions interrompues
  par interruption, pas résolution. Borne stricte sanctionne exactement les sessions
  qui ont le plus besoin d'un bon handoff. *Pourquoi ça compte :* la règle doit être
  conçue pour le comportement observé, pas le comportement idéal.

- **Reset périodique toutes les N sessions** (émergé Phase 2) — rewrite obligatoire
  toutes les 3-5 sessions, indépendamment du volume. Préserve le "tri impérieux" de A
  sans faire de la borne volumétrique le seul levier. *Insight outsider clé : séparer
  le déclencheur de réécriture (temporel) de la contrainte de volume.*

---

## Arguments contestés (pas de consensus)

- **"50 lignes tient en format discipliné" vs "sessions denses génèrent 70 lignes légitimes"**
  - Pour (A) : avec le format "We do X because Y. Rejected: Z." = 1 ligne par décision.
    Sessions denses → fichiers satellites (.meta/active/), SESSION-CONTEXT reste navigation.
  - Contre (B, C) : les raisons du rejet perdent leur valeur extraites en satellite.
    Le contexte de rejet dépend de son contexte d'écriture. Compression à 50 = sacrifice
    du contenu le plus précieux.
  - **Pourquoi ça compte :** détermine si 50 est réaliste ou pathologique sous pression.

- **Mur mécanique (50 hard) vs alerte progressive (50/60/80)**
  - Pour mur (A) : la mécanique ne s'érode pas, l'intention oui. Mur = événement
    observable qui force l'action.
  - Pour alerte (B révisé) : borne progressive (50 nominale / 60 alerte / 80 max) +
    format strict par section = sweet spot. Mur à 50 kills les sessions denses.
  - **Pourquoi ça compte :** enforcement mécanique ou signal + discipline ?

---

## Arguments écartés (réfutés ou non applicables)

- **"Borne adaptative suffit sans reset"** (B Phase 1) — réfuté par C Phase 2 :
  warn + fail n'est pas un déclencheur de rewrite si l'agent juge lui-même l'exception.
- **"Format seul suffit, pas besoin de borne"** (C Phase 1) — réfuté par A + B :
  format sans borne crée illusion de discipline pendant que le volume enfle.
- **"Enforcement advisory suffit"** (brainstorm initial) — tous trois suggèrent un
  mécanisme plus fort (hook ou reset périodique) pour la borne ou le rewrite.

---

## Points de convergence

- Rewrite complet (non-appending) est le comportement à enforcer, pas la taille.
- Format structuré par section est nécessaire (et pas encore dans le template).
- Une soupape pour les sessions denses est légitime (désaccord sur la forme).
- Un reset périodique indépendant du volume est une idée émergente valide.
- 50 lignes reste la **cible nominale** — désaccord sur si c'est un hard ceiling.

---

## Tensions irréductibles

- **Mur vs alerte** : borne stricte force l'action, alerte progressive évite la
  compression toxique. Les deux protègent contre R1 via des mécanismes différents.
  Choix = jugement de valeur sur "quel comportement pathologique est le moins pire :
  contournement silencieux ou compression toxique ?"

- **Session dense = exception ou cas nominal ?** Si sessions denses sont rares → borne
  stricte OK. Si elles sont fréquentes (projets complexes, debugging) → borne stricte
  pathologique. Réponse dépend du profil du projet cible.

---

## Recommandation (orchestrateur)

Les 3 agents ont convergé sur un framework que **aucun n'avait au départ** :

**Borne nominale 50 lignes + format structuré par section + soupape segmentation + reset périodique**

Détail :
1. **Format strict par section** (émergé Phase 2, consensus) — sections nommées avec
   budget indicatif. C'est le mécanisme primaire de discipline.
2. **50 lignes cible nominale** — non comme hard block, mais comme signal d'alerte
   intégré dans le format ("si tu dépasses, tu dois justifier ou segmenter").
3. **Soupape de segmentation** (évolution A) — session dense → créer
   `.meta/active/session-YYYY-MM-DD-slug.md`, référencer depuis SESSION-CONTEXT.
   SESSION-CONTEXT reste < 50 lignes même pour sessions complexes.
4. **Reset périodique** (insight C Phase 2) — rewrite complet obligatoire toutes les
   3-5 sessions, indépendamment du volume. Sépare le déclencheur de réécriture du
   signal volumétrique.

Ce framework résout la tension irréductible : il préserve le "tri impérieux" (A) sans
tuer les sessions denses (B, C), et force la réécriture via cadence temporelle plutôt
que borne volumétrique seule.

**Confiance :** MEDIUM-HIGH — les 3 agents ont convergé sur les composantes, mais la
borne (50 hard vs 50 nominale) reste un jugement de valeur non tranché.

---

## Décision

**USER DECISION NEEDED**

Pour décider, considère :

1. **50 hard ceiling ou 50 cible nominale ?** La différence pratique : avec hard ceiling,
   une session à 53 lignes ne peut pas commiter sans supprimer 3 lignes. Avec cible
   nominale, elle peut commiter en "zone alerte" sans bloquer.

2. **Le reset périodique (toutes les N sessions) : N=3 ou N=5 ?** N=3 = discipline
   forte, overhead fréquent. N=5 = discipline plus souple, plus réaliste sur projets
   longs.

3. **Format strict par section : dans `memory.md` seulement ou aussi dans le template
   `SESSION-CONTEXT.md.jinja` ?** (impact sur tous les projets générés)
