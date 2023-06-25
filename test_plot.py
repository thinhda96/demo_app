import unittest
from plot import Plot
from database import Database
from config import db_config

class TestPlot(unittest.TestCase):

    def setUp(self):
        self.plot = Plot()
        self.db_instance = Database(db_config)

    def test_plot_monthly_transactions(self):
        transactions = self.db_instance.fetch_current_month_transactions()
        chart = self.plot.plot_monthly_transactions(transactions)
        self.assertIsNotNone(chart)
        self.assertEqual(chart.gca().get_title(), 'Total Transactions This Month')
        self.assertEqual(chart.gca().get_xlabel(), 'Date')
        self.assertEqual(chart.gca().get_ylabel(), 'Transaction Amount')

    def test_plot_user_transactions_pie_chart(self):
        transactions_by_user = self.db_instance.fetch_top_10_user_transactions()
        chart_user = self.plot.plot_user_transactions_pie_chart(transactions_by_user)
        self.assertIsNotNone(chart_user)
        self.assertEqual(chart_user.gca().get_title(), 'Total Transactions by User')
        self.assertEqual(chart_user.gca().get_ylabel(), '')

if __name__ == '__main__':
    unittest.main()