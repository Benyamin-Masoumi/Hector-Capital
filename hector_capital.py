import datetime as dt
import pandas as pd

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