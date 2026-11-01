# OilPulse — Python Analytics Portfolio

An educational Streamlit application for exploring synthetic oil operations data covering 2015–2026.

**Tools:** Python · Streamlit · pandas · Plotly · SQLite · Excel/CSV

## Application pages

| Page | Current implementation |
| --- | --- |
| Home | Project introduction and navigation guidance. |
| Analytics | Year, region and country filters; production, sales, revenue, profit and downtime KPIs; five monthly trend charts. |
| Data Explorer | Record table, year/region/country filters and CSV download. |
| About Project | Educational purpose, technologies and data limitations. |
| Contact & Social | LinkedIn and GitHub links; generic Instagram, Facebook and X links awaiting personal profile addresses. |

The current interface places filters above the charts and a **Log off** button in the top bar. It does not expose an account-settings page, margin KPI or top-producer comparison chart.

## Run locally

Download or clone this repository and open the folder containing `app.py` and `requirements.txt`. Run these commands separately:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address printed by Streamlit, normally http://localhost:8501, and keep the terminal running.

## Account demonstration

The opening screen offers registration, login and password reset. Registration collects a name, address, date of birth, recovery email, username and password. Use fictional details for demonstrations.

- Account data is stored locally in `customers.db`.
- Passwords use salted PBKDF2-HMAC-SHA256 hashes.
- Password reset matches the entered username, email address and date of birth against stored details.
- No recovery email or time-limited reset token is sent. Matching an email address does not verify ownership of that mailbox.
- An authenticated user can log off using the top-bar button.

These are educational account workflows, not a production-ready authentication service. Do not publish `customers.db` or use the demonstration to collect real customer information.

## Data and analysis

The workbook is [World_Oil_Operations_Practice_Dataset.xlsx](data/World_Oil_Operations_Practice_Dataset.xlsx), read from its **Oil Data** sheet.

All figures are synthetic practice data, not official oil statistics, live market information or financial advice. Production, sales, revenue and profit are summed for the selected records; downtime is displayed as an arithmetic mean. Filter choices are drawn from the workbook.

## Repository contents

- [app.py](app.py): Streamlit pages, filters, charts and CSV export.
- [auth.py](auth.py): SQLite account functions and password hashing.
- [requirements.txt](requirements.txt): application dependencies.
- [run_app.bat](run_app.bat): Windows launch helper.
- [tests/test_auth.py](tests/test_auth.py): existing authentication test source.
- [data/World_Oil_Operations_Practice_Dataset.xlsx](data/World_Oil_Operations_Practice_Dataset.xlsx): practice workbook.

## Verification status

This README was aligned with the current source files. Application execution, browser behaviour and authentication tests were not rerun during the documentation update. The presence of a test file does not establish that tests pass.
