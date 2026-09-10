---
type: research
title: {Short descriptive title}
date: {YYYY-MM-DD}
status: draft            # draft | final
informs: []              # ADR ids this research feeds, e.g. [ADR-006]
tags: [research, {project}]
---

# {Title}

## 1. Question & decision criteria

**Decision informed:** {one sentence}

**Criteria (ranked):**
1. {criterion — why it matters}
2. …

**Hard constraints:** {budget / license / platform / timeline}

## 2. Sources consulted

| Source | Type | Verdict |
|---|---|---|
| {link/name} | repo / docs / paper / blog | used / dead end |

{Convention for large sweeps (20+ sources): aggregate one row per modality —
"GitHub sweep: N repos, notable: X, Y" — and move the full per-source list to
an annex file `{this-file}-anexa-surse.md` linked here. Volatile adoption
metrics: record as `value @ read-date`; divergent reads → interval.}

## 3. Candidates evaluated

{One technology-evaluation grid per candidate — inline or linked. For 6+
candidates: one aggregated criteria × candidates grid in an annex, per-
candidate grids only for the shortlist.}

## 4. Comparison

| Criterion | {Candidate A} | {Candidate B} | {Candidate C} |
|---|---|---|---|
| {criterion 1} | {evidence + citation} | … | … |

**Load-bearing claims verified adversarially:**

| Claim | Verdict | Primary-source evidence |
|---|---|---|
| {claim that would flip the recommendation} | confirmed / refuted / unresolved | {link/observation} |

**Environment claims** (about the operator's own live system — ADR-010).
Everything this research asserts about what is running, how it is configured,
or what a console contains. No source can confirm these; only observation.
Mark each one, even when verification was not possible:

| Claim about the environment | verified @ / assumed | Evidence or basis of inference |
|---|---|---|
| {e.g. "hostname X is in the tunnel ingress"} | verified @ {YYYY-MM-DD} | {exact command + its output, or console observation} |
| {e.g. "the service keeps DOMAIN and ADMIN_TOKEN in env"} | assumed | {"typical install per official docs" — not checked against this host} |

Every `assumed` row becomes a "verify X, then do Y" task in the derived plan —
never "do Y".

## 4.5 Completeness critique

| Round | What the critic caught | Resolution |
|---|---|---|
| 1 | {pasted from the subagent's output — never pre-written} | {fixed in §N / rejected because …} |

{Input given to the critic: draft + §4 verdict table + access to {repo/probes}.
Final round recorded only AFTER it ran.}

## 5. Recommendation

**Recommended:** {candidate} — {one-paragraph rationale with trade-offs}

**Rejected alternatives:**
- {candidate}: {reason}

**Open questions:**
- {what remains unknown and how it could be resolved}
