# AREOS — Project Instructions

AREOS is the executable methodology (skills, rules, templates) through which an AI
team (Claude Code + subagents) works on large software projects. This repo is the
kernel; project memory lives in the Obsidian vault.

## Instruction ownership (ADR-006)

One instruction = one mechanism. Never duplicate an instruction across mechanisms —
link to its owner instead.

| Mechanism | Owns | Loaded |
|---|---|---|
| `CLAUDE.md` (this file) | Facts and pointers: what AREOS is, where things live, conventions | Every session, in full |
| `.claude/rules/*.md` | Always-on constraints; `paths:` frontmatter only for path-scoped rules | Every session (path-scoped: on matching files) |
| `skills/` | Multi-step procedures invoked on demand (research-methodology, …) | On invocation |
| Vault `~/Documents/obsidian-claude/areos/` | State (current-state.md), decisions (ADRs), research reports, session notes | Read at session start per global tracking rule |

## Conventions

- **Executable-first (ADR-002):** a methodology rule exists only in a form Claude
  Code loads at runtime (skill, rule, template). Docs explain rules; the executable
  artifact is the source of truth.
- Executable artifacts (skills, rules, templates) are written in **English**;
  vault content (ADRs, session notes) and user communication are in **Romanian**.
- Skill lifecycle (descriptions, budgets, install-by-symlink command, TDD
  gate): `.claude/rules/skill-authoring.md`.
- Model/effort selection for subagents and workflow stages follows
  `.claude/rules/model-routing.md`.

## Pointers

- Skills, rules, hooks: this repo (the kernel).
- Decision records (ADRs), project state, and session notes live in the
  maintainer's **private** Obsidian vault — not in this repo (ADR-004:
  kernel public, memory private). The handbook (`handbook/`) is the public
  "why" for each validated skill.
