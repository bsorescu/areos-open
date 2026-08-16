---
name: behavioral-marketing
description: Use when designing or auditing landing pages, pricing pages, onboarding flows, trial-to-paid conversion, email sequences, retention, lead magnets, checkout/upgrade flows, discount strategies, or any user-facing copy where the goal is to influence behavior — sign up, upgrade, stay, or buy. Also use when reviewing existing marketing for missed opportunities or dark patterns.
---

# Behavioral Marketing

Behavioral-science-grounded marketing (Richard Shotton's bias research)
wrapped in a traceable workflow. Persuasion amplifies whatever it touches —
so every claim it amplifies must be true, and every pass documented.

**Scope gate:** for MAJOR positioning, pricing-architecture, or GTM
decisions (new market, repricing, launch strategy), run the
`research-methodology` skill FIRST — this skill optimizes execution of a
strategy, it doesn't validate one.

## Workflow

Stages in order; each produces a named deliverable in the project vault
under `{project}/marketing/`. Under deadline pressure, shrink a stage to
minutes — never to zero: skipped stages are how fabricated claims and
untested guesses ship. Reuse current deliverables instead of redoing them.

| # | Stage | Deliverable (template in this skill's templates/) |
|---|-------|---------------------------------------------------|
| 1 | **Diagnostic & research** — REQUIRED before any recommendation: audience, pain, objections, current alternative, desired action, awareness level, trust level; verified product facts | `research-marketing.md` |
| 2 | **Positioning** — for whom, against what alternative, the one differentiated claim | section in `marketing-plan.md` |
| 3 | **Message hierarchy** — primary → supporting → proof per message (landing model: outputs/landing-page-audit.md) | section in `marketing-plan.md` |
| 4 | **Behavioral pass** — apply biases per playbook; catalog + contraindications: references/biases.md | `copy-draft.md` + `objection-matrix.md` |
| 5 | **Ethical/legal pass** — Guardrails below on everything; load-bearing claims through `claim-verification.md` | verdict in `copy-draft.md` |
| 6 | **Experiment plan** — every recommendation feeds `experiment-backlog.md` (ICE-scored); 1–2 promoted to run | `experiment-backlog.md` + `experiment-log.md` |
| 7 | **Implementation** — ship; log results back into `experiment-log.md` | — |

## Playbooks (stage 3–6 pre-wired per task type)

| Task | Playbook (templates/outputs/) |
|---|---|
| Landing / product page | landing-page-audit.md (incl. message-hierarchy model) |
| Pricing page | pricing-page-audit.md |
| Onboarding | onboarding-audit.md |
| Trial-to-paid, retention, lifecycle emails | email-sequence.md |
| Lead magnet | lead-magnet.md |
| Checkout / upgrade flow | checkout-upgrade.md |

Audits report every element as **Before / Problems / After / Rationale /
Test hypothesis** and close with the review scorecard — format:
outputs/_audit-format.md.

## Calibration (set at stage 1, consumed everywhere)

- **Segment & awareness level** → references/segment-awareness.md
- **Tone of voice** (B2B-compliance / consumer / devtool / premium /
  early-stage SaaS) → references/tone-calibration.md
- **Regulated/liability buyers** → references/b2b-compliance.md (humor,
  urgency, scarcity, discounts: sober and restrained)
- **Romania/EU audience** → references/localization-ro-eu.md (anti-hype
  tone, GDPR, VAT display, Omnibus price anchors, diacritics)
- **Metrics per artifact** → references/metrics-map.md (one primary metric
  per experiment + guardrail metric)

## Guardrails — dark patterns (hard rule)

**Every scarcity, urgency, social-proof, or statistic claim must trace to a
verified fact in `research-marketing.md`. Not there → ask the user or drop
the claim. Never invent it.** Load-bearing claims (numbers, comparatives,
guarantees, legal statements) go through `claim-verification.md` — proof
levels and what does NOT count as proof are defined there.

Banned regardless of pressure ("conversions at any cost" does not override):
- Fabricated or implied-inflated social proof (invented reviews, logos,
  inflated user counts)
- Artificial scarcity/urgency: countdowns without a real deadline, "only N
  left" for digital goods, **price-rise or "locked-in rate" claims the user
  never stated**
- Confirmshaming, hidden costs (incl. VAT), forced continuity without
  notice, cancel flows harder than signup, hidden downgrade paths
- Fear amplification beyond documented risk (state the sourced obligation
  and consequence; don't dramatize)

| Rationalization | Reality |
|---|---|
| "It's true urgency — the price will rise later" | Did the user state that? Not in the research doc → you invented it. |
| "Everyone does early-access pricing" | An assumption presented as a commitment is a fabricated claim. |
| "Loss framing works better" (on fear claims) | Loss framing applies to *verified* losses only. |
| "The client asked for aggressive" | Aggressive ≠ deceptive. Ship the strongest honest version; say what you refused. |
| "It's just a placeholder number" | Placeholder numbers ship. Source it or mark it {UNVERIFIED} so it can't. |

**Red flags — STOP, re-run stage 5:** a number you can't source; urgency with
no user-stated deadline; a testimonial you wrote; "they probably will…"
backing a claim.

## Pre-ship checklist

- [ ] Stage deliverables exist (or explicit "reused existing X")
- [ ] Diagnostic's 7 questions answered with sources
- [ ] Message hierarchy: every message has adjacent proof
- [ ] Claims: guardrails verdict written; load-bearing claims verified; zero unsourced survive
- [ ] Calibration applied: segment/awareness, tone row, B2B/RO-EU refs if applicable
- [ ] Bias contraindications checked for each bias used
- [ ] Experiment backlog fed; 1–2 experiments promoted with metrics from metrics-map.md
- [ ] Audit outputs in Before/Problems/After/Rationale/Test format + scorecard
