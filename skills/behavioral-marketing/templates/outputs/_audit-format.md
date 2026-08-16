# Standard audit output format (all audits use this)

Every audited element is reported in exactly this shape — no freeform
critique:

```
### {Element} (e.g. Hero headline)
- **Before:** {current state, quoted verbatim}
- **Problems:** {what's wrong, each tied to a bias, guardrail, or diagnostic mismatch}
- **After:** {proposed rewrite/change}
- **Rationale:** {bias/principle + proof source from research doc}
- **Test hypothesis:** {→ one experiment-backlog.md entry: change → metric → because}
```

Rules: "After" copy passes the same guardrails as new copy (claims sourced);
every "After" generates a backlog entry — recommendations without test
hypotheses are opinions.

## Review scorecard (fill at the end of every audit)

Score 1–5 per dimension; anything ≤2 must have at least one audit element
addressing it.

| Dimension | Score | Worst offender |
|---|---|---|
| Message clarity (one primary message, visible in 5s) | | |
| Proof density (claims backed near where they're made) | | |
| Awareness match (copy register fits traffic's awareness level) | | |
| Friction (fields, steps, cognitive load on the desired action) | | |
| Framing & concreteness (specific, sourced, loss-framed where valid) | | |
| Guardrails (zero dark patterns, zero unsourced claims) | | |
| Segment/tone fit (tone-calibration.md row respected) | | |
| Peak-end (identifiable peak; strong ending) | | |
| Localization (RO/EU rules if applicable) | | |
| Experiment readiness (measurable, backlog fed) | | |

**Verdict:** ship as-is / ship with fixes / rework — {one sentence}
