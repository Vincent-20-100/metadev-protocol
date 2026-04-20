---
type: spec
date: 2026-04-12
slug: outreach-messaging
status: active
---

# Spec — Outreach messaging system for v1.0.0 launch

**Date:** 2026-04-12
**Purpose:** Cadrer la génération de messages personnalisés pour chaque lead beta, avec le bon ton, la bonne langue, et la bonne nuance de relation.

---

## 1. Lead table

| # | Name | Lang | Project | Relation | What to say | Channel | Tier |
|---|------|------|---------|----------|-------------|---------|------|
| 1 | Guillaume Desforges | fr | nix-copier-python | convergence | Arrivés indépendamment à "template Copier = opinions cristallisées". Découvert son projet après avoir déjà choisi Copier. Point commun validant, pas une inspiration directe. Son approche prose-first complémente notre enforcement-first | LinkedIn DM | D1 |
| 2 | Safi Shamsi | en | Graphify | reference | Audité Graphify pour benchmarker nos choix. Patterns retenus : confidence tagging, deterministic-first. Pas d'emprunt direct — l'audit a challengé nos décisions et confirmé certaines directions | GitHub issue / X | D1 |
| 3 | Todd Gilbert | en | Superpowers | inspiration | Le skills ecosystem de Superpowers a directement influencé notre architecture de skills (/brainstorm, /plan, /debate). Notre template recommande Superpowers comme plugin complémentaire | GitHub issue / X | D1 |
| 4 | Paul Bennett (mrpbennett) | en | Everything Claude Code | inspiration | La collection community-driven de skills (TDD, security review, linting) a inspiré nos agent personas dans AGENTS.md. Approche complémentaire : lui curate, nous scaffold | GitHub issue / X | D1 |
| 5 | Companion AI team | en | Feynman | inspiration | Honesty constraint (Rule #9) directement inspiré de leur SYSTEM.md. Tiered confidence gates inspiré de leur approche multi-agent. Audité post-v1.0.0 | GitHub issue | D3 |
| 6 | Yedan Zhang | en | Earnings Call Analyst | reference | Audité pour patterns de verification. Tiered scoring (green/amber/red) a influencé nos confidence gates dans le plan skill. Prompt versioning noté pour backlog | GitHub issue / X | D3 |
| 7 | Copier core team (Yajo) | en | Copier | ecosystem | Notre template est un showcase Copier : meta_visibility, execution_mode, copier update avec semver tags immutables, tests CI matrix 4 combinaisons | GitHub Discussion | D3 |
| 8 | Claudio Jolowicz | en | Hypermodern Python | peer | Deux templates Python opinionated, philosophies différentes. Le sien : tooling (mypy, nox, sphinx). Le nôtre : AI governance (.meta/, workflow gates). Complémentaires | GitHub issue | D3 |
| 9 | Frankie Robertson | en | cookiecutter-poetry | peer | Même espace (template Python), approche différente (cookiecutter vs copier). Notre migration vers Copier + AI-native features est un point de discussion naturel | GitHub issue | D3 |
| 10 | Scientific Python (cookie) | en | scientific-python/cookie | ecosystem | Templates Copier pour la communauté scientifique. Notre approche .meta/ taxonomy pourrait les intéresser pour la reproductibilité | GitHub Discussion | D5 |
| 11 | Caleb Sacks | en | claude-code-tips | cold | Documente les workflows Claude Code publiquement. Notre template est un workflow packagé — naturel pour son contenu | X reply/DM | D5 |
| 12 | Simon Willison | en | (blog/tools) | cold | Écrit régulièrement sur Claude Code et AI tooling. Notre .meta/ taxonomy et devil's advocate seraient des sujets de blog naturels pour lui | X / blog comment | D10 |
| 13 | Thorsten Ball | en | (Zed editor) | cold | Écrit sur les workflows agentic coding. Notre approche workflow gates + structured context est pertinente | X | D10 |
| 14 | Harper Reed | en | (AI tooling) | cold | Vocal Claude Code user, grande audience. Le template résout un problème qu'il a sûrement rencontré | X DM | D5 |
| 15 | Matt Shumer | en | (AI agents) | cold | Builds AI agent frameworks. Notre approche structured-context pour agents est pertinente pour son audience | X DM | D5 |
| 16 | Paul Gauthier | en | Aider | cold | Aider = autre agent coding. Le problème de context persistence est identique. Notre .meta/ taxonomy est agent-agnostic | GitHub Discussion / X | D5 |
| 17 | Continue.dev team | en | Continue | cold | Open-source AI coding. Notre template pourrait fonctionner avec leur agent. Les workflow gates sont editor-agnostic | GitHub Discussion | D5 |
| 18 | r/ClaudeAI | en | (community) | community | Post Show & Tell, before/after narrative, recursive bit | Reddit post | D7 |
| 19 | r/ChatGPTCoding | en | (community) | community | Post cross-posté, adapté au ton de la communauté (plus tool-agnostic) | Reddit post | D7 |
| 20 | Python Discord | en | (community) | community | #showcase channel, bref et technique | Discord message | D7 |
| 21 | Hacker News | en | (community) | community | Show HN, stripped of hype, technical, concise | HN post | D10 |
| 22 | Changelog podcast | en | (newsletter) | community | Submit for inclusion — AI-native project template angle | Newsletter intake form | D10 |
| 23 | Dev.to / Hashnode | en | (platform) | community | Tutorial post "How I gave my AI agent structured memory" | Blog post | D10 |

---

## 2. Relation types — wording rules

### `convergence` — on a fait le même choix indépendamment

**Ton :** pair à pair, respect mutuel, validation croisée.

**Structure :**
> On est arrivés à la même conclusion indépendamment — [choix commun].
> Quand j'ai découvert [project], ça m'a conforté dans l'approche.
> Nos projets sont complémentaires : [leur force] vs [notre force].

**Interdit :** "tu m'as inspiré" (faux — on avait déjà choisi avant), "grâce à toi" (sous-entend dépendance)

**Exemple Guillaume :**
> On est tous les deux arrivés à "template Copier = opinions cristallisées sur le dev AI" sans se connaître.
> Ton approche est prose-first (playbook, philosophie), la mienne est enforcement-first (hooks, permissions, workflow gates).
> L'union serait puissante.

### `inspiration` — on a vu leur approche et adopté/adapté

**Ton :** reconnaissance directe, sans excès. Montrer ce qu'on a pris ET ce qu'on a ajouté.

**Structure :**
> [Aspect spécifique] de [project] m'a directement inspiré pour [notre feature].
> J'ai adapté l'idée à [notre contexte] en ajoutant [notre valeur ajoutée].
> Tu es cité dans nos CREDITS.

**Interdit :** "sans toi ce projet n'existerait pas" (disproportionné), lister 10 trucs copiés (overwhelm)

**Exemple Todd :**
> L'architecture skills-as-folders de Superpowers a directement inspiré nos 7 skills dans le template.
> On recommande Superpowers comme plugin complémentaire dans notre CLAUDE.md — nos skills sont le fallback quand le plugin n'est pas installé.

### `reference` — on a audité leur projet pour benchmarker

**Ton :** respect professionnel. On a pris le temps d'étudier leur travail en profondeur.

**Structure :**
> J'ai audité [project] en détail pour challenger mes propres choix.
> Ce qui m'a le plus marqué : [pattern spécifique].
> Tu es cité dans nos CREDITS comme source de référence.

**Interdit :** "j'ai copié X de ton projet" (même si c'est le cas — reformuler en "X m'a influencé"), tone condescendant ("ton projet est intéressant mais...")

**Exemple Safi :**
> J'ai audité Graphify en détail pour comparer nos approches.
> Le confidence tagging sur les edges et l'approche deterministic-first m'ont beaucoup marqué.

### `ecosystem` — on est dans leur écosystème

**Ton :** contributeur/utilisateur enthousiaste. Montrer qu'on fait briller leur outil.

**Structure :**
> [Tool] est au cœur de [notre projet]. Voici comment on l'utilise : [usage spécifique].
> On pense que notre template est un bon showcase pour [tool].

### `cold` — aucune relation préexistante

**Ton :** bref, factuel, une seule raison de cliquer.

**Structure :**
> Je construis [pitch]. [Une phrase sur pourquoi ça les concerne].
> Lien.

---

## 3. Message templates

### Template A — Sources (convergence / inspiration / reference)

**FR :**
```
Salut {name},

Je suis Vincent, je développe metadev-protocol — un template Copier
pour bootstrapper des projets Python avec un protocole de collaboration
AI intégré (workflow gates, .meta/ taxonomy, audit de sécurité).

{relation_block}

Tu es cité dans nos CREDITS : https://github.com/Vincent-20-100/metadev-protocol/blob/main/CREDITS.md

Je te présente la v1.0.0 en avant-première :
https://github.com/Vincent-20-100/metadev-protocol

Si tu as 5 minutes pour jeter un œil, ton retour m'aiderait beaucoup.
Merci pour l'inspiration !

Vincent
```

**EN :**
```
Hi {name},

I'm Vincent, building metadev-protocol — a Copier template for
bootstrapping AI-assisted Python projects with built-in workflow gates,
.meta/ taxonomy, and security audit.

{relation_block}

You're credited in our CREDITS: https://github.com/Vincent-20-100/metadev-protocol/blob/main/CREDITS.md

Here's the v1.0.0, fresh out:
https://github.com/Vincent-20-100/metadev-protocol

If you have 5 minutes to take a look, your feedback would mean a lot.
Thanks for the inspiration!

Vincent
```

### Template B — Ecosystem

**EN :**
```
Hi {name}/{team},

I built metadev-protocol, a Copier template for AI-assisted Python projects.
{tool} is central to how it works: {usage_detail}.

I think it could serve as a good real-world showcase for {tool}.

Here's v1.0.0: https://github.com/Vincent-20-100/metadev-protocol

Would love any feedback. Happy to write up a case study if useful.

Vincent
```

### Template C — Cold

**EN :**
```
Hi {name},

I built an open-source Copier template that gives AI coding assistants
persistent project memory and safety gates. {one_line_why_they_care}.

https://github.com/Vincent-20-100/metadev-protocol

Vincent
```

---

## 4. Tone rules

### DO
- Écrire dans la langue du destinataire
- Mentionner UN aspect spécifique de leur projet (pas une liste)
- Montrer la valeur mutuelle (ils gagnent en visibilité via CREDITS)
- Remercier naturellement — la gratitude invite à regarder
- Rester sous 150 mots (sauf LinkedIn DM où 200 est OK)

### DON'T
- "Ton projet est incroyable" → remplacer par un fait précis
- "Sans toi..." → disproportionné pour un template
- Lister tout ce qu'on a pris → un seul point, le plus fort
- Supplier → "si tu as 5 minutes" pas "est-ce que tu pourrais stp"
- Mentir sur la temporalité → si on avait déjà choisi avant, dire convergence pas inspiration
- Demander directement un like/comment → ça vient naturellement avec le message de notif du post

### Curseur de familiarité

| Relation | Tutoiement (FR) | Ton |
|----------|-----------------|-----|
| convergence | oui (pair à pair) | collègue qui partage une découverte |
| inspiration | oui | dev qui reconnaît une bonne idée |
| reference | oui/vous selon profil | professionnel respectueux |
| ecosystem | vous | contributeur enthousiaste |
| cold | vous | bref et factuel |

---

## 5. CTA séquence (2 temps)

### Temps 1 — Message initial (D1-D5)
Objectif : feedback + remerciement. Aucune demande de promotion.
> "Si tu as 5 minutes pour jeter un œil, ton retour m'aiderait beaucoup. Merci pour l'inspiration !"

### Temps 2 — Notification du post officiel (D7-D10)
Objectif : informer qu'on a publié. Le like/comment vient naturellement si le contenu est bon.
> "Le post officiel est en ligne ! [lien]. Merci encore pour ton influence sur le projet."

Pas de "peux-tu liker", pas de "un commentaire aiderait". Si le projet les intéresse (et le Temps 1 a planté la graine), ils interagiront d'eux-mêmes.

### Si réponse positive au Temps 1
> "Merci ! Si tu veux être dans les premiers testeurs, je t'envoie les updates."

Ne jamais relancer plus d'une fois si pas de réponse.

---

## 6. Usage

Pour générer un message, fournir :
```
Lead: #3 (Todd Gilbert)
Channel: GitHub issue
```

→ L'agent utilise le lead table + le template correspondant au relation type + les tone rules pour produire le message final.
