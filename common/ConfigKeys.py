from enum import Enum
import json

class ConfigKeys:
    class Keys(Enum):
        EVENT_COLOR = {"Light Blue": "#7986cb", "Green": "#33b679", "Purple": "#8e24aa", "Pink": "#e67c73", "Yellow": "#f6bf26", "Orange": "#f4511e", "Blue": "#039be5", "Grey": "#616161", "Dark Blue": "#3f51b5", "Dark Green": "#0b8043", "Red": "#d50000"}
        GOOGLE_CALENDAR_LINK = "https://calendar.google.com/"
        TUTORIAL_SETUP_LINK = "https://github.com/DennisTurco/Calendar-Data-Manager/blob/master/docs/GoogleCloudAPISetup.md"
        GITHUB_ISSUES_LINK = "https://github.com/DennisTurco/Calendar-Data-Manager/issues"
        GITHUB_PAGE_LINK = "https://github.com/DennisTurco/Calendar-Data-Manager"
        DONATE_BUYMEACOFFE_PAGE_LINK = "https://www.buymeacoffee.com/denno"
        DONATE_PAYPAL_PAGE_LINK = "https://www.paypal.com/donate/?hosted_button_id=M7CJXS929334U"
        SHARD_WEBSITE = "https://www.shardpc.it/"
        SHARD_EMAIL = "assistenza.shard@gmail.com"
        VERSION = "1.0.3"
        APP_WIDTH = 1100
        APP_HEIGHT = 900
        CONFIG_DIR = "./config/"
        CONFIG_FILE = "config.json"
        PREFERENCE_FILE = "preferences.json"
        LOG_FILE = "logs.log"
        GRAPH_TIMEOUT = 10
        HOMEBUTTONS_MESSAGESECTION = True
        HOMEBUTTONS_GITHUB = True
        HOMEBUTTONS_BUYMEACOFFE = True
        HOMEBUTTONS_PAYPAL = True
        MENUITEM_BUGREPORT = True
        MENUITEM_SUPPORT = True
        MENUITEM_EXIT = True
        MENUITEM_THEME = True
        MENUITEM_SCALING = True
        MENUITEM_APPEARANCE = True
        MENUITEM_SHARE = True
        MENUITEM_DONATE = True
        LOG_SERVICE_LEVEL = "INFO"
        LOG_SERVICE_MAXLINES = 1000
        LOG_SERVICE_LINESTOKEEP = 3000

        @classmethod
        def set(cls, key: str, value: bool):
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
            with open(f"{ConfigKeys.Keys.CONFIG_DIR.value}{ConfigKeys.Keys.CONFIG_FILE.value}", 'r') as file:
                data = json.load(file)  # Parse JSON file content

            ConfigKeys.Keys.set('GOOGLE_CALENDAR_LINK', data['GOOGLE_CALENDAR_LINK'])
            ConfigKeys.Keys.set('TUTORIAL_SETUP_LINK', data['TUTORIAL_SETUP_LINK'])
            ConfigKeys.Keys.set('GITHUB_ISSUES_LINK', data['GITHUB_ISSUES_LINK'])
            ConfigKeys.Keys.set('GITHUB_PAGE_LINK', data['GITHUB_PAGE_LINK'])
            ConfigKeys.Keys.set('DONATE_BUYMEACOFFE_PAGE_LINK', data['DONATE_BUYMEACOFFE_PAGE_LINK'])
            ConfigKeys.Keys.set('DONATE_PAYPAL_PAGE_LINK', data['DONATE_PAYPAL_PAGE_LINK'])
            ConfigKeys.Keys.set('SHARD_WEBSITE', data['SHARD_WEBSITE'])
            ConfigKeys.Keys.set('SHARD_EMAIL', data['SHARD_EMAIL'])
            ConfigKeys.Keys.set('VERSION', data['VERSION'])
            ConfigKeys.Keys.set('APP_WIDTH', data['APP_WIDTH'])
            ConfigKeys.Keys.set('APP_HEIGHT', data['APP_HEIGHT'])
            ConfigKeys.Keys.set('CONFIG_DIR', data['CONFIG_DIR'])
            ConfigKeys.Keys.set('PREFERENCE_FILE', data['PREFERENCE_FILE'])
            ConfigKeys.Keys.set('LOG_FILE', data['LOG_FILE'])
            ConfigKeys.Keys.set('EVENT_COLOR', data['EVENT_COLOR'])
            ConfigKeys.Keys.set('MENUITEM_BUGREPORT', data['MenuItems']['BugReport'])
            ConfigKeys.Keys.set('MENUITEM_SUPPORT', data['MenuItems']['Support'])
            ConfigKeys.Keys.set('MENUITEM_EXIT', data['MenuItems']['Exit'])
            ConfigKeys.Keys.set('MENUITEM_THEME', data['MenuItems']['Theme'])
            ConfigKeys.Keys.set('MENUITEM_SCALING', data['MenuItems']['Scaling'])
            ConfigKeys.Keys.set('MENUITEM_APPEARANCE', data['MenuItems']['Appearance'])
            ConfigKeys.Keys.set('MENUITEM_SHARE', data['MenuItems']['Share'])
            ConfigKeys.Keys.set('MENUITEM_DONATE', data['MenuItems']['Donate'])
            ConfigKeys.Keys.set('HOMEBUTTONS_MESSAGESECTION', data['HomeButtons']['MessageSection'])
            ConfigKeys.Keys.set('HOMEBUTTONS_GITHUB', data['HomeButtons']['Github'])
            ConfigKeys.Keys.set('HOMEBUTTONS_BUYMEACOFFE', data['HomeButtons']['BuyMeACoffe'])
            ConfigKeys.Keys.set('HOMEBUTTONS_PAYPAL', data['HomeButtons']['Paypal'])
            ConfigKeys.Keys.set('GRAPH_TIMEOUT', data['GraphTimeout']['value'])
            ConfigKeys.Keys.set('LOG_SERVICE_LEVEL', data['LogService']['Level'])
            ConfigKeys.Keys.set('LOG_SERVICE_MAXLINES', data['LogService']['MaxLines']['value'])
            ConfigKeys.Keys.set('LOG_SERVICE_LINESTOKEEP', data['LogService']['LinesToKeepAfterFileClear']['value'])

        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            print(f"Error loading log type values from JSON: {e}")
            raise
