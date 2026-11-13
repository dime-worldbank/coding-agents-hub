# Reading test: specification-style files

One run, done by Claude following `references/comparison-method.md` on `md/spec-paper.md` and the reduced `md/spec-form.md`. This is a single reading test on a small invented pair, not a full evaluation.

Steps: the form was reduced with `pick_columns.sh "type,name,label::english,relevant,constraint,required,calculation"`. The paper was converted with `extract-text` (markitdown has no docx support in the test environment). Language: English (shared). Paper kind: specification style.

Result: all 13 planted differences were found by reading. No false alarms on the module-level conditions (consent = 1 on modules B and C, which match on both sides).

| Planted difference | Found | Needed column or sheet |
|---|---|---|
| B1 constraint `.<=18` on paper, `.<=17` in form | Yes | constraint |
| B2 "Other" on paper only | Yes | choices sheet |
| B2 required on paper, not in form | Yes | required |
| B3 skip `>=5` on paper, `>=6` in form | Yes | relevant |
| B5 7 days on paper, 30 in form | Yes | label |
| B4 and B5 swapped on paper | Yes | name order |
| B6 on paper only | Yes | name |
| C4 in form only | Yes | name |
| C1 name `hl_illness` vs `hl_ill` | Yes | name |
| C1 codes No = 2 vs 0 | Yes | choices sheet |
| C3 type text vs integer | Yes | type |
| age_group calculation `<5` vs `<6` | Yes | calculation (added only because the paper prints calculate fields) |
| Enumerator list file name differs | Yes | type |

What this does not show: how reliable the method is on a form of 1,000 rows, how many tokens it costs, or whether a long run skips a question. The ledger and count check exist for that. Test it on a large real pair before relying on it.

Word counts on this pair: converted form 788 words, reduced form 351 words.
