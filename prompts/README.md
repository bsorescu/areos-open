# Prompt Library (per role)

Dispatch prompts for standalone roles run as **fresh-context Claude
subagents** — agents that do NOT see the current conversation, so their
independence comes from clean context, not from a different vendor
(ADR-008; supersedes the original external-models use of this library).

## Entry criterion (dogfooding, ADR-002)

A prompt enters this library only when its role has been exercised in a real
session (or is explicitly required by the design spec). No speculative
role catalog. New prompts start as "validate on first real use" and are
confirmed or cut after that run.

## Ownership (ADR-006)

Roles that are sub-steps of a skill (e.g. claim-verifier and
completeness-critic in research-methodology) are owned by that skill — they
are NOT duplicated here. This library owns only standalone roles.

## Index

| Prompt | Role | Status |
|---|---|---|
| `external-reviewer.md` | Adversarial review of an AREOS artifact by a fresh-context subagent | validated 2026-07-05 (kernel audit, methodology lens) |
