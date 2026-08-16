# Playbook — Onboarding Flow (build or audit)

Prereqs: diagnostic + a defined activation event (the "first value" moment —
if undefined, define it FIRST; everything else calibrates to it). Metrics:
activation rate, time-to-value; guardrail: d7/d30 churn.

## Structure

1. **Map the path to activation:** every screen/step between signup and the
   activation event. Count fields, decisions, waits.
2. **Cut or defer** everything not on that path (Make It Easy): ask only
   what the next step needs; pre-populate from public data where possible
   (careful: GDPR consent stays explicit — localization-ro-eu.md).
3. **One strategic-friction moment maximum** (IKEA effect): a step where
   the user invests and the product becomes "theirs" (first building added,
   first invoice issued). Everything else stays frictionless.
4. **Progress + effort display:** progress bar; loading states that show
   work ("checking 47 legal requirements…") — only claims that are true.
5. **Peak engineering:** the activation event is the peak — celebrate it
   proportionally to the segment (B2B-regulated: confirmation + what's now
   safe; consumer: warmer).
6. **Implementation intentions for retention:** "When {existing routine},
   {product action}" prompt after activation; let the user pick a start
   date (Fresh Start, commitment device).

## Element checklist (audit with Before/Problems/After/Rationale/Test)

Signup form fields, each step between signup→activation, empty states
(humor per tone-calibration.md), progress indicators, the activation moment
itself, first-session ending (peak-end), day-1 email.

Close with scorecard + experiment-backlog entries.
