---
mode: deep
date: 2026-04-15
slug: caveman
url: https://github.com/JuliusBrussee/caveman
angle: multi-LLM + multi-IDE + benchmarks/evals primary source
status: active
---

# Deep — JuliusBrussee/caveman

## 1. Fingerprint

- **primary_lang:** JavaScript (hooks) + Python (benchmarks/evals) + Markdown (skills/rules)
- **repo_type:** Multi-agent distribution package (one skill → 8+ agents)
- **file_count:** ~80 tracked files (shallow clone depth 20)
- **license:** MIT
- **pitch:** "why use many token when few do trick" — a single caveman-speak skill shipped simultaneously as a Claude Code plugin, Codex plugin, Gemini CLI extension, Cursor/Windsurf/Cline/Copilot rule, and `npx skills` drop-in for 40+ other agents. Cuts ~65–75% output tokens while keeping technical accuracy.
- **stars:** Referenced as "viral" in README; active, 57+ commits on main in shallow window

## 2. Structure map

```
caveman/
├── .agents/plugins/marketplace.json        # generic marketplace manifest
├── .claude-plugin/
│   ├── marketplace.json                    # Claude Code marketplace manifest
│   └── plugin.json                         # Claude Code plugin definition (hooks wired here)
├── .clinerules/caveman.md                  # Cline rule (auto-synced from rules/)
├── .codex/
│   ├── config.toml                         # [features] codex_hooks = true
│   └── hooks.json                          # Codex SessionStart hook (echo -> stdout)
├── .cursor/
│   ├── rules/caveman.mdc                   # Cursor rule with alwaysApply: true
│   └── skills/caveman/SKILL.md             # mirrored skill (auto-synced)
├── .windsurf/
│   ├── rules/caveman.md                    # Windsurf rule with trigger: always_on
│   └── skills/caveman/SKILL.md             # mirrored skill (auto-synced)
├── .github/
│   ├── copilot-instructions.md             # Copilot instructions (auto-synced from rules/)
│   └── workflows/sync-skill.yml            # THE sync workflow — one source → many outputs
├── AGENTS.md                               # 4-line file: @imports to SKILL.md files
├── GEMINI.md                               # Same 4-line file, different filename
├── CLAUDE.md                               # 215-line agent cockpit (ownership table, CI rules)
├── CLAUDE.original.md                      # Pre-compress backup (caveman-compress output pattern)
├── README.md                               # 416-line product front door (install matrix)
├── benchmarks/
│   ├── prompts.json                        # Canonical prompt set
│   ├── requirements.txt
│   ├── results/                            # Committed JSON snapshots
│   └── run.py                              # Anthropic SDK, median-of-trials, README auto-patch
├── evals/
│   ├── llm_run.py                          # Three-arm harness (baseline / terse / skill)
│   ├── measure.py                          # Offline tiktoken measurement (no API)
│   ├── plot.py
│   ├── prompts/en.txt
│   ├── snapshots/results.json              # Committed snapshot
│   └── README.md
├── hooks/
│   ├── caveman-activate.js                 # SessionStart hook (reads SKILL.md, filters by mode)
│   ├── caveman-config.js                   # safeWriteFlag / readFlag symlink-safe primitives
│   ├── caveman-mode-tracker.js             # UserPromptSubmit hook (slash + NL triggers + reinforcement)
│   ├── caveman-statusline.sh / .ps1        # Badge renderer
│   ├── install.sh / .ps1                   # Idempotent standalone installer
│   ├── uninstall.sh / .ps1
│   └── package.json                        # {"type": "commonjs"} pin — prevents ESM shadowing
├── commands/
│   ├── caveman.toml                        # 2-line slash command format (description + prompt)
│   ├── caveman-commit.toml
│   └── caveman-review.toml
├── rules/caveman-activate.md               # 16-line SOURCE for all agent rule files
├── skills/
│   ├── caveman/SKILL.md                    # SOURCE skill
│   ├── caveman-commit/SKILL.md
│   ├── caveman-review/SKILL.md
│   ├── caveman-help/SKILL.md
│   └── compress/SKILL.md                   # auto-synced from caveman-compress/
├── plugins/caveman/                        # bundled plugin artifact (auto-synced)
├── caveman/SKILL.md                        # top-level mirror (auto-synced)
├── caveman-compress/                       # sub-project: Python compressor for CLAUDE.md files
└── caveman.skill                           # ZIP artifact (auto-built)
```

