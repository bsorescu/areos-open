# Injection corpus

Falsifiable security fixtures. These are **inert attack DATA** — never loaded
by any agent. `contribution-lint.py` exempts this directory from content
checks; `run-corpus.sh` deliberately scans the samples to assert layer
behavior.

- `L1-must-fail/` — attacks the deterministic lint MUST reject (capability
  grants, exfil URLs, disable-model-invocation tampering).
- `L2-must-catch/` — pure-prose attacks that PASS L1 by design (no
  capability change) and must be caught by the model reviewer
  (`prompts/contribution-reviewer.md`): suppression, reviewer-targeting.
- `should-pass/` — legitimate skill content that must stay clean.

Run: `./tests/run-corpus.sh` (asserts L1). Every new attack that slips a
layer becomes a sample here in the same fix PR — the defense grows with
contact (SECURITY.md).
