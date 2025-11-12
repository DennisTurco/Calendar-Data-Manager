from googleapiclient.errors import HttpError
import pandas as pandas
from Logger import Logger

class ExceptionHandler:

    @staticmethod
    def handle_exception(common, log_box, error):
        error_map = {
            FileNotFoundError: "File not found error",
            PermissionError: "Permission error",
            ValueError: "Value error",
            KeyError: "Key error",
            HttpError: "HTTP error",
            pandas.errors.EmptyDataError: "Error, the file is empty"
        }

        common.messagebox_exception(error)

        error_type = type(error)
        base_msg = error_map.get(error_type, "Generic error")
        msg = f"{base_msg}: {str(error)}"

        Logger.write_log(msg, Logger.LogType.ERROR, error)
        common.write_log(log_box, msg)
