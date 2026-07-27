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