#!/usr/bin/env python3
"""Build an invented specification-style paper (Word) and its programmed form, with planted differences.
Run from this folder: python build_spec_test.py. Outputs spec-form.xlsx and spec-paper.docx."""
import docx
from openpyxl import Workbook

Y = [("1", "Yes"), ("0", "No")]
# (num, name, type, list, label, required, relevance, constraint, cmsg)
FORM = {
 "Module A Introduction": ("mod_a_intro", "", [
   ("A1", "enumerator_id", "select_one", "enumerator", "Enumerator: What is your name?", True, "", "", "", "search('enumerator_list')"),
   ("A2", "consent", "select_one", "yesno", "Do you agree to take part in this survey?", True, "", "", "", "")]),
 "Module B Household": ("mod_b_hh", "${consent}=1", [
   ("B1", "hh_age", "integer", "", "How old is the child in completed years?", True, "", ".>=0 and .<=17", "Age must be between 0 and 17.", ""),
   ("B2", "hh_sex", "select_one", "sex", "What is the child's sex?", False, "", "", "", ""),
   ("B3", "hh_school", "select_one", "yesno", "Is the child enrolled in school?", True, "${hh_age}>=6", "", "", ""),
   ("B4", "hh_grade", "integer", "", "Which grade is the child in?", True, "${hh_school}=1", ".>=1 and .<=8", "Grade must be 1 to 8.", ""),
   ("B5", "hh_meals", "integer", "", "In the past 30 days, how many days did the child eat a school meal?", True, "", ".>=0 and .<=7", "Enter 0 to 7.", "")]),
 "Module C Health": ("mod_c_health", "${consent}=1", [
   ("C1", "hl_ill", "select_one", "yesno", "Was the child ill in the last 2 weeks?", True, "", "", "", ""),
   ("C2", "hl_clinic", "select_one", "yesno", "Did the child visit a clinic?", True, "${hl_ill}=1", "", "", ""),
   ("C3", "hl_cost", "integer", "", "How much did the visit cost in total?", True, "${hl_clinic}=1", ".>=0", "Enter a positive amount.", ""),
   ("C4", "hl_vaccine", "select_one", "yesno", "Has the child been vaccinated?", True, "", "", "", "")]),
}
LISTS = {"yesno": Y, "sex": [("1", "Boy"), ("2", "Girl")]}


def build_form(path):
    wb = Workbook(); ws = wb.active; ws.title = "survey"
    ws.append(["type", "name", "label::English", "label::French", "relevant", "constraint", "constraint message::English", "required", "appearance", "question_number"])
    ws.append(["calculate", "age_group", "", "", "", "", "", "", "", ""])
    ws.append(["start", "start", "", "", "", "", "", "", "", ""])
    for mod, (gname, grel, items) in FORM.items():
        ws.append(["begin group", gname, mod, mod + " (fr)", grel, "", "", "", "", ""])
        for num, name, typ, lst, label, req, rel, con, msg, app in items:
            t = f"{typ} {lst}" if lst else typ
            if name == "enumerator_id":
                t = "select_one_from_file enumerator_list.csv"
            ws.append([t, name, f"{num} {label}", f"{num} [fr] {label}", rel, con, msg, "yes" if req else "", app, num])
        ws.append(["end group", gname, "", "", "", "", "", "", "", ""])
    ch = wb.create_sheet("choices"); ch.append(["list_name", "value", "label::English", "label::French"])
    for ln, opts in LISTS.items():
        for v, l in opts:
            ch.append([ln, v, l, l + " (fr)"])
    cl = wb["survey"]; cl["D2"] = ""  # calc label
    wb["survey"]["A2"] = "calculate"; wb["survey"]["I2"] = ""
    wb["survey"].cell(row=2, column=11, value="if(${hh_age}<6,1,2)")
    wb["survey"].cell(row=1, column=11, value="calculation")
    wb.create_sheet("settings").append(["form_title", "form_id", "version"])
    wb.save(path)


def para(d, text):
    d.add_paragraph(text)


def build_paper(path):
    d = docx.Document()
    d.add_heading("Spec test survey", 0)
    para(d, "Paper version for test workflows, English labels")
    for mod, (gname, grel, items) in FORM.items():
        d.add_heading(f"{mod}   [{gname}]", 1)
        if grel:
            para(d, f"Ask whole group if:  {grel}")
        items = list(items)
        if gname == "mod_b_hh":                      # plant: B4 and B5 swapped, B6 on paper only
            items[3], items[4] = items[4], items[3]
            items.append(("B6", "hh_siblings", "integer", "", "How many siblings does the child have?", True, "", "", "", ""))
        if gname == "mod_c_health":                  # plant: vaccine question dropped from paper
            items = [i for i in items if i[1] != "hl_vaccine"]
        for num, name, typ, lst, label, req, rel, con, msg, app in items:
            lab, typ2, req2, rel2, con2 = label, typ, req, rel, con
            if name == "hh_meals": lab = "In the past 7 days, how many days did the child eat a school meal?"
            if name == "hh_school": rel2 = "${hh_age}>=5"
            if name == "hh_age": con2 = ".>=0 and .<=18"
            if name == "hh_sex": req2 = True
            if name == "hl_cost": typ2 = "text"
            if name == "hl_ill": name = "hl_illness"
            t = f"{typ2} {lst}" if lst else typ2
            para(d, f"{num}   {name}   {t}" + ("   Required" if req2 else ""))
            para(d, f"{num}: {lab}")
            if lst == "enumerator":
                para(d, "\u25cb  id  \tname")
                para(d, "Choices are loaded at run time from enumerators.csv (search appearance); the list above is only the structure.")
            elif lst:
                opts = list(LISTS[lst])
                if name == "hh_sex": opts = opts + [("3", "Other")]
                if name == "hl_illness": opts = [("1", "Yes"), ("2", "No")]
                for v, l in opts:
                    para(d, f"\u25cb  {v}   \t{l}")
            if app: para(d, f"Appearance:  {app}")
            if rel2: para(d, f"Ask if:  {rel2}")
            if con2:
                para(d, f"Constraint:  {con2}")
                para(d, f"Constraint message:  {msg}")
    d.add_heading("Calculate fields", 1)
    t = d.add_table(rows=2, cols=5)
    for i, h in enumerate(["#", "Name", "Calculation", "Relevance", "Section"]): t.rows[0].cells[i].text = h
    for i, v in enumerate(["1", "age_group (here)", "if(${hh_age}<5,1,2)", "", ""]): t.rows[1].cells[i].text = v
    d.save(path)


if __name__ == "__main__":
    build_form("spec-form.xlsx"); build_paper("spec-paper.docx"); print("built")
