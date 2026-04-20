---
type: spec
date: 2026-04-20
slug: research-architecture
status: DRAFT
---

# Spec — Research architecture v2.1

**Date:** 2026-04-20
**Status:** DRAFT
**Target tag:** v2.1.0

---

## Objective

Unifier la stack de recherche autour de deux skills jumeaux (`/research` + `/tech-watch`), un schéma d'output partagé à 3 tiers de densité (briefs/analyses/sources), un catalog versionné pour déduplication, et des scripts de curation déterministes. Objectif final : permettre des campagnes de recherche reproductibles, résilientes aux crashes, et économes en contexte via un pattern d'augmentation progressive de mémoire.

## Context

Déclencheur : Vincent a signalé (session 2026-04-20) que la stack `/research` actuelle n'est pas viable pour une recherche en profondeur sur ≥10 cibles — les subagents qui plantent font perdre toute la session, le format "card" hérité de `/tech-watch` est opaque, et il n'y a aucun mécanisme de dedup. En parallèle, l'architecture mémoire multi-étages (briefs/analyses/sources) émerge comme solution au context rot observé sur les sessions longues. Ce spec formalise l'ensemble pour ship en v2.1.0.

---

## Requirements (MoSCoW)

### MUST

**Architecture & taxonomie**
- Deux axes orthogonaux : **maturité** (existing `raw/` → `interim/` → `synthesis/`) × **densité** (new tiers `briefs/` T1 + `analyses/` T2 + `sources/` T3)
- Batch comme unité atomique : `raw/batch-<YYYY-MM-DD>-<slug>/` pour toute recherche (mono ou multi-cible)
- Vocabulaire "card" supprimé partout, remplacé par brief/analysis/source

**Skills jumeaux**
- `/research` et `/tech-watch` partagent le même output-schema et le même catalog
- Output identique du point de vue du projet, mécanique interne différente
- `output-schema.md` owned by `/research`, référencé par `/tech-watch`, parité enforce par contract check

**Modes**
- `/research` light (défaut) : briefs + sources (no analyses)
- `/research --deep` : briefs + analyses + sources
- `/research --batch` ou multi-cible : hérite du mode par cible
- `/tech-watch --deep <url>` : deep mode, même output shape

**Résilience**
- `agent.md` dans `/research` : contrat subagent unitaire avec pré-écriture du squelette + edits incrémentaux (no memory accumulation)
- Écriture T3 source immédiatement après WebFetch, puis T1 brief, puis T2 analysis (si deep), puis update `_index.md`
- Failure mode : `status: partial` avec section `## Limitations`, jamais de perte silencieuse

**Dedup catalog**
- `.meta/references/_catalog.json` versionné, unifié (/research + /tech-watch)
- Check pré-analyse via `scripts/research_curate/check.py`, strict URL normalisation
- Fraîcheur 30 jours par défaut, `--max-age Nd` configurable
- Fresh hit → skip + lien vers brief existant (LLM lit brief directement, compatible ADR-011)
- Stale hit → prompt `--force` (refait) ou `--update` (V2, backlog PM.18)
- Forked/renamed repos : résolution GitHub API pour URL canonique avant normalisation

**Scripts curation (déterministes, no new skill)**
- `scripts/research_curate/promote.py` — batch/briefs/X → interim/card-<date>-<slug>.md (frontmatter patché)
- `scripts/research_curate/cleanup.py` — purge sources/ par TTL (`--older-than Nd`) ou par batch (`--batch <id>`), `--dry-run` default
- `scripts/research_curate/reorg.py` — rename/move entre tiers et batchs
- `scripts/research_curate/index.py` — maintien `_index.md` (batch-local) et `_catalog.json` (global)
- `scripts/research_curate/check.py` — dedup pré-analyse, exit codes 0=no hit / 1=fresh / 2=stale / 3=error, JSON par défaut (`--human` markdown)
- Tous invoqués via `uv run python -m scripts.research_curate.<cmd>`

**Versioning & gitignore**
- Tracké : `_catalog.json`, `briefs/`, `analyses/`, `_index.md`, `interim/`, `synthesis/`
- Gitignored : `raw/batch-*/sources/` (volumes verbatim, local-only)
- Patch `.gitignore` (meta) et `template/.gitignore.jinja` (conditionnel `meta_visibility == "public"`)

