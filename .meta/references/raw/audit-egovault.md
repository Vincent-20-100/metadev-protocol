# Audit EgoVault — pour metadev-protocol

**Date :** 2026-04-01
**Repo :** `egovault` (Python 3.10+, SQLite, FastAPI, MCP)
**Version :** 2.0.0
**État :** projet fonctionnel, 374 tests passing, architecture stabilisée post-refactoring VaultContext

---

## Section 1 — Architecture du repo

### Arborescence (2 niveaux, annotée)

```
egovault/
├── core/                    <- Interfaces, schemas Pydantic, config, erreurs, sécurité, UID
│   ├── config.py            <- Chargement + validation des 3 YAML via Pydantic
│   ├── context.py           <- VaultContext (DI container) + Protocols
│   ├── schemas.py           <- Tous les modèles Pydantic (Note, Source, *Result, *Filters)
│   ├── errors.py            <- Exceptions métier (NotFoundError, ConflictError, LargeFormatError)
│   ├── security.py          <- Validation URLs, paths, permissions
│   ├── logging.py           <- Décorateur @loggable + callback injection
│   ├── sanitize.py          <- Redaction de données sensibles dans les logs
│   └── uid.py               <- Génération UUID4 + slugs
├── tools/                   <- Fonctions atomiques — typed input -> typed output
│   ├── media/               <- transcribe, compress, fetch_subtitles, extract_audio
│   ├── text/                <- chunk, embed, embed_note, summarize
│   ├── vault/               <- CRUD notes/sources, search, finalize, generate, purge, restore
│   └── export/              <- typst, mermaid
├── workflows/               <- Orchestration séquentielle de tools (ingest_youtube, audio, pdf)
├── infrastructure/          <- Implémentations concrètes (DB, embedding, LLM, vault writer)
│   ├── context.py           <- build_context() — factory VaultContext
│   ├── db.py                <- SQLite + sqlite-vec, init/migration
│   ├── vault_db.py          <- VaultDB facade (~25 méthodes de délégation)
│   ├── embedding_provider.py
│   ├── llm_provider.py
│   └── vault_writer.py
├── api/                     <- FastAPI — routing only, zero business logic
│   ├── main.py              <- create_app() factory, rate limiting, lifespan
│   ├── models.py            <- Modèles request/response API
│   └── routers/             <- 7 routers (health, jobs, ingest, notes, sources, search, vault)
├── cli/                     <- Typer CLI — routing only
│   ├── main.py              <- Entry point, commandes assemblées
│   ├── output.py            <- Helpers de formatage Rich
│   └── commands/            <- ingest, search, notes, sources, status, purge
├── mcp/
│   └── server.py            <- FastMCP server — 22+ tools exposés via MCP
├── config/
│   ├── system.yaml          <- Params algo + taxonomie (versionné)
│   ├── user.yaml            <- Préférences utilisateur (gitignored)
│   ├── install.yaml         <- Chemins machine + secrets (gitignored)
│   └── templates/generation/ <- Prompt templates YAML (extensible)
├── tests/                   <- Miroir exact de la structure source
├── scripts/
│   ├── setup/               <- init_user_dir.py (premier install)
│   └── temp/                <- Migrations one-shot
├── docs/
│   ├── architecture/        <- ARCHITECTURE.md, DATABASES.md, CONTRACTS.md
│   ├── VISION.md            <- Stratégie produit
│   ├── FUTURE-WORK.md       <- Backlog d'idées
│   └── superpowers/         <- Specs, plans, audits (provisoire, archivable)
├── CLAUDE.md                <- Entry point IA — rules, status, workflow
├── PROJECT-STATUS.md        <- État courant du projet (live)
├── SESSION-CONTEXT.md       <- Contexte décisionnel (réécrit chaque session)
└── pyproject.toml
```

### Pattern architectural

**Hexagonal / Ports & Adapters**, implémenté via un pattern **VaultContext** (inspiré de
LangGraph state passing + FastAPI DI) :

```
core/           <- ports (Protocols), schemas — importe RIEN du projet
tools/          <- business logic atomique — reçoit VaultContext, importe core/ uniquement
workflows/      <- orchestration — construit le pipeline, importe tools/ + core/
infrastructure/ <- adapters concrets — implémente les Protocols de core/
api/ | cli/ | mcp/ <- surfaces — build_context(), routage pur
```

**Règles dures :**
- Un tool n'importe JAMAIS infrastructure/
- Un tool n'importe JAMAIS un autre tool
- core/ a ZERO import du projet
- Les surfaces (API, CLI, MCP) = < 15 lignes par handler

### Points forts

- **Séparation des couches stricte et appliquée** — validée par audit (374 tests, 0 violation G4)
- **Trois surfaces (API, CLI, MCP) sur le même core** — une seule business logic
- **Config-driven** : toute valeur tunable dans YAML, taxonomie extensible sans code
- **VaultContext = DI sans framework** — simple dataclass, testable avec mocks
- **Tests miroir la structure** — chaque tool a son test file

### Points faibles

- **Pas de CI/CD** — aucun pipeline GitHub Actions
- **Pas de linter/formatter configuré** — aucun ruff, black, pyright dans pyproject.toml
- **Pas de pre-commit hooks** — fichier `.pre-commit-config.yaml` absent
- **Pas de type checking** — pyright/mypy non configurés
- **egg-info commité** — artefact de build dans le repo
- **mcp/ shadows le package pip `mcp`** — workaround complexe dans server.py (lignes 38-49)

---

## Section 2 — Stack et tooling

### Dépendances principales

