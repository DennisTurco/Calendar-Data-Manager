from enum import Enum
import json

from ConfigKeys import ConfigKeys

ConfigKeys.load_values_from_json()
JSON_PATH = ConfigKeys.Keys.CONFIG_DIR.value + ConfigKeys.Keys.PREFERENCE_FILE.value

class JsonProperty(Enum):
    TIMEZONE = "TimeZone"
    APPEARENCE = "Appearence"
    TOKEN = "TokenPath"
    CREDENTIALS = "CredentialsPath"
    TEXTSCALING = "TextScaling"
    COLORTHEME = "ColorTheme"

class JSONPreferences:
    @staticmethod
    def ReadFromJSON() -> list:
        try:
            fileObject = open(JSON_PATH, "r")
            jsonContent = fileObject.read()
            list = json.loads(jsonContent)
            fileObject.close()
            return list
        except:
            return []

    @staticmethod
    def WriteCredentialsToJSON(credentials_path: str, token_path: str) -> None:
        JSONPreferences.__update_json_value(credentials_path, JsonProperty.CREDENTIALS)
        JSONPreferences.__update_json_value(token_path, JsonProperty.TOKEN)

    @staticmethod
    def WriteTimeZoneToJSON(timezone: str) -> None:
        JSONPreferences.__update_json_value(timezone, JsonProperty.TIMEZONE)

    @staticmethod
    def WriteAppearanceToJSON(appearance: str) -> None:
        JSONPreferences.__update_json_value(appearance, JsonProperty.APPEARENCE)

    @staticmethod
    def WriteTextScalingToJSON(scaling: str) -> None:
        JSONPreferences.__update_json_value(scaling, JsonProperty.TEXTSCALING)

    @staticmethod
    def WriteColorThemeToJSON(theme: str) -> None:
        JSONPreferences.__update_json_value(theme, JsonProperty.COLORTHEME)

    @staticmethod
    def __update_json_value(property_value: str, property_type: JsonProperty) -> None:
        if property_value is None or len(property_value) == 0: raise ValueError(f"{property_type.name} can't be empty")

        existing_data = JSONPreferences.__read_from_file()
        existing_data[property_type.value] = property_value # add or update
        JSONPreferences.__write_to_file(existing_data)

    @staticmethod
    def __read_from_file() -> dict:
        existing_data = {}
        try:
            with open(JSON_PATH, "r") as jsonFile:
                existing_data = json.load(jsonFile)
        except FileNotFoundError:
            # If the file doesn't exist, ignore the error and create a new file later
            pass
        return existing_data

    @staticmethod
    def __write_to_file(existing_data) -> None:
        with open(JSON_PATH, "w") as jsonFile:
            json.dump(existing_data, jsonFile)
