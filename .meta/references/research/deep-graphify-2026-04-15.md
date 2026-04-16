---
mode: deep
date: 2026-04-15
slug: graphify
url: https://github.com/safishamsi/graphify
angle: multi-platform skill distribution + cache/confidence/surprise patterns
status: active
---

# Deep — safishamsi/graphify

## 1. Fingerprint

- **Repo:** safishamsi/graphify — 27k★ — PyPI package `graphifyy` v0.4.14
- **Pitch:** "AI coding assistant skill" that ships to **14 platforms** (Claude Code, Codex, OpenCode, Cursor, Gemini CLI, Copilot CLI, Aider, OpenClaw, Factory Droid, Trae, Trae CN, Hermes, Kiro, Google Antigravity), turning any folder of code/docs/papers/images/videos into a queryable knowledge graph.
- **Language:** Python ≥3.10, setuptools, no uv.
- **Stack:** tree-sitter (25 languages), NetworkX, Leiden community detection (graspologic), faster-whisper, optional MCP server, optional Neo4j.
- **Scope:** ~13 Python modules (`graphify/`) + 10 per-platform skill-\*.md files + 1 canonical skill.md.
- **Distinctive shape:** One Python package, 11 hand-tailored skill markdown files, one CLI dispatcher that reads a `_PLATFORM_CONFIG` dict and installs to the correct per-platform path with the correct per-platform "always-on" mechanism (hooks, rules, steering, plugins, AGENTS.md).

## 2. Structure map

```
graphify/
├── graphify/                # Python package
│   ├── __main__.py          # 1265 LOC CLI dispatcher + per-platform install logic
│   ├── skill.md             # canonical skill (1306 lines)
│   ├── skill-codex.md       # per-platform variants (differ in 20-50 lines)
│   ├── skill-aider.md
│   ├── skill-claw.md
│   ├── skill-copilot.md
│   ├── skill-droid.md
│   ├── skill-kiro.md
│   ├── skill-opencode.md
│   ├── skill-trae.md
│   ├── skill-windows.md
│   ├── cache.py             # SHA256 content-hash cache
│   ├── extract.py           # 3235 LOC multi-language AST extractor
│   ├── analyze.py           # surprise scoring, god nodes
│   ├── hooks.py             # git post-commit/post-checkout installer
│   ├── detect.py, build.py, cluster.py, report.py, export.py, ...
├── ARCHITECTURE.md          # 84 LOC pipeline doc
├── CHANGELOG.md             # 361 LOC
├── AGENTS.md                # 9 LOC — eats its own dogfood
├── README.md + README.zh-CN + README.ja-JP + README.ko-KR
├── pyproject.toml           # heavy baseline deps + 9 optional-dependency groups
└── worked/                  # sample corpora (httpx, karpathy-repos, mixed-corpus)
```

## 3. Key findings

### 3.1 Extension points

**Per-language extractor registry (lazy).** `graphify/extract.py:651-668` — `_extract_generic(path, config: LanguageConfig)` dynamically imports the tree-sitter language module at call time. Adding a language = adding a `LanguageConfig` entry, no top-level import. Missing module → graceful degradation with `{"error": f"{config.ts_module} not installed"}`.

```python
def _extract_generic(path: Path, config: LanguageConfig) -> dict:
    try:
        mod = importlib.import_module(config.ts_module)
        from tree_sitter import Language, Parser
        lang_fn = getattr(mod, config.ts_language_fn, None)
        ...
        language = Language(lang_fn())
    except ImportError:
        return {"nodes": [], "edges": [], "error": f"{config.ts_module} not installed"}
```

Rationale: 25 languages × tree-sitter = big import tax at startup. Config-driven + lazy module import turns each language into opt-in cost.

**Optional features as extras.** `pyproject.toml:44-53` — 9 named extras (`mcp`, `neo4j`, `pdf`, `watch`, `svg`, `leiden`, `office`, `video`, `all`). Pipeline branches check for import and degrade silently.

### 3.2 Safety & governance

**Shell-injection-safe hook script.** `graphify/hooks.py:11-38` — `_PYTHON_DETECT` parses the shebang of the `graphify` binary, then **allowlists** `[a-zA-Z0-9/_.-]` to prevent metacharacter injection before running it, and re-validates by importing `graphify`:

