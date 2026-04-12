# Claude Code Source Leak Analysis

> Source: https://dev.to/gabrielanhaia/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-cjo
> Note: URL could not be fetched directly (403). Content reconstructed from web search indexes and cross-references.

## What Happened

On March 31, 2026, Anthropic accidentally published the entire source code of Claude Code inside an npm package. A missing `.npmignore` entry shipped a 59.8 MB source map (`cli.js.map`) containing 512,000 lines of unobfuscated TypeScript across roughly 1,900 files. Security researcher Chaofan Shou spotted the issue and posted the direct bucket link on X.

The Bun runtime (which Claude Code uses instead of Node) generates source maps by default. A Bun bug (oven-sh/bun#28001), filed on March 11, reports that source maps are served in production mode even when docs say they should be disabled. The `.npmignore` did not exclude the `.map` file.

Within hours, the code was mirrored, dissected, rewritten in Python and Rust. A clean-room rewrite hit 50,000 GitHub stars in two hours -- likely the fastest-growing repository in GitHub history.

## Architecture Overview

Claude Code v2.1.88 is a serious engineering artifact:
- 512,000 lines of TypeScript
- ~1,900 source files
- ~40 discrete, permission-gated tools (plugin-style architecture)
- Custom context compression system
- Multi-agent coordinator
- Feature flag infrastructure for 108+ gated modules

This is the "agentic harness" that wraps the underlying Claude model -- not model weights, but the orchestration layer that gives Claude the ability to use tools, manage files, run bash, and coordinate multi-agent workflows.

## Key Files

| File | Size | Role |
|------|------|------|
| `QueryEngine.ts` | ~46,000 lines | Core LLM API engine: streaming, tool loops, token tracking, prompt caching, retry logic |
| `bashSecurity.ts` | ~2,300+ lines | 23 numbered security checks for bash command validation |
| `coordinatorMode.ts` | — | Multi-agent orchestration (algorithm is a prompt, not code) |
| `undercover.ts` | ~90 lines | Strips Anthropic internals from external-facing outputs |
| `claude.ts` | — | Anti-distillation flags, core configuration |
| `promptCacheBreakDetection.ts` | — | Tracks 14 cache-break vectors with "sticky latches" |

## Tool System

Every capability (file read, bash execution, web fetch, LSP integration) is a discrete, permission-gated tool. The base tool definition alone is 29,000 lines of TypeScript. Read-only operations run concurrently; mutating operations run serially to avoid conflicts.

## Permission System

The bash permission system runs 25+ validators in a specific chain:
- Regex matching
- shell-quote parsing
- tree-sitter AST analysis
- 23 numbered security checks in `bashSecurity.ts`
- 18 blocked Zsh builtins
- Defense against Zsh equals expansion
- Unicode zero-width space injection detection
- IFS null-byte injection detection
- Malformed token bypass (found during HackerOne review)

Five-level settings cascade for permission configuration. An "auto" mode runs an LLM classifier on each action, racing multiple resolvers in parallel.

Critical detail: validators like `validateGitCommit` can return "allow" which bypasses ALL subsequent validators. The source contains explicit warnings: "validateGitCommit returns allow -> bashCommandIsSafe short-circuits -> validateRedirections NEVER runs -> ~/.bashrc overwritten".

## Context Compression / Compaction

Five compaction strategies:
1. **Micro compact** -- time-based clearing of old tool results
2. **Context collapse** -- summarizes spans of conversation
3. **Session memory** -- extracts key context to a file
4. **Full compact** -- complete context rewrite

Prompt cache economics drive much of the architecture. `promptCacheBreakDetection.ts` tracks 14 cache-break vectors with "sticky latches" that prevent mode toggles from busting the cache. One function is annotated `DANGEROUS_uncachedSystemPromptSection()`.

## Multi-Agent Patterns

Three distinct execution models for subagents:

1. **Fork model** -- Creates a byte-identical copy of the parent context. Hits the API's prompt cache. Running several in parallel costs roughly the same as running one sequentially.
2. **Teammate model** -- Communicates via file-based mailbox across terminal panes.
3. **Worktree model** -- Assigns each agent its own isolated git branch.

The orchestration algorithm in `coordinatorMode.ts` is a prompt, not code.

## Hidden / Unreleased Features

### KAIROS (Autonomous Daemon Mode)
Referenced 150+ times. An always-on background daemon where Claude operates as a persistent agent:
- Receives periodic `<tick>` prompts to decide whether to act proactively
- Maintains append-only daily log files
- Subscribes to GitHub webhooks
- Runs "dreaming" memory-consolidation during idle time

### autoDream (Memory Consolidation)
Located in `services/autoDream/`. A background memory consolidation engine running as a forked subagent:
- Merges disparate observations
- Removes logical contradictions
- Converts vague insights into absolute facts
- Gets read-only bash (can look at project, cannot modify)
- Runs in a fork to prevent main agent's "train of thought" from being corrupted by maintenance routines

### ULTRAPLAN
Offloads complex planning to a remote Cloud Container Runtime (CCR) session running Opus 4.6:
- Up to 30 minutes of dedicated think time
- Special sentinel value `__ULTRAPLAN_TELEPORT_LOCAL__` brings result back to local terminal
- Approved from browser

### Penguin Mode
Internal name for what users know as "Fast Mode":
- API endpoint: `/api/claude_code_penguin_mode`
- Kill-switch flag: `tengu_penguins_off`

### BUDDY (Terminal Pet)
18 species including capybara, with stats like DEBUGGING, PATIENCE, and CHAOS. Categories: common, uncommon, rare.

## Anti-Distillation Mechanisms

### Fake Tools
Flag `ANTI_DISTILLATION_CC` in `claude.ts` (line 301-313). When enabled, sends `anti_distillation: ['fake_tools']` in API requests. Server silently injects decoy tool definitions into the system prompt to pollute training data from API traffic recording. Gated behind GrowthBook feature flag `tengu_anti_distill_fake_tool_injection`, only active for first-party CLI sessions.

### Connector-Text Summarization
In `betas.ts` (lines 279-298). Server-side mechanism: API buffers assistant text between tool calls, summarizes it, returns summary with a cryptographic signature. On subsequent turns, original text can be restored from the signature.

## Undercover Mode
`utils/undercover.ts` (~90 lines). Prevents AI from revealing internal information in commits/PRs:
- Activates for Anthropic employees (`USER_TYPE === 'ant'`)
- Can force ON with `CLAUDE_CODE_UNDERCOVER=1`
- No force-off switch
- Strips Co-Authored-By attribution on external repos
- Blocks mention of internal codenames ("Capybara", "Tengu"), unreleased version numbers, internal Slack channels
- In external builds, entire function gets dead-code-eliminated to trivial returns
