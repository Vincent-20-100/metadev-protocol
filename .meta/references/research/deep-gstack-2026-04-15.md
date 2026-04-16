---
mode: deep
date: 2026-04-15
slug: gstack
url: https://github.com/garrytan/gstack
angle: 23-tool opinionated Claude Code setup, persona-as-agent framing
status: active
---

# Deep — garrytan/gstack

## 1. Fingerprint

- **Author:** Garry Tan (YC president/CEO). README frames it as his personal
  "answer to Karpathy" — how a solo builder ships 10k-20k LOC/day.
- **Stack:** Bun + TypeScript runtime, Playwright browse binary, Markdown SKILL
  files generated from `.tmpl` templates via `scripts/gen-skill-docs.ts`. MIT.
- **Scale:** ~35 skill directories at repo root (much more than the "23" claim
  — README lists 23+8 "power tools" in tables). Multi-host: Claude, Codex,
  Factory, Kiro, Opencode, Slate, Cursor, OpenClaw — 8 hosts in `hosts/*.ts`.
- **Install model:** global symlink at `~/.claude/skills/gstack`, one-liner
  curl-equivalent in README. "Team mode" via `bin/gstack-team-init` vendors
  a thin pointer into a repo so CI/teammates auto-get the latest.
- **Distribution philosophy:** "paste this block into Claude Code, it does the
  rest" — the install instruction IS a prompt for the LLM, not a bash command.

## 2. Structure map

```
gstack/
├── README.md (32KB)               # Opinion manifesto + 23-tool table
├── CLAUDE.md (27KB)               # Dev contract with token ceiling, workflow
├── AGENTS.md (2.6KB)              # Same-table for non-Claude agents
├── ETHOS.md                       # "Boil the Lake", "Search Before Building"
├── ARCHITECTURE.md (22KB)
├── SKILL.md + SKILL.md.tmpl       # Top-level (describes /browse)
├── setup (34KB bash)              # Multi-host installer, team mode, prefix choice
├── hosts/{claude,codex,cursor,factory,kiro,opencode,slate,openclaw}.ts
│                                  # Typed host adapters — add a host = 1 TS file
├── scripts/
│   ├── gen-skill-docs.ts          # .tmpl → SKILL.md per host
│   ├── host-config.ts             # HostConfig interface
│   ├── resolvers/                 # {{PREAMBLE}}, {{BASE_BRANCH_DETECT}}, etc.
│   └── host-adapters/             # OpenClaw tool mapping
├── test/                          # 40+ test files
│   ├── skill-validation.test.ts   # Tier 1 free <1s
│   ├── skill-llm-eval.test.ts     # Tier 3 LLM-as-judge ~$0.15
│   ├── skill-e2e-*.test.ts        # Tier 2 E2E via `claude -p` ~$3.85
│   ├── helpers/{llm-judge, session-runner, eval-store, touchfiles}.ts
│   └── fixtures/ (planted bugs, ground-truth JSON)
├── <skill>/SKILL.md(+.tmpl)       # 35 skill dirs: office-hours, cso, review,
│                                  #   ship, qa, autoplan, plan-*, design-*,
│                                  #   investigate, retro, careful, freeze,
│                                  #   guard, learn, checkpoint, canary, …
├── bin/gstack-*                   # gstack-config, gstack-slug, gstack-repo-mode,
│                                  #   gstack-update-check, gstack-telemetry-log,
│                                  #   gstack-timeline-log, gstack-learnings-search
├── browse/                        # Playwright headless Chromium CLI ($B cmd)
├── design/                        # GPT Image CLI (design-shotgun generator)
├── extension/                     # Chrome side panel (sidebar agent)
├── .github/                       # evals.yml (Ubicloud), Dockerfile.ci
└── TODOS.md (46KB), CHANGELOG.md (221KB)
```

## 3. Key findings

### 3.1 Extension points

**Typed multi-host registry — `hosts/index.ts:1-67`**

```ts
export const ALL_HOST_CONFIGS: HostConfig[] = [claude, codex, factory, kiro,
  opencode, slate, cursor, openclaw];
export type Host = (typeof ALL_HOST_CONFIGS)[number]['name'];
export function getHostConfig(name: string): HostConfig { ... }
export function resolveHostArg(arg: string): string { /* alias → name */ }
export function getExternalHosts(): HostConfig[] {
  return ALL_HOST_CONFIGS.filter(c => c.name !== 'claude');
}
```

And `hosts/claude.ts:3-43`:

```ts
const claude: HostConfig = {
  name: 'claude', displayName: 'Claude Code', cliCommand: 'claude',
  globalRoot: '.claude/skills/gstack',
  frontmatter: { mode: 'denylist', stripFields: ['sensitive','voice-triggers'],
                 descriptionLimit: null },
  generation: { generateMetadata: false, skipSkills: [] },
  pathRewrites: [], toolRewrites: {}, suppressedResolvers: [],
  install: { prefixable: true, linkingStrategy: 'real-dir-symlink' },
  coAuthorTrailer: 'Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>',
  learningsMode: 'full',
};
```

