---
mode: deep
date: 2026-04-15
slug: claude-mem
url: https://github.com/thedotmack/claude-mem
angle: memory architecture — 3-layer retrieval, FTS5+vector hybrid, private tags
status: active
---

# Deep — thedotmack/claude-mem

## 1. Fingerprint

- **Stack:** TypeScript / Bun runtime / `bun:sqlite` + ChromaDB (via chroma-mcp stdio) / Claude Agent SDK
- **Scope:** persistent cross-session memory plugin for Claude Code, Gemini CLI, OpenCode (multi-IDE)
- **Size:** ~680 files, `src/` organized into `cli/`, `services/`, `sdk/`, `servers/`, `supervisor/`, `hooks/`
- **License:** AGPL-3.0 (the `ragtime/` subdir is PolyForm Noncommercial)
- **Version:** 6.5.0 (README), 9+ DB migrations already shipped — mature, actively evolving
- **Distribution:** `npx claude-mem install`, plugin marketplace, `/plugin install`
- **Runtime model:** long-running local Worker HTTP service on port 37777 + web viewer UI + 6 lifecycle hooks

## 2. Structure map

```
src/
  cli/handlers/           # Hook event handlers: observation.ts, session-init.ts, context.ts, summarize.ts, user-message.ts, file-edit.ts, file-context.ts, session-complete.ts
  services/
    sqlite/               # SessionStore, SessionSearch, Observations, Summaries, Sessions, Import, Timeline, Prompts, PendingMessageStore
    sqlite/migrations.ts  # 9 migrations, FTS5 virtual tables, hierarchical memory fields, ROI column
    context/              # ContextBuilder, ObservationCompiler, TokenCalculator, sections/* renderers (Header/Timeline/Summary/Footer), formatters/Agent|Human
    sync/                 # ChromaSync.ts (843 lines), ChromaMcpManager.ts (stdio MCP client)
    worker/search/        # SearchOrchestrator + strategies/{Chroma,SQLite,Hybrid}SearchStrategy, TimelineBuilder, ResultFormatter
    worker/validation/    # PrivacyCheckValidator
    worker/session/       # SessionCompletionHandler
    queue/ transcripts/ smart-file-read/  # ancillary
  sdk/                    # parser.ts + prompts.ts — Claude Agent SDK "observer" prompts and XML output parser
  servers/mcp-server.ts   # MCP server exposing search/timeline/get_observations tools to Claude
  utils/tag-stripping.ts  # <private> / <system-reminder> / <claude-mem-context> edge-filter
plugin/
  hooks/hooks.json        # Claude Code lifecycle hook registrations (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd, Setup)
  skills/mem-search/      # The user-facing search skill with strict 3-layer workflow doctrine
  modes/                  # code, code--zh, code--ja — language/mode-specific observer prompts
```

## 3. Key findings

### 3.1 Extension points — memory capture hooks

**PostToolUse hook fires on every tool use and streams to a background worker.** The hook handler is a 79-line thin shim; all heavy lifting (privacy check, SDK extraction, storage) happens in the worker.

`src/cli/handlers/observation.ts:50-62`
```ts
// Send to worker - worker handles privacy check and database operations
const response = await workerHttpRequest('/api/sessions/observations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    contentSessionId: sessionId,
    platformSource,
    tool_name: toolName,
    tool_input: toolInput,
    tool_response: toolResponse,
    cwd
  })
});
```

**Rationale:** hooks are fast + idempotent; the persistent Bun worker (`http://localhost:37777`) buffers, synthesizes, and survives hook death. SessionStart / UserPromptSubmit / PostToolUse / Stop / SessionEnd — 5 lifecycle touchpoints, each with a dedicated handler in `src/cli/handlers/`.

**Background SDK agent as "observer".** A Claude Agent SDK instance runs in parallel with the main session and watches tool uses through structured XML observation prompts:

`src/sdk/prompts.ts:42-88`
```ts
export function buildInitPrompt(project, sessionId, userPrompt, mode) {
  return `${mode.prompts.system_identity}