## 3. Key findings

### 3.1 Extension points

**F1 — AGENTS.md / GEMINI.md as 4-line `@import` stubs** — `AGENTS.md:1`

```
@./skills/caveman/SKILL.md
@./skills/caveman-commit/SKILL.md
@./skills/caveman-review/SKILL.md
@./caveman-compress/SKILL.md
```

`GEMINI.md` is byte-identical. The multi-LLM story is NOT three forked files — it's one skill source, imported by reference from agent-specific entrypoints. Metadev's v2.0 multi-LLM question ("CLAUDE.md + AGENTS.md + GEMINI.md side-by-side?") has a cleaner answer here: same content, different filenames, trivial `@include` stubs, zero drift surface.

**F2 — SessionStart hook reads SKILL.md at runtime and filters by mode** — `hooks/caveman-activate.js:53-91`

```js
let skillContent = '';
try {
  skillContent = fs.readFileSync(
    path.join(__dirname, '..', 'skills', 'caveman', 'SKILL.md'), 'utf8'
  );
} catch (e) { /* standalone install — will use fallback below */ }
// ...
if (skillContent) {
  const body = skillContent.replace(/^---[\s\S]*?---\s*/, '');
  const filtered = body.split('\n').reduce((acc, line) => {
    const tableRowMatch = line.match(/^\|\s*\*\*(\S+?)\*\*\s*\|/);
    if (tableRowMatch) {
      if (tableRowMatch[1] === modeLabel) acc.push(line);
      return acc;
    }
    // ...
  }, []);
  output = 'CAVEMAN MODE ACTIVE — level: ' + modeLabel + '\n\n' + filtered.join('\n');
}
```

The hook reads the source-of-truth SKILL.md live, strips YAML frontmatter, and line-filters the intensity table to keep only the currently-active row. No hardcoded duplication. If SKILL.md edits, next session picks it up automatically. This is progressive disclosure implemented at hook-time: inject only the relevant slice.

**F3 — Slash command `.toml` format is 2 lines** — `commands/caveman.toml:1-2`

```toml
description = "Switch caveman intensity level (lite/full/ultra/wenyan)"
prompt = "Switch to caveman {{args}} mode. If no level specified, use full. Respond terse like smart caveman — drop articles, filler, pleasantries. Fragments OK. Technical terms exact. Code unchanged. Pattern: [thing] [action] [reason]. [next step]."
```

Compared to metadev's markdown-based skill format, this is drastically cheaper to write and parse. Two fields. `{{args}}` interpolation. Done. Worth considering as an alternate "micro-skill" format for commands that are just parameterized prompts.

**F4 — CI sync workflow: one source → 10+ destinations** — `.github/workflows/sync-skill.yml:35-95`

```yaml
- name: Sync SKILL.md copies
  run: |
    cp skills/caveman/SKILL.md caveman/SKILL.md
    cp skills/caveman/SKILL.md plugins/caveman/skills/caveman/SKILL.md
    cp skills/caveman/SKILL.md .cursor/skills/caveman/SKILL.md
    mkdir -p .windsurf/skills/caveman
    cp skills/caveman/SKILL.md .windsurf/skills/caveman/SKILL.md

- name: Sync auto-activation rules
  run: |
    BODY="rules/caveman-activate.md"
    cp "$BODY" .clinerules/caveman.md
    cp "$BODY" .github/copilot-instructions.md
    printf '%s\n' '---' 'description: "..."' 'alwaysApply: true' '---' '' > .cursor/rules/caveman.mdc
    cat "$BODY" >> .cursor/rules/caveman.mdc
    printf '%s\n' '---' 'trigger: always_on' '---' '' > .windsurf/rules/caveman.md
    cat "$BODY" >> .windsurf/rules/caveman.md
```

