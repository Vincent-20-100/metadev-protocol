---
mode: deep
date: 2026-04-15
slug: deepagents
url: https://github.com/langchain-ai/deepagents
angle: agent harness architecture (planning, filesystem, subagent spawning)
status: active
---

# Deep — langchain-ai/deepagents

## 1. Fingerprint

- primary_lang: Python
- repo_type: library (pip-installable harness + examples)
- file_count: ~80 files in `libs/deepagents/` (source + tests + backends + middleware + profiles)
- license: MIT
- pitch: "Agents using an LLM to call tools in a loop fail at long horizons. Deep Agents adds the four things Claude Code / Deep Research / Manus have in common — planning tool, subagents, filesystem, detailed prompt — as a reusable harness."
- stars: 20k+
- explicit inspiration: "This project was primarily inspired by Claude Code, and initially was largely an attempt to see what made Claude Code general purpose."

## 2. Structure map

```
libs/deepagents/deepagents/
├── graph.py                # create_deep_agent — assembles full middleware stack
├── _models.py              # provider:model string resolution
├── backends/
│   ├── protocol.py         # BackendProtocol: ls/read/write/edit/glob/grep/execute
│   ├── state.py            # StateBackend (LangGraph state, ephemeral, default)
│   ├── filesystem.py       # FilesystemBackend (real disk)
│   ├── sandbox.py          # SandboxBackend (execute shell)
│   ├── store.py            # StoreBackend (LangGraph BaseStore, cross-thread)
│   ├── composite.py        # CompositeBackend (route paths to different backends)
│   └── local_shell.py
├── middleware/
│   ├── subagents.py        # SubAgentMiddleware + task tool + TASK_TOOL_DESCRIPTION
│   ├── async_subagents.py  # remote / background LangSmith-deployed subagents
│   ├── filesystem.py       # ls/read/write/edit/glob/grep tools wrapping backend
│   ├── skills.py           # load .md skills from backend paths
│   ├── memory.py           # AGENTS.md injection at startup
│   ├── summarization.py    # context-window compaction
│   ├── permissions.py      # FilesystemPermission rules, runs last
│   ├── patch_tool_calls.py
│   └── _tool_exclusion.py
└── profiles/
    ├── _harness_profiles.py  # per-provider overrides (tool descriptions, excluded tools)
    ├── _openai.py
    └── _openrouter.py
examples/deep_research/agent.py   # canonical usage (~60 LOC)
```

## 3. Key findings

### 3.1 Extension points (tools, mid-graph hooks)

Everything is a `AgentMiddleware` that wraps the model call. The middleware stack
is **ordered and layered**, and the graph is just `create_agent(model, tools, middleware=...)`
from langchain. Users inject middleware between a "base stack" and a "tail stack".

**graph.py:551-598**
```python
deepagent_middleware: list[AgentMiddleware[Any, Any, Any]] = [
    TodoListMiddleware(),
]
if skills is not None:
    deepagent_middleware.append(SkillsMiddleware(backend=backend, sources=skills))
deepagent_middleware.extend([
    FilesystemMiddleware(backend=backend, ...),
    SubAgentMiddleware(backend=backend, subagents=inline_subagents, ...),
    create_summarization_middleware(model, backend),
    PatchToolCallsMiddleware(),
])
if async_subagents:
    deepagent_middleware.append(AsyncSubAgentMiddleware(...))
if middleware:
    deepagent_middleware.extend(middleware)  # user injection point
# ... tail: profile middleware, prompt caching, memory, HITL, permissions (last)
```

Rationale: extension is **declarative stacking**, not subclassing or event hooks.
Each concern is a middleware; order is explicit and documented in the create_deep_agent
docstring. Permissions *always* last because they must see every tool injected by
earlier middleware.

### 3.2 Safety & governance

Permissions are a middleware that filters tool calls by rule, appended after
all tool-injecting middleware. Subagents inherit parent permissions unless they
declare their own (total replacement, not merge).

**graph.py:496-498**
```python
# Resolve permissions: subagent's own rules take priority, else inherit parent's
subagent_permissions = spec.get("permissions", permissions)
```

