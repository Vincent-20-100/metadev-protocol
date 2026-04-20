# Spec — Hooks ↔ Rules pairing doctrine

**Date:** 2026-04-20
**Status:** DRAFT
**Phase:** 1/2 (cahier des charges ; phase 2 = audit complet du repo)

## Objective

Établir une doctrine qui garantit que chaque contrainte automatisée (hook) du template metadev-protocol est doublée d'une règle lisible par le LLM, et que chaque règle critique est garantie par un hook. Toute déviation à l'état de l'art (PEP 8/257, Black, Google styleguide) doit être justifiée pour éviter la friction au bootstrap (cf. rapport `template-ruff-report.md` du 2026-04-19 : 15 erreurs ruff dès le premier commit du scaffold).

## Requirements

### Doctrine (principes directeurs)

- **[MUST]** Tout hook (pre-commit, `.claude/settings.json` hooks, scripts `check_*.py`) qui peut bloquer une action utilisateur ou LLM doit avoir une règle correspondante dans `.claude/rules/*.md` ou `CLAUDE.md`. Sans règle, le LLM répète l'erreur sans comprendre — le hook devient un piège.
- **[MUST]** Toute règle marquée critique (= si violée, l'action doit échouer) doit être garantie par un hook. Sinon elle est rétrogradée en `advisory` ou supprimée. Une règle critique sans enforcement est un vœu pieux.
- **[MUST]** Toute déviation à l'état de l'art doit être justifiée en 1-2 lignes dans la règle, avec lien vers la source (PEP, Black docs, Google styleguide).

### Taxonomie

- **[MUST]** 3 niveaux d'enforcement, chaque item du repo classé dans un seul :
  - `hard-block` — hook bloquant + règle obligatoire. Ex: ruff lint sur fichiers commités.
  - `soft-warn` — check non bloquant (warning visible) + règle. Ex: complexité cyclomatique élevée.
  - `advisory` — règle seule, pas d'enforcement mécanique. Ex: "préférer fonctions pures quand possible".
- **[MUST]** Le niveau est marqué dans le frontmatter ou en-tête de la règle (`enforcement: hard-block|soft-warn|advisory`) pour audit automatisé.

### Politique de strictness différenciée

- **[MUST]** Strictness par catégorie de fichier — pas de règle uniforme :

  | Catégorie | line-length | docstring-length | Justification |
  |---|---|---|---|
  | `src/{{ project_slug }}/**` | 100 | 100 | Code applicatif utilisateur ; 100 = Google styleguide, suffisant sans être PEP 8 strict (79). |
  | `scripts/**` | 120 | 120 | Scripts CLI : messages d'erreur et `argparse help=` lisibles priment. |
  | `tests/**` | 120 | — | Asserts et fixtures longues lisibles. |
  | `**/*.md` | aucune | — | Markdown : pas de wrap forcé, lisible en éditeur. |

- **[MUST]** Docstrings : `D` rules (pydocstyle) configurées séparément de `E501`, conformément à PEP 257 (un docstring lisible vaut mieux qu'un docstring tronqué). Référence : https://peps.python.org/pep-0257/
- **[MUST]** Justifier `line-length = 100` (vs PEP 8 = 79, Black = 88) en commentaire dans le `pyproject.toml.jinja` du template.

### Patterns de timing

- **[MUST]** Pattern list documenté dans une nouvelle règle `.claude/rules/workflow-timing.md` :

  | Action | Timing | Pourquoi AVANT, pas APRÈS |
  |---|---|---|
  | Créer la branche feature | AVANT le 1er edit | Switcher en plein milieu force stash/rebase, perte de contexte. |
  | Lancer `uv sync` | AVANT le 1er run de script | Évite ImportError opaques, échec rapide. |
  | Format ruff | APRÈS l'edit, AVANT commit | Sinon le hook reformate et le diff change. |
  | Test pytest | APRÈS impl, AVANT commit | Cf. règle existante `testing.md`. |
  | Tag semver | APRÈS merge, AVANT push externe | Tags immutables (mémoire utilisateur validée). |

- **[MUST]** Ces patterns deviennent des règles avec niveau `hard-block` si un hook peut les enforcer (ex: hook `pre-commit` qui refuse commit sur `main`), `advisory` sinon.

### Matrice hook ↔ règle (template à remplir en phase 2)

- **[MUST]** Le spec définit le format ; la phase 2 remplit. Format :

  ```markdown
  ## Inventaire

  ### Hooks
  | ID | Localisation | Type | Niveau | Règle associée |
  |---|---|---|---|---|
  | H001 | template/.pre-commit-config.yaml#ruff-check | pre-commit | hard-block | rules/code-style.md#linting |
  | H002 | ... | ... | ... | ... |

  ### Règles
  | ID | Fichier | Niveau déclaré | Hook associé |
  |---|---|---|---|
  | R001 | template/.claude/rules/code-style.md#linting | hard-block | H001 |
  | R002 | ... | ... | ... |

  ### Gaps
  - Hooks sans règle : [liste]
  - Règles critiques sans hook : [liste]
  - Règles `advisory` qui devraient être `hard-block` : [liste]
  ```

### Anti-patterns connus

- **[SHOULD]** Section "Lessons learned" listant les frictions résolues, source datée :
  - **2026-04-19** — Bootstrap cassé par 15 erreurs ruff (`line-length=88` trop strict pour messages CLI). Résolu par strictness différenciée par catégorie de fichier.
  - [À enrichir au fur et à mesure des incidents.]

## Non-goals

- Pas d'audit du repo ni de fix dans cette phase — phase 2.
- Pas de réécriture des hooks existants — on définit la doctrine, pas l'implémentation.
- Pas de règles sur le contenu sémantique du code utilisateur (déjà couvert par `code-style.md`).
- Pas de couverture des règles comportementales du LLM (Rule of 3, devil's advocate) — focus sur contraintes mécaniques uniquement.
- Pas de support multi-langage — Python uniquement (cohérent avec stack du repo).

## Proposed approach

Phase 1 (ce spec) produit la **doctrine + taxonomie + politique de strictness + patterns timing + format de matrice**. Aucun fichier du template touché.

Phase 2 (après validation) produit :
1. La matrice hook↔règle remplie via inventaire complet (`.pre-commit-config.yaml` meta + template, `.claude/settings.json` hooks, scripts `check_*.py`, `.claude/rules/*.md`, sections de `CLAUDE.md`).
2. Liste de fixes par item (ajuster strictness, ajouter règle manquante, retirer hook orphelin, justifier déviation).
3. PR groupée par catégorie (strictness ruff, règles manquantes, hooks orphelins) pour bisectabilité.

## Open questions

1. **Frontmatter ou en-tête markdown ?** Pour marquer le niveau d'enforcement dans les règles, on utilise un frontmatter YAML (`enforcement: hard-block`) ou une ligne de header (`> Enforcement: hard-block`) ? Frontmatter = plus parsable, header = plus lisible humain.
2. **Per-file-ignores via ruff config ou commentaires `# noqa` ?** Pour les exceptions ponctuelles (ex: une ligne légitimement longue), on privilégie `per-file-ignores` global ou `# noqa: E501` local ? Recommandation : config globale par catégorie + `# noqa` interdit sauf justification en commentaire.
3. **Niveau pour les règles de timing ?** "Crée la branche AVANT" est-il enforcable par hook (refuser commit sur `main`) ou reste advisory ? Recommandation : hook `hard-block` qui refuse commit direct sur `main`/`master`.

## Next step

Validation utilisateur sur :
- les 3 questions ouvertes
- la table de strictness (les chiffres 100/120/120 sont-ils OK ?)
- la table des patterns timing (oubli ?)

Puis lancer phase 2 (audit complet) avec `/plan` ou directement skill `/orchestrate` si on veut spec→audit→fix→test→tag en chaîne.
