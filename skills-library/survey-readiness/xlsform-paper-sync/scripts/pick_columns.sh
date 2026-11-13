#!/usr/bin/env bash
# Keep only chosen columns of the Markdown tables that markitdown makes from an XLSForm.
# Usage: pick_columns.sh form.md "type,name,label::english,relevant,constraint" [sheet]
#   Column names are matched without case, with spaces as underscores. "label" with no language matches the
#   first label:: column (not label::stata). "relevant" also matches "relevance". Missing columns are reported
#   on stderr. A "#" column counts the data rows in each sheet (spreadsheet row is about # + 1).
#   NaN cells print empty and escaped underscores are restored. Rows with no type and no name are dropped.
#   "value" falls back to a "name" column, because a choices sheet may use either.
# Plain shell and awk. It changes no file: output goes to the screen.
set -eu
[ $# -ge 2 ] || { sed -n 2,9p "$0" | sed 's/^# \{0,1\}//'; exit 1; }
awk -v want="$2" -v only="${3:-}" '
function norm(s) { gsub(/^ +| +$/, "", s); s = tolower(s); gsub(/\\_/, "_", s); gsub(/ /, "_", s); return s }
function clean(s) { gsub(/^ +| +$/, "", s); if (s == "NaN" || s == "nan") s = ""; gsub(/\\_/, "_", s); return s }
BEGIN { nw = split(want, W, ","); for (i = 1; i <= nw; i++) W[i] = norm(W[i]) }
/^## / { sheet = substr($0, 4); intable = 0; skip = (only != "" && norm(sheet) != norm(only)); if (!skip) print; next }
/^\|/ {
  if (skip) next
  n = split($0, C, "|")
  if (!intable) {
    intable = 1; rows = 0; nsel = 0
    for (j = 1; j <= nw; j++) {
      f = 0
      for (k = 2; k < n; k++) { h = norm(C[k]); if (h == W[j] || (W[j] == "relevant" && h == "relevance") || (W[j] == "label" && h ~ /^label::/ && h !~ /stata/ && !f)) { f = k; break } }
      if (!f && W[j] == "value") { for (k = 2; k < n; k++) if (norm(C[k]) == "name") { f = k; break } }
      if (f) { sel[++nsel] = f; names[nsel] = W[j] } else print "pick_columns: no column " W[j] " in sheet " sheet > "/dev/stderr"
    }
    line = "| #"; sep = "|---"
    for (j = 1; j <= nsel; j++) { line = line " | " clean(C[sel[j]]); sep = sep "|---" }
    print line " |"; print sep "|"
    next
  }
  if ($0 ~ /^\| *-/) next
  rows++
  out = ""; has = 0
  for (j = 1; j <= nsel; j++) { v = clean(C[sel[j]]); if ((names[j] == "type" || names[j] == "name" || names[j] == "list_name" || names[j] == "value") && v != "") has = 1; out = out " | " v }
  if (has || nsel == 0) print "| " rows out " |"
  next
}
{ intable = 0 }
' "$1"
