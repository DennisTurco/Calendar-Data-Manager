from enum import Enum
import json


class ConfigKeys:
    class Keys(Enum):
        EVENT_COLOR = ""
        TIMEZONE = ""
        GOOGLE_CALENDAR_LINK = "https://calendar.google.com/"
        TUTORIAL_SETUP_LINK = "https://github.com/DennisTurco/Calendar-Data-Manager/blob/master/docs/GoogleCloudAPISetup.md"
        GITHUB_ISSUES_LINK = "https://github.com/DennisTurco/Calendar-Data-Manager/issues"
        GITHUB_PAGE_LINK = "https://github.com/DennisTurco/Calendar-Data-Manager"
        DONATE_BUYMEACOFFE_PAGE_LINK = "https://www.buymeacoffee.com/denno"
        DONATE_PAYPAL_PAGE_LINK = "https://www.paypal.com/donate/?hosted_button_id=M7CJXS929334U"
        VERSION = "1.0.3"
        APP_WIDTH = 1100
        APP_HEIGHT = 900
        CONFIG_DIR = "./config/"
        CONFIG_FILE = "config.json"
        PREFERENCE_FILE = "preferences.json"
        LOG_FILE = "logs.txt"
        GRAPH_TIMEOUT = 5
        HOMEBUTTONS_MESSAGESECTION = True
        HOMEBUTTONS_GITHUB = True
        HOMEBUTTONS_BUYMEACOFFE = True
        HOMEBUTTONS_PAYPAL = True
        MENUITEM_BUGREPORT = True
        MENUITEM_EXIT = True
        MENUITEM_HOME = True
        MENUITEM_THEME = True
        MENUITEM_SCALING = True
        MENUITEM_APPEARANCE = True
        MENUITEM_SHARE = True
        MENUITEM_DONATE = True

        @classmethod
        def _set(cls, key: str, value: bool):
            """Set the value for a given config key."""
            if key in cls.__members__:
                cls.__members__[key]._value_ = value  # Dynamically update the Enum value
            else:
                raise KeyError(f"Key '{key}' not found in ConfigKeys.Keys")

    @staticmethod
    def load_values_from_json():
        """
        Load log type values from a JSON file and update the ConfigKeys enum.
        """
        try:
            with open(ConfigKeys.Keys.CONFIG_DIR.value + ConfigKeys.Keys.CONFIG_FILE.value, 'r') as file:
                data = json.load(file)  # Parse JSON file content

            ConfigKeys.Keys._set('GOOGLE_CALENDAR_LINK', data['GOOGLE_CALENDAR_LINK'])
            ConfigKeys.Keys._set('TUTORIAL_SETUP_LINK', data['TUTORIAL_SETUP_LINK'])
            ConfigKeys.Keys._set('GITHUB_ISSUES_LINK', data['GITHUB_ISSUES_LINK'])
            ConfigKeys.Keys._set('GITHUB_PAGE_LINK', data['GITHUB_PAGE_LINK'])
            ConfigKeys.Keys._set('DONATE_BUYMEACOFFE_PAGE_LINK', data['DONATE_BUYMEACOFFE_PAGE_LINK'])
            ConfigKeys.Keys._set('DONATE_PAYPAL_PAGE_LINK', data['DONATE_PAYPAL_PAGE_LINK'])
            ConfigKeys.Keys._set('VERSION', data['VERSION'])
            ConfigKeys.Keys._set('APP_WIDTH', data['APP_WIDTH'])
            ConfigKeys.Keys._set('APP_HEIGHT', data['APP_HEIGHT'])
            ConfigKeys.Keys._set('CONFIG_DIR', data['CONFIG_DIR'])
            ConfigKeys.Keys._set('PREFERENCE_FILE', data['PREFERENCE_FILE'])
            ConfigKeys.Keys._set('LOG_FILE', data['LOG_FILE'])
            ConfigKeys.Keys._set('MENUITEM_BUGREPORT', data['MenuItems']['BugReport'])
            ConfigKeys.Keys._set('MENUITEM_EXIT', data['MenuItems']['Exit'])
            ConfigKeys.Keys._set('MENUITEM_HOME', data['MenuItems']['Home'])
            ConfigKeys.Keys._set('MENUITEM_THEME', data['MenuItems']['Theme'])
            ConfigKeys.Keys._set('MENUITEM_SCALING', data['MenuItems']['Scaling'])
            ConfigKeys.Keys._set('MENUITEM_APPEARANCE', data['MenuItems']['Appearance'])
            ConfigKeys.Keys._set('MENUITEM_SHARE', data['MenuItems']['Share'])
            ConfigKeys.Keys._set('MENUITEM_DONATE', data['MenuItems']['Donate'])
            ConfigKeys.Keys._set('HOMEBUTTONS_MESSAGESECTION', data['HomeButtons']['MessageSection'])
            ConfigKeys.Keys._set('HOMEBUTTONS_GITHUB', data['HomeButtons']['Github'])
            ConfigKeys.Keys._set('HOMEBUTTONS_BUYMEACOFFE', data['HomeButtons']['BuyMeACoffe'])
            ConfigKeys.Keys._set('HOMEBUTTONS_PAYPAL', data['HomeButtons']['Paypal'])
            ConfigKeys.Keys._set('GRAPH_TIMEOUT', data['GraphTimeout']['value']) 

        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            print(f"Error loading log type values from JSON: {e}")
            raise