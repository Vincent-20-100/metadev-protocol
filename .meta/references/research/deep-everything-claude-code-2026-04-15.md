---
mode: deep
date: 2026-04-15
slug: everything-claude-code
url: https://github.com/affaan-m/everything-claude-code
angle: agent harness architecture, skills/instincts/memory/security organization, multi-IDE
status: active
---

# Deep — affaan-m/everything-claude-code

## 1. Fingerprint

- **primary_lang**: JavaScript/Node.js (hooks & installer) + Rust (`ecc2/` session daemon, 12.5k LOC `main.rs`) + Python (`instinct-cli.py`, `ecc_dashboard.py`)
- **repo_type**: Claude Code plugin / multi-IDE harness distribution
- **file_count**: ~1963 tracked files (depth-20 clone)
- **license**: present (LICENSE file)
- **pitch**: "Production-ready AI coding plugin with 30 agents, 135 skills, 60 commands, automated hook workflows" (SOUL.md). Self-describes as the "initial portability layer for ECC's shared identity, governance, and skill catalog" across Claude Code / Cursor / OpenCode / Codex / Antigravity / Gemini / CodeBuddy.
- **stars**: (not fetched; target is "massive everything-plugin")

## 2. Structure map

```
everything-claude-code/
├── agents/                  # 48 specialist agents (planner, reviewer, harness-optimizer, build-resolvers per language)
├── skills/                  # 183 skills (agent-harness-construction, eval-harness, benchmark, continuous-learning-v2, search-first, ...)
├── commands/                # 79 slash commands
├── hooks/                   # hooks.json (652 lines, ~30 hooks) + README
├── rules/                   # common/ + 12 language dirs (cpp,csharp,dart,golang,java,kotlin,perl,php,python,rust,swift,typescript,web,zh)
├── contexts/                # dev.md, research.md, review.md (mode profiles)
├── manifests/               # install-components.json / install-modules.json / install-profiles.json (core/developer/security/research)
├── schemas/                 # JSON Schema for hooks, install-state, plugin, provenance, state-store, package-manager
├── scripts/
│   ├── harness-audit.js     # 738-line scoring engine: 7 categories, pass-rated checks
│   ├── lib/install-targets/ # claude-home / cursor-project / opencode-home / codex-home / gemini-project / antigravity-project / codebuddy-project
│   ├── ci/                  # validate-{agents,commands,hooks,skills,rules,install-manifests,workflow-security,no-personal-paths,unicode-safety}
│   ├── hooks/               # 30+ hook scripts (block-no-verify, commit-quality, quality-gate, auto-tmux-dev, ...)
│   └── codex/, codemaps/, session-inspect.js, orchestrate-worktrees.js, skills-health.js
├── src/llm/                 # Python LLM CLI subpackage (providers, tools, core, prompt)
├── ecc2/                    # Rust rewrite: session daemon (daemon.rs, manager.rs, store.rs, runtime.rs), tui, worktree, observability
├── .claude/
│   ├── identity.json        # { technicalLevel, verbosity, domains } — persisted user profile
│   ├── enterprise/controls.md
│   ├── homunculus/instincts/inherited/
│   └── rules/, skills/, team/
├── mcp-configs/mcp-servers.json
├── plugins/                 # (placeholder)
├── tests/                   # Node tests (tests/run-all.js)
├── CLAUDE.md, AGENTS.md, SOUL.md, RULES.md, SECURITY.md
└── install.sh, install.ps1, agent.yaml, VERSION
```

## 3. Key findings

### 3.1 Extension points

**Install-target registry pattern** — `scripts/lib/install-targets/registry.js` + one file per target (`claude-home.js`, `cursor-project.js`, `opencode-home.js`, `codex-home.js`, `gemini-project.js`, `antigravity-project.js`, `codebuddy-project.js`). A profile (e.g. "developer", "security") resolves to a module set, and each target rewrites the content to its own layout. Directly addresses PM.15 multi-IDE concern.

`scripts/install-apply.js:1-40`:
```js
const {
  SUPPORTED_INSTALL_TARGETS,
  listLegacyCompatibilityLanguages,
} = require('./lib/install-manifests');
// Usage: install.sh [--target <claude|cursor|antigravity|...>] [--profile <name>]
//                   [--modules <id,id,...>] [--with <component>]... [--without <component>]...
```

