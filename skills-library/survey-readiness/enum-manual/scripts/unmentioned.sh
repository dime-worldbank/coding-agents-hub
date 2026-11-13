#!/usr/bin/env bash
# List the form questions a manual does not mention by name.
# Usage: unmentioned.sh manual.md survey.md
#   survey.md is the reduced form made by pick_columns.sh (columns # | type | name | ...).
#   Groups, notes, calculate fields and metadata fields are skipped. A question counts as mentioned if its
#   name appears as a whole word in the manual. A manual may describe several questions together, so treat
#   the list as questions to look at, not as errors.
set -eu
[ $# -eq 2 ] || { sed -n 2,7p "$0" | sed 's/^# \{0,1\}//'; exit 1; }
total=0; miss=0
while read -r n; do
  total=$((total + 1))
  grep -qiw -- "$n" "$1" || { echo "$n"; miss=$((miss + 1)); }
done < <(awk -F'|' 'NR>2 && $2 !~ /---/ { t=$3; gsub(/^ +| +$/, "", t); split(t, a, " "); b=a[1]
  if (b=="begin" || b=="end" || b=="note" || b ~ /^calculate/ || b=="start" || b=="deviceid" || b=="subscriberid" || b=="simserial" || b=="phonenumber" || b=="username" || b=="audit" || b=="comments") next
  n=$4; gsub(/ /, "", n); if (n != "") print n }' "$2")
echo "# $((total - miss)) of $total questions mentioned by name" >&2
