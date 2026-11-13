#!/usr/bin/env bash
# Test for scripts/pick_columns.sh. Run from this folder: bash check_pick_columns.sh
set -u
cd "$(dirname "$0")"; P=../scripts/pick_columns.sh; fail=0
t() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (got '$3', want '$2')"; fail=1; fi; }
out=$($P md/spec-form.md "type,name,label::english,relevant,constraint" survey 2>/dev/null)
t "keeps the chosen columns" "| # | type | name | label::English | relevant | constraint |" "$(echo "$out" | sed -n 2p)"
t "blanks NaN cells" "0" "$(echo "$out" | grep -c NaN)"
t "restores underscores" "0" "$(echo "$out" | grep -c '\\_')"
t "numbers the data rows" "| 8 | integer | hh_age | B1 How old is the child in completed years? |  | .>=0 and .<=17 |" "$(echo "$out" | grep '| hh_age |')"
t "relevance alias" "| 10 | select_one yesno | hh_school | B3 Is the child enrolled in school? | \${hh_age}>=6 |  |" "$(echo "$out" | grep '| hh_school |')"
c=$($P md/spec-form.md "list_name,value,label" choices 2>/dev/null | grep -c "| sex |")
t "reads the choices sheet and a language-less label" "2" "$c"
t "value falls back to a name column" "| 1 | yesno | 1 | Yes |" "$($P md/programmed-form.md "list_name,value,label" choices 2>/dev/null | sed -n 4p)"
t "reports a missing column" "pick_columns: no column nonexistent in sheet survey" "$($P md/spec-form.md "name,nonexistent" survey 2>&1 >/dev/null)"
[ $fail = 0 ] && echo "All tests passed." || { echo "Some tests failed."; exit 1; }