**Layered rules (common + language extensions)** — `rules/README.md:1-30`:
```
rules/
├── common/          # coding-style, git-workflow, testing, performance,
│                   # patterns, hooks, agents, security  (always installed)
├── typescript/      # extends common with language code examples
├── python/ golang/ web/ swift/ php/ ...
```
"Language directories extend the common rules with framework-specific patterns... Each file references its common counterpart." — pattern exactly maps to a `rules-core` + `rules-python` split for metadev profiles.

**Profile manifest** — `manifests/install-profiles.json:1-50`:
```json
{ "profiles": {
    "core":      { "modules": ["rules-core","agents-core","commands-core","hooks-runtime","platform-configs","workflow-quality"] },
    "developer": { "modules": [... + "framework-language","database","orchestration"] },
    "security":  { "modules": [... + "security"] },
    "research":  { "modules": [... + "research-apis",...] }
}}
```
Clean separation between atomic components (`install-components.json`), composable modules (`install-modules.json`), and user-facing profiles.

### 3.2 Safety & governance

**Harness audit scoring rubric** (this is the headline pattern). `scripts/harness-audit.js:7-20`:
```js
const CATEGORIES = [
  'Tool Coverage',
  'Context Efficiency',
  'Quality Gates',
  'Memory Persistence',
  'Eval Coverage',
  'Security Guardrails',
  'Cost Efficiency',
];
```
Each check is a declarative record with `{id, category, points, scopes, path, description, pass: <boolean fn>, fix: <string>}`. At `harness-audit.js:411-440`:
```js
{ id: 'security-review-skill', category: 'Security Guardrails', points: 3,
  path: 'skills/security-review/SKILL.md',
  pass: fileExists(rootDir, 'skills/security-review/SKILL.md'),
  fix:  'Add skills/security-review/SKILL.md for security checklist coverage.' },
{ id: 'security-agent', ... points: 3, path: 'agents/security-reviewer.md', ... },
{ id: 'security-prompt-hook', ... points: 2, path: 'hooks/hooks.json',
  pass: hooksJson.includes('beforeSubmitPrompt') || hooksJson.includes('PreToolUse'), ... },
```
`summarizeCategoryScores()` at line 608 normalizes earned/max to a 0-10 score per category. Runs in `--scope repo` (self-audit) OR `--scope consumer` (audit a user project via `detectTargetMode`). Output is text or JSON. **This is a concrete deterministic self-benchmark framework** — exactly what metadev PM.15 wants for "benchmarks first-class."

**`block-no-verify` hook** — `hooks/hooks.json:4-23`. Pre-tool-use matcher on Bash that blocks `git commit --no-verify` / `--no-gpg-sign` flags. Implements the "never skip hooks" policy metadev already documents as a rule, but as a real enforcement.

**CI validators as first-class contract** — `scripts/ci/validate-{agents,commands,hooks,skills,rules,install-manifests,workflow-security,no-personal-paths,unicode-safety}.js`. Each artifact type has a dedicated validator that runs in CI. Directly analogous to metadev's `check_skills_contract.py` but multi-dimensional.

### 3.3 Documentation quality

- Nine top-level `.md` files (README 1498 lines, CLAUDE 72 lines, AGENTS 166 lines, SOUL 17 lines, RULES, EVALUATION, SECURITY, TROUBLESHOOTING, three `the-*-guide.md`). CLAUDE.md is lean (points to specialist guides), SOUL.md is a "core identity + principles" 17-line manifesto.
- **`contexts/` directory (dev.md, research.md, review.md)** — mode profiles that encode three operating stances as documents. Easy to reference/load on demand. Analogous concept to metadev's skills but at a coarser granularity.
- **Two-layer skill placement policy** (`CLAUDE.md:50`): "Curated in `skills/`; generated/imported under `~/.claude/skills/`. See docs/SKILL-PLACEMENT-POLICY.md". Clean separation of template vs runtime skills — matches metadev's `template/` vs user-home split.

### 3.4 Developer workflow

**Research-first enforcement as a skill + agent** — `skills/search-first/SKILL.md:1-30`:
```
Research-before-coding workflow. Search for existing tools, libraries, and
patterns before writing custom code. Invokes the researcher agent.
Trigger: starting a new feature / adding a dependency / user says "add X" and
you're about to write code.
Workflow: 1) NEED ANALYSIS  2) PARALLEL SEARCH (npm/PyPI | MCP/skills | GitHub/web)
```
Maps directly to metadev's `/research` + `/audit-repo` trigger table.

**Eval harness as a skill** — `skills/eval-harness/SKILL.md:20-55`:
```
Eval-Driven Development treats evals as the "unit tests of AI development":
- Define expected behavior BEFORE implementation
- Run evals continuously
- Track regressions with each change
- Use pass@k metrics for reliability

Eval types: Capability / Regression.
Grader types: Code-based (grep/npm test) / Model-based (Claude judges).
```
Pairs with `skills/benchmark/SKILL.md` which measures page/API/build perf with Core Web Vitals targets.

