#!/usr/bin/env bash
# Tests for pick_columns.sh and unmentioned.sh. Run from this folder: bash check_scripts.sh
set -u
cd "$(dirname "$0")"; fail=0
t() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (got '$3', want '$2')"; fail=1; fi; }
../scripts/pick_columns.sh md/form.md "type,name,label::english,relevant,constraint,required" survey > /tmp/_s.md 2>/dev/null
t "keeps the chosen columns" "| # | type | name | label::English | relevant | constraint | required |" "$(sed -n 2p /tmp/_s.md)"
t "blanks NaN cells" "0" "$(grep -c NaN /tmp/_s.md)"
t "all questions of the complete manual are mentioned" "" "$(../scripts/unmentioned.sh manual-ok.md /tmp/_s.md 2>/dev/null)"
t "questions missing from the incomplete manual are listed" "hh_sex hh_grade hh_meals hl_ill hl_clinic hl_cost hl_vaccine" "$(../scripts/unmentioned.sh manual-gaps.md /tmp/_s.md 2>/dev/null | tr '\n' ' ' | sed 's/ $//')"
t "count is reported" "# 4 of 11 questions mentioned by name" "$(../scripts/unmentioned.sh manual-gaps.md /tmp/_s.md 2>&1 >/dev/null)"
t "metadata and groups are skipped" "0" "$(../scripts/unmentioned.sh manual-gaps.md /tmp/_s.md 2>/dev/null | grep -cw 'start\|mod_a_intro\|age_group')"
[ $fail = 0 ] && echo "All tests passed." || { echo "Some tests failed."; exit 1; }