```sh
case "$GRAPHIFY_PYTHON" in
    *[!a-zA-Z0-9/_.-]*) GRAPHIFY_PYTHON="" ;;
esac
if [ -n "$GRAPHIFY_PYTHON" ] && ! "$GRAPHIFY_PYTHON" -c "import graphify" 2>/dev/null; then
    GRAPHIFY_PYTHON="";
fi
```

**Idempotent git-hook append.** `graphify/hooks.py:120-131` — `_install_hook` uses start/end markers (`# graphify-hook-start` / `# graphify-hook-end`) so it can append to existing user hooks without clobbering them, and `_uninstall_hook` regex-deletes only its own slice. Same pattern reused across platforms (`_CLAUDE_MD_MARKER`, `_GEMINI_MD_MARKER`, `_KIRO_STEERING_MARKER`, `_AGENTS_MD_MARKER`).

**Confidence tagging as first-class edge field.** `graphify/extract.py:697-707` — every `add_edge()` stamps `confidence: "EXTRACTED" | "INFERRED" | "AMBIGUOUS"` + `confidence_score: float`. No silent guessing: the AST extractor always emits `"EXTRACTED"` / `1.0`, LLM subagents emit lower tiers.

### 3.3 Documentation quality

- README is 4-language localized, heavy on concrete install one-liners per platform.
- `ARCHITECTURE.md` documents the pipeline as `detect → extract → build_graph → cluster → analyze → report → export` with a module/function/IO table. Every stage = one function in one file, communicates via dicts and NetworkX graph only. No side effects outside `graphify-out/`.
- `AGENTS.md` at repo root shows it *uses its own always-on mechanism on itself* — pure dogfood.
- `CHANGELOG.md` is 361 lines of honest, granular per-version notes.

### 3.4 Developer workflow

**Git-hook auto-rebuild.** `graphify/hooks.py:155-167` — `graphify hook install` wires a `post-commit` hook that reruns `_rebuild_code(Path("."))` (AST-only, no LLM cost) on each commit, and a `post-checkout` hook that rebuilds on branch switch **only if `graphify-out/` already exists**. Cost-aware.

**Content-hash cache with frontmatter-aware body hashing.** `graphify/cache.py:20-41` — `file_hash()` is SHA256 of `(body + \x00 + relative_path)`, where **body strips YAML frontmatter for `.md` files**. Result: metadata-only edits (e.g. `reviewed: true`, `tags: [x]`) do NOT invalidate the cache. Plus: relative path (not absolute) so the cache is portable across machines and CI checkouts.

```python
def file_hash(path: Path, root: Path = Path(".")) -> str:
    p = Path(path)
    raw = p.read_bytes()
    content = _body_content(raw) if p.suffix.lower() == ".md" else raw
    h = hashlib.sha256()
    h.update(content)
    h.update(b"\x00")
    try:
        rel = p.resolve().relative_to(Path(root).resolve())
        h.update(str(rel).encode())
    except ValueError:
        h.update(str(p.resolve()).encode())
    return h.hexdigest()
```

**Atomic-write with Windows fallback.** `cache.py:79-89` — writes `{hash}.tmp`, `os.replace()` → entry, and on Windows `PermissionError` falls back to copy-then-unlink. Small thing, real pain-avoidance.

### 3.5 Distinctive patterns ⭐

#### A. Multi-platform distribution from a single package (⭐ THE pattern)

`graphify/__main__.py:49-115` — a single Python dict `_PLATFORM_CONFIG` defines, per platform, which per-platform `skill-*.md` file to ship, which destination path under `$HOME`, and whether to also register in a `CLAUDE.md`:

