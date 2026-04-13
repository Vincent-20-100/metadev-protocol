---
name: research
description: External research with WebSearch + WebFetch + MCP — structured output to .meta/references/raw/
---

# /research

Gather structured external research on a question and write the findings to
`.meta/references/raw/`. Clean orthogonality with `/brainstorm` (internal
ideation) and `/audit-repo` (GitHub repo deep dives).

**When to use:** the answer depends on facts outside your training data —
recent libraries, competitor tools, emerging patterns, state-of-the-art, or
any claim that may have changed since the knowledge cutoff.

**When NOT to use:** you already know the answer and it is timeless (use
`/brainstorm` instead). Do not use `/research` to avoid thinking — use it to
avoid guessing.

---

## Hard rules

- **No code editing.** This skill only reads and writes research artifacts.
- **Always write an output file** to `.meta/references/raw/` — never deliver
  findings only in chat. Chat context disappears; files don't.
- **Always cite sources** with URL + date accessed. A finding without a source
  is an opinion.
- **Warn if fewer than 3 distinct sources** — single-source findings are
  fragile.
- **Soft budget:** recommend stopping at 8 WebFetch calls per run. The user
  can override; the skill recommends, it does not enforce.
- **No credential-gated sources** — only publicly accessible URLs.

---

## Process

### Step 1 — Clarify the question

Reformulate the user's question in one precise sentence:
- What exactly needs to be known?
- What time horizon? (current state, trends, history)
- What level of depth? (overview, technical detail, comparison)

If the reformulation differs from the user's phrasing, show it and confirm
before starting.

### Step 2 — Initial search (2-3 query variants)

Run WebSearch with 2-3 query variants to cover different angles:
- Direct question form
- Comparative form ("X vs Y")
- Trend form ("X 2025" or "X post-<event>")

Note which queries returned strong vs weak signals.

### Step 3 — Fetch promising URLs (3-5 sources)

For each promising URL from Step 2:
- Use WebFetch to retrieve the page
- Skim for relevance before extracting findings
- Prioritize: official docs > peer-reviewed > well-known blogs > forums
- Stop when 3 strong sources are confirmed; continue to 5 if findings diverge

Check for MCP servers if available (e.g., context7 for library docs) — they
often provide higher-quality structured content than raw WebFetch.

### Step 4 — Identify themes

Group findings into 2-5 themes based on what the sources actually say.
Do not force a theme if only one source mentions it.

### Step 5 — Spot consensus and divergence

- **Consensus:** claims multiple independent sources agree on
- **Divergence:** claims where sources contradict each other or give different
  context — this is often the most valuable finding

### Step 6 — Write the output file

Write to `.meta/references/raw/session-YYYY-MM-DD-research-<slug>.md`
following the locked schema below.

### Step 7 — Propose next step

Based on findings, propose:
- `/brainstorm` — if a decision needs to be made
- `/spec` — if the scope is clear enough to formalize
- `/audit-repo` — if a specific repo surfaced and deserves a deep dive
- Nothing — if research is self-contained

---

## Output schema (locked)

```markdown
---
type: session
date: YYYY-MM-DD
slug: research-<slug>
status: active
---

# Research — <question in one line>

**Question:** <full question>
**Date:** YYYY-MM-DD
**Sources consulted:** N (web: A, docs: B, MCP: C)

## 1. Context

<2-4 lines on why this research was needed>

## 2. Sources

- **[1]** <title> — <url> — accessed YYYY-MM-DD
- **[2]** ...

## 3. Findings (by theme)

### 3.1 <theme>

- <finding> [1]
- <finding> [2,3]

### 3.2 <theme>

...

## 4. Consensus vs divergence

- **Consensus across sources:** ...
- **Divergences / contradictions:** ...

## 5. Open questions for follow-up

- ...

## 6. Suggested next step

- `/brainstorm` if decision needed, `/spec` if scope clear, or state why none needed
```

---

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|---|---|
| "I know the answer from training data" | Training data has a cutoff and known gaps. Research is for current facts, not for avoiding thinking. |
| "One source is enough" | Single-source findings are fragile. Enforce the minimum-3-sources rule; warn the user if you can't reach it. |
| "I'll just summarize in chat, no file needed" | Chat context disappears. The output file is the deliverable, not the chat summary. |
| "The user seems in a hurry" | A poor research artifact is worse than no artifact — it creates false confidence. Write the file even if brief. |
| "WebFetch is slow, I'll skip some sources" | Source diversity is the point. Slow is acceptable. Skipping is not. |
