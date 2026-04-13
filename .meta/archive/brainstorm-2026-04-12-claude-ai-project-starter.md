---
type: brainstorm
date: 2026-04-12
slug: claude-ai-project-starter
status: active
---

# Brainstorm — Absorption ideas from `GuillaumeDesforges/claude-ai-project-starter`

**Purpose:** capture everything worth taking (philosophy, concepts, prose, features) from a comparable public repo, so we can turn it into a spec post-v1.0.0 merge. Parked during v1.0.0 finalization — **do not touch before merge**.

**Follow-up:** a post-merge task in PILOT.md turns this brainstorm into a concrete spec + plan.

---

## 1. The project

**Repo:** https://github.com/GuillaumeDesforges/claude-ai-project-starter
**License:** MIT (LICENSE.md present, to be removed by users on fork per their own Phase 1)
**State at time of review:** active, early-stage template, few files, strong prose

### 1.1 Shape

```
claude-ai-project-starter/
├── .claude/
│   └── commands/         # 7 slash commands (one per SDLC phase)
├── bootstrap/            # 5-file manual playbook
├── docs/                 # log/ + wiki/ (referenced, populated by user)
├── CLAUDE.md             # minimal schema pointing to bootstrap
├── LICENSE.md
└── README.md
```

Six root items. No copier, no pre-commit, no skills, no taxonomy enforcement. Everything is prose the user reads and executes manually after forking.

### 1.2 Positioning vs metadev-protocol

| Axis | claude-ai-project-starter | metadev-protocol |
|---|---|---|
| **Mechanism** | Fork + follow manual playbook | `copier copy` + pre-wired enforcement |
| **Onboarding** | Human reads `01-*.md` → `05-*.md`, answers questions | `copier.yml` prompts, CLAUDE.md fires automatisms |
| **SDLC scope** | **Full lifecycle** (strategy → growth → support) | **Development discipline** (brainstorm → ship) |
| **Enforcement** | Rules in prose; user self-discipline | Hooks, regex validators, settings.json permissions |
| **Structure** | `docs/log/` + `docs/wiki/` + `.claude/commands/` | `src/` + `tests/` + `.meta/{active,archive,drafts,decisions,references}` + `.claude/skills/` |
| **Language lock-in** | None (language-agnostic prose) | Python 3.13 + uv + ruff |
| **Stakeholders** | Solo builders thinking full product lifecycle | Solo builders who already know their stack, want zero-setup discipline |
| **Commercial axis** | Shape Up, PostHog, MCP, PostgreSQL opinions baked in | Template deliberately minimal on product-stack opinions |
| **Feature set** | 7 SDLC commands + 5-phase playbook | 8 dev skills + workflow gates + meta taxonomy + agent personas |
| **Maintenance model** | User edits markdown directly | Versioned semver + `copier update` diffs |

**Core insight:** the two projects are **complementary, not competing**. Theirs is a *methodology guide* for the full builder journey. Ours is a *structural enforcement system* for the coding discipline. The union would be powerful — the question is where the boundary sits.

### 1.3 What they do better than us

1. **Prose quality.** Every paragraph in `bootstrap/04-engineering-setup.md` is quotable. Our GUIDELINES.md is factual but flat.
2. **Explicit opinions with justification.** They name *trunk-based development*, *linear history*, *modular monolith*, *single language*, *dependencies-as-liability* and explain *why*. We ship these behaviors implicitly.
3. **Full-SDLC slash commands.** /strategize, /research, /shape, /operate, /grow, /support — we have zero coverage of these workflows.
4. **Business vision scaffolding.** Their Phase 3 (`03-business-vision.md`) is a mini product-brief template: problem statement, target user, principles ranking, V1 scope, north star. We have nothing equivalent.
5. **4-layer knowledge architecture vocabulary.** Git / Log / Wiki / Schema — clean mental model, easy to teach.
6. **Memorable one-liners** — see §3 below.

### 1.4 What we do better than them

1. **Enforcement.** Copier, pre-commit hooks, filename regex, permissions model, attribution suppression — none of which they have.
2. **Versioned updates.** `copier update` propagates template improvements; they rely on fork-diffing which ages poorly.
3. **Workflow gates.** Explicit approval tiers (trivial/standard/complex), mandatory plan-before-code, decision tree.
4. **Meta/ taxonomy.** State-outer flat layout with enforced filenames, lifecycle transitions via `git mv`.
5. **Debate skill.** Hybrid-context adversarial debate with steelman + cross-critique — nothing comparable in their repo.
6. **Agent personas.** AGENTS.md with 4 specialists (code-reviewer, test-engineer, security-auditor, data-analyst).
7. **Commit strategy enforcement.** Rule + GUIDELINES section + `check_git_author` hook rejecting Claude as author.

