---
paths:
  - "skills/**"
---

# Skill Authoring Rules (AREOS)

Apply when creating or editing any skill in this repo.

## Description = trigger, not summary

- The `description` frontmatter is the ONLY part loaded into every session;
  Claude decides from it alone whether to invoke. Write it as trigger
  conditions ("Use BEFORE/WHEN …"), put the primary use case first.
- `description` + `when_to_use` are truncated at 1,536 characters in the
  skill listing — front-load what matters.
- Do not describe implementation in the description; describe the situation
  that should activate the skill.

## Token budget

- SKILL.md under 500 lines (official guidance); AREOS target: under ~150.
  Move reference material to `templates/` or `references/` files loaded on
  demand.
- Once invoked, the body stays in context for the rest of the session —
  every line is a recurring cost. State what to do; don't narrate why.

## Side effects → user-only invocation

- Any skill that commits, deploys, publishes, sends messages, or mutates
  external state gets `disable-model-invocation: true` — the user controls
  timing, not the model.
- Background-knowledge skills that aren't meaningful as a command get
  `user-invocable: false`.
- Use `allowed-tools` narrowly (exact commands, e.g. `Bash(git status *)`),
  never blanket grants.

## TDD for skills (dogfooding gate, ADR-002)

- A skill enters the kernel only after it has run on at least one REAL task,
  with friction documented in the session note (`## Fricțiune {skill}`).
- Every iteration of a skill must cite the documented friction it addresses
  (commit message or session note link). No speculative features.
- New process steps start as "validate on first real use" and are confirmed
  or cut after that run.

## Conventions

- Skills are written in English; one directory per skill under `skills/`,
  installed via symlink (this rule owns the command):
  `ln -sfn "$PWD/skills/<name>" ~/.claude/skills/<name>`
- One skill = one procedure. Facts and pointers belong in CLAUDE.md;
  always-on constraints in `.claude/rules/` (ADR-006).
