## survey
| type | name | label::English | label::French | required | relevant | constraint | calculation | choice\_filter | publishable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| text | hh\_id | Household ID | ID du menage | yes | NaN | NaN | NaN | NaN | NaN |
| begin group | demo | Demographics | Demographie | NaN | NaN | NaN | NaN | NaN | NaN |
| integer | age | Age of respondent | Age | NaN | NaN | NaN | NaN | NaN | NaN |
| select\_one sex | sex | Sex | Sexe | yes | NaN | NaN | NaN | NaN | NaN |
| select\_multiple assets | assets | Which assets does the household own? | Quels biens? | yes | NaN | NaN | NaN | NaN | NaN |
| text | phone | Phone number | Telephone | NaN | NaN | NaN | NaN | NaN | yes |
| integer | n\_goats | How many goats? | Combien de chevres? | NaN | ${assets}='goat' | NaN | NaN | NaN | NaN |
| decimal | goat\_ratio | NaN | NaN | NaN | NaN | NaN | ${n\_goats} div ${n\_sheep} | NaN | NaN |
| text | first\_name | First name | Prenom | yes | ${resp\_edu}!='' | NaN | NaN | NaN | NaN |
| note | wait\_note | Please wait for the supervisor | NaN | yes | NaN | NaN | NaN | NaN | NaN |
| select\_one occupation | job | Main occupation | Profession principale | yes | NaN | NaN | NaN | NaN | NaN |
| select\_one regions | region | Region | Region | yes | NaN | NaN | NaN | NaN | NaN |
| calculate | note\_pos | NaN | NaN | NaN | NaN | NaN | position(..) | NaN | NaN |
| select\_one edu | resp\_edu | Highest education | NaN | yes | NaN | NaN | NaN | NaN | NaN |
| integer | age | Age (repeat) | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| end group | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| begin group | consent\_grp | Consent | Consentement | NaN | NaN | NaN | NaN | NaN | NaN |
| select\_one yesno | consent | Do you agree to take part? | Etes-vous d'accord? | yes | NaN | NaN | NaN | NaN | NaN |
| end group | consent\_grp | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## choices
| list\_name | name | label::English | label::French |
| --- | --- | --- | --- |
| sex | 1 | Male | Homme |
| sex | 2 | Female | Femme |
| assets | goat | Goat | Chevre |
| assets | none | NaN | Aucun |
| assets | dk | Don't know | Ne sait pas |
| occupation | Farmer | Farmer | Agriculteur |
| occupation | Factory Worker | Factory worker | Ouvrier |
| edu | 1 | NaN | Aucune |
| edu | 2 | Primary | Primaire |
| edu | 2 | Secondary | Secondaire |
| yesno | 1 | Yes | Oui |
| yesno | 0 | No | Non |
| unused\_list | 1 | Spare | Spare |

## settings
| form\_title | form\_id | version |
| --- | --- | --- |
| Planted errors test form | planted\_test | 1 |