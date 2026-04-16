# Debate Record — PreToolUse gate hook on .meta/references/

**Date:** 2026-04-16
**Preset:** architecture
**Mode:** standard
**Context:** hybrid (2 insiders + 1 lone wolf)
**Wolf:** Agent C (Minimaliste)
**Status:** USER DECISION NEEDED

---

## Subject

The v2.0 spec proposes a PreToolUse hook that blocks Read calls on `.meta/references/` to force usage of the librarian agent. Should this be: hard block (exit 1), soft warning (print + exit 0), or no gate at all (CLAUDE.md convention only)?

Tension: deterministic enforcement vs workflow flexibility vs user/agent friction vs template multiplier cost.

## Angles

- **A (Enforcer):** hard block (exit 1) — conventions drift, ghost features prove it, this is the same pattern as check_skills_contract.py [insider]
- **B (Pragmatiste):** soft warning (print + exit 0) — educate without breaking, avoid hidden workarounds, escalate only with data [insider]
- **C (Minimaliste):** no hook — CLAUDE.md convention is sufficient, hooks are wrong-layer for probabilistic actors, template multiplier problem [lone wolf]

## Strong arguments (survived cross-critique)

- **Ghost features are empirical evidence** — raised by A, conceded by all 3. PM.15 found 4 orphan trigger rows despite existing conventions. Soft rules failed in this exact repo.
- **Template multiplier is real** — raised by C, conceded by A and B. Every hook ships to every downstream project. Friction for non-AI workflows.
- **Soft warning is worst of both worlds** — raised by C, conceded by A and B. All complexity cost, zero enforcement benefit. Eliminates pure option B.
- **Convention sharpening eliminates ambiguity at source** — raised by C (Phase 2 revision). If CLAUDE.md never mentions `.meta/references/` as a direct Read target, the LLM has no path to rationalize. 0 LOC fix.

## Lone wolf insights

- **Wrong-layer argument (partially survived):** hooks are for deterministic actors. LLMs are probabilistic. The hook is a "noisy middleman" between the LLM and the CLAUDE.md rule it reads anyway. Weakened by PM.15 evidence but the principle of layer-matching remains valid.
- **Convention sharpening (survived, evolved to key recommendation):** don't enforce reading restrictions — remove the ambiguity entirely by never documenting `.meta/references/` as a direct target. If the LLM never sees the path in its instructions, it doesn't take it. This is the highest-leverage intervention at 0 LOC.

## Contested arguments (no consensus)

- **PM.15 analogy** — A says "conventions failed, same failure mode." C says "PM.15 was documentation drift (ghost rows), not read-path bypass — different category." Both are logically valid. The question is whether the analogy extends.
- **Layer matching** — A says "hooks work on LLM behavior via check_skills_contract, same tier." C says "contract check validates static files, gate intercepts runtime calls — different enforcement surfaces." Legitimate architectural distinction.

## Dismissed arguments (refuted or irrelevant)

- **"LLMs follow documented conventions reliably"** (B Phase 1) — weakened by PM.15 evidence and by B's own Phase 2 concession. True in single sessions, unreliable across fleet of autonomous agents.
- **"Fix the convention, hooks treat symptoms"** (C Phase 1) — partially refuted by PM.15. But C's Phase 2 revision ("sharpen the convention") rescued the core insight.

## Convergence points

- Soft warning pure = eliminated (all 3 agree)
- Ghost features = real evidence of convention failure (all 3 concede)
- Template multiplier = real cost (all 3 concede)
- Convention sharpening = high-leverage, 0 LOC, should be done regardless (all 3 implicitly agree)

## Irreducible tensions

- **Enforcement vs template multiplier:** a hook that protects a pattern in meta-repo imposes cost on 50 downstream projects. Value judgment: protect the pattern (A) or trust the prompt (C)?
- **Category match:** is the Read gate the same pattern as check_skills_contract.py (A) or a different enforcement surface (C)?

## Recommendation

**Confidence: AMBER**

**Synthesized position — "sharpened convention + opt-in hook":**

1. **Convention aiguisée (immediate, 0 LOC):** rewrite CLAUDE.md so `.meta/references/` is NEVER mentioned as a direct Read target. The librarian is the only documented entry point. Prompt engineering as first line of defense.
2. **Hook shipped but commented out in template (immediate):** `scripts/gate_deep_sources.py` exists in the template. The settings.json hook entry is present but commented, with documentation on when to enable.
3. **Meta-repo: hook ACTIVE (immediate):** the meta-repo itself uncomments the hook and dogfoods it. If it breaks workflows here, we know before downstream.
4. **Data at 6 weeks:** if meta-repo shows no workarounds and librarian covers use cases, promote hook to active-by-default in template (v2.1). If it gêne, leave opt-in. Falsifiable.

## Decision

**USER DECISION NEEDED**

To decide, consider:
- Are you comfortable with the meta-repo being the guinea pig for hard block while downstream gets opt-in?
- Does "convention aiguisée + opt-in hook" feel like principled pragmatism or like a committee compromise?
- Would you rather ship hard block everywhere and accept the template multiplier cost upfront?
