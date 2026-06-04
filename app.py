from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)
FILE_NAME = "expenses.csv"

def initialize_csv():
    try:
        with open(FILE_NAME, mode='x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

def get_all_expenses():
    expenses = []
    total = 0.0
    try:
        with open(FILE_NAME, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                expenses.append({
                    "date": row[0],
                    "category": row[1],
                    "amount": float(row[2]),
                    "description": row[3]
                })
                total += float(row[2])
    except FileNotFoundError:
        pass
    return expenses, total

@app.route('/')
def index():
    initialize_csv()
    expenses, total = get_all_expenses()
    # Renders the HTML page and passes data to it
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form.get('category').strip()
    amount = float(request.form.get('amount'))
    description = request.form.get('description').strip()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, f"{amount:.2f}", description])

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)