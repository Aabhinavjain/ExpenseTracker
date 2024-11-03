import os
import csv
from datetime import datetime, timedelta

class Expense:
    def __init__(self, amount, date, category, description):
        self.amount = amount
        self.date = date
        self.category = category
        self.description = description

class Category:
    def __init__(self, name):
        self.name = name
        
class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)
        print(f"Added expense: {expense.description} - {expense.amount} on {expense.date} in {expense.category}")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        else:
            for expense in self.expenses:
                print(f"{expense.date} | {expense.category} | {expense.description} | ${expense.amount}")

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed_expense = self.expenses.pop(index)
            print(f"Deleted expense: {removed_expense.description}")
        else:
            print("Invalid index. No expense deleted.")

    def save_to_csv(self, filename=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '../data/expenses.csv')
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Date", "Category", "Description"])
            for expense in self.expenses:
                writer.writerow([expense.amount, expense.date, expense.category, expense.description])
        print(f"Expenses saved to {filename}")

    def load_from_csv(self, filename=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '../data/expenses.csv')
        try:
            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    amount, date, category, description = row
                    self.expenses.append(Expense(float(amount), date, category, description))
            print(f"Expenses loaded from {filename}")
        except FileNotFoundError:
            print(f"No previous data found. {filename} will be created upon saving.")
    def filter_by_category(self, category_name):
        """Display all expenses for a specific category."""
        filtered_expenses = [expense for expense in self.expenses if expense.category == category_name]
        if not filtered_expenses:
            print(f"No expenses found for category: {category_name}")
        else:
            print(f"Expenses for category '{category_name}':")
            for expense in filtered_expenses:
                print(f"{expense.date} | {expense.category} | {expense.description} | ${expense.amount}")
    def total_expense_by_day(self, day):
        """Display total expenses for a specific day."""
        total = sum(expense.amount for expense in self.expenses if expense.date == day)
        print(f"Total expenses for {day}: ${total}")

    def total_expense_by_week(self, start_date):
        """Display total expenses for a specific week starting from a given date."""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(days=7)
        total = sum(expense.amount for expense in self.expenses
                    if start <= datetime.strptime(expense.date, "%Y-%m-%d") < end)
        print(f"Total expenses for the week starting {start_date}: ${total}")

    def total_expense_by_month(self, month, year):
        """Display total expenses for a specific month."""
        total = sum(expense.amount for expense in self.expenses
                    if datetime.strptime(expense.date, "%Y-%m-%d").month == month and
                    datetime.strptime(expense.date, "%Y-%m-%d").year == year)
        print(f"Total expenses for {year}-{month:02d}: ${total}")

    def add_expense(self, expense):
        """Add an expense with validation checks."""
        if expense.amount <= 0:
            print("Error: Amount must be a positive number.")
            return

        try:
            datetime.strptime(expense.date, "%Y-%m-%d")
        except ValueError:
            print("Error: Date must be in the format YYYY-MM-DD.")
            return

        if not expense.category:
            print("Error: Category cannot be empty.")
            return

        self.expenses.append(expense)
        print(f"Added expense: {expense.description} - {expense.amount} on {expense.date} in {expense.category}")

    def save_to_csv(self, filename=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '../data/expenses.csv')
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Amount", "Date", "Category", "Description"])  # Header
                for expense in self.expenses:
                    writer.writerow([expense.amount, expense.date, expense.category, expense.description])
            print(f"Expenses saved to {filename}")
        except IOError as e:
            print(f"Error: Unable to save expenses to {filename}. {e}")

    def load_from_csv(self, filename=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '../data/expenses.csv')
        try:
            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    amount, date, category, description = row
                    try:
                        amount = float(amount)
                        if amount <= 0:
                            raise ValueError("Amount must be positive.")
                    except ValueError:
                        print("Error: Invalid amount found in CSV. Skipping entry.")
                        continue
                    # Add expense with valid data
                    self.expenses.append(Expense(amount, date, category, description))
            print(f"Expenses loaded from {filename}")
        except FileNotFoundError:
            print(f"No previous data found. {filename} will be created upon saving.")
        except IOError as e:
            print(f"Error: Unable to read from {filename}. {e}")

    def update_expense(self, index, amount=None, date=None, category=None, description=None):
        """Update an expense's details based on provided parameters."""
        try:
            expense = self.expenses[index]
            if amount is not None:
                if amount > 0:
                    expense.amount = amount
                else:
                    print("Error: Amount must be positive.")
        
            if date is not None:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    expense.date = date
                except ValueError:
                    print("Error: Date must be in format YYYY-MM-DD.")
        
            if category is not None:
                if category:
                    expense.category = category
                else:
                    print("Error: Category cannot be empty.")
        
            if description is not None:
                expense.description = description

            print(f"Expense updated: {expense.description} - {expense.amount} on {expense.date} in {expense.category}")
        except IndexError:
            print("Error: No expense found at the provided index.")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.load_from_csv()

    #data
    tracker.add_expense(Expense(50, "2024-11-01", "Groceries", "Bought groceries"))
    tracker.add_expense(Expense(20, "2024-11-02", "Utilities", "Paid electricity bill"))

    #Show all
    print("\nViewing all expenses:")
    tracker.view_expenses()
    print("\nUpdating expense at index 1:")
    tracker.update_expense(1, amount=25, category="Bills", description="Updated electricity bill")

    #expenses after update
    print("\nViewing all expenses after update:")
    tracker.view_expenses()
    tracker.save_to_csv()
