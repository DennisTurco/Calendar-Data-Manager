import unittest
import os
from DataEditor import DataCSV  # module name

class TestDataCSV(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up any common data needed for the tests
        cls.test_data = {
            '1': ['1', 'John', 'Doe', 'john.doe@example.com'],
            '2': ['2', 'Jane', 'Smith', 'jane.smith@example.com']
        }
        cls.test_file_path = 'test_data.csv'
        cls.delimiter = '|'
        cls.encoding_type = 'utf-8'

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources created during the tests
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

    def test_save_data_to_file(self):
        # Test saving data to a CSV file
        DataCSV.saveDataToFile(self.test_data, self.test_file_path, self.delimiter, self.encoding_type)

        # Verify the content of the CSV file
        with open(self.test_file_path, 'r', encoding=self.encoding_type) as file:
            lines = file.readlines()
            expected_lines = ['1|John|Doe|john.doe@example.com\n', '2|Jane|Smith|jane.smith@example.com\n']
            self.assertEqual(lines, expected_lines)

    def test_load_data_from_file(self):
        # Save data to the CSV file first
        DataCSV.saveDataToFile(self.test_data, self.test_file_path, self.delimiter, self.encoding_type)

        # Test loading data from the CSV file
        loaded_data = DataCSV.loadDataFromFile(self.test_file_path, self.delimiter)
        self.assertEqual(loaded_data, self.test_data)

    def test_add_data(self):
        # Add data to the existing data dictionary
        new_data_id = '3'
        new_data = ['3', 'Alice', 'Wonderland', 'alice.wonderland@example.com']
        result = DataCSV.addData(self.test_data, new_data_id, new_data)

        # Verify that data was added successfully
        self.assertTrue(result)
        self.assertIn(new_data_id, self.test_data)
        self.assertEqual(self.test_data[new_data_id], new_data)

    def test_add_existing_data(self):
        # Add existing data to the dictionary (should return False)
        existing_data_id = '1'
        existing_data = ['1', 'John', 'Doe', 'john.doe@example.com']
        result = DataCSV.addData(self.test_data, existing_data_id, existing_data)

        # Verify that data was not added (already exists)
        self.assertFalse(result)
        self.assertEqual(self.test_data[existing_data_id], existing_data)

if __name__ == '__main__':
    unittest.main()
