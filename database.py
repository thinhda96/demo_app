
import mysql.connector
import pandas as pd
from datetime import datetime
from config import db_config


class Database:
    def __init__(self, config):
        self.config = config

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def fetch_all_transactions(self) -> list:
        cnx = self._connect()
        cursor = cnx.cursor()
        query = "SELECT * FROM transactions"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def fetch_current_month_transactions(self) -> list:
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

        return data

    def fetch_top_user_transactions(self) -> list:
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