The entire multi-IDE distribution strategy is implemented in ~50 lines of bash in a GitHub Action. Two source files (`skills/caveman/SKILL.md` + `rules/caveman-activate.md`) fan out to every IDE's convention, with per-target frontmatter grafted on at sync time. Commits with `[skip ci]` to avoid loop. This is the governance model metadev needs if it goes multi-IDE.

**F5 — Three-arm eval harness with the terse control** — `evals/llm_run.py:86-97`

```python
print("baseline (no system prompt)", flush=True)
snapshot["arms"]["__baseline__"] = [run_claude(p) for p in prompts]

print("terse (control: terse instruction only, no skill)", flush=True)
snapshot["arms"]["__terse__"] = [
    run_claude(p, system=TERSE_PREFIX) for p in prompts
]

for skill in skills:
    skill_md = (SKILLS / skill / "SKILL.md").read_text()
    system = f"{TERSE_PREFIX}\n\n{skill_md}"
    print(f"  {skill}", flush=True)
    snapshot["arms"][skill] = [run_claude(p, system=system) for p in prompts]
```

The key insight (documented in `CLAUDE.md:186-188`): comparing skill-vs-baseline conflates the skill with "just be terse". Caveman explicitly measures skill-vs-terse-control to isolate what the skill adds beyond a plain "Answer concisely." instruction. This is the single most important pattern in the repo for metadev's benchmarks-first-class question.

### 3.2 Safety & governance

**S1 — `safeWriteFlag` symlink-safe primitive** — `hooks/caveman-config.js:73-107`

```js
function safeWriteFlag(flagPath, content) {
  try {
    const flagDir = path.dirname(flagPath);
    fs.mkdirSync(flagDir, { recursive: true });
    try {
      if (fs.lstatSync(flagDir).isSymbolicLink()) return;
    } catch (e) { return; }
    try {
      if (fs.lstatSync(flagPath).isSymbolicLink()) return;
    } catch (e) {
      if (e.code !== 'ENOENT') return;
    }
    const tempPath = path.join(flagDir, `.caveman-active.${process.pid}.${Date.now()}`);
    const O_NOFOLLOW = typeof fs.constants.O_NOFOLLOW === 'number' ? fs.constants.O_NOFOLLOW : 0;
    const flags = fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | O_NOFOLLOW;
    let fd;
    try {
      fd = fs.openSync(tempPath, flags, 0o600);
      fs.writeSync(fd, String(content));
      try { fs.fchmodSync(fd, 0o600); } catch (e) {}
    } finally {
      if (fd !== undefined) fs.closeSync(fd);
    }
    fs.renameSync(tempPath, flagPath);
  } catch (e) {
    // Silent fail — flag is best-effort
  }
}
```

Refuses symlinks at target and immediate parent, uses `O_NOFOLLOW`, atomic temp+rename, `0600` perms, silent fail. Defends against local-attacker symlink-clobber on a predictable user-owned path. `readFlag` is symmetric: 64-byte cap + whitelist of VALID_MODES before return (lines 122-152). Any hook in metadev that writes a user-readable flag file should crib this.

**S2 — Statusline script has the same symlink + whitelist guards** — `hooks/caveman-statusline.sh:16-28`

