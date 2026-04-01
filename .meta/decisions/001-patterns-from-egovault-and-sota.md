# ADR-001 — Patterns a integrer dans le template (EgoVault + Etat de l'art)

**Date :** 2026-04-01
**Statut :** DRAFT — en attente de validation Vincent
**Sources :** audit-egovault.md, state-of-the-art-vibe-coding.md, claude-code-leak-analysis.md

---

## Contexte

Croisement de l'audit EgoVault (projet reel, 374 tests, architecture mature) avec
la recherche etat de l'art (CLAUDE.md sizing, hooks vs instructions, progressive disclosure).
L'objectif est de decider quels patterns integrer dans le template metadev-protocol.

---

## Decisions

### ADOPTER — Integration directe dans le template

#### 1. Cockpit 2 fichiers : PILOT.md (etat) + SESSION-CONTEXT.md (pourquoi)

- **Source :** EgoVault (PROJECT-STATUS + SESSION-CONTEXT)
- **Adaptation :** Renommer en PILOT.md (deja fait) + ajouter SESSION-CONTEXT.md.jinja
- **Regle cle :** SESSION-CONTEXT.md est REECRIT chaque session, pas complete
- **Impact :** `template/.meta/` — ajouter SESSION-CONTEXT.md.jinja

#### 2. Regles anti-LLM universelles dans CLAUDE.md

- **Source :** EgoVault G1-G13, filtre sur les universelles
- **Regles a inclure dans tous les profils :**
  - G2 — Docstrings: WHAT not HOW
  - G5 — No over-engineering
  - G6 — Every except must log or re-raise
  - G13 — Comments: concis, chirurgicaux
- **Regles profilables (app seulement) :**
  - G4 — tools n'importent jamais infrastructure
  - G11 — Routing layers are thin (<15 lines)
- **Impact :** `template/CLAUDE.md.jinja` — ajouter section regles

#### 3. CLAUDE.md < 200 lignes (contrainte de sizing)

- **Source :** Etat de l'art (Boris Cherny, ~100 lignes / 2500 tokens)
- **Constat :** EgoVault a 350 lignes = trop long. Compliance drops au-dela de 200.
- **Decision :** Le template genere un CLAUDE.md de 80-120 lignes max
- **Trade-off :** Les regles detaillees (exemples Wrong/Right) vont dans `.claude/` skills,
  pas dans CLAUDE.md
- **Impact :** `template/CLAUDE.md.jinja` — garder lean, deporter le detail

#### 4. Hooks > CLAUDE.md pour l'enforcement

- **Source :** Etat de l'art (hooks = 100% compliance vs CLAUDE.md = ~70-80%)
- **Constat :** EgoVault n'a AUCUN hook — tout est porte par CLAUDE.md = fragile
- **Decision :** Le template genere `.pre-commit-config.yaml` avec ruff (deja fait)
  + potentiellement des hooks Claude Code dans `.claude/settings.json`
- **Impact :** Deja partiellement fait. Explorer les hooks Claude Code.

#### 5. Config a 3 niveaux (system / user / install)

- **Source :** EgoVault config/
- **Adaptation :** Pour le profil `app`, generer `config/` avec .example files
- **Impact :** `template/` — conditionnel sur project_type == "app"

#### 6. Hierarchie documentaire permanente / provisoire

- **Source :** EgoVault CLAUDE.md §3
- **Decision :** Integrer dans le CLAUDE.md genere : "CLAUDE.md > docs/ > docstrings"
  + distinguer `.meta/` (provisoire) de `docs/` (permanent)
- **Impact :** `template/CLAUDE.md.jinja`

#### 7. Tests miroir structure + conftest.py avec DI mock

- **Source :** EgoVault tests/conftest.py
- **Decision :** Generer `tests/conftest.py` minimal avec fixtures de base
- **Impact :** `template/tests/conftest.py.jinja`

### ADAPTER — A moduler par profil

#### 8. Workflow de developpement

- **Source :** EgoVault (7 phases) + Etat de l'art (Research > Plan > Execute > Review > Ship)
- **Decision :** Le template inclut un workflow simplifie dans PILOT.md :
  Research > Plan > Implement > Test > Ship (5 phases, pas 7)
- **EgoVault ajoutait BRAINSTORM + AUDIT** = pertinent pour projets matures, pas bootstrap
- **Impact :** `template/.meta/PILOT.md.jinja`

#### 9. Surfaces multiples (API + CLI + MCP)

- **Source :** EgoVault
- **Decision :** Pas dans le template de base. Documenter comme pattern dans CLAUDE.md
  du profil `app` : "Si tu as besoin de plusieurs surfaces, suis le pattern ports & adapters"
- **Impact :** `template/CLAUDE.md.jinja` (section conditionnelle app)

### REJETER — Trop specifique ou over-engineered pour un bootstrap

#### 10. @loggable decorator avec callback injection

- Trop specifique a EgoVault. Le pattern est elegant mais pas generalisable a un bootstrap.

#### 11. Taxonomie config-driven

- Specifique aux projets avec classification utilisateur. Pas un pattern de template.

#### 12. Workflow 7 phases complet

- Over-engineered pour un bootstrap. Simplifie en 5 phases (voir #8).

#### 13. docs/superpowers/ lifecycle (specs/plans/audits/archive)

- Trop lourd. Le template genere `.meta/decisions/` pour les ADRs, c'est suffisant.

---

## Plan d'implementation

| Priorite | Action | Fichier impacte |
|----------|--------|-----------------|
| P0 | Reduire CLAUDE.md.jinja a <120 lignes | template/CLAUDE.md.jinja |
| P0 | Ajouter regles anti-LLM (G2, G5, G6, G13) | template/CLAUDE.md.jinja |
| P1 | Creer SESSION-CONTEXT.md.jinja | template/.meta/ |
| P1 | Enrichir PILOT.md.jinja (workflow 5 phases) | template/.meta/PILOT.md.jinja |
| P1 | Ajouter `_tasks` post-copy dans copier.yml | copier.yml |
| P2 | Generer tests/conftest.py minimal | template/tests/ |
| P2 | Config 3 niveaux pour profil app | template/config/ (conditionnel) |
| P3 | Explorer hooks Claude Code (.claude/settings.json) | template/.claude/ |
