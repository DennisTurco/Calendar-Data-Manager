import json
from typing import Dict, Any


class ConfigKeys:
    class Keys:
        """A mutable keys class to mimic Enum behavior with dynamic values."""
        _keys = {
            "EVENT_COLOR": None,
            "TIMEZONE": None,
            "GOOGLE_CALENDAR_LINK": None,
            "TUTORIAL_SETUP_LINK": None,
            "GITHUB_ISSUES_LINK": None,
            "GITHUB_PAGE_LINK": None,
            "DONATE_BUYMEACOFFE_PAGE_LINK": None,
            "DONATE_PAYPAL_PAGE_LINK": None,
            "VERSION": None,
            "CONFIG_DIR": str,
            "CONFIG_FILE": str,
            "PREFERENCE_FILE": str,
            "HOMEBUTTONS_MESSAGESECTION": bool,
            "HOMEBUTTONS_GITHUB": bool,
            "HOMEBUTTONS_BUYMEACOFFE": bool,
            "HOMEBUTTONS_PAYPAL": bool,
            "MENUITEM_BUGREPORT": bool,
            "MENUITEM_EXIT": bool,
            "MENUITEM_HOME": bool,
            "MENUITEM_THEME": bool,
            "MENUITEM_SCALING": bool,
            "MENUITEM_APPEARANCE": bool,
            "MENUITEM_SHARE": bool,
            "MENUITEM_DONATE": bool,
        }

        @classmethod
        def get(cls, key: str):
            return cls._keys.get(key)

        @classmethod
        def set(cls, key: str, value: Any):
            if key in cls._keys:
                cls._keys[key] = value

        @classmethod
        def all_keys(cls) -> Dict[str, Any]:
            return cls._keys

    @staticmethod
    def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flattens a nested dictionary by concatenating keys with a separator.
        
        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string for recursion.
            sep (str): Separator to use when joining keys.
        
        Returns:
            dict: A flattened dictionary.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(ConfigKeys.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def load_and_set_keys(file_path: str):
        """
        Reads a JSON file, flattens it, and sets values in the mutable keys class.
        
        Args:
            file_path (str): Path to the JSON file.
        
        Returns:
            None
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Validate data is a dictionary
            if not isinstance(data, dict):
                raise ValueError(f"JSON file '{file_path}' must contain a dictionary at the root.")

            # Flatten the dictionary
            flat_data = ConfigKeys.flatten_dict(data)

            # Update Keys values for matching keys
            for key, value in flat_data.items():
                enum_key = key.upper().replace('.', '_')
                ConfigKeys.Keys.set(enum_key, value)

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading or processing JSON file: {e}")
            raise