**graph.py:596-598**
```python
# _PermissionMiddleware must be last so it sees all tools from prior middleware
if permissions:
    deepagent_middleware.append(_PermissionMiddleware(rules=permissions, backend=backend))
```

Also: `HumanInTheLoopMiddleware(interrupt_on=...)` pauses the graph on specific
tool calls for human approval (requires a checkpointer). The repo also ships a
`THREAT_MODEL.md` which is notable for a library.

### 3.3 Documentation quality

- Docstrings in `create_deep_agent` explicitly document **full middleware ordering**
  (base stack → user middleware → tail stack) — readers see the architecture from
  the signature alone.
- `TASK_TOOL_DESCRIPTION` (subagents.py:191-299) is ~100 lines of in-context examples
  teaching the model *when* to spawn subagents: parallel research, single large
  repo analysis, refuse for trivial cases. This is prompt-as-documentation.
- Snapshot tests of the full rendered system prompt
  (`tests/unit_tests/smoke_tests/snapshots/system_prompt_*.md`) — docs and tests
  co-located, prompts treated as versioned artifacts.

### 3.4 Developer workflow

- `libs/` monorepo layout: `deepagents` core, `acp`, `cli`, `repl`, `partners`, `evals`.
- Profiles system (`profiles/_harness_profiles.py`) — per-provider overrides for
  tool descriptions, excluded tools, base prompt, extra middleware, system prompt
  suffix. Swapping models doesn't require re-authoring the harness.
- `evals/` subpackage exists alongside the library — evaluation is a first-class
  artifact, not an afterthought.

### 3.5 Distinctive patterns ⭐

**A. Task tool = subagent spawner with isolated context + single-message return**

**middleware/subagents.py:413-426**
```python
def task(
    description: str,
    subagent_type: str,
    runtime: ToolRuntime,
) -> str | Command:
    if subagent_type not in subagent_graphs:
        allowed_types = ", ".join([f"`{k}`" for k in subagent_graphs])
        return f"We cannot invoke subagent {subagent_type} because it does not exist..."
    if not runtime.tool_call_id:
        raise ValueError("Tool call ID is required for subagent invocation")
    subagent, subagent_state = _validate_and_prepare_state(subagent_type, description, runtime)
    result = subagent.invoke(subagent_state)
    return _return_command_with_state_update(result, runtime.tool_call_id)
```

**middleware/subagents.py:405-411**
```python
def _validate_and_prepare_state(subagent_type, description, runtime):
    subagent = subagent_graphs[subagent_type]
    # Create a new state dict to avoid mutating the original
    subagent_state = {k: v for k, v in runtime.state.items() if k not in _EXCLUDED_STATE_KEYS}
    subagent_state["messages"] = [HumanMessage(content=description)]
    return subagent, subagent_state
```

Rationale: subagents are **ephemeral, stateless, isolated-context**. The parent
state is filtered (`_EXCLUDED_STATE_KEYS = {"messages", "todos", "structured_response", "skills_metadata", "memory_contents"}`),
a fresh `HumanMessage` with just the task description is injected, the subagent
runs, and only the **last message's text** comes back as a `ToolMessage`. This
is the context-budgeting mechanism: multi-step reasoning happens inside the
subagent and collapses to one summary in the parent thread. Exactly Claude Code's
Task tool semantics, but expressed as ~30 LOC of pure Python around any
LangChain Runnable.

**B. Backend protocol — state, disk, sandbox, store, composite all behind one interface**

**backends/state.py:38-48**
```python
class StateBackend(BackendProtocol):
    """Backend that stores files in agent state (ephemeral).

    Uses LangGraph's state management and checkpointing. Files persist within
    a conversation thread but not across threads. State is automatically
    checkpointed after each agent step.
    """
```

