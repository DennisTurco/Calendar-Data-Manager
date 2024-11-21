from datetime import datetime
from enum import Enum
import json

from ConfigKeys import ConfigKeys

ConfigKeys.load_values_from_json()
FILE_PATH = ConfigKeys.Keys.CONFIG_DIR.value + ConfigKeys.Keys.LOG_FILE.value

class Logger:
    class LogType(Enum):
        INFO = True
        DEBUG = True
        WARN = True
        ERROR = True
        MAX_LINES = 10000
        LINES_TO_KEEP_AFTER_FILE_CLEAR = 3000

        @classmethod
        def _set(cls, key: str, value: bool):
            """Set the value for a given log type."""
            if key in cls.__members__:
                cls.__members__[key]._value_ = value  # Dynamically update the Enum value
            else:
                raise KeyError(f"Key '{key}' not found in Logger.LogType")

    @staticmethod
    def load_values_from_json():
        """
        Load log type values from a JSON file and update the LogType enum.
        """
        try:
            with open(ConfigKeys.Keys.CONFIG_DIR.value + ConfigKeys.Keys.CONFIG_FILE.value, 'r') as file:
                data = json.load(file)  # Parse JSON file content

            # Update LogType enum values
            Logger.LogType._set('INFO', data['LogService']['INFO'])
            Logger.LogType._set('DEBUG', data['LogService']['DEBUG'])
            Logger.LogType._set('WARN', data['LogService']['WARN'])
            Logger.LogType._set('ERROR', data['LogService']['ERROR'])
            Logger.LogType._set('MAX_LINES', data['LogService']['MaxLines']['value'])
            Logger.LogType._set('LINES_TO_KEEP_AFTER_FILE_CLEAR', data['LogService']['LinesToKeepAfterFileClear']['value'])

        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            print(f"Error loading log type values from JSON: {e}")
            raise

    @staticmethod
    def write_log(message: str, log_type: LogType = LogType.INFO, exception: Exception = None):
        """
        Write a log entry to the file, always adding it to the top of the log file.

        Args:
            message (str): The log message.
            log_type (Logger.LogType): The type of log (e.g., LogType.INFO, LogType.DEBUG).
            exception (Exception, optional): An exception to log, if any.
        """
        # Validate the log type
        if not isinstance(log_type, Logger.LogType):
            raise ValueError(f"Invalid log type: '{log_type}'. Allowed types: {', '.join(Logger.LogType.__members__.keys())}")

        # Check if the log type is enabled
        if not log_type.value:  # Use the `value` attribute of the Enum
            return

        # Ensure that an exception is provided if log type is ERROR
        if log_type == "ERROR" and exception is None:
            raise ValueError("For log type 'ERROR', the exception cannot be empty!")

        # Prepare the new log entry
        if exception:
            new_log_entry = f"{str(datetime.now())} [{log_type.name}] {message}: {exception}\n"  # Use `log_type.name` for string representation
        else:
            new_log_entry = f"{str(datetime.now())} [{log_type.name}] {message}\n"

        # Read existing content from the log file
        try:
            with open(FILE_PATH, "r") as file:
                existing_content = file.readlines()
        except FileNotFoundError:
            existing_content = []  # Initialize if the file doesn't exist

        # Check if we need to trim the log file
        if len(existing_content) >= Logger.LogType.MAX_LINES.value: 
            existing_content = existing_content[-Logger.LogType.LINES_TO_KEEP_AFTER_FILE_CLEAR.value:]

        # Write the new log entry to the top of the file
        with open(FILE_PATH, "w") as file:
            file.write(new_log_entry)
            file.writelines(existing_content)