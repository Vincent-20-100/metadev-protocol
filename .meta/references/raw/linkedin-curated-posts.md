# LinkedIn — Posts curates pertinents pour metadev-protocol

> Source : posts sauvegardes par Vincent, filtres pour pertinence.
> Date de curation : 2026-04-01

---

## Post 1 — Lexique fondamental des agents IA (MCP vs Skills)

**Auteur :** Wilfried de Renty — Ingenieur & architecte IA
**Date :** ~29 mars 2026
**Pertinence :** TEMPLATE — concepts a integrer dans le CLAUDE.md des projets app/data

### Contenu

6 termes fondamentaux des agents IA :

1. **MCP — Model Context Protocol**
   - Standard universel de connexion entre une IA et ses outils externes
   - "L'USB-C de l'IA" : un seul protocole pour tout brancher

2. **Skills (Competences)**
   - Logique de haut niveau qui orchestre les outils MCP
   - MCP fournit la connexion. La Skill decide quand et pourquoi l'utiliser

3. **Architecture Mono-Agent**
   - Un seul agent gere l'integralite du pipeline : comprehension, planification, execution

4. **Architecture Multi-Agent**
   - Plusieurs agents specialises collaborent sur une meme tache
   - L'un recupere, un autre valide, un troisieme genere la reponse finale

5. **RAG Agentique**
   - Implementation avancee du RAG pilotee par un agent
   - Route les requetes, valide le contexte, selectionne dynamiquement les donnees utiles

6. **Memoire de l'Agent**
   - Court terme : dans la fenetre de contexte, pour l'usage immediat
   - Long terme : stockee en externe (base vectorielle), recuperee a la demande

**Distinction cle :**
- MCP = comment l'agent parle a ses outils
- Skills = comment l'agent decide de les utiliser
- Memoire = ce que l'agent retient entre les interactions

**Implication pour metadev-protocol :** Ces 3 couches sont le modele mental a integrer
dans le CLAUDE.md des projets generes. Le template devrait preparer la structure
pour MCP (`.claude/` config), Skills (chargement a la demande), et memoire (.meta/sessions/).

---

## Post 2 — Les 9 couches d'une application IA en production

**Auteur :** Wilfried de Renty
**Date :** ~25 mars 2026
**Pertinence :** PROFILE:app — checklist d'architecture pour le profil app

### Contenu

1. **Donnees** — Ingestion, nettoyage, chunking, indexation vectorielle
2. **Recuperation** — Requetes hybrides (semantique + mots-cles), reranking, filtrage par source
3. **Memoire et etat** — Contexte conversationnel, cache semantique, gestion de sessions
4. **Routage** — Classification d'intention, selection du bon template, logique de fallback
5. **Generation** — Templates de prompts versionnes, regles d'ancrage, streaming token par token
6. **Evaluation** — Jeu de tests golden, pipeline offline, monitoring en production
7. **Securite** — Detection d'injection, filtrage du contenu recupere, protection des donnees
8. **Observabilite** — Tracage par etape, capture du feedback, cout par requete
9. **Infrastructure** — API async, frontend conteneurise, scripts de deploiement et de healthcheck

**Implication pour metadev-protocol :** Pour le profil `app`, cette checklist pourrait
etre integree dans le PILOT.md genere ou dans un `.meta/decisions/architecture-checklist.md`
pour guider les premieres decisions d'architecture.

---

## Post 3 — MCP (temps reel) vs Indexation (Onyx)

**Auteur :** Wilfried de Renty
**Date :** ~31 mars 2026
**Pertinence :** INSPIRATION — pattern architectural pour acces aux donnees

### Contenu

Deux architectures pour donner a un agent acces aux donnees :

**Approche 1 — Requete en temps reel (MCP)**
- L'agent interroge les outils au moment de la requete
- Pas d'indexation prealable
- Depend de la disponibilite des APIs externes
- Resultat : latence variable, fiabilite incertaine en production

**Approche 2 — Indexation complete (Onyx)**
- Toutes les sources sont indexees en amont (Slack, Drive, Confluence, Jira, GitHub, emails)
- 40+ connecteurs alimentent un index unifie
- L'agent recherche dans l'index, pas dans les outils eux-memes
- Resultat : recherche plus rapide, plus fiable, cross-sources

Implications strategiques :
- Souverainete des donnees (deploiement Docker sur infra propre)
- Independence du modele (compatible Claude, GPT, Gemini, Llama)
- Qualite de recherche (classe n°1 sur DeepResearchBench)

**Repo :** Onyx (GitHub)

**Implication pour metadev-protocol :** Ce trade-off MCP vs indexation est une decision
d'architecture recurrente. Pourrait devenir un ADR template dans `.meta/decisions/`.

---

## Voices a suivre (extraites de ces posts)

| Nom | Titre | Pourquoi |
|---|---|---|
| **Wilfried de Renty** | Ingenieur & architecte IA | Contenu structure sur agents, MCP, architecture IA |
| **Fabrizio Rocco** | Solutions Architect @ AWS | Infrastructure IA, caching agents |
| **Gael PENESSOT** | Fondateur mes-formations-data.fr | Streamlit, data workflows Python |
