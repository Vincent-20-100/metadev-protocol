# ADR-004 — Matrice de decision : tous les patterns classes

**Date :** 2026-04-01
**Statut :** DRAFT — en attente de validation Vincent

---

## Grille de classification

### Axe 1 — Priorite (qualite/importance)

| Tier | Signification | Critere |
|------|--------------|---------|
| **T1 INDISPENSABLE** | Si c'est pas la, le template n'a pas de valeur | Sans ca, le projet genere est pire qu'un `mkdir` |
| **T2 RECOMMANDE** | Forte valeur ajoutee, consensus de la communaute | Adopte par >50% des bons repos, impact mesurable |
| **T3 NICE-TO-HAVE** | Utile mais pas critique, peut venir plus tard | Ameliore l'experience sans etre bloquant |
| **T4 A EVITER** | Over-engineering, trop specifique, ou contre-productif | Ajoute de la complexite sans benefice clair pour un bootstrap |

### Axe 2 — Scope (vanilla vs custom)

| Scope | Signification |
|-------|--------------|
| **VANILLA** | Dans tous les profils (minimal/app/data/quant) |
| **PROFILE** | Conditionnel au type de projet |
| **USER** | L'utilisateur l'ajoute lui-meme si besoin |

---

## La matrice

### T1 INDISPENSABLE

| Pattern | Scope | Source | Implemente ? |
|---------|-------|--------|-------------|
| CLAUDE.md avec instructions IA (<120 lignes) | VANILLA | SOTA, ADR-003 | OUI |
| pyproject.toml avec deps par profil | VANILLA | EgoVault, SOTA | OUI |
| .gitignore propre | VANILLA | Standard | OUI |
| uv comme gestionnaire de deps | VANILLA | SOTA, consensus | OUI |
| ruff pour lint + format | VANILLA | SOTA, consensus | OUI |
| pre-commit hooks (ruff) | VANILLA | SOTA, ADR-001 | OUI |
| Conventional commits documentes | VANILLA | EgoVault, SOTA | OUI |
| .meta/ cockpit (PILOT.md) | VANILLA | EgoVault, ADR-003 | OUI |
| tests/ avec conftest.py | VANILLA | EgoVault, SOTA | OUI |
| .claude/settings.json (permissions) | VANILLA | ADR-002 | OUI |
| git init post-copy | VANILLA | SOTA | OUI |

### T2 RECOMMANDE

