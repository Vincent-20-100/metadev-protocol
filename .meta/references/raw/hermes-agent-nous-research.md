# Hermes Agent — Nous Research (boucle d'apprentissage fermée)

**Source:** Hermes Agent by Nous Research (open source)
**Date:** 2026-04-07
**Type:** Reference (bronze)

---

## What it is

Agent IA open source avec boucle d'apprentissage fermée. Tourne en
permanence sur serveur distant, accessible via Telegram/Discord/Slack.
Compatible 200+ modèles via OpenRouter.

## 5 capacités structurantes

1. **Boucle d'apprentissage fermée** — crée de nouvelles skills après chaque tâche complexe, s'améliore à l'usage, recherche ses propres conversations passées
2. **Mémoire persistante cross-sessions** — modèle évolutif du style de travail, compatible agentskills.io
3. **Automatisations planifiées** — rapports, sauvegardes, audits en langage naturel, exécution continue
4. **Architecture multi-agents** — délègue à des sous-agents en parallèle
5. **Indépendance du modèle** — 200+ modèles, aucun lock-in

## Comparaison avec metadev-protocol

| Axe | metadev-protocol | Hermes Agent |
|-----|------------------|--------------|
| Mémoire | Explicite (PILOT.md, SESSION-CONTEXT.md) — contrôlé, versionné | Implicite, base vectorielle — magic mais opaque |
| Multi-agents | /debate (3 agents), /orchestrate | Sous-agents parallèles runtime |
| Skills | Manuelles (SKILL.md) — fiables mais lentes | Auto-générées post-tâche — rapides mais qualité non validée |
| Automatisations | PostToolUse hook, pre-commit, /save-progress | Planification en langage naturel, exécution continue |
| Architecture | Local-first, fichiers git | Serveur distant obligatoire |
| Portabilité | Copier template → n'importe quel projet | Serveur + bot messaging |
| Dépendance | Claude Code (pour l'instant) | 200+ modèles (OpenRouter) |

## Ce qui est déjà couvert chez nous

- Mémoire persistante → PILOT.md + SESSION-CONTEXT.md + SessionStart hook (manuel mais contrôlé)
- Multi-agents → /debate + /orchestrate
- Apprentissage patterns → GUIDELINES.md, anti-rationalization tables
- Automatisations → PostToolUse hook, pre-commit, /save-progress

## Ce qui est réellement nouveau

- **Auto-génération de skills post-tâche** — crée des compétences après une tâche complexe. Risqué (qualité non validée) mais concept intéressant
- **Serveur permanent** — tourne en continu, pas lié à une session. C'est notre concept "Nightshift" (déjà identifié dans PILOT.md)
- **agentskills.io** — standard ouvert pour partager des compétences entre agents. À surveiller pour interop

## Takeaways pour metadev-protocol

| Insight | Priority | Action |
|---------|----------|--------|
| Auto-génération de skills | Medium | Compromis possible : `/suggest-skill` qui propose mais ne crée pas automatiquement |
| Serveur permanent (Nightshift) | Low | Déjà identifié, needs server infra |
| agentskills.io standard | Low | Surveiller pour future interop des skills |
| Boucle fermée vs explicite | Info | Notre approche explicite est plus fiable pour le vibe coding (auditabilité, git, contrôle) |
