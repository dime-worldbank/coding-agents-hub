## survey
| type | name | label::English | hint | required | relevant | constraint |
| --- | --- | --- | --- | --- | --- | --- |
| start | start | NaN | NaN | NaN | NaN | NaN |
| end | end | NaN | NaN | NaN | NaN | NaN |
| deviceid | deviceid | NaN | NaN | NaN | NaN | NaN |
| begin group | consent | Consent | NaN | NaN | NaN | NaN |
| note | consent\_note | Hello, my name is [name]. I work for the Zandia Farm Advisory Study. We are asking farmers about their farming. The interview takes about 45 minutes and your answers are confidential. | NaN | NaN | NaN | NaN |
| select\_one yesno | consent | 1.1 Do you agree to take part in this survey? | NaN | yes | NaN | NaN |
| end group | consent | NaN | NaN | NaN | NaN | NaN |
| begin group | hh | Household | NaN | NaN | NaN | NaN |
| text | hh\_age | 2.1 What is your age in completed years? | NaN | yes | NaN | NaN |
| select\_one sex | hh\_sex | 2.2 What is your sex? | NaN | yes | NaN | NaN |
| select\_one edu | hh\_edu | 2.3 What is the highest level of education you have completed? | NaN | yes | NaN | NaN |
| end group | hh | NaN | NaN | NaN | NaN | NaN |
| begin group | farm | Farm practices | NaN | NaN | NaN | NaN |
| select\_one yesno | farm\_maize | 3.1 Did you grow maize in the last 12 months? | NaN | yes | NaN | NaN |
| decimal | farm\_ha | 3.2 How many hectares of maize did you plant? | NaN | yes | ${farm\_maize}=1 | NaN |
| select\_multiple inputs | farm\_inputs | 3.3 Which inputs did you use on your maize? Select all that apply. | NaN | yes | NaN | NaN |
| integer | farm\_ext | 3.4 In the past 30 days, how many times did you speak with an extension agent? | NaN | yes | NaN | NaN |
| select\_one yesno21 | farm\_soil | 3.5 Did you receive advice on soil health? | NaN | yes | NaN | NaN |
| select\_one yesno | farm\_radio | 3.6 Does the household own a radio? | NaN | yes | NaN | NaN |
| end group | farm | NaN | NaN | NaN | NaN | NaN |
| begin group | food | Food security | NaN | NaN | NaN | NaN |
| select\_one yesno | food\_worry | 4.1 In the past 30 days, did you worry that food would run out? | NaN | yes | NaN | NaN |
| integer | food\_meals | 4.3 How many meals did your household eat yesterday? | NaN | yes | NaN | NaN |
| select\_one yesno | food\_skip | 4.2 In the past 30 days, did you skip a meal because there was not enough food? | NaN | yes | NaN | NaN |
| end group | food | NaN | NaN | NaN | NaN | NaN |
| begin group | tech | Technology | NaN | NaN | NaN | NaN |
| select\_one yesno | tech\_phone | 5.1 Do you own a mobile phone? | NaN | yes | NaN | NaN |
| select\_one yesno | tech\_ai | 5.4 Have you used an AI assistant to get farming advice? | NaN | yes | NaN | NaN |
| select\_one freq | tech\_freq | 5.3 How often do you use it? | NaN | yes | ${tech\_ai}=1 | NaN |
| select\_one sat | tech\_sat | 5.4 How satisfied were you with the advice you received? | NaN | yes | ${tech\_ai}=1 | NaN |
| end group | tech | NaN | NaN | NaN | NaN | NaN |

## choices
| list\_name | name | label::English |
| --- | --- | --- |
| yesno | 1 | Yes |
| yesno | 0 | No |
| yesno21 | 1 | Yes |
| yesno21 | 0 | No |
| sex | 1 | Male |
| sex | 2 | Female |
| edu | 1 | NaN |
| edu | 2 | Primary |
| edu | 3 | Secondary |
| edu | 4 | Tertiary |
| inputs | 1 | Improved seed |
| inputs | 2 | Fertilizer |
| inputs | 3 | Pesticide |
| inputs | 4 | Irrigation |
| freq | 1 | Daily |
| freq | 2 | Weekly |
| freq | 3 | Monthly |
| freq | 4 | Rarely |
| sat | 1 | Very dissatisfied |
| sat | 2 | Dissatisfied |
| sat | 3 | Neutral |
| sat | 4 | Satisfied |
| sat | 5 | Very satisfied |

## settings
| form\_title | form\_id | version |
| --- | --- | --- |
| Test form | test\_form | 2611010000 |