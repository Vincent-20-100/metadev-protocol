---
type: session
date: 2026-04-13
slug: audit-agent-reach
status: active
---

# Audit — Panniantong/Agent-Reach

**URL:** https://github.com/Panniantong/Agent-Reach
**Audited:** 2026-04-13
**Angle hint:** web-research-patterns (feeds future `/survey` + `/radar` skills design)

## 1. Fingerprint

- **Primary language:** Python (>= 3.10, type hints)
- **Type:** agentic glue layer — CLI + Python library + MCP server + OpenClaw skill
- **Size:** ~60 files, ~2400 LOC (cli.py dominates at 1721 lines; channels are ~30 lines each)
- **Activity:** v1.3.0, active (commit dated 2026-04-13), MIT license
- **License:** MIT
- **One-line pitch:** "Give your AI agent eyes to see the entire internet — unified access to 17 platforms (Twitter, Reddit, YouTube, GitHub, HN via RSS, Bilibili, XHS, LinkedIn, RSS, arbitrary web) via one install, zero API fees."

**Critical positioning quote** (`CLAUDE.md`):
> "Agent Reach is a **glue layer** — only route and call, don't reimagine. NOT a wrapper — after install, agents call upstream tools directly."

This is the single most important insight of the whole repo.

## 2. Structure map

```
agent_reach/
├── cli.py                    # 1721 LOC — argparse entry, all CLI subcommands
├── core.py                   # 42 LOC — thin AgentReach class, just doctor()
├── config.py                 # config management (YAML + env)
├── doctor.py                 # diagnostics engine
├── channels/
│   ├── base.py               # Channel ABC: can_handle(url), check(), tier
│   ├── github.py             # 32 LOC — `gh` CLI detection
│   ├── twitter.py, reddit.py, youtube.py, rss.py, web.py, exa_search.py
│   └── [12 more platforms — one file each]
├── skill/
│   ├── SKILL.md              # routing table → references/
│   └── references/
│       ├── search.md         # Exa AI
│       ├── dev.md            # GitHub CLI commands
│       ├── web.md            # Jina Reader, RSS, WeChat
│       ├── social.md         # Twitter, Reddit, etc.
│       └── [career, video]
├── integrations/mcp_server.py
└── guides/                   # setup-exa.md, setup-groq.md, setup-reddit.md, etc.
config/mcporter.json          # MCP tool config
llms.txt                      # LLM-oriented index
```

## 3. Key findings per category

### 3.1 Extension points

- **What:** `Channel` ABC with a 4-field contract — `name`, `description`, `backends`, `tier` + methods `can_handle(url)` and `check(config)`.
- **Where:** `agent_reach/channels/base.py:17-36`
- **Why it matters:** A new platform = one new file, ~30 lines. Zero touching the core. This is the cleanest "source pluggability" pattern I've seen for agentic research tools. Directly relevant to our "sources paramétrables par projet" requirement.

- **What:** `tier: int = 0|1|2` field classifying config complexity.
  - tier 0 = zero-config (gh, jina, feedparser)
  - tier 1 = needs free API key (Exa, Groq)
  - tier 2 = needs setup (cookies, login, proxies)
- **Where:** `channels/base.py:29`
- **Why it matters:** Lets the doctor surface "here's what works for free right now" vs "here's what's locked behind config". For our V1 we want tier 0 only, and this field makes that filter trivial.

- **What:** OpenClaw skill with progressive disclosure — `SKILL.md` holds a routing table, category-specific commands live in `references/<category>.md`, loaded only when that category matches.
- **Where:** `agent_reach/skill/SKILL.md:1-106`
- **Why it matters:** **This is the exact 3-layer progressive disclosure pattern I sketched for our KB.** Except it's applied to skills, not data. We should use it for BOTH. See INSPIRATION below.

### 3.2 Safety & governance

- Pre-commit: `.gitignore` exists but no `.pre-commit-config.yaml`. Weak on this axis.
- CI: single workflow `.github/workflows/pytest.yml` (not inspected in detail).
- `CONTRIBUTING.md` exists, `SECURITY.md` does not.
- **Auth surface:** cookie-based (Twitter, XHS) with Cookie-Editor export requirement — they explicitly forbid QR-login as "will hang". Useful war story.
- No secret scanning; `.env.example` is clean but no pattern enforcement.
- **Verdict:** not a safety reference. We keep our own `audit_public_safety.py` pattern.

