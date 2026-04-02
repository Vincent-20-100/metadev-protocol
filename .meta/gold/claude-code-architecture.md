# GOLD — Architecture Claude Code (leak + doc officielle)

> Synthese de : claude-code-leak-analysis.md, claude-code-security-deepdive.md,
> claude-code-undercover-mode.md, claude-code-hooks-skills-reference.md
> Date : 2026-04-01

---

## Vue d'ensemble

Claude Code est un harness de 512K lignes TypeScript (~1900 fichiers) qui enveloppe
le modele Claude. Ce n'est PAS le modele — c'est l'orchestration qui lui donne
la capacite d'utiliser des outils, gerer des fichiers, et coordonner des agents.

---

## Architecture en couches

```
User ──→ CLI/IDE ──→ Settings + Permissions ──→ Tool System ──→ QueryEngine ──→ Claude API
              ↑              ↑                       ↑
          Skills       Hooks (pre/post)        Context Compaction
              ↑              ↑                       ↑
         .claude/       settings.json          Prompt Cache
```

### 1. Tool System (~40 outils)

Chaque capacite (file read, bash, web fetch, LSP) est un outil discret permission-gated.
- Read-only operations : execution concurrente
- Mutating operations : execution serielle (evite les conflits)
- Base tool definition : 29K lignes TypeScript

**Implication template :** Nos permissions dans settings.json controlent exactement
ce systeme. `allow` et `deny` gatent les outils individuels.

### 2. Permission System (25+ validateurs bash)

Pipeline de securite en cascade :
1. Regex matching
2. shell-quote parsing
3. tree-sitter AST analysis
4. 23 checks numerotes dans bashSecurity.ts
5. 18 builtins Zsh bloques
6. Detection injection Unicode zero-width + IFS null-byte

**Point critique :** Certains validateurs (ex: validateGitCommit) retournent "allow"
qui court-circuite TOUS les validateurs suivants.

**Implication template :** Nos deny permissions sont une couche supplementaire
au-dessus de ce systeme. Elles ne le remplacent pas.

### 3. QueryEngine (~46K lignes)

Le coeur : streaming, tool loops, token tracking, prompt caching, retry logic.
Gere le cache prompt de maniere tres agressive (14 cache-break vectors surveilles).

**Implication template :** On ne touche pas a ca. Mais nos hooks et skills
doivent eviter de casser le cache prompt (pas de changements frequents de mode).

### 4. Multi-Agent (3 modeles)

| Modele | Comment ca marche | Quand l'utiliser |
|--------|------------------|-----------------|
| **Fork** | Copie identique du contexte parent, cache prompt | Review, exploration, investigation |
| **Teammate** | Communication par fichier-mailbox entre panes | Travail collaboratif long |
| **Worktree** | Git branch isolee par agent | Dev parallele sur features differentes |

**Implication template :**
- Skill `/review` avec `context: fork` = quasi gratuit (cache)
- Skill `/brainstorm` en main context (besoin d'interaction)
- Skill `/plan` en main context (l'user doit valider)

### 5. Context Compaction (5 niveaux)

Voir gold/context-management.md pour le detail.

---

## Features cachees (leak)

### KAIROS — Agent autonome 24/7
- Daemon background avec `<tick>` periodiques
- GitHub webhooks pour reactions automatiques
- Logs append-only journaliers
- **Status :** Non release, 150+ references dans le code
- **Implication :** Confirme que l'agent-as-daemon est la direction. Pas actionnable pour nous.

### autoDream — Consolidation memoire
- Subagent fork en background
- Fusionne observations, supprime contradictions, convertit insights → faits
- Bash read-only (peut lire le projet, pas modifier)
- **Implication :** C'est notre SESSION-CONTEXT.md en automatise. Notre skill
  `/consolidate` est la version manuelle de ce pattern.

### ULTRAPLAN — Planification remote
- Offload vers session CCR (Opus 4.6, 30 min de reflexion)
- Resultat teleporte localement via sentinel `__ULTRAPLAN_TELEPORT_LOCAL__`
- **Implication :** Confirme que la planification doit etre externalisee
  (dans un fichier, pas dans le chat). Notre `/plan` → `.meta/scratch/plan.md`.

---

## Systeme de hooks (officiel)

### Events les plus utiles

| Event | Ce qu'on en fait |
|-------|-----------------|
| **PostToolUse (Edit\|Write)** | Auto-ruff format (FAIT) |
| **SessionStart (compact)** | Re-injection PILOT.md (FAIT) |
| **SessionStart (startup)** | Potentiel : afficher le status du projet |
| **PreToolUse (Bash)** | Potentiel : audit log des commandes |
| **Stop** | Potentiel : rappeler de mettre a jour SESSION-CONTEXT.md |

### Schema de decision des hooks

```
Exit 0 → Succes, stdout parse en JSON
Exit 2 → Erreur bloquante, stderr envoye a Claude comme feedback
Autre  → Non-bloquant, stderr en verbose seulement
```

---

## Systeme de skills (officiel)

### Format SKILL.md

```yaml
---
name: skill-name
description: Description courte (toujours en contexte)
allowed-tools: Bash(uv *), Read, Edit(src/**)
context: fork          # Optionnel : execute en subagent isole
agent: Explore         # Optionnel : type d'agent
---

Instructions completes (chargees a la demande uniquement)
```

### Regles de design

1. **Description courte** — toujours en contexte, doit declencher le bon chargement
2. **Ne PAS resumer le workflow dans la description** — sinon Claude prend des raccourcis
3. **Max 500 lignes** de body
4. **Substitutions :** `$ARGUMENTS`, `$0`, `$1`, `${CLAUDE_SKILL_DIR}`
5. **`context: fork`** = execute en subagent isole (pas d'impact sur le contexte principal)
6. **`disable-model-invocation: true`** = seulement invocable par l'user (pas auto)

---

## Ce que le leak valide dans notre approche

| Notre choix | Confirmation du leak |
|-------------|---------------------|
| settings.json avec permissions | Le tool system est permission-gated |
| Hooks auto-ruff | Les hooks PostToolUse sont le pattern standard |
| Skills en SKILL.md | Le format est officiel et stable |
| Progressive disclosure | 108 feature flags = tout est charge a la demande |
| SESSION-CONTEXT.md rewrite | autoDream fait exactement ca en automatise |
| Plan dans un fichier | ULTRAPLAN externalise la planification |
| Review en fork | Le fork model est quasi gratuit (cache prompt) |
