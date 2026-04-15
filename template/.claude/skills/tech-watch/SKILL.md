---
name: tech-watch
description: Unified tech-watch skill — sweep mode (automated fetch of emerging repos/articles near project themes) and deep mode (structural analysis of one specific GitHub repo). Fuses /radar (sweep) and /audit-repo (deep) with a shared card schema in .meta/references/research/.
---

# /tech-watch

Two modes, one skill, one card format.

## Usage

```
/tech-watch                     # sweep: top-K veille, weekly cadence
/tech-watch --deep              # sweep: wider budgets, quarterly SOTA
/tech-watch --refresh-themes    # sweep: re-extract themes from PILOT.md
/tech-watch <url>               # deep: analyze one GitHub repo
/tech-watch <url> --angle X     # deep: with analysis hint
```

All output cards land under `.meta/references/research/`.

## Hard rules

- Never fetch content yourself — delegate to the script.
- Never edit `.meta/references/research/` manually — the script owns it.
- Always write the output card, even on failure (use the failure template).
- No secrets in the output — redact credentials and tokens.

---

## Mode A — sweep (no URL)

### Step 1 — Bootstrap themes (first run or `--refresh-themes`)

Check if `.meta/research-themes.yaml` exists. If missing:

Read `.meta/PILOT.md` and extract a draft: 2–5 themes, each with a kebab-case name, 3–6 keywords, 0–2 negative keywords. Defaults: `max_new_per_source: 5`, `max_new_per_theme: 15`, `weight: 1.0`. Show the draft to the user, wait for confirmation, then save to `.meta/research-themes.yaml`.

### Step 2 — Run the script

```bash
uv run python -m scripts.tech_watch [--deep] [--project-dir .]
```

Capture the JSON RunReport. If stdout is `{"action": "refresh_themes"}`, go back to step 1.

### Step 3 — Frame the results

Parse the RunReport. Report per source (fetched / new / known / failed), top new items per theme (up to 3), and any promotion candidates (cards with `mentions_count >= 3`). If nothing new, say so plainly and suggest widening the themes.

---

## Mode B — deep (URL provided)

### Step 1 — Run the script

```bash
uv run python -m scripts.tech_watch <url> [--angle <hint>]
```

The script clones, fingerprints (language, repo type, stars, last commit, license, pitch), builds `tree -L 2`, cleans `/tmp/`, emits one JSON. On `gh` unavailable, `stars`/`last_commit` fall back to `unknown`. On `error: clone_failed`, use the failure template.

### Step 2 — Write the deep card

Write to `.meta/references/research/deep-<slug>-<YYYY-MM-DD>.md` with locked sections:

```
frontmatter: mode: deep / date / slug / url / angle / status: active
# Deep — <owner/repo>
## 1. Fingerprint              (from JSON)
## 2. Structure map            (curated tree_output)
## 3. Key findings
   3.1 Extension points
   3.2 Safety & governance
   3.3 Documentation quality
   3.4 Developer workflow
   3.5 Distinctive patterns
## 4. Tiered recommendations
   USE AS-IS / EXTRACT PARTS / BORROW CONCEPTS / INSPIRATION / REJECT
## 5. Open questions for follow-up
```

Each finding: **what / where (path:line) / why it matters.** Each tier item: rationale. Empty tiers get `(none)` — never skip a tier.

---

## Failure modes

| Symptom | Cause | Action |
|---------|-------|--------|
| `gh: command not found` | GitHub CLI not installed | `brew install gh && gh auth login` |
| `feedparser not installed` | Optional deps missing | `uv sync --extra tech-watch` |
| `huggingface_hub not installed` | Optional deps missing | `uv sync --extra tech-watch` |
| Sweep: all themes return 0 items | Keywords too narrow | Suggest adding synonyms |
| Sweep: `research-themes.yaml` malformed | Manual edit broke YAML | Show error, offer re-bootstrap |
| Deep: `error: clone_failed` | Private repo, 404, non-git URL | Section 1 `UNREACHABLE`, sections 2–5 `(clone failed: <reason>)` |

## Rationalizations you must not accept

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll fetch a few URLs myself to help" | The script handles dedup. Manual fetches bypass dedup and pollute the index. |
| "The JSON looks fine, I'll skip the framing" | Framing is the only LLM value in this skill. Raw JSON is useless to the user. |
| "I'll skip a tier since there's nothing there" | Empty tiers are load-bearing — they prove you looked. Write `(none)`. |
| "Deep mode can reuse the sweep card format" | No. Deep cards have findings + tiers; sweep cards have source + mentions. Different schemas. |
