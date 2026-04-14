---
type: synthesis
date: 2026-04-14
slug: emergent-patterns
status: active
---

# Emergent patterns — PM.14 multi-agent synthesis run

**Date:** 2026-04-14
**Method:** 4 L1 agents (context, skill, workflow, ecosystem) → 1 L2 agent
**Sources:** 23 raw/interim files + 7 existing synthesis/ files

## Executive summary

Les quatre clusters L1 ont travaillé en isolement sur des corpus différents — contexte,
skills, workflow, écosystème — et convergent sur une même tension structurelle que les
synthèses humaines existantes n'ont jamais formulée : **les artefacts textuels qui
pilotent l'agent (CLAUDE.md, skills, mémoire, rules) sont traités comme de la
documentation alors qu'ils sont en réalité des prompts adversariaux continus, soumis à
négociation par le modèle, dégradation silencieuse, et réécriture par d'autres LLM**.
Les syntheses actuelles optimisent chaque artefact isolément (CLAUDE.md court, skills
modulaires, SESSION-CONTEXT rewrite) sans reconnaître qu'ils forment **une seule
surface de gouvernance cognitive** dont la fiabilité dépend de propriétés qui n'ont pas
de nom dans le template : classes d'accès (qui peut lire vs muter), budget de bootstrap
unifié, contrat récupérable, responsabilité éditoriale sur la compaction. Le run
révèle que metadev-protocol a implémenté la moitié haute (skills, workflow) en
supposant résolue la moitié basse (qui décide ce qui disparaît, qui voit sans muter,
qui paie le coût d'un fichier de plus).

## Patterns

### Pattern : Le rôle manquant du "lecteur privilégié sans droit de retour"

- **Signal dans L1-A :** « Le fork read-only comme forme de gouvernance cognitive »
  (autoDream « runs in a separate fork to prevent the main agent's reasoning from
  being corrupted », `/btw` « sees full context, no tool access, answer discarded »,
  claude-mem worker externe).
- **Signal dans L1-B :** « L'isolation de contexte comme antidote silencieux au biais
  d'auto-review » (Feynman parallel gather, superpowers subagent review, Claude Code
  `context: fork`). Formulé : « l'isolation n'est pas une optimisation — c'est une
  condition épistémologique ».
- **Signal dans L1-D :** « L'"auto mode" LLM-comme-gatekeeper apparaît partout sans
  être nommé comme catégorie » — race de résolveurs, classificateurs parallèles,
  skill-as-gatekeeper.
- **Absent des syntheses :** `context-management.md` mentionne le subagent pour
  « isoler les recherches verbeuses » mais uniquement comme optimisation tokens.
  `skills-workflow-and-utilities.md` parle du review en « subagent fork » strictement
  pour l'économie cache, jamais pour l'honnêteté critique. Aucune synthèse ne
  reconnaît qu'il existe une **classe d'opérations** (consolidation mémoire,
  critique, résumé, gatekeeping) qui doit voir le contexte sans pouvoir le muter ni
  laisser de trace dans l'historique parent.
- **Implication pour metadev-protocol :** Le template décrit ses subagents en termes
  de rôle fonctionnel (code-reviewer, security-auditor, devil's-advocate). Il devrait
  les décrire **aussi** en termes de classe d'accès : *lecteur-discard* (voit, répond,
  oublié), *lecteur-persist* (voit, écrit dans `.meta/`, historique propre),
  *auteur* (voit, mute, laisse trace git). Cette taxonomie manquante explique pourquoi
  la règle « devil's-advocate doit s'invoquer au 3e agrément » reste fragile : elle
  ne dit pas ce que l'agent a le droit de *lire* ni s'il doit *disparaître* ensuite.
- **Niveau de confiance :** fort (3 clusters indépendants, convergence claire).

### Pattern : La compaction/mémoire comme acte éditorial sans responsable désigné

- **Signal dans L1-A :** « La tension non-dite entre mémoire persistante et drift
  identitaire » (autoDream « converts vague insights into absolute facts », claude-mem
  compression via Claude SDK) + « Rewrite don't append est un principe plus profond
  que son énoncé » (log immuable + synthèse chaude, jamais nommés ensemble).
- **Signal dans L1-C :** « La compaction/compression comme acte éditorial déguisé en
  opération technique » — « personne ne demande : qui est responsable de ce qui
  disparaît à la compaction ? ». Vincent a l'intuition (« rewrite, don't append »)
  mais « sans cadre de responsabilité ».
- **Signal dans L1-D :** « L'écosystème sous-estime massivement ce qui sort d'une
  session » — convergence implicite sur « chaque session doit laisser une trace
  structurée récupérable » mais jamais formulé comme first-class design choice.