<observed_from_primary_session>
  <user_request>${userPrompt}</user_request>
  ...
</observed_from_primary_session>
${mode.prompts.observer_role}
...
\`\`\`xml
<observation>
  <type>[ ${mode.observation_types.map(t => t.id).join(' | ')} ]</type>
  <title>...</title>
  <subtitle>...</subtitle>
  <facts><fact>...</fact></facts>
  <narrative>...</narrative>
  <concepts><concept>...</concept></concepts>
  <files_read>...</files_read>
  <files_modified>...</files_modified>
</observation>
```

The observer SDK agent is prompted to emit an XML block per meaningful tool event. Parsing happens in `src/sdk/parser.ts`. The observation schema is locked down: `type` (bugfix/feature/decision/discovery/change), `title`, `subtitle`, `facts[]`, `narrative`, `concepts[]`, `files_read[]`, `files_modified[]`. This is the **compression** step — raw tool outputs become structured hierarchical records.

### 3.2 Safety & governance — private tags, redaction

**Edge-filter pattern for `<private>` and system tags.** Filtering happens at the hook layer before anything reaches the worker or storage. A single regex sweep removes 5 tag families with ReDoS protection.

`src/utils/tag-stripping.ts:6-71`
```ts
/**
 * 1. <claude-mem-context> - System-level tag for auto-injected observations
 * 2. <private>            - User-level tag for manual privacy control
 * 3. <system_instruction> / <system-instruction>
 * 4. <system-reminder>    - Claude Code-injected system reminders
 * EDGE PROCESSING PATTERN: Filter at hook layer before sending to worker/storage.
 */
const MAX_TAG_COUNT = 100;  // ReDoS protection
function stripTagsInternal(content: string): string {
  return content
    .replace(/<claude-mem-context>[\s\S]*?<\/claude-mem-context>/g, '')
    .replace(/<private>[\s\S]*?<\/private>/g, '')
    .replace(/<system_instruction>[\s\S]*?<\/system_instruction>/g, '')
    .replace(/<system-instruction>[\s\S]*?<\/system-instruction>/g, '')
    .replace(/<persisted-output>[\s\S]*?<\/persisted-output>/g, '')
    .replace(SYSTEM_REMINDER_REGEX, '')
    .trim();
}
```

**Three governance ideas to steal:**
1. `<private>...</private>` — user-authored opt-out, zero config, reads naturally in prose.
2. `<claude-mem-context>...</claude-mem-context>` — system self-tag on injected context so the observer doesn't recursively ingest its own output. Solves the "observer observing itself" loop cleanly.
3. ReDoS cap (`MAX_TAG_COUNT = 100`) — tiny hardening against adversarial prompts.

A dedicated `PrivacyCheckValidator` also exists at `src/services/worker/validation/PrivacyCheckValidator.ts` for worker-side secondary scrubbing.

### 3.3 Documentation quality

