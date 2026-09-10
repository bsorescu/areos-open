#!/bin/bash
# Friction harvest (AREOS kernel sessions only). The growth loop broke at
# HARVESTING, not logging: client projects log friction / model observations
# / outcome fields faithfully, but nothing carried them back into the kernel
# (gap review 2026-09-10: 7 friction sections + 6 iteration proposals sat
# unharvested since the last skill iteration on 2026-08-05).
#
# Called from session-start.sh when SLUG=areos. Scans every project's session
# notes modified after the marker and injects a compact digest into context —
# the kernel session can no longer fail to see them. Advance the marker with:
#   touch "$AREOS_VAULT_ROOT/areos/.last-harvest"   (after harvesting)
set -u
VAULT_ROOT="${AREOS_VAULT_ROOT:-$HOME/Documents/obsidian-claude}"
MARKER="$VAULT_ROOT/areos/.last-harvest"
[ -d "$VAULT_ROOT" ] || exit 0

if [ -f "$MARKER" ]; then
  newer=(-newer "$MARKER"); since="since $(date -r "$MARKER" +%Y-%m-%d)"
else
  newer=(); since="all time (no marker yet)"
fi

# session notes from every project EXCEPT areos itself (kernel notes are not
# client friction), modified after the marker
files=$(find "$VAULT_ROOT" -path '*/sessions/*.md' -not -path "$VAULT_ROOT/areos/*" \
        -not -path '*/.obsidian/*' ${newer[@]+"${newer[@]}"} 2>/dev/null | sort)
[ -z "$files" ] && exit 0

fric=0; obs=0; outc=0; digest=""
while IFS= read -r f; do
  rel=${f#"$VAULT_ROOT/"}
  # friction sections: "## Fricțiune <skill>" (any spelling of the header)
  while IFS=: read -r ln hdr; do
    fric=$((fric+1)); skill=$(printf '%s' "$hdr" | sed -E 's/^## [Ff]ric[țt]iune[[:space:]]*//; s/^[\/ ]*//')
    digest+="  [friction:${skill:-general}] $rel:$ln"$'\n'
  done < <(grep -nE '^## [Ff]ric' "$f" 2>/dev/null)
  # model observations
  while IFS=: read -r ln _; do
    obs=$((obs+1)); digest+="  [model-obs] $rel:$ln"$'\n'
  done < <(grep -nE '^## Model [Oo]bservations' "$f" 2>/dev/null)
  # non-null outcome fields (frontmatter)
  while IFS= read -r line; do
    outc=$((outc+1)); digest+="  [outcome] $rel: $line"$'\n'
  done < <(grep -E '^(decision_reversed|rework_caused_by|defect_from_skipped_step):' "$f" 2>/dev/null | grep -vE ':[[:space:]]*(null|"")[[:space:]]*$')
done <<< "$files"

total=$((fric+obs+outc))
[ "$total" = 0 ] && exit 0
echo "### Unharvested client signal ($since): $fric friction, $obs model-obs, $outc outcome"
echo "Kernel iteration input — read, act (skill iteration / model-observations.md / cut), then: touch areos/.last-harvest"
printf '%s' "$digest" | sort | head -60
[ "$(printf '%s' "$digest" | wc -l)" -gt 60 ] && echo "  … (truncated; run harvest-friction.sh directly for the full list)"
exit 0