### 3.3 Documentation quality

- **README:** 394 lines, quickstart + examples + feature matrix. Good.
- **llms.txt:** 32 lines, LLM-targeted index. **Interesting convention I didn't know about** — a stripped-down entry point specifically for LLM consumption, complementing README.
- **CLAUDE.md:** 44 lines, very tight, includes the "glue layer, not wrapper" positioning rule. Excellent density.
- **guides/:** one per tier-1/tier-2 channel (`setup-exa.md`, `setup-reddit.md`, `setup-twitter.md`…) — decoupled from SKILL.md so the skill context stays small.
- **ADRs:** none visible.
- **Docstrings:** thin but present, type hints everywhere.

### 3.4 Developer workflow

- `pyproject.toml` + `uv.lock` + `constraints.txt` (pip constraint file for upstream tools).
- Test runner: `pytest` with `tests/test_cli.py` and `test.sh` integration script (venv + install + doctor).
- No ruff, no mypy in CI (visible from workflow name).
- `test.sh` creates a throwaway venv — same idea as our `copier copy /tmp/test-proj` smoke test. **Validates that our pattern is normal for Python CLI projects.**
- Version pinned in three places (`pyproject.toml`, `__init__.py`, `tests/test_cli.py`) — they explicitly flag this as a trap. For us: keep it in one place.

### 3.5 Distinctive patterns

- **"Glue layer" philosophy.** Agent-Reach does not wrap upstream tools. After install, the agent calls `gh`, `yt-dlp`, `curl r.jina.ai`, `rdt`, `twitter` directly. Agent-Reach only (a) installs/detects them and (b) routes URLs to the right tool via `can_handle`. `core.py` is **42 lines total**. This is an inversion of the usual "wrapper for everything" trap.
- **Doctor as the main UX.** `agent-reach doctor` runs `check()` on every channel and reports `ok/warn/off/error`. Half the library's value is "does this channel work right now on my machine" rather than the channels themselves.
- **Jina Reader as the universal web fallback** (`curl https://r.jina.ai/<URL>`). Zero-config, works on most pages. Used as the default for anything not routed to a specific channel. Very powerful idea — free, no key, LLM-formatted markdown output.
- **Exa as the zero-effort premium search.** `mcporter call exa.web_search_exa(...)` — a single MCP call replaces the whole "serp+scrape+dedupe" pipeline most research tools rewrite.
- **`llms.txt` convention.** Separate from README, specifically for LLM navigation. Worth adopting ourselves.

## 4. Tiered recommendations

### USE AS-IS
- **`Channel` ABC pattern** (`channels/base.py`) — copy the 4-field + 2-method contract verbatim, rename to `Source` for our domain. Zero adaptation needed; it is already minimal.
- **`tier: int` config-complexity field** — copy the 0/1/2 convention directly into our Source class. Lets `/survey doctor` surface what works zero-config.
- **Jina Reader as default generic-web backend** (`curl https://r.jina.ai/<URL>`) — no install, no key, LLM-ready markdown. Use it in our `/survey` + `/radar` for any URL not matched by a specific source.

### EXTRACT PARTS
- **SKILL.md routing table + `references/<category>.md` pattern** — take the 2-layer skill structure (index in SKILL.md, details in references/). This IS the progressive disclosure we need, applied to skill content instead of KB content. Extract the layout, not the Chinese categories.
- **`llms.txt` file** — extract the format. 30-line LLM-oriented index, separate from README. Good lightweight convention for making our repo legible to external LLMs running `/audit-repo` on us.
- **`guides/setup-<channel>.md` split from SKILL.md** — take the idea: keep per-source setup docs OUT of the main skill context so the skill stays small. Load on-demand when the source is being configured for the first time.

