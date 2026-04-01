# Claude Code Source Map Leak: Security Deep Dive

> Source: https://www.penligent.ai/hackinglabs/claude-code-source-map-leak-what-was-exposed-and-what-it-means/
> Note: URL could not be fetched directly (403). Content reconstructed from web search indexes and cross-references.

## The Packaging Failure

Version 2.1.88 of `@anthropic-ai/claude-code` shipped with a 59.8 MB JavaScript source map file (`cli.js.map`). This debugging artifact mapped minified production code back to the original TypeScript and pointed directly to a publicly accessible zip archive on Anthropic's own Cloudflare R2 storage bucket.

Root cause: Bun (Anthropic's acquired runtime) generates source maps by default. The `.npmignore` did not exclude the `.map` file. Post-build inspection happened against the source tree, not the final package artifact.

Anthropic's statement: "This was a release packaging issue caused by human error, not a security breach."

## Security Architecture Exposed

### Bash Security Pipeline (bashSecurity.ts)

Every bash command runs through 23 numbered security checks (~2,300+ lines):

- **Regex matching** for known dangerous patterns
- **shell-quote parsing** to decompose commands
- **tree-sitter AST analysis** for structural validation
- 18 blocked Zsh builtins
- Defense against Zsh equals expansion (`=command` form)
- Unicode zero-width space injection detection
- IFS null-byte injection detection
- Malformed token bypass (found during HackerOne review)

Critical short-circuit risk documented in source: certain validators (e.g., `validateGitCommit`) can return "allow" which bypasses ALL subsequent validators in the chain. The code contains explicit warnings about past exploitability of this pattern.

### Permission System Design

Five-level settings cascade controls all permissions. Each tool action goes through an "allow this action?" dialog -- a unit of friction the tool was designed to eliminate through:
- Pre-configured glob patterns
- An "auto" mode that runs an LLM classifier on each action
- Multiple resolvers racing in parallel

Read-only operations run concurrently. Mutating operations run serially.

### Four-Stage Context Management Pipeline

Attackers can now study and fuzz exactly how data flows through the pipeline rather than brute-forcing jailbreaks and prompt injections. The readable source reveals not just blocked patterns, but security comments explaining the threat model -- effectively mapping the boundary of what Anthropic has already considered and patched.

## Anti-Distillation Defenses

### Fake Tool Injection
`ANTI_DISTILLATION_CC` flag in `claude.ts`. When enabled, sends `anti_distillation: ['fake_tools']` in API requests. The server silently injects decoy tool definitions into the system prompt. Purpose: if someone records Claude Code's API traffic to train a competing model, fake tools pollute that training data.

- Gated behind GrowthBook feature flag: `tengu_anti_distill_fake_tool_injection`
- Only active for first-party CLI sessions

### Connector-Text Summarization
In `betas.ts` (lines 279-298). Server-side mechanism where the API buffers assistant text between tool calls, summarizes it, returns summary with a cryptographic signature. On subsequent turns, original text restorable from the signature. Prevents complete conversation replay for training.

## Undercover Mode (utils/undercover.ts)

~90 lines. System prompt injection that strips all traces of Anthropic internals when Claude Code is used in non-internal repos:

- Never mention internal codenames ("Capybara", "Tengu")
- Never mention internal Slack channels, repo names
- Never mention "Claude Code" itself
- Strip all `Co-Authored-By` attribution
- Force ON: `CLAUDE_CODE_UNDERCOVER=1`
- No force-off switch (one-way door)
- In external builds: entire function dead-code-eliminated to trivial returns
- Activates for Anthropic employees (`USER_TYPE === 'ant'`)

Implication: AI-authored commits and PRs from Anthropic employees in open source projects carry no indication that an AI wrote them.

## Supply Chain Attack (Concurrent Incident)

Users who installed or updated Claude Code via npm on March 31, 2026, between 00:21 and 03:29 UTC, may have pulled in a malicious version of axios (1.14.1 or 0.30.4) containing a Remote Access Trojan (RAT).

Indicators of compromise:
- Dependency `plain-crypto-js` in lockfile
- axios versions 1.14.1 or 0.30.4

If found: treat the host machine as fully compromised, rotate all secrets, clean OS reinstallation.

## Security Lessons

### For Package Publishers
- Post-build inspection must happen against the **final package**, not the source tree
- Teams often have linters that ban secrets in repos and CI jobs that scan Docker images, but far fewer inspect the exact tarball/zip that users consume
- A package can be "clean" in repo terms and still ship a disclosure path once build, upload, and mirroring are finished

### For AI Agent Security
- Claude Code's permission system, sandboxing mechanism, and security prompt design is the only fully exposed production-grade AI agent security implementation
- The feature flag names alone are more revealing than the code -- KAIROS, anti-distillation flags, model codenames are product strategy decisions competitors can now plan around
- "You can refactor code in a week. You cannot un-leak a roadmap."

### Attack Surface Expansion
- Malicious forks can repackage Claude Code with inserted backdoors, difficult to detect without binary hash verification
- MCP server supply chain attacks: publish a useful-looking server on npm that exfiltrates data with the same privilege as built-in tools
- Attack research cost collapsed overnight with the source now public

### Prompt Cache as Attack Surface
`promptCacheBreakDetection.ts` tracks 14 cache-break vectors. The cache economics drive architecture decisions -- "sticky latches" prevent mode toggles from busting the cache. Function `DANGEROUS_uncachedSystemPromptSection()` is explicitly annotated as dangerous. Cache-break manipulation could be a novel attack vector for manipulating agent behavior.
