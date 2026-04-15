# Plan — PM.14 + PM.11 + PM.12

**Date:** 2026-04-13
**Based on:** brainstorm-pm14-synthesis-run.md
**Confidence:** AMBER (PM.14 — agent token budgets non testés ; PM.11/12 — GREEN)

---

## PLAN A — PM.14 : Multi-agent synthesis run

**Objectif :** produire `.meta/references/synthesis/emergent-patterns.md` via 4 agents L1 + 1 agent L2.

### Files involved

- `.meta/references/synthesis/emergent-patterns.md` — créer (output L2)
- `.meta/scratch/l1-context.md` — créer (signaux faibles L1-A)
- `.meta/scratch/l1-skill.md` — créer (signaux faibles L1-B)
- `.meta/scratch/l1-workflow.md` — créer (signaux faibles L1-C)
- `.meta/scratch/l1-ecosystem.md` — créer (signaux faibles L1-D)

### Tasks

#### A.1 — Guardrail : vérifier que emergent-patterns.md n'existe pas
- **Files :** `.meta/references/synthesis/emergent-patterns.md`
- **Do :** `test -f .meta/references/synthesis/emergent-patterns.md && echo EXISTS || echo OK`
- **Verify :** commande retourne "OK"

#### A.2 — Lancer les 4 agents L1 en parallèle

Utiliser l'outil `Agent` avec 4 appels dans le même message (`run_in_background: true` pour L1-A/B/C, `run_in_background: false` pour L1-D qui est le plus lourd). Attendre la complétion de tous avant de passer à A.3.

**Fallback L1-D context saturation :** si l'agent L1-D signale qu'il n'a pas pu lire tous les fichiers, il liste les fichiers sautés en tête de rapport et continue avec les fichiers traités. Ne pas aborter — un rapport partiel vaut mieux que rien pour L2.

Chaque agent reçoit le prompt L1 du brainstorm + les fichiers de son cluster (lus en contexte).

**L1-A — Context & memory** (5 fichiers) :
```
.meta/references/raw/claude-mem-audit.md
.meta/references/raw/claude-code-undercover-mode.md
.meta/references/raw/claude-code-docs-audit.md
.meta/references/interim/context-management-patterns.md
.meta/references/interim/session-2026-04-13-audit-agent-reach.md
```
Output → `.meta/scratch/l1-context.md`

**L1-B — Skill design** (5 fichiers) :
```
.meta/references/raw/feynman-audit.md
.meta/references/raw/github-skills-landscape.md
.meta/references/raw/superpowers-and-everything-claude-code.md
.meta/references/interim/claude-code-hooks-skills-reference.md
.meta/references/interim/dev-workflow-skills-patterns.md
```
Output → `.meta/scratch/l1-skill.md`

**L1-C — Workflow & governance** (5 fichiers) :
```
.meta/references/raw/state-of-the-art-vibe-coding.md
.meta/references/raw/audit-egovault.md
.meta/references/raw/sota-mcp-patterns.md
.meta/references/raw/hermes-agent-nous-research.md
.meta/references/interim/python-templating-best-practices.md
```
Output → `.meta/scratch/l1-workflow.md`

**L1-D — Ecosystem & signals** (8 fichiers) :
```
.meta/references/raw/claude-code-ecosystem-54-resources.md
.meta/references/raw/ecosystem-deep-dive.md
.meta/references/raw/top-repos-and-voices.md
.meta/references/raw/watchlist.md
.meta/references/raw/linkedin-curated-posts.md
.meta/references/raw/claude-code-leak-analysis.md
.meta/references/raw/claude-code-security-deepdive.md
.meta/references/interim/ecosystem-54-triage.md
```
Output → `.meta/scratch/l1-ecosystem.md`

- **Verify :** 4 fichiers `.meta/scratch/l1-*.md` existent et non-vides

#### A.3 — Lancer l'agent L2

