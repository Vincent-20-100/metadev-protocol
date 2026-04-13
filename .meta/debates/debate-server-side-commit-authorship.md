# Debate Record — Server-side commit authorship enforcement

**Date:** 2026-04-13
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user / Template adopter — DX & simplicity)
**Status:** USER DECISION NEEDED

---

## Subject

Should metadev-protocol add server-side commit authorship enforcement
(GitHub Action whitelist + branch protection + signed commits) on top of the
existing local pre-commit hook `check_git_author.py`?

**Trigger:** 10 Claude-authored commits reached `main` via a PR merged from a
cloud Claude Code sandbox (`claude/create-dev-branch-c6zlC`) that bypassed the
local hook entirely. The hook only runs on the developer's machine.

**Tension:** defense-in-depth principle vs. YAGNI rule in CLAUDE.md.

---

## Angles

- **A (Puriste):** the hook is security theater — only server-side creates a real guarantee [insider]
- **B (Pragmatique YAGNI):** one incident = process failure, not architectural gap; local hook suffices [insider]
- **C (End-user lone wolf):** server-side enforcement is governance overhead for a solo-dev bootstrap tool [lone wolf]

---

## Strong arguments (survived cross-critique)

- **The breach is empirical, not hypothetical** — raised by A, conceded by B and C. 10 Claude commits on `main` via cloud sandbox is a real event. Neither YAGNI nor "solo-dev trust model" can dismiss an observed failure.

- **Solo-dev discipline is not an architectural substitute** — raised by A, conceded by B partially. The cloud sandbox had no hook to invoke — this was an architecture gap, not a discipline failure.

- **GPG / signed commits solve identity, not author name** — raised by B (precise technical point), reinforced by C. A signed commit from `Claude <ai@anthropic.com>` is still a Claude commit. Signed commits are the wrong tool for this problem.

- **Branch protection rules don't filter `commit.author.name`** — raised by C (critical technical precision). GitHub's native branch protection cannot block by author name. Only a custom GitHub Action checking commit metadata can do this. The "server-side enforcement" framing was conflating several distinct mechanisms.

- **The `execution_mode` parameter is the correct architectural hook** — proposed by C in Phase 2 update. The template already has `execution_mode: safe|full-auto`. Server-side enforcement should be wired to this parameter, not shipped as a standalone opt-in.

---

## Lone wolf insights

- **Branch protection ≠ author name enforcement** — C identified that A's proposed mechanism (GitHub branch protection) does not actually address the specific failure mode (commit author name bypass). Insiders were treating "server-side = rigorous" as an axiom without checking whether the specific control blocks the specific vector. This is security theater by precise definition.

- **`execution_mode` already surfaces the right decision point** — C noticed that the template has a generation-time parameter that maps exactly to the solo/team distinction that drives this debate. The decision should be wired there, not added as a separate opt-in.

---

## Contested arguments (no consensus)

- **Is the root cause tooling or process?**
  - **B:** Review gate failure. The fix is a PR checklist reminder ("check author names"). Process rule is sufficient.
  - **A:** Review gates fail under pressure by design. Architecture must not rely on sustained human attention.
  - **Why it matters:** If process is sufficient, the fix is one line in a PR template. If architecture is required, we ship a GitHub Action.
  - **Resolution signal:** B self-contradicted — "process rule is sufficient" is discipline-dependent, and B argued elsewhere that discipline isn't reliable. A wins this point on logic.

- **Does "projects evolve solo→team" justify server-side enforcement?**
  - **A:** Yes — template reusability makes the scale concrete.
  - **B:** YAGNI still applies. One incident is not a pattern. If it repeats, revisit.
  - **C:** This argument applies to every possible feature — it's a blank check for complexity if taken unconstrained.
  - **Partial consensus:** All three agree the right answer is: **make it available, wired to execution mode, not mandatory for solo**.

---

## Dismissed arguments (refuted or irrelevant)

- **"GPG + signed commits solve this"** — refuted by B and C. Wrong tool: verifies key identity, not `author.name`. Adds ceremony for zero benefit on this specific problem.

- **"Server-side enforcement is zero cost (20 lines YAML)"** — partially dismissed. The YAML is cheap; GPG setup, branch protection config, and user cognitive overhead are not. A was conflating implementation cost with adoption cost.

- **"Solo dev can't breach their own trust"** — dismissed. A provided empirical evidence of the breach. The cloud sandbox was not the developer acting against themselves; it was an external execution path with no hook to invoke.

- **"Mandatory server-side by default"** — dismissed by all three agents after cross-critique. Too much friction for the majority case.

---

## Convergence points

1. **The local hook stays** — mandatory, non-negotiable, already exists, low friction.
2. **GPG / signed commits are the wrong tool** for this problem — don't ship them.
3. **Server-side enforcement should be optional** — not forced at `copier copy`.
4. **A GitHub Actions workflow checking `commit.author.name`** (not branch protection rules) is the correct mechanism if we do ship something.
5. **`execution_mode: full-auto`** is the natural flag to trigger inclusion of server-side enforcement.

---

## Irreducible tensions

- **YAGNI vs defense-in-depth for a reusable template:** B says wait for a second incident. A says one real incident is enough for a template that ships to dozens of projects. This requires a value judgment: how much weight do you give to observed failure vs. adoption friction for future adopters?

- **Solo-dev assumption in GUIDELINES.md:** "For a solo repo with a disciplined local workflow, the hook alone is enough." This statement was written before the breach. It's now empirically incorrect for cases involving cloud AI sandboxes or external contributors. GUIDELINES.md needs updating regardless of what the template ships.

---

## Recommendation

**Confidence: HIGH on mechanism, MEDIUM on default.**

**The correct mechanism is: a GitHub Actions workflow that checks `commit.author.name`** against a denylist (`Claude`, `Anthropic`) on PRs targeting `main`. Not branch protection rules. Not GPG. Just an Action that scans commit metadata and fails if it finds a blocked name.

**Recommended implementation:**

1. **Keep the local hook** (already exists, not changing).

2. **Add `template/.github/workflows/check-commit-authors.yml`** — a minimal GitHub Action (~25 lines) that runs on PR events, scans commit author names, and fails if any match the denylist. This closes the exact vector that caused the breach (cloud sandbox → PR → merge).

3. **Wire inclusion to `execution_mode`:**
   - `safe` mode: workflow is **not included** (solo dev, no external agents, hook is enough)
   - `full-auto` mode: workflow is **included** (external agent execution paths are expected)
   
   This reflects reality: full-auto mode *is* the mode where cloud AI sandboxes create branches and PRs. Safe mode is local-only. The enforcement should match the threat model.

4. **Update GUIDELINES.md:** Replace "the hook alone is enough" with an accurate statement: "the hook prevents accidental commits from your machine; if you use cloud AI sandboxes or have external contributors, also enable the server-side check."

**What this does NOT do:** mandatory GPG, mandatory branch protection rules, any ceremony at `copier copy` time for solo-safe-mode projects.

---

## Decision

**USER DECISION NEEDED**

To decide, consider:

1. **Does the breach justify action now, or do you wait for a second incident?** A argues yes (one empirical breach in a reusable template is enough). B argues wait. You own the threshold.

2. **Is `execution_mode: full-auto` the right gate, or do you want a separate `enable_server_auth_check` parameter?** Wiring to execution_mode is implicit (clean) but may not be obvious to adopters. A separate parameter is explicit but adds a question to `copier copy`.

3. **Do you want to update GUIDELINES.md now regardless?** The "hook alone is enough" statement is now demonstrably false for cloud sandbox workflows. This update seems unambiguous.
