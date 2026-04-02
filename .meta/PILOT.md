# PILOT.md — metadev-protocol

**Date :** 2026-04-01
**Phase :** Recherche terminee — pret pour implementation skills

---

## Etat du projet

### Infrastructure (FAIT)
- pyproject.toml, .pre-commit-config.yaml, copier.yml ✅
- Template complet : CLAUDE.md, pyproject.toml, .gitignore, .meta/, tests/, .claude/ ✅
- Generation testee (minimal + app) ✅
- Pre-commit installe ✅

### Recherche (FAIT)
- 12 fichiers raw dans .meta/references/ ✅
- 4 fichiers gold dans .meta/gold/ ✅
  - skills-workflow-and-utilities.md
  - context-management.md
  - claude-code-architecture.md
  - vibe-coding-practices.md
- 4 ADRs dans .meta/decisions/ ✅

### Implementation patterns (FAIT)
- CLAUDE.md.jinja v2 (<120 lignes, regles anti-LLM) ✅
- SESSION-CONTEXT.md.jinja ✅
- .claude/settings.json (permissions + hooks) ✅
- Skill /test ✅

### Skills fondation (A FAIRE — prochain sprint)

| Tier | Skill | Statut |
|------|-------|--------|
| T1 | /brainstorm | ❌ |
| T1 | /plan | ❌ |
| T1 | /ship | ❌ |
| T2 | /spec | ❌ |
| T2 | /tdd | ❌ |
| T2 | /review | ❌ |
| T2 | /debug | ❌ |
| T2 | /lint | ❌ |
| T2 | /consolidate | ❌ |
| T3 | /learn | ❌ |
| T3 | /digest | ❌ |

### Reste a faire (apres skills)

- src/{{project_slug}}/__init__.py dans template
- Config 3 niveaux pour profil app
- Instruction compaction dans CLAUDE.md
- Subagent guidance dans CLAUDE.md
- Skills profilees (api-test, pipeline-run, backtest)
- Ruff 120 chars config

---

## Structure des fichiers gold

```
.meta/
├── gold/                              ← Syntheses actionnables
│   ├── skills-workflow-and-utilities.md   ← Pipeline + utilitaires
│   ├── context-management.md             ← Compaction, memoire, sessions
│   ├── claude-code-architecture.md       ← Leak + doc officielle
│   └── vibe-coding-practices.md          ← Principes + anti-patterns
├── references/                        ← Sources brutes (12 fichiers)
├── decisions/                         ← ADRs (4 fichiers)
└── scratch/                           ← Brouillons (prompts, etc.)
```

---

## Contexte pour l'IA

- Les fichiers gold/ sont la source de verite synthetisee
- Les fichiers references/ sont les sources brutes (bronze)
- Les decisions/ sont les ADRs avec rationale et confiance
- Toute modification de template/ doit etre testee avec copier copy
- Stack : Python 3.12+, uv, ruff, copier, pre-commit
