# Frontmatter schemas + rationale (vault tracking rule)

Referință pentru regula de tracking a vault-ului (`templates/vault-tracking-rule.md`, instalată în `~/.claude/rules/`)
(split 2026-07-05, audit buget context: schemele sunt material de write-time,
nu constrângere always-on). Se citește DOAR când creezi un ADR / plan /
session note. Validare mecanică: chain-lint (AREOS `.claude/hooks/`).

## ADR

```yaml
---
id: ADR-007                     # sau slug descriptiv dacă nu folosim numerotare
title: Scurt și descriptiv
status: proposed                # proposed | accepted | implemented | superseded | deprecated
date_proposed: 2026-04-21
date_accepted: null             # populat la flip la accepted
date_implemented: null          # populat la flip la implemented
supersedes: null                # id ADR dacă înlocuiește o decizie
superseded_by: null             # id ADR dacă a fost înlocuit
research-waiver: null           # DOAR dacă ADR-ul nu are research: motivul (decizie PO, fondator, fast-path). Chain-lint cere link [[research]] SAU waiver la accepted/implemented
tags: [decision, {project}]
---
```

## Plan

```yaml
---
type: plan
title: Short description
status: active                  # draft | active | completed | abandoned
started: 2026-04-22
completed: null                 # populat la completion
abandoned_reason: null          # populat dacă abandoned
related_adrs: [adr-id]
tags: [plan, {project}]
---
```

## Session note

```yaml
---
type: session
date: 2026-04-21
duration: ~3h
related_plans: [plan-filename]
related_adrs: [adr-id]          # forma scurtă (ADR-006), un stil per proiect
tags: [session, {project}]
# Câmpuri de outcome (opționale; audit metodologie 2026-07-05 — semnalul
# că metodologia produce rezultate, nu doar conformare):
decision_reversed: null         # id ADR ajuns superseded/deprecated în fereastră
rework_caused_by: null          # link plan/ADR care a cauzat rework în sesiune
defect_from_skipped_step: null  # pas de metodologie sărit care a produs defect
---
```

## Log viu în decisions/ (ex. decision-log.md)

Un fișier din `decisions/` care NU e ADR (log append-only de micro-decizii)
poartă frontmatter minimal ca să fie clasificat, nu exceptat:

```yaml
---
type: decision-log
status: active                  # e un log viu; nu are lifecycle de ADR
tags: [decisions, {project}]
---
```

Chain-lint lasă orice status în afara lifecycle-ului de ADR să treacă
silențios — deci WARN-ul „no status field" apare DOAR la fișiere
neclasificate, exact ce trebuie să prindă. Nu se exclud filename-uri din
scanare (pattern stabilit la AQOS, 2026-07-05, primul WARN real al lint-ului).

## current-state.md

**Fără frontmatter.** E un index, nu un document. Doar
`**Ultima actualizare:** YYYY-MM-DD` în antet. Structura-model: vezi orice
`context/{project}/current-state.md` existent.

## De ce nu merge fără disciplină (rationale, istoric)

- **„Pun tot în current-state"** → 1000+ linii, nimeni nu citește, drift
  (incident real: 150+ linii de narrative acumulate într-un proiect, 2026-04).
- **„ADR-ul e vechi, îl rescriu"** → pierzi „de ce NU X?" peste 6 luni.
- **„Planul e done, îl șterg"** → link-uri rupte, pierzi traceability.
- **„Fac totul sesiunea următoare"** → cleanup-ul devine task major.

## Ce rămâne FLEXIBIL

- Session notes opționale pentru work trivial.
- Numerotare ADR strictă (`ADR-007`) sau slug-based — un stil per proiect.
- Numele priorităților din Backlog pot diferi per proiect.
- Template-urile pot fi adaptate per proiect dacă frontmatter-ul respectă
  schema.
