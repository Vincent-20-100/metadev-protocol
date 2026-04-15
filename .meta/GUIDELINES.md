# Guidelines — metadev-protocol

> These are recommended practices, not rules. Apply when relevant.
> Draw from these naturally and suggest them when appropriate.

## Working with AI

**Working rhythm:**

1. **Define intent** — what, why, constraints. Write it down before involving AI.
2. **Let AI draft** — research, plan, implement. Trust the process, not the output.
3. **Review critically** — AI is confident but not always right. Challenge every assumption.
4. **Commit and capture** — one logical unit, capture the decision, move on.
5. **Improve** — learn from wins and failures. Update CLAUDE.md when a pattern repeats.

**Anti-patterns to watch for:**

- **Over-engineering** — building for hypothetical futures instead of present needs
- **Knowledge amnesia** — not capturing decisions, repeating the same debates
- **Perfectionism paralysis** — polishing instead of shipping

If you find yourself correcting AI on the same thing twice, add it to CLAUDE.md.
Outdated documentation reduces AI effectiveness more than no documentation.
Update docs at the same commit that changes behaviour — never later.

**Practical defaults:**

- **Errors are knowledge** — fix root cause, not symptom
- **Third occurrence → automate** — the first time is learning, the second is a coincidence, the third is a pattern

**ADR decision template (4 questions):**

When making a technology or architecture decision, answer:
1. What problem does this solve?
2. What alternatives were considered?
3. Why this choice over the alternatives?
4. What is the exit cost if this choice is wrong?

## Code structure

- **Default to a modular monolith** — one codebase, clear module boundaries, no microservices until you've exhausted the monolith. *"AI reasons about a monolith far better than a mesh of services. You can always split later; you can't easily merge back."*
- Prefer small, focused functions over long ones
- Group related logic in modules, not mega-files
- Keep entry points thin — route to logic, don't contain it
- When a function grows beyond ~30 lines, consider splitting

## Skill vs tool — LLM-minimal principle

When designing a new skill, classify each step as **deterministic** (file I/O, subprocess, parsing, formatting) or **LLM** (reasoning, synthesis, semantic extraction).

> **Rule:** if ≥ 80% of steps are deterministic, build a Python script + thin skill wrapper — not a pure skill.

| Ratio | Format |
|-------|--------|
| 100% LLM | Pure skill (`SKILL.md` only) |
| Mix, LLM > 20% | Script in `scripts/` + thin skill wrapper |
| ≥ 80% deterministic | Script in `scripts/` + thin skill wrapper |
| 100% deterministic | Script or alias — no skill needed |

**Pattern (script + thin skill):**
- `scripts/<name>/` — all deterministic logic (fetch, parse, dedup, format, write). No LLM calls.
- `.claude/skills/<name>/SKILL.md` — ≤ 100 lines. Does exactly 3 things:
  1. One-time setup (if first run)
  2. `uv run python -m scripts.<name>`
  3. Frame the output for the user (present, summarize, propose next steps)

**Anti-pattern:** a skill that loops Bash commands and asks the LLM to parse output — burns tokens, non-reproducible, slow.

**When designing a new skill:** list its steps, classify each as deterministic vs LLM, calculate the ratio, pick the format above.

**Retroactive refactor:** apply this filter at next touch of an existing skill. Do not refactor en masse (YAGNI).

## Dependencies

**Dependencies are a liability.** Every package you add is a maintenance burden, a supply-chain risk, and a future version conflict. Ask stdlib first:

1. Can the stdlib solve this? If yes, use it.
2. Is the package well-maintained, widely trusted, and adds significant leverage? If yes, add it.
3. If in doubt, write the 20-line function yourself.

## Configuration

- Centralize config in files (yaml/toml), not scattered constants
- Separate concerns: system config vs user preferences vs secrets
- Use environment variables for deployment-specific values only

## Naming and clarity

- Names should reveal intent — avoid abbreviations
- A good name removes the need for a comment
- Consistent vocabulary: pick one term per concept, stick to it

## Error handling

- Handle errors at the right level — not too early, not too late
- Prefer explicit error types over generic exceptions
- Log context: what was attempted, what failed, what was the input

