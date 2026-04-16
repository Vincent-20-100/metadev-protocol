---
mode: deep
date: 2026-04-15
slug: bmad-method
url: https://github.com/bmad-code-org/BMAD-METHOD
angle: complete AI-driven dev methodology — agents, rituals, quality gates
status: active
---

# Deep — bmad-code-org/BMAD-METHOD

## 1. Fingerprint

- **44k★**, npm-based installer (`npx bmad-method install`), Node 20+ / Python 3.10+ / uv
- Distributes a "module ecosystem": BMM (core), BMB (builder), TEA (test architect), BMGD (game dev), CIS (creative intelligence)
- V6 is current; active churn (`@next` prerelease channel advertised in README)
- Supports **20+ IDEs/CLIs** as first-class install targets (Claude Code, Cursor, Cline, Windsurf, Gemini CLI, Codex, Kiro, Junie, Rovo Dev, Antigravity, etc.) — see `tools/platform-codes.yaml`
- Not a template-copier like metadev — it's an **installer that injects skills into an existing project** under `_bmad/bmm/`
- Config-driven via `{project-root}/_bmad/bmm/config.yaml` (user_name, communication_language, document_output_language, user_skill_level, planning_artifacts, implementation_artifacts, project_knowledge)
- All workflows use a home-grown XML-flavored DSL (`<workflow>`, `<step n=...>`, `<check if=...>`, `<action>`, `<goto>`, `<critical>`)

## 2. Structure map

```
BMAD-METHOD/
├── src/
│   ├── bmm-skills/                     # THE METHOD — numbered phases
│   │   ├── 1-analysis/                 # analyst, tech-writer, product-brief, prfaq, research
│   │   ├── 2-plan-workflows/           # pm, ux-designer, create-prd, validate-prd, edit-prd
│   │   ├── 3-solutioning/              # architect, create-architecture, create-epics-and-stories
│   │   ├── 4-implementation/           # dev, sm, qa, create-story, dev-story, code-review,
│   │   │                               # retrospective, sprint-planning, sprint-status, quick-dev
│   │   └── module.yaml                 # module config (project_name, paths, skill_level)
│   └── core-skills/                    # cross-cutting: brainstorming, distillator, help,
│                                       # index-docs, party-mode, shard-doc, review-adversarial,
│                                       # review-edge-case-hunter, editorial-review-{prose,structure}
├── tools/
│   ├── installer/                      # Node CLI (npx bmad-method install)
│   ├── platform-codes.yaml             # 20+ IDE targets
│   ├── validate-skills.js              # deterministic SKILL-01..07, WF-01..03, PATH-*, STEP-*, SEQ-* rules
│   └── skill-validator.md              # LLM-inference validator (second pass)
└── docs/                               # manifesto + tutorials + how-to + reference
    ├── tutorials/getting-started.md
    ├── how-to/                         # install, customize, upgrade, shard-large-docs, ...
    └── explanation/                    # conceptual docs
```

Each skill is a directory: `SKILL.md` (frontmatter + thin entry), `workflow.md` (DSL body),
`steps/step-NN-*.md` (micro-files), `checklist.md`, `templates/`, `data/`.
Agent skills also ship `bmad-skill-manifest.yaml` with `type: agent`, `displayName`,
`title`, `icon`, `capabilities`, `role`, `identity`, `communicationStyle`, `principles`.

## 3. Key findings

### 3.1 Extension points

**Two-tier skill validation** — `tools/skill-validator.md:7-15`:

```
## First Pass — Deterministic Checks
Before running inference-based validation, run the deterministic validator:
    node tools/validate-skills.js --json path/to/skill-dir
This checks 14 rules deterministically: SKILL-01..07, WF-01/02, PATH-02, STEP-01/06/07, SEQ-02.
Review its JSON output. For any rule that produced zero findings in the first pass, skip it during
inference-based validation below — it has already been verified. ... Focus your inference effort on
the remaining rules that require judgment (PATH-01/03/04/05, WF-03, STEP-02..05, SEQ-01, REF-01..03).
```

*Rationale:* exact instantiation of metadev's "skill-vs-tool principle" — deterministic
first, LLM only where judgment is required. BMAD even catalogs which rule numbers belong
to which tier. metadev's `check_skills_contract.py` is the embryo of this; BMAD shows the
full vision: 14 rules scripted, ~12 rules LLM-assisted, one shared rule catalog.

**Modular installer with platform plugins** — `tools/platform-codes.yaml:13-141`:

