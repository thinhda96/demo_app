
from typing import Any

import pandas as pd
import matplotlib.pyplot as plt


class Plot:
    @staticmethod
    def plot_monthly_transactions(data: list) -> Any:
        df = pd.DataFrame(data, columns=['transaction_date', 'transaction_amount'])
        df['transaction_amount'] = pd.to_numeric(df['transaction_amount'])
        daily_totals = df.groupby('transaction_date').sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        daily_totals.plot(kind='bar', ax=ax)
        ax.set_title('Total Transactions This Month')
        ax.set_xlabel('Date')
        ax.set_ylabel('Transaction Amount')
        return fig

    @staticmethod
    def plot_user_transactions_pie_chart(data):
        df = pd.DataFrame(data, columns=['user_id', 'transaction_amount'])
        df['transaction_amount'] = pd.to_numeric(df['transaction_amount'])
        user_totals = df.groupby('user_id').sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        user_totals.plot(kind='pie', y='transaction_amount', ax=ax, legend=False, autopct='%1.1f%%')
        ax.set_title('Total Transactions by User')
        ax.set_ylabel('')
        return fig

    @staticmethod
    def plot_spending_money_per_month(data: list) -> Any:
        df = pd.DataFrame(data, columns=['transaction_date', 'transaction_amount'])
        df['transaction_amount'] = pd.to_numeric(df['transaction_amount'])
        monthly_totals = df.groupby(pd.Grouper(key='transaction_date', freq='M')).sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_totals.plot(kind='bar', ax=ax)
        ax.set_title('Spending Money per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Spending Amount')
        return fig
