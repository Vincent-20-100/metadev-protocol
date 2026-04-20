# Audit — Hooks ↔ Rules pairing

**Date:** 2026-04-20
**Status:** DRAFT (phase 2 du spec `spec-hooks-rules-pairing.md`)
**Scope:** meta-repo `metadev-protocol` + son `template/`
**Source inventaire:** Explore agent run du 2026-04-20 (33 hooks, 57 règles + 3 ADR)

---

## Résumé exécutif

Le repo a **bonne couverture côté hooks** (33 mécanismes d'enforcement) mais **cassures structurelles côté pairing** :

1. **6 hooks critiques sans règle correspondante** — le LLM ne sait pas qu'ils existent et reproduit l'erreur (cas exact du rapport ruff du 2026-04-19).
2. **9 règles `hard-block` sans hook** — vœux pieux, violables silencieusement.
3. **Strictness ruff non documentée** (line-length 88 partout) — c'est la cause racine du bootstrap cassé.
4. **Aucune règle sur le timing de la branche** alors que H013 bloque commit sur `main` — friction garantie.

Total : **~17 actions correctives** réparties en 4 PR (strictness, règles manquantes, hooks manquants, justifications).

---

## 1. Matrice hook ↔ règle

### 1.1 Hooks AVEC règle (couverture OK)

| Hook ID | Hook | Règle(s) associée(s) | Notes |
|---|---|---|---|
| H003, H018 | `check_meta_naming` | R012, R053, R054 | Triple couverture, OK |
| H004, H019 | `check_git_author` | R022 | OK |
| H005, H020 | `check_coauthor_trailer` | R022 | OK |
| H013 | `no-commit-to-branch main` (template) | — (R023 advisory dit l'inverse) | **CONFLIT** : R023 promeut trunk-based, H013 le bloque |
| H015, H017 | `SessionStart welcome` | R032, R033 | OK |
| H023-H025 | CI lint/pre-commit/template-test | R013, R014 (partiel) | OK |
| H026, H027 | CI public-safety | ADR-002, ADR-008 | OK (ADR seulement, pas de rule .md) |
| H028-H030 | `audit_public_safety` checks A/B/C | ADR-002 partiel | Couverture faible |
| H032 | `save_progress_preflight` | R010 (testing#Before committing) | Couverture indirecte |
| H033 | `pyproject.toml#testpaths` | R007 (testing#Structure) | OK |

### 1.2 Hooks SANS règle (gap critique — LLM aveugle)

| Gap ID | Hook | Ce qu'il enforce | Action |
|---|---|---|---|
| **G1** | H001, H002, H014, H016 (ruff lint+format) | line-length=88, ruleset E/F/W/I/N/UP/B/SIM | **Créer `rules/linting.md`** : justifier choix, lister rules actives, documenter strictness différenciée par catégorie |
| **G2** | H007, H021, H022 (`check_skills_contract`) | Skills/agents listés dans CLAUDE.md trigger-table existent en filesystem | **Créer `rules/skills-contract.md`** : tout ajout dans trigger-table = créer fichier `.claude/skills/<n>/SKILL.md` ou `.claude/agents/<n>.md` |
| **G3** | H008, H031 (`sync_hosts`) | Stubs multi-host à jour | **Créer `rules/multi-host.md`** ou ajouter section dans CLAUDE.md (sinon LLM modifie source-of-truth sans regen stubs) |
| **G4** | H013 (`no-commit-to-branch`) | Pas de commit direct sur `main` | **Créer `rules/branching.md`** : "crée la branche AVANT le 1er edit" — c'est exactement le pain point utilisateur |
| **G5** | H006, H026-H030 (audit public-safety) | Pas de secrets / fichiers sensibles trackés | **Créer `rules/secrets.md`** : patterns interdits, où mettre les `.env`, comment marquer un fichier sensible (le LLM va régulièrement vouloir committer un `.env.example` mal nommé) |
| **G6** | H009-H012 (whitespace, eof, yaml, toml) | Standards formatage | **Acceptable sans règle** (fix mécanique automatique, pas de cas où le LLM doit comprendre) — laisser tel quel mais mentionner en 1 ligne dans `linting.md` |

### 1.3 Règles `hard-block` SANS hook (vœux pieux)

| Gap ID | Règle | Critique car | Action |
|---|---|---|---|
| **G7** | R002, R016 (English everywhere) | Critique pour cohérence template, mais aucun check | Soft : retrograder en `advisory` OU ajouter check ruff `RUF` rules + commitlint |
| **G8** | R015, R024, R026, R040, R048 (Conventional Commits format) | Tag/changelog dépendent du format | **Ajouter hook `commitlint`** ou `conventional-pre-commit` |
| **G9** | R032 (lire PILOT.md au session start) | Toute la chaîne contexte en dépend | Hook Claude SessionStart existe (H015/H017) mais ne FORCE pas la lecture, juste affiche un message — gap réel |
| **G10** | R035-R037 (approval avant Edit/Write) | Le plus critique | **Pas hookable** (pure comportement LLM) — accepter `advisory` mais le rendre explicite dans la doctrine |
| **G11** | R039 (rewrite SESSION-CONTEXT en fin de session) | Continuité inter-sessions | **Pas hookable directement** — `/save-progress` skill existe + H032 preflight, mais rien ne force l'invocation |
| **G12** | R043 (Rule of 3) | Anti-consensus bias | Pure LLM, accepter `advisory` |
| **G13** | R047 (no silent errors) | Bug silencieux possible | **Ajouter ruff rules `BLE`, `TRY`** pour partial enforcement |
| **G14** | R052 (honesty constraint) | Réputation et confiance | Pure LLM, `advisory` |
| **G15** | R054 (lifecycle `git mv` drafts→active→archive) | Pas critique mais déclaré hard-block | Retrograder en `advisory` OU ajouter check optionnel |

### 1.4 Conflits doctrinaux

| Conflit | Description | Résolution |
|---|---|---|
| **C1** | R023 (`advisory` trunk-based, work on main) ↔ H013 (`hard-block` no-commit-to-branch main, dans template uniquement) | Différencier explicitement : meta-repo permet trunk-based ; template force branches feature. Documenter dans `branching.md` (G4). |
| **C2** | R017 + R051 (YAGNI `advisory`) ↔ ruleset ruff `B` (bugbear) qui flag complexité | Rien à faire, pas vraiment conflictuel mais à mentionner |

---

## 2. Cause racine du bootstrap cassé (rapport 2026-04-19)

**Diagnostic** : `template/pyproject.toml.jinja` L30 `line-length = 88` appliqué uniformément à tout le scaffold, alors que :
- `scripts/` contient des messages CLI longs et `argparse help=` (légitime → 100-120 chars)
- Les docstrings de fonctions explicites dépassent 88 chars naturellement (PEP 257 ne fixe pas de limite)
- Le template ne fournit pas `per-file-ignores`

**Aggravation** : aucune règle dans `.claude/rules/` ne mentionne ce choix → le LLM génère naturellement du code à 100 chars (Google styleguide qu'il a en training par défaut), pre-commit échoue, friction.

**Fix recommandé** (validé en spec) :
```toml
[tool.ruff]
line-length = 100  # Google styleguide, vs PEP 8 (79) / Black (88)
                   # Justification: error messages and CLI help strings
                   # Source: https://google.github.io/styleguide/pyguide.html#32-line-length

[tool.ruff.lint.per-file-ignores]
"scripts/**/*.py" = ["E501"]  # CLI scripts: long error messages legit
"tests/**/*.py" = ["E501"]    # Test asserts and fixtures
```

Plus création de `template/.claude/rules/linting.md` (cf. G1).

---

## 3. Plan d'action proposé (4 PR séquentielles)

### PR-1 — Strictness ruff + justifications
- Modifier `template/pyproject.toml.jinja` : `line-length=100` + `per-file-ignores` + commentaire justificatif
- Fix les 2 SIM108 à la source dans `template/scripts/`
- Test : `copier copy . /tmp/test-proj --defaults` → `uv run ruff check .` → 0 erreur
- Bump semver + tag annoté

### PR-2 — Règles manquantes (G1-G5)
- Créer `template/.claude/rules/linting.md` (G1)
- Créer `template/.claude/rules/skills-contract.md` (G2)
- Créer `template/.claude/rules/multi-host.md` (G3, conditionnel : seulement si execution_mode=multi-host)
- Créer `template/.claude/rules/branching.md` (G4) — **prioritaire pour le pain point timing**
- Créer `template/.claude/rules/secrets.md` (G5)
- Mêmes fichiers dans le meta-repo `.claude/rules/` (dogfood)
- Chaque règle utilise frontmatter `enforcement: hard-block|soft-warn|advisory`

### PR-3 — Hooks manquants (G8, G13)
- Ajouter `commitlint` ou `conventional-pre-commit` dans `.pre-commit-config.yaml` meta + template (G8)
- Ajouter ruff rules `BLE` (blind except) et `TRY` (tryceratops) au ruleset (G13)
- Adapter `linting.md` pour documenter les nouveaux checks

### PR-4 — Doctrine et conflits
- Résoudre C1 : documenter explicitement meta vs template branching dans `branching.md`
- Retrograder G7, G15 en `advisory` ou ajouter checks
- Ajouter section "Anti-patterns connus" dans `.meta/GUIDELINES.md` avec entrée 2026-04-19 (ruff bootstrap)
- Mettre à jour `CLAUDE.md` pour pointer vers les nouvelles règles

---

## 4. Décisions à prendre avant exécution

1. **Frontmatter des règles** : YAML (`---\nenforcement: hard-block\n---`) ou en-tête markdown (`> **Enforcement:** hard-block`) ? Je recommande **YAML** pour parsing automatique futur (matrice générable).
2. **Commitlint vs conventional-pre-commit** : le second est pure-Python, plus simple à intégrer dans pre-commit existant. Je recommande **conventional-pre-commit**.
3. **Ordre des PR** : séquentiel (1→2→3→4) ou regrouper PR-1+PR-2 (strictness + règle linting font sens ensemble) ? Je recommande **PR-1+PR-2 mergées** (cohérent), PR-3 et PR-4 séparées.
4. **G3 (multi-host)** : règle inconditionnelle ou jinja conditionnelle (`{% if execution_mode == "multi-host" %}`) ? Je recommande **jinja conditionnelle** pour ne pas polluer projets simples.

---

## 5. Items hors-scope de cet audit

- Refacto des skills (hors périmètre hooks/rules)
- Audit des permissions `.claude/settings.json` (autre chantier)
- Migration vers superpowers (déjà en flight)
- Tests pytest des scripts `check_*.py` eux-mêmes (à proposer ailleurs)

---

## Next step

Validation utilisateur sur :
- les 4 décisions section 4
- le périmètre des 4 PR (rien à ajouter/retirer ?)
- l'ordre / le batching

Puis lancer PR-1+PR-2 avec `/plan` (ou directement `/orchestrate` si on veut full-auto jusqu'au tag).
