# /research — Output schema

Reference format for every `/research` output. The skill writes one file per
run to `.meta/references/raw/session-YYYY-MM-DD-research-<slug>.md` using this
template. All fields are mandatory unless marked optional.

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

## Rules for filling the schema

- **Sources header counts must match the source list** — if you write
  "web: 3, docs: 1", section 2 must list exactly 4 entries.
- **Every finding cites at least one source** using `[N]` or `[N,M]`.
- **Consensus** = 2+ independent sources agree. Do not call a single source
  "consensus".
- **Divergence** = sources contradict or give materially different context.
  This section is often the most valuable — do not leave it empty if
  divergences exist.
- **Open questions** = gaps you could not close with the current sources.
  Empty is acceptable only if the research is self-contained.
