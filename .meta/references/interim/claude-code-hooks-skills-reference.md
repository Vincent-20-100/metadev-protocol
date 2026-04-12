# Claude Code — Hooks, Settings, Skills & MCP Reference

> Source : documentation officielle Claude Code (claude-code-guide agent)
> Date : 2026-04-01

---

## 1. Hooks System

### Events disponibles

| Event | Quand | Matcher |
|-------|-------|---------|
| `SessionStart` | Session demarre/reprend | `startup`, `resume`, `clear`, `compact` |
| `PreToolUse` | Avant execution d'un outil | Nom de l'outil (regex) |
| `PostToolUse` | Apres execution reussie | Nom de l'outil (regex) |
| `PostToolUseFailure` | Apres echec d'un outil | Nom de l'outil (regex) |
| `UserPromptSubmit` | Avant traitement du prompt | - |
| `Stop` | Claude finit de repondre | - |
| `PermissionRequest` | Dialogue de permission | Nom de l'outil |
| `CwdChanged` | Changement de repertoire | - |
| `FileChanged` | Fichier surveille modifie | Pattern filename |
| `PreCompact` | Avant compaction contexte | - |
| `PostCompact` | Apres compaction | - |
| `SubagentStart` | Subagent lance | Type agent |
| `SubagentStop` | Subagent termine | Type agent |

### Types de hooks

1. **`command`** — Script shell, recoit JSON sur stdin
2. **`http`** — POST vers endpoint HTTP
3. **`prompt`** — Evaluation single-turn Claude (Haiku par defaut)
4. **`agent`** — Subagent multi-turn avec outils

### Exit codes

- **0** : Succes, stdout parse comme JSON
- **2** : Erreur bloquante, stderr envoye a Claude comme feedback
- **Autre** : Non-bloquant, stderr visible en mode verbose

### Patterns utiles pour projets Python

**Auto-format ruff apres edit :**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} sh -c 'if [[ {} == *.py ]]; then uv run ruff format {} && uv run ruff check {} --fix; fi'"
          }
        ]
      }
    ]
  }
}
```

**Re-injecter contexte apres compaction :**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Using uv for package management. Run uv run pytest before committing.'"
          }
        ]
      }
    ]
  }
}
```

**Bloquer commandes dangereuses :**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "if": "Bash(rm *)",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Blocked: rm not allowed' >&2; exit 2"
          }
        ]
      }
    ]
  }
}
```

---

## 2. Settings.json

### Fichiers et precedence (du plus fort au plus faible)

| Fichier | Scope | Partage ? |
|---------|-------|-----------|
| Managed settings | Organisation | Oui (admin) |
| `.claude/settings.local.json` | Local projet | Non (gitignored) |
| `.claude/settings.json` | Projet | Oui (git) |
| `~/.claude/settings.json` | Utilisateur | Non |

### Schema complet

```json
{
  "permissions": {
    "allow": [
      "Bash(uv *)",
      "Bash(git *)",
      "Read",
      "Edit(/src/**)",
      "Edit(/tests/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Edit(.env)",
      "Edit(.git/**)"
    ]
  },
  "hooks": { ... },
  "sandbox": {
    "filesystem": {
      "denyRead": ["**/.env"],
      "denyWrite": [".git/**", ".venv/**"]
    },
    "network": {
      "allowedDomains": ["pypi.org", "github.com"]
    }
  }
}
```

### Syntaxe des permissions

```
Bash(uv *)                    # uv avec n'importe quels args
Edit(/src/**)                 # Edition relative a la racine projet
Read(~/.config)               # Repertoire home
mcp__github                   # Tous les outils d'un serveur MCP
mcp__github__search_repositories  # Outil MCP specifique
Agent(Explore)                # Subagent specifique
```

---

## 3. Skills System

### Structure

```
.claude/skills/
├── test/
│   └── SKILL.md
├── deploy/
│   └── SKILL.md
└── review/
    └── SKILL.md
```

### Frontmatter SKILL.md

```yaml
---
name: skill-command-name
description: What this skill does
disable-model-invocation: false    # true = seulement invocable par l'user
user-invocable: true
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Bash(uv *)
model: claude-3-5-haiku            # Override modele
effort: high                       # low|medium|high|max
context: fork                      # Run en subagent isole
agent: Explore|Plan|general-purpose
paths: "src/**,lib/**"             # Auto-load sur ces paths
---

Instructions ici...

Substitutions : $ARGUMENTS, $0, $1, ${CLAUDE_SESSION_ID}, ${CLAUDE_SKILL_DIR}
```

### Progressive disclosure

| Declencheur | Comportement | Impact contexte |
|-------------|-------------|-----------------|
| Description skill toujours en contexte | Claude sait ce qui est dispo | ~10% fenetre |
| User invoque `/skill-name` | Skill complete chargee | Ajoutee au contexte |
| Claude decide (match description) | Skill auto-chargee | Ajoutee au contexte |
| `disable-model-invocation: true` | Jamais auto-chargee | Pas dans le contexte |

### Exemples pour projets Python

**Skill test :**
```yaml
---
name: test
description: Run the test suite with coverage
allowed-tools: Bash(uv *)
---
Run tests on $ARGUMENTS:
1. Run pytest with coverage: `uv run pytest --cov=src --cov-report=term-missing`
2. Report the coverage percentage
3. Highlight any modules below 80% coverage
```

**Skill deploy (manual only) :**
```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
allowed-tools: Bash(uv *), Bash(git *)
---
Deploy $ARGUMENTS to production:
1. Run the full test suite: `uv run pytest`
2. Build: `uv build`
3. Push to PyPI or deployment target
4. Verify the deployment succeeded
```

**Skill review (forked subagent) :**
```yaml
---
name: review-code
description: Perform a detailed code review
context: fork
agent: Explore
---
Review the code in $ARGUMENTS for:
1. Performance issues
2. Security vulnerabilities
3. Code style violations
4. Missing error handling
5. Test coverage gaps
```

---

## 4. MCP Server Configuration

### Dans .claude/.mcp.json

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/mcp-filesystem/dist/index.js"]
    },
    "github": {
      "type": "http",
      "url": "http://localhost:3000/mcp",
      "headers": {
        "Authorization": "Bearer $GITHUB_TOKEN"
      }
    }
  }
}
```

### Scopes

| Scope | Fichier | Quand |
|-------|---------|-------|
| Projet | `.claude/.mcp.json` | Ce projet |
| User | `~/.claude/.mcp.json` | Tous les projets |

### Nommage des outils MCP

Pattern : `mcp__<server>__<tool>`
- `mcp__github__search_repositories`
- `mcp__filesystem__read_file`

---

## 5. Structure .claude/ recommandee pour template Python

```
.claude/
├── settings.json              # Permissions + hooks projet
├── settings.local.json        # Overrides locaux (gitignored)
├── skills/
│   └── test/
│       └── SKILL.md           # /test skill
├── hooks/
│   └── lint-on-edit.sh        # Auto-format ruff
└── .mcp.json                  # Serveurs MCP (si besoin)
```

### Implication pour metadev-protocol

Le template devrait generer :
1. `.claude/settings.json` avec permissions de base (allow uv/git, deny rm/sudo/.env)
2. `.claude/skills/test/SKILL.md` — skill pytest
3. Un hook PostToolUse pour auto-format ruff apres edit (optionnel, selon question copier)
4. `.claude/.mcp.json` vide ou absent (l'user configure selon ses besoins)
