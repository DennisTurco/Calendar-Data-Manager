from enum import Enum
import json


class ConfigKeys:
    class Keys(Enum):
        EVENT_COLOR = {"Light Blue": "#7986cb", "Green": "#33b679", "Purple": "#8e24aa", "Pink": "#e67c73", "Yellow": "#f6bf26", "Orange": "#f4511e", "Blue": "#039be5", "Grey": "#616161", "Dark Blue": "#3f51b5", "Dark Green": "#0b8043", "Red": "#d50000"}
        TIMEZONE = ['Africa/Abidjan', 'Africa/Accra', 'Africa/Algiers', 'Africa/Bissau', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/El_Aaiun', 'Africa/Juba', 'Africa/Khartoum', 'Africa/Lagos', 'Africa/Maputo', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Sao_Tome', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Asuncion', 'America/Atikokan', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Cayenne', 'America/Chicago', 'America/Chihuahua', 'America/Costa_Rica', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Fort_Nelson', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Riyadh', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faroe', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GMT', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Wake', 'Pacific/Wallis', 'UTC']
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
        LOG_FILE = "logs.txt"
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
            ConfigKeys.Keys._set('SHARD_WEBSITE', data['SHARD_WEBSITE'])
            ConfigKeys.Keys._set('SHARD_EMAIL', data['SHARD_EMAIL'])
            ConfigKeys.Keys._set('VERSION', data['VERSION'])
            ConfigKeys.Keys._set('APP_WIDTH', data['APP_WIDTH'])
            ConfigKeys.Keys._set('APP_HEIGHT', data['APP_HEIGHT'])
            ConfigKeys.Keys._set('CONFIG_DIR', data['CONFIG_DIR'])
            ConfigKeys.Keys._set('PREFERENCE_FILE', data['PREFERENCE_FILE'])
            ConfigKeys.Keys._set('LOG_FILE', data['LOG_FILE'])
            ConfigKeys.Keys._set('EVENT_COLOR', data['EVENT_COLOR'])
            ConfigKeys.Keys._set('TIMEZONE', data['TIMEZONE'])
            ConfigKeys.Keys._set('MENUITEM_BUGREPORT', data['MenuItems']['BugReport'])
            ConfigKeys.Keys._set('MENUITEM_SUPPORT', data['MenuItems']['Support'])
            ConfigKeys.Keys._set('MENUITEM_EXIT', data['MenuItems']['Exit'])
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