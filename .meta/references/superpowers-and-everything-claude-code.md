# Superpowers & Everything Claude Code — Research

> Date : 2026-04-01
> Source : GitHub repos, web research

---

## 1. Superpowers (obra / Jesse Vincent)

**URL :** https://github.com/obra/superpowers
**Stars :** ~130K | **Version :** v5.0.7 (mars 2026) | **Licence :** MIT

### Ce que c'est

Un **plugin Claude Code** (aussi compatible Cursor, Codex, Gemini CLI) qui fournit un workflow
de dev complet sous forme de skills composables. Utilise le systeme de plugins officiel
(`.claude-plugin/` avec manifest).

### Installation

```bash
/plugin install superpowers@claude-plugins-official
```
Auto-updates avec `/plugin update superpowers`.

### Skills fournies (14)

| Skill | Fonction |
|---|---|
| **brainstorming** | Exploration socratique avant de coder |
| **writing-plans** | Decomposition d'implementation detaillee |
| **executing-plans** | Execution batch avec checkpoints |
| **test-driven-development** | Cycle RED-GREEN-REFACTOR enforce |
| **systematic-debugging** | Analyse root cause en 4 phases |
| **verification-before-completion** | Verification avant de marquer "done" |
| **dispatching-parallel-agents** | Workflows subagents concurrents |
| **requesting-code-review** | Checklist pre-review |
| **receiving-code-review** | Workflow de reponse au feedback |
| **using-git-worktrees** | Branches paralleles de dev |
| **finishing-a-development-branch** | Decisions merge/PR |
| **subagent-driven-development** | Review 2 etapes (spec + qualite code) |
| **writing-skills** | Creer de nouvelles skills |
| **using-superpowers** | Introduction au systeme |

### Methodologie

Prescriptif : brainstorm d'abord → git worktree → plan → TDD via subagents → code review
→ branch completion. C'est un workflow impose, pas suggestif.

### Ecosysteme

- **superpowers-marketplace** (780 stars) — Catalogue de plugins curate
- **superpowers-skills** (594 stars) — Skills editables par la communaute
- **superpowers-lab** (264 stars) — Skills experimentales
- **superpowers-chrome** (230 stars) — Controle navigateur via DevTools Protocol

---

## 2. Everything Claude Code (affaan-m)

**URL :** https://github.com/affaan-m/everything-claude-code
**Stars :** ~131K | **Version :** 1.9.0 (mars 2026) | **Licence :** MIT
**Origine :** Gagnant hackathon Anthropic (Cerebral Valley, fev 2026)

### Ce que c'est

Un **systeme d'optimisation de harness** complet : skills, agents, hooks, rules, MCP configs,
contexts. Beaucoup plus large que Superpowers — c'est une boite a outils, pas une methodologie.

### Installation

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code && npm install
./install.sh --profile full          # install complete
./install.sh typescript python       # par langage
```

### Echelle

| Composant | Nombre |
|-----------|--------|
| Skills | 80+ |
| Agents/subagents | 36 |
| Slash commands (legacy) | 68 |
| Rules directories | 9 (par langage) |
| Tests | 997+ |
| MCP configs | Multiple (GitHub, Supabase, Vercel, Railway) |

### Skills cles (selection)

- **Core :** tdd-workflow, security-review, eval-harness, verification-loop,
  continuous-learning, strategic-compact, search-first, autonomous-loops
- **Stacks :** django-*, springboot-*, laravel-*, golang-*, python-*, cpp-*
- **Frontend :** frontend-patterns, frontend-slides, liquid-glass-design
- **Backend :** database-migrations, api-design, deployment-patterns, docker-patterns
- **Business :** article-writing, market-research, investor-materials

### Agents cles (36 total)

planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver,
e2e-runner, refactor-cleaner, doc-updater, chief-of-staff, loop-operator, harness-optimizer,
plus reviewers et resolvers par langage.

### Patterns cles

- Hook-based session state management (pre/post tool, session lifecycle)
- Memory persistence (load/save contexte entre sessions)
- Strategic compaction (quand et comment compresser le contexte)
- Contexts dynamiques (modes dev, review, research)
- Hook profiles configurables : `minimal | standard | strict`

---

## Comparaison

| | Superpowers | Everything Claude Code |
|---|---|---|
| Philosophie | Methodologie opinionnee (un workflow) | Boite a outils (pick what you need) |
| Install | Plugin officiel (`/plugin install`) | Clone + shell script |
| Skills | 14 focalisees, composables | 80+ larges, domain-specific |
| Agents | Dispatch subagent comme skill | 36 agents dedies |
| Hooks | Minimal | Lifecycle management complet |
| Langages | Agnostique | Rules specifiques pour 9 langages |
| Updates | `/plugin update` | Git pull + reinstall |

---

## Implications pour metadev-protocol

### Ce qu'on peut apprendre de Superpowers

1. **Le workflow brainstorm → plan → execute est la killer feature** — c'est ce que Vincent
   utilise le plus. On devrait en faire des skills fondation.
2. **Prescriptif > suggestif** — Superpowers impose le workflow, pas le suggere. Nos skills
   devraient etre opinionated.
3. **TDD comme skill, pas comme regle CLAUDE.md** — "write test first" est plus efficace
   comme skill invocable que comme instruction permanente.
4. **Verification-before-completion** — pattern a adopter : avant de dire "c'est fait",
   verifier que ca marche vraiment.
5. **Git worktrees comme skill** — pattern avance pour dev parallele.

### Ce qu'on peut apprendre d'Everything Claude Code

1. **Profiles d'installation** — minimal/standard/full. On a deja minimal/app/data/quant,
   mais on pourrait aussi avoir un axe "legereté" du harness.
2. **Agents dedies** — planner, architect, reviewer comme agents, pas juste des skills.
   Plus puissant mais plus complexe.
3. **Memory persistence** — load/save contexte entre sessions. Notre SESSION-CONTEXT.md
   est la version simple de ca.
4. **Strategic compaction** — skill pour decider quand et comment compresser. Plus avance
   que notre hook head -30.
5. **Hook profiles** — minimal/standard/strict. Bonne idee pour laisser l'user choisir
   son niveau d'automation.

### Ce qu'on ne devrait PAS copier

1. **80+ skills** — trop pour un template bootstrap. On est dans le T1/T2, pas le kitchen-sink.
2. **36 agents** — over-engineered pour un nouveau projet.
3. **Installation via npm/shell script** — notre approche copier est plus propre.
4. **Rules par langage** — on est Python-only, pas besoin.