**Rationale:** Adding an agent is literally one typed TS file + registry push.
`frontmatter.mode: 'denylist'`, `pathRewrites`, `toolRewrites`,
`suppressedResolvers` are the exact knobs that make a Markdown skill
portable across 8 CLI agents. This is the "single-LLM, single-IDE" problem
solved. Directly addresses PM.15's multi-IDE goal.

### 3.2 Safety & governance

**Skill preamble = observability + telemetry + session state — `cso/SKILL.md:28-99`**

```bash
_UPD=$(~/.claude/skills/gstack/bin/gstack-update-check ... || true)
mkdir -p ~/.gstack/sessions
touch ~/.gstack/sessions/"$PPID"
_SESSIONS=$(find ~/.gstack/sessions -mmin -120 -type f | wc -l)
_PROACTIVE=$(~/.claude/skills/gstack/bin/gstack-config get proactive || echo true)
_BRANCH=$(git branch --show-current)
source <(~/.claude/skills/gstack/bin/gstack-repo-mode) || true
_TEL=$(~/.claude/skills/gstack/bin/gstack-config get telemetry || true)
if [ "$_TEL" != "off" ]; then
  echo '{"skill":"cso","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",...}' \
    >> ~/.gstack/analytics/skill-usage.jsonl
fi
_LEARN_FILE="${GSTACK_HOME}/projects/${SLUG}/learnings.jsonl"
if [ "$_LEARN_COUNT" -gt 5 ]; then
  ~/.claude/skills/gstack/bin/gstack-learnings-search --limit 3
fi
~/.claude/skills/gstack/bin/gstack-timeline-log '{"skill":"cso",...}' &
```

**Rationale:** Every skill shares a ~70-line preamble injected via
`{{PREAMBLE}}` resolver. It wires: auto-update check, session counting
(for "are you running 10 sprints?" awareness), proactive-suggestion opt-out,
repo mode detection, telemetry with opt-out, per-project learnings
injection, local-only session timeline. This is the "gstack is one process"
implementation — shared state without a runtime. metadev has NOTHING like it;
our preambles are empty.

**Careful/freeze/guard as separate composable "safety skills"** (dirs exist).
README line 229-232:
> `/careful` warn before destructive, `/freeze` edit-lock to dir, `/guard`
> both at once, `/unfreeze` release.
These are first-class skills, not rules. Safety is a *toggle*, not a config.

### 3.3 Documentation quality

**README is a 32KB opinion manifesto, not a feature list.** `README.md:1-25`
opens with a Karpathy quote, then Garry's personal stats (600k LOC in 60 days),
then positions the whole product as "turns Claude Code into a virtual team."
Every skill in the table has a **persona** (CEO / Eng Manager / Staff Eng /
QA Lead / SRE / Release Engineer / Technical Writer) before describing what it
does. This is the "persona-as-agent" framing the user asked about — it lives
in README prose and in skill `description:` frontmatter, NOT in a separate
agents/personas config.

**Generated SKILL.md with token ceiling — `CLAUDE.md:140-145`**

```
**Token ceiling:** Generated SKILL.md files must stay under 100KB (~25K tokens).
`gen-skill-docs` warns if any file exceeds this. If a skill template grows past
the ceiling, consider extracting optional sections into separate resolvers that
only inject when relevant, or making verbose evaluation rubrics more concise.
```

**Rationale:** Hard budget per skill, enforced at build time, with a clear
mitigation (resolvers). Progressive disclosure encoded numerically.

### 3.4 Developer workflow

**Three-tier eval system — `CLAUDE.md:37-46`**

```
**Two-tier system:** Tests are classified as `gate` or `periodic` in E2E_TIERS.
CI runs only gate tests (EVALS_TIER=gate); periodic tests run weekly or manually.
When adding new E2E tests, classify them:
1. Safety guardrail or deterministic functional test? -> gate
2. Quality benchmark, Opus model test, or non-deterministic? -> periodic
3. Requires external service (Codex, Gemini)? -> periodic
```

Plus `test/skill-llm-eval.test.ts:30-48` — **diff-based test selection** via
touchfiles:

```ts
if (changedFiles.length > 0) {
  const selection = selectTests(changedFiles, LLM_JUDGE_TOUCHFILES, GLOBAL_TOUCHFILES);
  selectedTests = selection.selected;
  process.stderr.write(`LLM-judge selection (${selection.reason}): ` +
    `${selection.selected.length}/${Object.keys(LLM_JUDGE_TOUCHFILES).length} tests\n`);
}
```

