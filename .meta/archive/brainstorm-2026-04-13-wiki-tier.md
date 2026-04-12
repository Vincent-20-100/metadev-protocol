---
type: brainstorm
date: 2026-04-13
slug: wiki-tier
status: rejected-for-v1.2
---

# Brainstorm — Wiki tier (PM.1d) — REJECTED for v1.2

**Parent:** `archive/brainstorm-2026-04-12-claude-ai-project-starter.md` §4.2 C2
**Outcome:** REJECTED for v1.2. Gap acknowledged. Revisit when ≥3 real projects demand it.
**Status:** decisions locked, no plan produced, archived with rejection.

---

## 1. The gap being considered

Guillaume Desforges's `claude-ai-project-starter` ships a `docs/wiki/` tier — **living, topic-based, AI-maintained, human-reviewed** narrative documentation of how the system works in its current form, detached from chronology.

### Mental test: what does a dev read after 3 months away?

| Need | Today's answer in metadev | Satisfies? |
|------|---------------------------|------------|
| Where we are | `PILOT.md` | ✅ |
| What's moving now | `SESSION-CONTEXT.md` | ✅ |
| Why we chose X | `decisions/adr-NNN.md` | ✅ |
| What happened, chronologically | `archive/` | ✅ |
| User-facing manual | `docs/` | ✅ |
| **How part Y of the system works right now** | — | ❌ **gap** |

The gap is real. A topic-based, always-current "how this subsystem works" layer is missing between ADRs (point-in-time decisions) and user docs (user-facing).

---

## 2. Why reject for v1.2

### Option analysis

| Option | Verdict |
|---|---|
| **A. Ship `.meta/wiki/`** with topic files, AI-maintained | Addresses the gap, adds a 4th layer of cognitive load |
| **B. REJECT for v1.2** — `ARCHITECTURE.md` at meta/ root + `docs/` cover 90% for solo-builder Python scale | **Chosen** |
| **C. Rename `ARCHITECTURE.md` → multi-file wiki** | Same gap at scale, but a rename-level change does not justify a new subsystem |

### Rationale

- **Scale mismatch.** Target audience is solo builders on Python projects. At that scale, `ARCHITECTURE.md` covers the "how it works today" need. Wiki tier shines for 10+ contributor teams with complex subsystems.
- **Cognitive load cost.** Adding a 4th narrative layer (wiki, on top of PILOT, SESSION-CONTEXT, decisions, archive, references) pushes the `.meta/` cockpit past the point where new users can hold the whole model in their head.
- **No demonstrated pain.** User confirmed: "feature importante mais surtout pour les gros repo donc ça peut attendre". Nobody is hitting this today on the real projects we're shipping.
- **Anti-YAGNI argument fails.** We would be building a subsystem for a hypothetical future need. Rule #6.

### User quote (2026-04-13)

> "c'est une feature importante mais comme tu le dis surtout pour les gros repo donc ça peut attendre"

---

## 3. Revisit trigger

Reopen this brainstorm when ANY of the following happen:

1. ≥3 real projects (either metadev-protocol itself or user-generated projects) demand a wiki tier — i.e., `ARCHITECTURE.md` has become unwieldy or multi-topic narratives are repeatedly needed
2. A team of ≥3 contributors is working on a metadev-generated project and friction surfaces
3. A competitor template ships a wiki tier and user feedback explicitly asks for parity

Until then, `ARCHITECTURE.md` (meta-repo) and user `docs/` (generated projects) are the canonical "how it works now" layer.

---

## 4. What we do NOT keep in backlog

- **PM.1d is CLOSED, not deferred.** Explicitly rejected for v1.2. No PENDING entry.
- If the revisit trigger fires, a NEW brainstorm will be written with fresh context — not a resurrection of this one.

---

## 5. Archive note

This brainstorm lives in `archive/` as evidence of a rejection decision. Future sessions reading the archive can see that the wiki-tier option was explicitly considered and rejected with rationale — not forgotten.
