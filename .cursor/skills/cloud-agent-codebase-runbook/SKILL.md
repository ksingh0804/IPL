---
name: cloud-agent-codebase-runbook
description: Practical setup, execution, and testing runbook for Cloud agents working on this IPL analysis repository.
---

# Cloud Agent Codebase Runbook

Use this skill when you need to run, test, or update the IPL analysis project in Cursor Cloud.

## Repository map

- `IPL.ipynb`: Main Jupyter notebook for IPL 2008-2017 data exploration and visualization.
- `Match.csv`: Checked-in match-level dataset used by the notebook.
- `Presentation.pdf`: Project write-up/output reference.
- `README.md`: Short project summary.

There is no web app, backend service, auth flow, or feature-flag system in this repository today. Do not spend time looking for logins, `.env` files, or flag toggles unless new application code is added.

## Notebook workflow

1. Work from the repository root: `cd /workspace`.
2. Create a local environment if one is not already active:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `python3 -m pip install --upgrade pip`
3. Install the notebook dependencies:
   - `python3 -m pip install pandas numpy matplotlib seaborn scipy jupyter nbconvert`
   - The notebook imports `thinkstats2` and `thinkplot`; install them if available in the environment, or mock/remove only the cells that need them for the specific task.
4. Start the notebook UI when manual inspection is needed:
   - `jupyter notebook --ip 0.0.0.0 --no-browser`
5. Open `IPL.ipynb` from the Jupyter URL shown in the terminal.

### Notebook testing

- Fast import check:
  - `python3 - <<'PY'\nimport pandas, numpy, matplotlib, seaborn, scipy\nprint('core imports ok')\nPY`
- Dataset smoke test:
  - `python3 - <<'PY'\nimport pandas as pd\nmatch = pd.read_csv('Match.csv')\nprint(match.shape)\nprint(match[['Season_Year', 'match_winner']].head())\nPY`
- Notebook execution check:
  - `jupyter nbconvert --to notebook --execute IPL.ipynb --output /tmp/IPL.executed.ipynb`
  - Expect this to fail until `Deliveries.csv`, `thinkstats2`, and `thinkplot` are supplied or the dependent cells are intentionally skipped for the task.

## Data workflow

1. Treat checked-in CSV files as source data. Do not rewrite them unless the task explicitly asks for data corrections.
2. Validate schemas before changing analysis code:
   - `python3 - <<'PY'\nimport pandas as pd\nprint(pd.read_csv('Match.csv').columns.tolist())\nPY`
3. If a task depends on delivery-level analysis, confirm whether `Deliveries.csv` is present. The notebook references it, but it is not checked in at the time this skill was created.

### Data testing

- Row and column count check:
  - `python3 - <<'PY'\nimport pandas as pd\nmatch = pd.read_csv('Match.csv')\nassert not match.empty\nassert {'Team1', 'Team2', 'Season_Year', 'match_winner'} <= set(match.columns)\nprint(match.shape)\nPY`
- Basic analysis sanity check:
  - `python3 - <<'PY'\nimport pandas as pd\nmatch = pd.read_csv('Match.csv')\nprint(match.groupby('Season_Year')['match_id'].count())\nPY`

## Presentation and docs workflow

- Use `Presentation.pdf` as a reference for expected questions, variables, and conclusions.
- For README or runbook changes, verify the referenced files and commands still match the repository.
- If editing notebooks, prefer preserving outputs only when they are useful for review; otherwise clear or regenerate outputs consistently.

### Docs testing

- Confirm referenced files exist:
  - `python3 - <<'PY'\nfrom pathlib import Path\nfor path in ['README.md', 'IPL.ipynb', 'Match.csv', 'Presentation.pdf']:\n    print(path, Path(path).exists())\nPY`
- If commands are documented in this skill, run the smallest relevant command and record whether missing dependencies or missing data are expected.

## Updating this skill

When you discover new runbook knowledge, update this file in the same PR as the related code or test change.

- Add commands that actually worked in Cursor Cloud.
- Note environment blockers exactly, including missing files, missing packages, or services that are not part of this repo.
- Keep each workflow short and task-oriented.
- Remove stale steps as soon as the repository gains first-class setup files such as `requirements.txt`, `environment.yml`, or project-specific test scripts.
