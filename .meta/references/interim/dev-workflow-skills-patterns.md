# Dev Workflow Skills Patterns — Research Reference

> Date: 2026-04-02
> Source: obra/superpowers (594+ stars), community skills ecosystem
> Purpose: Inform which skills to include in metadev-protocol template

## 1. Brainstorming (`/brainstorming`)

**Source:** `obra/superpowers/skills/brainstorming/SKILL.md`

**What it tells Claude to do:**
- Activates BEFORE any code writing. Intercepts "Let's build X" requests.
- Asks one question at a time, multiple choice preferred.
- Explores 2-3 alternative approaches for every decision.
- Applies YAGNI ruthlessly — kills scope creep before it starts.
- Presents design in digestible sections for human validation.
- Assesses if project is too large for single spec; decomposes into sub-projects.
- Saves approved design document to `docs/superpowers/plans/`.

**Key insight:** Replaces Claude's native "plan mode" entirely. The skill intercepts plan mode and routes through brainstorming instead.

**For our template:** YES. Core skill. Prevents the #1 AI-coding failure: jumping to code without shared understanding.

## 2. Spec Writing (via brainstorming output)

**Source:** Integrated into brainstorming + writing-plans pipeline.

**What makes a good /spec skill:**
- Teases requirements out of conversation, not from assumptions.
- Shows spec in chunks short enough to read and digest (not a wall of text).
- Each section gets explicit human sign-off before proceeding.
- Spec must be concrete enough that "an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing" could implement it.
- No placeholders allowed — every file path, function signature, type must be exact.

**For our template:** YES. Fold into brainstorming skill or make it a separate phase. The "junior engineer" test is a great quality bar.

## 3. Planning (`/writing-plans`)

**Source:** `obra/superpowers/skills/writing-plans/SKILL.md`

**What it tells Claude to do:**
- Activates after an approved design exists.
- Maps out ALL files to create/modify BEFORE defining tasks.
- Breaks work into bite-sized tasks (2-5 minutes each).
- Every task has: exact file paths, complete code, verification steps.
- Designs units with clear boundaries and well-defined interfaces.
- Each file has one clear responsibility.

