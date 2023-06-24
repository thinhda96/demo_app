import unittest
from unittest import mock
from database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a mock config for testing
        self.mock_config = {
            "user": "test",
            "password": "test",
            "host": "localhost",
            "database": "test"
        }

        # Create a mock connection object for testing
        self.mock_cnx = mock.MagicMock()

        # Create a mock cursor object for testing
        self.mock_cursor = mock.MagicMock()

    @mock.patch("mysql.connector.connect")
    def test_fetch_all_transactions(self, mock_connect):
        # Arrange
        # Set up the mock connection and cursor objects to return expected values
        mock_connect.return_value = self.mock_cnx
        self.mock_cnx.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            (1, 1, "2021-01-01", 100),
            (2, 2, "2021-01-02", 200),
            (3, 3, "2021-01-03", 300)
        ]

        # Act
        # Create a database object with the mock config and call the method under test
        db = Database(self.mock_config)
        result = db.fetch_all_transactions()

        # Assert
        # Verify that the expected query was executed and the expected result was returned
        mock_connect.assert_called_once_with(**self.mock_config)
        self.mock_cnx.cursor.assert_called_once()
        self.mock_cursor.execute.assert_any_call("SELECT * FROM transactions")
        self.assertEqual(result, [
            (1, 1, "2021-01-01", 100),
            (2, 2, "2021-01-02", 200),
            (3, 3, "2021-01-03", 300)
        ])


    @mock.patch("mysql.connector.connect")
    def test_fetch_current_month_transactions(self, mock_connect):
        # Arrange

        # Set up the mock connection and cursor objects to return expected values
        mock_connect.return_value = self.mock_cnx
        self.mock_cnx.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            ("2021-01-01", 100),
            ("2021-01-02", 200),
            ("2021-01-03", 300)
        ]

        # Act
        # Create a database object with the mock config and call the method under test
        db = Database(self.mock_config)
        result = db.fetch_current_month_transactions()

        # Assert
        # Verify that the expected query was executed and the expected result was returned
        mock_connect.assert_called_once_with(**self.mock_config)
        self.mock_cnx.cursor.assert_called_once()
        self.assertEqual(result, [
            ("2021-01-01", 100),
            ("2021-01-02", 200),
            ("2021-01-03", 300)
        ])

    @mock.patch('mysql.connector.connect')
    def test_fetch_top_user_transactions(self, mock_connect):
        mock_cursor = mock.MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 100), (2, 200)]

        db = Database({'host': 'localhost', 'user': 'test', 'password': 'test', 'database': 'test'})
        result = db.fetch_top_10_user_transactions()

        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        self.assertEqual(result, [(1, 100), (2, 200)])


if __name__ == "__main__":
    unittest.main()
