
import unittest
from unittest import mock
import pandas as pd
import matplotlib.pyplot as plt
from plot import Plot


class TestPlot(unittest.TestCase):

    @mock.patch("matplotlib.pyplot.subplots")
    @mock.patch("pandas.DataFrame")
    @mock.patch("pandas.to_numeric")
    def test_plot_monthly_transactions(self,mock_to_numeric, mock_dataframe, mock_subplots):
        # Arrange
        mock_data = [
            ("2021-01-01", 100),
            ("2021-01-02", 200),
            ("2021-01-03", 300)
        ]
        mock_fig = mock.MagicMock()
        mock_ax = mock.MagicMock()
        data = pd.DataFrame(mock_data, columns=['transaction_date', 'transaction_amount'])
        mock_subplots.return_value = (mock_fig, mock_ax)
        mock_dataframe.return_value = data
        mock_to_numeric.return_value = pd.to_numeric(data['transaction_amount'])
        # Act
        plot_instance = Plot()
        _ = plot_instance.plot_monthly_transactions(mock_data)
        # Assert
        mock_dataframe.assert_any_call(mock_data, columns=['transaction_date', 'transaction_amount'])
        mock_subplots.assert_called_once_with(figsize=(10, 6))

    @mock.patch("matplotlib.pyplot.subplots")
    @mock.patch("pandas.DataFrame")
    @mock.patch("pandas.to_numeric")
    def test_plot_user_transactions_pie_chart(self, mock_to_numeric, mock_dataframe, mock_subplots):
        # Arrange
        mock_data = [
            (1, 100),
            (2, 200),
            (3, 300)
        ]
        mock_fig = mock.MagicMock()
        mock_ax = mock.MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        data = pd.DataFrame(mock_data, columns=['user_id', 'transaction_amount'])
        mock_dataframe.return_value = data
        mock_to_numeric.return_value = pd.to_numeric(data['transaction_amount'])
        # Act
        plot_instance = Plot()
        _ = plot_instance.plot_user_transactions_pie_chart(mock_data)
        # Assert
        mock_dataframe.assert_any_call(mock_data, columns=['user_id', 'transaction_amount'])
        mock_subplots.assert_called_once_with(figsize=(10, 6))

if __name__ == "__main__":
    unittest.main()