---

## 2. The author

**Name:** Guillaume Desforges
**Location:** Paris, France
**Headline (LinkedIn):** *"Mathematics & Data & AI & Fullstack (basically, a wizard)"*
**Current:** Software engineer at **TamTam** (Oct 2024 →), SalesTech full-stack + product analytics
**Previous:** Senior consultant at **Tweag** (data engineering, distributed computing, ML infra)
**Education:** École des Ponts ParisTech + M2 at École Polytechnique (Data & AI)
**Languages:** FR native, EN pro, ES, IT, JP basic
**Network:** 2k+ followers, 500+ connections on LinkedIn

### 2.1 Signal from pinned repos

- **NixOS/nixpkgs** (24.3k ⭐) — contributor — *signals deep interest in reproducible, declarative systems*
- **fix-python** (163 ⭐) — solo CLI, Python venvs on NixOS — *signals Python + reproducibility pain-point authority*
- **tweag/pyfunflow** (7 ⭐) — type-safe declarative workflows in Python — *signals FP bias + domain-specific language design*
- **ELF-file-manual** gist — *signals systems-level curiosity*

**Technical identity:** functional-programming / static-typing / reproducibility / DDD-oriented engineer with data + ML background, currently shipping SalesTech product code.

### 2.2 Recent public posture

Described his own project as *"distilling experience, knowledge and opinions on AI-driven product development into a reusable bootstrap template."*

Keyword inventory: **experience**, **knowledge**, **opinions**, **AI-driven**, **bootstrap**. He's positioning the template as a crystallization of personal taste, not a framework. Same thesis as metadev-protocol — but he went opinion-first, we went enforcement-first.

### 2.3 Why his template matters for metadev-protocol

- **Peer validation.** Senior-profile engineer, strong FP + reproducibility sensibility, independently arrived at *"AI-driven template as crystallized opinion"* — validates the metadev thesis.
- **Complementary shape.** His prose quality compensates for our enforcement-first austerity; our enforcement compensates for his self-discipline dependency.
- **Network asset.** Paris-based, bilingual FR/EN, Tweag alumnus → overlap with the European Nix / FP / data engineering community. Potential outreach target for launch Phase 4.
- **Contrast material.** The side-by-side comparison (see §1.2) is a ready-made README section for our own positioning.

### 2.4 Risk / dissonance

- **Nix bias.** He ships Nix-adjacent defaults and FP thinking. We ship Python + uv. Don't absorb defaults that smuggle in Nix assumptions.
- **Full SDLC sprawl.** His 7 commands cover strategy → support. Absorbing all of them would dilute our "few skills, deep discipline" philosophy.
- **No enforcement in his template.** If we absorb his prose without keeping our mechanism, we become him — lose the differentiator.

---

## 3. Triage — what's worth taking

### Block A — Philosophy & prose (HIGH value, LOW cost)

- **A1** — *"AI as a core team member, not just a helper"* → README hero or PHILOSOPHY.md
- **A2** — Three pillars:
  - *Product excellence:* "Ship less, ship better. Every feature earns its place."
  - *Technical agility:* "Small, reversible decisions over big upfront designs. Optimize for changeability, because the first architecture will be wrong."
  - *AI intensity:* "The human role shifts from doing to directing, reviewing, and deciding."
- **A3** — Working rhythm:
  1. Define intent clearly (what, why, constraints)
  2. Let AI draft / research / implement
  3. Review critically (AI is confident but not always right)
  4. Commit, capture knowledge, move on
  5. Improve: learn from both wins and failures
- **A4** — Anti-patterns trio: over-engineering, knowledge amnesia, perfectionism paralysis
- **A5** — 4-layer knowledge architecture vocabulary (Git / Log / Wiki / Schema)
- **A6** — **"If you find yourself correcting AI on the same thing twice, add it to CLAUDE.md"** — HIGHEST behavioral value
- **A7** — *"Outdated documentation reduces AI effectiveness more than no documentation"*
- **A8** — Knowledge lifecycle: Experience → Capture → Structure → Retrieve → Apply → Improve
- **A9** — *"Capture timing is critical — documentation happens at decision moments, not retrospectively"*

### Block B — Engineering defaults (HIGH value, variable cost)