`BackendProtocol` defines `ls/read/write/edit/glob/grep` (+ optional `execute`
for `SandboxBackendProtocol`). Swapping storage is a one-line change: `StateBackend()`
for ephemeral in-memory files, `FilesystemBackend(root_dir=...)` for real disk,
`StoreBackend` for cross-thread persistence, `CompositeBackend` to route path
prefixes to different backends (e.g., `/skills/` → disk, `/workspace/` → state).
Rationale: filesystem is *the abstraction* shared by every Claude Code-like
harness; making it swappable decouples "agent sees a filesystem" from "where
those bytes actually live". The sandbox variant even adds `execute(command)` so
code-running is the same interface.

**C. Declarative middleware stack as the harness definition**

**graph.py:443-473** (general-purpose subagent build)
```python
gp_middleware: list[AgentMiddleware[Any, Any, Any]] = [
    TodoListMiddleware(),
    FilesystemMiddleware(backend=backend, ...),
    create_summarization_middleware(model, backend),
    PatchToolCallsMiddleware(),
]
if skills is not None:
    gp_middleware.append(SkillsMiddleware(backend=backend, sources=skills))
gp_middleware.extend(_resolve_extra_middleware(_profile))
if _profile.excluded_tools:
    gp_middleware.append(_ToolExclusionMiddleware(excluded=_profile.excluded_tools))
gp_middleware.append(AnthropicPromptCachingMiddleware(unsupported_model_behavior="ignore"))
if permissions:
    gp_middleware.append(_PermissionMiddleware(rules=permissions, backend=backend))
```

Rationale: there is **no god-class "DeepAgent"**. The harness is an ordered list
of composable middlewares, and `create_deep_agent` is just a function that
builds that list. Each feature (todos, fs, subagents, skills, memory, summarization,
permissions, prompt caching) is a separate middleware module. To turn off
planning, drop `TodoListMiddleware`. To add a new cross-cutting concern, write
one middleware class.

**D. TASK tool description as few-shot curriculum**

**middleware/subagents.py:191-299** — the task tool's description is ~100 lines
with 5 worked examples teaching the model when to spawn subagents (parallel
LeBron/Jordan/Kobe research, single large-repo security analysis, parallel
meeting prep, **counter-example** for trivial pizza/burger/salad orders, and
custom-agent routing). Rationale: the harness trains the model's delegation
policy via the tool description itself — no external prompt engineering layer,
no policy file. Prompts are treated as code.

**E. Unconditional prompt caching, positioned before memory writes**

**graph.py:584-593**
```python
# Provider-specific middleware goes between user middleware and memory so
# that memory updates (which change the system prompt) don't invalidate the
# Anthropic prompt cache prefix.
deepagent_middleware.extend(_resolve_extra_middleware(_profile))
...
deepagent_middleware.append(AnthropicPromptCachingMiddleware(unsupported_model_behavior="ignore"))
if memory is not None:
    deepagent_middleware.append(MemoryMiddleware(backend=backend, sources=memory))
```

Rationale: the comment is the lesson. Cache invalidation order is load-bearing —
anything mutating the system prompt must come *after* caching is configured, or
you pay full prefix tokens on every turn. This is the kind of subtle ordering
knowledge that only surfaces after you've felt the pain.

## 4. Tiered recommendations for metadev-protocol

### USE AS-IS
(none) — deepagents is a runtime harness; metadev is a template generator. No direct code lift.

### EXTRACT PARTS
- **`_EXCLUDED_STATE_KEYS` + task-tool context filtering pattern** — if metadev ever ships a "subagent-within-skill" mechanism, this is the exact recipe for isolating context: fresh message list, filter parent state, collapse to last message. ~30 LOC.
- **`TASK_TOOL_DESCRIPTION` few-shot structure** — the 5-example + counter-example format is directly portable to metadev's `orchestrate` / `brainstorm` skill descriptions to teach Claude Code *when* to invoke them.
- **Snapshot tests of rendered system prompts** — `tests/unit_tests/smoke_tests/snapshots/` is a pattern metadev could adopt for its 10 skills: golden-file the final prompt each skill injects so accidental drift is caught.

