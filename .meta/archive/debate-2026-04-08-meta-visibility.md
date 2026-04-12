# Debate Record — .meta/ visibility for public release

**Date:** 2026-04-08
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (The Open Source Strategist)
**Status:** USER DECISION NEEDED

---

## Subject

Should .meta/ be public, private, or selectively exposed — both for the
metadev-protocol repo itself AND as a recommendation to projects generated
from it? What does the protocol's philosophy say about the visibility of
development context?

This is a foundational question: the answer affects the launch strategy,
the template defaults, and the project's credibility.

## Angles

- **A (The Transparency Advocate):** .meta/ IS the product. Hiding it undermines credibility. [insider]
- **B (The Minimalist):** Ship clean artifacts. Internal context is noise for consumers. [insider]
- **C (The Open Source Strategist):** What actually drives adoption and trust? [lone wolf]

---

## Strong arguments (survived cross-critique)

- **Artifact-based boundary, not directory-based** — raised by C, conceded by
  A and B. The binary "all public or all private" is a false choice. The right
  boundary is by artifact TYPE: curated reasoning (decisions, architecture) is
  signal; ephemeral process (sessions, scratch) is noise. All 3 agents converged.

- **ARCHITECTURE.md + decisions/ must be public** — raised by A, uncontested.
  These are credibility anchors. Developers evaluating the tool need to see
  WHY design choices were made. Rust RFCs, Django ADRs, Linux commit messages
  all prove this pattern works.

- **The template source repo must be the exemplar** — raised by A, conceded by
  B and C. "Eat your own dogfood" is not optional for a meta-tool. If the
  method works, the source repo should demonstrate it visibly.

- **scratch/ and sessions/ should be gitignored** — raised by B, uncontested.
  Drafts and session archives are truly ephemeral. Publishing them creates
  maintenance burden without value.

- **Maintenance burden is real** — raised by B, conceded by A and C. Stale
  decisions create confusion. Mitigation: use status flags and dates on all
  decision records, not hiding.

## Lone wolf insights

- **Credibility comes from clean reasoning, not raw process** — C identified
  that transparency and quality are different signals. Publishing raw session
  logs looks like chaos pretending to be transparency. Publishing synthesized
  decisions looks like competence. The distinction is what survives critique.

- **The template source repo and generated projects serve different audiences** —
  C and B converged on this. The source repo is for people evaluating the METHOD.
  Generated projects are for people USING the method. Different needs, possibly
  different .meta/ contents.

- **Competitive differentiation through visible reasoning** — C identified that
  most Python templates are "boring but solid." Visible architecture thinking
  makes people STUDY your tool, not just use it.

## Contested arguments (no consensus)

- **gold/ (research synthesis)** — A and C say public with disclaimers. B says
  only if mature enough to stand on its own.
  - **For:** prevents recurring conversations, shows depth of thinking
  - **Against:** working notes mistaken for endorsements
  - **Mitigation:** add disclaimer header to gold/ files

- **references/ (raw research)** — A says public (shows rejected approaches,
  prevents re-proposals). B and C say private (noise, liability).
  - **For:** institutional memory, shows what was considered and why not
  - **Against:** users might implement rejected ideas
  - **Why it matters:** references/ is the most "raw" content in .meta/

- **PILOT.md** — not directly debated but implicated. It contains current state,
  roadmap, priorities. Public = shows the project is alive and managed.
  Private = avoids exposing internal blockers (e.g., "git author leak").
  - For a launch, a clean PILOT.md is actually good marketing

## Dismissed arguments (refuted or irrelevant)

- **"All .meta/ must be public for philosophical purity"** — Agent A's initial
  maximalist position was refined after cross-critique. A conceded that
  selective exposure satisfies the philosophy without the noise.

- **"All .meta/ should be hidden"** — Agent B's initial minimalist position
  was explicitly retracted. B moved to artifact-based curation after
  seeing A's credibility argument and C's selective boundary.

## Convergence points

- Artifact-based boundary (not directory-based) (3/3)
- ARCHITECTURE.md + decisions/ = public (3/3)
- scratch/ + sessions/ = gitignored (3/3)
- Template source repo = visible exemplar of the method (3/3)
- Maintenance burden mitigated by status flags, not by hiding (3/3)
- Generated projects may have different defaults than source repo (2/3, A partially)

## Irreducible tensions

- **Exemplar completeness vs noise reduction** — the more .meta/ you show,
  the more authentic the exemplar but the higher the maintenance burden.
  No clear resolution: requires a judgment call on where to draw the line.

## Recommendation

**Confidence: high** — strong convergence on the core model.

### For metadev-protocol (this repo):

| .meta/ content | Visibility | Rationale |
|----------------|------------|-----------|
| ARCHITECTURE.md | Public | Credibility anchor — shows design thinking |
| DECISIONS.md + decisions/ | Public | Accountability — users evaluate choices |
| gold/ | Public (with headers) | Synthesized research — competitive differentiation |
| PILOT.md | Public (cleaned) | Shows project is alive and managed |
| GUIDELINES.md | Public | Already public — advisory best practices |
| references/ | Gitignored | Raw research — noise risk > value |
| sessions/ | Gitignored | Ephemeral archives — maintenance burden |
| scratch/ | Gitignored | Drafts — already designed to be private |
| SESSION-CONTEXT.md | Gitignored | Ephemeral per-session state |
| debates/ | Public | Shows structured decision-making in action |

### For generated projects (template defaults):

| .meta/ content | Visibility | Rationale |
|----------------|------------|-----------|
| PILOT.md | Committed | Project dashboard — essential for team/AI context |
| SESSION-CONTEXT.md | Committed | Living context — essential for AI continuity |
| GUIDELINES.md | Committed | Best practices reference |
| decisions/ | Committed (empty) | Pattern for user's own ADRs |
| sessions/ | Gitignored | User's own archives — private by default |
| scratch/ | Gitignored | User's own drafts — private by default |

Note: generated projects don't have gold/, references/, or debates/ by default.
Users can create them following the expansion paths pattern.

### Recommendation for users of generated projects:

Add to GUIDELINES.md a note: "If your project is open-source, consider keeping
.meta/decisions/ and .meta/PILOT.md public — they demonstrate thoughtful
development. Gitignore scratch/ and sessions/ as they contain ephemeral state."

## Decision

**USER DECISION NEEDED**

Key questions:
1. Does the artifact-based boundary feel right? (decisions/ public, sessions/ private)
2. Should gold/ be public in this repo? It contains synthesized research that shows depth.
3. Should PILOT.md be cleaned up and made public? It's currently raw with internal blockers.
4. For generated projects: commit PILOT.md + SESSION-CONTEXT.md by default, or gitignore?
