# Playbook — Email Sequences (trial-to-paid, retention, lifecycle)

Prereqs: diagnostic + activation event + verified trial mechanics (length,
gating, cancel UX) in research-marketing.md. GDPR: opt-in consent + working
unsubscribe on every send (localization-ro-eu.md). Metrics: per-email
click→goal; guardrail: unsubscribes, spam complaints.

## Trial-to-paid skeleton (14-day example — adapt to real trial length)

| Send | Timing | Job | Bias material |
|---|---|---|---|
| Welcome | Day 0 | One action: reach activation; nothing else | Make It Easy; implementation intention |
| Activation nudge | Day 1–2 (skip if activated) | Remove the specific blocker (behavior-triggered, not calendar) | Generation Effect (question format) |
| Value proof | Day 3–5 | Show THEIR data/result so far, concretely | Concreteness, Precision, IKEA (their work) |
| Expansion | Day 7 | Second value moment / feature adjacent to their usage | Peak engineering |
| Objection email | Day 9–10 | Top objection from objection-matrix.md, answered with proof | Fairness ("because") |
| Conversion open | Day 11–12 | The offer: plan fit + honest framing; real deadline = trial end | Extremeness Aversion (plan choice), Framing (verified loss: what they lose access to) |
| Last day | Day 13–14 | Peak-end: celebrate what they accomplished, then the ask | Peak-End; Freedom of Choice ("you're free to walk away — export anytime") |

Behavior-triggered beats calendar-triggered wherever the ESP allows;
calendar sends are the fallback.

## Retention / lifecycle rules

- Trigger on behavior change (usage drop, renewal proximity, milestone),
  not on marketing calendar.
- Renewal emails in regulated B2B: sober summary of value delivered
  (numbers), renewal terms explicit — no surprise auto-renew (dark pattern
  + EU law).
- Win-back: one honest email > a discount ladder that trains cancellation.

## Per-email checklist

Subject (concrete > clever; A/B from experiment-backlog), one job per email,
one CTA, plain-text feel for B2B, loss framing only on verified losses
(losing access at trial end = verified; "prices going up" = only if true),
unsubscribe visible.

Close with scorecard (_audit-format.md) + experiment-backlog entries.