L2 reçoit :
- Les 4 rapports L1 (`.meta/scratch/l1-*.md`)
- Les 7 fichiers synthesis/ existants :
  ```
  .meta/references/synthesis/claude-code-architecture.md
  .meta/references/synthesis/context-management.md
  .meta/references/synthesis/gstack-skill-pack.md
  .meta/references/synthesis/python-dev-and-templating.md
  .meta/references/synthesis/skill-design-sources.md
  .meta/references/synthesis/skills-workflow-and-utilities.md
  .meta/references/synthesis/vibe-coding-practices.md
  ```

L2 produit directement `.meta/references/synthesis/emergent-patterns.md`.

- **Verify :** fichier existe, contient au moins 3 sections `### Pattern :`, niveau de confiance explicite pour chaque pattern

#### A.4 — Commit du résultat

```bash
git add .meta/references/synthesis/emergent-patterns.md
git commit -m "feat(synthesis): emergent-patterns — PM.14 multi-agent synthesis run"
```

- **Verify :** `git log --oneline -1` montre le commit

#### A.4b — Nettoyage des fichiers scratch L1

```bash
rm .meta/scratch/l1-context.md .meta/scratch/l1-skill.md \
   .meta/scratch/l1-workflow.md .meta/scratch/l1-ecosystem.md
```

- **Verify :** `ls .meta/scratch/l1-*.md` retourne erreur

---

**Risque AMBER :** L1-D a 8 fichiers — si l'agent dépasse son budget de contexte, scinder en deux appels séquentiels et merger les signaux avant de passer à L2.

---

## PLAN B — PM.11 : Refactor /research sous skill-vs-tool

**Analyse ratio LLM/déterministe :**
- Déterministe : fetch HTTP, écriture fichier, formatage schema → ~35%
- LLM : formulation queries, identification thèmes, consensus/divergence, synthèse → ~65%

Conclusion : LLM-dominant. Le refactor n'est PAS un script lourd. C'est un **allégement** : extraire la logique de formatage/écriture en un wrapper fin, garder le SKILL.md comme orchestrateur LLM.

**Ce qui change :**
1. Le SKILL.md perd les sections process détaillées (devenu verbeux)
2. Le schéma output sort du SKILL.md → fichier de référence séparé
3. Le SKILL.md devient ≤80 lignes : quand l'utiliser, 3 étapes (clarify → research → write), et pointer vers le schéma

### Files involved

- `template/.claude/skills/research/SKILL.md` — modifier (allégir de ~200 à ~80 lignes)
- `template/.claude/skills/research/output-schema.md` — créer (schéma extrait du SKILL.md actuel)

### Tasks

#### B.1 — Créer output-schema.md

- **Files :** `template/.claude/skills/research/output-schema.md`
- **Do :** Extraire la section "Output schema (locked)" du SKILL.md actuel. Ajouter une courte intro "Ce fichier est la référence de format pour les outputs de /research."
- **Verify :** fichier existe, contient le template markdown complet avec tous les champs

#### B.2 — Réécrire SKILL.md à ≤80 lignes

- **Files :** `template/.claude/skills/research/SKILL.md`
- **Do :** Garder : quand utiliser / quand ne pas utiliser / hard rules / 3 étapes (clarify → fetch → write) / pointeur vers output-schema.md. Supprimer : rationalizations, détail des 7 steps, output schema inline.
- **Verify :** `wc -l template/.claude/skills/research/SKILL.md` ≤ 80

#### B.3 — Propager dans les tests

- **Files :** `tests/test_template_generation.py`
- **Do :** Vérifier que `TestSkills` liste bien `research` dans `EXPECTED_SKILLS` (déjà présent). Ajouter assertion `test_research_has_output_schema` : vérifie que `output-schema.md` existe dans le skill dir.
- **Verify :** `uv run pytest tests/test_template_generation.py::TestSkills -v` — tous les tests verts

#### B.4 — Commit

```bash
git add template/.claude/skills/research/
tests/test_template_generation.py
git commit -m "refactor(template): thin /research skill — extract output schema, ≤80 LOC"
```

---

## PLAN C — PM.12 : Refactor /audit-repo sous skill-vs-tool

