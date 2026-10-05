"""app.py - main Flask application. Run with: python app.py"""
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

import database as db
from config import CATEGORIES, CURRENCY, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


def read_form():
    """Read and validate the expense form. Returns (data, error)."""
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "")
    expense_date = request.form.get("date", "")
    note = request.form.get("note", "").strip()
    try:
        amount = float(request.form.get("amount", ""))
    except ValueError:
        return None, "Amount must be a number."

    if not title:
        return None, "Title is required."
    if amount <= 0:
        return None, "Amount must be greater than zero."
    if category not in CATEGORIES:
        return None, "Please choose a valid category."
    if not expense_date:
        return None, "Date is required."
    return (title, amount, category, expense_date, note), None


@app.route("/")
def index():
    selected = request.args.get("category", "")
    expenses = db.get_expenses(selected or None)
    totals = db.get_category_totals()
    grand_total = sum(row["total"] for row in totals)
    return render_template(
        "index.html",
        expenses=expenses,
        categories=CATEGORIES,
        selected=selected,
        currency=CURRENCY,
        grand_total=grand_total,
        labels=[row["category"] for row in totals],
        values=[round(row["total"], 2) for row in totals],
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data, error = read_form()
        if error:
            flash(error, "error")
        else:
            db.add_expense(*data)
            flash("Expense added!", "success")
            return redirect(url_for("index"))
    return render_template(
        "add_expense.html", categories=CATEGORIES, today=date.today().isoformat()
    )


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):
    expense = db.get_expense(expense_id)
    if expense is None:
        flash("Expense not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        data, error = read_form()
        if error:
            flash(error, "error")
        else:
            db.update_expense(expense_id, *data)
            flash("Expense updated!", "success")
            return redirect(url_for("index"))
    return render_template("edit_expense.html", expense=expense, categories=CATEGORIES)


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    db.delete_expense(expense_id)
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=5000)
