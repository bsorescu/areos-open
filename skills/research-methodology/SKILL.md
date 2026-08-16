---
name: research-methodology
description: Use BEFORE any architecture decision, technology/framework/library choice, or new subsystem design — enforces research with evidence before design. Produces a standardized research report in the project vault, which feeds the resulting ADR. Completes the chain research → brainstorming → plan → implementation.
---

# Research Methodology

Research before architecture. Evidence before decisions. No technology choice
without a comparison the team can re-read six months later and still trust.

**Announce at start:** "Using research-methodology to investigate [question]."

<HARD-GATE>
Do NOT proceed to brainstorming/design/implementation of the decision this
research informs until the research report exists and the user has seen the
recommendation.
</HARD-GATE>

## When to trigger

- Choosing a technology, framework, library, protocol, or provider
- Designing a new subsystem or replacing an existing one
- Any decision that will become an ADR
- User asks "what should we use for X?" or "how do others do X?"

When the decision is trivially reversible AND low-cost (e.g. picking a dev
dependency), say so explicitly and propose the fast path below. Never skip
silently.

### Fast path (small decisions) — validate on first real use

For reversible, low-cost decisions only, with the user's explicit OK:
1. Frame in two lines (decision + top criterion).
2. Check at most 5 sources (official docs first; Context7 for libraries).
3. In-chat mini-comparison (one short table), recommend, note rejected options.
4. Record the outcome in the session note — no standalone report, no ADR
   unless the decision later proves architectural.

If during the fast path a hard constraint or a contradiction between sources
appears, STOP and escalate to the full 5-step process.

## Process (5 steps)

### Step 1 — Frame the question

WRITE DOWN before searching:
- The decision this research informs (one sentence)
- Decision criteria, ranked (e.g. maturity, cost, fit with existing stack)
- Hard constraints (budget, licenses, platform, timeline)

### Step 2 — Discover sources (actively)

Do NOT assume any initial list is complete. Sweep at least 3 modalities:
- Mature open-source projects (GitHub search, awesome-lists)
- Official documentation (via Context7 when it's a library/framework)
- Industry practice (engineering blogs, papers, conference talks — WebSearch,
  deep-research skill for large sweeps)

Record every source consulted, including dead ends (they prove coverage).

**Data hygiene for volatile metrics:** adoption numbers (GitHub stars, npm
downloads, contributor counts) drift between reads — record each as
`value @ read-date`. If reads diverge across the research, report an interval
(`12k–14k, read 2026-07-03/04`), never a single stale number.

### Step 3 — Evaluate with the standard grid

Every candidate goes through the SAME grid — use
`templates/technology-evaluation.md`. No candidate gets a pass on a criterion
because it's the favorite.

For structure/process decisions (restructuring, ownership, workflow design)
the candidates are usually mechanisms per cluster, not comparable
technologies: keep the discipline (same criteria for every option), drop the
technology-specific rows (license, maintenance), and evaluate options
per cluster instead of forcing one global grid. State in the report which
grid variant was used.

### Step 4 — Compare with evidence

Comparison table where every non-obvious claim has a citation (link, doc
reference, or repo observation). Impressions are labeled as impressions.

**Adversarial claim verification (mandatory for load-bearing claims):** a
claim is load-bearing if the recommendation flips when it is false, or if two
sources dispute it. For each such claim, dispatch an independent verifier
subagent prompted to REFUTE the claim against primary sources (official docs,
the actual repo/artifact — not blog posts citing blog posts). Record verdict
(confirmed / refuted / unresolved) plus the primary-source evidence in the
report. An unresolved load-bearing claim goes to "Open questions" and cannot
silently support the recommendation.

Sampling (verifying a subset of claims) is triage, not verification. If a
sampled check finds ANY error, or if the research feeds an execution plan,
the plan must contain an explicit full-verification gate before the affected
step — never extrapolate "sample OK" to "all OK".

**Environment claims — mark verified vs assumed (ADR-010).** Adversarial
verification above targets claims *about the world* (APIs, versions,
compatibility) — checkable against primary sources. A different class needs a
different rule: claims about **the operator's own live system** (what is
running, how it is configured, what a dashboard contains, what a container
mounts). No documentation can confirm these; only direct observation can. A
verifier subagent cannot "refute" what runs on a given host.

Mark every environment claim explicitly, in the report and in anything derived
from it:
- `verified: <command or observation> @ <date>`, or
- `assumed` — plus the basis of the inference ("typical install per docs").

Marking is mandatory even when verification is impossible — autonomous research
often runs without access to live systems. An honestly-marked `assumed` claim is
useful; an unmarked one is indistinguishable from a fact.

**Consequence for plans:** a task derived from an `assumed` environment claim is
written as "verify X, then do Y" — never "do Y". The cost is one command; the
alternative is an execution window planned on a false premise. Origin: a session
where 3 of 4 planned tasks had false premises, all inferred from docs describing
a *typical* install rather than *this* one.

### Step 4.5 — Completeness critique

Before recommending, run a critic pass (independent subagent, strongest
available model) over the draft with one question: **what is missing?**
Specifically:
- a candidate everyone in the field would expect to see evaluated;
- a discovery modality from Step 2 not actually swept;
- a contradiction between evaluation grids or between grid and comparison;
- a load-bearing claim that skipped adversarial verification;
- when the change touches a shared field or artifact: who READS it, not only
  who writes it — a producer-side sweep reads as complete while missing consumers.

Feed findings back into Steps 2–4. Repeat until the critic returns nothing
material (typically 1–2 rounds). Note in the report that the critique ran and
what it caught.

### Step 5 — Recommend

- Recommendation with explicit trade-offs
- Rejected alternatives WITH reasons (this becomes the ADR's "alternatives
  considered" section)
- Open questions that remain

## Output

Fill `templates/research-report.md` and save to the project vault:
`~/Documents/obsidian-claude/{project}/research/YYYY-MM-DD-{topic}.md`.
Link the report from the ADR it informs. Chain must be traceable:
research → ADR → plan → implementation.

## Routing

Follow `.claude/rules/model-routing.md` (AREOS repo): discovery fan-out → cheap
models via parallel subagents; synthesis, contradiction-detection, and the
final recommendation → strongest available model. For sweeps of 5+ sources,
prefer the deep-research skill or a Workflow fan-out over sequential fetches.

## Friction log

Owned by the skill-authoring rule (AREOS `.claude/rules/skill-authoring.md`,
TDD-for-skills): after each run, append friction to the session note under
`## Fricțiune research-methodology`.
