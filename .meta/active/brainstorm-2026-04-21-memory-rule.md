# Brainstorm — memory.md rule pour metadev-protocol

**Date:** 2026-04-21

## Contexte

Pattern découvert en session PBI-Distribution-Numerique : l'infrastructure documentaire
existante (PILOT + SESSION-CONTEXT + specs + ADRs) était solide mais les automatismes
de fin de session trop vagues. Après compaction de contexte, les docs étaient périmés
et auraient envoyé un fresh context sur une mauvaise piste.

Librarian confirme : tous les 3 principes candidats sont ancrés dans les refs existantes
(ADR-003, context-management.md, brainstorm skill step 5).

## Décisions

- **Problème prioritaire :** docs périmés/contradictoires (pas docs manquants) — le faux
  contexte fait plus de dégâts que le contexte absent. Conséquence : la règle n°1 est
  "supprimer l'erroné avant d'ajouter", pas "tout capturer".
  Rejeté : traiter l'exhaustivité comme priorité (rend le fichier durable mais stale).

- **Borne SESSION-CONTEXT :** ≤ 50 lignes (ADR-003, pas 100).
  La contrainte courte force le rewrite complet à chaque session — c'est ça qui empêche
  le stale. Un fichier de 100 lignes s'amende (stale s'accumule) ; un fichier de 50 lignes
  se réécrit (stale s'efface).
  Rejeté : ≤ 100 lignes (intuition terrain PBI) — plus de contexte mais rewrite complet
  devient impraticable, on amende à la place.

- **Borne PILOT :** ≤ 120 lignes (déjà établi, Boris Cherny sizing, ADR-003).
  Non remis en question.

- **Trigger compaction contexte :** milestone livré (feature done, spec validée, plan
  complété) — compact avant d'entamer la phase suivante.
  Rejeté : trigger temporel (arbitraire, compacte quand inutile).
  Rejeté : trigger subjectif "quand Claude se répète" (fragile, dépend de l'attention user).

- **Enforcement :** advisory uniquement — pas de hook.
  Cohérent avec code-style.md (langage naturel = comportement LLM, pas mécanique).
  Si la règle est claire, le LLM l'applique. Si non appliquée → problème de clarté,
  pas d'absence de hook. YAGNI.
  Rejeté : hook sur taille SESSION-CONTEXT dans save_progress_preflight.
  Rejeté : hard-block freshness check (fragile, over-engineering).

- **Périmètre :** template + meta-repo simultanément (6 fichiers).
  Dogfood principle : une règle non appliquée au meta-repo est une dette immédiate.
  Rejeté : template only (incohérence .meta/template, valeur dogfood perdue).

## Insight clé (à encoder dans la règle)

L'intuition "mémoire plus grande + compacter souvent" était partiellement correcte :
la vraie réponse c'est **compacter plus souvent** (milestone-based), pas agrandir
SESSION-CONTEXT. Les deux effets recherchés (contexte propre en session + mémoire
longue fiable) s'obtiennent par la discipline de compaction, pas par des fichiers plus
grands.

## Fichiers touchés (6)

1. `template/.claude/rules/memory.md` — nouveau fichier (règle complète)
2. `template/CLAUDE.md.jinja` — automatismes 4+5 durcis
3. `template/.meta/SESSION-CONTEXT.md.jinja` — header note ≤ 50 lignes + rewrite
4. `.claude/rules/memory.md` — meta-repo (même contenu)
5. `CLAUDE.md` — meta (automatismes 4+5)
6. `.meta/SESSION-CONTEXT.md` — rewrite avec header note

## Open questions

- Faut-il ajouter une note dans PILOT.md.jinja sur la borne ≤ 120 lignes ? (déjà
  implicite dans ADR-003, peut-être redondant)
- Format exact du header dans SESSION-CONTEXT.md.jinja : commentaire HTML
  `<!-- ≤ 50 lignes — rewrite complet, pas d'append -->` ou section dédiée ?
- Le trigger de compaction milestone : le documenter dans memory.md seulement,
  ou aussi dans CLAUDE.md comme automatisme explicite n°6 ?

## Next step

Run /spec pour formaliser les requirements, puis /plan pour les 6 fichiers.
