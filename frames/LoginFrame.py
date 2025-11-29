from enums.FrameTypes import FrameTypes
import webbrowser
import os
import customtkinter as ctk
from CTkMessagebox import *

from ConfigKeys import ConfigKeys
import frames.FrameController as FrameController
from frames.BaseFrame import BaseFrame
from Images import Images
from services.EventsService import EventsService
from CommonOperations import CommonOperations

class LoginFrame(BaseFrame):
    _common = CommonOperations()

    def __init__(self, parent, main_class):
        BaseFrame.__init__(self, parent)
        self.main_class = main_class
        self.event_service = EventsService(self._common)
        img = Images()

        ctk.CTkLabel(self, text="Login", fg_color="transparent", font=("Arial", 32)).pack(padx=20, pady=20)

        google_calendar = ctk.CTkButton(master=self, image=img.google_image, text="Google Calendar", height=50, width=250, command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
        google_login = ctk.CTkButton(master=self, image=img.arrow_image, text="Login with Google", height=50, width=250, command=lambda: self.__set_credentials_path_frame())

        google_calendar.pack(padx=20, pady=10, anchor='center')
        google_login.pack(padx=20, pady=10, anchor='center')

        self.add_tooltips((google_calendar, "View and manage your Google Calendar"), (google_login, "Login using your Google account"))

    def __set_credentials_path_frame(self):
        self.__set_credentials_path()

    def __set_credentials_path(self):
        credentials_path = './settings/client.json'
        if len(credentials_path) == 0: return
        token_path = credentials_path.rsplit("/", 1)[0] + "/" + "token.json"

        try:
            credentials = self.event_service.get_connection_setup(credentials_path, token_path)
        except Exception as error:
            self._common.messagebox_exception(error)
            credentials = None

            try:
                os.remove(token_path)
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

        if credentials:
            self._common.set_credentials(credentials, credentials_path, token_path)
            self.__update_username_menu_item()
            FrameController.show_frame(FrameTypes.MainFrame, self._common)
            return

        msg = CTkMessagebox(title="Credentials error", message="Do you wish to retry?", icon="cancel", option_1="No", option_2="Yes")
        if msg.get() == "Yes":
            self.__set_credentials_path_frame()

    def __update_username_menu_item(self):
        self.main_class.update_username_menu_item()