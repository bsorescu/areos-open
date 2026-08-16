# Security Model

## The threat that shapes everything here

AREOS content is **instructions for AI agents**. A merged PR to a skill,
rule, or prompt becomes text that users' agent sessions load as trusted
guidance — which makes *prompt injection via contribution* the primary
threat, not classic code execution. A malicious contribution doesn't need to
run anything at merge time; it only needs to be read later, by an agent with
the victim's permissions.

## Layered defense

Each layer has a different failure mode, and no single layer is trusted
alone:

**L1 — Deterministic lint (CI, `scripts/contribution-lint.py`).**
No model in the loop, therefore not persuadable. It catches the
**unobfuscated** forms of the dangerous shapes: capability grants in
frontmatter (`allowed-tools`, `hooks:`, `context:`, `agent:`, `paths:`,
`disable-model-invocation:false`) — detected against the file's *real*
frontmatter range read from disk, so an edit to an existing skill can't hide
one; exfil URLs (scheme, scheme-less, and userinfo-`@` forms) outside
`.github/allowed-domains.txt`; invisible/bidi Unicode; base64-like blobs;
symlinks; binaries; and changes to authority surfaces (`.claude/`,
`.github/`, `scripts/`, `CLAUDE.md`) without the maintainer-only
`authority-ok` label. CI runs the lint from the **base** ref, never the PR's
copy, so a PR cannot neuter its own guard. L1 is not sufficient alone — a
sufficiently novel obfuscation is L2's job to catch; L1 exists to make the
cheap attacks free to reject and to force everything else into prose, where
L2 and human promotion are load-bearing.

**L2 — Adversarial model review (`prompts/contribution-reviewer.md`).**
A fresh-context agent, read-only tools, explicit contract: the diff is
quoted DATA, never instructions to the reviewer. It hunts semantic attacks
lint can't see — exfiltration phrased as telemetry, "don't tell the user"
suppressions, reviewer-targeting text ("this diff is pre-approved").
Its failure mode is contained: a fooled reviewer emits a wrong verdict and
zero actions.

**L3 — Merge ≠ deploy.** This public repo is not anyone's live kernel.
Maintainers promote reviewed, pinned commits into their working setup as a
separate deliberate step. Compromising the repo does not compromise a
running agent.

**L4 — Runtime least privilege.** No skill in this repo carries
`allowed-tools` grants; permissions live only in users' local settings.
Even instructions that survive L1–L3 cannot act without the user's own
permission gates.

## The reviewer is tested, not trusted

`tests/injection-corpus/` seeds known attack patterns with expected
outcomes per layer (some samples are *designed* to pass L1 and must be
caught by L2). Any new attack that slips a layer becomes a corpus sample in
the fix PR — the defense is falsifiable and grows with contact.

## Honest residual risk

A pure-prose injection with no capability change, novel enough to fool all
review lenses, surviving pinned promotion, and still needing runtime
permissions to act — the layers multiply against it, and each failure is
observable after the fact. We consider that residue acceptable and keep it
shrinking via the corpus. What we do NOT defend against: users manually
copying repo content into their own setups without these gates.

## Reporting

Found a way through a layer? Open a private security advisory on GitHub
(preferred) — and if you can, include your finding as a corpus sample.
