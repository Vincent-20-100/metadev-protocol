# PILOT.md — Session : metadev-protocol bootstrap

**Date :** 2026-04-01
**Phase :** Fondation — avant premier push to origin

---

## 🎯 Objectif de cette session

Finaliser et valider tous les documents de fondation avant de pousser sur GitHub
et d'instancier Claude Code dans ce repo.

Les docs doivent être cohérents, précis, et représenter l'état réel du projet —
pas un idéal théorique copié de Gemini.

---

## 📊 État du projet

| Composant | Statut | Notes |
|---|---|---|
| Repo GitHub créé | ✅ | `metadev-protocol` |
| Premier commit local | ✅ | Structure initiale |
| `.venv` + `uv` configurés | ✅ | |
| `CLAUDE.md` | ✅ Refondu | Instructions Claude Code correctes |
| `ARCHITECTURE.md` | ✅ Refondu | ADRs propres |
| `DECISIONS.md` | ✅ Refondu | Journal des choix |
| `PILOT.md` (ce fichier) | ✅ Refondu | |
| `template/CLAUDE.md.jinja` | ✅ | Template pour projets générés |
| `template/.meta/PILOT.md.jinja` | ✅ | Cockpit template |
| `template/pyproject.toml.jinja` | ✅ | Dépendances par profil |
| `template/.gitignore.jinja` | ✅ | Gitignore template |
| `template/.pre-commit-config.yaml` | ✅ | Config pre-commit template |
| `copier.yml` | ✅ Corrigé | Choices format fixé |
| `pyproject.toml` (meta-repo) | ✅ Corrigé | Python >=3.12, pre-commit ajouté |
| `.pre-commit-config.yaml` | ✅ | ruff hooks |
| Test `copier copy` | ✅ | Génération fonctionnelle |
| `pre-commit install` | ✅ | Hooks installés |
| Push to origin | ⏳ En cours | |
| Instanciation Claude Code | ❌ Après le push | |

---

## 🚦 Prochaines étapes (dans l'ordre)

1. **Valider ces docs** avec Claude.ai (en cours)
2. **Créer `copier.yml`** — questions d'init + structure conditionnelle
3. **Créer `template/CLAUDE.md.jinja`** — le contrat Claude Code des projets générés
4. **Créer `template/.meta/PILOT.md.jinja`** — le cockpit template
5. **Créer `template/pyproject.toml.jinja`** avec les 4 profils de dépendances
6. **Créer `.pre-commit-config.yaml`** au niveau du meta-repo
7. **Push to origin** (main branch)
8. **Instancier Claude Code** dans ce repo et tester la session

---

## 🧠 Contexte important pour l'IA

- Ce repo EST le template — toute modification dans `template/` doit être testée
  avec `copier copy . /tmp/test-proj --defaults` avant commit
- Claude Code lira ce `PILOT.md` automatiquement (via `CLAUDE.md` qui l'instruite)
- La philosophie centrale : séparer le produit du process via `.meta/`
- Stack : Python 3.12+, uv, ruff, copier, pre-commit

---

## 📝 Notes de session

- Gemini a fourni la direction générale mais contenait des erreurs factuelles
  (notamment sur la lecture automatique de CLAUDE.md par Claude Code)
- La conversation initiale a validé le concept `.meta/` et l'approche `copier`
- Les branches orphelines ont été explorées et rejetées → `copier.yml` avec conditionnels Jinja
- L'approche récursive (utiliser la méthode pour créer la méthode) est le bon angle de test
