# GOLD — Skills : Workflow de dev + Utilitaires

> Synthese de : dev-workflow-skills-patterns.md, superpowers-and-everything-claude-code.md,
> github-skills-landscape.md, claude-code-hooks-skills-reference.md
> Date : 2026-04-01

---

## Le principe fondamental

**Les skills sont le bon endroit pour le workflow de dev.** Pas CLAUDE.md (trop court,
toujours charge), pas des hooks (trop rigides). Les skills sont chargees a la demande,
partagees via git, et composables en pipeline.

**Source :** Superpowers (130K stars) a prouve que 14 skills focalisees > 80+ skills generiques
(everything-claude-code). La qualite bat la quantite.

---

## Skills de workflow — Le pipeline

Chaque skill nourrit la suivante. L'output de brainstorm → input de spec → input de plan.

### 1. /brainstorm — Exploration structuree

**Ce que ca fait :**
- Pose UNE question a la fois (pas de liste de 10)
- Force 2-3 alternatives pour chaque decision
- Applique YAGNI agressivement (coupe le scope creep)
- Interdit de coder pendant le brainstorm

**Pourquoi c'est critique :**
- Le piege #1 des LLM : foncer dans l'implementation sans explorer les alternatives
- Le brainstorm socratique force a considerer des approches qu'on aurait ignorees

**Output :** Decisions cles + alternatives rejetees (avec raisons) → `.meta/scratch/brainstorm.md`

**Confiance : TRES ELEVEE** — 130K stars, Vincent l'utilise quotidiennement.

### 2. /spec — Specification concrete

**Ce que ca fait :**
- Test de "l'ingenieur junior enthousiaste" : si un dev junior ne peut pas
  implementer depuis la spec, elle n'est pas assez concrete
- Definit les inputs, outputs, edge cases
- Identifie les fichiers a creer/modifier

**Pourquoi c'est critique :**
- Sans spec, Claude improvise. Avec spec, Claude execute.
- La spec est le contrat entre le "toi qui decide" et le "Claude qui code"

**Output :** Spec actionnable → `.meta/scratch/spec.md`

**Confiance : ELEVEE** — Pattern Superpowers valide.

### 3. /plan — Decomposition en taches

**Ce que ca fait :**
- Mappe TOUS les fichiers concernes avant de definir les taches
- Decoupe en chunks de 2-5 minutes
- Chaque tache a : fichier(s), quoi faire, comment verifier
- Ecrit le plan dans un fichier (pas dans le chat)

**Pourquoi c'est critique :**
- Planning-with-files (OthmanAdi, 17K stars) prouve que l'externalisation
  du plan dans un fichier > le plan dans le contexte
- Les chunks de 2-5 min evitent les taches ambigues

**Output :** Plan ordonne → `.meta/scratch/plan.md`

**Confiance : TRES ELEVEE** — Confirme par Superpowers + OthmanAdi + leak (ULTRAPLAN).

### 4. /implement (ou /execute)

**Ce que ca fait :**
- Execute le plan tache par tache
- Checkpoint apres chaque tache (verification)
- Si une tache echoue, stop et diagnostique au lieu de continuer

**Pourquoi c'est critique :**
- Empeche Claude de devier du plan
- Les checkpoints attrapent les erreurs tot

**Output :** Code + tests implementes, plan mis a jour

**Confiance : ELEVEE** — Pattern Superpowers (executing-plans).

### 5. /tdd — Test-Driven Development

**Ce que ca fait :**
- Cycle RED-GREEN-REFACTOR enforce
- Regle dure : "delete code written before tests"
- Multi-agent : un agent ecrit les tests, un autre implemente (contextes separes)

**Pourquoi c'est critique :**
- Adresse directement la rationalisation LLM ("j'ecris le test apres")
- La separation multi-agent empeche la pollution de contexte

**Output :** Tests + implementation

