# ADR-002 — Generation d'un repertoire .claude/ dans le template

**Date :** 2026-04-01
**Statut :** IMPLEMENTED
**Sources :**
- `.meta/references/claude-code-hooks-skills-reference.md` (doc officielle)
- `.meta/references/state-of-the-art-vibe-coding.md` (finding #2 : hooks > CLAUDE.md)
- `.meta/references/claude-code-leak-analysis.md` (architecture interne Claude Code)
- ADR-001 decision #4 (hooks > CLAUDE.md pour enforcement)

---

## Probleme

Les instructions dans CLAUDE.md ont un taux de compliance de ~70-80% (source : Boris Cherny,
createur de Claude Code, confirme par la communaute). Ca veut dire que 1 fois sur 4-5,
Claude ignore une regle ecrite dans CLAUDE.md.

Pour les regles critiques (formatting, lint, fichiers interdits), c'est inacceptable.

EgoVault illustre le probleme : 13 regles dans CLAUDE.md, 0 hook, 0 enforcement automatique.
Resultat : pas de ruff configure, pas de pre-commit, pas de type checking. Les regles sont
documentees mais pas appliquees.

## Decision

Le template genere un repertoire `.claude/` pre-configure avec :

### 1. `settings.json` — Permissions et hooks

**Quoi :** Fichier de configuration Claude Code, charge automatiquement a chaque session.

**Permissions :**
- **Allow :** `Bash(uv *)`, `Bash(git status/diff/log/add/commit *)`, `Read`, `Edit(src/**)`, `Edit(tests/**)`
- **Deny :** `Bash(rm -rf *)`, `Bash(sudo *)`, `Edit(.env)`, `Edit(.git/**)`

**Pourquoi ces permissions :**
- `uv` et `git` = outils quotidiens, les demander a chaque fois tue la productivite
- `Read` = toujours safe, pas besoin de demander
- `Edit` restreint a `src/` et `tests/` = empeche Claude de modifier la config par accident
- Deny `rm -rf` et `sudo` = securite de base, irreversibles
- Deny `.env` = empeche d'ecrire des secrets dans un fichier souvent gitignore par erreur

**Niveau de confiance : ELEVE** — Les permissions sont un pattern bien documente et largement
adopte par la communaute. Le pire cas = trop restrictif, l'user ajuste.

### 2. Hook PostToolUse — Auto-format ruff

**Quoi :** Apres chaque `Edit` ou `Write` d'un fichier `.py`, lance automatiquement
`uv run ruff format` + `uv run ruff check --fix`.

**Pourquoi :**
- C'est le finding #2 de l'etat de l'art : hooks = 100% compliance, CLAUDE.md = ~70-80%
- Ecrire "run ruff before committing" dans CLAUDE.md ne suffit pas
- Le hook est silencieux (stderr redirige vers /dev/null) — pas de bruit si ruff n'est pas installe
- Le hook ne bloque pas (exit 0 toujours) — il corrige mais ne casse pas le flow

**D'ou vient l'idee :**
- Doc officielle Claude Code (hook patterns for Python)
- Confirme par le leak : Claude Code interne utilise des hooks similaires
- Pattern #4 de ADR-001

**Comment s'en servir :** Transparent. L'utilisateur n'a rien a faire. Chaque fichier .py
edite est auto-formate. Si l'user veut desactiver : supprimer le bloc dans settings.json.

**Niveau de confiance : ELEVE** — Pattern standard, bien documente, fail-safe (exit 0).
Le seul risque : ruff change un import que Claude venait d'ecrire → rare et corrigible.

### 3. Hook SessionStart (compact) — Re-injection PILOT.md

**Quoi :** Quand le contexte est compresse (fenetre de contexte pleine), le hook re-injecte
les 30 premieres lignes de `.meta/PILOT.md` pour que Claude ne perde pas l'etat du projet.

**Pourquoi :**
- La compaction supprime du contexte pour liberer de la place
- CLAUDE.md est re-charge automatiquement, mais PILOT.md non
- Sans ce hook, apres compaction Claude perd l'objectif de session et l'etat du projet
- 30 lignes = assez pour le titre, la phase, et le tableau d'etat

**D'ou vient l'idee :**
- Doc officielle : le matcher `compact` sur `SessionStart` est fait pour ca
- Le pattern "Dream Mode" du leak confirme l'importance de la persistance inter-contexte
- Notre propre experience : le cockpit PILOT.md est inutile s'il n'est pas lu

**Niveau de confiance : MOYEN** — Le pattern est documente mais on ne l'a pas encore teste
en conditions reelles sur un long projet. Le `head -30` est arbitraire. A ajuster si
le PILOT.md change de format.

**Risque :** Si PILOT.md n'existe pas, le `|| true` empeche le crash. Mais le hook est
silencieux = l'user ne sait pas si ca marche. Pas de feedback visible.

### 4. Skill `/test` — Raccourci pytest

**Quoi :** Commande `/test` dans Claude Code qui lance `uv run pytest` avec arguments optionnels.

**Pourquoi :**
- C'est le use case #1 des skills : raccourci pour une commande frequente
- La skill decode aussi le resultat (passed/failed/skipped) et suggere des fixes
- Progressive disclosure : la description est toujours en contexte (~10% fenetre),
  le contenu complet n'est charge que quand `/test` est invoque

**D'ou vient l'idee :**
- Doc officielle skills system
- Pattern "verification commands are highest-leverage CLAUDE.md content" (etat de l'art finding #4)
- Plutot que de mettre "run pytest" dans CLAUDE.md, on en fait une skill invocable

**Comment s'en servir :** Taper `/test` dans Claude Code, ou `/test tests/tools/` pour un sous-ensemble.

**Niveau de confiance : MOYEN** — Le skills system est relativement nouveau. Le format SKILL.md
et les frontmatter pourraient evoluer. La skill est simple, donc le risque de casse est faible.

---

## Ce qu'on n'a PAS fait (et pourquoi)

### settings.local.json
- Pas genere — c'est un fichier personnel (gitignored par defaut par Claude Code)
- L'user le cree s'il veut override les permissions projet

### .mcp.json
- Pas genere — la config MCP est trop specifique a chaque user/environnement
- Generer un fichier vide serait confusant ("c'est quoi MCP ?")
- L'user ajoute ses serveurs MCP quand il en a besoin

### Skills deploy, review, fix-issue
- Pas generees — trop specifiques, chaque projet a des besoins differents
- `/test` est le seul skill universel
- On documente les exemples dans les references, l'user cree les siennes

### Hook PreToolUse pour bloquer rm
- Pas implemente — le `deny` dans permissions fait le meme job plus simplement
- Un hook serait redondant

### Sandbox
- Pas active — la sandbox est un feature avance, pas pertinent pour un bootstrap
- L'user l'active s'il a des besoins de securite specifiques

---

## Fichiers impactes

| Fichier | Action |
|---------|--------|
| `template/.claude/settings.json.jinja` | CREE — permissions + 2 hooks |
| `template/.claude/skills/test/SKILL.md` | CREE — skill /test |

## Comment modifier

- Permissions : editer `permissions.allow` / `permissions.deny` dans settings.json
- Hooks : ajouter/supprimer des blocs dans `hooks.PostToolUse` / `hooks.SessionStart`
- Skills : creer un dossier dans `.claude/skills/<nom>/SKILL.md`
- MCP : creer `.claude/.mcp.json` avec la config serveurs
