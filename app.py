from typing import Any

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)
DB_NAME = "expenses.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    expenses: list[Any] = conn.execute("SELECT * FROM expenses ORDER BY created_at DESC").fetchall()
    total = conn.execute("SELECT SUM(amount) as total FROM expenses").fetchone()['total'] or 0.0
    conn.close()
    conn = get_db_connection()
    total_spent = conn.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total FROM expenses
    """).fetchone()["total"]
    this_month = datetime.now().strftime("%Y-%m")
    monthly_total = conn.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (this_month,)).fetchone()["total"]
    category_rows = conn.execute("""
        SELECT category, COALESCE(SUM(amount), 0) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    category_summary = {row["category"]: row["total"] for row in category_rows}
    return render_template(
        "index.html",
        expenses=expenses,
        total_spent=round(total_spent, 2),
        monthly_total=round(monthly_total, 2),
        category_summary=category_summary
    )
@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount", "").strip()
    category = request.form.get("category", "").strip()
    expense_date = request.form.get("expense_date", "").strip()
    if not title or not amount or not category or not expense_date:
        return redirect(url_for("index"))
    try:
        amount = float(amount)
        if amount <= 0:
            return redirect(url_for("index"))
    except ValueError:
        return redirect(url_for("index"))
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO expenses (title, amount, category, expense_date, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        amount,
        category,
        expense_date,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
if __name__ == "__main__":
    init_db()
    app.run(debug=True)