```python
_PLATFORM_CONFIG: dict[str, dict] = {
    "claude":     {"skill_file": "skill.md",         "skill_dst": Path(".claude")/"skills"/"graphify"/"SKILL.md",     "claude_md": True},
    "codex":      {"skill_file": "skill-codex.md",   "skill_dst": Path(".agents")/"skills"/"graphify"/"SKILL.md",    "claude_md": False},
    "opencode":   {"skill_file": "skill-opencode.md","skill_dst": Path(".config")/"opencode"/"skills"/"graphify"/"SKILL.md"},
    "aider":      {"skill_file": "skill-aider.md",   "skill_dst": Path(".aider")/"graphify"/"SKILL.md"},
    "copilot":    {"skill_file": "skill-copilot.md", "skill_dst": Path(".copilot")/"skills"/"graphify"/"SKILL.md"},
    "claw":       {"skill_file": "skill-claw.md",    "skill_dst": Path(".openclaw")/"skills"/"graphify"/"SKILL.md"},
    "droid":      {"skill_file": "skill-droid.md",   "skill_dst": Path(".factory")/"skills"/"graphify"/"SKILL.md"},
    "trae":       {"skill_file": "skill-trae.md",    "skill_dst": Path(".trae")/"skills"/"graphify"/"SKILL.md"},
    "trae-cn":    {"skill_file": "skill-trae.md",    "skill_dst": Path(".trae-cn")/"skills"/"graphify"/"SKILL.md"},
    "hermes":     {"skill_file": "skill-claw.md",    "skill_dst": Path(".hermes")/"skills"/"graphify"/"SKILL.md"},
    "kiro":       {"skill_file": "skill-kiro.md",    "skill_dst": Path(".kiro")/"skills"/"graphify"/"SKILL.md"},
    "antigravity":{"skill_file": "skill.md",         "skill_dst": Path(".agent")/"skills"/"graphify"/"SKILL.md"},
    "windows":    {"skill_file": "skill-windows.md", "skill_dst": Path(".claude")/"skills"/"graphify"/"SKILL.md",    "claude_md": True},
}
```

Then `install(platform)` at `__main__.py:118-166` copies the source skill, stamps `.graphify_version` next to it (so `_check_skill_version` can warn on drift at `__main__.py:17-24`), optionally registers in `~/.claude/CLAUDE.md` via marker append. **Gemini, Cursor, and Antigravity are special-cased** because their always-on mechanism is different (see below).

This is NOT one skill with a template; it is **11 hand-maintained per-platform skill variants** (skill.md + 10 siblings, 1183–1306 lines each). The differences are small but load-bearing: different hook commands, different file-path conventions (`.graphify_python` location, `graphify-out/` vs `.graphify/`), platform-specific language ("Claude" vs "your AI assistant"), platform-specific caveats about parallel subagent support. Total: ~12k lines of skill markdown.

#### B. Per-platform "always-on" mechanism matrix

For each platform, the installer injects the graph reminder through whatever always-on primitive that platform offers. `__main__.py:26-38` (Claude PreToolUse hook), `:210-222` (Gemini BeforeTool hook), `:482-505` (Cursor rules with `alwaysApply: true`), `:521-575` (OpenCode `tool.execute.before` plugin), `:346-355` (Kiro steering with `inclusion: always`), `:409-449` (Antigravity `.agent/rules` + `.agent/workflows`), AGENTS.md for the rest (Aider, Claw, Droid, Trae, Hermes).

Example — Claude Code hook (`__main__.py:26-38`):

```python
_SETTINGS_HOOK = {
    "matcher": "Glob|Grep",
    "hooks": [{
        "type": "command",
        "command": (
            "[ -f graphify-out/graph.json ] && "
            r"""echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"graphify: Knowledge graph exists. Read graphify-out/GRAPH_REPORT.md for god nodes and community structure before searching raw files."}}' """
            "|| true"
        ),
    }],
}
```

Example — OpenCode JS plugin (`__main__.py:523-545`):

```js
export const GraphifyPlugin = async ({ directory }) => {
  let reminded = false;
  return {
    "tool.execute.before": async (input, output) => {
      if (reminded) return;
      if (!existsSync(join(directory, "graphify-out", "graph.json"))) return;
      if (input.tool === "bash") {
        output.args.command =
          'echo "[graphify] Knowledge graph available. Read graphify-out/GRAPH_REPORT.md..." && ' +
          output.args.command;
        reminded = true;
      }
    },
  };
};
```

The unifying abstraction: **"make the host inject a context string before file-search tool calls, whenever `graphify-out/graph.json` exists."** The implementation per platform is different, the behavior is identical.

#### C. Content-hash cache, Markdown body-only (validated)

Already flagged. `graphify/cache.py:10-41`. Confirmed and sharper than I remembered: the body-only trick for `.md` frontmatter means status/review metadata edits don't bust the cache. Relative paths for portability. Atomic writes with Windows fallback.

#### D. Confidence tagging (validated)

Already flagged. `extract.py:697-707` + 40+ call sites in extract.py. Every edge has `confidence ∈ {EXTRACTED, INFERRED, AMBIGUOUS}` plus a `confidence_score`. AST code always emits `EXTRACTED / 1.0`; LLM subagents are expected to downgrade. The confidence field is then **consumed** by the surprise scorer (see E) — so it's not just metadata, it drives behavior.

