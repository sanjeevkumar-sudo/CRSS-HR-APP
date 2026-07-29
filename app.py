# HR Command Center — Setup & Run Guide

A single-file Streamlit app (`app.py`) for automated HR department reporting,
plus an AI-powered natural-language custom report studio (Anthropic Claude API).

## 1. Prerequisites

- Python 3.9+
- An Anthropic API key (only needed for the "AI Natural Language Report Studio"
  tab) — get one at https://console.anthropic.com/

## 2. Setup (Terminal Commands)

```bash
# 1. Create a project folder and move into it
mkdir hr-command-center && cd hr-command-center

# 2. Place app.py and requirements.txt in this folder

# 3. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

## 3. Using the App

1. **Upload data** — In the sidebar, upload the daily HRMS export
   (`.xlsx`, `.xls`, or `.csv`). Snapshot metrics (Total Employees, Active
   Departments, Total Zones) appear automatically.
2. **Tab 1 — Pre-Set Standard Reports** — Choose a Department, Frequency, and
   Report type (Zonal Headcount, Location-wise Distribution, Grade &
   Designation Matrix, or all three). Preview the pivot table and click
   **📥 Download Report as Excel**.
3. **Tab 2 — AI Report Studio** — Paste your Anthropic API key into the
   sidebar once, then describe any custom report in plain English (e.g.
   *"Show me a zonal count of Non-HO staff hired after January 2024"*).
   Claude generates the pandas logic, the app executes it safely on your
   data, and shows a table + auto chart + Excel download.

## 4. Expected Column Names

The app auto-detects common column-name variants (e.g. "Emp Code", "Employee
ID", "ID" all map to the same internal field), so it is tolerant of
inconsistent HRMS exports. For best results, your file should ideally
contain columns resembling:

`Employee ID, Employee Name, Department, Zone, Location, Core/Non-HO Status,
Grade, Designation, Date of Joining`

Any missing columns are handled gracefully — affected reports are skipped
with a clear on-screen warning instead of crashing the app.

## 5. Notes on the AI Studio's Safety Model

- Only the schema (column names, dtypes, sample values) — never full row-level
  data — is sent to Claude as context, alongside your plain-English request.
- Claude returns pandas code only; the app executes it in a restricted
  namespace with dangerous operations (file I/O, OS/network/system access)
  blocked before execution.
- Your Anthropic API key is kept in Streamlit's session memory only and is
  never written to disk.

## 6. Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` inside your activated virtualenv. |
| AI tab says "Please provide your Anthropic API key" | Paste a valid key (starts with `sk-ant-...`) into the sidebar field. |
| A report shows "Missing column" warning | Your uploaded file doesn't contain that field under a recognized name — the app will still render the reports it can build. |
| Excel download fails | Ensure `openpyxl` and `xlsxwriter` installed correctly (`pip install openpyxl xlsxwriter`). |