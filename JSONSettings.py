import json
import os

DIRECTORY = "settings/"
FILE = "session.json"
JSON_PATH = DIRECTORY + FILE

class JSONSettings:
    def __init__():
        pass
    
    @staticmethod
    def ReadFromJSON() -> list:
        try:
            fileObject = open(JSON_PATH, "r")
            jsonContent = fileObject.read()
            list = json.loads(jsonContent)
            fileObject.close()
            return list
        except:
            return None
            
    @staticmethod
    def WriteCredentialsToJSON(credentials_path: str, token_path: str) -> None:
        if credentials_path is None or len(credentials_path) == 0: raise ValueError("Credentials path can't be empty")
        if token_path is None or len(token_path) == 0: raise ValueError("Token path can't be empty")

        # check if directory exists
        JSONSettings.__checkIfDirectoryExists()
        
        # Read existing data from the file
        existing_data = JSONSettings.__readFromFile()

        # Update or add the new credentials paths
        existing_data["CredentialsPath"] = credentials_path
        existing_data["TokenPath"] = token_path

        # Write the updated data back to the file
        JSONSettings.__writeToFile(existing_data)
        
    @staticmethod
    def WriteTimeZoneToJSON(timezone: str) -> None:
        if timezone is None or len(timezone) == 0: raise ValueError("TimeZone can't be empty")

        # check if directory exists
        JSONSettings.__checkIfDirectoryExists()
        
        # Read existing data from the file
        existing_data = JSONSettings.__readFromFile()

        # Update or add the new timezone
        existing_data["TimeZone"] = timezone

        # Write the updated data back to the file
        JSONSettings.__writeToFile(existing_data)
            
    @staticmethod
    def WriteAppearenceToJSON(appearance: str) -> None:
        if appearance is None or len(appearance) == 0: raise ValueError("Appearance can't be empty")

        # check if directory exists
        JSONSettings.__checkIfDirectoryExists()
        
        # Read existing data from the file
        existing_data = JSONSettings.__readFromFile()

        # Update or add the new appearance
        existing_data["Appearence"] = appearance

        # Write the updated data back to the file
        JSONSettings.__writeToFile(existing_data)
            
    @staticmethod
    def WriteAppearanceToJSON(appearance: str) -> None:
        if appearance is None or len(appearance) == 0: raise ValueError("Appearance can't be empty")

        # check if directory exists
        JSONSettings.__checkIfDirectoryExists()
        
        # Read existing data from the file
        existing_data = JSONSettings.__readFromFile()

        # Update or add the new appearance
        existing_data["Appearence"] = appearance

        # Write the updated data back to the file
        JSONSettings.__writeToFile(existing_data)
            
    @staticmethod
    def WriteTextScalingToJSON(scaling: str) -> None:
        if scaling is None or len(scaling) == 0: raise ValueError("TextScaling can't be empty")

        # check if directory exists
        JSONSettings.__checkIfDirectoryExists()
        
        # Read existing data from the file
        existing_data = JSONSettings.__readFromFile()

        # Update or add the new scaling
        existing_data["TextScaling"] = scaling

        # Write the updated data back to the file
        JSONSettings.__writeToFile(existing_data)
    
    @staticmethod
    def WriteColorThemeToJSON(theme: str) -> None:
        if theme is None or len(theme) == 0: raise ValueError("ColorTheme can't be empty")

        # check if directory exists
        JSONSettings.__checkIfDirectoryExists()
        
        # Read existing data from the file
        existing_data = JSONSettings.__readFromFile()

        # Update or add the new color theme
        existing_data["ColorTheme"] = theme

        # Write the updated data back to the file
        JSONSettings.__writeToFile(existing_data)
            
    @staticmethod
    def __readFromFile() -> dict:
        existing_data = {}
        try:
            with open(JSON_PATH, "r") as jsonFile:
                existing_data = json.load(jsonFile)
        except FileNotFoundError:
            # If the file doesn't exist, ignore the error and create a new file later
            pass
        return existing_data
    
    @staticmethod
    def __writeToFile(existing_data) -> None:
        with open(JSON_PATH, "w") as jsonFile:
            json.dump(existing_data, jsonFile)  
    
    @staticmethod
    def __checkIfDirectoryExists():
        if not os.path.isdir(DIRECTORY):
            os.mkdir(DIRECTORY)