```bash
[ -L "$FLAG" ] && exit 0
[ ! -f "$FLAG" ] && exit 0
MODE=$(head -c 64 "$FLAG" 2>/dev/null | tr -d '\n\r' | tr '[:upper:]' '[:lower:]')
MODE=$(printf '%s' "$MODE" | tr -cd 'a-z0-9-')
case "$MODE" in
  off|lite|full|ultra|wenyan-lite|wenyan|wenyan-full|wenyan-ultra|commit|review|compress) ;;
  *) exit 0 ;;
esac
```

The flag could be pointed at `~/.ssh/id_rsa` and the statusline would render raw bytes (including ANSI escapes) to the terminal on every keystroke. Three lines of defense: refuse symlinks, cap read, whitelist content. Anything outside whitelist → render nothing.

**S3 — CommonJS lock to prevent ESM shadowing** — `CLAUDE.md:84`

```
hooks/package.json pins the directory to {"type": "commonjs"} so the .js hooks
resolve as CJS even when an ancestor package.json (e.g. ~/.claude/package.json
from another plugin) declares "type": "module". Without this, require() blows
up with ReferenceError: require is not defined in ES module scope.
```

Defensive. Multi-plugin contamination is a real issue in `~/.claude/` — caveman defends itself against another plugin's `package.json` silently breaking its hooks. Metadev template should consider this pattern for any JS/TS-touching artifacts.

**S4 — Ownership table in CLAUDE.md** — `CLAUDE.md:26-54`

```
### Single source of truth files — edit only these
| File | What it controls |
| skills/caveman/SKILL.md | Caveman behavior: intensity levels, rules... |
| rules/caveman-activate.md | Always-on auto-activation rule body. CI injects... |

### Auto-generated / auto-synced — do not edit directly
Overwritten by CI on push to main when sources change. Edits here lost.
| File | Synced from |
| caveman/SKILL.md | skills/caveman/SKILL.md |
| .cursor/skills/caveman/SKILL.md | skills/caveman/SKILL.md |
...
```

Every file is explicitly tagged "source" or "generated". This is the exact contract metadev already enforces via `check_skills_contract.py`, but caveman puts it in the agent-visible CLAUDE.md so the LLM knows before touching anything. Metadev could embed this table in its CLAUDE.md template.

### 3.3 Documentation quality

- **README treats non-technical users as first-class.** CLAUDE.md:8 states: "Readable by non-AI-agent users. If you write 'SessionStart hook injects system context,' invisible to most — translate it." An explicit readability check is part of the commit contract for README changes.
- **Before/After sits at the top of the README** as the pitch. Install matrix is second. Everything else is progressive disclosure under `<details>` tags.
- **Benchmark numbers are generated, not typed.** `benchmarks/run.py:205-220` parses markers `<!-- BENCHMARK-TABLE-START -->` and splices in fresh median values. README is literally auto-patched.
- **CLAUDE.md is a file-ownership contract, not a tutorial.** 215 lines, mostly tables. No prose. Tells the agent "here is what you own, here is what CI owns, here is how they sync." Metadev's CLAUDE.md is conceptually close but heavier on philosophy — the caveman style is more actionable for agents.
- **Per-agent install details are collapsed** behind `<details>` blocks. Reader scans install table → expands only their agent. This keeps the README digestible despite supporting 8+ agents.

### 3.4 Developer workflow

**Install idempotency** — `hooks/install.sh:52-96`

```bash
ALL_FILES_PRESENT=1
for hook in "${HOOK_FILES[@]}"; do
  if [ ! -f "$HOOKS_DIR/$hook" ]; then
    ALL_FILES_PRESENT=0; break
  fi
done

HOOKS_WIRED=0
HAS_STATUSLINE=0
if [ "$ALL_FILES_PRESENT" -eq 1 ] && [ -f "$SETTINGS" ]; then
  if CAVEMAN_SETTINGS="$SETTINGS" node -e "
    const settings = JSON.parse(fs.readFileSync(process.env.CAVEMAN_SETTINGS, 'utf8'));
    const hasCavemanHook = (event) =>
      Array.isArray(settings.hooks?.[event]) &&
      settings.hooks[event].some(e =>
        e.hooks && e.hooks.some(h => h.command && h.command.includes('caveman'))
      );
    process.exit(hasCavemanHook('SessionStart') && hasCavemanHook('UserPromptSubmit') && !!settings.statusLine ? 0 : 1);
  " >/dev/null 2>&1; then
    HOOKS_WIRED=1; HAS_STATUSLINE=1
  fi
fi
```

