import unittest
import json
import os
from JSONSettings import JSONSettings  # module name

DIRECTORY = "settings/"
FILE = "session.json"
JSON_PATH = DIRECTORY + FILE

class TestJSONSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up any common data needed for the tests
        cls.credentials_path = "path/to/credentials"
        cls.token_path = "path/to/token"
        cls.timezone = "UTC"

    def test_read_from_json_existing_file(self):
        # Create a sample JSON file for testing
        with open(JSON_PATH, "w") as json_file:
            json.dump({"CredentialsPath": "existing_credentials", "TokenPath": "existing_token"}, json_file)

        # Test reading from the existing JSON file
        result = JSONSettings.ReadFromJSON()
        expected_result = {"CredentialsPath": "existing_credentials", "TokenPath": "existing_token"}
        
        print(f"Actual Result: {result}")
        print(f"Expected Result: {expected_result}\n")
        
        self.assertEqual(result, expected_result)

    def test_write_credentials_to_json(self):
        # Test writing credentials to the JSON file
        JSONSettings.WriteCredentialsToJSON(self.credentials_path, self.token_path)

        # Verify the content of the JSON file
        with open(JSON_PATH, "r") as json_file:
            data = json.load(json_file)
            expected_data = {"CredentialsPath": self.credentials_path, "TokenPath": self.token_path}
            
            print(f"test_write_credentials_to_json: {expected_data}")
            
            self.assertEqual(data, expected_data)

    def test_write_timezone_to_json(self):
        # Test writing timezone to the JSON file
        JSONSettings.WriteTimeZoneToJSON(self.timezone)

        # Verify the content of the JSON file
        with open(JSON_PATH, "r") as json_file:
            data = json.load(json_file)
            expected_data = {"CredentialsPath": self.credentials_path, "TokenPath": self.token_path, "TimeZone": self.timezone}
            
            print(f"Actual result test_write_timezone_to_json: {data}")
            print(f"Expected result test_write_timezone_to_json: {expected_data}")
            
            self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()