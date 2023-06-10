import mysql.connector
import pandas as pd
from datetime import datetime
from config import db_config

class Database:
    def __init__(self, config):
        self.config = config

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def query_all(self):
        cnx = self._connect()
        cursor = cnx.cursor()
        query = "SELECT * FROM transactions"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def fetch_transactions(self):
        cnx = self._connect()
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

        df = pd.DataFrame(data, columns=['transaction_date', 'transaction_amount'])
        return df

    def fetch_total_transactions_by_user(self):
        cnx = self._connect()
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

        df = pd.DataFrame(data, columns=['user_id', 'transaction_amount'])
        return df