import csv
from datetime import datetime

FILE_NAME = "expenses.csv"

def initialize_csv():
    """Creates the CSV file with headers if it doesn't exist."""
    try:
        with open(FILE_NAME, mode='x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

def add_expense():
    """Prompts user for details and appends the expense to the CSV."""
    print("\n--- Add New Expense ---")
    category = input("Enter category (e.g., Food, Transport, Rent): ").strip()
    
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number for the amount.")
            
    description = input("Enter description/notes: ").strip()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, f"{amount:.2f}", description])
        
    print("Expense added successfully!")

def view_expenses():
    """Reads and displays all expenses from the CSV."""
    print("\n--- All Expenses ---")
    try:
        with open(FILE_NAME, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) # Skip the header row
            
            expenses = list(reader)
            if not expenses:
                print("No expenses recorded yet.")
                return
                
            for row in expenses:
                print(f"[{row[0]}] {row[1]}: ${row[2]} - {row[3]}")
    except FileNotFoundError:
        print("No expenses recorded yet.")

def view_total():
    """Calculates and displays the sum of all expenses."""
    total = 0.0
    try:
        with open(FILE_NAME, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                total += float(row[2])
        print(f"\nTotal Money Spent: ${total:.2f}")
    except FileNotFoundError:
        print("\nTotal Money Spent: $0.00")

def main():
    initialize_csv()
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spend")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            view_total()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()