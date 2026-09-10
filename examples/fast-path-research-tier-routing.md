---
type: research
title: Model routing keyed by capability tier, with per-harness binding
date: 2026-07-05
status: final
informs: [ADR-009]
path: fast-path
tags: [research, example]
---

# Example: a real fast-path research run

This is a lightly generalized copy of a real run of the `research-methodology`
skill on its **fast path** (small, reversible decision). It is here so a new
user can see the output shape end-to-end: framing, a few primary sources, a
short comparison, a recommendation with rejected alternatives, and the
decision record it fed. Total time: ~15 minutes.

## 1. Question & decision criteria

**Decision informed:** should the model-routing rule be keyed by concrete
model names, or by capability tiers with a per-harness binding?

**Criteria (ranked):** (1) works on a second harness with a different model
list; (2) does not duplicate the routing policy; (3) zero runtime cost.

**Hard constraints:** must stay a single always-on rule file; no new tooling.

**Fast path justified because:** reversible (a rule rewrite, not a system
change), low cost, no vendor lock-in involved. Announced; user did not object.

## 2. Sources consulted

| Source | Type | Verdict |
|---|---|---|
| The second harness's own docs on model configuration (per-provider model list, in-session switching) | docs | used |
| The harness's public repository (model config file format) | repo | used |

Two primary sources, both official — the fast path caps candidates (~5),
not sources, and here two were sufficient to settle the decisive criterion.

## 4. Comparison

| Option | Works on 2nd harness | Duplicates policy | Runtime cost |
|---|---|---|---|
| A. Keep model names in the rule | no — names are vendor-specific | no | 0 |
| B. One rule per harness | yes | **yes** (policy copied, will drift) | 0 |
| C. Tiers in the rule + binding per harness | yes | no | 0 |
| D. Auto-benchmark at session start | yes | no | recurring cost every session |

**Load-bearing claim verified:** "the second harness allows switching models
within one session and lists them in a local config file" — confirmed
against its docs and repo (primary sources), read 2026-07-05.

## 5. Recommendation

**Recommended: C** — the kernel owns the *policy* (capability tiers T1–T5),
each harness owns the *binding* (tier → concrete model). One rule, no
duplication, portable.

**Rejected alternatives:**
- A: silently wrong on any harness without the named models.
- B: duplicated policy — guaranteed drift between copies.
- D: recurring cost every session; deferred for the same reason an
  evaluation harness was deferred earlier.

**Open questions:** the binding heuristic on the second harness is
unvalidated until a real working session records a `## Model binding`.

## What happened next

This fed a decision record (ADR-009 in the maintainer's vault). The rule
was rewritten on tiers the same day. The open question is still open at the
time of writing — which is exactly what the record is for.
