# Git Author Cleanup — Corriger l'historique et prévenir les récidives

> Réécrire l'auteur de commits sans changer les dates. Applicable à tout repo Git.
> Deux phases : nettoyage rétroactif, puis protection préventive.

---

## Contexte

Claude Code peut écrire des commits sous `Claude <noreply@anthropic.com>` — via
injection d'env vars (`GIT_AUTHOR_NAME`, `GIT_COMMITTER_NAME`), pas via `--author`.
Le problème se manifeste dans GitHub UI et dans `git log --format="%an"`.

---

## Phase 1 — Nettoyage rétroactif (historique existant)

### Diagnostic

```bash
# Vérifier les auteurs présents dans tout l'historique
git log --all --format='%an <%ae>' | sort -u

# Identifier les commits concernés (auteur OU committer)
git log --all --format='%H author:%an committer:%cn' | grep -iE "claude|anthropic"
```

### Outil : `git filter-repo` (préserver les dates)

> **Pourquoi filter-repo et pas `rebase --reset-author` ?**
> `rebase --reset-author` réécrit la date (auteur ET committer) au moment du rebase.
> `filter-repo` ne touche que les champs que les callbacks retournent — dates inchangées.

```bash
# Installation (une fois par machine)
pip install git-filter-repo
# ou : uv tool install git-filter-repo

# Réécrire auteur + email sur tout l'historique (toutes branches, tous tags)
git filter-repo --force \
  --name-callback  'return b"Votre Nom" if name  == b"Claude"                  else name' \
  --email-callback 'return b"vous@example.com" if email == b"noreply@anthropic.com" else email'
```

> **Note :** `filter-repo` supprime le remote `origin` par sécurité. Le rajouter :
> ```bash
> git remote add origin git@github.com:user/repo.git
> ```

### Vérification avant push

```bash
# Doit ne montrer que votre identité
git log --all --format='%an <%ae>' | sort -u

# Vérifier que les dates sont bien préservées
git log --format="%H %an %ai" -10
```

### Push

```bash
# Force-push requis (historique réécrit)
git push origin main --force-with-lease

# Si des tags ont été réécrits (les SHAs changent après filter-repo)
git push origin --tags --force-with-lease

# Supprimer les branches remote orphelines (branches Claude éventuelles)
git branch -r | grep "claude/" | sed 's|origin/||' | xargs -I{} git push origin --delete {}
```

### Nettoyage local

```bash
# Forcer les autres clones à se resynchroniser :
# git fetch --prune && git reset --hard origin/main
```

---

## Phase 2 — Protection préventive (4 couches)

### Couche 1 — Env vars dans `settings.json`

Claude Code injecte son identité via `GIT_AUTHOR_NAME` / `GIT_COMMITTER_NAME`.
La contremesure directe : surcharger ces vars dans `settings.json`.

```json
// .claude/settings.json
{
  "env": {
    "GIT_AUTHOR_NAME":    "Votre Nom",
    "GIT_AUTHOR_EMAIL":   "vous@example.com",
    "GIT_COMMITTER_NAME": "Votre Nom",
    "GIT_COMMITTER_EMAIL":"vous@example.com"
  }
}
```

Vérification : `jq '.env' .claude/settings.json`

### Couche 2 — PreToolUse hook (`force_git_author.py`)

Intercepte chaque `git commit` avant exécution.
Supprime tout `--author` existant. Injecte l'identité depuis `git config user.name`.

```python
# scripts/force_git_author.py — zéro dépendance externe
#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess, sys

def git_identity(key: str) -> str:
    try:
        return subprocess.check_output(["git", "config", key], text=True).strip()
    except subprocess.CalledProcessError:
        return ""

def strip_author_flag(cmd: str) -> str:
    cmd = re.sub(r"\s+--author=['\"]?[^'\"\s][^'\"]*['\"]?", "", cmd)
    cmd = re.sub(r"\s+--author='[^']*'", "", cmd)
    cmd = re.sub(r'\s+--author="[^"]*"', "", cmd)
    return cmd

def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0
    cmd: str = data.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\b.*\bcommit\b", cmd):
        return 0
    name = git_identity("user.name")
    email = git_identity("user.email")
    if not name or not email:
        return 0
    cmd_final = f"{strip_author_flag(cmd).rstrip()} --author='{name} <{email}>'"
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": {"command": cmd_final}}}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Câblage dans `settings.json` :

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "python scripts/force_git_author.py"}]
    }
  ]
}
```

