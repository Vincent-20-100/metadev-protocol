---
name: research
description: External research with WebSearch + WebFetch + MCP — structured output to .meta/references/raw/
---

# /research

Gather structured external research on a question and write findings to
`.meta/references/raw/`. Orthogonal to `/brainstorm` (internal ideation) and
`/audit-repo` (GitHub repo deep dives).

**When to use:** the answer depends on facts outside your training data —
recent libraries, competitor tools, emerging patterns, state-of-the-art, or
any claim that may have changed since the knowledge cutoff.

**When NOT to use:** you already know the answer and it is timeless — use
`/brainstorm` instead. Do not use `/research` to avoid thinking, only to
avoid guessing.

---

## Hard rules

- **No code editing.** This skill only reads and writes research artifacts.
- **Always write an output file** to `.meta/references/raw/` — never deliver
  findings only in chat. Chat disappears; files don't.
- **Always cite sources** with URL + date accessed. A finding without a
  source is an opinion.
- **Warn if fewer than 3 distinct sources** — single-source findings are
  fragile.
- **Soft budget:** recommend stopping at 8 WebFetch calls per run. User can
  override.
- **No credential-gated sources** — public URLs only.
- **Prefer MCP when available** (e.g., context7 for library docs) — higher
  signal than raw WebFetch.

---

## Three steps

### 1. Clarify

Reformulate the question in one precise sentence: what needs to be known,
what time horizon, what depth. If the reformulation differs from the user's
phrasing, show it and confirm before starting.

### 2. Research

- Run WebSearch with 2-3 query variants (direct, comparative, trend form).
- Fetch 3-5 promising URLs. Prioritize official docs > peer-reviewed >
  well-known blogs > forums.
- Stop when 3 strong sources agree; continue to 5 if findings diverge.
- Group findings into 2-5 themes. Identify consensus and divergence —
  divergence is often the most valuable finding.

### 3. Write

Write to `.meta/references/raw/session-YYYY-MM-DD-research-<slug>.md`
following `output-schema.md` (same directory as this SKILL.md). Every field
in the schema is mandatory.

Then propose one next step: `/brainstorm` (decision needed), `/spec` (scope
clear), `/audit-repo` (specific repo surfaced), or nothing (self-contained).

---

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|---|---|
| "I know the answer from training data" | Training has a cutoff. Research is for current facts. |
| "One source is enough" | Single-source = fragile. Warn if you can't reach 3. |
| "I'll just summarize in chat, no file needed" | Chat context disappears. The file is the deliverable. |
| "The user seems in a hurry" | A poor artifact creates false confidence. Write the file even if brief. |
