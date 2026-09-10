---
name: areos-init
description: Bootstrap a new project onto the AREOS methodology — vault folder, project CLAUDE.md, portable session hooks, chain-lint. Use when starting work on a repo that has no vault folder or no .claude/ scaffolding, or when the user says "pune proiectul pe AREOS" / "inițializează proiectul".
disable-model-invocation: true
---

# AREOS Init

Scaffold the AREOS methodology onto a project. Idempotent: NEVER overwrite
an existing file — report it and skip. Announce: "Using areos-init for
{repo}."

## Inputs (derive, then confirm with the user in one message)

- `REPO` = project repo root (default: cwd).
- `SLUG` = lowercase `basename $REPO`. BEFORE accepting it, list existing
  vault folders (`ls ~/Documents/obsidian-claude/`) and check whether one
  already belongs to this repo (similar name, or referenced from the repo's
  CLAUDE.md) — if yes, propose THAT as the slug instead. Creating a parallel
  vault folder for an already-tracked project is the failure mode to avoid
  (precedent: a unilateral split that had to be reverted; near-miss: a repo
  named `<project>-configs` almost got a parallel vault next to `<project>`). When slug ≠ repo basename, write it to
  `$REPO/.claude/areos-project` (single line) — the hooks read it.
- `AREOS` = the directory this skill lives in, two levels up from this
  file (`$(dirname "$0")/../..` from `skills/areos-init/`) — never a
  hardcoded path; the kernel may be cloned anywhere.

## Steps

### 1. Vault skeleton (`~/Documents/obsidian-claude/$SLUG/`)

```
mkdir -p context/$SLUG decisions plans/archive sessions research
```

Create `context/$SLUG/current-state.md` (skip if exists):
header `# {Project} — Stare curentă` + `**Ultima actualizare:** {today}`,
sections: Active Work (max 5) / Recently Shipped / Backlog (P0-P1-P2) /
Known Issues / Arhitectură (pointers). No frontmatter, no narrative.

### 2. Repo scaffolding

- `$REPO/CLAUDE.md` (skip if exists): what the project is (1 paragraph),
  instruction-ownership table (copy structure from AREOS CLAUDE.md, per
  ADR-006), pointer to vault `$SLUG/` + current-state. Under 60 lines.
- `cp $AREOS/.claude/hooks/{session-start,session-stop,chain-lint}.sh`
  → `$REPO/.claude/hooks/` + `chmod +x`. Copy VERBATIM — they derive the
  slug at runtime; do not edit them.
- Merge into `$REPO/.claude/settings.json` (preserve existing keys): the
  `hooks` block from AREOS settings.json (SessionStart startup|clear +
  resume --brief, Stop).
- If the repo is not a git repo: ask the user before `git init`.

### 3. Verify (do not skip)

1. `CLAUDE_PROJECT_DIR=$REPO $REPO/.claude/hooks/session-start.sh | head`
   → must print the injected current-state for `$SLUG`.
2. `$REPO/.claude/hooks/chain-lint.sh` → must be clean (or only expected
   WARNs; explain each to the user).
3. `python3 -c "import json; json.load(open('$REPO/.claude/settings.json'))"`
4. Tell the user: full proof is a NEW session in `$REPO` showing CLAUDE.md
   + hook injection in context.

### 4. Record

Add the bootstrap to the project's first session note (or current-state
Recently Shipped): "Proiect pus pe AREOS (areos-init) → hooks + CLAUDE.md +
vault skeleton". The project inherits the always-on vault tracking rule
from `~/.claude/rules/` — do not copy it per project. If no tracking rule is
installed yet, install the kernel's copy once: `cp $AREOS/templates/vault-tracking-rule.md
~/.claude/rules/vault-tracking.md` (and read `$AREOS/templates/frontmatter-schemas.md` when
creating ADRs/plans/session notes — chain-lint validates that schema).

## Out of scope

Skills/rules of the new project (grow from friction, ADR-002); vault git
setup (the vault repo already exists); multi-machine setup (backlog P2).
