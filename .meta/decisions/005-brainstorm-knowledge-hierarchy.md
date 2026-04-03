# Raw ideas — Hierarchical knowledge system

> Capture of Vincent's ideas, 2026-04-01. To be brainstormed in depth later.
> NOT a decision — an input for the brainstorm.

---

## Idea 1: Skill /digest — Systematic information processing

**The problem:** When an agent does web research or parses a large document,
the result stays in the chat (volatile context) or in an unstructured raw file.

**The proposed rule:** As soon as an agent does research or parsing, it MUST
produce (or propose) a synthesis file. The work is returned AND memorized.

**Implications:**
- This is not just a skill, it is a **work convention** to put in CLAUDE.md
- The /digest skill automates the raw → gold transformation
- But the rule "always produce a synthesis" is broader than the skill

## Idea 2: Knowledge hierarchy with docstrings

**The problem:** An LLM arriving in a project must understand the general
context BEFORE diving into the details. Today it has to open and read
each file.

**The proposed solution:** Use docstrings/headers as "executive summaries"
at each level of the hierarchy:

```
.meta/gold/
├── INDEX.md                         ← Summary of ALL gold files (10-20 lines)
│                                       Read first, provides the map
├── skills-workflow-and-utilities.md ← Header = summary (5 lines)
│                                       Body = full detail
├── context-management.md           ← Header = summary (5 lines)
│                                       Body = full detail
└── ...
```

**The LLM reading flow:**
1. Reads INDEX.md (20 lines) → understands everything we know
2. Opens the relevant gold file → actionable detail
3. If needed, goes to the source in references/ → raw data

**This is progressive disclosure applied to documentation, not just to skills.**

## Idea 3: Mapping onto the 3 levels

| Level | Content | When to read | Equivalent |
|-------|---------|--------------|------------|
| **Map** (INDEX.md) | 1-2 lines per topic | Always | Skill description |
| **Gold** (gold/*.md) | Structured key takeaways | When working on the topic | Skill body |
| **Source** (references/*.md) | Raw data, URLs, citations | When you need proof | External documentation |

## Idea 4: File convention

Each .md file in gold/ and references/ starts with a standardized header:

```markdown
# Title

> SUMMARY: [1-2 sentences that convey the essence]
> SOURCES: [source files]
> DATE: [creation date]
> CONFIDENCE: [high/medium/low]
```

This header is what appears in INDEX.md. The LLM can scan
the headers without opening the files.

## Idea 5: Generalize to the template

This hierarchy is not just for metadev-protocol. It should be
in the GENERATED template:

```
.meta/
├── gold/           ← Actionable syntheses (the LLM reads this first)
│   └── INDEX.md    ← Map of everything we know
├── references/     ← Raw sources (the LLM goes here if needed)
├── decisions/      ← ADRs (why we chose)
├── sessions/       ← History
└── scratch/        ← Drafts (gitignored)
```

## Idea 6: Timestamp = truth (most recent wins)

**The problem:** If everything is saved, files can accumulate and contradict each other.
A gold file from January may say the opposite of a gold file from April.

**The proposed rule:** Each file is timestamped. In case of contradiction,
**the most recent takes precedence.** Simple, deterministic, no ambiguity.

**Implication for the standardized header:**
```markdown
> DATE: 2026-04-01
> SUPERSEDES: context-management-v1.md (if applicable)
```

## Idea 7: Knowledge base maintenance — Sorting and cleanup

**The problem:** If everything is saved, it becomes a dump. Sorting is needed.

**3 proposed sorting mechanisms:**

### A. Human-in-the-loop (most reliable)
- The human decides periodically: keep, archive, delete
- Skill /tidy that lists files by date, size, and asks "do we keep this?"
- Frequency: end of sprint or when .meta/ exceeds a threshold

### B. Dream Mode (automated, inspired by the leak)
- A process (skill or hook) that consolidates knowledge:
  - Merges overlapping files
  - Archives obsolete files (superseded)
  - Updates INDEX.md
- Equivalent of our /consolidate but for THE ENTIRE gold/references base
- Could be a skill /dream or /maintain

### C. Natural lifecycle (convention)
- references/ files have a limited lifespan
  - > 3 months without being cited by a gold file → archive candidate
- gold/ files are maintained as long as the topic is active
- decisions/ files are permanent (ADRs are never deleted)

**The 3 mechanisms are complementary, not mutually exclusive.**

## Idea 8: Knowledge file lifecycle

```
RESEARCH                     SYNTHESIS                   MAINTENANCE
   |                            |                            |
   v                            v                            v
references/raw.md  --/digest--> gold/synthesis.md  --/dream--> gold/synthesis-v2.md
   (bronze)                     (gold)                       (gold, updated)
                                  |
                                  v
                              INDEX.md (updated)
                                  |
                                  v
                          decisions/ADR-xxx.md (if decision made)
```

### The transitions:
1. **Research → Reference**: web/parsing agent, timestamped save
2. **Reference → Gold**: skill /digest, key takeaways extraction
3. **Gold → Gold v2**: skill /dream or /consolidate, merge/update
4. **Gold → Decision**: human validates, creates an ADR
5. **Reference → Archive**: /tidy or human-in-the-loop, obsolete file

### The transition rules:
- Ref → Gold: ALWAYS (no ref that stays without a synthesis)
- Stale gold (>3 months without update): flag for human review
- Contradictory gold: most recent wins, old one archived
- Decision: NEVER deleted, can be SUPERSEDED by a new one

## Open questions for the brainstorm

- Exact format of INDEX.md (table? list? sections?)
- How the /digest skill updates INDEX.md automatically
- Should CLAUDE.md point to INDEX.md ("read .meta/gold/INDEX.md")?
- Should sessions/ also have an INDEX?
- Volume threshold to trigger /tidy (number of files? total size?)
- Does /dream run automatically (SessionStart hook?) or manually?
- How to handle gold files that cover multiple domains?
- Should the generated template include empty gold/ and references/ directories
  or only create them on first use?
