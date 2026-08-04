import datetime as dt
import pandas as pd
import time

# Shows a professional sign-off message with version, company name, and GitHub link.
def show_info():
    return """
Goodbye, friend! Hector Capital is always here to secure your wealth.
===========================================================
                Hector Capital
===========================================================
 Powered by Hector Tech ™ © 2026  |  Version 1.0.1
===========================================================
 🔗 GitHub: https://github.com/Benyamin-Masoumi/Hector-Capital
===========================================================
           """


# This function improves the user experience (UX) of the command-line interface (CLI) by printing text gradually (line-by-line) with a typing animation.
def type_lines(text, line_delay = 0.15, char_delay = 0.015, flush = True):
    lines = text.splitlines()
    for line in lines:
        for char in line:
            print(char, end= "", flush = True)
            time.sleep(char_delay)
        print()
        time.sleep(line_delay)

class HectorCapital:
    # Initialize the Hector Capital manager with a designated CSV filename
    def __init__(self, file_name = "hector_capital_data.csv"):
        self.file_name = file_name
        self._initialize_database()

    # Private method to check if the database file exists, and create it if missing
    def _initialize_database(self):
        try:
            pd.read_csv(self.file_name)
        except FileNotFoundError:
            # Create a structured DataFrame with default headers if file is not found
            df = pd.DataFrame(columns = ["date", "type", "category", "amount", "notes"])
            df.to_csv(self.file_name, index = False)
    # Method to record either an income or an expense transaction into the database
    def add_transaction(self, trans_type, category, amount, notes):
        df = pd.read_csv(self.file_name)

        # Construct a new row containing the transaction data with today's date
        new_row = pd.DataFrame([{
            "date": dt.date.today(),
            "type": trans_type,  # income or expense
            "category": category,
            "amount": amount,
            "notes": notes
        }])

        # Append the new row and save back to the CSV file
        df = pd.concat([df, new_row], ignore_index = True)
        df.to_csv(self.file_name, index=False)

    # Method to calculate overall financial standing (income, expenses, and net balance)
    def get_financial_summary(self):
        df = pd.read_csv(self.file_name)

        # Handle case where no data has been entered yet
        if df.shape[0] == 0:
            return "No transactions recorded yet."

        # Compute totals using pandas boolean masking and summation
        total_income = df[df["type"] == "income"]["amount"].sum()
        total_expense = df[df["type"] == "expense"]["amount"].sum()
        net_balance = total_income - total_expense

        summary_msg = f"""
        =========================================
        📊 HECTOR CAPITAL - FINANCIAL SUMMARY
        =========================================
        💰 Total Income: ${total_income:,.2f}
        💸 Total Expenses: ${total_expense:,.2f}
        ⚖️ Net Balance: ${net_balance:,.2f}
        =========================================
        """
        return summary_msg

    # Method to group expenses by category and generate a structured report
    def get_category_report(self):
        df = pd.read_csv(self.file_name)
        expenses_df = df[df["type"] == "expense"]

        if expenses_df.shape[0] == 0:
            return "No expenses recorded."

        # Aggregate total expenses per category
        category_sum = expenses_df.groupby("category")["amount"].sum()

        report = "\n--- 📑 EXPENSE BREAKDOWN BY CATEGORY ---\n"
        for cat, total in category_sum.items():
            report += f"🔹 [{cat}]: ${total:,.2f}\n"
        return report
    # Method to retrieve and format the very last recorded transaction
    def recent_transaction(self):
        df = pd.read_csv(self.file_name)
        if df.shape[0] == 0:
            return "No transactions available."
        
        # Extract the last row of the dataset
        last = df.iloc[-1]
        t_type = "Income 🟢" if last["type"] == "income" else "Expense 🔴"

        return f"""
        --- RECENT TRANSACTION ---
        Date: {last['date']}
        Type: {t_type}
        Category: {last['category']}
        Amount: ${last['amount']:,.2f}
        Notes: {last['notes']}
        --------------------------
        """
# --- Main Application Loop ---
if __name__ == "__main__":
    # Instantiate the core management object
    hector = HectorCapital()
    message = "🚀 Welcome to Hector Capital Financial Management System!(Version 1.0.1)"

    # Interactive console loop
    while True:
        menu = """
-----------------------------------------
1. Add New Income 🟢
2. Add New Expense 🔴
3. View Financial Summary 📊
4. View Expense Breakdown by Category 📑
5. View Recent Transaction 🔍
6. Exit ❌
-----------------------------------------"""
        type_lines(message + menu)
        user_input = input("Enter your choice: ").strip()

        # Handle user selection for adding income
        if user_input == "1":
            category = input("Enter income category (e.g., Salary, Project): ").strip()
            try:
                amount = float(input("Enter income amount: "))
                notes = input("Enter additional notes: ").strip()
                hector.add_transaction("income", category, amount, notes)
                message = f"✅ Successfully added income of ${amount:,.2f}."
            except ValueError:
                message = "❌ Error: Please enter a valid number for the amount!"
        # Handle user selection for adding expense with validation against negative numbers
        elif user_input == "2":
            category = input("Enter expense category (e.g., Food, Transport): ").strip()
            try:
                amount = float(input("Enter expense amount: "))
                while amount < 0:
                    amount = float(input("Amount cannot be negative. Enter again: "))
                notes = input("Enter additional notes: ").strip()
                hector.add_transaction("expense", category, amount, notes)
                message = f"✅ Successfully recorded expense of ${amount:,.2f} under '{category}'."
            except ValueError:
                message = "❌ Error: Please enter a valid number for the amount!"

        # Handle viewing financial summary
        elif user_input == "3":
            message = hector.get_financial_summary()

        # Handle viewing categorized expense breakdown
        elif user_input == "4":
            message = hector.get_category_report()

        # Handle viewing the most recent transaction
        elif user_input == "5":
            message = hector.recent_transaction()

        # Exit the application loop
        elif user_input == "6":
            type_lines(show_info())
            break
        # Handle invalid inputs gracefully
        else:
            message = "❌ Invalid option! Please select a number between 1 and 6."