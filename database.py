"""database.py - all SQLite operations for the Expense Tracker."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            )
            """
        )


def add_expense(title, amount, category, date, note=""):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
            (title, amount, category, date, note),
        )


def get_expenses(category=None):
    query = "SELECT * FROM expenses"
    params = ()
    if category:
        query += " WHERE category = ?"
        params = (category,)
    query += " ORDER BY date DESC, id DESC"
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def get_expense(expense_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()


def update_expense(expense_id, title, amount, category, date, note=""):
    with get_connection() as conn:
        conn.execute(
            "UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=?",
            (title, amount, category, date, note, expense_id),
        )


def delete_expense(expense_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def get_category_totals():
    with get_connection() as conn:
        return conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC"
        ).fetchall()