Test rapide :
```bash
echo '{"tool_input": {"command": "git commit -m \"test\""}}' | python scripts/force_git_author.py
# Attendu : --author='Votre Nom <vous@example.com>' injecté
```

### Couche 3 — Pre-commit hook (`check_git_author.py`)

Bloque le commit si l'auteur résolu est interdit.
Vérifie **à la fois** `$GIT_AUTHOR_NAME` (env) et `git var GIT_AUTHOR_IDENT` (config).

```python
# scripts/check_git_author.py (extrait clé)
FORBIDDEN_SUBSTRINGS = ["claude", "anthropic"]

def check_author() -> str | None:
    if os.environ.get("CI"):
        return None

    # Couche A : env var directe
    env_name = os.environ.get("GIT_AUTHOR_NAME", "").lower()
    if env_name and any(bad in env_name for bad in FORBIDDEN_SUBSTRINGS):
        return f"$GIT_AUTHOR_NAME='{env_name}' est interdit"

    # Couche B : git config
    try:
        ident = subprocess.check_output(["git", "var", "GIT_AUTHOR_IDENT"], text=True).strip()
    except subprocess.CalledProcessError:
        return None
    name = ident.split("<", 1)[0].strip().lower()
    if any(bad in name for bad in FORBIDDEN_SUBSTRINGS):
        return f"Auteur '{name}' est interdit"
    return None
```

Câblage dans `.pre-commit-config.yaml` :
```yaml
- id: check-git-author
  name: Check git author identity
  language: python
  entry: python scripts/check_git_author.py
  pass_filenames: false
  stages: [commit]
```

### Couche 4 — CI GitHub Actions

Bloque les PRs ET les pushs directs contenant des commits Claude/Anthropic.
Vérifie **auteur ET committer**.

```yaml
# .github/workflows/check-commit-authors.yml
name: Check commit authors
on:
  pull_request:
    branches: [main]
  push:
    branches: ['**']

jobs:
  check-authors:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Scan commits for blocked author/committer
        run: |
          BLOCKED="Claude|Anthropic"
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            RANGE="${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }}"
          else
            BEFORE="${{ github.event.before }}"
            HEAD="${{ github.sha }}"
            [ "$BEFORE" = "0000000000000000000000000000000000000000" ] \
              && RANGE="${HEAD}~1..${HEAD}" || RANGE="${BEFORE}..${HEAD}"
          fi
          FOUND=$(git log "${RANGE}" --format="%H author:%an committer:%cn" | grep -iE "$BLOCKED" || true)
          if [ -n "$FOUND" ]; then
            echo "::error::Commits avec auteur/committer bloqué:"
            echo "$FOUND"
            exit 1
          fi
          echo "Tous les auteurs OK."
```

---

## Checklist d'application à un projet existant

```
[ ] git log --all --format='%an <%ae>' | sort -u   → identifier les identités parasites
[ ] git filter-repo --force --name-callback ... --email-callback ...
[ ] git remote add origin <url>                     → filter-repo le supprime
[ ] git log --all --format='%an <%ae>' | sort -u   → vérifier
[ ] git push origin main --force-with-lease
[ ] Ajouter env block dans .claude/settings.json
[ ] Copier scripts/force_git_author.py
[ ] Câbler PreToolUse hook dans settings.json
[ ] Copier scripts/check_git_author.py
[ ] Ajouter hook dans .pre-commit-config.yaml
[ ] Copier .github/workflows/check-commit-authors.yml
[ ] git add . && git commit -m "chore: git author hardening"
```

---

## Erreurs courantes

| Erreur | Conséquence | Fix |
|--------|-------------|-----|
| `rebase --reset-author` au lieu de `filter-repo` | Dates réécrites à aujourd'hui | Relancer avec filter-repo depuis le backup |
| Oublier de re-rajouter `origin` après filter-repo | `git push` échoue sans message clair | `git remote add origin <url>` |
| Force-push sans `--force-with-lease` | Écrase des commits tiers éventuels | Toujours utiliser `--force-with-lease` |
| Tags non force-pushés | Tags pointent encore vers les anciens SHAs | `git push origin --tags --force-with-lease` |
| Env vars dans settings.json hardcodées | Ne s'adapte pas à un autre dev sur le même repo | Dériver depuis `git config user.name/email` (copier.yml `shell` filter) |
