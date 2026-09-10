# Model Routing Matrix (living document)

Governed by ADR-005 + ADR-009 (vault: areos/decisions/). AREOS owns the
POLICY (capability tiers below); the harness owns the BINDING (tier →
concrete model). All work is Claude-native in Claude Code (ADR-008);
independent review = fresh-context subagent with prompts from `prompts/`.

## Routing table (by capability tier)

| Tier | Task type | Effort | Rationale |
|---|---|---|---|
| T1 cheap-mechanical | Bulk edits, file sweeps, extraction, transcription | low | No deep reasoning; verify transcriptions byte-wise |
| T2 breadth | Search fan-out, discovery, repo scans | low–medium | Parallel breadth; synthesis happens at T4/T5. Research discovery: sonnet (4 sessions: primary sources, structured dead-ends; haiku unproven here) |
| T3 standard | Implementation, tests, doc drafting | medium | Best cost/quality for well-specified work |
| T4 sustained-reasoning | Complex implementation, debugging, code review, **adversarial verification of research claims against primary sources** (3 sessions, 3 projects) | high | Sustained reasoning over large context. Review prompts must NAME the lens ("verify interactions with X") — without it the class escapes (2 sessions) |
| T5 frontier | Architecture, specs, research synthesis, adversarial review / completeness critique, final whole-branch review | high–max | Long-horizon trade-offs. Final review catches classes invisible task-level (7 sessions); completeness critique yields material findings, not compliance (6 sessions). Not self-validating: verify T5 facts before acting on them (2 sessions) |
| — | Harness capability verification (Claude Code docs) | agent default | Use the purpose-built `claude-code-guide` agent (2 sessions confirmed) |

**Cross-tier rule (4 sessions, 2 projects, opus and fable alike):** a
reviewer or debugger that RUNS the code (probes, mutations, revert-to-green,
live reproduction) beats one that only reads the diff. Review prompts in
`prompts/` carry an explicit empirical-verification mandate.

## Bindings

**Claude Code (native, ADR-005):** T1 haiku · T2 haiku/sonnet · T3 sonnet ·
T4 opus · T5 fable/mythos-class. Declared per subagent/workflow stage via
`model` + `effort`.

**Any other harness (e.g. pi — ADR-009):** bind tiers at session start from
the models the harness actually has; record the binding in the session note
under `## Model binding`. Heuristics + status (unvalidated on pi as of
2026-09-10 despite one AiMate session on the pi harness): vault
`areos/model-observations.md`.

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