```yaml
platforms:
  claude-code:
    name: "Claude Code"
    preferred: true
    category: cli
  cursor:
    name: "Cursor"
    preferred: true
    category: ide
  cline: { ... }
  windsurf: { ... }
  junie: { ... }
  # 20+ total: gemini, codex, qwen, kiro, rovo-dev, antigravity, roo, github-copilot, ...
```

*Rationale:* BMAD solved multi-IDE by decoupling "the method" (skills under `src/`) from
"the host adapter" (installer renders per-IDE glue: `.claude/settings.json`,
`.cursor/rules/`, `.windsurf/`, etc.). This is directly what PM.15 is exploring for
metadev v2.0. The answer is not "ship one CLAUDE.md" — it's a matrix installer with a
central platform registry.

### 3.2 Safety & governance (quality gates, validation)

**Multi-subagent adversarial review with classification cascade** —
`src/bmm-skills/4-implementation/bmad-quick-dev/step-04-review.md:24-46`:

```
### Review
Launch three subagents without conversation context. If no sub-agents are available, generate three
review prompt files in {implementation_artifacts} — one per reviewer role below — and HALT. Ask the
human to run each in a separate session (ideally a different LLM) and paste back the findings.

- Blind hunter — receives {diff_output} only. No spec, no context docs, no project access.
- Edge case hunter — receives {diff_output} and read access to the project.
- Acceptance auditor — receives {diff_output}, {spec_file}, and context docs. Checks violations.

### Classify
2. Classify each finding:
   - intent_gap — cannot be resolved from the spec because captured intent is incomplete
   - bad_spec — caused by the change, incl. direct deviations from spec
   - patch — trivially fixable without human input
   - defer — pre-existing, not caused by this story
   - reject — noise. Drop silently.
3. Process findings in cascading order. intent_gap/bad_spec trigger loopback — lower findings
   are moot since code will be re-derived. Increment {specLoopIteration}. If >5, HALT and escalate.
```

*Rationale:* this is a **rigorous** quality gate. Three reviewers with **different
context scopes** (diff-only / diff+code / diff+spec+code), explicit recommendation to use
a **different LLM**, and a 5-class triage where the two "upstream" classes force a
loopback. metadev's `devil's-advocate` agent is one-shot; BMAD runs three parallel
devils with context starvation and an iteration cap.

**Anti-lying gates in the dev agent** —
`src/bmm-skills/4-implementation/bmad-dev-story/workflow.md:288-292, 311-345`:

```
<critical>NEVER implement anything not mapped to a specific task/subtask in the story file</critical>
<critical>NEVER proceed to next task until current task/subtask is complete AND tests pass</critical>

<step n="8" goal="Validate and mark task complete ONLY when fully done">
  <critical>NEVER mark a task complete unless ALL conditions are met - NO LYING OR CHEATING</critical>
  <action>Verify ALL tests for this task/subtask ACTUALLY EXIST and PASS 100%</action>
  <action>Confirm implementation matches EXACTLY what the task/subtask specifies - no extra features</action>
  ...
  <check if="ANY validation fails">
    <action>DO NOT mark task complete - fix issues first</action>
    <action>HALT if unable to fix validation failures</action>
  </check>
```

And the dev persona itself (`bmad-agent-dev/SKILL.md:32-34`):

```
- Execute continuously without pausing until all tasks/subtasks are complete
- NEVER lie about tests being written or passing — tests must actually exist and pass 100%
- Run full test suite after each task — NEVER proceed with failing tests
```

*Rationale:* BMAD encodes the well-known LLM failure mode ("hallucinated green tests")
as a first-class governance rule, not a hope. metadev has nothing equivalent — this is
an easy steal for the `/test` skill and for the plan-execution workflow.

### 3.3 Documentation quality (the manifesto / method docs)

**Docs structure follows Diátaxis** — `docs/`:

```
docs/
├── tutorials/getting-started.md        # learning-oriented
├── how-to/{install,upgrade,customize,established-projects,...}.md
├── explanation/                        # understanding-oriented
├── reference/                          # information-oriented
├── roadmap.mdx
└── _STYLE_GUIDE.md
```

*Rationale:* clean Diátaxis split with an explicit style guide. metadev's `.meta/` is
cockpit-only; there's no user-facing documentation surface yet. When metadev starts
shipping externally (v2.0), this is the structure to copy.

**Scale-adaptive planning** — advertised in README:10 ("true scale-adaptive intelligence
that adjusts from bug fixes to enterprise systems") and realized via the dual track:
`bmad-dev-story` (full epic → story → context → dev flow with sprint-status.yaml) vs
`bmad-quick-dev` (5-step clarify → plan → implement → review → present, single spec
file). Both live side-by-side in `4-implementation/` as peer skills — it's not a
config flag, it's **two different entry points** that converge on the same review gate.

### 3.4 Developer workflow (rituals, sprint flow, story flow)

**Sprint status as a machine-readable ritual state** —
`src/bmm-skills/4-implementation/bmad-dev-story/workflow.md:228-260`:

```
<step n="4" goal="Mark story in-progress" tag="sprint-status">
  <check if="{{sprint_status}} file exists">
    <action>Load the FULL file: {{sprint_status}}</action>
    <action>Read all development_status entries to find {{story_key}}</action>
    <action>Get current status value for development_status[{{story_key}}]</action>
    <check if="current status == 'ready-for-dev' OR review_continuation == true">
      <action>Update the story in the sprint status report to = "in-progress"</action>
      <action>Update last_updated field to current date</action>