**Rationale:** Each test declares file deps in `test/helpers/touchfiles.ts`;
CI only runs what the diff touches. Tiers: free static (<1s), LLM-judge
(~$0.15), E2E via `claude -p` (~$3.85). Cost-aware benchmarks-as-first-class.
This is *exactly* what PM.15 means by "benchmarks first-class."

**autoplan — encoded decision principles for auto-review — `autoplan/SKILL.md.tmpl:46-97`**

```
## The 6 Decision Principles
1. Choose completeness — Ship the whole thing.
2. Boil lakes — Fix everything in the blast radius (< 1 day CC effort).
3. Pragmatic — If two options fix the same thing, pick the cleaner one.
4. DRY — Duplicates existing functionality? Reject.
5. Explicit over clever — 10-line obvious > 200-line abstraction.
6. Bias toward action — Merge > review cycles > stale deliberation.

**Conflict resolution:**
- CEO phase:   P1+P2 dominate.
- Eng phase:   P5+P3 dominate.
- Design phase: P5+P1 dominate.

## Decision Classification
Mechanical → auto silently. Taste → auto w/ recommendation, surface at gate.
User Challenge → NEVER auto-decided (both models disagree with user).
```

**Rationale:** /autoplan reads /plan-ceo-review, /plan-design-review,
/plan-eng-review, /plan-devex-review from disk and runs them sequentially,
auto-answering intermediate AskUserQuestion calls via 6 principles.
User only sees a final taste-gate. This is orchestration encoded as a
decision rubric, not a DAG. Zero agentic magic — just prose rules the LLM
follows. Directly relevant to metadev's /orchestrate skill.

### 3.5 Distinctive patterns ⭐

**Install command = LLM prompt, not bash — `README.md:47-49`**

```
> Install gstack: run `git clone --single-branch --depth 1 https://github.com/
> garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack &&
> ./setup` then add a "gstack" section to CLAUDE.md that says to use the /browse
> skill from gstack for all web browsing, never use mcp__claude-in-chrome__*
> tools, and lists the available skills: /office-hours, ..., /learn. Then ask
> the user if they also want to add gstack to the current project so teammates
> get it.
```

**Rationale:** Users paste a *natural-language paragraph* into Claude Code,
which then runs the shell + edits CLAUDE.md + prompts for team bootstrap.
The installer is a multi-step agent instruction. Zero "bash one-liner"
friction. Same pattern for OpenClaw install (line 78-79). This is a new
UX primitive and it explains how Garry onboards non-engineers.

**Persona-as-prompt encoded in frontmatter `description:` — `office-hours/SKILL.md.tmpl:1-27`**

```yaml
---
name: office-hours
preamble-tier: 3
version: 2.0.0
description: |
  YC Office Hours — two modes. Startup mode: six forcing questions that expose
  demand reality, status quo, desperate specificity, narrowest wedge, observation,
  and future-fit. Builder mode: design thinking brainstorming for side projects...
  Proactively invoke this skill (do NOT answer directly) when the user describes
  a new product idea...
  Use before /plan-ceo-review or /plan-eng-review. (gstack)
allowed-tools: [Bash, Read, Grep, Glob, Write, Edit, AskUserQuestion, WebSearch]
---
```

And the body opens with `office-hours/SKILL.md.tmpl:32-38`:

```
You are a **YC office hours partner**. Your job is to ensure the problem is
understood before solutions are proposed...
**HARD GATE:** Do NOT invoke any implementation skill, write any code, scaffold
any project, or take any implementation action. Your only output is a design
document.
```

**Rationale:** There is no separate "personas.md" or "agents/" directory with
JSON personas (the `agents/` dir holds a single `openai.yaml` tool-mapping,
not personas). Personas live IN the skill prose — role declaration at top,
HARD GATE constraints, operating principles. Opinions are encoded entirely
in prompt prose. This is the simplest possible implementation and it works.

**Shared resolvers as prompt macros — `scripts/resolvers/`**

Templates reference `{{PREAMBLE}}`, `{{BASE_BRANCH_DETECT}}`,
`{{LEARNINGS_SEARCH}}`, `{{SCOPE_DRIFT}}`, `{{PLAN_COMPLETION_AUDIT_REVIEW}}`,
`{{REVIEW_ARMY}}`, `{{CROSS_REVIEW_DEDUP}}`, `{{CONFIDENCE_CALIBRATION}}`,
`{{BENEFITS_FROM}}`, `{{BROWSE_SETUP}}`, `{{SLUG_EVAL}}`. Each resolver
injects a prose block at build time — mixins for prompts. This is how
gstack keeps ~35 skills in sync without duplication, and how it enforces a
house style. metadev has nothing equivalent.

## 4. Tiered recommendations

### USE AS-IS
- **The typed host adapter pattern** (`hosts/*.ts` + `host-config.ts`). Copy
  the interface shape directly. It's the cheapest path to multi-IDE for v2.0.

