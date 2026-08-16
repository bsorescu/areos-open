# Playbook — Checkout / Upgrade Flow

Prereqs: diagnostic; audience here is MOST-AWARE (segment-awareness.md) —
the job is removing reasons to stop, not adding persuasion. Metrics: start →
completion; guardrails: refunds, chargebacks, involuntary downgrades.

## Design rules

- **Friction only where law or trust requires it:** minimum fields, saved
  payment methods, no account-creation walls before purchase (create the
  account FROM the purchase). Every extra field is measurable drop-off
  (Make It Easy).
- **Price display:** full price with VAT visible before the final step
  (localization-ro-eu.md) — surprise costs at step 3 are the top checkout
  killer AND a dark pattern.
- **Reassurance at the money moment:** cancel/refund terms in plain words
  next to the pay button (Freedom of Choice — true statements only);
  security signals (payment provider logos) for first-time buyers.
- **Upgrade prompts (in-product):** trigger on hitting real limits or real
  value moments, not on a timer; show current-plan usage as the "because"
  (Fairness): "you used 9/10 buildings this month". Never interrupt a task
  mid-flow with an upsell.
- **Existing customers:** no hard sell (reactance −20% likeability);
  suggest, show the math, let them choose. Downgrade path visible — hiding
  it is a dark pattern and churns trust.
- **Post-purchase (peak-end):** confirmation states exactly what happens
  next + when; first invoice arrives correct and on time.

## Checklist

Field count minimal · VAT-inclusive price before final step · cancel/refund
terms adjacent to pay button · upgrade triggers behavior-based · downgrade
path visible · confirmation sets expectations · no dark patterns survive
audit (_audit-format.md).

Close with scorecard + experiment-backlog entries.
