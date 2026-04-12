---
type: plan
date: 2026-04-13
slug: outreach-messages
status: active
---

# Outreach messages — v1.1.0 beta launch

**Date:** 2026-04-13
**Version:** v1.1.0 (live but unannounced)
**Source spec:** `archive/spec-2026-04-12-outreach-messaging.md`
**Tracking:** `plan-2026-04-13-outreach-tracking.md`

Framing: repo is public on GitHub but has not been announced anywhere yet — recipients are "among the first" to be told, before the launch posts. No "private beta" wording (factually incorrect).

CTA: 5 min to take a look, feedback-oriented. No ask for likes/shares.

---

## Tier D1 — Immediate (2026-04-13)

### #1 — Guillaume Desforges (nix-copier-python) — LinkedIn DM — FR

**Relation:** convergence

```
Salut Guillaume,

Je suis Vincent — je viens de publier metadev-protocol v1.1.0, un template
Copier pour projets Python assistés par AI (workflow gates, .meta/ taxonomy,
audit de sécurité, 8 skills + 5 agents).

On est arrivés indépendamment à la même intuition : "template Copier =
opinions cristallisées sur le dev AI". J'ai découvert nix-copier-python
après avoir déjà fait mes choix d'archi — ta démarche prose-first (playbook,
philosophie) m'a conforté dans l'approche. Nos projets sont complémentaires :
toi côté prose et philosophie, moi côté enforcement (hooks, permissions,
decision tree). L'union serait puissante.

Le repo est live mais je ne l'ai encore annoncé nulle part — tu es parmi
les premiers à qui j'en parle avant les posts de lancement.

Si tu as 5 minutes pour y jeter un œil, ton retour vaudrait de l'or.

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #2 — Safi Shamsi (Graphify) — X DM — EN

**Relation:** reference

```
Hi Safi,

I'm Vincent — just shipped metadev-protocol v1.1.0, a Copier template for
AI-assisted Python projects with built-in workflow gates, .meta/ taxonomy,
and security audit.

