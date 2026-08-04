# OilPulse — Five-Page Python Analytics App

OilPulse is a professional student portfolio project for analysing synthetic global oil operations data from 2015–2026.

## Five pages

1. Home — headline, project benefits and navigation
2. Analytics — filters, KPIs and five operational charts
3. Data Explorer — record table and filtered CSV download
4. About Project — student purpose, learning outcomes and technologies
5. Contact & Social — LinkedIn, GitHub, Instagram, Facebook and X/Twitter links

The opening screen contains customer registration, login and forgotten-password reset. Passwords are stored as salted PBKDF2 hashes in a local SQLite database.

## Run on Windows

Extract the ZIP and open the inner `OilPulse_Python_App` folder in Visual Studio Code. Run these commands separately:

```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501 and keep the terminal open while using the app.

## Important

All oil figures are synthetic practice data. They are not official statistics or financial advice. Do not upload `customers.db` because it can contain personal registration details.

## Customer accounts

The app now opens on a customer access page. A customer can register using a
full name, home address, date of birth, recovery email, username and password, then log in to
view the dashboard and log off from the sidebar. If a password is forgotten,
the customer can verify their registered username, recovery email and date of birth,
then securely choose a new password.

Account data is stored locally in `customers.db`, which the app creates on its
first run. Passwords are protected with a salted PBKDF2 hash and are never
stored as readable text. Do not upload `customers.db` to GitHub or share it.

An interactive, professional Streamlit portfolio project that analyses a realistic synthetic monthly dataset for 15 major oil-producing countries from 2015 to 2026.

## Features

- Customer registration with full name, address, date of birth and recovery email
- Secure username and password login, plus sidebar logoff
- Forgot-password reset using the registered username, recovery email and date of birth
- Account settings for existing customers to add or change a recovery email
- Cleaner interface with Streamlit's technical three-dot menu hidden
- Responsive dark-blue OilPulse interface
- Left-side filters for all years from 2015–2026, six regions and 15 countries
- KPI cards for production, sales, revenue, profit and margin
- Monthly production and revenue trends
- Top-producer comparison
- Revenue, profit and downtime analysis
- Filtered data table and CSV download

The dataset contains 2,160 monthly practice records: 12 years × 12 months × 15 countries.

> The dataset is synthetic practice data and must not be presented as official statistics.

## Run the app

1. Open a terminal in this folder.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Start Streamlit:

   ```bash
   python -m streamlit run app.py
   ```

4. Open the local address shown in the terminal, normally `http://localhost:8501`.

## Project structure

```text
OilPulse_Python_App/
├── app.py
├── auth.py
├── requirements.txt
├── README.md
├── .gitignore
├── tests/
│   └── test_auth.py
└── data/
    └── World_Oil_Operations_Practice_Dataset.xlsx
```