- **B1** — Name "trunk-based + local CI" explicitly in GUIDELINES. *"The real CI is the discipline of always keeping `main` green, not just a GitHub Actions workflow."*
- **B2** — Modular monolith as default. *"AI reasons about a monolith far better than a mesh of services. You can always split later; you can't easily merge back."*
- **B3** — Single language across stack (rationale: shared tooling, fewer context switches, easier AI reasoning)
- **B4** — Dependencies are a liability → ask stdlib first
- **B5** — Errors are knowledge → fix root cause, not symptom
- **B6** — Automate what repeats → third occurrence triggers automation
- **B7** — IaC from day 1 (already covered by our `infra/` expansion path)
- **B8** — **4-question tech stack decision framework** (what problem / alternatives / why / exit cost) → perfect ADR template
- **B9** — Local-first environment (offline + git worktrees) — validates our implicit worktree support

### Block C — Structural features (VARIABLE value, MEDIUM-HIGH cost)

- **C1** — **Business vision scaffolding** (problem statement / target user / product principles ranking / V1 scope / north star metric / competitive landscape / success metrics). Ship as `/vision` skill OR as a section of `template/.meta/PILOT.md.jinja` filled during first session. **Potential flagship differentiator** for solo builders.
- **C2** — Wiki tier (`.meta/wiki/` or `docs/wiki/`). Living, AI-maintained, human-reviewed. Wiki Operations: Ingest / Query / Lint.
- **C3** — 7 SDLC slash commands. Don't port all. Candidate: **`/research`** (user discovery + competitive + sector research) fills a real gap vs our `/brainstorm` (which is internal ideation).
- **C4** — Bootstrap playbook (5-phase guided flow) — reject as manual playbook, absorb into `/vision` skill if we go that route.
- **C5** — Work-stream tags in archive frontmatter (`tags: [vision, ux]`) — adds cross-cutting indexability to our type-prefixed taxonomy.

### Block D — Explicit rejections

- **D1** — Manual bootstrap playbook as-is — redundant with copier
- **D2** — *"No em dashes"* rule — stylistic, we love em dashes
- **D3** — Commit type `bootstrap:` — non-standard, we use `chore:`
- **D4** — Shape Up as default methodology — too opinionated for a template
- **D5** — PostHog / session replay as template defaults — product-specific
- **D6** — MCP server integration as template concern — out of scope
- **D7** — Nix / Nix-adjacent defaults — author's bias, not portable to our Python-first stance

---

## 4. Tentative shortlists (for spec phase — NOT binding)

### 4.1 Zero-risk doc-only batch (candidate for one commit)

A2, A3, A4, A6, A7, B1, B2, B4, B5, B6, B8

One commit: `docs(philosophy): absorb framing and engineering-defaults prose from claude-ai-project-starter`. Target files: `docs/PHILOSOPHY.md`, `template/.meta/GUIDELINES.md.jinja`, `template/CLAUDE.md.jinja`, `template/.meta/decisions/adr-template.md` (new).

### 4.2 Needs dedicated brainstorm / spec

- **C1 (vision scaffolding)** — skill vs PILOT section vs hybrid — real design question, impacts first-session UX
- **C3 (/research skill)** — scope vs /brainstorm overlap — needs skill-design thinking
- **C2 (wiki tier)** — risks duplicating decisions/ + archive/; needs a clear boundary definition before committing

### 4.3 Backlog only (post-v1.1.0)

A1, A5, A8, A9, B3, B7, B9, C4, C5

### 4.4 Rejected

D1-D7

---

## 5. Post-merge task ownership

After `v1.0.0` ships, the owner (Vincent) will:

1. Re-read this brainstorm
2. Decide which of the three candidates in §4.2 deserve a dedicated spec
3. Write `spec-YYYY-MM-DD-<slug>.md` for each accepted candidate
4. Batch the §4.1 doc-only items into a single commit (could also ship as part of v1.0.1 polish)
5. Update `.meta/references/synthesis/` with a short synthesis entry on "what we absorbed from claude-ai-project-starter and what we rejected" — for future external context

---

## 6. Potential outreach note (Phase 4 launch)

Guillaume Desforges is a **high-fit launch contact**:
- Independently arrived at the same thesis as metadev-protocol
- Tweag alumnus → FP / reproducibility community reach
- Paris-based → potential in-person or local-community signal boost
- Active builder shipping in public
- His template is complementary, not competitive — a mutual signal-boost is plausible

Add to launch plan beta contact list. Hook: *"I built a template with converging philosophy but orthogonal mechanism — would love your take on the boundary."*

---

## 7. References

- Repo: https://github.com/GuillaumeDesforges/claude-ai-project-starter
- Author GitHub: https://github.com/GuillaumeDesforges
- LinkedIn: https://fr.linkedin.com/in/guillaume-desforges
- Key files reviewed: `README.md`, `CLAUDE.md`, `bootstrap/README.md`, `bootstrap/01` → `bootstrap/05`, `.claude/commands/` listing
