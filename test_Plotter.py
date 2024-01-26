import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO
from datetime import datetime
from Plotter import Plotter  # module name

class TestPlotter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary DataFrame for testing
        cls.test_data = pd.DataFrame({
            'ID': [1, 2, 3],
            'Summary': ['Task 1', 'Task 2', 'Task 3'],
            'Start': ['2022-01-01T10:00:00', '2022-01-01T12:00:00', '2022-01-01T14:00:00'],
            'End': ['2022-01-01T11:00:00', '2022-01-01T13:00:00', '2022-01-01T15:00:00'],
            'Duration': [1.0, 1.0, 1.0]
        })

        # Mock the read_csv method to return the test data
        cls.mock_csv_data = 'ID|Summary|Start|End|Duration\n1|Task 1|2022-01-01T10:00:00|2022-01-01T11:00:00|1.0\n2|Task 2|2022-01-01T12:00:00|2022-01-01T13:00:00|1.0\n3|Task 3|2022-01-01T14:00:00|2022-01-01T15:00:00|1.0\n'
        cls.mock_csv_file = StringIO(cls.mock_csv_data)

    def test_loadData_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            Plotter.loadData("nonexistent_file.csv")

    def test_loadData_empty_data_error(self):
        with self.assertRaises(pd.errors.EmptyDataError):
            with patch('pandas.read_csv', return_value=pd.DataFrame()):
                Plotter.loadData("existing_file.csv")

    def test_loadData_parser_error(self):
        with self.assertRaises(pd.errors.ParserError):
            with patch('pandas.read_csv', side_effect=pd.errors.ParserError()):
                Plotter.loadData("existing_file.csv")

    def test_loadData_successful(self):
        with patch('pandas.read_csv', return_value=self.test_data):
            data = Plotter.loadData("existing_file.csv")
        self.assertEqual(data.shape, self.test_data.shape)

    def test_extractTimeData(self):
        # Create a sample DataFrame with datetime format
        test_data = pd.DataFrame({
            'Start': ['2022-01-01T10:00:00'],
            'End': ['2022-01-01T11:00:00']
        })
        expected_result = pd.DataFrame({
            'Start': [datetime(2022, 1, 1, 10, 0, 0)],
            'End': [datetime(2022, 1, 1, 11, 0, 0)],
            'Year': [2022],
            'Duration': [1.0]
        })
        result = Plotter._Plotter__extractTimeData(test_data)
        pd.testing.assert_frame_equal(result, expected_result)

    # Add more test methods for other functions as needed

if __name__ == '__main__':
    unittest.main()
