# Model Routing Matrix (living document)

Governed by ADR-005 + ADR-009 (vault: areos/decisions/). AREOS owns the
POLICY (capability tiers below); the harness owns the BINDING (tier →
concrete model). All work is Claude-native in Claude Code (ADR-008);
independent review = fresh-context subagent with prompts from `prompts/`.

## Routing table (by capability tier)

| Tier | Task type | Effort | Rationale |
|---|---|---|---|
| T1 cheap-mechanical | Bulk edits, file sweeps, extraction, transcription | low | No deep reasoning; verify transcriptions byte-wise |
| T2 breadth | Search fan-out, discovery, repo scans | low–medium | Parallel breadth; synthesis happens at T4/T5 |
| T3 standard | Implementation, tests, doc drafting | medium | Best cost/quality for well-specified work |
| T4 sustained-reasoning | Complex implementation, debugging, code review | high | Sustained reasoning over large context |
| T5 frontier | Architecture, specs, research synthesis, adversarial review / completeness critique | high–max | Long-horizon trade-offs; self-correction scales with tier (confirmed 3 sessions, incl. Critical pe evidence 2026-07-08) |
| — | Harness capability verification (Claude Code docs) | agent default | Use the purpose-built `claude-code-guide` agent (2 sessions confirmed) |

## Bindings

**Claude Code (native, ADR-005):** T1 haiku · T2 haiku/sonnet · T3 sonnet ·
T4 opus · T5 fable/mythos-class. Declared per subagent/workflow stage via
`model` + `effort`.

**Any other harness (e.g. pi — ADR-009, validate on first real use):** at
session start, enumerate the models the harness actually has (pi:
`~/.pi/agent/models.json` + built-in providers), map them to tiers by:
cost-per-token and speed (T1/T2), vendor mid-tier general models (T3),
strongest reasoning/thinking variants available (T4/T5). Record the chosen
binding in the session note under `## Model binding`; keep it for the whole
session unless a model underperforms (then note it — see protocol).

**OpenRouter shortcut (coding tasks only):** where OpenRouter is available,
T1–T3 coding work MAY bind to `openrouter/pareto-code` (`min_coding_score`:
<0.33 ≈ T1/T2, 0.33–0.66 ≈ T3, ≥0.66 ≈ T4-coding; pass `session_id` for
cache stickiness). Caveats: coding-only; model/vendor list not
constrainable (data-governance call per project); T5 stays an explicit
strongest-model choice — the router optimizes cost within tier.

## Update protocol

1. During any session: if a model over/under-performs on a task type, note it
   in the session note (vault: areos/sessions/) under `## Model observations`
   — tier + concrete model + harness.
2. At each plan completion (or ~weekly, whichever first): fold session-note
   observations into the log at vault `areos/model-observations.md`; if a
   pattern holds across ≥2 sessions, update the table above and record the
   change in the git log.
3. Never update the table from a single anecdote.

Empirical observations log (append-only state, not always-on rule content):
vault `areos/model-observations.md`.