### BORROW CONCEPTS
- **Ordered middleware stack as harness = declarative composition > monolithic agent class.** Metadev's "skills contract" already has this shape in spirit (trigger → skill → artifact). Making it explicit that each skill is a "middleware" that composes with others (ordering matters) is the v2.0 framing.
- **Backend protocol abstraction.** Metadev could define a minimal `ProjectBackend` protocol (read_artifact / write_artifact / list_artifacts / grep_artifacts) so that `.meta/` vs `drafts/` vs `active/` vs `archive/` is a routing concern, not a path-handling concern in every skill. Same shape as `CompositeBackend` routing by path prefix.
- **Harness profiles per provider.** Metadev has one CLAUDE.md contract assuming Claude Code. A `_HarnessProfile` equivalent (tool description overrides, excluded tools, base prompt, system prompt suffix) would let the template target Cursor / Cline / Codex without forking — PM.15's multi-IDE angle. See `profiles/_harness_profiles.py`.
- **Permissions middleware runs *last*.** Metadev's `check_skills_contract.py` enforces contract after the fact; a "governance runs last, sees everything" architectural rule is worth making explicit for future safety hooks.

### INSPIRATION
- **Prompts-as-code with snapshot diff gates.** The fact that `TASK_TOOL_DESCRIPTION` is a Python string literal versioned in git, snapshot-tested, and rendered into the model's tool catalog is the right ergonomic for metadev's skills. Treat every skill `SKILL.md` the same way: it IS the tool description the model sees; test it as such.
- **"Planning tool" = TodoListMiddleware.** The planning layer in deepagents is literally just a todo list the agent can read/write. Not a state machine, not a DAG — just a markdown-ish todo list as a first-class tool. Vindicates metadev's lightweight `.meta/active/plan-*.md` convention.
- **THREAT_MODEL.md in the repo.** Metadev should ship one for v2.0 (what skills can/cannot do, what an adversarial skill could exfiltrate, permission boundaries).
- **One monorepo, many packages.** `libs/deepagents`, `libs/acp`, `libs/cli`, `libs/evals`. Metadev's equivalent could be `template/`, `scripts/`, `evals/`, `contracts/` — evals as a first-class sibling, not a subfolder of scripts.

### REJECT
- **Full LangGraph/LangChain dependency.** Metadev targets Claude Code's native Task tool and its skill harness; adopting LangGraph state machines inside metadev would be a v2.0 → v3.0 rewrite for zero benefit over Claude Code's existing agent loop. The whole *point* of PM.15's question is answered: metadev does **not** need to build a harness — Claude Code already is one. What metadev needs is the **conceptual vocabulary** deepagents demonstrates (middleware ordering, context isolation, backend abstraction, profiles), expressed in metadev's existing template/skills idiom.
- **`create_deep_agent` as a function with 16 kwargs.** The god-function signature is the tax deepagents pays for being a library. Metadev doesn't need it — skills are discovered, not configured.
- **AsyncSubAgentMiddleware / LangSmith deployments.** Out of scope for a local-first project template.

## 5. Open questions

1. Is metadev v2.0's "harness" actually just a **CLAUDE.md + skills contract + trigger table** (which we already have), rephrased in middleware-ordering vocabulary? If yes, the PM.15 decision is: no new runtime, better conceptual framing + snapshot-tested skill descriptions.
2. Should metadev introduce a `ProjectBackend` abstraction to route `.meta/active/` vs `.meta/drafts/` vs `.meta/archive/` writes, the way `CompositeBackend` routes path prefixes? Or is that YAGNI for a template repo?
3. Is the `_HarnessProfile` pattern (per-provider overrides) the right shape for metadev's multi-IDE ambition (Cursor, Cline, Codex)? Could `template/.claude/` become `template/.agent/<profile>/` with profile-specific skill description overrides?
4. Should metadev ship snapshot tests of its 10 skills' rendered SKILL.md content (like deepagents' `system_prompt_*.md` snapshots), so prompt drift is caught in CI alongside the contract checker?
5. Threat model for a skills ecosystem — what does an adversarial skill look like, and what permission boundaries should v2.0 document?
