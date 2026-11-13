Spec test survey

Paper version for test workflows, English labels

# Module A Introduction   [mod_a_intro]

A1   enumerator_id   select_one enumerator   Required

A1: Enumerator: What is your name?

○  id  	name

Choices are loaded at run time from enumerators.csv (search appearance); the list above is only the structure.

Appearance:  search('enumerator_list')

A2   consent   select_one yesno   Required

A2: Do you agree to take part in this survey?

○  1   	Yes

○  0   	No

# Module B Household   [mod_b_hh]

Ask whole group if:  ${consent}=1

B1   hh_age   integer   Required

B1: How old is the child in completed years?

Constraint:  .>=0 and .<=18

Constraint message:  Age must be between 0 and 17.

B2   hh_sex   select_one sex   Required

B2: What is the child's sex?

○  1   	Boy

○  2   	Girl

○  3   	Other

B3   hh_school   select_one yesno   Required

B3: Is the child enrolled in school?

○  1   	Yes

○  0   	No

Ask if:  ${hh_age}>=5

B5   hh_meals   integer   Required

B5: In the past 7 days, how many days did the child eat a school meal?

Constraint:  .>=0 and .<=7

Constraint message:  Enter 0 to 7.

B4   hh_grade   integer   Required

B4: Which grade is the child in?

Ask if:  ${hh_school}=1

Constraint:  .>=1 and .<=8

Constraint message:  Grade must be 1 to 8.

B6   hh_siblings   integer   Required

B6: How many siblings does the child have?

# Module C Health   [mod_c_health]

Ask whole group if:  ${consent}=1

C1   hl_illness   select_one yesno   Required

C1: Was the child ill in the last 2 weeks?

○  1   	Yes

○  2   	No

C2   hl_clinic   select_one yesno   Required

C2: Did the child visit a clinic?

○  1   	Yes

○  0   	No

Ask if:  ${hl_ill}=1

C3   hl_cost   text   Required

C3: How much did the visit cost in total?

Ask if:  ${hl_clinic}=1

Constraint:  .>=0

Constraint message:  Enter a positive amount.

# Calculate fields

| # | Name | Calculation | Relevance | Section |
| --- | --- | --- | --- | --- |
| 1 | age_group (here) | if(${hh_age}<5,1,2) |  |  |