I audited Graphify in depth to benchmark my own choices. What stuck with me:
confidence tagging on edges and the deterministic-first approach. Both
influenced how I designed the plan skill's GREEN/AMBER/RED confidence gates
and the honesty constraint (Rule #9) in the session contract. You're
credited in our CREDITS as a reference source.

The repo is live but I haven't announced it anywhere yet — you're among
the first I'm reaching out to before the launch posts.

5 min to take a look? Your feedback would mean a lot.

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #3 — Todd Gilbert (Superpowers) — X DM — EN

**Relation:** inspiration

```
Hi Todd,

I'm Vincent — just shipped metadev-protocol v1.1.0, a Copier template for
AI-assisted Python projects (workflow gates, .meta/ taxonomy, 8 skills +
5 agents).

The skills-as-folders architecture of Superpowers directly inspired how
I designed the skill ecosystem in my template — /brainstorm, /plan,
/debate, /orchestrate. The template recommends Superpowers as a complementary
plugin in CLAUDE.md: my built-in skills are the fallback when your plugin
isn't installed. You're credited in our CREDITS.

The repo is live but I haven't announced it anywhere yet — you're among
the first I'm reaching out to before the launch posts.

5 min to take a look? Your feedback would mean a lot. Thanks for Superpowers.

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #4 — Paul Bennett (Everything Claude Code / mrpbennett) — X DM — EN

**Relation:** inspiration

```
Hi Paul,

I'm Vincent — just shipped metadev-protocol v1.1.0, a Copier template for
AI-assisted Python projects (workflow gates, .meta/ taxonomy, 8 skills +
5 agents).

Your community-curated skills collection in Everything Claude Code (TDD,
security review, linting) directly inspired the agent personas in my
AGENTS.md — code-reviewer, test-engineer, security-auditor, data-analyst,
devil's-advocate. Complementary angle: you curate, I scaffold. You're
credited in our CREDITS.

The repo is live but I haven't announced it anywhere yet — you're among
the first I'm reaching out to before the launch posts.

5 min to take a look? Your feedback would mean a lot.

https://github.com/Vincent-20-100/metadev-protocol
```

---

## Tier D3 — 2026-04-15

### #5 — Companion AI team / Feynman — GitHub issue — EN

**Relation:** inspiration

```
Hi team,

I'm Vincent, author of metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
a Copier template for AI-assisted Python projects with workflow gates,
.meta/ taxonomy, and security audit.

Opening this issue as a thank-you, not a bug report. Feynman's SYSTEM.md
directly inspired two features in our v1.1.0:

- **Honesty constraint (Rule #9)** — never write "verified / confirmed /
  tested / reproduced" without cited evidence. Adapted from your framing.
- **Tiered confidence gates (GREEN/AMBER/RED)** in the plan skill —
  inspired by your multi-agent approach to uncertainty.

You're credited in our CREDITS. The repo is live but unannounced so far —
you're among the first I'm reaching out to before the launch posts.

If you have 5 minutes to take a look, any feedback would mean a lot.
```

---

### #6 — Yedan Zhang (Earnings Call Analyst) — X DM — EN

**Relation:** reference

```
Hi Yedan,

I'm Vincent — just shipped metadev-protocol v1.1.0, a Copier template
for AI-assisted Python projects with workflow gates and structured context.

I audited Earnings Call Analyst in depth to benchmark verification patterns.
Your tiered scoring (green/amber/red) directly influenced our plan skill's
confidence gates, and your prompt versioning approach is on our backlog
for post-v1.1. You're credited in our CREDITS as a reference source.

The repo is live but I haven't announced it anywhere yet — you're among
the first I'm reaching out to before the launch posts.

5 min to take a look? Your feedback would mean a lot.

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #7 — Copier core team (Yajo) — GitHub Discussion — EN

**Relation:** ecosystem

Channel: https://github.com/copier-org/copier/discussions (new discussion, Show & Tell category)

**Title:** `Show & tell: metadev-protocol — an AI-assisted Python project template built on Copier`

```
Hi Yajo and Copier team,

I built metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
a Copier template for AI-assisted Python projects. Copier is central to
how it works, and I wanted to share it as a real-world showcase:

- **`execution_mode` parameter** — `safe` vs `full-auto` conditionally rewrites
  `.claude/settings.json` permissions (safe blocks write tools by default,
  full-auto unlocks them). Nice demonstration of conditional file generation.
- **`meta_visibility` parameter** — `public` commits `.meta/`, `private`
  gitignores it. Single parameter, two distinct project shapes.
- **Immutable semver tags + `copier update`** — template versions tracked
  via annotated tags, users pull improvements with reviewable diffs.
- **CI matrix tests** — 4 combinations (safe/full-auto × public/private)
  via pytest + `copier copy`, ensuring every parameter combination generates
  a working project.

The repo just shipped v1.1.0 and is live but unannounced so far. Happy to
write a case study or blog post if useful for the Copier community.

Any feedback on how we're using Copier would be gold. Thanks for the tool!
```

---

### #8 — Claudio Jolowicz (Hypermodern Python) — GitHub issue — EN

**Relation:** peer

Channel: https://github.com/cjolowicz/cookiecutter-hypermodern-python/issues (new issue, Discussion label)

**Title:** `Discussion: metadev-protocol — a complementary take on opinionated Python templates`

```
Hi Claudio,

Longtime reader of the Hypermodern Python series. I built metadev-protocol
(https://github.com/Vincent-20-100/metadev-protocol), another opinionated
Python template, with a very different focus — and I think they're
complementary rather than competing.

- **Hypermodern Python:** tooling excellence (mypy, nox, sphinx, poetry,
  nox sessions). The gold standard for Python build/test/docs hygiene.
- **metadev-protocol:** AI-native governance. `.meta/` taxonomy for
  AI-session context, workflow gates (plan-before-edit decision tree),
  11 automatisms in CLAUDE.md, 8 skills + 5 agents, security audit for
  pre-public repos, honesty constraint on AI claims.

Different problem space (AI collaboration structure vs Python tooling rigor)
but same philosophy (opinionated, enforcement-first, templates as crystallized
decisions). v1.1.0 just shipped — live but unannounced so far.

Curious what you think. Happy to discuss anything that might be useful
cross-pollination.
```

---

### #9 — Frankie Robertson (cookiecutter-poetry) — GitHub issue — EN

**Relation:** peer

Channel: https://github.com/fpgmaas/cookiecutter-poetry/issues (new issue, Discussion label)

**Title:** `Discussion: metadev-protocol — Copier + AI-native features, happy to share notes`

```
Hi Frankie,

I built metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
a Python project template in the same space as cookiecutter-poetry but with
two different choices:

- **Copier over Cookiecutter** — primarily for `copier update`, so template
  improvements propagate to existing projects with reviewable diffs and
  immutable semver tags. I'd love to compare notes if you've looked at
  migrating.
- **AI-native governance layer** — `.meta/` taxonomy, workflow gates,
  11 automatisms, 8 skills + 5 agents. The template assumes Claude Code
  as primary collaborator and scaffolds accordingly.

v1.1.0 just shipped — live but unannounced so far. You're among the first
I'm reaching out to before the launch posts.

If you have 5 minutes to take a look, any feedback on the Copier migration
angle or AI governance choices would be really valuable.
```

---

## Tier D5 — 2026-04-17

### #10 — Scientific Python (cookie) — GitHub Discussion — EN

**Relation:** ecosystem

Channel: https://github.com/scientific-python/cookie/discussions (new discussion, Show & Tell)

**Title:** `Show & tell: metadev-protocol — Copier template with .meta/ taxonomy for reproducibility`

```
Hi Scientific Python folks,

I built metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
a Copier template for AI-assisted Python projects. Sharing it here because
one piece might interest the scientific-python community for reproducibility:

**The `.meta/` taxonomy** — every generated project has a canonical folder
for process artifacts, separate from the product:

- `active/` — validated plans, specs, debates currently in flight
- `archive/` — implemented or historical artifacts (chronological memory)
- `decisions/` — ADRs (adr-NNN-slug.md)
- `references/{raw,interim,synthesis}/` — external research by maturity
- `drafts/` — WIP, gitignored

Filename convention `<type>-<YYYY-MM-DD>-<slug>.md` is enforced by a
pre-commit hook. The point: a new session (human or AI) can reconstruct
project history from `.meta/` alone — without asking.

v1.1.0 just shipped — live but unannounced so far. Curious if this kind
of structure could help reproducibility workflows beyond AI collaboration.
Any feedback welcome.
```

---

### #11 — Caleb Sacks (claude-code-tips) — X reply/DM — EN

**Relation:** cold

```
Hi Caleb,

I built metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
an open-source Copier template that gives Claude Code persistent project
memory, workflow gates, and safety hooks — the kind of workflow you document
regularly on claude-code-tips.

v1.1.0 just shipped: 11 automatisms in CLAUDE.md, 8 skills + 5 agents,
inverted-default trigger table so the LLM proposes features proactively,
pre-commit secret scanning, Rule of 3 anti-consensus bias.

Live but unannounced so far. If any piece of it matches what your audience
cares about, feel free to use it. Happy to answer questions.

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #14 — Harper Reed — X DM — EN

**Relation:** cold

```
Hi Harper,

Built an open-source Copier template that gives Claude Code persistent
project memory and safety gates. The kind of problem I think you've
definitely run into: AI loses context between sessions, drafts pile up at
repo root, every project restarts from scratch.

metadev-protocol v1.1.0: 11 CLAUDE.md automatisms, 8 skills + 5 agents,
pre-commit secret scanning, devil's-advocate agent auto-triggered after
3 user agreements. One `copier copy` command.

Live but unannounced so far. 5 min to take a look?

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #15 — Matt Shumer — X DM — EN

**Relation:** cold

```
Hi Matt,

Built an open-source Copier template for AI-assisted Python projects —
gives agents persistent project memory (PILOT.md, SESSION-CONTEXT.md,
.meta/ taxonomy) and enforced workflow gates before any edit.

metadev-protocol v1.1.0. The structured-context approach is agent-agnostic —
could be relevant to the frameworks you build. 11 automatisms, 8 skills,
5 agent personas, hooks for secrets/lint/author identity.

Live but unannounced so far. 5 min to take a look?

https://github.com/Vincent-20-100/metadev-protocol
```

---

### #16 — Paul Gauthier (Aider) — GitHub Discussion — EN

**Relation:** cold

Channel: https://github.com/Aider-AI/aider/discussions (new discussion, Show & Tell / Ideas)

**Title:** `metadev-protocol — .meta/ taxonomy as agent-agnostic context structure`

```
Hi Paul and Aider community,

I built metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
a Copier template for AI-assisted Python projects. Cross-posting here because
one piece is explicitly agent-agnostic and might be interesting to Aider users.

**The `.meta/` taxonomy** — a canonical folder for process artifacts
separate from product code:

- PILOT.md as project dashboard
- SESSION-CONTEXT.md as living context
- `active/` / `archive/` / `decisions/` / `references/`
- Filename convention `<type>-<YYYY-MM-DD>-<slug>.md`, pre-commit-enforced

The point: whichever agent you use (Claude Code, Aider, Cursor, ...), it
reconstructs project history from `.meta/` before acting. No re-explaining.
The workflow gates are Claude Code-flavored but the `.meta/` structure isn't.

v1.1.0 just shipped — live but unannounced so far. Would love thoughts
from the Aider community on whether this kind of structured context could
integrate cleanly with Aider's workflow.
```

---

### #17 — Continue.dev team — GitHub Discussion — EN

**Relation:** cold

Channel: https://github.com/continuedev/continue/discussions (new discussion, Show & Tell)

**Title:** `Show & tell: metadev-protocol — structured context + workflow gates (editor-agnostic)`

```
Hi Continue team,

I built metadev-protocol (https://github.com/Vincent-20-100/metadev-protocol),
a Copier template for AI-assisted Python projects. Sharing because the
`.meta/` taxonomy and workflow gates are editor-agnostic and might be
interesting for Continue users.

- **`.meta/` taxonomy** — canonical folder for process artifacts (PILOT.md
  dashboard, SESSION-CONTEXT.md living context, `active/`, `archive/`,
  `decisions/`, `references/`). Filename convention enforced by pre-commit.
- **Workflow gates** — plan-before-edit decision tree, 11 automatisms,
  honesty constraint, Rule of 3 anti-consensus, secret scanning.
- **8 skills + 5 agent personas** — the skills are Claude Code-flavored
  but the structure (`.claude/skills/<name>/SKILL.md`) maps cleanly to
  Continue's custom commands model.

v1.1.0 just shipped — live but unannounced so far. Curious how well this
would fit with Continue. Happy to answer questions or collaborate on a
Continue-native adaptation.
```

---

## Tier D7 — 2026-04-19 (community posts)

### #18 — r/ClaudeAI — Reddit post — EN

**Title:** `I built a Copier template that gives Claude Code persistent project memory and workflow gates`

**Body:**
```
Hi r/ClaudeAI,

I kept running into the same loop: every session, Claude forgot where
the project stood, invented new file layouts, dropped drafts at repo
root, and tomorrow it started from zero. I got tired of re-explaining
intent instead of building.

So I built metadev-protocol — a Copier template for AI-assisted Python
projects. One `copier copy` command and you get:

- **PILOT.md + SESSION-CONTEXT.md** — Claude reads where you stopped,
  before doing anything.
- **`.meta/` taxonomy** — `active/`, `archive/`, `decisions/`,
  `references/`. Process artifacts separate from product code.
- **11 automatisms in CLAUDE.md** — plan-before-edit decision tree,
  honesty constraint (no "verified/tested" without evidence),
  Rule of 3 (devil's-advocate agent auto-fires after 3 user agreements).
- **8 skills + 5 agents** — /brainstorm, /plan, /debate, /orchestrate,
  code-reviewer, security-auditor, devil's-advocate.
- **Pre-commit hooks** — ruff, secret scanning, block Claude-as-author,
  filename convention enforcement.
- **Recommends Superpowers** as a complementary plugin.

Before/after diagrams, install in one command, v1.1.0 just shipped.

https://github.com/Vincent-20-100/metadev-protocol

Feedback welcome. What's broken in your Claude Code workflow that this
doesn't solve yet?
```

---

### #19 — r/ChatGPTCoding — Reddit post — EN

**Title:** `Open-source Copier template that gives AI coding assistants persistent project memory (Claude Code-flavored, agent-agnostic `.meta/`)`

**Body:**
```
Hi r/ChatGPTCoding,

Cross-posting a project I just shipped. Problem: AI coding assistants
lose context between sessions, invent file layouts, drop drafts at repo
root. Compound cost across dozens of sessions is worse than the
individual friction.

metadev-protocol is a Copier template for AI-assisted Python projects
that fixes this structurally, not with prompts.

- **PILOT.md + SESSION-CONTEXT.md** — the agent reads where you
  stopped before any action.
- **`.meta/` taxonomy** — `active/`, `archive/`, `decisions/`,
  `references/`, filename convention enforced by pre-commit. Agent-agnostic
  (works with Cursor, Aider, Continue, ChatGPT in a browser, whatever).
- **Workflow gates** — plan-before-edit decision tree, honesty constraint,
  Rule of 3 anti-consensus bias.
- **Skills + agent personas** — Claude Code-flavored in v1.1.0, but
  the structure maps to other tools.
- **Pre-commit hooks** — secret scanning, lint, filename enforcement.

One `copier copy` command. v1.1.0 live.

https://github.com/Vincent-20-100/metadev-protocol

Would love feedback, especially from folks using non-Claude stacks —
where does the structure hold, where does it need adaptation?
```

---

### #20 — Python Discord #showcase — EN

```
Hi everyone, I built metadev-protocol — a Copier template for AI-assisted
Python projects. One command and you get PILOT.md + SESSION-CONTEXT.md
as persistent project memory, a `.meta/` taxonomy for process artifacts,
workflow gates (plan-before-edit, honesty constraint, Rule of 3 anti-consensus),
8 skills, 5 agent personas, and pre-commit hooks for secrets/lint/author
identity. Built on uv + ruff + copier + pre-commit. v1.1.0 just shipped.

https://github.com/Vincent-20-100/metadev-protocol

Feedback welcome.
```

---

## Tier D10 — 2026-04-22

### #12 — Simon Willison — X / blog comment — EN

**Relation:** cold

```
Hi Simon,

Longtime reader. Built metadev-protocol
(https://github.com/Vincent-20-100/metadev-protocol), an open-source
Copier template for AI-assisted Python projects. Two pieces I think
might be blog-worthy:

- **`.meta/` taxonomy** — canonical folder for process artifacts
  separate from product code. Agent reconstructs project history before
  acting, no re-explaining.
- **Devil's-advocate agent auto-triggered by Rule of 3** — after 3
  consecutive user agreements without friction, an adversarial agent
  fires automatically. Anti-consensus bias built into the workflow.

v1.1.0 live. Happy to answer anything.
```

---

### #13 — Thorsten Ball (Zed) — X — EN

**Relation:** cold

```
Hi Thorsten,

Enjoyed your writing on agentic coding workflows. Built metadev-protocol
(https://github.com/Vincent-20-100/metadev-protocol) — a Copier template
for AI-assisted Python projects with workflow gates, plan-before-edit
decision tree, and `.meta/` taxonomy for persistent project memory.

v1.1.0 live. The structured-context approach is editor-agnostic — could
be interesting to adapt for Zed's agent panel.
```

---

### #21 — Hacker News — Show HN — EN

**Title:** `Show HN: Metadev-protocol – Copier template with workflow gates for Claude Code`

**Body:**
```
I built an opinionated Copier template for AI-assisted Python projects.
The problem it solves: AI coding assistants lose context between sessions,
invent file layouts, drop drafts at repo root, and every project restarts
from scratch. Compound cost across dozens of sessions is worse than the
individual friction.

metadev-protocol provides:

- PILOT.md + SESSION-CONTEXT.md as persistent project memory.
- A `.meta/` taxonomy (active, archive, decisions, references, drafts)
  with filename convention enforced by pre-commit. Process artifacts
  separate from product code.
- 11 automatisms in CLAUDE.md (plan-before-edit decision tree, honesty
  constraint, Rule of 3 anti-consensus bias).
- 8 skills (/brainstorm, /spec, /plan, /debate, /orchestrate, /test,
  /lint, /save-progress) and 5 agent personas (code-reviewer,
  test-engineer, security-auditor, data-analyst, devil's-advocate).
- Pre-commit hooks: ruff, secret scanning, Claude-as-author block,
  filename enforcement.
- Two execution modes (safe / full-auto) and two visibility modes
  (public / private `.meta/`) via Copier parameters.
- Immutable semver tags so `copier update` propagates template
  improvements to existing projects with reviewable diffs.

Built on Python 3.13, uv, ruff, copier, pre-commit. Recommends Superpowers
as a complementary plugin. v1.1.0 just shipped.

https://github.com/Vincent-20-100/metadev-protocol

Feedback welcome, especially on the `.meta/` taxonomy and whether the
workflow gates feel over-engineered or under-engineered for your use case.
```

---

### #22 — Changelog podcast / newsletter — intake form — EN

**Subject:** `Submission: metadev-protocol — AI-native project template (Copier + Claude Code)`

**Body:**
```
Project: metadev-protocol
URL: https://github.com/Vincent-20-100/metadev-protocol
One-liner: A Copier template that gives AI coding assistants persistent
project memory, workflow gates, and safety hooks.

Why it might be interesting to Changelog readers:

The compound cost of AI coding isn't any one session — it's losing context
between sessions and restarting from scratch. metadev-protocol attacks
this structurally: PILOT.md + SESSION-CONTEXT.md as persistent memory,
`.meta/` taxonomy for process artifacts, 11 automatisms in CLAUDE.md,
8 skills + 5 agent personas, pre-commit hooks for secrets and author
identity.

Technically distinctive: uses Copier's immutable semver tags so template
improvements propagate to existing projects via `copier update` with
reviewable diffs. Two execution modes (safe/full-auto) conditionally
generate `.claude/settings.json` permissions. Recursive — the template
is built using its own method.

v1.1.0 shipped 2026-04-12. Happy to write a case study or do an interview
if useful.

Vincent
```

---

### #23 — Dev.to / Hashnode — blog post — EN

**Title:** `How I gave my AI coding assistant structured memory (and stopped re-explaining my projects)`

**Angle / outline:**
```
1. The problem — compound cost of AI context loss, not any individual
   session. Every project restarts from scratch. Drafts at repo root.
2. The insight — the fix isn't a better prompt. It's structural:
   separate the product (src/, tests/, docs/) from the process (.meta/).
3. The `.meta/` taxonomy — active, archive, decisions, references, drafts.
   Filename convention `<type>-<YYYY-MM-DD>-<slug>.md`, enforced by
   pre-commit. Show directory tree.
4. Session memory — PILOT.md as dashboard, SESSION-CONTEXT.md rewritten
   each session. Show a concrete example.
5. Workflow gates — plan-before-edit decision tree, honesty constraint,
   Rule of 3 anti-consensus bias (devil's-advocate agent auto-fires
   after 3 user agreements).
6. Skills and agents — /brainstorm, /plan, /debate, /orchestrate + 5
   agent personas. Screenshots of invocation.
7. Making it reusable — why Copier over Cookiecutter (immutable semver
   tags + `copier update` diff propagation).
8. Try it — one `copier copy` command. Link.

Target length: 1500-2000 words. Publish after the launch posts settle.
Link back to repo and CREDITS (Todd/Superpowers, Companion AI/Feynman,
Safi/Graphify, Yedan/Earnings Call Analyst, Guillaume/nix-copier-python).
```

---

## Notes

- **Language:** Guillaume in FR (native). All others in EN.
- **Channel discipline:** follow the spec's channel per lead. D1 leans
  X DM (user preference), D3/D5 mix X DM + GitHub issue / Discussion
  depending on natural habitat. D7/D10 are community posts, not DMs.
- **Reframe:** repo is public but unannounced. No "private beta" wording —
  replaced by "live but unannounced" / "you're among the first I'm
  reaching out to before the launch posts".
- **CTA séquence:** these are Temps 1 messages. Temps 2 notifications
  (after the official launch posts) to be written in a separate batch.
- **Never re-relance more than once** if no reply, per spec.
