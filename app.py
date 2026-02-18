from flask import Flask, render_template, jsonify
import mysql.connector
from decimal import Decimal

app = Flask(__name__)

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "3008",
    "database": "banking"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def to_float(val):
    """Convert Decimal/None to float safely."""
    if val is None:
        return 0.0
    return float(val)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    db = get_db()
    cur = db.cursor()

    # ── KPIs ──
    cur.execute("SELECT COUNT(*) FROM banking")
    total_clients = cur.fetchone()[0]

    cur.execute("SELECT SUM(`Bank Loans`), AVG(`Bank Loans`) FROM banking")
    r = cur.fetchone()
    total_loans, avg_loans = to_float(r[0]), to_float(r[1])

    cur.execute("SELECT SUM(`Bank Deposits`), AVG(`Bank Deposits`) FROM banking")
    r = cur.fetchone()
    total_deposits, avg_deposits = to_float(r[0]), to_float(r[1])

    cur.execute("SELECT SUM(`Checking Accounts`) FROM banking")
    total_checking = to_float(cur.fetchone()[0])

    cur.execute("SELECT SUM(`Saving Accounts`) FROM banking")
    total_saving = to_float(cur.fetchone()[0])

    cur.execute("SELECT SUM(`Business Lending`) FROM banking")
    total_biz = to_float(cur.fetchone()[0])

    cur.execute("SELECT AVG(`Estimated Income`) FROM banking")
    avg_income = to_float(cur.fetchone()[0])

    cur.execute("SELECT AVG(`Risk Weighting`) FROM banking")
    avg_risk = to_float(cur.fetchone()[0])

    # ── Nationality ──
    cur.execute("SELECT Nationality, COUNT(*) as cnt FROM banking GROUP BY Nationality ORDER BY cnt DESC")
    nat_rows = cur.fetchall()
    nat_labels = [r[0] for r in nat_rows]
    nat_values = [r[1] for r in nat_rows]

    # ── Gender ──
    cur.execute("SELECT GenderId, COUNT(*) FROM banking GROUP BY GenderId ORDER BY GenderId")
    gen_rows = cur.fetchall()
    gender_labels = ["Male" if r[0] == 1 else "Female" for r in gen_rows]
    gender_values = [r[1] for r in gen_rows]

    # ── Loyalty ──
    cur.execute("SELECT `Loyalty Classification`, COUNT(*) FROM banking GROUP BY `Loyalty Classification` ORDER BY COUNT(*) DESC")
    loy_rows = cur.fetchall()
    loyalty_labels = [r[0] for r in loy_rows]
    loyalty_values = [r[1] for r in loy_rows]

    # ── Risk Weighting ──
    cur.execute("SELECT `Risk Weighting`, COUNT(*) FROM banking GROUP BY `Risk Weighting` ORDER BY `Risk Weighting`")
    risk_rows = cur.fetchall()
    risk_labels = [f"Risk {r[0]}" for r in risk_rows]
    risk_values = [r[1] for r in risk_rows]

    # ── Income Band ──
    cur.execute("""
        SELECT
            CASE
                WHEN `Estimated Income` < 100000  THEN 'Low (<100K)'
                WHEN `Estimated Income` < 300000  THEN 'Mid (100K-300K)'
                ELSE 'High (>300K)'
            END AS band,
            COUNT(*) as cnt
        FROM banking
        GROUP BY band
        ORDER BY MIN(`Estimated Income`)
    """)
    ib_rows = cur.fetchall()
    income_band_labels = [r[0] for r in ib_rows]
    income_band_values = [r[1] for r in ib_rows]

    # ── Fee Structure ──
    cur.execute("SELECT `Fee Structure`, COUNT(*) FROM banking GROUP BY `Fee Structure` ORDER BY COUNT(*) DESC")
    fee_rows = cur.fetchall()
    fee_labels = [r[0] for r in fee_rows]
    fee_values = [r[1] for r in fee_rows]

    # ── Loans by Nationality ──
    cur.execute("SELECT Nationality, ROUND(SUM(`Bank Loans`)/1000000,1) FROM banking GROUP BY Nationality ORDER BY SUM(`Bank Loans`) DESC")
    ln_rows = cur.fetchall()
    loan_nat_labels = [r[0] for r in ln_rows]
    loan_nat_values = [to_float(r[1]) for r in ln_rows]

    # ── Deposits by Nationality ──
    cur.execute("SELECT Nationality, ROUND(SUM(`Bank Deposits`)/1000000,1) FROM banking GROUP BY Nationality ORDER BY SUM(`Bank Deposits`) DESC")
    dn_rows = cur.fetchall()
    dep_nat_labels = [r[0] for r in dn_rows]
    dep_nat_values = [to_float(r[1]) for r in dn_rows]

    # ── Loans by Income Band ──
    cur.execute("""
        SELECT
            CASE
                WHEN `Estimated Income` < 100000 THEN 'Low'
                WHEN `Estimated Income` < 300000 THEN 'Mid'
                ELSE 'High'
            END AS band,
            ROUND(SUM(`Bank Loans`)/1000000,1)
        FROM banking GROUP BY band ORDER BY MIN(`Estimated Income`)
    """)
    li_rows = cur.fetchall()
    loan_income_labels = [r[0] for r in li_rows]
    loan_income_values = [to_float(r[1]) for r in li_rows]

    # ── Deposits by Income Band ──
    cur.execute("""
        SELECT
            CASE
                WHEN `Estimated Income` < 100000 THEN 'Low'
                WHEN `Estimated Income` < 300000 THEN 'Mid'
                ELSE 'High'
            END AS band,
            ROUND(SUM(`Bank Deposits`)/1000000,1)
        FROM banking GROUP BY band ORDER BY MIN(`Estimated Income`)
    """)
    di_rows = cur.fetchall()
    dep_income_labels = [r[0] for r in di_rows]
    dep_income_values = [to_float(r[1]) for r in di_rows]

    # ── Top Occupations by Loans ──
    cur.execute("SELECT Occupation, ROUND(SUM(`Bank Loans`)/1000000,1) FROM banking GROUP BY Occupation ORDER BY SUM(`Bank Loans`) DESC LIMIT 6")
    occ_rows = cur.fetchall()
    occ_labels = [r[0] for r in occ_rows]
    occ_values = [to_float(r[1]) for r in occ_rows]

    # ── Properties Owned ──
    cur.execute("SELECT `Properties Owned`, COUNT(*) FROM banking GROUP BY `Properties Owned` ORDER BY `Properties Owned`")
    prop_rows = cur.fetchall()
    prop_labels = [f"{r[0]} Properties" for r in prop_rows]
    prop_values = [r[1] for r in prop_rows]

    # ── Portfolio summary ──
    cur.execute("SELECT ROUND(SUM(`Business Lending`)/1000000,1) FROM banking")
    total_biz_m = to_float(cur.fetchone()[0])

    cur.execute("SELECT ROUND(SUM(`Checking Accounts`)/1000000,1) FROM banking")
    total_check_m = to_float(cur.fetchone()[0])

    cur.execute("SELECT ROUND(SUM(`Saving Accounts`)/1000000,1) FROM banking")
    total_sav_m = to_float(cur.fetchone()[0])

    cur.close()
    db.close()

    return jsonify({
        "kpis": {
            "total_clients":  total_clients,
            "total_loans_b":  round(total_loans / 1e9, 2),
            "total_deposits_b": round(total_deposits / 1e9, 2),
            "total_checking_m": round(total_checking / 1e6, 0),
            "total_saving_m":   round(total_saving / 1e6, 0),
            "total_biz_b":    round(total_biz / 1e9, 2),
            "avg_income_k":   round(avg_income / 1000, 1),
            "avg_risk":       round(avg_risk, 2),
        },
        "nationality":     {"labels": nat_labels,         "values": nat_values},
        "gender":          {"labels": gender_labels,      "values": gender_values},
        "loyalty":         {"labels": loyalty_labels,     "values": loyalty_values},
        "risk":            {"labels": risk_labels,        "values": risk_values},
        "income_band":     {"labels": income_band_labels, "values": income_band_values},
        "fee":             {"labels": fee_labels,         "values": fee_values},
        "loan_nat":        {"labels": loan_nat_labels,    "values": loan_nat_values},
        "dep_nat":         {"labels": dep_nat_labels,     "values": dep_nat_values},
        "loan_income":     {"labels": loan_income_labels, "values": loan_income_values},
        "dep_income":      {"labels": dep_income_labels,  "values": dep_income_values},
        "occupations":     {"labels": occ_labels,         "values": occ_values},
        "properties":      {"labels": prop_labels,        "values": prop_values},
        "portfolio": {
            "labels": ["Bank Loans", "Deposits", "Biz Lending", "Checking", "Savings"],
            "values": [
                round(total_loans/1e6, 1),
                round(total_deposits/1e6, 1),
                total_biz_m,
                total_check_m,
                total_sav_m
            ]
        }
    })


if __name__ == "__main__":
    print("🏦 Credit Risk Dashboard running at http://localhost:5000")
    app.run(debug=True, port=5000)