**Harness construction skill (meta-skill)** — `skills/agent-harness-construction/SKILL.md:10-74`:
```
Agent output quality is constrained by:
  1. Action space quality   2. Observation quality
  3. Recovery quality       4. Context budget quality

Every tool response should include: status | summary | next_actions | artifacts.
Every error path should include: root cause hint | safe retry | stop condition.
Context budgeting: 1) minimal invariant system prompt  2) skills loaded on demand
  3) file refs over inlined docs  4) compact at phase boundaries, not token thresholds.
```
**This is a design contract for writing skills/tools.** Metadev has the principle ("skill-vs-tool", "progressive disclosure") but not a normative checklist. ECC does.

### 3.5 Distinctive patterns ⭐

**1. Instinct-based continuous learning (`skills/continuous-learning-v2/`)**
An atomic-grained learning pipeline that observes sessions via `PreToolUse`/`PostToolUse` hooks, stores `observations.jsonl` per project (hashed git remote → stable project ID), runs a background Haiku "observer" agent, and writes instinct YAML files with confidence scores. `SKILL.md:47-71`:
```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
---
# Prefer Functional Style
## Action: Use functional patterns over classes when appropriate.
## Evidence: Observed 5 instances... User corrected class-based on 2025-01-15.
```
Flow: observations → atomic instincts (0.3-0.9 confidence) → `/evolve` clusters → promoted to skills/commands/agents. **v2.1 adds project-scoped instincts** (prevents cross-project contamination) with `/promote` when an instinct appears in ≥2 projects. Supporting files: `skills/continuous-learning-v2/{agents/observer.md, hooks/observe.sh, scripts/instinct-cli.py, scripts/detect-project.sh, scripts/test_parse_instinct.py, config.json}`. Closed-loop self-improvement with real storage, not vibes.

**2. Seven-category harness scorecard (`scripts/harness-audit.js`)**
Already quoted above. Two invocation modes: `--scope repo` (self-check the harness repo) vs `--scope consumer` (check a user project). Consumer-mode checks `.claude/settings.json`, `AGENTS.md`/`CLAUDE.md` presence, ADRs under `docs/adr/`, `.env` in `.gitignore`, project-local hook guardrails, CI workflows (`harness-audit.js:484-605`). Output JSON can be consumed by the `harness-optimizer` agent in a loop. **This is exactly the `/audit-harness` primitive metadev PM.15 needs.**

**3. Multi-target install registry (`scripts/lib/install-targets/*`)**
Seven install targets (claude-home, cursor-project, opencode-home, codex-home, gemini-project, antigravity-project, codebuddy-project) sharing a profile → module → component resolution pipeline. A single `install.sh --profile developer --target cursor` rewrites content to each IDE's native layout. For metadev, this is the architectural answer to "one template, multiple IDEs."

**4. Agent-harness-construction meta-skill**
Ships a normative checklist for writing tools/skills: action space rules (stable names, schema-first inputs, deterministic shapes), observation contract (status/summary/next_actions/artifacts), error recovery contract (root cause, safe retry, stop condition), context budgeting (minimal system prompt, lazy skills, refs over inlines, phase-boundary compaction), anti-patterns list. **The metadev `.claude/rules/` files are analogous but focus on code style; this focuses on agent-tool ergonomics.**

**5. `identity.json` persisted user profile (`.claude/identity.json`)**
```json
{ "version": "2.0", "technicalLevel": "technical",
  "preferredStyle": { "verbosity": "minimal", "codeComments": true, "explanations": true },
  "domains": ["javascript"], "suggestedBy": "ecc-tools-repo-analysis" }
```
Plus `team/everything-claude-code-team-config.json` for team-level overrides and `enterprise/controls.md` for enterprise guardrails. Three-tier scope (user / team / enterprise) for harness configuration — cleaner than metadev's current single-repo `.meta/`.

**6. Declarative hook catalog with `async` + `id` + `description`**
`hooks/hooks.json` is 652 lines, ~30 hooks, each with stable `id` (e.g. `pre:bash:block-no-verify`, `post:bash:build-complete`), `description`, `async: true` + `timeout: 30` for non-blocking post-hooks. Hooks have tiered applicability (`minimal,standard,strict`) passed to `run-with-flags.js`, so users pick their strictness level. Complex but disciplined.

## 4. Tiered recommendations for metadev-protocol

