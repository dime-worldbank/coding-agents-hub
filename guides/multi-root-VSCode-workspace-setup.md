# Set Up a Multi-Root VS Code Workspace

This example uses a project called **`water-security`**.

- Code is stored in GitHub: `water-security`
- Data is stored in OneDrive: `OneDrive\water-security`

## 1. Open both folders in VS Code

Open the GitHub repository`watrer-security` in VS Code.

Then select:

**File → Add Folder to Workspace**

Add the OneDrive data folder.

Your workspace should look approximately like this:

```text
WATER-SECURITY
├── water-security-code
│   ├── AGENTS.md.     <- Memory file
│   ├── skills/        <- Folder with all the skills
│   └── code/
│
└── water-security-data
    ├── raw/
    ├── processed/
    └── outputs/
```

The actual folders can both still be named `water-security`.

For example:

```text
C:\Users\<username>\GitHub\water-security
C:\Users\<username>\OneDrive\water-security
```

Inside VS Code, you can give them clearer workspace names such as:

- `water-security-code`
- `water-security-data`

## 2. Save the workspace

Select:

**File → Save Workspace As...**

Save the workspace locally, for example:

```text
C:\Users\<username>\Workspaces\water-security\water-security.code-workspace
```

The `.code-workspace` file is a local file that connects the different project folders on your computer.

Each collaborator can create their own workspace file using the locations of the GitHub and OneDrive folders on their machine.

The workspace file does not need to be committed to GitHub.

## 3. Keep shared agent files in GitHub

Files that should be shared across collaborators should live in the GitHub repository.

For example:

```text
water-security/
├── AGENTS.md
├── skills/
└── code/
```

Use:

- `AGENTS.md` for project-level instructions and rules for the coding agent.

- `skills/` for reusable procedures or workflows.

These files can still apply to both the code and data folders even though they are stored in the GitHub repository.

## 4. Describe the data location in `AGENTS.md`

If a skill needs files from the OneDrive data folder, document the workspace structure and relevant data locations in `AGENTS.md`.

For example:

```md
## Workspace structure

This project uses a multi-root VS Code workspace.

- `water-security-code` contains the GitHub repository, project code, agent instructions, memory, and skills.
- `water-security-data` contains project data stored in OneDrive.

## Data used by skills

Skills may use files from `water-security-data` when required.

Relevant locations:

- Raw data: `water-security-data/raw/`
- Processed data: `water-security-data/processed/`
- Outputs: `water-security-data/outputs/`

Do not copy project data into the GitHub repository.

Do not modify files in `raw/` unless explicitly instructed.
```

## Final setup

The overall setup is:

```text
GitHub
└── water-security
    ├── AGENTS.md
    ├── skills/
    └── code/

OneDrive
└── water-security
    ├── raw/
    ├── processed/
    └── outputs/

Local computer
└── Workspaces
    └── water-security
        └── water-security.code-workspace
```

The GitHub repository contains the shared project instructions and skills, OneDrive contains the data, and the local VS Code workspace connects the two.