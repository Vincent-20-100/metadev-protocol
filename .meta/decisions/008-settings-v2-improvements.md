# ADR-008 — Settings.json v2 improvements

**Date:** 2026-04-05
**Status:** VALIDATED
**Sources:**
- update-config skill schema (official Claude Code docs)
- `.meta/references/ecosystem-deep-dive.md` (trailofbits security config)
- `.meta/references/claude-code-docs-audit.md` (comprehensive feature audit)
- ADR-006 strategic brainstorm decisions

---

## Context

After completing MVP Phase A and v2 Parts 1-2, we audited the full Claude Code
documentation and ecosystem to identify improvements for settings.json and the
template configuration. Each element was reviewed individually with trade-offs.

---

## Decisions

### ADOPTED

#### 1. Attribution: hide co-author (native)
```json
"attribution": {"commit": ""}
```
Replaces the planned pre-commit hook approach. Native, zero maintenance, 100% reliable.
The git commit author (from `git config`) remains unchanged — only the "Co-authored-by"
trailer is removed. User can re-enable in `settings.local.json`.

**Confidence: VERY HIGH**

#### 2. Security deny rules (trailofbits-inspired)
```json
"deny": [
  "Bash(rm -rf *)",
  "Bash(sudo *)",
  "Bash(dd *)",
  "Edit(.env)",
  "Edit(.git/**)",
  "Read(~/.ssh/**)",
  "Read(~/.aws/**)",
  "Read(~/.pypirc)"
],
"ask": [
  "Bash(git push --force *)"
]
```
Credentials reads (SSH keys, AWS creds, PyPI tokens) blocked — zero legitimate reason
for Claude to access them. `dd` added (destructive). Force push moved to `ask` instead
of `deny` — legitimate after rebase, user confirms.

**Confidence: VERY HIGH** — trailofbits security team patterns.

#### 3. SessionStart hook: check first_session flag
Permanent hook (not `once: true`) that reads PILOT.md and injects a welcome message
if `first_session: true` is present. No self-deletion, no git diff noise.
Works in tandem with CLAUDE.md automatism #2 (conversational onboarding).

**Confidence: HIGH**

#### 4. .claude/rules/ starter files
Generate 1-2 modular instruction files:
- `testing.md` — pytest conventions, test structure
- `code-style.md` — formatting, naming, patterns

Complements GUIDELINES.md: rules/ is instructions FOR the LLM,
GUIDELINES.md is advice for the developer AND the LLM.
Loaded lazily — no context cost when not relevant.

**Confidence: HIGH** — official feature, reduces CLAUDE.md size.

#### 5. Plan mode enforcement in CLAUDE.md
Strengthen automatism #4: "Before any Edit or Write, confirm the user has seen
and approved a plan. If no plan exists, propose one. Do not implement without
explicit approval."

Stronger than current "propose a plan before implementing". User always decides,
but Claude cannot skip the proposal step.

**Confidence: MEDIUM** — instruction-based (70-80% compliance), but combined with
the plan mode documentation in GUIDELINES.md, should be effective.

### DEFERRED (documented in GUIDELINES.md as advanced options)

#### 6. enabledPlugins (auto-activate Superpowers)
**Why deferred:** Forces an external dependency. Current flow (detect → propose → install
if user agrees) respects user choice. Documented as a commented example in GUIDELINES.md:
"To force Superpowers for all contributors, add to settings.json:
`enabledPlugins: {superpowers@claude-plugins-official: true}`"

#### 7. autoDreamEnabled
**Why deferred:** Creates two competing memory systems (autoDream + SESSION-CONTEXT.md).
Risk of contradiction. Wait for better understanding of interaction. Documented as
advanced option.

#### 8. autoMemoryEnabled + autoMemoryDirectory
**Why deferred:** Same logic as autoDream. Relocating memory to .meta/ without
clarifying the relationship with SESSION-CONTEXT.md is premature. Part of the
.meta/ reorganization brainstorm.

#### 9. plansDirectory
**Why deferred:** scratch/ is gitignored = plans lost between sessions. Plans need
a proper lifecycle (active/archived/deleted), not just a directory redirect.
Part of the .meta/ reorganization brainstorm.

### REJECTED

#### 10. language setting
**Why rejected:** Default is already English. No value added until we implement
the copier language parameters (project_language / dev_language). Revisit then.

#### 11. autoCompactWindow
**Why rejected:** Anthropic's default is optimized. Tuning without measurement is
micro-management.

#### 12. Status line
**Why rejected for MVP:** Polish, not fundamental. Document in GUIDELINES.md
as an advanced tip for users who want context % visibility.

#### 13. AGENTS.md generation
**Why rejected for now:** 95% of users won't use it. Planned as Part 5 (multi-agent
support). Future: copier question "Which AI agents?" → generate CLAUDE.md / .cursorrules / AGENTS.md accordingly.

### NOTED FOR FUTURE

- **Public vs private repo:** .meta/ visibility question. Private repo = everything visible.
  Public repo = .meta/ should potentially be gitignored. Needs design work.
- **Multi-AI support:** Part 5 — question copier for AI agent choice, generate
  appropriate config files (CLAUDE.md, .cursorrules, AGENTS.md).

---

## Implementation plan

| # | Action | File impacted |
|---|--------|---------------|
| 1 | Add `attribution.commit: ""` | settings.json.jinja |
| 2 | Add security deny rules + ask force-push | settings.json.jinja |
| 3 | Add SessionStart hook (first_session check) | settings.json.jinja |
| 4 | Create .claude/rules/testing.md | template/.claude/rules/ |
| 5 | Create .claude/rules/code-style.md | template/.claude/rules/ |
| 6 | Strengthen automatism #4 (plan enforcement) | CLAUDE.md.jinja |
| 7 | Document deferred options | GUIDELINES.md.jinja |
| 8 | Test full generation | all profiles |