### USE AS-IS
- **`scripts/harness-audit.js` category rubric** (the 7 CATEGORIES + declarative check records). Port to Python, feed results to a metadev `harness-optimizer` agent. This is the single highest-leverage import.
- **`block-no-verify` hook script** (small, enforces an already-documented metadev rule).

### EXTRACT PARTS
- **continuous-learning-v2 instinct format** (atomic YAML with trigger/confidence/domain/evidence/scope) — extract the schema and the project-scoping logic (`git remote url → hash → project id → isolation`). Skip the observer-agent runtime for v2.0; just define the storage format and a manual `/learn` command first.
- **Install-target registry** (`scripts/lib/install-targets/*` shape) — extract the `registry.js` + one-file-per-target pattern. For metadev this reshapes copier into a `target=claude|cursor|codex` switch.
- **Profile/module/component manifest split** (`manifests/install-*.json`) — extract the three-tier resolution and port to copier questions or a `profiles.yml`.

### BORROW CONCEPTS
- **`agent-harness-construction` meta-skill** — write metadev's equivalent: a normative contract for skill/tool authors (observation contract, error recovery contract, context-budgeting rules). Currently metadev has rules in `.claude/rules/code-style.md` but no skill-design rubric.
- **Contexts directory (dev/research/review.md)** — metadev could ship three operating-mode context files loadable on demand, analogous to but coarser than skills.
- **Layered rules (common + language extensions)** — metadev already has `.claude/rules/` but flat. Add `.claude/rules/common/` + `.claude/rules/python/` structure to prepare for multi-language support.
- **`SOUL.md` as 17-line identity anchor** — metadev has `PILOT.md` + `ARCHITECTURE.md` but no "core identity + principles" ultra-short file. Could be a candidate for template output.
- **Three-tier identity (user/team/enterprise)** — aligns with metadev's "adoption mode" backlog item.

### INSPIRATION
- **Eval-harness skill (pass@k metrics, regression evals, code-grader + model-grader)** — PM.15 "benchmarks first-class" direction. Don't copy the doc; build a real eval runner script analogous to `scripts/check_skills_contract.py`.
- **Rust session daemon (`ecc2/`, 12.5k LOC)** — inspirational proof that harness state (sessions, worktrees, observability, TUI) can be externalized to a native binary. Out of scope for metadev v2.0 but interesting for a future "metadev daemon" direction.
- **Two-layer skill placement (curated template vs generated `~/.claude/skills/`)** — metadev already has this via `template/` vs user home, but document it explicitly like ECC does in `docs/SKILL-PLACEMENT-POLICY.md`.

### REJECT
- **Scale of the skill catalog (183 skills)**. ECC ships skills for every imaginable framework (django-tdd, swift-actor-persistence, kotlin-ktor-patterns, laravel-security, perl-testing, visa-doc-translate...). Violates metadev's YAGNI rule and the "skill-vs-tool: max determinism" principle. Metadev should keep its 10-skill core and resist catalog inflation.
- **Obfuscated inline `node -e '...'` hook bootstrap** (the 40-line minified resolver in every `hooks.json` entry). Clever but unmaintainable; metadev should keep hooks as separate files.
- **Per-language build-resolver agents** (`cpp-build-resolver.md`, `java-build-resolver.md`, etc. × 10+). Metadev is Python-only by stack choice; don't replicate.
- **Bespoke `ecc_dashboard.py` + Rust TUI** for harness introspection. Nice-to-have; `harness-audit --format json` is enough.
- **48 agents total**. Most ECC agents are language-specific reviewers. Metadev's current "few heavy agents" stance is better.

## 5. Open questions for follow-up

1. How stable/reliable is the `continuous-learning-v2` observer in practice? The flow is elegant but depends on a Haiku background agent — what's the false-positive rate on instinct extraction? Would a purely deterministic "corrections only" trigger be more reliable?
2. Does `harness-audit.js` scorecard actually correlate with task success rate, or is it a proxy metric? (EVALUATION.md may answer — not read.)
3. How does ECC resolve conflicts when the same skill is defined in `skills/`, `.claude/skills/`, AND `~/.claude/skills/`? Precedence order?
4. The install-targets pattern assumes a shared module format — does ECC lose fidelity when converting a Claude Code skill to a Cursor rule? What's the lowest-common-denominator content shape?
5. `ecc2/` Rust daemon — is it used in production, or an experimental rewrite? Implications for whether metadev should consider a native backend.
6. How is the "context-budget" skill enforced at runtime? Advisory doc, or wired into a hook that measures token usage?