## Testing

- Test behavior, not implementation
- One assertion per test when possible
- Name tests as sentences: `test_should_reject_negative_amounts`

## Commit strategy

One commit = one complete logical unit. Not one file, not one timer tick.

- **Trunk-based development** — work directly on `main` (or short-lived branches that merge within a day). No long-lived feature branches. *"The real CI is the discipline of always keeping `main` green, not just a GitHub Actions workflow."*
- **Granularity** — a commit is a feature, a fix, or a decision. A `feat:` touching 5 files is one commit, not five
- **Review test** — a reviewer should understand the commit in under 5 minutes
- **Bisectable** — each commit must pass tests independently so `git bisect` works
- **Decomposition upfront** — the plan determines commit granularity, not git rebase after the fact
- **No timer commits** — never commit partial work to satisfy a hook or timer; stash or branch instead
- **Conventional format** — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:` describe the *type* of change, not its size
- **History as documentation** — git log is an artifact reviewers read, not a personal journal

Anti-patterns: "wip", "more changes", "fix typo" chains, commits that break tests, commits that mix unrelated changes.

## Commit authorship

The `check_git_author.py` pre-commit hook blocks commits authored as `Claude` or `Anthropic` on your machine. That's the local layer — it protects against forgetting to set your git identity before a session with an AI assistant.

Set your identity once, globally:

```bash
git config --global user.name "Vincent"
git config --global user.email "you@example.com"
```

The hook does **not** protect against commits created server-side — cloud AI sandboxes, GitHub web merges, or CI-generated commits never touch your machine and bypass it entirely.

**Two-layer protection:**

| Layer | What it catches | What it misses |
|-------|-----------------|----------------|
| Local hook (`check_git_author.py`) | Accidental AI-authored commits from your machine | Cloud sandbox branches, web commits, CI-generated commits |
| Server-side Action (`.github/workflows/check-commit-authors.yml`) | Any PR whose commit history contains a Claude/Anthropic author name | Nothing — runs on GitHub's infrastructure, always |

The server-side Action (if you generated this project with `enable_server_auth_check: true`) scans every commit in a PR targeting `main` and fails the check if it finds a blocked author name. This is the correct tool — not signed commits (which verify key identity, not author name).

If you only work locally and never merge from cloud AI sandboxes or external contributors, the hook alone is sufficient. Enable the Action as soon as you start using any tool that commits on your behalf outside your machine.

## Refactoring signals

- When you copy-paste: extract
- When a file exceeds ~200 lines: consider splitting
- When you add a parameter to avoid changing logic: reconsider the design
- Ask the user before large refactors — propose, don't impose

## Working with the user

- When the request is vague, ask a clarifying question before coding
- Propose 2-3 approaches for non-trivial decisions
- Explain trade-offs, let the user decide
- After completing work, suggest what to verify

### Approval tiers (see CLAUDE.md decision tree)

- **Trivial** (1 file, localized): state the change, ask "OK to proceed?", wait
- **Standard** (>1 file or structural): write a brief plan, ask for approval, wait
- **Complex** (new pattern / architecture): spec → plan → approval → execute

Silence is not approval. Reading your plan is not approval. Only an
affirmative answer to a direct question counts.

### Rule of 3 — anti-consensus bias

If you find yourself agreeing with the user on 3 positions in a row
without genuine friction, pause and invoke the devil's-advocate agent.
Consensus is often a smell — actively look for what's missing, wrong,
or oversimplified before continuing.

## Advanced Claude Code configuration

These are optional settings you can add to `.claude/settings.json` or
`.claude/settings.local.json` for advanced use cases.

### Force Superpowers plugin for all contributors

```json
"enabledPlugins": {
  "superpowers@claude-plugins-official": true
}
```

### Background memory consolidation (autoDream)

Automatically summarize session learnings into memory files.
Use with caution — may conflict with SESSION-CONTEXT.md.

```json
"autoDreamEnabled": true
```

### Redirect memory to .meta/

Keep all AI-generated memory alongside project context.

```json
"autoMemoryEnabled": true,
"autoMemoryDirectory": ".meta/memory"
```

### Plan mode

For maximum control, use plan mode (`Shift+Tab` or `--permission-mode plan`).
Claude proposes changes, you approve each one. Recommended for architectural work.

### Status line

Show context usage in your terminal:

```json
"statusLine": true
```

### Subagent persistent memory

In agent frontmatter (AGENTS.md), use `memory: user` to persist context
across subagent invocations.

## Expansion paths

These directories do NOT exist yet. Create them only when the first real file
needs to land there. When proposing a plan that introduces a new area of the
project, include the relevant expansion path — always faithful to this
reference architecture. The user validates the plan before execution.

| Directory | Purpose | When to create |
|-----------|---------|----------------|
| `notebooks/` | Jupyter notebooks — exploration, analysis, prototyping | First notebook |
| `app/` | Web application layer (FastAPI, Flask, Streamlit…) | First endpoint or page |
| `api/` | Standalone API layer when separate from app | First route definition |
| `models/` | Trained models, weights, serialized pipelines | First model artifact |
| `config/` | YAML/TOML config files (system, user, profiles) | When config outgrows pyproject.toml |
| `infra/` | Docker, Terraform, CI/CD, deployment configs | First Dockerfile or IaC file |
| `chore/` | Maintenance scripts — DB migrations, data backfills, one-off fixes | First maintenance script |
| `cli/` | CLI entry points and command definitions | First CLI command beyond `__main__` |
| `integrations/` | Third-party connectors — APIs, webhooks, SDKs | First external service adapter |
| `pipelines/` | Data or ML pipelines — ETL, DAGs, orchestration flows | First pipeline definition |
| `outputs/` | Final results — generated reports, exports, deliverables | First export or deliverable |
| `static/` | Static assets — images, CSS, fonts, templates | First static file served |
| `docs/` | Project documentation beyond inline docstrings | Already created by default |

All directories live at project root. Prefer these names over custom alternatives.

## Data versioning

Data directories (`data/raw/`, `data/interim/`, `data/processed/`) are
tracked by default so the project structure is visible from day one.

If datasets grow large, add them to `.gitignore`:
```
data/raw/*.csv
data/raw/*.parquet
data/processed/*.pkl
```

When excluding data from git, document the data source and access
instructions in `data/README.md` or `.meta/PILOT.md`.

## .meta/ taxonomy

This project was generated with `meta_visibility=public`.

### Directories

| Dir | Purpose |
|-----|---------|
| `active/` | Validated artifacts, not yet implemented or still referenced |
| `archive/` | Implemented or superseded artifacts — chronological memory |
| `drafts/` | Work-in-progress — **gitignored**, safe to throw away |
| `decisions/` | ADRs (`adr-NNN-slug.md`) |
| `references/raw/` | Untriaged external research |
| `references/interim/` | Partial notes and digests |
| `references/synthesis/` | Canonical, citable syntheses |
| `references/research/` | Auto-generated by `/tech-watch` — cards, synthesis, INDEX. Created at first run, not at project generation. |

### Filename convention (enforced by pre-commit)

Every file in `active/` and `archive/` must match:

    <type>-<YYYY-MM-DD>-<kebab-slug>.md

Allowed types: `spec`, `plan`, `brainstorm`, `debate`, `session`, `synthesis`.

### Slug lineage

When a plan spawns from a spec (or vice versa), both share the same slug
suffix. This makes lineage visible in `ls`:

    spec-2026-01-15-auth-redesign.md
    plan-2026-01-15-auth-redesign.md

The naming script does not enforce this — it is a convention, not a rule.

### Lifecycle

- New WIP → `drafts/<anything>.md` (not tracked)
- Validated → `git mv drafts/X active/<type>-<date>-<slug>.md`
- Implemented/superseded → `git mv active/X archive/X` (keep the filename)

### Visibility modes

| Mode | Committed |
|------|-----------|
| `public` (default) | Everything except `drafts/` |
| `private` | Nothing — entire `.meta/` gitignored |

Change later with `copier update --data meta_visibility=<mode>`.