#### E. Surprise / novelty scoring (validated, richer than expected)

Already flagged but not fully understood. `graphify/analyze.py:131-184` — `_surprise_score()` is a composable additive scorer with 6 signals:

```python
def _surprise_score(G, u, v, data, node_community, u_source, v_source):
    score = 0; reasons = []
    # 1. Confidence weight
    conf = data.get("confidence", "EXTRACTED")
    score += {"AMBIGUOUS": 3, "INFERRED": 2, "EXTRACTED": 1}.get(conf, 1)
    # 2. Cross file-type (code↔paper)
    if _file_category(u_source) != _file_category(v_source): score += 2
    # 3. Cross-repo (top-level dir)
    if _top_level_dir(u_source) != _top_level_dir(v_source): score += 2
    # 4. Cross-community (Leiden structural distance)
    if cid_u != cid_v: score += 1
    # 4b. Semantic similarity multiplier
    if data.get("relation") == "semantically_similar_to": score = int(score * 1.5)
    # 5. Peripheral→hub (low degree reaching high degree)
    if min(deg_u, deg_v) <= 2 and max(deg_u, deg_v) >= 5: score += 1
    return score, reasons
```

Each signal contributes **both** a score bump and a human-readable reason string, accumulated into `reasons: list[str]`. The final output per surprising edge is `{score, reasons, ...}` — so users see not only WHAT surprised the scorer but WHY (e.g. "bridges separate communities", "peripheral node `X` unexpectedly reaches hub `Y`", "crosses file types (code ↔ paper)"). This is a tiny, readable, tunable scoring function — the kind I would have made a dense sklearn mess of.

#### F. Lazy per-language importlib (validated)

`extract.py:656` — already covered in 3.1.

#### G. Version-drift warning per install target

`__main__.py:17-24` — each install writes a `.graphify_version` next to the installed skill. On later `install` runs, `_check_skill_version` reads it and warns if it drifts from the currently-installed package version. Cheap mechanism to catch "I upgraded the pip package but forgot to re-install into Cursor/Codex/etc."

## 4. Tiered recommendations for metadev-protocol

### USE AS-IS (copy essentially unchanged)

- **SHA256 content-hash cache with body-only Markdown hashing** (`cache.py:20-41`). Drop into the template's `.meta/cache/` story for things like `/research`, `/audit-repo`, `/tech-watch` artifact dedup. The frontmatter-skip trick is especially good for our `.meta/references/` flow where we mutate `status:` and `reviewed:` front-matter fields all the time without changing the body.
- **Idempotent marker-append pattern for `CLAUDE.md` / `AGENTS.md`** (`hooks.py:120-131`). We already do this ad hoc; formalizing it as a `scripts/inject_section.py` helper would remove a lot of brittle code from `/audit-repo` and the adoption-mode story in memory (`project_adoption_mode`).
- **`.graphify_version` drift file** (`__main__.py:17-24`). We ship via copier with semver tags already; a stamp file per-installed artifact would let us detect "template vNEXT but your project's `.claude/skills/brainstorm/SKILL.md` is from vOLD" — directly answers a `copier update` pain we haven't solved.

### EXTRACT PARTS

- **`_PLATFORM_CONFIG` dict + single `install(platform)` dispatcher** (`__main__.py:49-166`). Extract the *shape* — one dict, per-platform path + per-platform source skill file + per-platform always-on mechanism flag — not their literal platforms. For v2.0 multi-IDE: metadev's version would be `{"claude-code": {...}, "cursor": {...}, "codex": {...}}` and copier would render per-platform skill files under `template/.claude/skills/<skill>/variants/`. Crucial insight: **do not try to templatize one file; keep N hand-maintained variants and a dispatcher.** A 3% copy-paste duplication cost buys 100% fidelity per host.
- **Surprise-score additive scoring shape** (`analyze.py:131-184`). Not for knowledge graphs — for `/audit-repo` deep-mode scoring. Today our audit cards ask the LLM to rank findings freeform; replacing that with a small `_priority_score(finding)` that adds points for "cross-domain reuse", "contradicts existing decision", "low-cost high-impact" — each with a reason string — would give us sortable, explainable findings without any additional LLM cost. This maps cleanly to the "max déterministe, LLM minimal" principle in our memory.
- **Shell-injection allowlist for hook scripts** (`hooks.py:20-27`). If we ever auto-install hooks into the child project's `.git/hooks/`, we need this exact allowlist trick. Worth bookmarking.

