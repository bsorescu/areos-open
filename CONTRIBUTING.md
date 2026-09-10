# Contributing to AREOS

The contribution process **is** the methodology. If a PR doesn't follow it,
the review will ask for exactly what the methodology would have produced.

## Ground rules

1. **Friction-driven, never speculative.** Every change to a skill or rule
   must cite the concrete friction it addresses — a real session where the
   current version failed or fell short. "This would be nice" is not a
   contribution category here; "this failed on a real task, here's how" is.
2. **TDD for skills.** A new skill (or a behavior-changing iteration) ships
   with RED/GREEN evidence in the PR description: what a baseline agent did
   WITHOUT the skill (RED), what it did WITH it (GREEN), on the same task.
   See `handbook/behavioral-marketing.md` for the founding example.
3. **Budgets are hard.** Skill descriptions are trigger-only (what situation
   activates it, not how it works); SKILL.md stays under ~150 lines; loaded
   content is a recurring token cost and is reviewed as such.
4. **One instruction = one mechanism.** Don't restate an instruction that
   another file owns — link to it. Duplication is drift waiting to happen.

## Where to start

Issues labeled **`good-first-friction`** are real, logged frictions with the
methodology, each a concrete iteration target: the friction is quoted, the
proposed change is small, and the acceptance test is RED/GREEN on a real
session of yours. Most are single-session observations that are *not yet
earned* under rule 1 — your second session is what earns them. Pick one,
run the skill on a real decision, and bring the evidence.

## What you can and can't touch

- **Open to contribution:** skill bodies, references, templates, handbook
  chapters (including translations), attack samples for the injection
  corpus, documentation.
- **Authority surfaces (maintainer-only, enforced by CI):** `.claude/`
  (hooks, rules, settings), `.github/`, `scripts/`, `CLAUDE.md`, and any
  frontmatter that grants capabilities (`allowed-tools`, `hooks:`,
  `context:`, removal of `disable-model-invocation`). PRs touching these
  fail the lint unless a maintainer applies the `authority-ok` label.

## Why the review is strict

Skill text is not documentation — it is **instructions loaded into users'
agent sessions**. A merged PR here becomes part of what an AI agent treats
as trusted guidance. That's why every PR passes:

1. a deterministic lint that rejects the unobfuscated attack shapes (no
   model involved, run from the trusted base ref so a PR can't disable it);
2. an adversarial model review with a data-contract framing — the
   load-bearing layer for anything subtle;
3. and merged content still doesn't auto-deploy anywhere — maintainers
   promote pinned commits deliberately.

Details and threat model: [SECURITY.md](SECURITY.md). Don't take the
strictness personally; it's the cost of shipping executable trust.

## Practicalities

- Conventional commits (`feat:`/`fix:`/`docs:`/`chore:`).
- English for executable artifacts (skills, rules, scripts); the handbook is
  currently Romanian — translations welcome as separate PRs.
- Run `python3 scripts/contribution-lint.py --base origin/main` locally
  before pushing; CI runs the same script.