**Output format:** Markdown plan saved to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`.

**Self-review checklist after writing plan:**
1. Spec coverage — can you point to a task for every requirement?
2. Placeholder scan — search for vague red flags, fix them.
3. Type consistency — names/signatures match across tasks.

**For our template:** YES. The file-mapping-before-tasks pattern is critical. Plans enable autonomous multi-hour execution.

## 4. TDD (`/test-driven-development`)

**Source:** `obra/superpowers/skills/test-driven-development/SKILL.md`

**How it enforces RED-GREEN-REFACTOR:**
- **RED:** Write a failing test. Run it. Confirm it fails. If you didn't watch it fail, you don't know if it tests the right thing.
- **GREEN:** Write MINIMUM code to pass. Don't add features, refactor, or "improve" beyond the test.
- **REFACTOR:** Clean up while staying green. Don't add behavior.
- Strict rules: "Write code before the test? Delete it. Start over."
- Addresses rationalization directly: "Thinking 'skip TDD just this once'? Stop. That's rationalization."
- Bug fix protocol: Write failing test reproducing bug FIRST, then fix.

**Anti-context-pollution pattern:** Multi-agent TDD uses separate agents for test-writing vs implementation to prevent the implementation from "bleeding" into test logic.

**For our template:** YES. Essential discipline skill. The "delete and start over" enforcement is what makes it work vs. suggestions.

## 5. Code Review (`/requesting-code-review`)

**Source:** `obra/superpowers/skills/requesting-code-review/SKILL.md` + `receiving-code-review/SKILL.md`

**What it checks — two-stage review:**
1. **Spec compliance:** Did the implementer build what was requested? Nothing more, nothing less. Reviewer is explicitly told: "The implementer finished suspiciously quickly. Their report may be incomplete, inaccurate, or optimistic. You MUST verify everything independently."
2. **Code quality:** Only runs AFTER spec compliance passes. Checks patterns, naming, architecture.

**Self-review vs external:**
- Review is dispatched to a SUBAGENT with isolated context (not the implementing agent).
- Reviewer gets crafted context, never the session's history — prevents bias.
- Core principle: "Review early, review often."

**Critical lesson:** Skill descriptions that summarize workflow cause Claude to take shortcuts. A description saying "code review between tasks" caused ONE review instead of TWO. Fix: don't summarize workflow in the description.

**For our template:** YES. The two-stage pattern (spec then quality) is more rigorous than a single pass. Subagent isolation is ideal but even self-review with explicit phases helps.

## 6. Ship/Verification (`/verification-before-completion`)

**Source:** `obra/superpowers/skills/verification-before-completion/SKILL.md`

**What it does:**
- Activates before claiming work is done.
- Requires verification that the fix/feature actually works.
- "Untested fixes don't stick. Test first proves it."
- Coordinates verification across teammates before claiming team-wide completion.
- Prevents the common failure mode: Claude says "Done!" but nothing actually works.

**Checklist pattern (inferred from ecosystem):**
- All tests pass (not just new ones).
- Linter/formatter clean.
- The specific user-facing behavior works end-to-end.
- No regressions in related functionality.
- Commit is clean and follows conventions.

**For our template:** YES. Non-negotiable. This is the skill that turns "vibes" into "verified."

## 7. Debugging (`/systematic-debugging`)

**Source:** `obra/superpowers/skills/systematic-debugging/SKILL.md`

**4-phase structure:**
1. **Phase 1 — Evidence gathering:** For EACH component boundary, log what data enters/exits. Verify env/config propagation. Check state at each layer. Run once to gather evidence showing WHERE it breaks. THEN analyze. THEN investigate that specific component.
2. **Phase 2 — Root cause identification:** Trace bugs backward through call stack to find original trigger (`root-cause-tracing.md`).
3. **Phase 3 — Fix with defense in depth:** Add validation at multiple layers after finding root cause (`defense-in-depth.md`).
4. **Phase 4 — Verify fix.** If 3+ fixes fail, question the architecture (Phase 4.5).

**Strict enforcement:** "If you haven't completed Phase 1, you cannot propose fixes." This prevents guess-and-check thrashing — the #1 AI debugging anti-pattern.

**Supporting files in skill directory:** `condition-based-waiting.md`, `defense-in-depth.md`, `root-cause-tracing.md`, `find-polluter.sh`.

**For our template:** YES. Crucial. Without this, Claude's default is to guess-and-patch in loops.

---

## Summary: Skills for metadev-protocol template

| Skill | Priority | Rationale |
|---|---|---|
| brainstorming | P0 | Prevents premature coding |
| writing-plans | P0 | Enables autonomous execution |
| test-driven-development | P0 | Enforces quality discipline |
| verification-before-completion | P0 | Prevents false "done" claims |
| systematic-debugging | P0 | Stops guess-and-check loops |
| requesting-code-review | P1 | Two-stage review catches different bugs |
| spec-writing | P1 | Can fold into brainstorming initially |

All 7 should be in our template. The P0 skills are non-negotiable for any AI-assisted project.

## Sources

- [obra/superpowers](https://github.com/obra/superpowers) — primary reference
- [obra/superpowers skills directory](https://github.com/obra/superpowers/tree/main/skills)
- [Forcing Claude Code to TDD](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)
- [Best Claude Code Skills 2026 Guide](https://dev.to/raxxostudios/best-claude-code-skills-plugins-2026-guide-4ak4)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [claude-code-skill-factory TDD guide](https://github.com/alirezarezvani/claude-code-skill-factory/blob/dev/generated-skills/tdd-guide/SKILL.md)
