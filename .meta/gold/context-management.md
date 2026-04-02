# GOLD — Gestion de contexte

> Synthese de : context-management-patterns.md, claude-code-leak-analysis.md,
> claude-code-hooks-skills-reference.md, state-of-the-art-vibe-coding.md
> Date : 2026-04-01

---

## Le probleme

Claude Code a une fenetre de contexte finie (~200K tokens). Quand elle se remplit :
- A 70% : la precision commence a baisser
- A 85% : les hallucinations augmentent
- A 90%+ : comportement erratique
- A ~95% : compaction automatique (lossy — perte d'information)

**Source :** state-of-the-art-vibe-coding.md, confirme par le leak (5 strategies de compaction).

---

## Les 3 axes de gestion

### Axe 1 — Prevenir le remplissage

| Pattern | Ce que ca fait | Comment | Confiance |
|---------|---------------|---------|-----------|
| **CLAUDE.md court (<120 lignes)** | Moins de tokens charges a chaque prompt | Fait — 57-63 lignes | TRES ELEVEE |
| **Skills a la demande** | Chargees uniquement quand invoquees | Fait — progressive disclosure | TRES ELEVEE |
| **Subagent pour investigation** | Isole les recherches verbeuses hors du contexte | A documenter dans CLAUDE.md | ELEVEE |
| **Regle du >5 fichiers** | Si exploration de >5 fichiers → subagent | A documenter | ELEVEE |
| **Path-scoped rules** | Instructions par sous-dossier, chargees a la demande | T3 — `.claude/rules/` | MOYENNE |

### Axe 2 — Survivre a la compaction

| Pattern | Ce que ca fait | Comment | Confiance |
|---------|---------------|---------|-----------|
| **Hook post-compact** | Re-injecte PILOT.md apres compaction | Fait — SessionStart compact | ELEVEE |
| **Instruction dans CLAUDE.md** | "Preserver fichiers modifies + commandes test" | A ajouter | ELEVEE |
| **Planning-with-files** | Plan/context dans des fichiers .meta/, pas dans le chat | A integrer dans /plan | TRES ELEVEE |
| **Checkpoint verification** | Verifier apres chaque etape, pas en fin | A integrer dans /implement | ELEVEE |

### Axe 3 — Persister entre sessions

| Pattern | Ce que ca fait | Comment | Confiance |
|---------|---------------|---------|-----------|
| **SESSION-CONTEXT.md (rewrite)** | Contexte decisionnel reecrit chaque session | Fait | TRES ELEVEE |
| **PILOT.md (accumulate)** | Etat factuel mis a jour chaque session | Fait | TRES ELEVEE |
| **Auto Memory (MEMORY.md)** | Built-in Claude Code v2.1.59 | Natif — pas besoin de template | REFERENCE |
| **Handoff structure** | Document de passation en fin de session | A integrer dans /ship | ELEVEE |
| **/consolidate skill** | Aide a reecrire SESSION-CONTEXT.md | A creer | MOYENNE |

---

## Les 5 strategies de compaction (du leak)

| # | Nom | Quand | Perte |
|---|-----|-------|-------|
| 1 | Micro compact | Time-based, vieux resultats d'outils | Faible |
| 2 | Context collapse | Resumer des spans de conversation | Moyenne |
| 3 | Session memory | Extraire le contexte cle dans un fichier | Faible |
| 4 | Full compact | Reecriture complete du contexte | Elevee |
| 5 | Clear | Reset total | Totale |

**Ce qu'on fait pour chaque :**
- 1-2 : Automatique, pas de controle direct
- 3 : Notre SESSION-CONTEXT.md + hook post-compact
- 4 : Le hook re-injecte PILOT.md pour limiter la perte
- 5 : L'user doit manuellement relire les fichiers .meta/

---

## Actions concretes pour le template

### Deja fait
- CLAUDE.md court (57-63 lignes)
- Skills progressive disclosure
- SESSION-CONTEXT.md rewrite pattern
- Hook post-compact (re-injection PILOT.md)

### A ajouter dans CLAUDE.md (1 ligne)
```
Quand le contexte est compresse, preserve la liste des fichiers modifies et les commandes de test.
```

### A ajouter dans les skills
- `/plan` ecrit dans `.meta/scratch/plan.md` (pas dans le chat)
- `/ship` inclut un handoff structure
- `/consolidate` aide a reecrire SESSION-CONTEXT.md

### A documenter dans CLAUDE.md (1-2 lignes)
```
Pour les explorations de >5 fichiers, utilise un subagent (contexte isole).
```

---

## Ce qu'on NE fait PAS

| Pattern | Pourquoi non |
|---------|-------------|
| MCP memory server | Trop complexe pour un bootstrap, natif MEMORY.md suffit |
| Hook profiles (minimal/standard/strict) | Over-engineering, un seul profil suffit |
| Token counting UI | Gere par Claude Code nativement |
| Auto-compact dirigee | Trop intrusif, la compaction auto suffit |
