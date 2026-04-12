---
type: plan
date: 2026-04-12
slug: launch-posts
status: active (draft — needs brainstorm refinement)
---

# Plan — Launch posts v1.0.0

**Date:** 2026-04-12
**Confidence:** AMBER — structure ready, voice needs Vincent's personal touch

---

## LinkedIn (~1450 chars)

I've been building with AI coding assistants for months. Here's what I learned: the AI is not the bottleneck. The lack of structure around it is.

Every new session starts from zero. No memory of past decisions. No guard rails. No way to stop the AI from confidently shipping secrets to GitHub. So I built a system to fix that.

metadev-protocol is an open-source Copier template that bootstraps Python projects with a built-in collaboration protocol between you and your AI assistant.

What makes it different from yet another project template:

→ A .meta/ taxonomy (PILOT, active specs, decision logs) that gives AI persistent context across sessions — no more re-explaining your architecture every Monday morning

→ Workflow gates with a devil's advocate step — the AI must argue against its own plan before you approve it. Sounds extreme. Catches real problems.

→ A public safety audit scanning 40+ secret patterns (AWS keys, tokens, private keys) at every commit. Because "I'll add .gitignore later" is how credentials end up on GitHub

→ Two execution modes: safe (human approves everything) and full-auto (for when you trust the pipeline). You choose per project.

→ Versioned updates via copier update — when the template improves, your existing projects get the diff, not a full regeneration

The recursive part: metadev-protocol uses its own method to build itself. The .meta/ folder, the specs, the workflow gates — they're both the product and the process.

This is a solo project. I built it because I needed it. If you're using Claude Code, Cursor, or any AI assistant and feel like you're fighting entropy every session, this might help.

GitHub: https://github.com/Vincent-20-100/metadev-protocol

#OpenSource #AI #Python #DeveloperTools #ClaudeCode

---

## X/Twitter Thread (5 tweets)

**Tweet 1:**
I spent months building with AI coding assistants. The AI was never the problem. The missing structure around it was.

So I built metadev-protocol — an open-source template that gives AI persistent memory, workflow gates, and secret scanning from commit zero.

It just hit v1.0.0. Here's what it does 🧵

**Tweet 2:**
The core idea: a .meta/ taxonomy that travels with your repo.

PILOT.md = project state. Active specs. Decision logs. Archive.

Your AI reads these at session start. No more "let me re-explain the entire architecture." Context survives across sessions, across days, across assistants.

**Tweet 3:**
The part I'm most proud of: devil's advocate gates.

Before any plan gets approved, the AI must argue against its own proposal. Sounds annoying. In practice, it catches overengineering, missed edge cases, and bad assumptions — before a single line of code is written.

**Tweet 4:**
The safety layer that should have existed from day one:

40+ regex patterns scanning for AWS keys, GitHub tokens, private keys, database URIs — running at every commit via pre-commit hooks.

Plus two execution modes: safe (human approves all) and full-auto (for trusted pipelines). You pick per project.

**Tweet 5:**
It's Copier-based, so existing projects get versioned updates via `copier update` — just the diff, not a regeneration.

And yes, the template builds itself using its own method. Recursive by design.

Solo project, MIT licensed, built for Claude Code but works with any AI assistant.

→ https://github.com/Vincent-20-100/metadev-protocol

---

## Reddit r/ClaudeAI

**Title:** I built an open-source project template that gives Claude Code persistent memory and safety rails — metadev-protocol v1.0.0

**The problem I kept hitting**

Every time I started a Claude Code session, I was spending the first 10 minutes re-explaining context. What the project does. What decisions were already made. What not to touch. And even then, Claude would occasionally go rogue — refactoring things I didn't ask for, or worse, committing files with hardcoded secrets that I caught just in time.

I tried CLAUDE.md instructions. Better, but not enough. The AI had no structured memory of past sessions, no workflow that forced it to slow down before acting, and no automated safety net for the dumb mistakes.

**What I built**

metadev-protocol is a Copier template that bootstraps Python projects with a full AI collaboration protocol baked in. Here's the before/after:

**Before:**
- New session → Claude has no idea what happened yesterday
- Claude proposes a plan → you skim it → you say "go" → you regret it
- You remember to add secrets to .gitignore... eventually
- Template updates mean regenerating your whole project

**After:**
- New session → Claude reads .meta/PILOT.md, active specs, decision logs. It knows where things stand.
- Claude proposes a plan → a devil's advocate skill forces it to argue against its own proposal → you review both sides → then you decide
- 40+ secret patterns (AWS keys, tokens, private keys, DB URIs) are scanned at every commit automatically via pre-commit hooks
- Template updates arrive via `copier update` as a clean diff

There are also two execution modes: `safe` (Claude asks permission for everything) and `full-auto` (for when you trust the setup and want to let it run). You configure this per project.

**The recursive bit**

The template was built using its own methodology. The .meta/ folder in the repo is both the development cockpit for building the template AND the thing that gets shipped to new projects. I found that eating your own dog food is the fastest way to find what's missing.

**What it's NOT**

- Not a framework. It's a project template.
- Not Claude-specific. The .meta/ structure works with any AI assistant. The .claude/ skills are Claude Code specific but optional.
- Not magic. It's just structured files and pre-commit hooks. The value is in the methodology, not the tech.

MIT licensed, solo project, feedback very welcome.

GitHub: https://github.com/Vincent-20-100/metadev-protocol

---

## Hacker News (Show HN)

**Title:** Show HN: metadev-protocol – Copier template for AI-assisted Python projects with persistent context and safety gates

I've been using AI coding assistants (primarily Claude Code) for several months. The biggest friction wasn't the AI's capability — it was the lack of structure around it. Every session started from scratch, there were no workflow gates to prevent bad decisions, and secret leakage was one careless commit away.

metadev-protocol is a Copier template that addresses this by shipping three things with every new Python project:

1. A .meta/ taxonomy — PILOT.md (project state), active specs, decision logs, archive. The AI reads these at session start and has full context without re-prompting. Files follow a strict naming convention enforced by a linter.

2. Workflow gates — skills for brainstorming, planning, and shipping that include a devil's advocate step. The AI argues against its own proposal before you approve. This catches overengineering and missed edge cases early.

3. Safety scanning — pre-commit hooks running 40+ regex patterns for common secret types (AWS keys, GitHub/GitLab tokens, private keys, JWTs, database URIs). Two execution modes (safe/full-auto) control what the AI can do without human approval.

Being Copier-based means existing projects receive versioned updates via `copier update` — you get a diff of what changed in the template, not a full regeneration.

The template is built using its own methodology (the .meta/ folder is both the dev cockpit and the shipped artifact).

Stack: Python 3.13+, uv, ruff, pre-commit, copier. MIT licensed.

https://github.com/Vincent-20-100/metadev-protocol

---

**TODO:** Brainstorm — personalize voice, add specific anecdotes from Vincent's experience
