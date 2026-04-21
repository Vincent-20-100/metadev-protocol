# ADR-012 — Claude-only default, multi-host as opt-in capability

**Date:** 2026-04-21
**Status:** Accepted
**Supersedes:** partial reframing of ADR-011 (multi-host fan-out)
**Debate reference:** `.meta/debates/debate-2026-04-21-claude-only-mode-implementation.md`

## Context

v2.0.0 (ADR-011) introduced multi-LLM host coordination unconditionally. Every project generated from the template received:

- `AGENTS.md` (Codex stub)
- `GEMINI.md` (Gemini stub)
- `sync-config.yaml`
- `scripts/sync_hosts.py`
- Pre-commit hook `H008` (sync-hosts-check)
- CI workflow `.github/workflows/sync-hosts.yml`

This was a calculated bet on multi-LLM fan-out. Empirically (6 months later, projects egovault / T7 / Certification Masterclass), zero of these files have been read or edited post-generation by the primary user. The scaffolding was dormant in 100% of observed cases while adding onboarding surface area to every new project.

CLAUDE.md Rule 6 ("complexity must be justified") and the YAGNI doctrine were violated by speculative justification (future 3rd host).

## Decision

**Claude-only becomes the template's default.** Multi-host support becomes an opt-in capability activated by `--data enable_multi_host=true` at `copier copy` time.

Implementation:

- Single copier question `enable_multi_host: bool`, default `false`, `when: false` (no prompt at default `copier copy`).
- `_exclude` in `copier.yml` uses Jinja to gate the five multi-host artifacts on `enable_multi_host`.
- `template/.pre-commit-config.yaml` renamed to `.jinja` with the `sync-hosts-check` hook wrapped in `{% if enable_multi_host %}…{% endif %}`.
- The rule file `template/.claude/rules/multi-host.md` continues to ship **unconditionally** (see D4 clarification below).

No post-generation script, no sub-template fork, no two-step activation. Single `copier copy` invocation with one optional flag.

## D4 clarification (category distinction)

Debate D4 (2026-04-20) mandated that rule files ship unconditionally to avoid silent Jinja-gated doctrine. v2.0.0 over-applied this: shipping the *entire feature* (rule + stubs + script + hooks + workflow) unconditionally, not just the rule file.

**Correct interpretation of D4:**

| Artifact type | Shipping policy |
|---|---|
| Rule files (`.claude/rules/*.md`) | **Unconditional** — always present so doctrine is visible even to projects that will later opt in. |
| Feature artifacts (stubs, scripts, hooks, workflows) | **Conditional** on the relevant opt-in flag. |

This ADR formalizes the distinction. Future features should ship their rule file unconditionally and their artifacts conditionally.

## Consequences

### Positive
- New projects start minimal (Claude-only), matching the actual use pattern.
- Onboarding friction reduced: no "what is AGENTS.md?" question at first read.
- Template default state now honestly reflects what it endorses.
- Extensible: future hosts can reuse the `enable_multi_host` gate or introduce their own opt-in flag without re-running this debate.

### Negative / trade-offs
- Existing projects (egovault, T7, Certification Masterclass) that run `copier update` to v2.2.0 will have their `AGENTS.md` / `GEMINI.md` / `sync-config.yaml` / `scripts/sync_hosts.py` / `.github/workflows/sync-hosts.yml` removed unless they answer `enable_multi_host=true` during the update. Empirically (devil's advocate question, confirmed 2026-04-21): these files are not in use in any of the three projects, so removal is a service, not a regression.
- The migration footgun for *future* projects that did enable multi-host is real but narrow: the v2.2.0 tag annotated message must flag it.

### Neutral
- Schema stability: `enable_multi_host` becomes a permanent field in `copier.yml`. Removing it later would be a breaking change. This is acceptable — the field reflects a genuine axis of template variation.

## Rejected alternatives

| Option | Reason for rejection |
|---|---|
| Keep v2.0.0 status quo | YAGNI violation, dormant machinery in 100% of cases |
| 2 per-host bools (`enable_codex` + `enable_gemini`) | Premature extensibility; no evidence future hosts follow the stub pattern |
| Negative flag (`disable_multi_host`, default false) | Silent state-vs-contract regression on `copier update`; file lingers while flag says "no" |
| Post-generation activation script | Two sources of truth; copier update semantics break; unmaintainable test matrix |

## References

- Debate record: `.meta/debates/debate-2026-04-21-claude-only-mode-implementation.md`
- Superseded design intent from: ADR-011 (v2.0.0 multi-host fan-out)
- Devil's advocate empirical check: confirmed 2026-04-21 by user — AGENTS.md/GEMINI.md unused in last 6 months across egovault / T7 / Certification Masterclass
