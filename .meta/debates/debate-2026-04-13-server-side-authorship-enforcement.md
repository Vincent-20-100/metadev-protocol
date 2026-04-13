---
type: debate
date: 2026-04-13
slug: server-side-authorship-enforcement
preset: architecture
mode: standard
context: hybrid
status: USER DECISION NEEDED
---

# Debate Record — Server-side authorship enforcement in metadev-protocol template

**Date:** 2026-04-13
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (End-user d'un template)
**Status:** USER DECISION NEEDED

---

## Subject

Should metadev-protocol's Copier template ship a GitHub Action that enforces commit authorship on main (whitelist a single author + copier param `author_email` + post-install instructions to enable branch protection + "Require signed commits"), or is this overengineering that violates the template's YAGNI rule?

**Trigger incident:** 10 commits authored by `Claude <noreply@anthropic.com>` landed on main via a PR merged from a Claude Code cloud sandbox branch (`claude/create-dev-branch-c6zlC`). The local `check_git_author.py` pre-commit hook never ran because the commits were created server-side.

## Angles

- **A (Puriste sécurité):** defense in depth — local hooks cannot defend server-side commits; the template must close the gap [insider]
- **B (Pragmatique YAGNI):** ship the cheapest upstream fix, iterate later; one incident ≠ pattern [insider]
- **C (End-user d'un template):** a fresh user running `copier copy` will resent post-install homework and unexpected prompts [lone wolf]

## Strong arguments (survived cross-critique)

- **Local pre-commit hooks are architecturally wrong for server-side threats** (A) — validated by the incident, conceded by C as "the logic holds regardless of incident count". B did not dispute the layer analysis, only the response proportion.
- **Copier param inflation (`author_email`) is unjustified friction** (B + C) — A conceded this in Phase 2 and narrowed the ask to "Action only, no prompt".
- **Post-install branch-protection homework creates a half-configured gate** (C) — neither insider defended the "enable it in GitHub UI after install" step. A half-enforced control is worse than no control because it creates false confidence.
- **The template already ships 2 Actions for server-side threats (`public-safety.yml`, `public-alert.yml`)** (A) — establishes precedent that SOME security concerns warrant server-side enforcement in the template. B partially contested by arguing authorship is a lower-stakes category than secret leakage.

## Lone wolf insights (survived cross-critique — HIGH VALUE)

- **Reframe: comprehension gap, not enforcement gap.** The outsider pointed out that both insiders assumed the deliverable must be code (hook, Action, workflow). But the solo-dev user's actual problem is "I don't know which commits are mine vs the AI's, and six months later I can't audit my history." That's an education problem, solvable with a GUIDELINES note + a one-line git config snippet — zero template complexity, zero platform dependency (works on GitLab/Gitea too), zero false enforcement theater. **This is the single most valuable contribution of the debate.**
- **A GitHub Action is not enforcement, it is a reminder in CI clothing.** It only runs if the user (a) pushes to GitHub, (b) has Actions enabled, (c) hasn't disabled the workflow. Insiders assumed GitHub as the deployment target; the outsider flagged this as an unexamined assumption.

## Contested arguments (no consensus)

- **Is one incident a pattern?**
  - A: "1 incident = 1 existence proof of a structural gap; the incident validates, not invalidates, the threat model"
  - B: "1 incident across 1 user in the meta-repo itself = exogenous bug, not template design flaw. Ship on downstream demand, not meta-repo events."
  - **Why it matters:** determines whether the fix goes in the template (ships to N future projects) or stays in the meta-repo only.
- **Is authorship the same category as secret leakage?**
  - A: "both are server-side threats, same enforcement layer"
  - B: "secret leakage is irreversible with catastrophic blast radius; AI authorship is reversible with a `git commit --amend --reset-author`. Different tier."
  - **Why it matters:** determines whether consistency with `public-safety.yml` is a valid architectural argument.
- **Does the proposed Action actually catch the observed attack?** (B exposed this as A's blind spot)
  - B: "A never showed the Action would catch the 10-commit pattern. If the commits were pushed via a token with Vincent's identity baked in, the Action checks nothing. Without that proof, shipping it is security theater."
  - A: did not directly refute — narrowed to "check `git log --format='%ae'` server-side, which does catch the incident's author field".
  - **Why it matters:** a control that doesn't close the observed gap is worse than useless.

## Dismissed arguments (refuted or irrelevant)

- **"author_email copier param is needed"** (original A position) — A conceded in Phase 2 that prompt inflation is real and not worth it.
- **"Signed commits are org norm, not solo default"** (C Phase 1) — B contested successfully: modern GitHub surfaces commit signatures as individual trust signal, not team governance. C did not re-defend in Phase 2.
- **"Signal mismatch — template is for solo dev, Actions are team governance"** (C Phase 1) — contested by both insiders; the template already ships 2 Actions without the audience resenting it. C implicitly retreated by shifting focus to "the right artifact is docs, not code."
- **"Template Rule 3 forbids this because there's no downstream demand"** (B Phase 1) — C exposed this as insider reasoning: new template users can't demand features they don't know exist.

## Convergence points

All three agents agreed by end of Phase 2:
1. The original full-stack proposal (Action + `author_email` copier param + post-install branch protection instructions + "Require signed commits" recommendation) is wrong as-is.
2. The local pre-commit hook is architecturally insufficient against server-side commit creation — this is a real gap, not a hypothetical.
3. Any fix that ships to the template must be zero-prompt and zero-post-install-homework.
4. The incident is real evidence of a structural layer problem, but the proportionality of the response is contested.

## Irreducible tensions

- **Code vs. docs as the deliverable.** A+B debate which artifact to ship; C challenges the premise that code is the right artifact at all. This is a value judgment about what a template's role is: enforcement scaffold, or legible mental model? No amount of cross-critique resolves it — it depends on who you think the template user is.
- **Meta-repo incident ≠ template user demand.** Whether a problem observed in metadev-protocol's own development justifies a template feature is a governance question about how scope expands. B's Rule 3 reading vs. A's consistency-with-existing-Actions reading is a genuine interpretive disagreement.

## Recommendation

**Confidence: high.** Ship the minimum: a GUIDELINES.md note and a one-line git config snippet. No Action, no copier param, no post-install homework.

**Rationale:**
- The lone wolf's reframe (comprehension > enforcement) survived both insiders' cross-critique intact. When an outsider challenges an unexamined premise and neither insider can refute it, that's a signal the insiders were debating the wrong question.
- A's original full stack was narrowed by A itself in Phase 2 to "Action only, no prompt" — meaning even the security puriste conceded 2 of the 3 original pieces.
- B's "cheaper upstream fix" list includes the best durable solution: configure the Claude Code sandbox identity at source, OR enable GitHub native "Require signed commits" via branch protection — both zero template code.
- The incident is real (the gap is real), but the fix that matches the severity is **documentation + a default `.gitconfig` snippet in the generated project's README**, not a YAML workflow.

**Proposed minimum deliverable:**
1. `template/.meta/GUIDELINES.md.jinja` gains a short "Commit authorship" section: why identity matters, the one-line git config, a link to GitHub's native "Require signed commits" doc for users who want server-side enforcement.
2. (Optional, low-confidence) `template/README.md.jinja` gains a 3-line "Before your first commit" note with the git config command.
3. Nothing else. No Action, no copier param, no branch protection instructions.

**What this leaves unaddressed:**
- metadev-protocol itself still has 10 Claude-authored commits on main. That's a separate decision (rewrite history vs. accept it) that the debate does not cover.
- If a second incident occurs across a different user, revisit with fresh evidence.

## Decision

**USER DECISION NEEDED**

To decide, consider:
1. **Do you think the template user's risk is "bad commits land on main" (enforcement problem) or "I can't audit my history six months later" (comprehension problem)?** If enforcement: A's narrowed Action proposal. If comprehension: C's docs note.
2. **Is Rule 3 (validated work only) a hard gate that requires downstream demand, or a guideline overridden by meta-repo incidents?** If hard gate: ship nothing template-side, fix meta-repo only. If overridable: the docs note is safe to ship.
3. **For the meta-repo specifically: do you want to rewrite history to remove the 10 Claude commits, or accept them as a documented historical anomaly?** (Separate decision — not covered by this debate.)
