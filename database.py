from datetime import datetime

import mysql.connector


class Database:
    def __init__(self, config):
        self.config = config

    def connect(self):
        return mysql.connector.connect(**self.config)

    def fetch_all_transactions(self) -> list:
        """
        Fetches all transaction records from the database and returns them as a list of tuples.
        """
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "SELECT * FROM transactions"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def fetch_current_month_transactions(self) -> list:
        """
        Fetches transaction data (date and amount) for the current month and year
        from the `transactions` table in the database.

        Returns:
            data (list): A list of tuples containing transaction_date and transaction_amount
                         for the current month and year.
        """
        cnx = self.connect()
        cursor = cnx.cursor()

        current_month = datetime.now().month
        current_year = datetime.now().year

        query = f"SELECT transaction_date, transaction_amount FROM transactions WHERE MONTH(transaction_date) = {current_month} AND YEAR(transaction_date) = {current_year}"

        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return data

    def fetch_top_user_transactions(self) -> list:
        """
        Connects to the database, retrieves the total transaction amounts for the top 10 users, and returns the data.
        The transactions are grouped by user_id and the sum of transaction amounts for each user is calculated.
        """
        cnx = self.connect()
        cursor = cnx.cursor()

        query = """
        SELECT user_id, SUM(transaction_amount) as transaction_amount
        FROM transactions
        GROUP BY user_id
        LIMIT 10
        """

        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return data
