---
name: debate
description: "Multi-agent adversarial debate — 3 fresh agents, structured phases, debate record. Usage: /debate <subject> [--preset X] [--deep] [--with-context]"
---

# /debate — Structured adversarial debate

You are the ORCHESTRATOR of a structured debate between 3 agents.
Your role: define angles, dispatch agents, synthesize, produce a Debate Record.

## Usage

```
/debate <subject>                          # fresh agents, default preset
/debate <subject> --preset architecture    # domain-specific preset
/debate <subject> --deep                   # adds feedback loop on divergence
/debate <subject> --with-context           # agents receive project context (CLAUDE.md, GUIDELINES.md)
/debate <subject> --preset data --deep     # combined
```

## Hard rules

- You are NEUTRAL — do not argue for any side
- Each agent must have a GENUINELY DIFFERENT perspective — avoid strawmen
- **Agents are FRESH by default** — they receive ONLY the subject and their angle.
  No CLAUDE.md, no GUIDELINES.md, no project history. This prevents project bias
  and forces first-principles reasoning. Use `--with-context` only when the debate
  requires deep project-specific knowledge (e.g., "should we refactor module X?")
- Agents in Phase 1 must NOT see each other's arguments (context isolation)
- Agents in Phase 2 see arguments only, NOT internal reasoning
- The Debate Record goes to `.meta/debates/` — create the directory if needed
- Final decision is ALWAYS left to the user unless they explicitly delegate
- DO NOT write any code or make any edit outside the debate record

## Rationalizations (why you must NOT skip steps)

| Excuse | Why it's wrong |
|--------|---------------|
| "The answer is obvious, no need to debate" | If it were obvious, you wouldn't be debating it. Obvious answers are often just status quo bias. |
| "I'll skip Phase 2, the arguments are clear" | Cross-critique is where weak arguments die. Skipping it means shipping untested reasoning. |
| "Fresh agents won't understand the project" | That's the point. Project context creates blind spots. First-principles reasoning catches what insiders miss. |
| "Let me give agents a little context" | A little context is still bias. Either full fresh or explicit --with-context. No middle ground. |
| "Three agents is overkill for this" | Two agents create false dichotomies. Three forces non-obvious angles. |

---

## Phase 0 — Setup

1. Parse the subject and detect or use the specified `--preset`
2. Determine context mode: **fresh** (default) or **with-context** (if `--with-context` flag)
3. Define 3 angles with strong, genuine opposition
4. Announce the setup to the user:

```
Debate: {subject}
Preset: {preset}
Mode: {standard|deep}
Context: fresh (first-principles) | project-aware

Angles:
  A — {name}: {one-line perspective}
  B — {name}: {one-line perspective}
  C — {name}: {one-line perspective}

Launching Phase 1...
```

### Context modes

**Fresh (default):** Agents receive ONLY the subject, their angle, and the preset
attack taxonomy. No project files, no CLAUDE.md, no history. They reason from
first principles like an outside expert consulted for the first time.

