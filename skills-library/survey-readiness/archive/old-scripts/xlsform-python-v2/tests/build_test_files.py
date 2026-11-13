#!/usr/bin/env python3
"""Build invented test files for xlsform-paper-sync (no real data).

Creates in this folder: paper-questionnaire.docx / .xlsx / .pdf and programmed-form.xlsx.
The paper and programmed versions differ on purpose; see expected-discrepancies.md.
Run: python build_test_files.py
"""
import subprocess
from pathlib import Path
import docx
from docx.shared import Pt
from openpyxl import Workbook

HERE = Path(__file__).parent
YN = ["1 = Yes", "0 = No"]

CONSENT = ("Hello, my name is [name]. I work for the Zandia Farm Advisory Study. We are asking farmers about their "
           "farming and food. The interview takes about 30 minutes. Taking part is voluntary and you can stop at any "
           "time. Your answers will be kept confidential and used only for research.")

PAPER = {
 "Module 1: Consent": [
  ("1.1", "Do you agree to take part in this survey?", YN, "If No, end the interview"),
 ],
 "Module 2: Household": [
  ("2.1", "What is your age in completed years?", ["Numeric"], ""),
  ("2.2", "What is your sex?", ["1 = Male", "2 = Female", "3 = Other"], ""),
  ("2.3", "What is the highest level of education you have completed?", ["1 = None", "2 = Primary", "3 = Secondary", "4 = Tertiary"], ""),
  ("2.4", "How many people usually live in this household?", ["Numeric"], ""),
 ],
 "Module 3: Farm practices": [
  ("3.1", "Did you grow maize in the last 12 months?", YN, "If No, go to 3.4"),
  ("3.2", "How many hectares of maize did you plant?", ["Numeric"], "Ask if 3.1 = Yes"),
  ("3.3", "Which inputs did you use on your maize? Select all that apply.", ["1 = Improved seed", "2 = Fertilizer", "3 = Pesticide", "4 = Irrigation", "5 = Other"], ""),
  ("3.4", "In the past 7 days, how many times did you speak with an extension agent?", ["Numeric"], ""),
  ("3.5", "Did you receive advice on soil health?", ["1 = Yes", "2 = No"], ""),
 ],
 "Module 4: Food security": [
  ("4.1", "In the past 30 days, did you worry that food would run out?", YN, ""),
  ("4.2", "In the past 30 days, did you skip a meal because there was not enough food?", YN, ""),
  ("4.3", "How many meals did your household eat yesterday?", ["Numeric"], ""),
 ],
 "Module 5: Technology": [
  ("5.1", "Do you own a mobile phone?", YN, ""),
  ("5.2", "Have you used an AI assistant to get farming advice?", YN, ""),
  ("5.3", "How often do you use it?", ["1 = Daily", "2 = Weekly", "3 = Monthly", "4 = Rarely"], "Ask if 5.2 = Yes"),
  ("5.4", "How satisfied are you with the advice you received?", ["1 = Very dissatisfied", "2 = Dissatisfied", "3 = Neutral", "4 = Satisfied", "5 = Very satisfied"], "Ask if 5.2 = Yes"),
 ],
}


def build_docx():
    d = docx.Document()
    d.add_heading("Zandia Farm Advisory Survey: paper questionnaire (TEST DOCUMENT)", 0)
    for mod, qs in PAPER.items():
        d.add_heading(mod, 1)
        if mod.startswith("Module 1"):
            d.add_paragraph(CONSENT)
        t = d.add_table(rows=1, cols=4)
        t.style = "Table Grid"
        for c, h in zip(t.rows[0].cells, ["No.", "Question", "Response options", "Skip / notes"]):
            c.text = h
        for n, q, ch, note in qs:
            r = t.add_row().cells
            r[0].text, r[1].text, r[2].text, r[3].text = n, q, "\n".join(ch), note
    d.save(HERE / "paper-questionnaire.docx")


def build_xlsx_paper():
    wb = Workbook()
    wb.remove(wb.active)
    for mod, qs in PAPER.items():
        ws = wb.create_sheet(mod.split(":")[0].replace("Module ", "M"))
        ws.append(["No.", "Question", "Response options", "Skip / notes"])
        for n, q, ch, note in qs:
            ws.append([n, q, "\n".join(ch), note])
    wb.save(HERE / "paper-questionnaire.xlsx")


