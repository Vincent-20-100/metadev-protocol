# Claude Code Source Leak: Undercover Mode, Fake Tools, and Frustration Regexes

> Source: https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/
> Note: URL could not be fetched directly (403). Content reconstructed from web search indexes and cross-references.

## Context

Alex Kim's blog post is one of the primary detailed technical analyses of the Claude Code source leak. When security researcher Chaofan Shou noticed that Anthropic had shipped a `.map` file alongside their Claude Code npm package containing the full readable source code, the package was widely mirrored and picked apart on Hacker News. This was Anthropic's second accidental exposure in a week (the model spec leak was just days ago).

## Undercover Mode (utils/undercover.ts)

The most controversial discovery. Roughly 90 lines of code that inject a system prompt instructing Claude to:

- **Never mention that it is an AI** when operating on external repositories
- **Strip all `Co-Authored-By` attribution** when contributing to external repositories
- Never reference internal codenames like "Capybara" or "Tengu"
- Never mention internal Slack channels, internal repo names, or "Claude Code" itself
- Never mention unreleased version numbers

Activation rules:
- Activates for Anthropic employees (`USER_TYPE === 'ant'`)
- Can force ON with `CLAUDE_CODE_UNDERCOVER=1`
- **No force-off switch** -- if the system is not confident it is operating in an internal repo, it stays undercover
- In external builds, the entire function gets dead-code-eliminated to trivial returns (one-way door)

The implication: Anthropic employees use Claude Code to contribute to open-source projects, and the undercover mode ensures those contributions appear to be entirely human-authored with no AI attribution.

## Anti-Distillation: Fake Tools

In `claude.ts` (lines 301-313), a flag called `ANTI_DISTILLATION_CC`:

```
When enabled, Claude Code sends:
  anti_distillation: ['fake_tools']
in its API requests.
```

This tells the server to silently inject decoy tool definitions into the system prompt. If someone is recording Claude Code's API traffic to train a competing model, the fake tools pollute that training data with non-functional tool schemas.

- Gated behind GrowthBook feature flag: `tengu_anti_distill_fake_tool_injection`
- Only active for first-party CLI sessions

Second mechanism in `betas.ts` (lines 279-298): server-side connector-text summarization. The API buffers assistant text between tool calls, summarizes it, returns summary with a cryptographic signature. On subsequent turns, the original text can be restored from the signature. This prevents complete conversation replay for training purposes.

## KAIROS (Always-On Background Daemon)

Referenced over 150 times in the source. An unreleased autonomous daemon mode:

- Claude operates as a persistent, always-on background agent
- Receives periodic `<tick>` prompts to decide whether to act proactively
- Watches files and logs events
- Subscribes to GitHub webhooks
- Maintains append-only daily log files

## autoDream (Memory Consolidation)

Located in `services/autoDream/`. A background memory consolidation engine that runs as a forked subagent:

- Runs during idle time as part of KAIROS
- Merges disparate observations from the session
- Removes logical contradictions
- Converts vague insights into absolute facts
- Gets **read-only bash** -- can look at the project but not modify anything
- Runs in a separate fork to prevent the main agent's reasoning from being corrupted by maintenance routines
- Purely a memory consolidation pass, not an action-taking agent

## ULTRAPLAN

Offloads complex planning tasks to a remote Cloud Container Runtime (CCR):

- Runs Opus 4.6 with up to 30 minutes of dedicated think time
- Special sentinel value `__ULTRAPLAN_TELEPORT_LOCAL__` brings the result back to local terminal
- User approves the plan from their browser before it executes locally

## Multi-Agent Execution Models

Three distinct patterns discovered:

1. **Fork model** -- Byte-identical copy of parent context. Hits the API's prompt cache, so running several in parallel costs roughly the same as running one sequentially.
2. **Teammate model** -- File-based mailbox communication across terminal panes.
3. **Worktree model** -- Each agent gets its own isolated git branch.

The multi-agent coordinator (`coordinatorMode.ts`) is notable: the orchestration algorithm is a prompt, not imperative code.

## Penguin Mode

Internal name for what users know as "Fast Mode":
- API endpoint: `/api/claude_code_penguin_mode`
- Kill-switch flag: `tengu_penguins_off`

## BUDDY (Terminal Pet)

An easter egg / morale feature:
- 18 species including capybara, duck, goose, cat, octopus, owl, penguin, turtle, snail
- Rarity tiers: common, uncommon, rare
- Stats: DEBUGGING, PATIENCE, CHAOS
- Each pet has a different personality

## Architecture Insights

### Scale
- 512,000 lines of TypeScript
- ~1,900 source files
- ~40 discrete permission-gated tools
- 108+ feature flags via GrowthBook
- Base tool definition alone: 29,000 lines

### QueryEngine.ts (~46,000 lines)
Drives everything that touches the Anthropic API:
- Prompt construction
- Streaming response handling
- Token counting and cost tracking
- Prompt caching
- Retry logic for long-running agent sessions
- Multi-turn orchestration

### Context Compaction Strategies
Five levels:
1. **Micro compact** -- time-based clearing of old tool results
2. **Context collapse** -- summarizes spans of conversation
3. **Session memory** -- extracts key context to a file
4. **Full compact** -- complete context rewrite

`promptCacheBreakDetection.ts` tracks 14 cache-break vectors with "sticky latches" to prevent mode toggles from busting the prompt cache.

### Bash Security (bashSecurity.ts)
25+ validators in a chain:
- 23 numbered security checks
- Regex matching, shell-quote parsing, tree-sitter AST analysis
- 18 blocked Zsh builtins
- Defense against Zsh equals expansion, unicode zero-width space injection, IFS null-byte injection

## Strategic Impact

The feature flag names alone are more strategically revealing than the code itself. KAIROS, the anti-distillation flags, model codenames ("Capybara", "Tengu") -- these are product strategy decisions competitors can now plan around.

The irony: Anthropic built Undercover Mode specifically to prevent internal information from leaking into external contexts, then leaked everything through a `.npmignore` oversight.
