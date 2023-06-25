
import mysql.connector
from datetime import datetime

import pandas as pd


class Database:
    def __init__(self, config):
        self.config = config

    def connect(self):
        return mysql.connector.connect(**self.config)

    def fetch_all_transactions(self) -> list:
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "SELECT * FROM transactions"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def fetch_current_month_transactions(self) -> list:
        cnx = self.connect()
        cursor = cnx.cursor()

        current_month = datetime.now().month
        current_year = datetime.now().year

        query = f"""
        SELECT transaction_date, transaction_amount
        FROM transactions
        WHERE MONTH(transaction_date) = {current_month} AND YEAR(transaction_date) = {current_year}
        """

        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return data

    def fetch_top_10_user_transactions(self) -> list:
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

    def fetch_spending_money_per_month(self) -> list:
        cnx = self._connect()
        cursor = cnx.cursor()
        query = """
        SELECT transaction_date, transaction_amount
        FROM transactions
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return data

    def insert_transactions(self, df: pd.DataFrame):
        """
        Inserts transactions from a DataFrame into the database.
        Args:
            df (pd.DataFrame): A DataFrame containing transaction data.
        """
        cnx = self.connect()
        cursor = cnx.cursor()

        for index, row in df.iterrows():
            query = f"""
            INSERT INTO transactions (user_id, product_id, transaction_date, transaction_amount, payment_method)
            VALUES ({row['user_id']}, {row['product_id']}, '{row['transaction_date']}', {row['transaction_amount']}, '{row['payment_method']}')
            """
            cursor.execute(query)

        cnx.commit()
        cursor.close()
        cnx.close()
