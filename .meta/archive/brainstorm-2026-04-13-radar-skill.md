# Brainstorm — `/radar` skill pour metadev-protocol

**Date:** 2026-04-13
**Contexte amont:** audit `.meta/references/interim/session-2026-04-13-audit-agent-reach.md`
**Memories associées:** `feedback_skill_vs_tool_principle`, `feedback_devils_advocate_rule_of_3`, `project_metadev_skills_refactor_backlog`

## Objectif

Créer un outil de veille tech automatisée pour metadev-protocol, utilisable dans les projets générés, qui fetche des items pertinents depuis plusieurs sources (GitHub, HuggingFace, RSS, Reddit, Web) et construit une base de connaissance markdown navigable par progressive disclosure. Sert deux usages intégrés dans un seul skill :

- **Veille émergente** (mode normal) — "qu'est-ce qui vient de sortir proche de mon projet ?"
- **État de l'art large** (mode `--deep`) — "c'est quoi le paysage de X ?"

Use case validé empiriquement par Vincent ("je l'ai fait très régulièrement").

## Décisions

- **Décision 1 — Un seul skill `/radar` avec flag `--deep`**
  Choix : un point d'entrée unique, le mode par défaut fait de la veille fréquente top-K, `--deep` élargit les budgets pour un survey trimestriel.
  Rejeté : **2 skills séparés (`/survey` + `/radar`)** — écarté après devil's-advocate : `/survey` aurait été dead weight parce qu'un solo dev ne fait pas de revues trimestrielles en pratique, seul `/radar` tournerait vraiment. Un skill qui dort est un skill de trop.
  Rejeté : **1 skill `/research-kb` avec sous-commandes à la Agent-Reach** — mini-CLI interne, contourne l'atomicité recommandée, risque de devenir un framework en miniature.

- **Décision 2 — Naming `/radar`, sans préfixe**
  Choix : nom court, verbe d'action, porte intrinsèquement la notion de détection + proximité au projet.
  Rejeté : **`/survey` + `/radar`** — découle de la décision 1.
  Rejeté : **préfixe `/search-radar` ou `/outreach-radar`** — préfixe redondant avec le namespacing de Claude Code (`projectSettings:radar`), `search` clashe avec `WebSearch`, `outreach` est un faux ami en anglais (= atteindre des personnes, pas scanner des sources). La proximité thématique se signale via trigger table + cross-links dans SKILL.md, pas via préfixe à taper.
  Rejeté : **`/landscape` + `/pulse`, `/atlas` + `/radar`** — trop imagés ou trop livresques.

- **Décision 3 — 5 sources V1, tier-0 uniquement**
  Choix : GitHub (`gh search`), HuggingFace (`huggingface_hub`), RSS générique (`feedparser`), Reddit (via flux RSS, pas OAuth), Web (`curl r.jina.ai`).
  Rejeté : **ajout d'Exa (tier-1)** — clé API à créer même si gratuite, casse "copier copy et ça marche". Ajoutable V1.1 si manque mesuré.
  Rejeté : **ajout de X/Twitter (tier-2)** — cookies expirent, maintenance continue, info X recoupe HN+Reddit+HF avec 24-48h de décalage, acceptable en V1.
  Rejeté : **sources chinoises et métier-spécifiques** (XHS, douyin, weibo, bilibili, v2ex, wechat, xiaoyuzhou, xueqiu, linkedin, boss直聘) — hors use case Vincent, reject pur.