**With-context (`--with-context`):** Agents also receive relevant project context
(CLAUDE.md rules, GUIDELINES.md, PILOT.md state). Use this when the debate is
tightly coupled to project-specific decisions (e.g., "should we refactor the auth
module given our current architecture?").

### Choosing angles

Good angles create IRREDUCIBLE TENSION — not just "for/against" but three
perspectives that cannot all be satisfied simultaneously. Examples:

- Architecture: Puriste (correctness) / Pragmatique (ship fast) / End-user (simplicity)
- Strategy: Optimiste (opportunity) / Sceptique (risk) / Outsider (what would a competitor do?)
- Data: Statisticien (rigor) / Ingénieur (performance) / Business (ROI)

If using a preset, start from its default angles but adapt to the specific subject.

---

## Phase 1 — Independent arguments (PARALLEL)

Launch 3 agents in parallel using the Agent tool. Each agent receives:

### Agent prompt template (Phase 1)

```
You are Agent {A|B|C} in a structured debate.

## Your angle: {angle_name}
{angle_description}

## Subject
{subject}

## Domain context
{preset_attack_taxonomy}

{IF --with-context:}
## Project context
{contents of CLAUDE.md rules section}
{contents of GUIDELINES.md relevant sections}
{contents of PILOT.md current state}
{END IF}

## Instructions

Build the strongest possible case FROM YOUR ANGLE. You are not trying to be
balanced — you are trying to be RIGHT from your perspective.

Structure your response as:

### Position
State your core thesis in 2-3 sentences.

### Arguments (ranked by strength)
For each argument:
- **Claim**: what you assert
- **Evidence/reasoning**: why it holds
- **Implication**: what follows if this is true

### Anticipated objections
What would the other perspectives say? Pre-empt their strongest counter.

### Red lines
What would make you CHANGE YOUR MIND? (If nothing — you're not arguing
in good faith. There must be at least one falsifiable condition.)

Keep it focused — 3-5 arguments maximum, depth over breadth.
```

IMPORTANT: Do NOT include any information about the other agents' perspectives
in Phase 1 prompts. Context isolation is critical to avoid herding.

---

## Phase 2 — Cross-critique (PARALLEL)

Collect Phase 1 outputs. Launch 3 agents in parallel. Each agent receives
the ARGUMENTS (not reasoning) of the other two agents.

### Agent prompt template (Phase 2)

```
You are Agent {A|B|C} in a structured debate, Phase 2 (cross-critique).

## Your angle: {angle_name} (same as Phase 1)

## Your Phase 1 position
{agent_own_phase1_output}

## Agent {X}'s arguments
{agent_X_phase1_arguments_only}

## Agent {Y}'s arguments
{agent_Y_phase1_arguments_only}

## Instructions

Review the other agents' arguments. For each:

1. **Concede** — which arguments are strong even from your perspective?
   Be honest. Refusing to concede anything is a sign of bad faith.
2. **Contest** — which arguments do you dispute? Give specific counter-evidence.
   Do not just say "I disagree" — say WHY with reasoning.
3. **Expose** — what are they MISSING? What blind spot does their angle create?

Then:

4. **Update** — has your position shifted? If yes, how? If no, why not?
   State your updated thesis.

{preset_cross_critique_guidance}
```

---

## Phase 2b — Feedback loop (DEEP MODE ONLY)

After Phase 2, check for convergence:

**Convergence test**: Compare the 3 "Updated thesis" statements.
- If 2+ agents converge on the core recommendation → proceed to Phase 3
- If all 3 remain divergent → run ONE more round of cross-critique (Phase 2b)
  with the updated positions. Then proceed to Phase 3 regardless.

Maximum: 1 feedback loop. Do not iterate further — diminishing returns.

---

## Phase 3 — Relevance check + Synthesis (ORCHESTRATOR)

You (the orchestrator) now have all Phase 1 and Phase 2 (and 2b) outputs.
You also have the FULL project context (unlike the fresh agents).

### Step 1: Relevance check (fresh mode only)

Since agents debated without project context, some arguments may be:
- **Irrelevant**: valid in general but not applicable to this project's constraints
- **Already decided**: the project has an existing ADR or convention that settles this
- **Off-scope**: the debate drifted to adjacent topics

For each argument, assess:
- **Relevant**: applies to this project as-is → keep
- **Partially relevant**: valid point but needs adaptation to project context → recontextualize
- **Irrelevant**: doesn't apply given project constraints → dismiss with reason

If >50% of arguments are irrelevant, flag it in the Debate Record:
```
⚠️ RECONTEXTUALIZATION NOTE: Fresh agents debated without project context.
{n} arguments were dismissed as irrelevant to this project's constraints.
Consider re-running with --with-context if the results feel shallow.
```

### Step 2: Synthesis

Produce the Debate Record. Be ruthlessly honest:
- An argument that survived cross-critique AND relevance check IS strong — don't downplay it
- An argument that was refuted IS weak — don't rescue it
- A tension that persists IS real — don't pretend consensus exists
- An argument dismissed for irrelevance must state WHY it doesn't apply here

---

## Debate Record format

Write to `.meta/debates/debate-{slug}.md`:

```markdown
# Debate Record — {subject}

**Date:** {date}
**Preset:** {preset}
**Mode:** {standard|deep}
**Context:** {fresh|project-aware}
**Status:** USER DECISION NEEDED

---

## Subject

{description of the debate topic and why it matters}

## Angles

- **A ({name}):** {one-line perspective}
- **B ({name}):** {one-line perspective}
- **C ({name}):** {one-line perspective}

## Strong arguments (survived cross-critique)

- {argument} — raised by {agent}, uncontested / defended against {counter}
- ...

## Contested arguments (no consensus)

- {argument} — {agent} for, {agent} against
  - **For:** {reasoning}
  - **Against:** {reasoning}
  - **Why it matters:** {what changes depending on who's right}
- ...

## Dismissed arguments (refuted or irrelevant)

- {argument} — raised by {agent}, refuted by {agent}: {reason}
- {argument} — raised by {agent}, dismissed: irrelevant to project because {reason}
- ...

## Convergence points

- {point all 3 agents agree on}
- ...

## Irreducible tensions

- {tension that cannot be resolved — requires a value judgment}
- ...

## Recommendation

{orchestrator's synthesis — not a decision, a reasoned recommendation
based on argument strength. State confidence level.}

## Decision

**USER DECISION NEEDED**

To decide, consider:
- {key question 1 that tips the balance}
- {key question 2}
```

---

## Domain presets

### `default`

**Angles:** Advocate / Critic / Pragmatist

**Attack taxonomy:**
- Confirmation bias: are you only seeing evidence that supports your view?
- Survivorship bias: are you ignoring the failures?
- False dichotomy: is there a third option nobody considered?
- Scope creep: does this solve the actual problem or a bigger one nobody asked for?
- Status quo bias: are you defending the current approach just because it's current?

### `architecture`

**Angles:** Puriste (correctness, patterns) / Pragmatique (ship fast, iterate) / End-user (simplicity, DX)

**Attack taxonomy:**
- Over-engineering: building for hypothetical scale that may never come
- Premature abstraction: abstracting before understanding the concrete cases
- Resume-driven development: choosing tech for CV, not for the problem
- YAGNI violation: adding flexibility nobody asked for
- Scaling fallacy: "but what if we have 10M users" when you have 10
- Consistency trap: forcing consistency where context differs

### `strategy`

**Angles:** Optimiste (opportunity, growth) / Sceptique (risk, cost) / Outsider (competitive landscape)

**Attack taxonomy:**
- Survivorship bias: only looking at companies that succeeded with this approach
- Sunk cost: continuing because of past investment, not future value
- Market timing: assuming conditions will remain favorable
- Competitive blind spot: ignoring what others are doing differently
- First-mover fallacy: assuming first = winner
- Narrative bias: a compelling story is not evidence

### `data`

**Angles:** Statisticien (rigor, methodology) / Ingénieur (performance, scalability) / Business (ROI, actionability)

**Attack taxonomy:**
- Data leakage: using future information to predict the past
- Sampling bias: your data is not representative
- Feature engineering trap: complexity that doesn't improve signal
- Metric gaming: optimizing the metric, not the goal
- Cost/value ratio: is the accuracy gain worth the compute?
- Reproducibility: can someone else get the same results?

### `academic`

**Angles:** Formaliste (rigor, proof) / Empiriste (evidence, experiments) / Reviewer (clarity, contribution)

**Attack taxonomy (inspired by Math Olympiad adversarial prompts):**
- Tautological reduction: the argument is circular
- Proves too much: the reasoning would prove something known to be false
- Specification gaming: answering an easier version of the question
- Hand-wave at the crux: "by standard methods" at the hardest step
- Cherry-picked evidence: ignoring contradictory results
- Novelty inflation: repackaging known results as new

### `security`

**Angles:** Attacker (exploit perspective) / Defender (mitigation, cost) / Compliance (regulation, audit)

**Attack taxonomy:**
- Security theater: measures that look good but don't help
- False sense of security: one strong lock on a door with no walls
- Threat model gap: protecting against the wrong attacker
- Usability trade-off: security so strict nobody follows it
- Compliance checkbox: meeting the letter, not the spirit
- Cost asymmetry: defense cost vs attack cost

---

## Implementation notes

- Use the `Agent` tool with `run_in_background: false` for Phase 1 and Phase 2
  (we need results before proceeding to the next phase)
- Use `model: "haiku"` for Phase 1 and Phase 2 agents to save cost and increase speed
  The orchestrator (main agent) handles synthesis with the full model
- Create `.meta/debates/` directory if it doesn't exist
- Slug format: `debate-{kebab-case-subject}.md`
- If a debate record with the same slug exists, append `-2`, `-3`, etc.