The install script uses `node -e` to do safe JSON merging into `settings.json` — doesn't shell out to `jq`, doesn't sed-edit JSON (which is the common wrong answer). Backs up to `.bak` before writing. Passes paths via env vars to avoid shell injection if `$HOME` contains quotes. Exactly the pattern metadev's install-mode script needs.

**Benchmark harness uses Anthropic SDK directly, not CLI** — `benchmarks/run.py:52-75`

```python
def call_api(client, model, system, prompt, max_retries=3):
    delays = [5, 10, 20]
    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=model, max_tokens=4096, temperature=0,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            return {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                ...
            }
        except anthropic.RateLimitError:
            if attempt < max_retries:
                delay = delays[min(attempt, len(delays) - 1)]
                time.sleep(delay)
            else:
                raise
```

Benchmarks go through the SDK with exponential backoff and skill-file SHA256 in the output metadata (line 192: `"skill_md_sha256": skill_hash`). Results are committed to git with hash, so you can replay-bisect benchmark regressions. Metadev's benchmark story should adopt: SHA256 the skill, commit the result JSON, auto-patch the README.

**Evals are offline-readable** — `evals/measure.py:14` + `evals/llm_run.py` split

```
Run: uv run --with tiktoken python evals/measure.py
```

`llm_run.py` makes real LLM calls and writes `snapshots/results.json`. `measure.py` reads the snapshot offline with tiktoken and produces the table. CI can run `measure.py` without any API key or credentials — the expensive part only runs locally when SKILL.md changes. Snapshot-driven evals = no flaky CI, no secrets in CI.

### 3.5 Distinctive patterns ⭐

**D1 — The single-source-two-sources fan-out model**

Caveman has exactly **two** editable files for the core skill:
1. `skills/caveman/SKILL.md` — behavior
2. `rules/caveman-activate.md` — activation rule

These two files fan out via CI to ~10 destinations across 7+ agent ecosystems (Claude Code plugin, standalone, Codex plugin, Gemini extension, Cursor rule, Windsurf rule, Cline rule, Copilot instructions, plugin ZIP, npx skills). The CLAUDE.md ownership table makes the "don't touch this, edit upstream" contract explicit. The CI workflow enforces it with `[skip ci]` loop-break.

This is THE answer to metadev's multi-IDE question. Don't ship parallel files. Ship one source and a bash-in-GitHub-Actions fan-out, with an ownership table in CLAUDE.md. The cost of adding a new agent is ~5 lines in the sync workflow.

**D2 — Two-file multi-LLM: identical content, different filenames**

`AGENTS.md` and `GEMINI.md` are byte-identical 4-line files that `@import` the real skills. This is a weirdly elegant answer to "how do we support agents that want CLAUDE.md vs AGENTS.md vs GEMINI.md?" You don't. You put nothing in them. You make them imports. The real content lives in `skills/*/SKILL.md`. Adding another agent with yet another magic filename is `cp AGENTS.md NEWAGENT.md`.

Metadev could ship its root `CLAUDE.md` as the cockpit and have `AGENTS.md` / `GEMINI.md` be one-line `@./CLAUDE.md` imports. Zero drift, trivial.

**D3 — Runtime skill-filter by mode in SessionStart hook**

