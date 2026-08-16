# Handbook: research-methodology

De ce există skill-ul, ce decizii l-au format, ce s-a respins. Sursa
regulilor rămâne skill-ul însuși (ADR-002); capitolul explică.

## De ce există

Componenta definitorie AREOS (design spec 2026-07-03): fără el, deciziile de
arhitectură se iau din impresii și memoria modelului. Completează lanțul
superpowers cu veriga lipsă: **research → brainstorming → plan →
implementare → review**. O regulă simplă îl rezumă: nicio alegere de
tehnologie pe care echipa să n-o poată re-citi peste 6 luni și să aibă
încredere în ea.

## Deciziile care l-au format

- **ADR-002 (executable-first):** skill, nu capitol de manual. Validat pe o
  sarcină reală înainte să intre în kernel (Sprint 0: research-ul
  „metodologii AI-assisted engineering", 14 candidați, 20 de agenți).
- **ADR-005/ADR-009:** execuția rutează pe tier-uri — fan-out de descoperire
  pe modele ieftine (T2), sinteză + verificare adversarială pe frontier (T5).
- **ADR-008:** verificarea independentă = subagent Claude cu context
  proaspăt, nu model extern.

## Istoria iterațiilor (totul din fricțiune reală, nimic speculativ)

- **v1 (Sprint 0):** procesul în 5 pași + template-uri. Chiar la prima
  rulare, criticul de completitudine (improvizat atunci) a prins constatarea
  cea mai valoroasă a research-ului: `rules/` nu era încărcat la runtime —
  contradicție între grile pe care niciun agent individual n-o văzuse.
- **v2 (2026-07-04, cele 5 fricțiuni din Sprint 0):** verificarea
  adversarială a afirmațiilor load-bearing a devenit obligatorie (Step 4);
  criticul de completitudine a devenit Step 4.5 formal, cu buclă până la
  „nimic material"; igiena metricilor volatile (`valoare @ dată-citire`);
  agregarea pe modalitate pentru sweep-uri 20+ surse; fast-path pentru
  decizii mici, reversibile.
- **v3 (2026-07-05, fricțiunea din research-ul de harness):** grila
  technology-evaluation nu se potrivea deciziilor de structură/proces —
  variantă documentată (aceleași criterii, opțiuni per cluster); regula
  „eșantionul e triaj, nu verificare" cu gate obligatoriu de verificare
  completă.

## Ce s-a respins și de ce

- **Handbook-first** (16 capitole scrise în avans) — ADR-002: documentația
  neîncărcată de niciun tool driftează și moare.
- **Proces complet obligatoriu pentru orice decizie** — fast-path-ul există
  exact pentru decizii reversibile și ieftine; validat prima dată la
  ADR-009 (~15 min, 2 surse, fără escaladare).
- **Eval harness cross-vendor** — amânat (ADR-005): feedback loop ieftin din
  session notes în locul unui sub-proiect de benchmarking.

## Dovada că funcționează (empiric, nu declarativ)

Criticul de completitudine a produs constatări decisive în 3 sesiuni
consecutive (log: vault `areos/model-observations.md`) — e singurul pas de
proces care a prins de fiecare dată ceva ce agentul principal ratase.