### BORROW CONCEPTS
- **"Glue layer, not wrapper" philosophy.** For our `/survey` + `/radar`: do NOT reimplement search/scrape logic. Call `gh search repos`, `curl r.jina.ai`, `feedparser`, `hf_hub_list`, `mcporter call exa...` directly. Our skill is routing + persistence + synthesis, not platform integration. This single principle probably saves us a 500-LOC detour.
- **Doctor-as-UX.** Our `/survey` and `/radar` should each ship with a `doctor` subcommand that reports which sources are ready (tier 0), which need keys (tier 1), which need setup (tier 2). Makes first-run discoverability trivial: "here's what you can use right now".
- **Config-complexity tier as filter.** When the user runs `/survey` without specifying sources, default to tier-0-only. Opt into tier-1/2 explicitly. Keeps the happy path fast.
- **One-file-per-source module layout** (`sources/github.py`, `sources/reddit.py`, `sources/hf.py`…) — mirror Agent-Reach's `channels/` directory.

### INSPIRATION
- **Exa MCP for code/web search.** If Vincent already uses MCP in other projects, wiring `exa.web_search_exa` and `exa.get_code_context_exa` as a tier-1 source in `/survey` is trivial and gives us paper-grade web search without our own infra. Not V1 blocking, but an obvious V1.1.
- **Cookie-based auth war stories.** Their "QR login will hang, use Cookie-Editor export" note is the kind of hard-won knowledge we should capture in our own `guides/` when we hit similar traps (Reddit rate limits, X API walls).
- **Finance channel (xueqiu)** — not directly relevant, but signals that Agent-Reach's channel pattern scales to non-tech domains. Reinforces confidence in the architecture.

### REJECT
- **OpenClaw-specific skill metadata** (`triggers:` block with Chinese keywords, `openclaw:` homepage field) — specific to their skill loader format, not Claude Code's. We use Claude Code's SKILL.md format which already has triggers via the `Skill` tool.
- **Chinese-market channels** (xiaohongshu, douyin, weibo, bilibili, v2ex, wechat, xiaoyuzhou) — not our use case. Reject wholesale. Keeps our source catalogue focused on EN-speaking tech ecosystem (GitHub, HF, Reddit, X, HN, arXiv).
- **MCP server packaging** (`integrations/mcp_server.py`) — overhead we don't need in V1. Our skill runs inside Claude Code, we don't need to expose ourselves as an MCP server to other agents. Revisit if Nightshift needs it.
- **1700-line `cli.py`.** Monolithic argparse file. Anti-pattern for us — if we ship a CLI, split commands per file.
- **Three-place version pinning.** Explicit anti-pattern they flag themselves. We keep version in one place.

## 5. Open questions for follow-up

- Does Agent-Reach handle **rate limiting** across sources? Didn't see a shared rate-limit pool — each channel probably lets the upstream tool fail. Need to decide our policy (retry? fail fast? per-source cool-down?) before shipping `/radar` which will poll frequently.
- What's the actual **output format** of each channel's read/search? Agent-Reach documents commands but doesn't impose a schema — each upstream tool returns its own format. For our KB we need a normalized schema across sources. **This is a design decision we must make in the brainstorm.**
- How does Agent-Reach handle **dedup across sources** (same repo mentioned on Reddit + X + GitHub trending)? Doesn't appear to — it's a router, not an aggregator. Our `/survey` + `/radar` will need dedup that Agent-Reach does not provide. We're on our own here.
- Is there a **cost/quality comparison** between Jina Reader free and Exa tier-1? The docs say Jina is "good enough for most pages" but Exa for "technical/English". We should benchmark on our actual use cases before deciding which to make default.

## 6. Metadata

- **Clone command used:** `git clone --depth=1 --filter=blob:none https://github.com/Panniantong/Agent-Reach /tmp/audit-agent-reach/`
- **Files read:** `README.md`, `CLAUDE.md`, `llms.txt`, `agent_reach/core.py`, `agent_reach/channels/base.py`, `agent_reach/channels/github.py`, `agent_reach/skill/SKILL.md`, `agent_reach/skill/references/search.md`, `agent_reach/skill/references/dev.md`, `agent_reach/skill/references/web.md`, `pyproject.toml` (listing only)
- **Audit duration:** ~8 min
