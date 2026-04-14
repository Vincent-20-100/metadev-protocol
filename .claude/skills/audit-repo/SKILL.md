---
name: audit-repo
description: Structural analysis of any GitHub repo — fingerprint, 5 categories, tiered recommendations
---

# /audit-repo

Usage: `/audit-repo <url>` or `/audit-repo <url> --angle <hint>`

Produces an audit report in `.meta/references/interim/`. Language/domain/framework-agnostic.

## Hard rules

- No modifications to the audited repo.
- No secrets in the output — redact credentials/tokens.
- Always write the output file, even on failure.
- Locked sections — never rename or skip.
- Every tier must appear — empty tiers get `(none)`.

## Two steps

### 1. Bootstrap (deterministic)

```bash
uv run python -m scripts.audit_repo <url> [--angle <hint>]
```

Script clones, fingerprints (language, type, stars, last commit, license, pitch,
file count), builds `tree -L 2`, cleans `/tmp/`, prints one JSON. If `gh` is
unavailable, stars/last_commit fall back to `"unknown"`. If JSON contains
`error: clone_failed`, use the failure template.

### 2. Analyze (LLM)

Read the JSON, then write
`.meta/references/interim/session-YYYY-MM-DD-audit-<slug>.md` with this schema
(sections locked, order fixed):

```
frontmatter: type: session / date / slug: audit-<slug> / status: active
# Audit — <owner/repo>    URL / Audited / Angle hint
## 1. Fingerprint
## 2. Structure map                (curated tree_output from JSON)
## 3. Key findings
   3.1 Extension points
   3.2 Safety & governance
   3.3 Documentation quality
   3.4 Developer workflow
   3.5 Distinctive patterns
## 4. Tiered recommendations
   USE AS-IS / EXTRACT PARTS / BORROW CONCEPTS / INSPIRATION / REJECT
## 5. Open questions for follow-up
```

Each finding: what / where (path:line) / why it matters. Each tier item: rationale.

## Failure handling

On `error: clone_failed`: section 1 `UNREACHABLE`, sections 2-5
`(clone failed: <reason>)`. Common reasons: private repo, 404, non-git URL.