def build_form():
    wb = Workbook()
    s = wb.active; s.title = "survey"
    s.append(["type", "name", "label::English", "hint", "required", "relevant", "constraint"])
    S = []
    def grp(name, label): S.append(["begin group", name, label, "", "", "", ""])
    def end(name): S.append(["end group", name, "", "", "", "", ""])
    def q(t, n, l, rel="", hint="", con=""): S.append([t, n, l, hint, "yes", rel, con])
    S.append(["start", "start", "", "", "", "", ""]); S.append(["end", "end", "", "", "", "", ""])
    S.append(["deviceid", "deviceid", "", "", "", "", ""])
    grp("consent", "Consent")
    # consent note differs in wording from the paper script
    S.append(["note", "consent_note", "Hello, my name is [name]. I work for the Zandia Farm Advisory Study. We are asking farmers about their farming. The interview takes about 45 minutes and your answers are confidential.", "", "", "", ""])
    q("select_one yesno", "consent", "1.1 Do you agree to take part in this survey?")
    end("consent")
    grp("hh", "Household")
    q("text", "hh_age", "2.1 What is your age in completed years?")  # planted: type differs (text, paper numeric)
    q("select_one sex", "hh_sex", "2.2 What is your sex?")           # planted: 'Other' missing
    q("select_one edu", "hh_edu", "2.3 What is the highest level of education you have completed?")
    # planted: 2.4 household size missing from the form
    end("hh")
    grp("farm", "Farm practices")
    q("select_one yesno", "farm_maize", "3.1 Did you grow maize in the last 12 months?")
    q("decimal", "farm_ha", "3.2 How many hectares of maize did you plant?", rel="${farm_maize}=1")
    q("select_multiple inputs", "farm_inputs", "3.3 Which inputs did you use on your maize? Select all that apply.")  # planted: 'Other' missing
    q("integer", "farm_ext", "3.4 In the past 30 days, how many times did you speak with an extension agent?")  # planted: 7 -> 30 days
    q("select_one yesno21", "farm_soil", "3.5 Did you receive advice on soil health?")  # planted: codes 1/0 vs 1/2
    q("select_one yesno", "farm_radio", "3.6 Does the household own a radio?")  # planted: form only
    end("farm")
    grp("food", "Food security")
    q("select_one yesno", "food_worry", "4.1 In the past 30 days, did you worry that food would run out?")
    q("integer", "food_meals", "4.3 How many meals did your household eat yesterday?")  # planted: order swapped
    q("select_one yesno", "food_skip", "4.2 In the past 30 days, did you skip a meal because there was not enough food?")
    end("food")
    grp("tech", "Technology")
    q("select_one yesno", "tech_phone", "5.1 Do you own a mobile phone?")
    q("select_one yesno", "tech_ai", "5.4 Have you used an AI assistant to get farming advice?")  # planted: number 5.4 vs paper 5.2
    q("select_one freq", "tech_freq", "5.3 How often do you use it?", rel="${tech_ai}=1")
    q("select_one sat", "tech_sat", "5.4 How satisfied were you with the advice you received?", rel="${tech_ai}=1")  # planted: small wording change
    end("tech")
    for r in S: s.append(r)
    c = wb.create_sheet("choices")
    c.append(["list_name", "name", "label::English"])
    lists = {
     "yesno": [("1", "Yes"), ("0", "No")], "yesno21": [("1", "Yes"), ("0", "No")],
     "sex": [("1", "Male"), ("2", "Female")],
     "edu": [("1", "None"), ("2", "Primary"), ("3", "Secondary"), ("4", "Tertiary")],
     "inputs": [("1", "Improved seed"), ("2", "Fertilizer"), ("3", "Pesticide"), ("4", "Irrigation")],
     "freq": [("1", "Daily"), ("2", "Weekly"), ("3", "Monthly"), ("4", "Rarely")],
     "sat": [("1", "Very dissatisfied"), ("2", "Dissatisfied"), ("3", "Neutral"), ("4", "Satisfied"), ("5", "Very satisfied")],
    }
    for k, v in lists.items():
        for n, l in v: c.append([k, n, l])
    st = wb.create_sheet("settings")
    st.append(["form_title", "form_id", "version"]); st.append(["Test form", "test_form", "2611010000"])
    wb.save(HERE / "programmed-form.xlsx")


if __name__ == "__main__":
    build_docx(); build_xlsx_paper(); build_form()
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(HERE), str(HERE / "paper-questionnaire.docx")],
                   check=False, capture_output=True)
    print("built:", sorted(p.name for p in HERE.glob("*") if p.suffix in (".docx", ".xlsx", ".pdf")))
