# 🏦 Credit Risk Dashboard — Flask + MySQL

A live web dashboard that connects to your MySQL `banking` database
and renders all charts in real time in your browser.

---

## 📁 Project Structure

```
credit_dashboard/
├── app.py              ← Flask backend (edit your MySQL password here)
├── requirements.txt    ← Python dependencies
├── templates/
│   └── index.html      ← Frontend dashboard (auto-served by Flask)
└── README.md
```

---

## 🚀 Setup & Run (Step by Step)

### Step 1 — Open the folder in DataSpell terminal

```bash
cd credit_dashboard
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Edit your MySQL password in app.py

Open `app.py` and find this section near the top:

```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "YOUR_PASSWORD_HERE",   # <-- change this
    "database": "banking"
}
```

Replace `YOUR_PASSWORD_HERE` with your actual MySQL password.

### Step 4 — Run the app

```bash
python app.py
```

You should see:
```
🏦 Credit Risk Dashboard running at http://localhost:5000
```

### Step 5 — Open in browser

Go to: **http://localhost:5000**

---

## 📊 Dashboard Pages

| Page | Content |
|------|---------|
| Home | KPI cards, Nationality, Gender, Loyalty, Risk, Income Band |
| Loan & Deposit | Loans by Income/Nationality/Occupation, Fee Structure |
| Deposit Analysis | Deposits by Income/Nationality, Properties, Savings split |
| Summary | Full portfolio overview, grouped charts, radar chart |

---

## ✅ All data is fetched LIVE from your MySQL database on every page load.
