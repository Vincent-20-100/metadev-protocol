# GOLD — Vibe Coding Best Practices

> Synthese de : state-of-the-art-vibe-coding.md, top-repos-and-voices.md,
> linkedin-curated-posts.md, audit-egovault.md, dev-workflow-skills-patterns.md
> Date : 2026-04-01

---

## Le cadre mental

Le vibe coding en 2026 n'est plus du "laisser l'IA coder". C'est une discipline
avec des patterns valides et des anti-patterns documentes.

**Le ratio realiste :** L'IA ecrit 60-70% du first draft. Le reste = review,
refactor, integration. 45% du code IA contient des vulnerabilites secu.

**Source :** state-of-the-art-vibe-coding.md

---

## Les 5 principes fondamentaux

### 1. Research before code

Chercher/lire la doc AVANT de generer du code. L'exploration structuree bat
l'hallucination. Claude avec une skill `/brainstorm` qui force l'exploration
est 10x plus fiable que Claude qui fonce.

**Source :** everything-claude-code (search-first skill), Superpowers (brainstorming).

### 2. Hooks > Instructions

Les regles critiques (formatting, lint, fichiers interdits) sont des hooks
automatiques, pas des lignes dans CLAUDE.md.
- CLAUDE.md = compliance ~70-80%
- Hooks = compliance 100%

**Source :** Boris Cherny, state-of-the-art-vibe-coding.md

### 3. Progressive disclosure

Tout n'a pas besoin d'etre en contexte tout le temps.
- CLAUDE.md = toujours charge (le garder court)
- Skills = chargees a la demande (le gros du workflow)
- Subagents = contexte isole (les explorations)

**Source :** Doc officielle, leak (108 feature flags).

### 4. Verification > Generation

Fournir des criteres de verification (tests, screenshots, outputs attendus).
Sans criteres, Claude produit du code plausible mais casse.

**Source :** state-of-the-art-vibe-coding.md (finding #4).

### 5. Separer le produit du process

Le code (src/, tests/) est le livrable. Le cockpit (.meta/) est l'espace de
travail. Les deux ne se melangent jamais.

**Source :** Philosophie metadev-protocol, EgoVault, Pattern Superpowers.

---

## Red Zone / Green Zone

| Zone | Exemples | Regle |
|------|----------|-------|
| **Green** (IA excelle) | UI, CRUD, refactoring, tests, docs | Laisser Claude generer |
| **Red** (IA risquee) | Auth, crypto, financier, sanitization | Claude propose, humain verifie |

**Source :** state-of-the-art-vibe-coding.md. A documenter dans CLAUDE.md des profils
sensibles (app, quant).

---

## Anti-patterns documentes

### 1. Guess-and-check debugging
L'IA essaie des trucs au hasard au lieu de diagnostiquer.
**Fix :** Skill `/debug` avec 4 phases (evidence AVANT fix).

### 2. Over-engineering
L'IA cree des abstractions prematurees, factories de factories.
**Fix :** Regle R5 dans CLAUDE.md + YAGNI dans `/brainstorm`.

### 3. Context stuffing
Mettre trop d'instructions dans CLAUDE.md → compliance chute.
**Fix :** CLAUDE.md < 120 lignes, detail dans skills.

### 4. Silent exceptions
`except: pass` partout.
**Fix :** Regle R6 dans CLAUDE.md + hook ruff (ruff peut detecter certains bare except).

### 5. Blind trust
Accepter le code IA sans verifier.
**Fix :** Skill `/review` en subagent fork + `/ship` avec checklist.

### 6. Session amnesia
Perdre le contexte entre les sessions.
**Fix :** Cockpit 2 fichiers (PILOT.md + SESSION-CONTEXT.md rewrite).

### 7. Scope creep
L'IA ajoute des features non demandees.
**Fix :** Skill `/brainstorm` avec YAGNI, `/spec` avec scope defini.

---

## Workflow optimal

```
/brainstorm  →  /spec  →  /plan  →  /implement  →  /test  →  /review  →  /ship
     ↑                                                            |
     └────────────── feedback loop si review echoue ──────────────┘
```

Chaque etape produit un artefact dans `.meta/scratch/` ou directement dans le code.
La boucle de feedback revient au brainstorm si le probleme est fondamental,
ou au plan si c'est un probleme d'execution.

---

## Metriques de qualite

| Metrique | Comment mesurer | Cible |
|----------|----------------|-------|
| CLAUDE.md taille | `wc -l CLAUDE.md` | < 120 lignes |
| Tests | `uv run pytest` | 100% pass |
| Lint | `uv run ruff check .` | 0 erreur |
| Coverage | `uv run pytest --cov` | > 80% (profil app) |
| SESSION-CONTEXT.md fraicheur | Date dans le fichier | < 1 session |

---

## Voix de reference

| Personne | Pourquoi l'ecouter |
|----------|-------------------|
| **Boris Cherny** | Createur Claude Code, CLAUDE.md sizing |
| **Jesse Vincent (obra)** | Createur Superpowers, workflow skills |
| **affaan-m** | everything-claude-code, hackathon winner |
| **Andrej Karpathy** | A popularise "vibe coding" |
| **Simon Willison** | Analyses techniques IA, tooling |
| **Wilfried de Renty** | Architecture agents IA (MCP/Skills/Memoire) |
| **swyx** | Syntheses AI engineering |
