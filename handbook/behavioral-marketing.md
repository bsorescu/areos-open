# Handbook: behavioral-marketing

De ce există skill-ul, ce l-a format, ce s-a respins. Sursa regulilor:
skill-ul (ADR-002); capitolul explică.

## De ce există

Marketing bazat pe research-ul de biasuri (Richard Shotton), împachetat
într-un workflow trasabil în 7 etape. Teza centrală, plătită empiric (vezi
RED mai jos): **persuasiunea amplifică orice atinge** — fără proces, un
model amplifică și claim-uri fabricate, cu aceeași fluență. Skill-ul nu face
modelul „mai convingător"; îl face convingător *doar pe adevăr documentat*.

## Momentul fondator: baseline-ul RED (2026-07-04)

TDD per writing-skills + regula skill-authoring, două baseline-uri fără
skill (sonnet):

- **Scenariul A** (presiune „conversions at any cost", client B2B real):
  modelul a inventat „early-access pricing… renews at standard rate" — o
  creștere de preț inexistentă în brief — și a raționalizat-o verbatim ca
  „true urgency, not manufactured scarcity". Zero livrabile, proces sărit
  integral.
- **Scenariul B** (trial-to-paid): proces improvizat rezonabil, dar
  nereproductibil, fără ethical pass, livrabil pierdut în scratchpad.
- **GREEN (re-test A cu skill-ul):** etape comprimate, nu sărite; fapte
  extrase din vault-ul real al proiectului; refuzuri explicite — ROI intern
  neprezentabil ca outcome, fake scarcity, numirea clientului fără
  consimțământ; urgența doar din deadline-ul legal, sursat.

Diferența RED→GREEN este justificarea întregului skill: guardrails-urile nu
sunt decor etic, sunt ce separă output-ul de un generator de dark patterns.

## Deciziile de design

- **Scope gate spre research-methodology:** skill-ul optimizează execuția
  unei strategii, nu o validează — deciziile majore de positioning/pricing
  trec întâi prin research (compunerea gate-urilor, regula de precedență).
- **„Shrink, never skip":** sub presiune de deadline, o etapă se comprimă la
  minute, nu se sare — etapele sărite sunt exact cum se nasc claim-urile
  fabricate (lecția RED-ului).
- **Fiecare recomandare = experiment** (ICE-scored, o metrică primară + una
  de guardrail) — altfel skill-ul produce opinii, nu învățare.
- **Calibrare separată de proces** (references/): awareness, ton, B2B
  reglementat, localizare RO/EU — catalogul de biasuri include explicit
  contraindicațiile fiecăruia.

## Istoria

- **v1:** prima versiune, fără references/, validată pe task-urile reale
  ale unui proiect-client; 5 fricțiuni acumulate în backlog.
- **v2 (2026-07-04):** cele 5 puncte + addendum de 15 de la PO (playbooks
  per tip de task, diagnostic obligatoriu, objection matrix, claim
  verification, scorecard, integrarea research-methodology) — scope
  expansion absorbit în aceeași rescriere; mutat în kernel cu symlink.

## Ce s-a respins

- **Skill de „copywriting persuasiv" fără workflow** — exact ce a produs
  baseline-ul RED: fluență fără adevăr.
- **Umor/rimă ca default** — permise doar cu contraindicațiile citate
  (B2B reglementat: sobru, per references/b2b-compliance.md).

## Notă de ownership

Primul skill de *domeniu* din kernel (restul sunt metodologie). Decizia de
a-l ține aici: un singur loc, aceeași disciplină (TDD, chain-lint, friction
log). Dacă skill-urile de domeniu se înmulțesc, split-ul repo-ului e o
decizie mecanică de moment — vezi discuția din 2026-07-05.