### EXTRACT PARTS
- **Prompt-macro resolvers** (`{{PREAMBLE}}`, `{{BASE_BRANCH_DETECT}}`,
  `{{LEARNINGS_SEARCH}}`). Extract the pattern: `.tmpl` + generator +
  named injection points. metadev can encode shared blocks (e.g.
  `{{DEVILS_ADVOCATE_COUNTER}}`, `{{RULE_OF_3}}`) this way instead of
  repeating prose across skills.
- **Three-tier test system** (free static / LLM-judge / E2E via `claude -p`)
  with **touchfile-based diff selection**. Directly maps to PM.15
  benchmarks-first-class. The cost ceiling (~$4/run) is empirically tuned.
- **Token ceiling per skill** with build-time warning (100KB / 25K tok).
  Bake into metadev's `check_skills_contract.py`.

### BORROW CONCEPTS
- **Persona-in-description** — every skill frontmatter `description:`
  declares the role + "use when" + "proactively invoke when" + "use
  before/after which other skill". metadev's trigger table is one step
  less explicit; move that metadata INTO the skill frontmatter so it
  travels with the skill across hosts.
- **/autoplan's 6 decision principles** — encode orchestration via a
  prose rubric + Mechanical/Taste/UserChallenge classification, not a
  DAG. metadev's `/orchestrate` could adopt this shape.
- **Install = LLM prompt** for metadev's `copier copy` bootstrap — the
  one-line install could be a natural-language paragraph the user
  pastes into Claude Code.
- **Shared preamble for observability** — session counting, telemetry
  opt-out, learnings injection, update-check. metadev could gain all
  four by adding one resolver.

### INSPIRATION
- **Composable safety skills** (`/careful`, `/freeze`, `/guard`,
  `/unfreeze`). "Safety as a toggle" is a different mental model from
  rules files. metadev's rules/ dir could grow a companion "modes" dir.
- **Learnings as per-project JSONL** at `~/.gstack/projects/<slug>/
  learnings.jsonl`, auto-searched in every preamble. This is a concrete
  spec for metadev's future "memory" feature (cf. claude-mem note).
- **ETHOS.md** as a separate file from CLAUDE.md/ARCHITECTURE.md — Garry
  keeps "Boil the Lake" and "Search Before Building" as a cultural
  document, not architectural. metadev has `.meta/GUIDELINES.md` playing
  this role; consider whether it should be named ETHOS.

### REJECT
- **The 35-skill sprawl itself.** gstack has `design-consultation`,
  `design-shotgun`, `design-html`, `plan-design-review`, `design-review`,
  `devex-review`, `plan-devex-review` — seven design/DX variants. YAGNI
  alarm. Garry can absorb that because he's the sole user; metadev is a
  *template*, so every skill ships to every project. Stay lean.
- **Top-level directory per skill** (`review/`, `ship/`, `cso/`, etc.
  at repo root). Tolerable here because gstack has no app code, but it
  muddies the repo. metadev's `template/.claude/skills/` layout is cleaner.
- **Bun-only runtime.** gstack commits to Bun + TS for tooling, which
  forces non-Bun installers into weird adapter paths (`openclaw` exits
  with a "methodology artifacts" message — `setup:58-69`). metadev's
  Python+uv stack is broader.
- **Telemetry-on-by-default** with opt-out. Too heavy for a template;
  telemetry should stay off-by-default in `metadev-protocol`.

## 5. Open questions

1. **How do resolvers actually work?** `scripts/resolvers/` wasn't read here
   — next audit should dump one resolver (e.g. `preamble.ts`) to see whether
   they are static strings, Jinja-lite, or programmatic. This determines
   whether metadev can steal the pattern in a shell script or needs a mini
   DSL.
2. **How does `/learn` store and query learnings?** Preambles call
   `gstack-learnings-search --limit 3` unconditionally. Is it grep, FTS5,
   embeddings? The JSONL path suggests grep. Compare against claude-mem
   note in memory.
3. **Are the 8 hosts actually maintained?** Only `claude.ts` was read. Do
   `cursor.ts`, `slate.ts`, `kiro.ts` use the same tool names or do
   `toolRewrites` carry real substitution? The answer tells us whether
   multi-host is real or aspirational.
4. **How does `/autoplan` actually read sibling skill files?** Is it a
   `Read` tool call or a generator-time include? Latter is more reliable.
5. **Does `gstack-repo-mode` detect monorepos?** It's sourced inline into
   the preamble environment. If it distinguishes template/app/monorepo,
   that's directly reusable for metadev's `.meta/` vs `template/` split.
6. **23 vs 35 tool count discrepancy.** README says 23. Root dir has 35.
   Which ones are user-invokable slash commands vs internal helpers?
   A contract check like metadev's would immediately surface this.