| Package | Version | Rôle |
|---------|---------|------|
| pydantic | >=2.0 | Validation schémas, config, contrats |
| PyYAML | >=6.0 | Lecture config YAML |
| sqlite-vec | >=0.1.0 | Embeddings vectoriels en SQLite |
| requests | >=2.33 | HTTP client |
| faster-whisper | >=1.2.0 | Transcription audio locale |
| yt-dlp | >=2026.3.0 | Téléchargement YouTube |
| youtube-transcript-api | >=1.2 | Sous-titres YouTube |
| mcp[cli] | >=1.0 | Model Context Protocol server |
| anthropic | >=0.40 | Claude API pour génération LLM |
| pypdf | >=4.0 | Extraction texte PDF |
| fastapi | >=0.110 | API HTTP |
| uvicorn[standard] | >=0.29 | Serveur ASGI |
| typer | >=0.12 | CLI framework |
| rich | >=13 | Formatage terminal |

**Dev :** pytest >=9.0, httpx >=0.27

### Outils de développement

- **Test runner :** pytest (configuré dans pyproject.toml)
- **Linter / formatter :** **AUCUN configuré**
- **Type checker :** **AUCUN**
- **CI/CD :** **AUCUN**

### Gestion des dépendances

- **uv** (présence de `uv.lock`) — mais setuptools comme build-backend dans pyproject.toml

---

## Section 3 — Conventions et garde-fous

### Format de commits

Conventional commits : `feat:` / `fix:` / `docs:` / `chore:` + description **en anglais**.

### Pre-commit hooks

**Aucun.** Les garde-fous sont portés par :
- Les 13 règles G1-G13 dans CLAUDE.md §6
- Un checklist pré-commit manuelle dans CLAUDE.md
- Un process d'audit formel

### Stratégie de tests

- **Organisation :** miroir exact de la structure source
- **374 tests passing**
- **Fixtures centralisées** dans `tests/conftest.py`
- **Stubs pour dépendances optionnelles** — `sys.modules` injection
- **Pas de coverage configurée**

### Gestion des secrets

- `config/install.yaml` gitignored — contient API keys et chemins machine
- `config/user.yaml` gitignored — préférences utilisateur
- `.example` versionnés comme templates
- `core/sanitize.py` — redaction dans les logs
- `core/security.py` — validation URLs, paths, permissions fichiers

---

## Section 4 — Pratiques IA / Vibe coding

### CLAUDE.md

Fichier de **~350 lignes**, extrêmement détaillé. **C'est le meilleur asset du projet pour metadev.**

### Instructions spécifiques à l'IA — Règles G1-G13

Les règles sont spécifiquement conçues pour **éviter les erreurs courantes des LLM** :
- **G1** — Ne pas exposer les noms de librairies dans les strings publiques
- **G2** — Décrire WHAT pas HOW dans les docstrings
- **G5** — Pas d'over-engineering (le piège #1 des LLM)
- **G6** — Chaque except doit logger ou re-raise (anti-silent-failure)
- **G11** — Les couches de routing sont minces
- **G13** — Comments concis, chirurgicaux

### Cockpit de session à 2 fichiers

| Fichier | Rôle | Règle |
|---------|------|-------|
| `PROJECT-STATUS.md` | État courant : next action, features done, debt | Mis à jour fin de session |
| `SESSION-CONTEXT.md` | Contexte décisionnel : POURQUOI les décisions | **Réécrit** (pas complété) chaque session |

**Règle critique :** SESSION-CONTEXT.md est réécrit pour rester concis.

### Séparation brouillons / code validé

```
docs/superpowers/
├── specs/              <- Specs actives
│   └── future/         <- Specs validées mais pas encore implémentées
├── plans/              <- Plans d'exécution actifs
├── audits/             <- Résultats d'audit (datés)
└── archive/            <- Specs et plans implémentés ou obsolètes
```

### Workflow obligatoire en 7 phases

BRAINSTORM -> SPEC -> PLAN -> IMPLEMENT -> TEST -> AUDIT -> SHIP

---

## Section 5 — Patterns remarquables

### 1. VaultContext — DI sans framework
- **Où :** `core/context.py`, `infrastructure/context.py`
- **Transférable ?** `TEMPLATE`

### 2. Cockpit de session à 2 fichiers (PROJECT-STATUS + SESSION-CONTEXT)
- **Où :** `PROJECT-STATUS.md`, `SESSION-CONTEXT.md`
- **Transférable ?** `TEMPLATE` — le pattern "rewrite, don't append" est la clé

### 3. Règles G1-G13 anti-LLM-mistakes
- **Où :** `CLAUDE.md` §6
- **Transférable ?** `TEMPLATE` — G1, G2, G5, G6, G13 universelles. G4, G7, G9, G11 profilables

### 4. Config à 3 niveaux (system / user / install)
- **Où :** `config/`
- **Transférable ?** `TEMPLATE`

### 5. Taxonomie config-driven
- **Où :** `config/system.yaml`, `core/schemas.py`
- **Transférable ?** `PROFILE:app`

### 6. @loggable decorator avec callback injection
- **Où :** `core/logging.py`
- **Transférable ?** `INSPIRATION`

### 7. Hiérarchie documentaire permanente/provisoire
- **Où :** `CLAUDE.md` §3
- **Transférable ?** `TEMPLATE`

### 8. Surfaces multiples (API + CLI + MCP) sur un seul core
- **Où :** `api/`, `cli/`, `mcp/`
- **Transférable ?** `PROFILE:app`

### 9. Test fixtures VaultContext-aware
- **Où :** `tests/conftest.py`
- **Transférable ?** `TEMPLATE`

### 10. Workflow obligatoire en 7 phases
- **Transférable ?** `OVER-ENGINEERED` pour un bootstrap. Inspirant pour projets matures.

### 11. Gestion dépendances optionnelles dans les tests
- **Transférable ?** `INSPIRATION`
