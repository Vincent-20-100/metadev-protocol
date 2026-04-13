# Plan — `/radar` skill implementation

**Date:** 2026-04-13
**Based on:** `.meta/drafts/brainstorm-2026-04-13-radar-skill.md`
**Confidence:** 🟡 **AMBER**

## Why AMBER

Plan structurellement solide (architecture tranchée par brainstorm + devil's-advocate) mais 4 inconnues à résoudre avant ou pendant l'implémentation :

1. **Format de l'agent `devils-advocate`** — c'est le premier fichier `.claude/agents/*.md` du repo, aucun précédent à mimer. Il faut valider le format attendu par Claude Code (frontmatter YAML ? structure markdown ?) avant d'écrire. Risque : écrire un agent qui ne se charge pas.
2. **Reddit RSS via feedparser** — `https://reddit.com/r/X/.rss` fonctionne en pratique mais Reddit rate-limite les user-agents par défaut. Il faut tester avec un UA custom avant de valider `sources/reddit.py`. Risque : `/radar` marche en dev et échoue en CI.
3. **`huggingface_hub` sans token** — doit marcher pour `list_models(sort="likes")` sur du contenu public, mais untested dans notre contexte. Risque : échec silencieux ou rate-limit.
4. **MIT license attribution** — Agent-Reach est MIT, vendor-in légal. Forme exacte de l'attribution dans les headers de fichiers copiés à confirmer (copyright original + note de modification).

**Action à prendre avant kickoff :** résoudre #1 (format agent) et #2 (Reddit UA) par un spike de 10 min chacun. #3 et #4 sont résolvables pendant l'implémentation.

---

## Files involved

### Prérequis (tracks parallèles, pas bloquants pour `/radar` mais à ship avant ou en parallèle)

- `template/.claude/agents/devils-advocate.md` — **create** — agent flagué "game changer" par Vincent, référencé dans CLAUDE.md mais absent du repo
- `template/.meta/GUIDELINES.md.jinja` — **modify** — nouvelle section "Skill vs tool" codifiant le principe + mention du dossier `research/` dans la taxonomie `.meta/references/`
- `template/CLAUDE.md.jinja` — **modify** — une ligne de renvoi vers le principe Skill vs tool + entrée `/radar` dans la trigger table

### `/radar` core — scripts Python déterministes

- `template/scripts/radar/__init__.py` — **create** — package marker
- `template/scripts/radar/__main__.py` — **create** — CLI entry, parse `--deep` / `--refresh-themes`, invoque `core.run()`
- `template/scripts/radar/core.py` — **create** — orchestration fetch → partition connu/nouveau → score → rank → write → regen index. Retourne un rapport JSON pour le skill
- `template/scripts/radar/dedup.py` — **create** — canonicalisation d'URL par source + match
- `template/scripts/radar/cards.py` — **create** — read/write/append_mention sur les fichiers de cartes
- `template/scripts/radar/themes.py` — **create** — load/save yaml, scoring substring + weight, interface bootstrap (l'extraction LLM elle-même est faite par le skill, `themes.py` expose juste `write_themes_yaml(themes)`)
- `template/scripts/radar/index.py` — **create** — walk des frontmatters sous `cards/`, régénère `INDEX.md`
- `template/scripts/radar/report.py` — **create** — sérialisation JSON du rapport de run (top items, discarded, sources failed, promotion candidates)

### Sources vendored (Agent-Reach + additions)

- `template/scripts/radar/sources/__init__.py` — **create**
- `template/scripts/radar/sources/base.py` — **create** — `Source` ABC (adapté du `Channel` ABC d'Agent-Reach, nom rename). Attribution MIT en header
- `template/scripts/radar/sources/github.py` — **create** — `gh search repos --json ...` via subprocess, parse JSON, renvoie des items normalisés. Inspiré de `channels/github.py` d'Agent-Reach
- `template/scripts/radar/sources/rss.py` — **create** — wrapper `feedparser`, renvoie des items normalisés
- `template/scripts/radar/sources/reddit.py` — **create** — wrapper de `rss.py` qui construit les URLs `https://reddit.com/r/<sub>/hot/.rss` + User-Agent custom
- `template/scripts/radar/sources/huggingface.py` — **create** — wrapper `huggingface_hub.list_models(sort="likes", limit=30)`, renvoie des items normalisés
- `template/scripts/radar/sources/web.py` — **create** — wrapper `curl https://r.jina.ai/<URL>` pour lecture on-demand (pas utilisé dans le fetch régulier, disponible pour le mode `--deep` et le framing)

### Tests (dans `template/tests/`, shippés dans les projets générés)

- `template/tests/test_radar_dedup.py` — **create** — canonicalisation GitHub/HF/Reddit/Jina + round-trip
- `template/tests/test_radar_cards.py` — **create** — write carte neuve, append mention sur carte existante, mentions_count incrémenté, frontmatter valide
- `template/tests/test_radar_themes.py` — **create** — scoring substring + weight, negative_keywords, threshold, yaml load/save
- `template/tests/test_radar_index.py` — **create** — génération INDEX à partir de cartes fixtures, tri par thème + mentions_count desc + date
- `template/tests/test_radar_sources_base.py` — **create** — contrat de la `Source` ABC (can_handle, fetch, check)
- `template/tests/conftest.py` — **modify or create** — fixtures partagées : tmp `research/` layout, cartes fixtures

### Skill mince

- `template/.claude/skills/radar/SKILL.md` — **create** — ~100 LOC, orchestre uniquement les moments LLM (bootstrap thèmes, invocation script, framing résultat, proposition promotion)

### Template wiring

- `template/pyproject.toml.jinja` — **modify** — ajout d'un extra `radar` avec `feedparser>=6.0` et `huggingface_hub>=0.20` (pas dans les deps principales — évite de polluer les projets qui n'utilisent pas `/radar`)

### Meta-repo side

- `CREDITS.md` — **modify** — section "Vendored code" avec attribution `Panniantong/Agent-Reach` MIT, liste des fichiers concernés
- `tests/test_template_generation.py` — **modify** — assertions que le skill `/radar` existe dans le projet généré, que `research/` n'existe PAS au moment de la génération (créé au premier run seulement), que l'extra `radar` est disponible
- `.meta/PILOT.md` — **modify** — ajout des tâches `PM.N /radar`, `PM.N devils-advocate`, `PM.N skill-vs-tool principle`

---

## Tasks

Ordre : prérequis parallèles → sources (bas niveau) → core (dépend sources) → tests (dépendent core) → skill (dépend core) → wiring → docs.

Chunks de 2-5 min chacun. Les tâches sont regroupées en commits logiques (`feat:`, `docs:`, `test:`) — la colonne "Commit group" indique le regroupement.

### Phase 0 — Spikes préalables (résout AMBER #1 et #2)

#### 0.1 — Spike format agent Claude Code
- **Files:** (lecture uniquement)
- **Do:** WebFetch doc officielle Claude Code sur le format `.claude/agents/*.md`. Alternativement, grep dans `~/.claude/` ou les plugins superpowers/feature-dev pour trouver un exemple d'agent existant. Noter le format frontmatter + structure attendue dans une note `.meta/drafts/agent-format-note.md` (throwaway).
- **Verify:** on a au moins un exemple concret d'agent qui se charge correctement.
- **Commit group:** aucune (spike)

#### 0.2 — Spike Reddit RSS User-Agent
- **Files:** (test manuel)
- **Do:** `curl -A "radar/0.1 (metadev-protocol)" https://www.reddit.com/r/MachineLearning/hot/.rss | head -50`. Valider qu'on reçoit du XML et pas une page de blocage Reddit.
- **Verify:** réponse 200 + feed XML parsable.
- **Commit group:** aucune (spike)

### Phase 1 — Prérequis (commits indépendants, parallélisables avec Phase 2+)

#### 1.1 — Section "Skill vs tool" dans GUIDELINES
- **Files:** `template/.meta/GUIDELINES.md.jinja`
- **Do:** ajouter une nouvelle section `## Skill vs tool — le principe du LLM minimal` entre "Code structure" et "Dependencies", contenant le filtre 80/20 (déterministe vs LLM), le pattern bon (`scripts/` + skill mince), l'anti-pattern (skill qui boucle du Bash). Voir `feedback_skill_vs_tool_principle` memory pour le contenu exact.
- **Verify:** `copier copy . /tmp/test-proj --defaults` réussit, le fichier généré contient bien la nouvelle section.
- **Commit group:** `docs(template): add Skill vs tool principle to GUIDELINES`

#### 1.2 — Ajout trigger /radar + renvoi skill-vs-tool dans CLAUDE.md
- **Files:** `template/CLAUDE.md.jinja`
- **Do:** (a) dans la trigger table section "Skills & Agents", ajouter une ligne `| /radar | skill | veille tech automatisée ... | Propose |`. (b) dans la section "Skills & Agents", ajouter une phrase du type "Nouveau skill ? Applique le filtre Skill vs tool de GUIDELINES.md avant de coder."
- **Verify:** `copier copy . /tmp/test-proj --defaults` réussit, la trigger table généré liste bien `/radar`.
- **Commit group:** `docs(template): add Skill vs tool principle to GUIDELINES` (bundled avec 1.1)

#### 1.3 — Agent `devils-advocate` (dépend de spike 0.1)
- **Files:** `template/.claude/agents/devils-advocate.md`
- **Do:** créer l'agent selon le format identifié en 0.1. Contenu : persona d'un sceptique qui challenge N décisions récentes, doit attaquer au moins 3 points en steelman + contest + expose, doit poser une question de validation empirique à la fin. Voir `feedback_devils_advocate_rule_of_3` memory pour les principes.
- **Verify:** invocation manuelle via Task tool (subagent_type=devils-advocate) sur un sujet trivial et observer que l'agent se charge et répond.
- **Commit group:** `feat(template): add devil's-advocate agent for Rule of 3 check`

### Phase 2 — Vendor-in sources (bas niveau, aucune dépendance amont sauf Phase 0)

#### 2.1 — `sources/base.py` — Source ABC
- **Files:** `template/scripts/radar/__init__.py`, `template/scripts/radar/sources/__init__.py`, `template/scripts/radar/sources/base.py`
- **Do:** créer les package markers. Dans `base.py`, copier la structure de `Channel` ABC d'Agent-Reach (`/tmp/audit-agent-reach/agent_reach/channels/base.py`) en renommant `Channel` → `Source`. Ajouter une méthode abstraite `fetch(self, query: str, limit: int) -> list[Item]` où `Item` est une dataclass `{url, title, pitch, score_raw, discovered, source_name}`. Attribution MIT en header (copyright Panniantong + note "adapted for metadev-protocol").
- **Verify:** `import template.scripts.radar.sources.base` fonctionne, `Source` est bien une ABC non-instanciable.
- **Commit group:** `feat(template): vendor Agent-Reach Source ABC for /radar`

#### 2.2 — `sources/github.py`
- **Files:** `template/scripts/radar/sources/github.py`
- **Do:** sous-classe `Source` qui fait `subprocess.run(["gh", "search", "repos", query, "--sort", "stars", "--limit", str(limit), "--json", "name,fullName,description,stargazersCount,url"])` et parse le JSON en `list[Item]`. `can_handle(url)` check `github.com`. `check()` = `shutil.which("gh")` + `gh auth status`. Attribution MIT.
- **Verify:** test manuel `python -m template.scripts.radar.sources.github "mcp"` renvoie 10 items.
- **Commit group:** `feat(template): vendor Agent-Reach Source ABC for /radar`

#### 2.3 — `sources/rss.py` + `sources/reddit.py`
- **Files:** `template/scripts/radar/sources/rss.py`, `template/scripts/radar/sources/reddit.py`
- **Do:** `rss.py` = sous-classe `Source` avec `fetch(feed_url, limit)` qui appelle `feedparser.parse(feed_url)` et normalise les `entries[:limit]` en `Item` (score_raw = position chronologique). `reddit.py` = thin wrapper qui accepte une liste de subreddits, construit les URLs `https://www.reddit.com/r/<sub>/hot/.rss`, appelle `rss.fetch` avec un User-Agent custom passé via `feedparser.parse(url, agent="radar/0.1 (metadev-protocol)")`.
- **Verify:** tests unitaires avec feed fixture (xml local), pas de call réseau.
- **Commit group:** `feat(template): add RSS and Reddit sources for /radar`

#### 2.4 — `sources/huggingface.py`
- **Files:** `template/scripts/radar/sources/huggingface.py`
- **Do:** sous-classe `Source`, `fetch(query, limit)` appelle `huggingface_hub.list_models(search=query, sort="likes", limit=limit)`, normalise en `Item` avec `score_raw = model.likes`. `check()` vérifie `huggingface_hub` importable.
- **Verify:** test unitaire avec mock de `list_models` renvoyant une liste de fixtures.
- **Commit group:** `feat(template): add HuggingFace source for /radar`

#### 2.5 — `sources/web.py`
- **Files:** `template/scripts/radar/sources/web.py`
- **Do:** sous-classe `Source` avec une méthode `read(url)` qui renvoie le markdown de Jina Reader via `curl -s https://r.jina.ai/<url>` (utilisée à la demande par le skill pour approfondir une carte). `fetch()` n'est pas implémentée (raise NotImplementedError) — cette source est en lecture uniquement, pas en recherche.
- **Verify:** test unitaire avec mock subprocess.
- **Commit group:** `feat(template): add Jina Reader web source for /radar`

### Phase 3 — Core déterministe (dépend Phase 2)

#### 3.1 — `dedup.py` + test
- **Files:** `template/scripts/radar/dedup.py`, `template/tests/test_radar_dedup.py`
- **Do:** fonctions `canonicalize(url, source_name) -> str` avec règles par source (github strip tree/blob, hf garder owner/model, reddit garder link, web strip utm params). Fonction `is_known(canonical_url, index_path) -> bool` qui lit `research/INDEX.md` frontmatters et check la présence. Test : 6-8 cas d'URLs par source + round-trip.
- **Verify:** `uv run pytest tests/test_radar_dedup.py -v` — tous verts.
- **Commit group:** `feat(template): implement /radar dedup and canonicalization`

#### 3.2 — `cards.py` + test
- **Files:** `template/scripts/radar/cards.py`, `template/tests/test_radar_cards.py`
- **Do:** fonctions `write_new_card(item, theme, research_dir)` et `append_mention(card_path, new_item)` qui lit le YAML frontmatter, incrémente `mentions_count`, ajoute une ligne sous `## Mentions`, réécrit. Utilise `python-frontmatter` ou parsing YAML manuel (stdlib). Tests : créer une carte, l'append 2 fois, vérifier le contenu final.
- **Verify:** `uv run pytest tests/test_radar_cards.py -v` — tous verts.
- **Commit group:** `feat(template): implement /radar card write and mention append`

#### 3.3 — `themes.py` + test
- **Files:** `template/scripts/radar/themes.py`, `template/tests/test_radar_themes.py`
- **Do:** fonctions `load_themes(path) -> list[Theme]`, `save_themes(themes, path)`, `score_item(item, theme) -> float` (substring lowercase + weight), `filter_items(items, themes, threshold=1.0) -> dict[theme_name, list[Item]]`. Pas de bootstrap LLM ici — c'est le skill qui fait l'extraction et appelle `save_themes`. Tests : scoring d'items fixtures contre thèmes fixtures, negative_keywords, threshold.
- **Verify:** `uv run pytest tests/test_radar_themes.py -v` — tous verts.
- **Commit group:** `feat(template): implement /radar theme scoring and yaml I/O`

#### 3.4 — `index.py` + test
- **Files:** `template/scripts/radar/index.py`, `template/tests/test_radar_index.py`
- **Do:** fonction `regenerate_index(research_dir)` qui walk `research/cards/`, lit tous les frontmatters, groupe par thème, trie par `mentions_count desc` puis `discovered desc`, écrit `research/INDEX.md` avec une section par thème. Format : tableau markdown une ligne par carte avec pitch, mentions_count, date. Tests : créer 5 cartes fixtures, régénérer, assert format.
- **Verify:** `uv run pytest tests/test_radar_index.py -v` — tous verts.
- **Commit group:** `feat(template): implement /radar INDEX auto-generation`

#### 3.5 — `sources/base.py` test (contrat ABC)
- **Files:** `template/tests/test_radar_sources_base.py`
- **Do:** test que `Source` est abstraite, qu'une sous-classe minimale fonctionne, qu'un `Item` est hashable par URL.
- **Verify:** `uv run pytest tests/test_radar_sources_base.py -v` — vert.
- **Commit group:** `feat(template): vendor Agent-Reach Source ABC for /radar` (bundled avec 2.1)

#### 3.6 — `report.py`
- **Files:** `template/scripts/radar/report.py`
- **Do:** dataclass `RunReport` avec `top_items_per_theme`, `discarded`, `sources_failed`, `promotion_candidates` (cartes avec `mentions_count >= 3` nouvellement atteint). Sérialisation JSON.
- **Verify:** import + sérialisation d'un report fixture.
- **Commit group:** `feat(template): implement /radar core orchestration`

#### 3.7 — `core.py` + `__main__.py`
- **Files:** `template/scripts/radar/core.py`, `template/scripts/radar/__main__.py`
- **Do:** `core.run(mode: "normal"|"deep", research_dir, themes_path) -> RunReport` qui orchestre : load themes → pour chaque source active, fetch → canonicalize → partition known/new → pour known append_mention → pour new score + filter + rank + take top K → write cards → regenerate index → build RunReport → return. `__main__.py` parse argparse (`--deep`, `--refresh-themes`, `--project-dir`), appelle `core.run`, print le JSON sur stdout.
- **Verify:** test d'intégration manuel : créer un `research-themes.yaml` fixture, lancer `python -m scripts.radar` dans un projet de test, observer le rapport JSON.
- **Commit group:** `feat(template): implement /radar core orchestration`

### Phase 4 — Skill mince (dépend Phase 3)

#### 4.1 — `SKILL.md`
- **Files:** `template/.claude/skills/radar/SKILL.md`
- **Do:** ~100 lignes de markdown. Sections : Usage, Hard rules (no manual fetching, always invoke script), Process (step 1: bootstrap si pas de yaml = lit PILOT.md et propose → save via themes.save_themes ; step 2: `uv run python -m scripts.radar [--deep]` ; step 3: lit RunReport stdout, présente top 3 chauds + nouveautés par thème + sources failed ; step 4: propose promotions si candidates), Failure modes, Rationalizations. Pas de boucle de fetch dans le SKILL.md — c'est le script qui fetche.
- **Verify:** invocation manuelle du skill sur un projet de test, premier run → bootstrap thèmes, deuxième run → fetch + présentation.
- **Commit group:** `feat(template): add /radar skill wrapper`

### Phase 5 — Template wiring + meta-repo docs (dépend Phase 4)

#### 5.1 — Optional deps dans pyproject
- **Files:** `template/pyproject.toml.jinja`
- **Do:** ajouter `[project.optional-dependencies]` avec `radar = ["feedparser>=6.0", "huggingface_hub>=0.20"]`. Le SKILL.md mentionne l'installation via `uv sync --extra radar` au premier run.
- **Verify:** `copier copy . /tmp/test-proj --defaults && cd /tmp/test-proj && uv sync --extra radar` fonctionne.
- **Commit group:** `feat(template): add /radar optional dependencies`

#### 5.2 — Meta-repo CREDITS.md
- **Files:** `CREDITS.md`
- **Do:** section "Vendored code" avec ligne `Panniantong/Agent-Reach (MIT) — Source ABC + channels github/rss pattern — vendored into template/scripts/radar/sources/`.
- **Verify:** lecture humaine.
- **Commit group:** `docs: add Agent-Reach attribution for vendored code`

#### 5.3 — Template generation test update
- **Files:** `tests/test_template_generation.py`
- **Do:** ajouter assertions : (a) `template/.claude/skills/radar/SKILL.md` est bien copié dans le projet généré, (b) `scripts/radar/` est copié, (c) `research/` n'existe PAS dans le projet généré, (d) `research-themes.yaml` n'existe PAS dans le projet généré.
- **Verify:** `uv run pytest tests/test_template_generation.py -v` — vert.
- **Commit group:** `test: verify /radar ships without polluting generated projects`

### Phase 6 — PILOT.md update + release

#### 6.1 — PILOT.md backlog entries
- **Files:** `.meta/PILOT.md`
- **Do:** marquer les tâches `/radar` DONE dans le backlog (ou les créer si elles n'existent pas), ajouter `devils-advocate agent DONE`, `skill-vs-tool principle DONE`, ajouter deux nouvelles entrées PENDING : "refactor /research sous skill-vs-tool" et "refactor /audit-repo sous skill-vs-tool".
- **Verify:** lecture humaine du PILOT.md.
- **Commit group:** `docs(meta): update PILOT after /radar + devils-advocate ship`

#### 6.2 — Release tag
- **Files:** aucune (git tag seulement)
- **Do:** une fois tous les commits des phases précédentes mergés et tests verts, `git tag -a vX.Y.0 -m "..."` avec le message listant les changements (Added: `/radar`, `devils-advocate`; Changed: GUIDELINES codifies Skill vs tool; Fixed: none).
- **Verify:** `git tag` liste le nouveau tag, `git show vX.Y.0` affiche le message.
- **Commit group:** (tag, pas un commit)

---

## Ripple effects non-oubliés (cross-check brainstorm)

- ✅ `template/.meta/GUIDELINES.md.jinja` (1.1) — Skill vs tool + mention `research/`
- ✅ `template/CLAUDE.md.jinja` (1.2) — trigger table + renvoi
- ✅ `template/pyproject.toml.jinja` (5.1) — extra deps
- ✅ `CREDITS.md` (5.2) — attribution MIT
- ✅ `tests/test_template_generation.py` (5.3) — verify YAGNI (pas de pollution)
- ✅ `.meta/PILOT.md` (6.1) — backlog updates
- ✅ Pas de création de `research/` ou `research-themes.yaml` au template generation (confirmé dans 5.3)
- ✅ README.md meta-repo — **PAS nécessaire** pour V1 ; le skill est auto-documenté via son SKILL.md. À ajouter si on produit une release notes publique.

---

## Risques non-résolus à retester à la fin

1. Comportement de `/radar` sur un projet fraîchement généré avec `research-themes.yaml` et `research/` absents — vérifier que le premier run bootstrap proprement sans crash.
2. Comportement quand toutes les sources échouent simultanément — le RunReport doit être valide et le skill doit présenter "aucune source n'a répondu" sans exception.
3. Performance du walk d'`index.py` au-delà de 100 cartes — doit rester sous 500ms. Si ça dérape on optimise en V1.1.

---

## Next step

**Pour Vincent** : relire ce plan, valider la structure et l'ordre. Points de validation :
- Les phases 0 (spikes) sont-elles acceptables comme préalable ? Alternative : plonger directement en 1.1 sans spikes et corriger en cours de route.
- L'ordre Phase 1 (prérequis) → Phase 2 (sources) est-il correct, ou tu préfères que `/radar` ship d'abord et les prérequis après ?
- Le découpage en commits est-il cohérent avec la règle 4 du CLAUDE.md (1 commit = 1 logical unit) ?
- L'extra deps `radar` dans pyproject.toml au lieu de deps mainline — OK pour toi ?

Après validation : `git mv .meta/drafts/plan-2026-04-13-radar-skill.md .meta/active/plan-2026-04-13-radar-skill.md` et début de l'exécution phase par phase.