`hooks/caveman-activate.js:53-91` reads SKILL.md at hook-time, strips YAML, parses the markdown intensity table, and emits ONLY the active mode's row as the system-context injection. This is progressive disclosure at the injection layer: the full skill lives on disk, but the agent only ever sees the slice relevant to its current state. Hook reinforcement also emits a compact reminder on every user prompt (`caveman-mode-tracker.js` responsibility #3) to defend against "drift" where other plugins inject competing context mid-conversation.

Metadev's skills inject full SKILL.md every time. Caveman shows a way to inject a filtered slice based on runtime state, with a tiny per-turn reinforcement anchor. Relevant for skills that have modes/levels/profiles.

**D4 — Three-arm eval with "terse control"**

The cleanest benchmarking-a-skill pattern I've seen: don't compare skill-vs-nothing, compare skill-vs-"Answer concisely." The delta attributable to the skill itself (not just the terseness ask) is the honest number. `CLAUDE.md:186-188`:

> Honest delta = skill vs terse, not skill vs baseline. Baseline comparison conflates skill with generic terseness — that cheating. Harness designed to prevent this.

For metadev's benchmarks-first-class v2.0 direction, this is the pattern. Every skill's measurable claim must be measured against a credible control, not vs. no-op. Applicable far beyond caveman's token-compression claim — e.g., "does the `/plan` skill actually produce better plans than 'be thorough'?"

**D5 — Plugin manifest is almost empty; hooks do everything**

`.claude-plugin/plugin.json` is 34 lines total, most of it boilerplate. Two hook registrations point at `caveman-activate.js` and `caveman-mode-tracker.js`. All the actual skill logic lives in the SKILL.md (injected by the hook) and the JS files. The plugin manifest is a thin wiring layer. This separation (wiring vs content) is what makes the repo sync-able across IDEs — the "content" is plain markdown that any agent can consume.

## 4. Tiered recommendations for metadev-protocol

### USE AS-IS

- **`AGENTS.md` / `GEMINI.md` as `@import` stubs** — `AGENTS.md:1`. Metadev can ship 2-4 line stubs that re-export the real CLAUDE.md or skills directly. Zero-drift multi-LLM support for literally no cost.
- **Three-arm eval harness (baseline / terse / skill) with snapshot split** — `evals/llm_run.py` + `evals/measure.py`. Adopt the split: expensive LLM run writes JSON, cheap measure.py reads JSON offline. CI-safe, secret-free, reproducible.
- **`safeWriteFlag` / `readFlag` primitives** — `hooks/caveman-config.js:73-152`. If metadev ever ships a flag file (mode, session state, whatever), lift these two functions verbatim. The symlink-clobber attack surface is real and the fix is non-obvious.

### EXTRACT PARTS

- **`.github/workflows/sync-skill.yml`** — extract the fan-out pattern (one source → `.cursor/rules`, `.windsurf/rules`, `.clinerules`, `.github/copilot-instructions.md`, plus per-target frontmatter grafting). Metadev's `template/` is already the "source", so this workflow becomes: copy template CLAUDE.md + skills to per-IDE locations on release tag, with frontmatter injection per target.
- **Benchmarks runner pattern** — `benchmarks/run.py:184-202`. Lift: SHA256 the skill, commit results to git with hash, auto-patch README between `<!-- BENCHMARK-TABLE-START -->` markers. Enables replay-bisect of benchmark regressions.
- **CLAUDE.md ownership table** — `CLAUDE.md:26-54`. Metadev's existing `check_skills_contract.py` already enforces meta ↔ template parity, but putting the "source / generated" split in CLAUDE.md's body makes it visible to the agent at session start, not just at PR time.
- **Install script safe-JSON-merge via `node -e`** — `hooks/install.sh:128-190`. Passes paths via env vars (no shell injection), backs up to `.bak`, idempotent check before install. If metadev's adoption-mode script patches any user-owned JSON, clone this.

### BORROW CONCEPTS