**Parité & contracts**
- Dual-maintenance meta↔template pour tous fichiers touchés (SKILL.md × 2, output-schema.md, agent.md, scripts/research_curate/*)
- `scripts/check_skills_contract.py` étendu : (a) vérifie référence output-schema dans les deux SKILL.md, (b) vérifie parité `scripts/research_curate/`
- `evals/harness_audit.py` ne doit pas régresser (invariant 60/60)

**Intégration librarian**
- Après stabilisation de la base (phase 7), le librarian agent intègre la lecture du `_catalog.json` pour proposer les briefs existants avant toute recherche conversationnelle
- Extension de `.claude/agents/librarian.md` pour documenter la nouvelle source de données

**Backlog PILOT**
- **PM.17** — Étendre `check_meta_naming.py` à `references/` (regex avec types `card|deep|batch|synthesis`). Reporté jusqu'à ≥3 batchs en prod ou drift observée.
- **PM.18** — `--update` mode pour re-analyse deep : diff entre brief existant + état actuel du repo, produit un delta brief. Backlog après MVP.
- **PM.19** — Unifier `/tech-watch` sweep output sous l'arbre batch (actuellement `references/research/`). Différé post-v2.1.

### SHOULD

- Cleanup `.meta/scratch/` vestige en commit séparé du même cycle (suppression gitignore + update ADR-002 SUPERSEDED + scan mentions)
- Migration optionnelle des `references/research/deep-*.md` existants vers le nouveau format au cutover v2.1

### COULD

- Statusline ou hook post-batch affichant le résumé du batch en CLI
- Extension librarian : alerter si un catalog entry est stale sur un sujet actif
- Dashboard `scripts/research_curate/report.py` : vue d'ensemble batchs, hits dedup, promotion rate

---

## Non-goals (explicites)

1. **Update mode (`--update`)** — différé en backlog PM.18. Le MVP se contente de skip/force.
2. **Auto-cleanup TTL via cron ou hook** — cleanup manuel uniquement.
3. **Promotion automatique basée sur heuristiques scorées** — la promotion reste un geste éditorial, pas algorithmique.
4. **Nouveau skill `/curate`** — scripts invoqués directement via `uv run`, pas de skill wrapper.
5. **Migration des `references/research/` legacy dans le MVP** — PM.19 en backlog, pas de migration forcée au v2.1.
6. **Dashboard ou UI de visualisation des batchs** — hors scope, à considérer si usage le justifie.
7. **Enforcement regex sur filenames dans `references/`** — PM.17 backlog.

---

## Proposed approach — 7 phases, 7 commits, tag v2.1.0

### Phase 1 — Schema & conventions
- `template/.claude/skills/research/output-schema.md` étendu : frontmatter commun + formats brief / analysis / source / `_index.md` / `_catalog.json`
- `template/.claude/skills/research/agent.md` (nouveau) : contrat subagent unitaire
- `template/.meta/GUIDELINES.md.jinja` : ajout section « Research stack — 2 axes orthogonaux (maturité × densité), twin skills, dedup catalog »
- Parité meta `.claude/skills/research/*`
- Commit : `docs(research): define unified output schema and subagent contract`

### Phase 2 — Curation scripts
- `template/scripts/research_curate/` : `__init__.py` + `__main__.py` + 5 modules (promote, cleanup, reorg, index, check)
- Tests unitaires minimaux (`template/tests/test_research_curate.py`)
- Parité meta `scripts/research_curate/*`
- Commit : `feat(research): add deterministic curation scripts`

### Phase 3 — Skills update
- `template/.claude/skills/research/SKILL.md` : modes light/deep/batch, invocation scripts curation, références output-schema et agent.md
- `template/.claude/skills/tech-watch/SKILL.md` : référence explicite output-schema partagé, vocabulaire "card" remplacé
- Parité meta × 2 skills
- Commit : `feat(research): unify /research and /tech-watch around shared schema`

### Phase 4 — Contract, gitignore, PILOT
- `template/scripts/check_skills_contract.py` + `scripts/check_skills_contract.py` : assertions référence output-schema + parité research_curate
- `template/.gitignore.jinja` + `.gitignore` : `raw/batch-*/sources/` exclus
- `.meta/PILOT.md` : ajout PM.17, PM.18, PM.19 dans Post-merge backlog
- Commit : `chore(research): extend contract check, gitignore, PILOT backlog`

### Phase 5 — Dogfood
- Lancer le premier batch réel `batch-2026-04-20-token-efficiency` (les 12 cibles du post LinkedIn) pour valider l'architecture en production
- Mode : deep pour chaque cible
- Vérifier résilience (simuler crash d'un subagent), dedup (relancer sur même cible → skip), curation (promouvoir 3-4 briefs vers interim/)
- Feedback loop : si bug, retour phase 1-3 avant phase 6
- Commit : `chore(research): dogfood first batch — token efficiency stack`

### Phase 6 — Cleanup vestige scratch/
- `.gitignore` : suppression ligne `.meta/scratch/`
- `.meta/ARCHITECTURE.md` : ADR-002 mis à jour pour refléter la structure actuelle, marquer SUPERSEDED la mention scratch/
- `template/.meta/GUIDE.md.jinja` et autres mentions : scan + cleanup
- Commit : `chore: remove scratch/ vestige and update ADR-002`

### Phase 7 — Librarian integration
- `template/.claude/agents/librarian.md` + miroir meta : documentation de la nouvelle source `_catalog.json`, convention « avant toute recherche externe, propose les briefs existants du catalog »
- Mise à jour trigger-table CLAUDE.md : ajouter ligne librarian "propose cached brief avant WebFetch"
- Test manuel : question conversationnelle sur un sujet déjà indexé → librarian retourne brief + confidence au lieu de forcer recherche
- Commit : `feat(librarian): integrate catalog-aware brief retrieval`

### Tag release
- `git tag -a v2.1.0 -m "..."` avec changelog listant : twin skills, 3-tier batch architecture, dedup catalog, curation scripts, librarian integration, scratch/ cleanup
- Push tag
- Update `.meta/PILOT.md` section "Current state" avec v2.1.0 shipped

---

## Resolved open questions

| # | Question | Résolution |
|---|---|---|
| 1 | Frontmatter fields | `type` (brief\|analysis\|source\|index\|catalog) + `date` + `slug` + `target_slug` + `batch_id` + `tier` (T1/T2/T3) + `mode` (light/deep) + `status` + `sources` (array) + `promoted_from` (optional) |
| 2 | Brief section layout | 5 sections max : **What** / **Why it matters** / **Key findings** (3-7 bullets) / **Trade-offs** / **Integration hint** (for metadev) |
| 3 | Analysis section layout | Mirror brief étendu : **Context** / **Detailed findings** (subsections par thème) / **Verbatim citations** / **Code samples** / **Integration details** |
| 4 | Source section layout | Frontmatter (url, date_accessed, sha256, content_type) + verbatim body + footer `--- END SOURCE ---` |
| 5 | Promotion criteria | Manual LLM judgment guidé par checklist (signal fort ≥2 sources indépendantes, unicité, applicabilité metadev, freshness, non-redondance avec curated existant) — pas de score numérique |
| 6 | Batch naming slugs | Kebab, regex `[a-z][a-z0-9-]{2,49}`, max 50 chars, pas de date dans le slug (déjà dans le dir name) |
| 7 | Subagent wave size | **4 en parallèle** par défaut, `--wave-size N` configurable |
| 8 | check.py output format | JSON par défaut (script-friendly), `--human` flag pour markdown LLM-friendly. Exit codes : 0=no hit, 1=fresh hit (skip), 2=stale hit (update proposé), 3=error |
| 9 | Forked/renamed repos | Résolution GitHub API pour URL canonique avant normalisation. Archived repos acceptés mais flaggés `archived: true` dans catalog |
| 10 | /tech-watch sweep migration | **Reste dans `references/research/`** pour le MVP. Entrée backlog PM.19 pour unifier en v2.2 si besoin |

---

## Remaining open questions (à trancher pendant le plan ou implementation)

- **OQ-1** — Format exact du frontmatter YAML pour `_catalog.json` vs Markdown frontmatter : JSON natif ou YAML-in-Markdown pour lisibilité diff ? (reco : JSON pour `_catalog.json`, YAML frontmatter pour les .md)
- **OQ-2** — Stratégie de merge sur conflit catalog (deux machines push en parallèle) : last-write-wins / union sémantique / manuel. Probablement hors scope MVP.
- **OQ-3** — Script `check.py` : normalisation URL fait-elle un HEAD request pour valider 200 ou juste un parse syntaxique ? Trade-off latency vs exactitude.
- **OQ-4** — Phase 5 dogfood : si le batch échoue, rollback automatique des phases 1-4 ou fix forward ? Probablement fix forward (chaque phase est bisectable).
- **OQ-5** — Harness audit : faut-il ajouter une 7e catégorie « Research stack » au scorecard (au-delà de Skills/Agents/Hosts/Contract/Taxonomy/Safety) ou étendre les existantes ?

---

## Impact downstream

- **Versioning** : v2.0.0 → v2.1.0, breaking migration pour projets externes via `copier update`. Documenté dans CHANGELOG.md avec section migration (ajout dirs, ajout scripts, renommage vocabulaire).
- **Harness audit** : invariant 60/60 à préserver, OQ-5 à résoudre pendant le plan.
- **Contract check** : nouveau points de vérification = plus de sécurité mais plus de surface à maintenir. Acceptable.

---

## Next step

Lancer `/plan` sur ce spec pour décomposer chaque phase en tâches concrètes avec estimation, puis exécuter.

Plan d'exécution à produire : fichier `.meta/active/plan-2026-04-20-research-architecture.md` (slug lineage avec ce spec).