### BORROW CONCEPTS

- **"Always-on mechanism" as a named abstraction.** Graphify's architecture is: each host IDE exposes a primitive for "inject context before tool X"; graphify's job is to use whichever primitive that host offers. For metadev v2.0 multi-IDE, this is the right framing — don't chase feature parity between Cursor rules, Claude hooks, OpenCode plugins; define *what* metadev wants to inject and map it onto each host's nearest primitive.
- **Dogfood via `AGENTS.md` in the repo root.** Graphify's own AGENTS.md tells its own skill how to read graphify's own knowledge graph about itself. That matches our "this repo is recursive" rule in CLAUDE.md and validates the shape.
- **Honest audit trail as a first-class output.** The `EXTRACTED/INFERRED/AMBIGUOUS` tag pattern is exactly what `/research` and `/audit-repo` should enforce on their findings. We currently write "patterns" and "anti-patterns" flat; adding an explicit confidence tag per finding would make audit cards compose (and our synthesis runs sharper).
- **Per-platform skill variants with a base `skill.md`.** Validates the direction for PM.15: v2.0 should generate N per-IDE skill markdown files from a canonical source, with a test that diffs them for unintended drift.

### INSPIRATION

- **The "one skill, many platforms" marketing pitch.** Graphify's README leads with the platform matrix. If v2.0 ships multi-IDE, we should do the same: make the platform list the first thing users see in `template/README.md.jinja`.
- **Git hook for AST-only rebuild = "continuous graph integrity."** For metadev: a `post-commit` hook that runs `scripts/check_skills_contract.py` already exists in spirit. Graphify's `_rebuild_code` pattern — "LLM-free subset runs on every commit, full pipeline on demand" — is the right split for our contract check vs full `/audit-repo` rerun.
- **Pipeline as pure-function chain** (`ARCHITECTURE.md`): `detect → extract → build → cluster → analyze → report → export`, each stage = one function, one file, dict in / dict out. This is the architecture metadev's scripts should converge on. Our current scripts are more ad-hoc.

### REJECT

- **Hand-maintained 11× skill file variants at 1.2k lines each** (~12k lines). For graphify this is justified (25 languages, 14 platforms, billion-dollar compute cost per misfire). For metadev v2.0, hand-maintaining N skill variants per platform would be a maintenance disaster at our scale. **Take the dispatcher shape, not the file duplication.** We should generate per-platform variants from a Jinja base + per-platform overlay files.
- **Setuptools + no uv.** We already decided: uv exclusively. Graphify is on setuptools; we skip.
- **9 optional extras groups.** Our template is lean; we don't have the breadth to justify this. Good for reference, not for adoption.
- **Multi-language README (zh-CN, ja-JP, ko-KR).** Premature for us. Mentioned only because graphify's reach is interesting data.

## 5. Open questions

1. **Variant fidelity vs generation.** Graphify hand-maintains 11 skill files. Should metadev v2.0 (a) generate N files from one Jinja template + per-platform overlay, or (b) accept N hand-maintained variants with a drift-check script? Graphify picks (b). The right answer depends on how divergent the variants are — worth a debate. Leaning (a) for us because our skill count (10) × platform count (5–10) × ~500 lines = 25k–50k lines.
2. **What's the equivalent of `graphify-out/graph.json` for metadev?** Graphify's always-on mechanism checks for the existence of a build artifact before injecting context. metadev v2.0's equivalent would be... what? `.meta/active/*`? That might be the anchor: if any active artifact exists, the skill injects "read it first".
3. **Is the `confidence` tag worth adding to our `.meta/references/*.md` frontmatter?** Today our cards implicitly mix verified/inferred/speculative. Adopting `EXTRACTED / INFERRED / AMBIGUOUS` as a per-finding tag would make synthesis runs more honest. Small change, big compounding value if adopted early.
4. **Does metadev need a `post-commit` AST-only check?** Graphify reruns a cheap rebuild per commit. Our equivalent would be `check_skills_contract.py` + ruff — already essentially that shape. Does formalizing it as a mandatory post-commit hook (installed by copier) cross a line?
5. **Could we adopt graphify itself as a template dependency?** For projects that want codebase-aware Claude sessions out of the box — add `graphify install` as an opt-in post-gen hook in copier.yml. Would align with our `/audit-repo` story and give template users a day-one knowledge graph.
