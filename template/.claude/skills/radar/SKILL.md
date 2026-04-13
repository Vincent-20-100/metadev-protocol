# /radar — automated tech-watch

Fetch emerging repos and articles near this project, store them as cards in
`.meta/references/research/`. Uses a Python script for all I/O — your job is
only the three LLM moments listed below.

## Usage

```
/radar              # Normal mode: top-K veille, weekly cadence
/radar --deep       # Deep mode: wider budgets, quarterly SOTA survey
/radar --refresh-themes   # Re-extract themes from PILOT.md
```

## Hard rules

- Never fetch content yourself — always delegate to the script
- Never edit `.meta/references/research/` manually — the script owns it
- If `research-themes.yaml` is missing, bootstrap it before running the script

---

## Process

### Step 1 — Bootstrap themes (first run or --refresh-themes)

Check if `.meta/research-themes.yaml` exists.

**If it does:** skip to Step 2.

**If it doesn't (or --refresh-themes):**

Read `.meta/PILOT.md`. Extract a draft `research-themes.yaml`:
- Identify 2–5 core topics from Vision, Stack, and Goals sections
- For each topic: choose a short name (kebab-case), 3–6 keywords, 0–2 negative keywords
- Default `max_new_per_source: 5`, `max_new_per_theme: 15`, `weight: 1.0`

Show the draft to the user:

```
I extracted these themes from your PILOT.md:

[paste the YAML]

Looks good, or do you want to adjust before I save?
```

Wait for confirmation. Then save:

```python
from scripts.radar.themes import ThemesConfig, Theme, save_themes
from pathlib import Path
# build ThemesConfig from user-confirmed yaml
save_themes(config, Path(".meta/research-themes.yaml"))
```

Or write the YAML directly to `.meta/research-themes.yaml`.

### Step 2 — Run the script

```bash
uv run python -m scripts.radar [--deep] [--project-dir .]
```

Capture stdout (JSON RunReport). If the script errors, show the error and stop.

If stdout is `{"action": "refresh_themes"}`, the user passed `--refresh-themes` —
go back to Step 1 and bootstrap.

### Step 3 — Frame the results

Parse the RunReport JSON. Present:

**Sources:** list which sources ran, how many items fetched, how many new vs known.
Flag any that failed with their error.

**Top new items per theme:** for each theme, show up to 3 new cards with title,
source, and one-line pitch. Link to the card file.

**Promotion candidates:** if any cards reached mentions_count >= 3 without a
synthesis, propose promotion:

```
3 cards are hot enough to synthesize:
- [title] (3 mentions from github, hf, reddit)

Want me to write a synthesis for any of these? Just name it.
```

**Nothing new:** if all themes returned 0 new items, say so clearly:
> "No new items matched your themes this run. Either sources are quiet or
> your keywords are too narrow — consider adding synonyms to `research-themes.yaml`."

---

## Failure modes

| Symptom | Cause | Action |
|---------|-------|--------|
| `gh: command not found` | GitHub CLI not installed | Tell user: `brew install gh && gh auth login` |
| `feedparser not installed` | Optional deps missing | Tell user: `uv sync --extra radar` |
| `huggingface_hub not installed` | Optional deps missing | Tell user: `uv sync --extra radar` |
| All themes return 0 items | Keywords too narrow | Suggest adding synonyms |
| `research-themes.yaml` malformed | Manual edit broke YAML | Show the error, offer to re-bootstrap |

---

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll fetch a few URLs myself to help" | The script handles dedup. Manual fetches bypass dedup and pollute the index. |
| "I'll skip bootstrap, themes can be added later" | Without themes, the script returns nothing. Bootstrap is required. |
| "The JSON looks fine, I'll skip the framing" | Framing is the only LLM value in this skill. Raw JSON is useless to the user. |