- **Absent des syntheses :** `context-management.md` liste les 5 stratégies de
  compaction du leak comme mécaniques techniques (« Perte : Faible / Moyenne /
  Élevée / Totale ») et propose `SESSION-CONTEXT rewrite` comme bonne pratique —
  jamais comme un acte éditorial où quelqu'un (humain ou LLM) décide ce qui mérite
  d'être gardé. Le risque que la consolidation par LLM transforme « Vincent hésitait
  sur X » en « Vincent préfère X » (hallucination mémoire) n'est mentionné dans
  aucune synthèse.
- **Implication pour metadev-protocol :** La règle « rewrite, don't append » doit
  s'accompagner d'une **couche de log froid append-only** (déjà partiellement chez
  KAIROS : daily log files) pour permettre de détecter la dérive a posteriori. Le
  template a `.meta/archive/` mais pas de log brut antécédent à la réécriture.
  Structurellement : chaque compaction devrait produire un diff auditable (ce qui a
  disparu), pas juste un nouveau fichier propre. Sans ça, `/save-progress` et
  `/consolidate` reproduisent le bug d'autoDream à petite échelle.
- **Niveau de confiance :** fort (3 clusters, tension identifiée mais non résolue
  partout). Pourquoi les syntheses humaines l'ont raté : parce que l'intuition
  « rewrite, don't append » de Vincent *a résolu le problème visible* (bloat) tout
  en créant le problème invisible (perte non-tracée). Quand une bonne pratique marche
  sur la surface, on arrête de chercher ce qu'elle cache.

### Pattern : Le budget de bootstrap est un angle mort unifié

- **Signal dans L1-A :** « La prolifération silencieuse des points d'entrée
  contextuels » — CLAUDE.md, AGENTS.md, .claude/rules/, MEMORY.md, llms.txt,
  SESSION-CONTEXT, PILOT, handoffs. « L'utilisateur qui ajoute un fichier n'a aucun
  moyen de savoir s'il sera lu, quand, avec quelle priorité ».
- **Signal dans L1-C :** « L'absence de budget de tokens/contexte dans les règles de
  gouvernance » — chiffres épars (« 150-200 instructions avant chute », « 3 MCP
  servers = sweet spot, 5 = max », « 500-1000 tokens par tool »), jamais unifiés.
  « Personne ne mesure le coût de ses propres règles. »
- **Signal dans L1-D :** « Boris Cherny et trailofbits sont en désaccord silencieux
  sur la taille du CLAUDE.md » — additif réactif (Cherny) vs figé exhaustif
  (trailofbits). Aucune des deux écoles ne compte le coût cumulé.
- **Absent des syntheses :** `context-management.md` et `vibe-coding-practices.md`
  donnent chacun une métrique isolée (`wc -l CLAUDE.md < 120`), mais aucune synthèse
  ne somme **CLAUDE.md + skills chargées + MCP tools + rules/ lazy + MEMORY.md + hooks
  output** comme un budget unique. Le template fixe des plafonds par artefact sans
  vérifier leur somme.
- **Implication pour metadev-protocol :** Il manque un script de mesure unique
  (`scripts/bootstrap_budget.py`) qui évalue le coût total en tokens de tout ce qui
  est injecté avant que l'utilisateur tape son premier prompt : CLAUDE.md + skills
  name+description (progressive disclosure charge les descriptions même non invoquées,
  cf. signal L1-B.1) + MCP tools déclarés + hooks renvoyés dans le contexte. Sans
  mesure unifiée, chaque ajout paraît gratuit et la dégradation silencieuse se
  produit au niveau du projet, pas du fichier. C'est une règle de gouvernance
  quantifiable que le CLAUDE.md du template ne possède pas aujourd'hui.
- **Niveau de confiance :** fort (3 clusters, signaux numériques précis).

### Pattern : Les artefacts textuels sont adversariaux, pas documentaires

- **Signal dans L1-B :** « La description du skill est elle-même un champ de bataille
  comportemental » (le bug « one review instead of two » causé par un résumé dans
  la description) + « Rigide vs Flexible cache une question non-posée » (la rigidité
  encode des **contre-arguments** anti-rationalisation : « Thinking 'skip TDD just
  this once'? Stop. That's rationalization. »).
- **Signal dans L1-C :** « La dégradation silencieuse des artefacts textuels qui
  pilotent l'agent » — « CLAUDE.md ~70-80% compliance », « hotfix dump qui gonfle le
  fichier », les fichiers de gouvernance se dégradent par accumulation non-auditée.
