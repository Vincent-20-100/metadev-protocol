---
type: spec
date: 2026-04-12
slug: execution-mode
status: active
---

# Spec — Full-auto execution mode (P1)

**Context:** resolved from debate-2026-04-12-full-auto-execution. The debate initially framed the question as workflow semantics; the user reframed it as a concrete Claude Code permissions problem. This spec implements the reframed version.

## Problem

The template currently ships a `.claude/settings.json` where `permissions.allow` is under-specified: many common workflow actions (`Write`, `Edit` outside `src/tests/.meta`, non-uv/git shell commands, `Glob`, `Grep`, `TodoWrite`) fall into the implicit "ask" bucket. During a validated plan, Claude Code interrupts repeatedly to request authorization on actions the user already approved when they approved the plan. This breaks flow and defeats the purpose of upfront plan approval.

At the same time, the template must stay **safe by default** — a newcomer who forks the repo should not inherit a config that can accidentally wreck their machine. But it must also support a **full-auto** profile for the user who wants to launch a validated spec on a server and walk away.

## Goal

Ship a copier-tunable `execution_mode` parameter that selects between two coherent permission presets in the generated `.claude/settings.json`, paired with a CLAUDE.md prose rule that clarifies the semantics of plan approval. The user keeps the ability to edit `settings.json` manually after generation, or to re-run `copier update` with a different answer.

## Non-goals

- **No execution-receipt primitive.** The debate raised this as a valuable in-flight awareness mechanism, but it is a separate concern and would require changes to the plan-execution skill. Deferred to post-v1.0.0 backlog.
- **No session-log persistence.** Also deferred — requires a taxonomy addition.
- **No runtime mode switch.** The mode is a project-level default set at copier time. Runtime overrides happen via direct edit of `settings.json`, not via an in-session toggle.

## Solution

### 1. New copier parameter

Add to `copier.yml` after `meta_visibility`:

```yaml
execution_mode:
  type: str
  help: "Claude Code permission preset. 'safe' asks before touching repo structure or running destructive commands (recommended default). 'full-auto' allows everything except a hard safety net — use only for unsupervised runs (VPS, overnight spec execution)."
  choices:
    - safe
    - full-auto
  default: safe
```

Default is `safe`. The `full-auto` choice must be explicit.

### 2. Template conditional — `template/.claude/settings.json.jinja`

The file becomes conditional on `execution_mode`. The `attribution` and `hooks` blocks are identical in both modes; only `permissions` differs.

**Shared deny list (safety net, identical in both modes):**

```
Bash(rm -rf *)
Bash(sudo *)
Bash(dd *)
Bash(mkfs *)
Bash(chmod -R 777 *)
Bash(curl * | sh)
Bash(wget * | sh)
Edit(.env)
Edit(.env.*)
Edit(.git/**)
Read(~/.ssh/**)
Read(~/.aws/**)
Read(~/.gnupg/**)
Read(~/.pypirc)
Read(~/.netrc)
```

Rationale: the deny list is the one thing that must NEVER vary by mode. A fork bomb or a `curl | sh` is catastrophic regardless of supervision level. Uniformity also makes audits trivial.

**`safe` preset (default):**

```
allow:
  Bash(uv *)
  Bash(git status), Bash(git diff *), Bash(git log *), Bash(git add *),
  Bash(git commit *), Bash(git branch *), Bash(git checkout *),
  Bash(git switch *), Bash(git pull), Bash(git fetch *), Bash(git stash *)
  Bash(ls *), Bash(pwd)
  Bash(pytest *), Bash(ruff *), Bash(pre-commit *), Bash(copier *)
  Read, Glob, Grep, TodoWrite
  Edit(src/**), Edit(tests/**), Edit(.meta/**), Edit(docs/**)
  Write(src/**), Write(tests/**), Write(.meta/**), Write(docs/**)

ask:
  Bash(git push *)
  Bash(rm *), Bash(mv *), Bash(mkdir *)
  Edit(pyproject.toml), Edit(.gitignore),
  Edit(.pre-commit-config.yaml)
  Edit(CLAUDE.md), Edit(README.md)
  Edit(.claude/**), Edit(.github/**)
  Write(*)  (anything outside the allowed write globs)
```

Rationale: in `safe`, the user wants friction-free dev on source code, tests, docs, and `.meta/`, but any touch to the project's contract (pyproject, gitignore, pre-commit, CLAUDE.md, README, .claude config, .github) must be explicit. `Bash(rm *)` and `Bash(mv *)` ask because they're irreversible even when not `-rf`.