```

Story states: `draft` → `ready-for-dev` → `in-progress` → `review` → `done`. State
transitions are the **only** side-effect allowed outside the "Dev Agent Record" section
of the story file. `{story_key}` discipline: `number-number-name` (e.g. `1-2-user-auth`),
with explicit numeric-prefix matching to avoid `1-1` vs `1-10` collisions
(`step-01-clarify-and-route.md:44`).

*Rationale:* metadev tracks work via free-form `.meta/active/` markdown files. BMAD has
a **single yaml register** of story state that every workflow reads and mutates. That's
a much stronger coordination primitive across multi-agent runs.

### 3.5 Distinctive patterns ⭐

**XML-flavored workflow DSL** —
`src/bmm-skills/4-implementation/bmad-dev-story/workflow.md:41-172`:

```xml
<workflow>
  <critical>Execute ALL steps in exact order; do NOT skip steps</critical>

  <step n="1" goal="Find next ready story and load it" tag="sprint-status">
    <check if="{{story_path}} is provided">
      <action>Use {{story_path}} directly</action>
      <goto anchor="task_check" />
    </check>
    <check if="{{sprint_status}} file exists">
      <action>Load the FULL file: {{sprint_status}}</action>
      <action>Find the FIRST story where Status == "ready-for-dev"</action>
      ...
    </check>
    <action if="story file inaccessible">HALT: "Cannot develop story without access to story file"</action>
    <action if="incomplete task or subtask requirements ambiguous">ASK user to clarify or HALT</action>
  </step>
