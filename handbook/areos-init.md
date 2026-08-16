# Handbook: areos-init

De ce există skill-ul, ce l-a format, ce s-a respins. Sursa regulilor:
skill-ul (ADR-002); capitolul explică.

## De ce există

Fiecare proiect nou plătea un bootstrap manual nereproductibil: folder de
vault, current-state, CLAUDE.md de proiect, hooks, wiring. Primul
proiect-client AREOS a făcut totul de mână (vault-ul corect, repo-ul
deloc), iar auditul de metodologie din 2026-07-05 a numit problema mai
general: topologia single-machine/single-operator era load-bearing și
nescrisă. areos-init face onboarding-ul un pas executabil, idempotent.

## Deciziile de design

- **Hooks portabile în loc de parametrizare:** scripturile își derivă
  slug-ul proiectului la runtime (lowercase basename repo, override prin
  `.claude/areos-project`), deci skill-ul le copiază *verbatim*. Alternativa
  respinsă — copii parametrizate cu sed — ar fi însemnat n copii divergente
  ale aceleiași logici; verbatim = un singur comportament de întreținut.
- **Idempotent, never-overwrite:** orice fișier existent e raportat și
  sărit. A permis rularea pe un proiect real la mijlocul unei sesiuni active, peste un
  vault deja bootstrapped, cu zero risc.
- **`disable-model-invocation: true`** (regula skill-authoring): scaffolding
  = side effects; doar userul decide când un proiect intră pe AREOS.
- **Verify obligatoriu în skill:** hook rulat manual, chain-lint, JSON valid
  — plus onestitatea că proba completă e abia sesiunea următoare (hooks și
  CLAUDE.md se încarcă la startup).
- **Nu copiază regula de tracking:** proiectul o moștenește din
  `~/.claude/rules/` — o instrucțiune, un mecanism (ADR-006).

## Validare (gate-ul TDD-for-skills)

1. Gap-analysis contra bootstrap-ului real al primului proiect-client (ce făcuse manual sesiunea
   aia vs ce ar fi generat skill-ul) — a definit conținutul pașilor.
2. Test pe repo simulat: hooks-urile copiate au derivat corect slug-ul și
   au citit vault-ul lui; chain-lint a semnalat din prima o inconsistență
   reală (un log viu fără frontmatter de status).
3. **Prima rulare reală: 2026-07-05** (pe primul proiect-client, în repo-ul
   lui) — idempotență confirmată (zero suprascrieri), verify complet,
   WARN-ul așteptat și doar el.

## Ce s-a respins

- Copii de hooks parametrizate per proiect (drift garantat).
- `git init` automat fără întrebare (repo-ul poate exista deja — la prima rulare exista).
- Extensia pentru mașini/operatori noi — rămâne P2, se construiește la
  prima nevoie reală, nu speculativ.
