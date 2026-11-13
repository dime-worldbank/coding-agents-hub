# Describing the questions

The wiki says the manual should explain the questions and give common rules for asking them. Build this section from the form, not from memory.

## Read the form as Markdown, in pieces

No custom Python reads the form. Convert it to Markdown, cut it down to the columns that matter, and read it in chunks.

1. Convert: `markitdown form.xlsx -o form.md` (the Markdown Converter skill uses `uvx markitdown`). If that fails, use `extract-text form.xlsx`. Say which converter you used.
2. Find the languages: `grep -m1 '^| type' form.md | tr '|' '\n' | grep -i label`. Ask the team which language the manual uses.
3. Reduce:
   ```
   scripts/pick_columns.sh form.md "type,name,label::<language>,relevant,constraint,required" survey > survey.md
   scripts/pick_columns.sh form.md "list_name,value,label::<language>" choices > choices.md
   ```
   Read the helper's messages. "No column ..." means that detail is not available. The choices sheet may call its value column `name` or `value`: the helper accepts either. Locate a question by its `name`, not its `#`.
4. Read at most about 150 rows at a time: `sed -n '1,150p' survey.md`. For a large form, write one module of the manual before reading the next. Never paste the reduced form into chat.

## For each module write

1. **Purpose:** what the module collects and why, in one or two sentences. Ask the team if it is not obvious from the labels.
2. **Who is asked:** from the module's group condition, in plain words ("Ask only if the respondent agreed to take part"). A group's condition applies to every question inside it.
3. **Question by question** (a table is fine): number, name, what it asks, how to ask it, answer rules.
   - **Skip rules** in plain words from the `relevant` column ("Ask only if Q B3 is Yes").
   - **Valid answers** from the `constraint` column ("Enter a number from 0 to 7").
   - **Required** if the form will not let the enumerator skip it.
   - **Choices:** list codes and labels when the enumerator must pick one, from the choices sheet rows for the list named in `type`. Say whether more than one answer is allowed. If the list loads from a file, say so and ask the team how enumerators should use it.
   - **Definitions and probes:** from the team. Mark `[TO CONFIRM: definition of ...]` where a term needs one. Do not invent a definition.
   - **Common errors:** from the pilot or the team.
4. **Special answers:** what to do for Don't know, Refused, and Other, if the form has them. Ask the team for the rule.

## Rules

- Do not change a question's wording in the manual. Quote it as in the form, in the chosen language.
- Do not describe what the form does not do. If a skip rule is too complex to put in words, give the expression and mark it `[TO CONFIRM]`.
- When the label and the constraint disagree (for example "30 days" and a limit of 7), do not choose. Mark it `[TO CONFIRM]` and tell the team.
- Group very similar questions (for example a repeated roster item) to keep the manual short, and say they are grouped.
- Keep question names in the text so coverage can be checked.