- **Décision 4 — Schéma à deux niveaux, dossier `research/` sibling top-level**
  Choix : nouveau dossier `.meta/references/research/` (sibling à `raw/interim/synthesis/`), progressive disclosure 3 couches :
  - Layer 1 = `research/INDEX.md` (toujours loaded, listing compact auto-généré)
  - Layer 2 = `research/cards/<theme>/<source>-<slug>.md` (cartes ~200 mots, loadées sur match de thème)
  - Layer 3 = `research/synthesis/<theme>-<slug>.md` (synthèses longues, loadées sur demande explicite)

  Schéma de carte avec frontmatter YAML :
  ```yaml
  ---
  source: github | hf | rss | reddit | web
  source_url: <URL canonique>
  title: ...
  pitch: <1 ligne>
  tier: card | synthesis
  discovered: YYYY-MM-DD
  mentions_count: 1
  tags: [...]
  themes: [...]
  has_synthesis: true | false
  ---
  ## Pitch
  ## Pourquoi c'est pertinent
  ## Mentions
  - YYYY-MM-DD — <source> (<popularity signal>)
  ## Liens
  ```
  Rejeté : **nesting dans `interim/research/` ou `synthesis/research/`** — contradiction sémantique ("synthèse intérimaire" n'a pas de sens ; les cartes ne sont pas des synthèses). Un sibling top-level dédié au contenu skill-automatisé sépare proprement l'output machine du contenu humain curé.
  Rejeté : **schéma à un seul niveau (option A)** — perd la progressive disclosure qu'on vient de décider, force à reconstruire la distinction au parsing.
  Rejeté : **raw output par source + métadonnées séparées (option C)** — pas de normalisation, coût payé à chaque lecture, impossible de construire l'INDEX efficacement.

- **Décision 5 — Dedup par URL canonicalisée avec append de mention**
  Choix : avant d'écrire une carte, scan de l'INDEX pour match d'URL canonicalisée. Si trouvé, append d'une ligne dans la section `## Mentions` de la carte existante + incrément de `mentions_count`. Jamais de skip — les mentions multiples sont le signal cross-source le plus fort.
  Rejeté : **skip simple sur doublon (option A)** — perd l'info de pertinence émergente, "mentionné par 3 sources en 2 semaines" est plus précieux que la première découverte.
  Rejeté : **pas de dedup, fusion au read (option C)** — pollue l'INDEX, recalcule à chaque invocation, taxe permanente pour éviter une complexité d'écriture ponctuelle.
  Canonicalisation par source : GitHub strip `/tree/*` et `/blob/*` ; HF canonique `huggingface.co/<owner>/<model>` ; RSS/Reddit garde le `link` du feed ; Jina strip les `?utm_*`.
  Mécanisme de cleaning fuzzy-match (repos renommés, forks devenus canoniques) reporté en V1.1+.

- **Décision 6 — Bootstrap semi-auto des thèmes depuis PILOT.md**
  Choix : fichier `.meta/research-themes.yaml` au niveau de `PILOT.md`. Au premier run de `/radar` (ou sur `/radar --refresh-themes`), le skill lit `PILOT.md`, extrait un brouillon de thèmes via LLM, propose le yaml à l'utilisateur, sauve après validation. Runs suivants : lecture déterministe du fichier.
  Format :
  ```yaml
  default_theme: <nom>
  max_new_per_source: 5
  max_new_per_theme: 15
  themes:
    - name: agentic-research
      keywords: [agent, mcp, research, crawl, llm tools]
      negative_keywords: [game, minecraft]
      sources: [github, hf, rss]
      weight: 1.0
  ```
  Scoring : substring match lowercase sur `title + pitch`, somme pondérée des `weight`, threshold `>= 1.0`. Negative keywords retirent l'item. ~15 lignes de Python.
  Sélection : partition connu/nouveau, connus → mention, nouveaux → score → ranking par popularité native de la source (`stars` GitHub, `likes` HF, ordre RSS/Reddit), top K par (source × thème) borné par `max_new_per_source` et `max_new_per_theme`. Pas de normalisation cross-source — `mentions_count` est le vrai signal cross-source et émerge au fil des runs.
  Rejeté : **fichier 100% manuel (option A, version initiale)** — écarté après devil's-advocate : risque élevé de rot silencieux quand le projet pivote et que PILOT.md dérive ; `/radar` continuerait à servir des filtres obsolètes sans signal d'erreur.
  Rejeté : **inférence 100% automatique à chaque run (option B)** — boîte noire non-auditable, coût LLM récurrent, dépend de l'état de PILOT.md à chaque invocation.
  Failure modes explicites : pénurie (aucun item ne passe le threshold) → log "aucune nouveauté pour thème X" ; inondation → top K + section "discarded" dans l'output pour tuner ; source cassée → log + continue, pas de crash (principe du `doctor`).
  Reportés V1.1+ : score composite (popularité × recency × theme match), decay temporel des items anciens, boost explicite par `mentions_count` au ranking.

- **Décision 7 — Architecture : script Python déterministe + skill mince, pas de MCP**
  Choix : `/radar` est classifié comme **tool** selon le principe skill-vs-tool (~90% déterministe). Layout :
  ```
  template/
  ├── scripts/radar/
  │   ├── __main__.py         # CLI: uv run python -m scripts.radar [--deep]
  │   ├── core.py             # fetch → dedup → score → rank → write
  │   ├── sources/            # vendor-in Agent-Reach
  │   │   ├── base.py         # Channel ABC (copié from Agent-Reach)
  │   │   ├── github.py       # vendored
  │   │   ├── rss.py          # vendored + adapté Reddit
  │   │   ├── huggingface.py  # nouveau
  │   │   └── web.py          # wrapper Jina Reader
  │   ├── index.py            # génération auto INDEX.md
  │   └── themes.py           # bootstrap depuis PILOT.md + scoring
  └── .claude/skills/radar/
      └── SKILL.md            # ~100 lignes max
  ```
  SKILL.md fait 3 choses : (1) bootstrap des thèmes au premier run (moment LLM : extraction sémantique de PILOT.md), (2) invocation `uv run python -m scripts.radar`, (3) framing du résultat avec contexte (moment LLM : présentation des top items, propositions de promotion). Le reste (fetch, dedup, score, rank, write, INDEX) est 100% Python, aucun token LLM consommé.
  Rejeté : **dépendance PyPI `agent-reach`** — embarque 15 sources dont 80% inutiles + `cli.py` de 1721 lignes, couplage au format OpenClaw et à leur config YAML spécifique. Vendor-in de 4 fichiers (~150 LOC total) + attribution MIT dans CREDITS.md est plus léger.
  Rejeté : **réécriture from scratch sans vendor-in** — refaire 36 lignes de Channel ABC qui marchent déjà est une optimisation esthétique sans valeur.
  Rejeté : **MCP server V1** — sert à exposer la logique à d'autres agents externes, pas nécessaire pour un seul consommateur Claude Code. Revisiter quand Nightshift voudra invoquer `/radar` à distance.

- **Décision 8 — `INDEX.md` auto-généré à chaque run**
  Choix : script Python walk les frontmatters YAML des cartes sous `research/cards/`, régénère `research/INDEX.md` complet (triée par thème, mentions_count desc, discovered desc). Une seule section, pas de contenu manuel.
  Rejeté : **INDEX manuel** — drift garanti entre l'INDEX et les cartes, coût de maintenance sans valeur ajoutée.
  Rejeté : **INDEX hybride (auto + section pinned manuelle)** — complexifie la régénération, bénéfice marginal. Le user peut toujours taguer ses favoris via `tags:` dans les cartes, le tri naturel remonte ce qui compte.

## Sources vendored (attribution MIT dans CREDITS.md)

- `Panniantong/Agent-Reach` — patterns empruntés : `Channel` ABC (base.py), structure de `channels/github.py` et `channels/rss.py`, tier system 0/1/2, concept du `doctor`, conventions de `can_handle(url)` et `check(config)`. Licence MIT compatible.

## Open questions

- **Promotion carte → synthèse** : automatique quand `mentions_count >= 3` ou manuelle via commande dédiée (`/radar promote <slug>`) ? À trancher dans le plan d'implémentation. Piste par défaut : proposition auto dans le framing LLM en fin de run, exécution après confirmation user.
- **Extraction exacte des thèmes depuis PILOT.md** au bootstrap : quelles sections lire, quel format de prompt pour le LLM, validation YAML avant écriture ? Détail d'implémentation pour le plan, pas structurant.
- **Liste par défaut des feeds RSS** pour le template : Hacker News, r/MachineLearning, r/LocalLLaMA, simonwillison.net — à figer dans une référence de template avec possibilité d'override per-project.
- **Rate limiting et politesse** vers les sources externes : politique V1 = laisser échouer, logger, continuer. Politique long terme = cool-down per-source à intégrer quand on ajoutera le scheduling server.
- **Mécanisme de cleaning fuzzy-match** (repos renommés, forks devenus canoniques, titres proches) : reporté V1.1+ une fois qu'on aura de vrais doublons à traiter.
- **Score composite, decay temporel, boost mentions_count** au ranking : roadmap V1.1+ explicite, ne pas ajouter en V1.

## Prérequis / dépendances amont

- **Implémenter l'agent `devil's-advocate`** dans `template/.claude/agents/` — flagué comme "game changer" par Vincent, référencé dans la trigger table du CLAUDE.md mais pas encore écrit. Pas un bloqueur pour `/radar` mais à prioriser en parallèle.
- **Section "Skill vs tool"** à ajouter dans `template/.meta/GUIDELINES.md.jinja` + ligne de renvoi dans `template/CLAUDE.md.jinja`. Codifie le principe utilisé pour designer `/radar`. Pas un bloqueur mais devrait shipper en même temps que `/radar` pour justifier l'architecture atypique.

## Ripple effects à prévoir dans le plan

- `template/pyproject.toml.jinja` — ajouter `huggingface_hub` et `feedparser` en dépendances (tier-0 sans besoin de tokens pour le read public)
- `template/.meta/GUIDELINES.md.jinja` — section Skill vs tool + mention du nouveau dossier `research/` dans la taxonomie `.meta/references/`
- `template/CLAUDE.md.jinja` — ajout de `/radar` dans la trigger table Skills & Agents avec description courte
- `template/.gitignore.jinja` — rien à ajouter, `research/` est tracké par défaut
- `template/.meta/research-themes.yaml` — PAS créé par le template ; le skill le crée au premier run (évite de polluer les projets qui n'utiliseront jamais `/radar`)
- `template/.meta/references/research/` — PAS créé par le template ; le skill crée ce dossier au premier run (même raison)
- `CREDITS.md` (meta-repo + template) — ajout de l'attribution `Panniantong/Agent-Reach` MIT pour les fichiers vendored
- Tests : `tests/test_template_generation.py` doit vérifier qu'un projet généré n'a PAS `research/` avant le premier run de `/radar` (preservation YAGNI pour les non-users), et qu'un projet généré a bien le skill `/radar` disponible

## Next step

Lancer `/plan` sur ce brainstorm pour décomposer en tâches atomiques commitables. Le plan devra :

1. Commencer par les prérequis (`devil's-advocate` agent, section GUIDELINES Skill vs tool)
2. Vendor-in Agent-Reach (Channel ABC + 4 channels) dans `template/scripts/radar/sources/`
3. Écrire le core déterministe (`core.py`, `themes.py`, `index.py`) avec tests unitaires
4. Écrire le SKILL.md mince
5. Test d'intégration : générer un projet via copier, lancer `/radar` au premier run, valider le bootstrap + le premier fetch
6. Documenter dans README.md (meta-repo) et dans le README.md.jinja généré

Plan à produire dans `.meta/drafts/plan-2026-04-13-radar-skill.md` puis validé → `.meta/active/`.
