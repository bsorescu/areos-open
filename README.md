# AREOS — AI Research Engineering Operating System

An **executable methodology** for AI-team software development (Claude Code +
subagents): research before design, design before implementation, traceable
decisions, persistent memory — where every rule exists in a form the agent
harness actually loads at runtime. A rule that isn't executable is an opinion.

## Core ideas

- **Executable-first.** Rules live as skills, always-on rule files, hooks,
  and templates — loaded at runtime, not described in a wiki. Docs (the
  `handbook/`) explain rules; the executable artifact is the source of truth.
- **Friction-driven iteration.** Nothing is built speculatively. Every skill
  enters the kernel only after being validated on a real task; every
  iteration must cite the documented friction it addresses.
- **The methodology verifies itself.** A mechanical lint (`chain-lint`)
  checks the traceability chain (research → decision → plan → state) on
  every session start/stop; adversarial fresh-context reviews audit what
  lint can't see.
- **Kernel public, memory private.** This repo is the kernel. Project memory
  (decision records, state, session notes) lives in a private Obsidian vault
  — the architecture is documented here, the content is not.

## What's inside

| Path | What it is |
|---|---|
| `skills/` | Claude Code skills: `research-methodology` (evidence before architecture), `behavioral-marketing` (bias-grounded marketing with anti-dark-pattern guardrails), `areos-init` (bootstrap a project onto AREOS) |
| `.claude/rules/` | Always-on constraints: model routing by capability tier, skill authoring, methodology precedence |
| `.claude/hooks/` | Session lifecycle: context injection at start, checklist reminder at stop, `chain-lint` verification |
| `prompts/` | Dispatch prompts for fresh-context subagent roles (adversarial reviewer, adherence auditor) |
| `handbook/` | One chapter per validated skill: why it exists, what shaped it, what was rejected |
| `scripts/` | Contribution lint (CI), publish tooling |
| `tests/injection-corpus/` | Seeded attack samples used to validate the security layers (see SECURITY.md) |

## Install

Skills are installed by symlink into your Claude Code skills directory:

```bash
ln -sfn "$PWD/skills/research-methodology" ~/.claude/skills/research-methodology
```

Hooks are copied verbatim into a project's `.claude/hooks/` — they derive the
project slug at runtime (see `skills/areos-init/SKILL.md` for the full
bootstrap). The vault root defaults to `~/Documents/obsidian-claude` and can
be overridden with `AREOS_VAULT_ROOT`.

Handbook chapters are currently in Romanian (the project's working language);
translations are a welcome first contribution.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — the contribution process is the
methodology itself (TDD for skills, friction-cited iterations). Before
opening a PR that touches skill content, read [SECURITY.md](SECURITY.md):
skill text is loaded into users' agent context, so contributions pass a
layered defense (deterministic lint → adversarial model review → pinned
promotion) designed for exactly that threat.

## License

[MIT](LICENSE)