- **Signal dans L1-A :** « Rewrite don't append est un principe plus profond » — les
  fichiers de contexte souffrent de la même pression adversariale : soit on append
  (drift), soit on rewrite (qui décide ?).
- **Absent des syntheses :** `skills-workflow-and-utilities.md` et
  `skill-design-sources.md` traitent les skills comme des **contrats** workflow,
  avec une typologie rigid/flexible purement descriptive. Aucune synthèse ne formule
  que **le modèle négocie activement les instructions** et qu'écrire un skill est un
  exercice adversarial (anticiper les rationalisations, coder les contre-arguments
  en dur). `vibe-coding-practices.md` note « CLAUDE.md = compliance ~70-80% » mais
  en tire l'injonction pratique « préférer les hooks », pas la conclusion
  structurelle : **tout artefact textuel destiné au LLM doit être écrit comme un
  script adversarial, pas comme de la doc**.
- **Implication pour metadev-protocol :** La doc de `/brainstorm`, `/spec`, `/plan`
  dans le template est rédigée comme un contrat coopératif (« ce que ça fait »,
  « pourquoi c'est critique »). Elle devrait inclure un bloc *« rationalisations
  anticipées »* dans chaque SKILL.md, listant les contournements que le modèle va
  tenter et les réponses codées. Deuxième conséquence : le linter meta (le futur
  `scripts/check_meta_naming.py` étendu) devrait détecter les descriptions de skill
  qui « résument le workflow » — c'est un anti-pattern comportemental, pas
  stylistique. Troisième conséquence : le principe « max déterministe, LLM minimal »
  (du memory index user) trouve ici sa justification fondamentale — chaque fois
  qu'on reste sur un artefact textuel, on est en territoire adversarial.
- **Niveau de confiance :** fort (3 clusters, et contredit frontalement le framing
  « skills = documentation » des syntheses existantes). Pourquoi raté : parce que
  traiter les skills comme de la doc est *plus rassurant* — ça permet de les écrire
  sans se demander comment le modèle va les contourner.

### Pattern : Le contrat unifié « index léger + détail lazy + état récupérable »

- **Signal dans L1-A :** « Progressive disclosure appliquée au mauvais endroit par la
  plupart des sources » — le pattern « index léger → détail lazy-loaded » apparaît
  dans 3 contextes (KB retrieval claude-mem, SKILL.md index + references/, .claude/
  rules/ path-scoped) « sans qu'aucun auteur ne remarque que c'est la même solution
  architecturale à 3 niveaux différents ».
- **Signal dans L1-B :** « Le système de fichiers comme workaround universel de
  l'oubli » — « tout skill sérieux doit produire un état re-chargeable ». Skills
  deviennent implicitement des générateurs d'artefacts dont le but est la
  récupérabilité, pas le contenu.
- **Signal dans L1-D :** « L'écosystème sous-estime massivement ce qui sort d'une
  session » — trace structurée récupérable par la session suivante, couche traitée
  comme plomberie.
- **Absent des syntheses :** `context-management.md` a « Planning-with-files » et
  `skills-workflow-and-utilities.md` a « chaque étape produit un artefact dans
  `.meta/scratch/` ». Les deux le font sans le formaliser comme un **contrat unique**
  qui s'appliquerait indifféremment à : skills (SKILL.md index + references/), KB
  (index + entries lazy), rules path-scoped, mémoire (briefing + tiers), sessions
  (PILOT + SESSION-CONTEXT + archive). Le pattern est implémenté 5 fois dans le
  template, sans être nommé.
- **Implication pour metadev-protocol :** Le template devrait exposer ce contrat
  comme un **principe architectural transversal** dans `ARCHITECTURE.md` :
  tout artefact destiné au LLM doit avoir (1) un index compact chargé d'office,
  (2) du détail chargé à la demande, (3) un format suffisant pour reconstituer
  l'état si chargé à froid par la session N+1. Ce principe, une fois nommé,
  permet d'auditer uniformément skills, KB, rules, mémoire, et évite que chaque
  sous-système réinvente sa propre convention. C'est aussi le prérequis pour le
  « budget de bootstrap unifié » du pattern précédent : on ne peut pas mesurer un
  coût total si chaque artefact décide lui-même ce qui est « index » et ce qui est
  « détail ».
- **Niveau de confiance :** moyen-fort (3 clusters le voient mais pour des raisons
  différentes — L1-A le généralise explicitement, L1-B et L1-D le sous-entendent).
  Pourquoi raté : parce que « progressive disclosure » est déjà un buzzword dans
  les syntheses — il est tellement associé aux skills que personne ne remarque
  qu'il décrit aussi la mémoire, les rules, et la session output layer.