- **Runtime skill-filter by mode** — `hooks/caveman-activate.js:53-91`. Concept: inject only the skill slice relevant to the current mode, not the full SKILL.md. For metadev, a hook could filter `/plan` SKILL.md by project profile (lite/standard/enterprise), or filter skills by currently-active feature flag. Needs a hook system on the target agent.
- **Two-file source model (behavior + activation)** — metadev skills today are one file each. Caveman splits "what the skill does" from "how the skill gets turned on" because the activation rule needs to be reshaped per-IDE (frontmatter varies) while the behavior stays constant. Metadev could adopt this split for its auto-trigger rules in CLAUDE.md's skill table.
- **Slash command `.toml` format as a "micro-skill"** — `commands/caveman.toml`. Description + prompt, two lines, `{{args}}` interpolation. Metadev's current skill format is heavy for simple parameterized prompts. Worth considering a micro-skill tier.
- **README as a product artifact with readability contract** — `CLAUDE.md:5-17`. Metadev's README is already decent but not explicitly governed by a "would non-programmer understand in 60 seconds" contract. Adding this to the CLAUDE.md rules for README changes is zero-cost high-value.

### INSPIRATION

- **The "why use many token when few do trick" voice** — not copyable (metadev has a different brand) but informs thinking about how much personality belongs in a template repo. Caveman's voice is consistent across README, CLAUDE.md, and skills, and it's part of the product. Metadev's voice is neutral-professional; there's room to be more opinionated without losing credibility.
- **Independent sub-skills with their own frontmatter** — `skills/caveman-commit` and `skills/caveman-review` are standalone skills that happen to ship in the same repo. Loose coupling at the filesystem level. Metadev already does this but could be more explicit about it.
- **CommonJS pin to defend against ESM contamination** — `hooks/package.json` with `{"type": "commonjs"}`. Relevant only if metadev ever ships JS hooks; informs thinking about defensive packaging in user-shared directories.

### REJECT

- **`caveman-compress` sub-project (Python compressor for CLAUDE.md files)** — interesting but orthogonal to metadev's mission. Compressing CLAUDE.md by rewriting prose into caveman-speak optimizes for a problem (token cost of every-session-load) that metadev solves differently (progressive disclosure, skill descriptions). Don't pursue.
- **Intensity levels (`lite` / `full` / `ultra` / `wenyan`)** — caveman's domain-specific feature. Metadev skills don't have meaningful "intensity" axes. The runtime filter pattern from D3 is worth borrowing conceptually, but not the levels themselves.
- **Plugin marketplace JSON files** (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`) — only relevant if metadev wants to publish as a Claude Code plugin. Not the current direction. Skip.
- **Wenyan (Classical Chinese) mode** — clever, but it's caveman-specific product differentiation. No metadev angle.

## 5. Open questions for follow-up

- **`npx skills` tool (`vercel-labs/skills`)** — referenced heavily as the 40+-agent distribution mechanism. Not part of this repo; it's the upstream tool that reads caveman's `skills/` directory and installs into arbitrary agent conventions. Worth a separate audit — this might be the actual infrastructure metadev wants to ride rather than re-implementing per-IDE fan-out.
- **How does Codex's hook system differ from Claude Code's?** `.codex/hooks.json` uses `"matcher": "startup|resume"` while Claude Code uses SessionStart events. Cross-reference against any Codex-specific audits in PM.15.
- **The plugin install idempotency pattern (`node -e` in shell)** — worth checking against the official Claude Code docs to see if there's an endorsed merge strategy.
- **How does caveman handle template versioning across the sync targets?** No semver tags visible in the shallow clone. If a user installs via `npx skills add` today and via `claude plugin install` tomorrow, are they guaranteed to get the same SKILL.md? Does the sync workflow ever race with a release tag?
- **Cross-check against other multi-agent repos in PM.15** — this is one data point. The fan-out + two-source-files + import-stubs pattern needs to be validated against at least one other primary source before committing metadev v2.0 to it.