```

*Rationale:* this is the **biggest structural innovation** BMAD ships. Instead of
expressing a workflow as natural-language instructions (what metadev does today), they
express it as a **pseudo-executable DSL** with `<step>`, `<check if>`, `<action>`,
`<goto anchor>`, `<action if="...">HALT/ASK</action>`. The LLM parses and executes it
like a structured plan. This compresses ambiguity dramatically, makes loops/jumps
explicit, and is auto-validatable (`validate-skills.js` enforces WF-01..03, STEP-01..07,
SEQ-01..02). metadev's plan skill outputs prose; this would be a huge leap.

**Named personas with voice** — `src/bmm-skills/.../bmad-agent-*/SKILL.md`:

```
# John (PM)    — "Asks WHY? relentlessly like a detective on a case."
# Amelia (Dev) — "Ultra-succinct. Speaks in file paths and AC IDs — every statement citable."
# Mary (Analyst) — "Speaks with the excitement of a treasure hunter - thrilled by every clue."
```

Each agent: `displayName`, `title`, `icon`, `capabilities` table keyed by 2-letter codes
(CP, VP, EP, CE, ...) that the user types to trigger sub-skills (`bmad-agent-pm/SKILL.md:31-41`).
Activation block tells the LLM to stay in character across nested skill calls
(`bmad-agent-dev/SKILL.md:36-38`: "When you are in this persona and the user calls a
skill, this persona must carry through and remain active").

*Rationale:* BMAD's agents are **personas with menus**, not workflow handlers. The
2-letter menu (`CP`, `VP`, `SP`, ...) is essentially a REPL for each role. metadev's
agents are dispatched-by-trigger; BMAD's are addressed-by-name. Both approaches have
merit but BMAD's is more legible to a non-expert user.

**Party mode** — `src/core-skills/bmad-party-mode/` — multi-persona roundtable where
several agents collaborate in one session. Advertised in README:22. Closest thing to a
built-in debate/brainstorm primitive with personality diversity.

**quick-dev as a full parallel method, not a "lite" flag** — entire
`bmad-quick-dev/` directory with `step-01..05` + `step-oneshot.md`. It has its own
spec template, its own state machine, its own review gate — not a `--quick` parameter
on the main flow. Scale adaptation through **path selection**, not configuration.

## 4. Tiered recommendations for metadev-protocol

### USE AS-IS
- **Nothing.** BMAD is MIT-licensed but it's a Node/npm installer ecosystem, not a
  copier template. Wholesale adoption would mean abandoning metadev's architecture.

### EXTRACT PARTS
- **`tools/platform-codes.yaml` pattern** — lift the exact yaml shape (code, name,
  preferred, category, description) and seed metadev's v2.0 multi-IDE matrix with it.
  This is the canonical list of AI-coding IDEs circa early 2026.
- **`validate-skills.js` + `skill-validator.md` two-tier pattern** — extend
  `scripts/check_skills_contract.py` with a published rule catalog (SKILL-01..N) so the
  LLM inference pass has something to defer to. The "skip rules that passed
  deterministically" clause is the key insight.
- **State vocabulary for work items** — `draft / ready-for-dev / in-progress / review /
  done` + a `sprint-status.yaml` register. metadev's `.meta/{drafts,active,archive}/`
  only has 3 states and nothing machine-readable.

### BORROW CONCEPTS
- **XML workflow DSL** — biggest lever. Migrate `/plan` and `/orchestrate` outputs to a
  `<workflow><step><check if><action><goto>` shape. Immediate wins: explicit loopbacks,
  enforceable step ordering, scriptable validation, clearer HALT semantics. The LLM
  executes it faithfully because it reads like pseudo-code.
- **Named-persona agents with menu codes** — reframe devil's-advocate, architect-review,
  etc. as named characters with 2-letter command menus. Gives the "specialized agents"
  pitch a user-legible surface. Combine with a Party Mode primitive for multi-agent
  debates.
- **Multi-subagent adversarial review with context starvation** — the 3-reviewer
  cascade (blind hunter / edge-case hunter / acceptance auditor) with **intentionally
  different context scopes** and **different-LLM recommendation**. This is how multi-LLM
  should land in metadev: not "pick your provider" but "reviewer roles get different
  providers on purpose."
- **Anti-lying gate language** in `/test` — import the exact "NO LYING OR CHEATING —
  tests must ACTUALLY EXIST and PASS 100%" phrasing into metadev's `/test` skill.
  Shame-based prompting on LLM self-reporting actually works.
- **Scale-adaptive via parallel paths** — ship `/quick-dev` as a peer skill to
  `/spec+/plan+/implement`, not a flag. Two entry points converging on the same review
  gate.

### INSPIRATION
- **Installer-based distribution** for an eventual metadev v3 where copier-generation
  is replaced/augmented by an injector that works with existing projects (connects
  directly to Vincent's "adoption mode" memory note).
- **Module ecosystem** (BMM / BMB / TEA / BMGD / CIS) — long-term, metadev could split
  into core + domain modules (data-eng, game-dev, research) the same way.
- **Diátaxis docs structure** for when metadev starts having external users.

### REJECT
- **XML DSL as a hard requirement** — if adopted it must degrade gracefully to
  markdown prose; forcing every skill into DSL is YAGNI for metadev's current scale.
- **12+ named personas** — BMAD's roster (John, Mary, Amelia, plus ux/qa/sm/tech-writer)
  is heavy. metadev should pick 2-3 personas max and resist the RPG-ification.
- **Node/npm toolchain** — metadev is uv-pure. Don't bring Node in.
- **`_bmad/bmm/config.yaml` as a runtime source of truth** — BMAD reloads it in every
  single workflow init (`On Activation` steps). This is chatty and fragile; metadev's
  copier-rendered values are fine.

## 5. Open questions

1. Can the XML workflow DSL be introduced incrementally — e.g. only for `/plan` output
   initially — without a big-bang migration of all existing skills?
2. What's the right LLM to route each reviewer role to? Does metadev need a provider
   adapter layer before it can dogfood the "different-LLM per reviewer" pattern, or can
   it ship a "paste these 3 prompts into 3 separate sessions" fallback like BMAD does?
3. Is a sprint-status.yaml worth the coordination overhead for solo-dev workflows? BMAD
   makes it optional ("no-sprint-tracking" branch in `bmad-dev-story/workflow.md:257`).
4. How do BMAD's 14 deterministic rules (SKILL-01..07, WF-01/02, PATH-02, STEP-01/06/07,
   SEQ-02) map onto metadev's existing `check_skills_contract.py` rules? Worth a direct
   diff against BMAD's published catalog before v2.0.
5. Does the "numbered phases" directory layout (`1-analysis/`, `2-plan-workflows/`, ...)
   scale when phases become non-linear (parallel branches, sub-workflows)? BMAD's
   `core-skills/` already exists as an escape hatch for cross-cutting concerns.
