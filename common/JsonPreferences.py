from enum import Enum
import json

from common.ConfigKeys import ConfigKeys

ConfigKeys.load_values_from_json()
JSON_PATH = ConfigKeys.Keys.CONFIG_DIR.value + ConfigKeys.Keys.PREFERENCE_FILE.value

class JsonProperty(Enum):
    TIMEZONE = "TimeZone"
    APPEARANCE = "Appearance"
    TOKEN = "TokenPath"
    CREDENTIALS = "CredentialsPath"
    TEXTSCALING = "TextScaling"
    COLORTHEME = "ColorTheme"

class JsonPreferences:
    @staticmethod
    def read_from_json() -> list:
        try:
            file_object = open(JSON_PATH, "r")
            json_content = file_object.read()
            data = json.loads(json_content)
            file_object.close()
            return data
        except:
            return []

    @staticmethod
    def write_credentials_to_json(credentials_path: str, token_path: str) -> None:
        JsonPreferences.__update_json_value(credentials_path, JsonProperty.CREDENTIALS)
        JsonPreferences.__update_json_value(token_path, JsonProperty.TOKEN)

    @staticmethod
    def write_time_zone_to_json(timezone: str) -> None:
        JsonPreferences.__update_json_value(timezone, JsonProperty.TIMEZONE)

    @staticmethod
    def write_appearance_to_json(appearance: str) -> None:
        JsonPreferences.__update_json_value(appearance, JsonProperty.APPEARANCE)

    @staticmethod
    def write_text_scaling_to_json(scaling: str) -> None:
        JsonPreferences.__update_json_value(scaling, JsonProperty.TEXTSCALING)

    @staticmethod
    def write_color_theme_to_json(theme: str) -> None:
        JsonPreferences.__update_json_value(theme, JsonProperty.COLORTHEME)

    @staticmethod
    def __update_json_value(property_value: str, property_type: JsonProperty) -> None:
        if property_value is None or len(property_value) == 0: raise ValueError(f"{property_type.name} can't be empty")

        existing_data = JsonPreferences.__read_from_file()
        existing_data[property_type.value] = property_value # add or update
        JsonPreferences.__write_to_file(existing_data)

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
