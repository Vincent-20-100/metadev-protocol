# Launch Plan — metadev-protocol v1.0

**Date:** 2026-04-08
**Status:** DRAFT — awaiting user validation
**Target:** Public launch on GitHub with coordinated beta + announcement

---

## 1. Vision

metadev-protocol goes from private development repo to public open-source project.
The goal: establish it as THE reference template for AI-assisted Python development.

**Positioning:** Not "yet another Python template" — the first protocol that encodes
the contract between developer and AI into the project structure itself.

**Tagline candidate:** "One command. Zero context loss. AI that follows the plan."

---

## 2. Pre-launch implementation — all chantiers

Everything below must be done BEFORE any external eyes see the repo.

### Phase 0 — Pending specs/plans (core product)

| # | Chantier | Source | Effort | Dependency |
|---|----------|--------|--------|------------|
| 0.1 | **Workflow gates** — refonte Automatism #4, decision tree, tiers | spec-workflow-gates.md (validated) | Medium | None |
| 0.2 | **meta_visibility parameter** — copier question (standard/private/public) + conditional .gitignore.jinja | Debate record (validated) | Medium | None |
| 0.3 | **.meta/ gitignore alignment** — this repo: gitignore sessions/, scratch/, references/, SESSION-CONTEXT.md. Keep public: ARCHITECTURE.md, decisions/, gold/, PILOT.md, debates/ | Debate record (validated) | Low | 0.2 |
| 0.4 | **PILOT.md cleanup** — remove raw internal state (git author leak section, manual actions), make it public-worthy showcase | Debate decision | Low | 0.3 |
| 0.5 | **Rodin agent** (5th persona, devil's advocate) | plan-rodin-agent.md (ready) | Low | None |

### Phase 1 — Publication essentials

| # | Chantier | Description | Effort |
|---|----------|-------------|--------|
| 1.0 | **CREDITS.md** | Attribution complète de toutes les inspirations (repos, personnes, papers). Lien depuis README.md section "Acknowledgments" | Medium |
| 1.1 | **CONTRIBUTING.md** | Dev setup, PR process, code style, commit conventions, testing, template testing with copier | Low |
| 1.2 | **CODE_OF_CONDUCT.md** | Contributor Covenant (standard) | Trivial |
| 1.3 | **CHANGELOG.md** | Résumé v0.0.1 → v0.2.0 from tag messages + git history | Medium |
| 1.4 | **.github/ISSUE_TEMPLATE/** | Bug report, feature request, question (YAML format) | Low |
| 1.5 | **.github/PULL_REQUEST_TEMPLATE.md** | Checklist: description, test, copier copy verified | Low |
| 1.6 | **README update** | Add meta_visibility docs, 3 copier modes, badges, link PHILOSOPHY.md, clarify .meta/ visibility trade-off | Medium |
| 1.7 | **.gitignore meta-repo** | Add IDE, dist, build, logs, .DS_Store (align with template's .gitignore) | Trivial |
| 1.8 | **Pre-commit meta-repo** | Add trailing-whitespace, end-of-file-fixer, check-yaml, check-toml | Low |

### Phase 2 — CI/CD & quality

| # | Chantier | Description | Effort |
|---|----------|-------------|--------|
| 2.1 | **GitHub Actions: lint** | ruff check + ruff format --check on PR | Low |
| 2.2 | **GitHub Actions: template test** | copier copy --defaults → uv sync → pytest → ruff on generated project | Medium |
| 2.3 | **GitHub Actions: release** | On tag push → generate GitHub Release with changelog extract | Medium |
| 2.4 | **Template generation tests** | pytest suite: verify copier output structure, file contents, meta_visibility modes | Medium |

### Phase 3 — Git hygiene

| # | Chantier | Description | Effort | Risk |
|---|----------|-------------|--------|------|
| 3.1 | **Git author rewrite** | Fix 38 commits authored as "Claude". Rewrite history + retag | High | Destructive — must be done BEFORE any external fork |
| 3.2 | **Tag v1.0.0** | After all phases complete, annotated tag with full changelog | Low | Immutable — must be right |

---

## 3. Implementation sequence

```
Phase 0 (core product)     ━━━━━━━━━━━━━━━━━━━━  ~2-3 sessions
  0.1 Workflow gates
  0.2 meta_visibility param
  0.3 .meta/ gitignore alignment
  0.4 PILOT.md cleanup
  0.5 Rodin agent
         │
Phase 1 (publication)      ━━━━━━━━━━━━━━━━━━━━  ~1-2 sessions
  1.1-1.8 in parallel
         │
Phase 2 (CI/CD)            ━━━━━━━━━━━━━━━━━━━━  ~1-2 sessions
  2.1-2.4 in parallel
         │
Phase 3 (git hygiene)      ━━━━━━━━━━━━━━━━━━━━  ~1 session
  3.1 Author rewrite (MUST be before any public access)
  3.2 Tag v1.0.0
         │
Beta launch ──────────────────────────────────── Day 0
         │
Public launch ────────────────────────────────── Day 0 + 7-14 jours
```

---

## 4. Beta strategy

### Objectif beta

Obtenir 10-20 beta testeurs qui :
1. Testent `copier copy` sur un vrai projet
2. Reportent les frictions, bugs, confusions
3. Valident que le protocole tient ses promesses
4. Deviennent les premiers ambassadeurs au lancement public

### Profil cible

- Développeurs Python utilisant déjà Claude Code ou des LLMs pour coder
- Créateurs de templates/outils de dev
- Influenceurs dev tooling (LinkedIn, X, YouTube)
- Mainteneurs de repos populaires dans l'écosystème Claude/AI-assisted dev

### Liste de cibles beta

#### GitHub — créateurs de repos pertinents

| Repo / User | Pourquoi | Action |
|-------------|----------|--------|
| **anthropics/claude-code** | L'outil lui-même. Mention officielle = jackpot | Issue/discussion "Community template" |
| **obra/superpowers** | Plugin complémentaire, déjà intégré dans notre template | DM ou issue — synergy naturelle |
| **jlowin/fastmcp** | MCP ecosystem, même audience | DM GitHub |
| **simonw/datasette** | Simon Willison — influenceur AI+dev, Python, très vocal | DM/mention |
| **charliermarsh/ruff** (astral-sh) | Notre stack — on utilise ruff, uv. Visibilité dans leur écosystème | Mention dans une discussion |
| **copier-org/copier** | Le moteur de notre template. Show in their examples/gallery | PR to add to community templates list |
| **tiangolo/fastapi** | Énorme audience Python, potentiel de templates spécialisés | Mention/tag |
| Repos "awesome-claude-code" / "awesome-ai-coding" | Listes curated — inscription directe | PR to add |

#### Reddit

| Subreddit | Stratégie |
|-----------|-----------|
| r/ClaudeAI | Post détaillé "I built a protocol for AI-assisted Python dev" |
| r/ChatGPTCoding | Cross-post (audience AI coding généraliste) |
| r/Python | "Show /r/Python: template system for structured AI-assisted dev" |
| r/MachineLearning | Si angle data science pertinent |
| r/LocalLLaMA | Si support d'autres LLMs envisagé |

#### Hacker News

| Action | Timing |
|--------|--------|
| "Show HN: metadev-protocol — a protocol for AI-assisted Python projects" | Launch day — morning US EST |
| Focus: le problème (context loss), la solution (structure), le one-liner | Keep technical, zero hype |

#### LinkedIn — influenceurs à contacter / taguer

| Personne | Profil | Action |
|----------|--------|--------|
| **Benjamin Code** | [LinkedIn](https://www.linkedin.com/in/benjamin-code-3346a379/) | DM + tag — crédit Rodin, synergy directe |
| **Ludovic Sanchez** | [LinkedIn](https://www.linkedin.com/in/ludovic-sanchez-658b2854/) | DM / tag |
| **Wilfried de Renty** | [LinkedIn](https://www.linkedin.com/in/wilfried-de-renty/) | DM / tag |
| **Pierre R.** | [LinkedIn](https://www.linkedin.com/in/pierre-rondeau/) | DM / tag |
| **Gaël Penessot** | [LinkedIn](https://www.linkedin.com/in/gael-penessot/) | DM / tag |
| **Anthony Renard** | [LinkedIn](https://www.linkedin.com/in/anthonyrenardfox/) | DM / tag |
| **Giovanni Beggiato** | [LinkedIn](https://www.linkedin.com/in/giovanni-beggiato/) | DM / tag |
| **Rémi Tibi** | [LinkedIn](https://www.linkedin.com/in/remi-tibi/) | DM / tag |
| **Arthur Renaud** | [LinkedIn](https://www.linkedin.com/in/arthur-renaud-a9993a49/) | DM / tag |
| **Taha K.** | [LinkedIn](https://www.linkedin.com/in/taha-k-89184192/) | DM / tag |
| **Julian Luneau** | [LinkedIn](https://www.linkedin.com/in/julian-luneau-%F0%9F%A7%AC-b9710b72/) | DM / tag |
| **Ramses Djikaÿ** | [LinkedIn](https://www.linkedin.com/in/ramses-djika%C3%BF-fils/) | DM / tag |
| **Sina Movaghar** | [LinkedIn](https://www.linkedin.com/in/sinamovaghar/) | DM / tag |
| **Romain Maltrud** | [LinkedIn](https://www.linkedin.com/in/romainmaltrud/) | DM / tag |
| **Louis Adam** | [LinkedIn](https://www.linkedin.com/in/louis-adam1/) | DM / tag |
| **Yann Rapaport** | [LinkedIn](https://www.linkedin.com/in/yann-rapaport/) | DM / tag |
| **Charlie Hills** | [LinkedIn](https://www.linkedin.com/in/charlie-hills/) | DM / tag |
| **Medhi El Ouardouni** | [LinkedIn](https://www.linkedin.com/in/medhi-el-ouardouni/) | DM / tag |
| **Hassan Adnan** | [LinkedIn](https://www.linkedin.com/in/hassan-adnan-4b38b5215/) | DM / tag |

**Dream targets (tag, pas de DM direct) :**

| Personne | Pourquoi |
|----------|----------|
| **Jesse Vincent** (obra) | Créateur Superpowers — inspiration workflow |
| **Simon Willison** | Influenceur AI+dev, Python, blog de référence |
| **Boris Cherny** | Créateur de Claude Code, CLAUDE.md best practices |
| **Charlie Marsh** | Créateur ruff/uv — notre stack |
| **Andrej Karpathy** | Inventeur du terme "vibe coding" |
| **François Chollet** | Keras creator, opinions AI fortes |
| **Addy Osmani** | Pattern agent personas |

#### X (Twitter) — comptes à taguer

| Compte | Pourquoi | Action |
|--------|----------|--------|
| **@AnthropicAI** | L'outil parent | Tag dans le thread |
| **@benjamincode** | Agent Rodin — inspiration directe | Tag + crédit |
| **@simonw** | Simon Willison — AI+dev | Tag |
| **@charliermarsh** | ruff/uv creator | Tag |
| **@kaborak** | Jesse Vincent (obra/superpowers) | Tag |
| **@addyosmani** | Agent personas pattern | Tag si pertinent |
| **@fchollet** | Keras, opinions AI | Dream target |
| **@karpathy** | "Vibe coding" originator | Dream target |
| **@firaborakis** | Copier ecosystem | Tag |
| Demo GIF/video | 30s: copier copy → claude → session start | Asset obligatoire |

#### YouTube / Blogs

| Cible | Pourquoi | Action |
|-------|----------|--------|
| **Benjamin Code** (YouTube FR) | 400K+ abonnés, dev FR, créateur Rodin | Contact direct — crédit mutuel |
| Fireship | Dream target — "X in 100 seconds" format parfait | Pitch concis |
| ArjanCodes | Python dev tooling, audience parfaite | Pitch |
| Tech with Tim | Python tutorials, large audience |
| Blog post personnel | Article détaillé "Why I built metadev-protocol" |

---

## 5. Positionnement concurrentiel

### metadev-protocol vs alternatives

| | **LangGraph** | **Setup custom** (ex: Pierre R. "Liberty") | **metadev-protocol** |
|---|---|---|---|
| Niveau | Code (Python SDK) | Manuel (fichiers ad hoc) | Convention (fichiers standardisés) |
| Cible | Agents autonomes en prod | Dev expert Claude Code | Tout dev Python + Claude Code |
| Mémoire | State machine en code | Fichiers custom (48+ fichiers) | PILOT.md + SESSION-CONTEXT.md |
| Human-in-the-loop | Code (interrupt nodes) | Discipline personnelle | Automatism #4 (harness-level) |
| Dépendance runtime | Framework lourd | Aucune | Aucune (fichiers uniquement) |
| Reproductibilité | Code à écrire | Non portable | `copier copy` — 1 commande |
| Mise à jour | Semver packages | Manuelle | `copier update` — semver tags |

**Notre positionnement :** On n'est pas un framework, on est un **protocole**.
Zéro code, zéro dépendance runtime. Juste des fichiers qui structurent la
collaboration humain-AI. Le résultat d'un setup custom comme "Liberty"...
disponible en une commande pour chaque nouveau projet.

---

## 6. Workflow d'outreach personnalisé (beta + lancement)

### Principe

Chaque contact reçoit un message personnalisé en 3 parties :
1. **Hook personnalisé** — montre qu'on connaît et qu'on s'intéresse à SON travail
2. **Corps commun** — pitch metadev-protocol (lien repo ou PDF one-pager)
3. **Call-to-action** — adapté au profil (test, feedback, partage, collaboration)

### Workflow de recherche par personne

Pour chaque contact de la liste :
1. Lire ses 3-5 derniers posts LinkedIn/X
2. Identifier son angle : quel problème il résout, quel public, quel style
3. Trouver le pont : où metadev-protocol rejoint ou complète son travail
4. Rédiger le hook personnalisé (2-3 phrases max)

### Template de message

```
[HOOK PERSONNALISÉ — 2-3 phrases sur son travail récent]

J'ai construit un protocole open-source qui résout exactement ce type
de problème : metadev-protocol. Un `copier copy` et chaque projet
Python démarre avec la mémoire inter-sessions, le workflow structuré,
et les skills intégrés — sans rien coder.

[LIEN: repo GitHub ou PDF one-pager]

[CTA PERSONNALISÉ]
```

### Hooks personnalisés (drafts)

| Personne | Hook | CTA |
|----------|------|-----|
| **Pierre R.** | "Ton post sur l'architecture mémoire de Claude Code m'a marqué — les 48 fichiers typés, les hooks actifs, le Second Brain. J'ai construit exactement ça, mais en template reproductible : chaque nouveau projet démarre avec cette architecture en une commande." | "Tu serais le testeur idéal — ton setup Liberty est le benchmark. Feedback honnête ?" |
| **Ludovic Sanchez** | "Ton approche Forgejo + souveraineté des données résonne fort. metadev-protocol va dans le même sens : tout le contexte AI reste dans le repo, sous ton contrôle, portable, sans dépendance externe." | "En tant que coach Claude Code, ton regard sur le workflow serait précieux. Tu testes ?" |
| **Wilfried de Renty** | "Ton post sur LangGraph met le doigt sur le vrai problème : les chaînes de prompts sans mémoire ni contrôle. On a pris le même problème mais côté dev assisté : un protocole fichier (pas un framework) qui donne structure et mémoire à chaque session Claude Code." | "Curieux d'avoir ton avis d'architecte IA sur cette approche fichier vs framework." |
| **Benjamin Code** | "Ton agent Rodin m'a directement inspiré — l'anti-complaisance et le steelmanning sont intégrés dans notre template comme persona devil's-advocate. Crédit explicite dans le repo." | "J'aimerais te montrer comment on l'a intégré. Ça te dit un retour ?" |
| **Gaël Penessot** | *(à compléter après recherche de ses posts récents)* | Beta test |
| **Giovanni Beggiato** | *(à compléter)* | Beta test |
| **Rémi Tibi** | *(à compléter)* | Beta test |
| **Arthur Renaud** | *(à compléter)* | Beta test |
| **Taha K.** | *(à compléter)* | Beta test |
| **Julian Luneau** | *(à compléter)* | Beta test |
| **Ramses Djikaÿ** | *(à compléter)* | Beta test |
| **Sina Movaghar** | *(à compléter)* | Beta test |
| **Romain Maltrud** | *(à compléter)* | Beta test |
| **Louis Adam** | *(à compléter)* | Beta test |
| **Yann Rapaport** | *(à compléter)* | Beta test |
| **Charlie Hills** | *(à compléter)* | Beta test |
| **Anthony Renard** | *(à compléter)* | Beta test |
| **Medhi El Ouardouni** | *(à compléter)* | Beta test |
| **Hassan Adnan** | *(à compléter)* | Beta test |

### Asset "corps commun"

Préparer un **PDF one-pager** ou une **landing section dans le README** :
- Le problème en 3 bullet points
- La solution en 1 commande
- Ce que tu obtiens (tableau "What You Get" du README)
- Le one-liner `copier copy`
- "Feedback welcome — open a GitHub issue or DM me"

---

## 7. Assets à préparer

*(anciennement section 5)*

### Obligatoires (avant beta)

| Asset | Description | Format |
|-------|-------------|--------|
| **Demo GIF** | copier copy → project generated → claude session → plan → implement | GIF animé, 30-45s |
| **README finalisé** | Version public-ready avec tous les badges, docs, quickstart | Markdown |
| **PHILOSOPHY.md** | Déjà excellent — relire et polir | Markdown |
| **Example session** | Capture d'une vraie session montrant le protocole en action | Markdown dans docs/ |

### Obligatoires (avant lancement public)

| Asset | Description | Format |
|-------|-------------|--------|
| **Thread X** | 5-7 tweets, problème → solution → demo → link | Draft texte |
| **Post LinkedIn** | Long-form, storytelling, résultats concrets | Draft texte |
| **Post Reddit** | Technique, direct, zéro hype, link + quickstart | Draft texte |
| **Post HN** | "Show HN" — ultra concis, technique, link | Draft texte |
| **Release notes v1.0** | Changelog complet, what's included, getting started | GitHub Release |

### Nice-to-have

| Asset | Description | Format |
|-------|-------------|--------|
| **Video demo** | 2-3 min walkthrough complet | MP4 / YouTube |
| **Blog post** | "Why I built metadev-protocol" — storytelling + philosophy | Blog |
| **Comparison table** | metadev-protocol vs cookiecutter vs raw Claude Code | Markdown |
| **Logo** | Identité visuelle pour le projet | SVG |

---

## 8. Séquence de lancement

### Jour J-14 : Beta privée

1. Repo public (ou invitations privées si préféré)
2. Email/DM aux 10-20 beta testeurs identifiés
3. Message type :

> "I've been building a protocol for AI-assisted Python development — it eliminates
> context loss between sessions and enforces structured workflows. I'd love your
> feedback before the public launch. Here's early access: [link]
>
> Try: `copier copy gh:Vincent-20-100/metadev-protocol test-project --trust`
>
> I'm particularly interested in: first impressions, friction points, and whether
> the protocol feels natural or forced. No pressure to respond publicly — just
> honest feedback."

4. Collecter le feedback pendant 7-14 jours
5. Fix les frictions identifiées

### Jour J : Lancement public

Séquence dans la journée (timing US EST pour maximiser la visibilité) :

| Heure (EST) | Action |
|-------------|--------|
| 8h00 | Post Hacker News "Show HN" |
| 8h30 | Thread X (5-7 tweets) |
| 9h00 | Post LinkedIn long-form |
| 10h00 | Post Reddit r/ClaudeAI |
| 10h30 | Post Reddit r/Python |
| 11h00 | PR aux "awesome-*" lists |
| 12h00 | Cross-post Reddit r/ChatGPTCoding |
| PM | Répondre aux commentaires, engage |

### Jour J+1 à J+7 : Amplification

- Répondre à TOUS les commentaires (Reddit, HN, X, GitHub issues)
- Remercier publiquement les beta testeurs qui parlent du projet
- Partager les retours positifs (avec permission)
- Si traction HN : post de suivi "What I learned"

---

## 9. Métriques de succès

### Beta (J-14 à J)

| Métrique | Cible |
|----------|-------|
| Beta testeurs contactés | 20 |
| Beta testeurs ayant testé | 10 |
| Issues/feedback reçus | 5+ |
| Bugs critiques trouvés | 0 (après fix) |

### Lancement (J à J+30)

| Métrique | Cible réaliste | Cible ambitieuse |
|----------|---------------|------------------|
| GitHub stars | 50 | 200 |
| Forks | 5 | 20 |
| HN points | 30 | 100+ (front page) |
| copier copy (si mesurable) | 20 | 100 |
| Issues ouvertes | 10 | 30 |
| Contributors externes | 1 | 5 |

---

## 10. Risques et mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Git author leak visible publiquement | Crédibilité — "AI-generated repo" | Phase 3.1 AVANT toute publication |
| Template cassé pour certaines configs | Première impression ruinée | Phase 2.2 — CI template test |
| "Trop opinionated" — rejet communautaire | Adoption limitée | meta_visibility param + messaging "these are defaults, customize freely" |
| Copier pas assez connu | Friction d'adoption | Quickstart ultra simple, expliquer copier en 1 phrase |
| Claude Code only — pas d'autres LLMs | Marché limité | V1 = Claude Code only (notre force). V2 = adapter à d'autres |
| Pas de traction HN/Reddit | Lancement silencieux | Backup: contacter individuellement les influenceurs, itérer sur le messaging |

---

## 11. Sources & inspirations (CREDITS.md content)

### Repos & outils — inspirations directes

| Source | Auteur | Ce qu'on leur doit | Licence |
|--------|--------|-------------------|---------|
| [Agent Rodin](https://gist.github.com/bdebon/e22d0b728abc5f393227440907b334cf) | Benjamin Code (bdebon) | Anti-complaisance, steelmanning, classification des arguments → devil's-advocate persona | Gist public |
| [obra/superpowers](https://github.com/obra/superpowers) | Jesse Vincent | Workflow brainstorm → spec → plan → execute → review | MIT |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | OthmanAdi | Pattern PILOT.md + SESSION-CONTEXT.md (mémoire fichier) | MIT |
| [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | affaan-m | Patterns agent, continuous learning, multi-agent fork | MIT |
| [claude-code-config](https://github.com/trailofbits/claude-code-config) | Trail of Bits | Security deny rules, bash permission architecture | MIT |
| [copier-uv](https://github.com/pawamoy/copier-uv) | pawamoy | Structure template Python moderne, pyproject.toml patterns | MIT |
| [gstack](https://github.com/garrytan/gstack) | garrytan | Multi-agent sprint workflow, skill distribution SKILL.md.tmpl | MIT |
| [aider](https://github.com/Aider-AI/aider) | Paul Gauthier | CONVENTIONS.md pattern, lint-cmd/test-cmd feedback loop | Apache 2.0 |
| [copier](https://github.com/copier-org/copier) | copier-org | Template engine | MIT |
| [ruff](https://github.com/astral-sh/ruff) | Charlie Marsh / Astral | Linter + formatter | MIT |
| [uv](https://github.com/astral-sh/uv) | Charlie Marsh / Astral | Package manager + build backend | MIT/Apache 2.0 |

### Personnes & concepts

| Personne | Contribution au domaine |
|----------|------------------------|
| **Andrej Karpathy** | Invention du terme "vibe coding" (2025) |
| **Boris Cherny** | Créateur de Claude Code, best practices CLAUDE.md |
| **Addy Osmani** | Pattern agent personas structurés |
| **Benjamin Code** | Agent Rodin — interlocuteur socratique anti-complaisance |

### Recherche académique

| Paper | Auteurs | Contribution |
|-------|---------|-------------|
| [MAD: Multi-Agent Debate](https://arxiv.org/abs/2305.14325) | Du et al. | Architecture 3 rôles (Devil/Angel/Judge) → /debate skill |
| Vibe Coding in Practice (ICSE-SEIP 2026) | — | Validation académique du vibe coding |

---

## 12. Post-launch roadmap (noted, not in scope)

- Support d'autres LLMs (Cursor, Windsurf, Aider)
- Plugin marketplace pour les skills
- CLI `metadev init` comme wrapper autour de copier
- Templates spécialisés (FastAPI, data science, CLI app)
- Documentation site (MkDocs/Sphinx)
- Community Discord/Discussions

---

## Decision

**VALIDATED** (2026-04-08)

1. Séquence Phase 0→1→2→3→Beta→Launch : OK
2. Liste de cibles beta : OK + Benjamin Code ajouté
3. Timing J-14 beta → J launch : OK
4. Posts/DMs : préparation des drafts ensemble
5. Git author rewrite : OUI — obligatoire avant publication