| Pattern | Scope | Source | Implemente ? |
|---------|-------|--------|-------------|
| SESSION-CONTEXT.md (rewrite, don't append) | VANILLA | EgoVault, ADR-003 | OUI |
| Workflow 5 phases dans PILOT.md | VANILLA | EgoVault+SOTA, ADR-003 | OUI |
| Hierarchie documentaire (CLAUDE.md > decisions > docstrings) | VANILLA | EgoVault, ADR-003 | OUI |
| Regles anti-LLM universelles (G2, G5, G6, G13) | VANILLA | EgoVault, ADR-003 | OUI |
| Hook auto-ruff PostToolUse | VANILLA | ADR-002, SOTA | OUI |
| Hook re-injection contexte apres compaction | VANILLA | ADR-002, ref hooks | OUI |
| Skill /test (pytest) | VANILLA | ADR-002 | OUI |
| Deny permissions (rm -rf, sudo, .env, .git) | VANILLA | ADR-002 | OUI |
| Skill /lint (ruff check + format) | VANILLA | Logique directe | **NON** |
| Skill /ship (checklist pre-commit) | VANILLA | SOTA workflow | **NON** |
| src/{{project_slug}}/__init__.py | VANILLA | Standard Python | **NON** |
| PEP 735 dependency groups (dev/test) | VANILLA | SOTA | OUI (partiel) |
| Regles profilees app (routing mince, DI) | PROFILE:app | EgoVault G4/G11 | OUI |
| Regles profilees quant (vectorisation, doc math) | PROFILE:quant | EgoVault adapte | OUI |
| Regles profilees data (idempotent, raw immutable) | PROFILE:data | EgoVault adapte | OUI |
| Config 3 niveaux (system/user/install) | PROFILE:app | EgoVault, ADR-001 | **NON** |
| Deps fastapi+uvicorn | PROFILE:app | Standard | OUI |
| Deps polars+duckdb | PROFILE:data | Standard | OUI |
| Deps numpy+pandas+matplotlib | PROFILE:quant | Standard | OUI |

### T3 NICE-TO-HAVE

| Pattern | Scope | Source | Implemente ? |
|---------|-------|--------|-------------|
| Skill /review (code review en subagent fork) | VANILLA | Ref hooks/skills | **NON** |
| Instruction compaction dans CLAUDE.md | VANILLA | SOTA | **NON** |
| 120-char line length ruff config | VANILLA | SOTA consensus | **NON** |
| Dynamic versioning (git tags) | VANILLA | SOTA | **NON** |
| Skill /api-test (test endpoints) | PROFILE:app | Logique directe | **NON** |
| Skill /pipeline-run | PROFILE:data | Logique directe | **NON** |
| Skill /backtest | PROFILE:quant | Logique directe | **NON** |
| .mcp.json vide/template | USER | Ref MCP | **NON** |
| Subagent investigation pattern | USER | SOTA, leak | **NON** |
| Red Zone / Green Zone documentation | USER | SOTA | **NON** |
| 9 couches app IA comme checklist | PROFILE:app | LinkedIn posts | **NON** |
| Recursive arguing (code + review agents) | USER | SOTA | **NON** |
| agnix linter pour CLAUDE.md/skills | USER | top-repos | **NON** |
| Research-first development guide | VANILLA | SOTA | **NON** |

### T4 A EVITER (pour un bootstrap)

| Pattern | Pourquoi on le rejette | Source |
|---------|----------------------|--------|
| Workflow 7 phases (BRAINSTORM→AUDIT) | Over-engineered pour un nouveau projet | EgoVault |
| docs/superpowers/ lifecycle (specs/plans/audits/archive) | Trop lourd, pertinent pour projets matures | EgoVault |
| @loggable decorator avec callback injection | Trop specifique a l'architecture EgoVault | EgoVault |
| Taxonomie config-driven (YAML enums) | Specifique aux projets avec classification user | EgoVault |
| Sandbox Claude Code active par defaut | Trop restrictif, casse le flow de dev | Ref hooks |
| MCP servers pre-configures | Trop specifique a chaque user/environnement | Ref MCP |
| Hook PreToolUse bloquer rm (redondant avec deny) | Le deny dans permissions fait deja le job | Ref hooks |
| KAIROS/autoDream/ULTRAPLAN patterns | Features non-releasees, pas utilisables | Leak |
| Anti-distillation fake tools | Specifique Anthropic, pas un pattern de dev | Leak |
| pyright/mypy active par defaut | Ajoute friction sans benefice pour un bootstrap | SOTA |
| CI/CD pipeline genere | Trop specifique (GitHub Actions vs GitLab vs...) | Standard |

---

## Prochaines actions (par priorite)

### Sprint 1 — Completer les T2 manquants

| Action | Effort |
|--------|--------|
| Creer skill /lint | Petit |
| Creer skill /ship | Petit |
| Creer src/{{project_slug}}/__init__.py dans template | Petit |
| Creer config/ 3 niveaux pour profil app | Moyen |

### Sprint 2 — T3 a forte valeur

| Action | Effort |
|--------|--------|
| Instruction compaction dans CLAUDE.md | Petit |
| Config ruff 120 chars dans pyproject.toml.jinja | Petit |
| Skill /review (subagent fork) | Moyen |
| Skills profilees (api-test, pipeline-run, backtest) | Moyen |

### Sprint 3 — Documentation et polish

| Action | Effort |
|--------|--------|
| Guide "comment ajouter ses propres skills" | Petit |
| Guide MCP configuration | Petit |
| Research-first development tips dans CLAUDE.md | Petit |

---

## Niveaux de confiance

| Tier | Confiance | Justification |
|------|-----------|---------------|
| T1 | TRES ELEVE | Standards de l'industrie, consensus large |
| T2 | ELEVE | Teste sur EgoVault et/ou documente par la communaute |
| T3 | MOYEN | Bonne idee mais pas encore testee dans notre contexte |
| T4 | ELEVE (sur le rejet) | Over-engineering prouve ou trop specifique |
