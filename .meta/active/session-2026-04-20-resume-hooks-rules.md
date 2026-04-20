# RESUME HERE — 2026-04-20 (chantier hooks↔rules)

> **Si tu reprends cette conversation : LIS CE FICHIER EN PREMIER, puis les 3 docs cités.**

## Contexte en 30 secondes

Vincent a signalé que le scaffold généré par metadev-protocol casse au premier commit (15 erreurs ruff, voir `infra-home-server/.meta/drafts/template-ruff-report.md`). Cause racine : `line-length=88` uniforme + aucune règle dans `.claude/rules/` n'explique ce choix au LLM, donc il génère du code à 100 chars et le hook bloque.

Ça a ouvert un chantier plus large : **toute contrainte enforced (hook) doit avoir une règle lisible par le LLM, et inversement**. Sinon les hooks deviennent des pièges.

## Où on en est (3 docs produits aujourd'hui, dans `.meta/active/`)

1. **`spec-2026-04-20-hooks-rules-pairing.md`** — cahier des charges (phase 1) : doctrine, taxonomie 3 niveaux (`hard-block` / `soft-warn` / `advisory`), politique de strictness différenciée par catégorie de fichier (src/=100, scripts/=120, tests/=120), patterns timing (branche AVANT edit, etc.). **Status : DRAFT, pas encore validé formellement par Vincent.**

2. **`synthesis-2026-04-20-hooks-rules-audit.md`** — audit complet du repo (phase 2) : 33 hooks + 57 règles inventoriés. **6 hooks critiques sans règle (G1-G5)**, **9 règles hard-block sans hook (G7-G15)**, **1 conflit doctrinal C1** (R023 trunk-based ↔ H013 no-commit-to-main). Plan d'action en 4 PR proposé.

3. **`debate-2026-04-20-hooks-rules-doctrine.md`** — débat sur les 4 décisions ouvertes. **Recos finales validées par l'orchestrateur (pas encore par Vincent)** :
   - **D1** : Hybride YAML frontmatter + blockquote header dans le body (DX + parsing)
   - **D2** : `conventional-pre-commit` (Python, pas Node)
   - **D3** : PR strictement séquentielles, mais PR-1 ship un stub doc minimal pour éviter LLM-blind gap
   - **D4** : Toujours générer la règle multi-host + prose marker (pas de Jinja conditionnelle)

## URGENT — backlog prioritaire après PR-2

**CI cassée sur `main` depuis ~1 semaine** (screenshot Vincent 2026-04-20) :
- `CI #15-#22` fails systématiquement (lint ou pre-commit)
- `Public safety audit #14-#22` fails systématiquement

Hypothèse : même cause racine que le bootstrap cassé (line-length 88 trop strict), PR-1 pourrait déjà le fixer. Sinon investigation dédiée juste après PR-2. Candidat "over-hard-hook" à démoter dans PR-3/PR-4.

## Prochaine étape (où on s'est arrêtés)

Vincent doit valider les 4 recos du débat. Ensuite le séquençage prévu était :

1. **Validation Vincent** des 4 recos D1-D4
2. **Question encore ouverte** : PR-1+PR-2 dans la même session (gap <1h) ou en 2 sessions ? Si en 2, PR-1 doit ship stub.
3. **`librarian` agent** pour vérifier les claims état de l'art (PEP 257 ne fixe pas de limite de docstring ✓ à confirmer, Google styleguide = 100 chars ✓ à confirmer, sources précises pour justifications dans les nouvelles règles)
4. **`/plan`** sur PR-1 (strictness ruff `pyproject.toml.jinja` + fix 2 SIM108) + PR-2 (créer 5 nouvelles règles `template/.claude/rules/`: linting, skills-contract, multi-host, branching, secrets)
5. **Exécution** avec `code-reviewer` agent auto-trigger en fin (≥3 fichiers touchés)
6. **`security-auditor`** sur la nouvelle `secrets.md` (auth/secrets trigger)
7. **PR-3** (hooks manquants : conventional-pre-commit + ruff rules BLE/TRY)
8. **PR-4** (doctrine cleanup, anti-patterns log, conflit C1 résolu)
9. Bump semver + tag annoté à chaque PR mergée

## Cleanup `.meta/` à faire (signalé en cours de session)

**`.meta/active/` (stale, à archiver)** :
- `brainstorm-2026-04-13-radar-skill.md` + `plan-2026-04-13-radar-skill.md` → DONE en v1.2.0, absorbé `/tech-watch` v1.6.0

**`.meta/drafts/` (status à clarifier)** :
- `brainstorm-skill-discoverability.md` → DONE PM.7 v1.1.0, à supprimer
- `plan-workflow-gates.md` → probablement DONE 0.1
- `plan-meta-visibility.md` → probablement DONE 0.2
- `migration-triage.md`, `monorepo-workspace-bootstrap.md` → status inconnu, à trier

**`.meta/active/` valides** :
- `plan-2026-04-13-outreach-messages.md` + `plan-2026-04-13-outreach-tracking.md` → prêts pour Phase 4 launch (4.6 demo GIF + 4.7 launch sequence TODO dans PILOT)

## Backlog non-specqué (PILOT)

- 4.6 Record demo GIF (vhs install requis)
- 4.7 Public launch sequence
- PM.5 Provenance sidecar convention (PENDING)
- PM.16 `--persist` flag /tech-watch (BACKLOG)

## Notes pour la prochaine session

- Vincent travaillait depuis `infra-home-server` (premier vrai dogfood du template, c'est lui qui a mis le bug en évidence)
- La doctrine "hooks sans règle = pièges" est une vraie découverte structurelle, à intégrer dans les ADR (`adr-012-hooks-rules-pairing.md` à créer après validation phase 1)
- L'audit a confirmé que cette session a généré beaucoup de drafts non triés — opportunité pour `/save-progress` skill plus tard

---

**Ordre de lecture recommandé pour la session de reprise** :
1. Ce fichier (`session-2026-04-20-resume-hooks-rules.md`)
2. `spec-2026-04-20-hooks-rules-pairing.md`
3. `synthesis-2026-04-20-hooks-rules-audit.md` (au moins section 1 matrice + section 3 plan)
4. `debate-2026-04-20-hooks-rules-doctrine.md` (section "Final recommendation")
