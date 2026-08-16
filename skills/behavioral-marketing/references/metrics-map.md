# Metrics Map — what to measure per artifact

Primary metric = what the experiment moves. Guardrail = what it must not
break. Vanity metrics (impressions, opens alone) never decide experiments.

| Artifact | Primary metric | Secondary | Guardrail |
|---|---|---|---|
| Landing page | Visitor → signup rate | Scroll depth, CTA click rate | Bounce rate; signup quality (activation of the cohort) |
| Pricing page | View → checkout start | Plan mix (target-tier share) | Refund/chargeback rate; support tickets about billing |
| Onboarding | Activation rate (first value event) | Time-to-value, step completion | Early churn (d7/d30); support contacts |
| Trial-to-paid | Trial → paid conversion | Card-added rate, usage depth | Involuntary churn, refunds |
| Email sequence | Sequence goal rate (per email: click → goal) | Open rate (diagnostic only) | Unsubscribe rate, spam complaints |
| Retention | N-week/month retention curve | Feature adoption breadth | Discount dependency (revenue per retained user) |
| Lead magnet | Download → qualified-lead rate | Email confirm rate | List quality (post-download unsubscribe) |
| Checkout/upgrade | Start → completion rate | AOV / plan value | Refunds, involuntary downgrades, chargebacks |

Rules:
- One primary metric per experiment (experiment-log.md enforces the field).
- Funnel position dictates patience: retention metrics need weeks — don't
  call experiments early (stop condition set upfront).
- Percentages need denominators recorded in the log — "conversion up 20%"
  without N is not a result.
