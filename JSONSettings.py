import json
import os

FOLDER = "settings/"
FILE = "session.json"
JSON_PATH = FOLDER + FILE

class JSONSettings:
    def __init__():
        pass
    
    @staticmethod
    def ReadFromJSON() -> list:
        try:
            fileObject = open(JSON_PATH, "r")
            jsonContent = fileObject.read()
            list = json.loads(jsonContent)
            return list
        except:
            return None
            
    @staticmethod
    def WriteCredentialsToJSON(credentials_path: str, token_path: str) -> None:
        if credentials_path is None or len(credentials_path) == 0: raise Exception("Credentials path can't be empty")
        if token_path is None or len(token_path) == 0: raise Exception("Token path can't be empty")

        # check if the folder exists
        if not os.path.exists(FOLDER):
            os.mkdir(FOLDER)    
        
        # Read existing data from the file
        existing_data = {}
        try:
            with open(JSON_PATH, "r") as jsonFile:
                existing_data = json.load(jsonFile)
        except FileNotFoundError:
            # If the file doesn't exist, ignore the error and create a new file later
            pass

        # Update or add the new credentials paths
        existing_data["CredentialsPath"] = credentials_path
        existing_data["TokenPath"] = token_path

        # Write the updated data back to the file
        with open(JSON_PATH, "w") as jsonFile:
            json.dump(existing_data, jsonFile)
        
    @staticmethod
    def WriteTimeZoneToJSON(timezone: str) -> None:
        if timezone is None or len(timezone) == 0: raise Exception("TimeZone can't be empty")

        # check if the folder exists
        if not os.path.exists(FOLDER):
            os.mkdir(FOLDER)
        
        # Read existing data from the file
        existing_data = {}
        try:
            with open(JSON_PATH, "r") as jsonFile:
                existing_data = json.load(jsonFile)
        except FileNotFoundError:
            # If the file doesn't exist, ignore the error and create a new file later
            pass

        # Update or add the new timezone
        existing_data["TimeZone"] = timezone

        # Write the updated data back to the file
        with open(JSON_PATH, "w") as jsonFile:
            json.dump(existing_data, jsonFile)