from googleapiclient.errors import HttpError
import pandas as pandas
from common.LogService import LogService
from common.CommonOperations import CommonOperations
import customtkinter as ctk

class ExceptionHandler:

    @staticmethod
    def handle_exception(common: CommonOperations, log_box: ctk.CTkTextbox, error: Exception):
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

        logger = LogService.get_logger(__name__)
        logger.error(msg)

        common.write_log(log_box, msg)
