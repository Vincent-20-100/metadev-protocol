# State of the Art: MCP (Model Context Protocol) Patterns

> Research compiled 2026-04-01. Reference material for metadev-protocol template design.

---

## 1. What is MCP and How It Works

### Overview

MCP (Model Context Protocol) is an open standard introduced by Anthropic in November 2024 to standardize how AI systems integrate with external tools, data sources, and APIs. Often called "the USB-C of AI," it provides a universal interface for tool discovery, execution, and context sharing.

In December 2025, Anthropic donated MCP to the **Agentic AI Foundation (AAIF)**, a directed fund under the Linux Foundation, co-founded by Anthropic, Block, and OpenAI. As of March 2026, the MCP SDK has reached **97 million monthly downloads**.

Sources:
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [MCP Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [MCP 2026 Roadmap](http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)

### Architecture: Host / Client / Server

MCP uses a **client-server architecture** over JSON-RPC 2.0:

| Component | Role |
|-----------|------|
| **Host** | User-facing app (Claude Code, Cursor, etc.) that owns the conversation and decides when to call tools |
| **Client** | Runs inside the host, manages connections to MCP servers, exposes their capabilities |
| **Server** | Implements tools, resources, and prompts; talks to external systems; returns structured results |

Each host starts one client per configured server. Clients connect, retrieve available capabilities, and relay tool calls from the model.

### Three Core Primitives

| Primitive | Purpose | Discovery | Execution |
|-----------|---------|-----------|-----------|
| **Tools** | Executable functions (file ops, API calls, DB queries) | `tools/list` | `tools/call` |
| **Resources** | Data sources that provide context (file contents, DB records) | `resources/list` | `resources/read` |
| **Prompts** | Reusable templates for structured LLM interactions | `prompts/list` | `prompts/get` |

### Transport Mechanisms

| Transport | Use case | Details |
|-----------|----------|---------|
| **stdio** | Local processes on same machine | No network overhead, optimal performance |
| **Streamable HTTP** | Remote servers, production deployments | TLS required, supports horizontal scaling |

Sources:
- [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [What is MCP (Descope)](https://www.descope.com/learn/post/mcp)
- [MCP Explained (Codilime)](https://codilime.com/blog/model-context-protocol-explained/)

---

## 2. Best MCP Servers for Python Development

### The "Three Server Sweet Spot" Rule

> Three servers is the sweet spot. Five is the max before token overhead hurts.
> Each server adds 500-1,000 tokens per tool to the context window.
> Five servers with 15 tools each = 50,000-75,000 tokens before you ask anything.

### Recommended Servers

| Server | Category | Why it matters |
|--------|----------|----------------|
| **GitHub MCP** | Code management | Full repo management, PRs, issues, code search -- zero-setup remote endpoint |
| **Context7** | Documentation | Solves stale docs hallucinations; fetches live library documentation |
| **Sentry MCP** | Error monitoring | Pull full issues with breadcrumbs and environment context |
| **Playwright MCP** | Browser automation | Accessibility snapshots, testing, UI verification |
| **Sequential Thinking** | Reasoning | Externalizes reasoning as explicit steps and branches |
| **E2B MCP** | Code execution | Secure cloud sandbox for running Python in isolated microVMs |
| **Supabase MCP** | Database | Manage entire backend through natural language |

### For Python Developers Specifically

| Server | Use case |
|--------|----------|
| **FastMCP** | Build custom MCP servers with decorator-based Python API |
| **Pipedream MCP** | Trigger serverless Python workflows |
| **PostgreSQL** | Direct database access and queries |

### Security Warning

> Over 20,000 MCP servers exist on public registries, but 66% of scanned servers had security findings.
> Stick to vendor-maintained servers (GitHub, Sentry, Figma) or AAIF reference servers.

Sources:
- [Best MCP Servers 2026 (Builder.io)](https://www.builder.io/blog/best-mcp-servers-2026)
- [10 Best MCP Servers (Firecrawl)](https://www.firecrawl.dev/blog/best-mcp-servers-for-developers)
- [6 Best MCP Servers for Python (Pythonic AF)](https://medium.com/pythonic-af/6-best-mcp-servers-tools-for-python-developers-4a3bac224961)
- [3 MCP Servers I Actually Use (Python Plain English)](https://python.plainenglish.io/3-mcp-servers-i-actually-use-as-a-python-developer-027c8cc0f610)

---

## 3. Configuring MCP Servers in Claude Code

### Three Configuration Scopes

| Scope | Storage | Shared? | Use case |
|-------|---------|---------|----------|
| **Local** (default) | `~/.claude.json` under project path | No | Personal dev servers, sensitive credentials |
| **Project** | `.mcp.json` in project root | Yes (committed) | Shared team servers |
| **User** | `~/.claude.json` global | No | Cross-project personal servers |

### CLI Commands

```bash
# Add a server (stdio transport)
claude mcp add github --scope user

# Add with inline JSON config
claude mcp add-json github '{"command":"npx","args":["-y","@modelcontextprotocol/server-github"],"env":{"GITHUB_PERSONAL_ACCESS_TOKEN":"'$GITHUB_TOKEN'"}}'

# Add with environment variables
claude mcp add my-server --env KEY=value --env SECRET=other

# List configured servers
claude mcp list

# Remove a server
claude mcp remove github
```

### Project-Level Configuration (`.mcp.json`)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server"],
      "env": {
        "SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}"
      }
    }
  }
}
```

### Team Pattern

Commit `.mcp.json` with shared server definitions. Each developer adds auth tokens via local-scoped entries in `~/.claude.json`. Server names stay consistent; credentials stay private.

### Enterprise / Managed

Administrators can deploy `managed-mcp.json` to system-wide directories with allowlist/denylist policies restricting which MCP servers are available.

### Startup Timeout

```bash
MCP_TIMEOUT=10000 claude  # 10-second timeout
```

### Verification

After config changes, restart Claude Code, then verify:
```bash
claude mcp list
# or inside a session:
/mcp
```

Sources:
- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
- [Configuring MCP in Claude Code (Scott Spence)](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)
- [Claude Code MCP Servers (Builder.io)](https://www.builder.io/blog/claude-code-mcp-servers)
- [MCPcat Setup Guide](https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code/)

---

## 4. Building Custom MCP Servers with Python

### When to Build Your Own

Build a custom MCP server when:
- You have internal tools/APIs not covered by existing servers
- You need project-specific tool orchestration
- You want to wrap legacy systems for AI access
- You need custom security or audit controls

Do NOT build when:
- A vendor-maintained server exists (prefer those for maintenance and security)
- The tool is simple enough for a Claude Code Skill or bash script
- You only need one-off access (use direct API calls instead)

### FastMCP: The Standard Framework

FastMCP 1.0 is part of the official MCP Python SDK. FastMCP 3.0 (released January 2026) adds component versioning, authorization, and OpenTelemetry.

**Requirements:** Python 3.10+ (3.12+ recommended)

**Setup:**
```bash
uv init my-mcp-server
uv add "mcp[cli]" httpx
```

### Minimal Server Example

```python
from fastmcp import FastMCP

mcp = FastMCP("My Project Tools")

@mcp.tool
def search_codebase(query: str, file_type: str = "py") -> str:
    """Search the codebase for a pattern in files of a given type."""
    import subprocess
    result = subprocess.run(
        ["rg", "--type", file_type, query],
        capture_output=True, text=True
    )
    return result.stdout or "No matches found."

@mcp.resource("project://config")
def get_project_config() -> str:
    """Return the project configuration."""
    with open("pyproject.toml") as f:
        return f.read()

@mcp.prompt
def review_prompt(file_path: str) -> str:
    """Generate a code review prompt for a file."""
    return f"Review the following file for bugs, style issues, and improvements: {file_path}"

if __name__ == "__main__":
    mcp.run()
```

### Key Patterns

| Pattern | When | Example |
|---------|------|---------|
| **Sync tools** | CPU-bound, fast operations | File parsing, calculations |
| **Async tools** | I/O-bound operations | API calls, database queries |
| **Resources** | Read-only data exposure | Config files, schemas, docs |
| **Prompts** | Reusable interaction templates | Review checklists, report formats |

### Async Tool Example

```python
@mcp.tool
async def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the project database."""
    async with aiosqlite.connect("project.db") as db:
        cursor = await db.execute(sql)
        rows = await cursor.fetchall()
        return json.dumps(rows)
```

### Testing and Debugging

```bash
# Built-in inspector (opens browser at http://127.0.0.1:6274)
fastmcp dev server.py

# Test with Claude Code
claude mcp add my-server --command "uv run server.py"
```

### Transport Options

| Transport | Config | Use case |
|-----------|--------|----------|
| **stdio** (default) | `mcp.run()` | Local development |
| **Streamable HTTP** | `mcp.run(transport="http")` | Remote/production |

Sources:
- [Build an MCP Server (Official)](https://modelcontextprotocol.io/docs/develop/build-server)
- [FastMCP Tutorial (Firecrawl)](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Building MCP Server (DataCamp)](https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp)

---

## 5. MCP vs Direct API Calls -- When to Use Which

### Decision Matrix

| Criterion | Use MCP | Use Direct API |
|-----------|---------|----------------|
| **AI agent workflows** | Yes -- natural discovery and multi-step reasoning | No |
| **Rapid prototyping** | Yes -- connect and go | No |
| **Multi-provider flexibility** | Yes -- same server works with Claude, GPT, Gemini | No |
| **Natural language interfaces** | Yes -- AI translates intent to tool calls | No |
| **High-performance / low-latency** | No | Yes -- less overhead |
| **Single-purpose automation** | No | Yes -- simpler, no discovery needed |
| **Bulk data operations** | No -- agents struggle with pagination | Yes |
| **Compliance-sensitive** | No -- AI interpretation introduces variability | Yes -- deterministic |
| **High-throughput pipelines** | No -- abstraction overhead | Yes |

### Key Insight

MCP does NOT replace APIs. MCP servers are **thin wrappers** around existing APIs that make them AI-friendly. Your API handles business logic; MCP provides the discovery and session layer on top.

### Token Cost Reality

- MCP adds a per-session overhead from tool descriptions in context
- For multi-step tasks, MCP is faster overall (persistent sessions, no repeated auth)
- For single calls, direct API is leaner

### The Complementary Architecture

```
User Request
    |
    v
AI Agent (Claude Code)
    |
    v
MCP Server (discovery + session + schema)
    |
    v
REST API (actual business logic)
    |
    v
Database / External Service
```

Sources:
- [MCP vs Direct API (Modelslab)](https://modelslab.com/blog/api/mcp-vs-direct-api-ai-integration)
- [MCP vs APIs (Tinybird)](https://www.tinybird.co/blog/mcp-vs-apis-when-to-use-which-for-ai-agent-development)
- [MCP vs APIs (freeCodeCamp)](https://www.freecodecamp.org/news/mcp-vs-apis-whats-the-real-difference/)
- [MCP vs API (Atlan)](https://atlan.com/know/when-to-use-mcp-vs-api/)

---

## 6. Real-World MCP Usage in Development Workflows

### Pattern 1: PR Review Pipeline

```
GitHub MCP (fetch PR diff + comments)
    --> Sequential Thinking MCP (analyze changes)
    --> GitHub MCP (post review comments)
```

### Pattern 2: Error Investigation

```
Sentry MCP (fetch error with stack trace)
    --> Claude Code (analyze root cause)
    --> GitHub MCP (create issue with fix proposal)
```

### Pattern 3: Database-Driven Development

```
PostgreSQL MCP (query schema + sample data)
    --> Claude Code (generate migration)
    --> E2B MCP (test migration in sandbox)
```

### Pattern 4: Documentation-Aware Coding

```
Context7 MCP (fetch latest library docs)
    --> Claude Code (generate code using current API)
    --> Playwright MCP (verify UI changes in browser)
```

---

## 7. Onyx (Pre-Indexation) vs MCP (Real-Time) Trade-Off

### Two Architectures for AI Data Access

| Dimension | MCP (Real-Time) | Onyx (Pre-Indexed) |
|-----------|-----------------|---------------------|
| **Approach** | Agent queries tools at request time | All sources indexed upfront (Slack, Drive, GitHub, Jira...) |
| **Indexation** | None required | 40+ connectors feed unified index |
| **Latency** | Variable (depends on external API) | Fast, predictable |
| **Freshness** | Real-time | Near-real-time (indexing lag) |
| **Reliability** | Depends on API availability | High (local index) |
| **Cross-source** | One query per source | Single query across all sources |
| **Setup cost** | Low (connect and go) | High (index management) |
| **Sovereignty** | Data flows through external APIs | Docker on own infra possible |
| **Model independence** | Server-agnostic | Compatible with Claude, GPT, Gemini, Llama |

### When to Use Which

| Scenario | Recommendation |
|----------|---------------|
| **Dev tools** (git, CI, error tracking) | MCP -- real-time data matters |
| **Knowledge base** (docs, wikis, Slack history) | Onyx-style indexation -- speed + cross-source search |
| **Hybrid** (most real projects) | MCP for tools, indexed search for knowledge |

### Implication for metadev-protocol

This trade-off is a recurring architectural decision. Consider adding an ADR template in `.meta/decisions/` for projects that need to choose between real-time MCP access and pre-indexed knowledge retrieval.

Source:
- [LinkedIn: MCP vs Onyx (Wilfried de Renty)](https://www.linkedin.com/in/wilfried-de-renty/) -- curated in `.meta/references/linkedin-curated-posts.md`

---

## 8. 2026 MCP Roadmap Highlights

| Priority | Timeline | Description |
|----------|----------|-------------|
| **Scalable transport** | Q1-Q2 2026 | Stateless sessions, load balancer compatibility, server metadata without connection |
| **Enterprise auth** | Q2 2026 | OAuth 2.1 with PKCE, SAML/OIDC for enterprise identity |
| **Agent-to-agent** | Q3 2026 | One agent calls another through MCP as if it were a tool server |
| **MCP Registry** | Q4 2026 | Curated, verified server directory with security audits and SLAs |

Source:
- [MCP 2026 Roadmap (Official)](http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [MCP Roadmap (The New Stack)](https://thenewstack.io/model-context-protocol-roadmap-2026/)

---

## 9. Actionable Patterns for metadev-protocol

### What to include in the template

1. **`.mcp.json` template** for project-level MCP config (profile-dependent)
   - `minimal`: no MCP config
   - `app`: GitHub MCP pre-configured
   - `data`: GitHub + database MCP
   - `quant`: GitHub + database + E2B sandbox

2. **CLAUDE.md guidance**: Add a section explaining available MCP servers and when to use `/mcp` to check status

3. **ADR template**: "MCP vs Direct API vs Pre-Indexed" decision record for data access architecture

4. **FastMCP skill**: A `.claude/skills/create-mcp-server/SKILL.md` that guides creating project-specific MCP servers

5. **Security rule**: Add to pre-commit or hooks -- never commit MCP auth tokens; always use env vars

### What NOT to do

- Do not pre-configure more than 3 MCP servers (token overhead)
- Do not build custom MCP servers for things Claude Code already does natively (file access, git, bash)
- Do not use MCP for bulk data pipelines or compliance-critical operations
