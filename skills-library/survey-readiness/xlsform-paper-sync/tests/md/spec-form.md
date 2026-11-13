## survey
| type | name | label::English | label::French | relevant | constraint | constraint message::English | required | appearance | question\_number | calculation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| calculate | age\_group | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | if(${hh\_age}<6,1,2) |
| start | start | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| begin group | mod\_a\_intro | Module A Introduction | Module A Introduction (fr) | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| select\_one\_from\_file enumerator\_list.csv | enumerator\_id | A1 Enumerator: What is your name? | A1 [fr] Enumerator: What is your name? | NaN | NaN | NaN | yes | search('enumerator\_list') | A1 | NaN |
| select\_one yesno | consent | A2 Do you agree to take part in this survey? | A2 [fr] Do you agree to take part in this survey? | NaN | NaN | NaN | yes | NaN | A2 | NaN |
| end group | mod\_a\_intro | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| begin group | mod\_b\_hh | Module B Household | Module B Household (fr) | ${consent}=1 | NaN | NaN | NaN | NaN | NaN | NaN |
| integer | hh\_age | B1 How old is the child in completed years? | B1 [fr] How old is the child in completed years? | NaN | .>=0 and .<=17 | Age must be between 0 and 17. | yes | NaN | B1 | NaN |
| select\_one sex | hh\_sex | B2 What is the child's sex? | B2 [fr] What is the child's sex? | NaN | NaN | NaN | NaN | NaN | B2 | NaN |
| select\_one yesno | hh\_school | B3 Is the child enrolled in school? | B3 [fr] Is the child enrolled in school? | ${hh\_age}>=6 | NaN | NaN | yes | NaN | B3 | NaN |
| integer | hh\_grade | B4 Which grade is the child in? | B4 [fr] Which grade is the child in? | ${hh\_school}=1 | .>=1 and .<=8 | Grade must be 1 to 8. | yes | NaN | B4 | NaN |
| integer | hh\_meals | B5 In the past 30 days, how many days did the child eat a school meal? | B5 [fr] In the past 30 days, how many days did the child eat a school meal? | NaN | .>=0 and .<=7 | Enter 0 to 7. | yes | NaN | B5 | NaN |
| end group | mod\_b\_hh | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| begin group | mod\_c\_health | Module C Health | Module C Health (fr) | ${consent}=1 | NaN | NaN | NaN | NaN | NaN | NaN |
| select\_one yesno | hl\_ill | C1 Was the child ill in the last 2 weeks? | C1 [fr] Was the child ill in the last 2 weeks? | NaN | NaN | NaN | yes | NaN | C1 | NaN |
| select\_one yesno | hl\_clinic | C2 Did the child visit a clinic? | C2 [fr] Did the child visit a clinic? | ${hl\_ill}=1 | NaN | NaN | yes | NaN | C2 | NaN |
| integer | hl\_cost | C3 How much did the visit cost in total? | C3 [fr] How much did the visit cost in total? | ${hl\_clinic}=1 | .>=0 | Enter a positive amount. | yes | NaN | C3 | NaN |
| select\_one yesno | hl\_vaccine | C4 Has the child been vaccinated? | C4 [fr] Has the child been vaccinated? | NaN | NaN | NaN | yes | NaN | C4 | NaN |
| end group | mod\_c\_health | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## choices
| list\_name | value | label::English | label::French |
| --- | --- | --- | --- |
| yesno | 1 | Yes | Yes (fr) |
| yesno | 0 | No | No (fr) |
| sex | 1 | Boy | Boy (fr) |
| sex | 2 | Girl | Girl (fr) |

## settings
| form\_title | form\_id | version |
| --- | --- | --- |