**Analyse ratio LLM/déterministe :**
- Déterministe : `git clone`, `tree`, lire fichiers, `rm -rf`, écriture output → ~55%
- LLM : fingerprint analysis, catégorisation, tiering, rédaction findings → ~45%

Conclusion : mix équilibré, légèrement déterministe. Le refactor crée un **script de bootstrap** qui prépare la matière première, laisse le LLM faire l'analyse.

**Ce qui change :**
1. `scripts/audit_repo.py <url>` : clone, fingerprint automatique (lang, type, stars via gh, last commit), tree, cleanup → produit un JSON structuré
2. Le SKILL.md devient : (1) `uv run python -m scripts.audit_repo <url>` (2) LLM analyse le JSON + écrit le rapport tiered

**Note :** /audit-repo est meta-repo only (pas dans template/). Le script va dans `scripts/` du meta-repo.

### Files involved

- `scripts/audit_repo/__main__.py` — créer (clone + fingerprint + tree + cleanup)
- `scripts/audit_repo/__init__.py` — créer (vide)
- `.claude/skills/audit-repo/SKILL.md` — modifier (≤60 lignes, 2 étapes)

### Tasks

#### C.1 — Créer scripts/audit_repo/__main__.py

- **Files :** `scripts/audit_repo/__main__.py`, `scripts/audit_repo/__init__.py`
- **Do :**
  ```
  CLI: python -m scripts.audit_repo <url> [--angle <hint>]
  1. slug = repo name (dashes, lowercase)
  2. git clone --depth=1 --filter=blob:none <url> /tmp/audit-<slug>/
  3. Fingerprint :
     - primary_lang : count extensions
     - repo_type : detect via presence signals (copier.yml → template, etc.)
     - stars + last_commit : gh api repos/<owner>/<repo> --jq '.stargazers_count, .pushed_at'
       → si gh échoue (pas auth, rate limit) : stars = "unknown", last_commit = "unknown" — ne pas aborter
     - license : lire LICENSE
     - pitch : première ligne non-vide du README après le titre
     - file_count : find /tmp/audit-<slug> -type f | wc -l
  4. tree -L 2 /tmp/audit-<slug> (filtré : exclure .git, __pycache__, node_modules)
  5. rm -rf /tmp/audit-<slug>/
  6. Print JSON : { slug, url, angle, fingerprint, tree_output }
  ```
- **Verify :** `uv run python -m scripts.audit_repo https://github.com/astral-sh/ruff --angle general` → JSON valide avec fingerprint et tree (stars peut être "unknown" si gh non auth)

#### C.2 — Réécrire .claude/skills/audit-repo/SKILL.md

- **Files :** `.claude/skills/audit-repo/SKILL.md`
- **Do :** ≤60 lignes. Structure :
  ```
  Étape 1 : uv run python -m scripts.audit_repo <url> [--angle <hint>]
  Étape 2 : LLM analyse le JSON → remplit les 5 catégories + tiering → écrit interim/
  ```
  Garder : hard rules (no secrets, always write file, all tiers), output schema (locked), failure handling.
- **Verify :** `wc -l .claude/skills/audit-repo/SKILL.md` ≤ 60

#### C.3 — Commit

```bash
git add scripts/audit_repo/ .claude/skills/audit-repo/SKILL.md
git commit -m "refactor(meta): thin /audit-repo skill — script handles clone+fingerprint, LLM handles analysis"
```

---

## Ordre d'exécution cette nuit

```
B (PM.11) → C (PM.12) → A (PM.14)
```

Rationale : B et C sont courts et verts → les faire d'abord valide l'approche. A est le run lourd → le lancer en dernier quand le corpus est stable.

---

## Checklist avant lancement

- [x] Confidence : PM.14 AMBER (risque contexte L1-D), PM.11 GREEN, PM.12 GREEN
- [x] Tous les fichiers listés
- [x] Chaque tâche a une étape Verify concrète
- [x] Ordre dépendances respecté (B → C → A)
- [ ] **Validation utilisateur requise avant exécution**