**`full-auto` preset:**

```
allow:
  Bash(*), Read, Glob, Grep, TodoWrite
  Edit(*), Write(*)
  WebFetch, WebSearch

ask: []
```

Rationale: unsupervised execution requires zero interactive prompts. The deny list is the only remaining brake. The user who picks this has been warned explicitly at copier time and must accept the risk.

### 3. CLAUDE.md prose rule

Add a new automatism (or extend automatism #4) in `template/CLAUDE.md.jinja`:

> **Plan validated = all actions validated.** Once the user has explicitly approved a plan, execute it end-to-end without asking for confirmation at each step. The plan's approval covers every action it lists. Interrupt only if (a) the plan itself requires an explicit checkpoint, (b) you encounter a situation genuinely not anticipated by the plan, or (c) Claude Code blocks you materially via `permissions.ask`.

This rule is identical in both modes. It clarifies that the existing decision tree's "wait → execute" semantic means *execute the whole thing*, not "execute step 1, wait, execute step 2, wait".

### 4. README section

Add a new section to `README.md` (after "What you get", before "Visibility modes" or as part of it):

- Title: "Execution modes"
- Explain the two modes, when to use each, and the fact that mode is modifiable post-generation by editing `.claude/settings.json` or re-running `copier update`.
- Include a **warning** for `full-auto`: "Only use full-auto on environments where you accept that the AI can modify any file in the project without prompting. Never use full-auto on machines with production credentials outside the deny list."

## Acceptance criteria

1. **AC1 — copier param exists.** `copier.yml` contains `execution_mode` with choices `safe` / `full-auto`, default `safe`, and explicit help text warning about full-auto.
2. **AC2 — safe preset.** `copier copy . /tmp/test-safe --defaults --trust --vcs-ref=HEAD` generates a project whose `.claude/settings.json` matches the safe preset exactly.
3. **AC3 — full-auto preset.** `copier copy . /tmp/test-auto --data execution_mode=full-auto --trust --vcs-ref=HEAD` generates a project whose `.claude/settings.json` matches the full-auto preset exactly.
4. **AC4 — deny parity.** The deny list is byte-identical between the two generated files (same entries in same order).
5. **AC5 — prose rule present.** Both generated `CLAUDE.md` files contain the "plan validated = all actions validated" rule verbatim.
6. **AC6 — README documents both modes.** The generated `README.md` (if it exists in the template — if not, the repo README at root) contains an "Execution modes" section mentioning both choices, the warning on full-auto, and how to switch.
7. **AC7 — JSON validity.** Both generated `.claude/settings.json` files parse as valid JSON.
8. **AC8 — hooks unchanged.** The `attribution` and `hooks` blocks are identical between modes and match the pre-change template.
9. **AC9 — pre-commit passes.** `uv run pre-commit run --all-files` passes on the meta-repo after changes.
10. **AC10 — no regression on meta_visibility.** Regenerating with `meta_visibility=public` and `meta_visibility=private` still works for both execution modes (matrix of 4).

## Out of scope (confirmed)

- Execution receipts / session log persistence — deferred to v1.1.0 backlog
- Runtime mode toggle via slash command — not planned
- Per-plan mode override — not planned (user can edit `settings.json` directly if they want a one-off)

## Risks

- **Risk 1 — `full-auto` is too loose.** If the deny list has a gap, an unsupervised run could do damage. Mitigation: explicit README warning, conservative deny list with known-dangerous patterns, user must opt in explicitly (not the default).
- **Risk 2 — `safe` still produces friction.** If the allow list is too tight, users will immediately switch to full-auto, defeating the safety goal. Mitigation: the allow list covers the full normal dev workflow (src/tests/.meta/docs edits+writes, common shell tools), only asking on structural-contract changes.
- **Risk 3 — Claude Code glob semantics.** `Edit(src/**)` syntax must be valid for Claude Code's permission matcher. Mitigation: AC2/AC3 include smoke-testing generation; if matchers are wrong, the test reveals it before commit.
- **Risk 4 — `copier update` conflict.** A user who edited `settings.json` manually will get a merge conflict on update. Mitigation: documented in the README section.

## References

- debate-2026-04-12-full-auto-execution.md — origin of the decision
- `template/.claude/settings.json.jinja` — current file to modify
- `copier.yml` — where `meta_visibility` lives as the shape precedent