- **README** is feature-rich, with a public docs site (`docs.claude-mem.ai`), 34 localized translations, and a clear "Quick Start" / "How It Works" / "MCP Search Tools" flow. 
- Architecture page series: Overview, Evolution v3→v5, Hooks, Worker Service, Database, Search Architecture.
- Per-directory `CLAUDE.md` files exist inside `src/`, `src/cli/`, `src/services/`, `src/services/domain/`, `src/services/sqlite/`, `plugin/`, etc. — this is *their* version of distributed session context for Claude Code to read on entry into a subtree. Very on-brand for this kind of repo, and consistent with the skill-vs-tool principle (don't fatten the root CLAUDE.md; push context where the work happens).
- `CHANGELOG.md` at root. Migration history in-source (`src/services/sqlite/migrations.ts`) doubles as an evolution log — each migration has a why-comment.

### 3.4 Developer workflow

- **Install:** `npx claude-mem install` or `/plugin install claude-mem`. Multi-IDE aware (`--ide gemini-cli`, `--ide opencode`). Bun and `uv` are auto-installed.
- **Config:** `~/.claude-mem/settings.json`, auto-created with defaults. `CLAUDE_MEM_MODE=code--zh` switches observer language + workflow mode. `CLAUDE_MEM_EXCLUDED_PROJECTS` project-filter.
- **Runtime:** worker HTTP API at `http://localhost:37777`, web viewer UI, 10 search endpoints, Bun process manager.
- **Query CLI:** via MCP (`search` / `timeline` / `get_observations`) from Claude, or REST from the viewer UI.
- **Bug reports:** `npm run bug-report` auto-generator.

### 3.5 Distinctive patterns ⭐

#### Pattern A — Hierarchical observation schema with dedicated FTS5 columns

Migration 002 adds structured fields that are *both* SQLite columns *and* FTS5 index columns. This gives you filter-by-column AND full-text-rank with one storage layer.

`src/services/sqlite/migrations.ts:136-156`
```ts
export const migration002: Migration = {
  version: 2,
  up: (db) => {
    db.run(`
      ALTER TABLE memories ADD COLUMN title TEXT;
      ALTER TABLE memories ADD COLUMN subtitle TEXT;
      ALTER TABLE memories ADD COLUMN facts TEXT;
      ALTER TABLE memories ADD COLUMN concepts TEXT;
      ALTER TABLE memories ADD COLUMN files_touched TEXT;
    `);
```

`src/services/sqlite/migrations.ts:388-426`
```ts
db.run(`
  CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(
    title, subtitle, narrative, text, facts, concepts,
    content='observations', content_rowid='id'
  );
`);
// + AFTER INSERT / DELETE / UPDATE triggers keep FTS table in sync
```

This is the level of table design metadev's "better memory" is missing today — right now we dump markdown blocks. Columnar + FTS5 trigger-maintained = queryable + fast.

#### Pattern B — 3-layer retrieval workflow enforced in the user-facing skill

The `mem-search` skill doesn't just expose tools — it **teaches** the token-efficient usage pattern and forbids shortcuts:

`plugin/skills/mem-search/SKILL.md:18-35`
```markdown
## 3-Layer Workflow (ALWAYS Follow)

**NEVER fetch full details without filtering first. 10x token savings.**

### Step 1: Search - Get Index with IDs
Use the `search` MCP tool:
    search(query="authentication", limit=20, project="my-project")
**Returns:** Table with IDs, timestamps, types, titles (~50-100 tokens/result)
...
### Step 3: Fetch - Get Full Details ONLY for Filtered IDs
**ALWAYS use `get_observations` for 2+ observations - single request vs N requests.**
```

The economics are declared in prose right in the skill (`~50-100 tok/result index` vs `~500-1000 tok/full observation` = 10× savings). This is the **progressive disclosure** pattern in practice: the skill *is* the retrieval protocol.

#### Pattern C — Hybrid search: metadata filter × semantic ranking × intersect × hydrate

Not a blind Chroma lookup — it runs a SQLite filter first, then uses Chroma only to *re-rank* those IDs, then hydrates back from SQLite in the semantic order.

`src/services/worker/search/strategies/HybridSearchStrategy.ts:64-103`
```ts
async findByConcept(concept, options) {
  // Step 1: SQLite metadata filter
  const metadataResults = this.sessionSearch.findByConcept(concept, filterOptions);
  if (metadataResults.length === 0) return this.emptyResult('hybrid');

  // Step 2: Chroma semantic ranking
  const ids = metadataResults.map(obs => obs.id);
  const chromaResults = await this.chromaSync.queryChroma(
    concept,
    Math.min(ids.length, SEARCH_CONSTANTS.CHROMA_BATCH_SIZE)
  );

  // Step 3: Intersect - keep only IDs from metadata, in Chroma rank order
  const rankedIds = this.intersectWithRanking(ids, chromaResults.ids);

  // Step 4: Hydrate in semantic rank order
  if (rankedIds.length > 0) {
    const observations = this.sessionStore.getObservationsByIds(rankedIds, { limit });
```

And the `SearchOrchestrator` formalizes the fallback tree: no-query → SQLite; with-query + Chroma → Chroma; Chroma fails → SQLite filter-only with `fellBack: true`.

`src/services/worker/search/SearchOrchestrator.ts:84-119`
```ts
// PATH 1: FILTER-ONLY (no query text) - Use SQLite
if (!options.query) { return await this.sqliteStrategy.search(options); }

// PATH 2: CHROMA SEMANTIC SEARCH
if (this.chromaStrategy) {
  const result = await this.chromaStrategy.search(options);
  if (result.usedChroma) return result;
  // Chroma failed - fall back to SQLite for filter-only
  const fallbackResult = await this.sqliteStrategy.search({ ...options, query: undefined });
  return { ...fallbackResult, fellBack: true };
}
```

#### Pattern D — Granular per-field vector embedding

Each observation does not become *one* vector — each semantic field (narrative, each fact, legacy text) becomes its own vector, sharing metadata. This means a search for "JWT expiration" can hit a single `fact` even if the full narrative is about something else.

`src/services/sync/ChromaSync.ts:156-184`
```ts
// Narrative as separate document
if (obs.narrative) {
  documents.push({
    id: `obs_${obs.id}_narrative`,
    document: obs.narrative,
    metadata: { ...baseMetadata, field_type: 'narrative' }
  });
}
// Each fact as separate document
facts.forEach((fact, index) => {
  documents.push({
    id: `obs_${obs.id}_fact_${index}`,
    document: fact,
    metadata: { ...baseMetadata, field_type: 'fact', fact_index: index }
  });
});
```

Trade-off: more vectors (cost) in exchange for precision. The `sqlite_id` is in every vector's metadata so you always re-hydrate from the authoritative SQL row. This is why their "10× savings" claim survives — vectors stay *small*, full payload lives in SQLite.

#### Pattern E — ROI/discovery tokens as first-class column

Migration 007 adds `discovery_tokens` to both observations and session_summaries. `TokenCalculator.calculateTokenEconomics` then reports `savings = discovery - read`, `savingsPercent`, shown in the injected context header. The system is *literally* accountable for its token value.

`src/services/sqlite/migrations.ts:491-509` + `src/services/context/TokenCalculator.ts:25-48`
```ts
// migration 007
db.run(`ALTER TABLE observations ADD COLUMN discovery_tokens INTEGER DEFAULT 0`);

// TokenCalculator
const savings = totalDiscoveryTokens - totalReadTokens;
const savingsPercent = totalDiscoveryTokens > 0
  ? Math.round((savings / totalDiscoveryTokens) * 100) : 0;
return { totalObservations, totalReadTokens, totalDiscoveryTokens, savings, savingsPercent };
```

Migration 008 adds `observation_feedback` table signalling semantic injection hits / search access / explicit retrieval — foundation for **Thompson Sampling**-based memory surfacing. Migration 009 adds `generated_by_model` + `relevance_count` for multi-model A/B. Signals: this project is moving toward *learned* memory surfacing, not just static retrieval.

## 4. Tiered recommendations for metadev-protocol

### USE AS-IS

Nothing — the stack gap is too large (TypeScript/Bun/Chroma/SDK agent vs Python/Copier/Claude Code markdown).

### EXTRACT PARTS

- **The `<private>...</private>` tag convention** — drop-in for the generated `CLAUDE.md.jinja` or `SESSION-CONTEXT.md.jinja`. Add a `strip_private_tags` helper to the save-progress skill. Zero dependency, huge UX win.
- **Per-subtree `CLAUDE.md` files** as a convention in generated projects: `src/{{slug}}/CLAUDE.md`, `tests/CLAUDE.md`. Progressive disclosure at the filesystem level, exactly matching our skill-vs-tool principle.
- **The 3-layer retrieval doctrine, prose form**, transplanted into our `/research` or a future `/memory` skill:
  "search → filter by ID → fetch full" even without any vector DB. Our current static memory already has the *data* (markdown blocks) — what's missing is the enforced usage protocol. This is a doc-level improvement, not code.

### BORROW CONCEPTS

- **Hierarchical observation schema** (title / subtitle / facts[] / narrative / concepts[] / files_read[] / files_modified[]). Whatever our v2.0 memory looks like, *stop storing freeform blocks*. Even in a markdown world, every memory entry should have these as YAML frontmatter so future tooling can parse them.
- **Hybrid search decision tree** (filter-first → semantic-rank → hydrate). If metadev ever ships a local SQLite memory index, use this architecture; do not do pure vector. Filter is cheap, vector is expensive, and filter cuts the candidate set by 100×.
- **Edge-filtering for governance**: all privacy/redaction happens at the hook boundary, before persistence. Never trust downstream layers. This matches our skill-vs-tool determinism principle.
- **ROI columns (`discovery_tokens`, `relevance_count`, `generated_by_model`)**: declare the value of each memory. We already flagged "context/reliability ratio matters" in user memory — this is the instrumented version. Even as static metadata, recording `generated_by` and `used_at` on memory entries lets `/save-progress` eventually do selection pressure.

### INSPIRATION

- **Background observer agent via SDK** → this is PM.15 territory. claude-mem runs a parallel Claude Agent SDK that watches the primary session. For metadev this is a v2.x stretch goal (cost/complexity): for now, take the *idea* that compression should happen in a separate process/context, not inline in the main session.
- **Worker HTTP service + web viewer at localhost:37777** → inspiration for a future metadev "dashboard" that shows session-context state live. Not a v2.0 must-have, but a nice long-term target.
- **Migration-as-evolution-log** — each `migration.ts` has a why-comment. Our `.meta/DECISIONS.md` should be cross-linked to schema / template-version bumps. Tag message = changelog rule already gestures at this.
- **Progressive skill teaching token economics in prose**: `mem-search` SKILL.md literally writes `~50-100 tok/result` vs `~500-1000 tok/full`. Our skills should advertise their own token cost in the description.

### REJECT

- **The full Worker/SDK/Chroma/FTS5 stack.** Wrong language, wrong runtime complexity for our use case. metadev is a Python template — we should not ship a Bun process manager.
- **The 34 README translations.** Cute, zero ROI for our audience.
- **Migration 005** (dropping streaming_sessions etc.) as a pattern — they thrash schema faster than external template users could follow. For metadev, additive-only schema, bigger semver bumps.
- **MCP-over-stdio Chroma integration** — fragile, Windows-unfriendly (they explicitly handle Bun-on-Windows FTS5 absence). We're Python, can use `sqlite-vec` or plain SQLite if we ever go there.

## 5. Open questions for follow-up

1. **Compression quality under load.** The observer SDK is prompted per-tool-use; what happens to rate / token cost after a long session with dozens of edits? Did they implement batching / deduplication in the worker? (Look: `src/services/worker/session/SessionCompletionHandler.ts`, `src/services/queue/`.)
2. **Cross-session linking.** How does `timeline` find the anchor when `query` is given instead of `anchor` ID? Is it FTS5, Chroma, or both? (Look: `src/services/worker/search/TimelineBuilder.ts`.)
3. **`observation_feedback` signals** — which hook fires on "injection hit" vs "explicit retrieval"? Can we replicate the feedback loop in a pure-markdown system by tagging which entries the next session actually *read* from?
4. **Endless Mode / biomimetic memory** — README mentions a beta. Where is the code? Is it a different strategy class or a full architectural fork?
5. **ROI measurement honesty.** `discovery_tokens - read_tokens` shows "savings" but doesn't account for the observer SDK's own token cost. Does the viewer UI expose that cost? This matters before metadev advertises similar numbers.
6. **Multi-IDE plugin abstraction.** How do Gemini CLI / OpenCode installers differ from Claude Code? (`src/cli/adapters/`, `install/` directories.) This is the multi-IDE piece of PM.15 sitting right there.
