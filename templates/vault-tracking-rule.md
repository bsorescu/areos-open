<!-- Public copy of the vault tracking rule. Install it as an always-on rule:
     cp templates/vault-tracking-rule.md ~/.claude/rules/vault-tracking.md
     Romanian; a translation is a welcome first contribution. -->
# Obsidian Project Tracking Rule

Context pattern pentru proiecte documentate în vault-ul Obsidian
(`~/Documents/obsidian-claude/`, un folder per proiect). Schemele de
frontmatter + rationale: `~/Documents/obsidian-claude/templates/frontmatter-schemas.md`
— se citește DOAR la crearea unui ADR/plan/session note (split 2026-07-05).

## Principiul zero: o informație = un fișier

Dacă același fapt apare în 2 locuri, **va** diverge. Alege SSOT-ul pentru
fiecare tip de informație și link-uiește, nu duplica.

## Ierarhia de fișiere

| Fișier | Răspunde la | Mutabilitate |
|---|---|---|
| `context/{project}/current-state.md` | „Unde suntem acum?" | Rescris frecvent; **max 16 KB** (se injectează la session start — peste, se taie tăcut de la coadă); snapshot + pointers, fără narrative |
| `decisions/ADR-*.md` | „De ce am ales X?" | Imutabil după `accepted`; excepții: flip `status`, addendum datat append-only. Nu rescrii, nu ștergi. |
| `plans/YYYY-MM-DD-*.md` | „Cum executăm X?" | Mutabil cât e `active`; la `completed`/`abandoned` → `plans/archive/` |
| `sessions/YYYY-MM-DD-*.md` | „Ce am făcut în ziua X?" | Append-only |
| `architecture/*.md` | „Cum funcționează sistemul?" | Refresh la refactor-uri mari |

## Tranziții de status

```
ADR:   proposed → accepted → implemented
                           ↘ superseded (înlocuit de alt ADR) ↘ deprecated
Plan:  draft → active → completed | abandoned  → mut în plans/archive/
```

**Regula critică pentru pivoturi:** nu ștergi/rescrii ADR-ul vechi — creezi
unul nou care `supersedes`. Istoricul deciziilor abandonate e valoros.

## Cele 4 cazuri de schimbare mid-flight (plan activ)

| Schimbare | Ce modifici | Ceremonie |
|---|---|---|
| Tweak tehnic (nu schimbă scope) | doar planul, inline | zero |
| Task descoperit | plan → `## Discovered during execution` | mențiune în session note |
| Scope expansion | task în plan SAU plan nou (după ship independence) | eventual plan nou |
| Pivot arhitectural | ADR nou care `supersedes`; plan vechi `abandoned` + plan nou | ADR + plan nou |

## Checklist la finalul sesiunii (~2 min)

1. Cod merge-uit azi? → update current-state (Active Work / Recently Shipped)
2. Decizie nouă? → ADR (`accepted`/`proposed`)
3. ADR devenit realitate? → flip `implemented` + dată
4. ADR flip la `superseded`? → notează în session note dacă research-ul
   original ar fi prezis inversarea (semnal de outcome, nu doar conformare)
5. Plan completat? → flip + mută în archive/ · Plan activ? → update checkboxes
6. Session note dacă s-a întâmplat ceva non-trivial (+ câmpurile de outcome
   din schemă, când se aplică). Fricțiunea pe un skill → secțiune
   `## Fricțiune {skill}`; kernel-ul AREOS o recoltează mecanic la
   următoarea lui sesiune (hook harvest-friction), NU trebuie propagată
   manual. Fricțiune pe skill terț (superpowers etc.): tot acolo — AREOS
   decide overlay sau issue upstream.
7. **Bugetul current-state — măsoară, nu estima:** `wc -c` pe current-state.
   Peste 16 KB ⇒ **taie înainte de commit**. Bugetul e pe secțiune, nu pe
   total: un total îți spune că ai depășit, nu ce să tai.
   - **Active Work: ≤ 5 itemuri × ~12 linii** (~5 KB). Fapte, cifre, blocaje,
     pointer — **zero argumentație**. Raționamentul stă în session note;
     dublat aici, e principiul zero încălcat, iar octeții sunt doar simptomul.
   - **Recently Shipped: ≤ 5 intrări**, o linie + link fiecare.
   - **Backlog:** itemele închise se scot, nu se marchează.
   - Restul (Sisteme LIVE, Reguli, Infrastructură, Known Issues) descriu
     sistemul — cresc doar când crește sistemul, nu la fiecare sesiune.
   Primele trei sunt singurele care cresc implicit: dacă fișierul a depășit,
   acolo e. Fiecare sesiune adaugă; dacă niciuna nu scade, plafonul cedează
   în ~3 sesiuni (măsurat pe un proiect-client, 2026-07).
   - **Excepția: descrierea de sistem domină (ADR-011).** Dacă secțiunile de
     descriere de sistem depășesc ~50% din fișier, sau a doua tăiere
     consecutivă nu atinge cele trei secțiuni de mai sus, tăierile sunt
     paliative — aplică split-ul pe domenii: current-state devine index
     (Active Work, ce urmează, pointeri de o linie + **data ultimei
     atingeri**), iar starea per subsistem merge în
     `context/{proiect}/<domeniu>.md` (cu problemele cunoscute ale
     domeniului lângă contextul lor), citită la cerere. Nu preventiv.
     Restructurarea cere confirmarea userului ȘI actualizarea pointerilor
     din CLAUDE.md-urile afectate, în aceeași schimbare (măsurători pe un
     proiect de infrastructură 2026-08; precedent negativ: un split unilateral, revertat).

## Git în vault: un singur repo, mai mulți agenți în paralel

Proiectele de cod sunt repo-uri separate. **Vaultul nu**: `~/Documents/obsidian-claude`
e UN repo cu un folder per proiect, în care scriu simultan sesiuni din proiecte
diferite. Ce vezi `modified` poate fi munca altcuiva, în desfășurare.

**Din Git 2.0, `git add -A` / `git add -u` fără cale stagiază tot repo-ul,
indiferent de directorul curent.** De aici vin commit-urile care ating două
proiecte. (Confirmat empiric 2026-08: patru commit-uri au trecut doar fiindcă
celălalt folder era curat în acel moment.)

- **Stagiază explicit, cu cale:** `git add {proiect}/…` sau `git add -A .` din
  folderul proiectului. Niciodată `git add -A` / `git add .` fără cale.
- **Commit-ul atinge un singur folder de proiect.** Un pre-commit hook refuză
  altfel — e plasă de siguranță, nu permisiune să te bazezi pe el.
- **La refuz, NU da `git reset`** — de-stagiază și munca celorlalte sesiuni.
  Adaugă doar fișierele tale (`git add {proiect}/…`) și comite.
- **Nu atinge fișiere din alte foldere de proiect**: fără `stash`, `restore`,
  `checkout .`, `clean`. Dacă un commit e blocat de starea altcuiva, spune-i
  ownerului; nu „rezolva".
- Înainte de `push`, `git pull --rebase` dacă remote-ul a avansat. Fără `--force`.

## Pentru Claude Code

- **La început de sesiune:** citește `context/{project}/current-state.md`
  înainte de orice (dacă un hook a injectat-o deja, NU o re-citi).
- **În timpul lucrului:** aplică regula celor 4 cazuri mid-flight.
- **La final:** rulează checklist-ul; cere confirmare înainte să muți/arhivezi
  fișiere. Nu aplica regula doar dacă userul zice explicit să o ignori.
