#!/bin/bash
# Falsifiable security test. Each corpus sample is applied as an EDIT to a
# real skill path (skills/victim/SKILL.md) in a throwaway git repo, then
# linted through the CI code path (`--base`). This is what a fork PR actually
# does — and the shape (edit to existing skill) that defeated the first lint.
#   L1-must-fail/   -> must FAIL at L1
#   should-pass/    -> must be clean
#   L2-must-catch/  -> must PASS L1 by design (no capability change); L2 (the
#                      model reviewer) is what catches these, not L1.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d); fail=0
git -C "$TMP" init -q
mkdir -p "$TMP/skills/victim" "$TMP/.github"
cp "$ROOT/scripts/contribution-lint.py" "$TMP/lint.py"
cp "$ROOT/.github/allowed-domains.txt" "$TMP/.github/"
printf -- '---\nname: victim\ndescription: seed.\n---\nseed body\n' \
  > "$TMP/skills/victim/SKILL.md"
git -C "$TMP" add -A && git -C "$TMP" commit -qm base
BASE=$(git -C "$TMP" rev-parse HEAD)

run() { # $1 = sample file, $2 = expect (fail|clean)
  cp "$1" "$TMP/skills/victim/SKILL.md"
  git -C "$TMP" commit -qam edit
  out=$(cd "$TMP" && python3 lint.py --base "$BASE" 2>/dev/null)
  git -C "$TMP" reset -q --hard "$BASE"
  hit=$(echo "$out" | grep -c '^FAIL')
  name=$(basename "$1")
  if [ "$2" = fail ] && [ "$hit" -gt 0 ]; then echo "ok   FAIL as required: $name"
  elif [ "$2" = clean ] && [ "$hit" = 0 ]; then echo "ok   clean as required: $name"
  else echo "MISS ($2 expected, $hit FAILs): $name"; echo "$out" | grep '^FAIL' | sed 's/^/       /'; fail=1; fi
}

for f in "$ROOT"/tests/injection-corpus/L1-must-fail/*.md;  do run "$f" fail;  done
for f in "$ROOT"/tests/injection-corpus/should-pass/*.md;   do run "$f" clean; done
for f in "$ROOT"/tests/injection-corpus/L2-must-catch/*.md; do run "$f" clean; done
rm -rf "$TMP"
[ "$fail" = 0 ] && echo "CORPUS: all assertions hold" || echo "CORPUS: FAILURES above"
exit "$fail"