**Confiance : ELEVEE** — Pattern Superpowers, mais le multi-agent est avance.
Pour un bootstrap, le cycle RED-GREEN-REFACTOR sans multi-agent suffit.

### 6. /review — Code review

**Ce que ca fait :**
- 2 etapes separees : spec compliance PUIS qualite code
- Execute en subagent fork (isole du contexte principal)
- Ne resume PAS le workflow dans la description (sinon Claude prend des raccourcis)

**Pourquoi c'est critique :**
- La review en subagent fork est quasi gratuite en tokens (cache prompt)
- La separation spec/qualite evite de tout melanger

**Output :** Liste de findings avec severite

**Confiance : ELEVEE** — Pattern Superpowers, confirme par le fork model du leak.

### 7. /debug — Debugging systematique

**Ce que ca fait :**
- 4 phases strictes, sequentielles :
  1. EVIDENCE — collecter les faits (logs, traces, repro)
  2. HYPOTHESES — lister les causes possibles
  3. TEST — verifier les hypotheses une par une
  4. FIX — corriger seulement quand la cause est prouvee
- Phase 1 DOIT etre complete avant toute tentative de fix

**Pourquoi c'est critique :**
- Anti-pattern #1 des LLM : guess-and-check loops (essayer des trucs au hasard)
- Forcer l'evidence d'abord elimine 80% des fausses pistes

**Output :** Diagnostic + fix

**Confiance : TRES ELEVEE** — Le guess-and-check est le probleme le plus courant.

### 8. /ship — Pre-commit + handoff

**Ce que ca fait :**
- Checklist : tests passent, lint clean, pas de fichiers oublies
- Met a jour PILOT.md (statut)
- Reecrit SESSION-CONTEXT.md (contexte pour la prochaine session)
- Document de handoff avec rationale (pas juste "fixed bug")

**Pourquoi c'est critique :**
- C'est la frontiere entre "en cours" et "livre"
- Le handoff structure garantit que la prochaine session demarre proprement

**Output :** Commit + fichiers .meta/ mis a jour

**Confiance : ELEVEE** — Combine nos patterns existants avec le handoff de Superpowers.

---

## Skills utilitaires — Quotidien

### 9. /test — Runner pytest (DEJA FAIT)

Invoque `uv run pytest` avec args optionnels, decode les resultats.

### 10. /lint — Ruff check + format (A FAIRE)

Invoque `uv run ruff check . --fix && uv run ruff format .`, rapporte les changements.

### 11. /consolidate — Reecriture SESSION-CONTEXT.md (A FAIRE)

Aide a reecrire SESSION-CONTEXT.md en fin de session. Inspire d'autoDream (leak) :
- Prend le contexte de la session courante
- Extrait les decisions, les pieges, les questions ouvertes
- Reecrit le fichier (pas complete)

---

## Skills meta — Avancees (T3)

### 12. /learn — Auto-extraction de patterns

Apres une session, extraire les patterns reusables en micro-skills.
Source : everything-claude-code (continuous learning pipeline).

### 13. /digest — Transformer source raw en key takeaways

Prend un fichier de reference brut, extrait les takeaways structures.
C'est le skill que Vincent vient de demander.

---

## Ce qu'on NE fait PAS en skills

| Idee | Pourquoi non |
|------|-------------|
| 36 agents dedies | Over-kill, everything-claude-code prouve que c'est du bloat |
| Skills par langage | On est Python-only |
| Skills business (market-research, investor-materials) | Hors scope template de dev |
| 68 legacy commands | Maintenance impossible |

---

## Classification finale

| Tier | Skills | Scope |
|------|--------|-------|
| **T1 FONDATION** | /brainstorm, /plan, /test, /ship | VANILLA |
| **T2 RECOMMANDE** | /spec, /tdd, /review, /debug, /lint, /consolidate | VANILLA |
| **T3 AVANCE** | /learn, /digest, /implement | VANILLA |
| **PROFILE** | /api-test, /pipeline-run, /backtest | Par profil |
